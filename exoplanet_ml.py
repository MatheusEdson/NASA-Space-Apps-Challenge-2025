"""
Sistema de Machine Learning para Detecção de Exoplanetas
Utiliza datasets da NASA (Kepler, TESS, K2)
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import xgboost as xgb
import lightgbm as lgb
from imblearn.over_sampling import SMOTE
import joblib
import requests
import json
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExoplanetDetector:
    """Classe principal para detecção de exoplanetas usando ML"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.models = {}
        self.feature_importance = {}
        self.model_performance = {}
        
    def load_nasa_data(self):
        """Carrega dados das missões NASA"""
        logger.info("Carregando dados da NASA...")
        
        # URLs dos datasets da NASA (exemplos)
        data_sources = {
            'kepler_koi': 'https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=cumulative&select=*&where=&format=csv',
            'tess_toi': 'https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=TIC&select=*&where=&format=csv'
        }
        
        datasets = {}
        
        for mission, url in data_sources.items():
            try:
                logger.info(f"Baixando dados do {mission}...")
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    datasets[mission] = pd.read_csv(url)
                    logger.info(f"Dados {mission} carregados: {len(datasets[mission])} registros")
                else:
                    logger.warning(f"Erro ao baixar {mission}: Status {response.status_code}")
            except Exception as e:
                logger.error(f"Erro ao carregar {mission}: {str(e)}")
                
        return datasets
    
    def prepare_sample_data(self):
        """Prepara dados de exemplo para demonstração"""
        logger.info("Preparando dados de exemplo...")
        
        np.random.seed(42)
        
        # Simular dados baseados nas características reais dos datasets NASA
        data = {
            'kepoi_name': [f'KIC-{1000000+i}' for i in range(1000)],
            'koi_disposition': np.random.choice(['CONFIRMED', 'CANDIDATE', 'FALSE POSITIVE'], 1000, p=[0.3, 0.4, 0.3]),
            'koi_period': np.random.lognormal(mean=1.5, sigma=1.0, size=1000),
            'koi_time0bk': np.random.uniform(100, 500, 1000),
            'koi_impact': np.random.uniform(0, 1, 1000),
            'koi_duration': np.random.uniform(0.5, 10, 1000),
            'koi_depth': np.random.uniform(0.0001, 0.01, 1000),
            'koi_prad': np.random.uniform(0.5, 20, 1000),
            'koi_teq': np.random.uniform(200, 2000, 1000),
            'koi_insol': np.random.uniform(0.1, 100, 1000),
            'koi_sep': np.random.uniform(0.01, 0.5, 1000),
            'koi_slogg': np.random.uniform(2.5, 5.0, 1000),
            'koi_smass': np.random.uniform(0.5, 2.0, 1000),
            'koi_srad': np.random.uniform(0.5, 2.0, 1000),
            'koi_kepmag': np.random.uniform(8, 16, 1000)
        }
        
        df = pd.DataFrame(data)
        logger.info(f"Dados de exemplo criados: {len(df)} registros")
        
        return df
    
    def preprocess_data(self, df):
        """Pré-processamento dos dados"""
        logger.info("Iniciando pré-processamento dos dados...")
        
        # Remove colunas não numéricas desnecessárias
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Filtra características importantes para análise de exoplanetas
        key_features = [col for col in numeric_columns if any(key in col for key in 
                       ['period', 'depth', 'duration', 'prad', 'teq', 'insol', 'impact'])]
        
        # Remove outliers usando ICR
        for col in key_features:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            ICR = Q3 - Q1
            lower_bound = Q1 - 1.5 * ICR
            upper_bound = Q3 + 1.5 * ICR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        
        # Codifica labels de destino
        if 'koi_disposition' in df.columns:
            df['target'] = self.label_encoder.fit_transform(df['koi_disposition'])
        elif 'tfowpg_disposition' in df.columns:
            df['target'] = self.label_encoder.fit_transform(df['tfowpg_disposition'])
        else:
            # Criar targets para dados de exemplo
            df['target'] = np.random.choice([0, 1, 2], len(df), p=[0.3, 0.4, 0.3])
        
        logger.info(f"Dados pré-processados: {len(df)} registros")
        
        return df, key_features
    
    def train_models(self, df, features):
        """Treina múltiplos modelos de ML"""
        logger.info("Iniciando treinamento dos modelos...")
        
        X = df[features].fillna(df[features].median())
        y = df['target']
        
        # Split dos dados
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Scaling
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Balanceamento com SMOTE
        smote = SMOTE(random_state=42)
        X_train_balanced, y_train_balanced = smote.fit_resample(X_train_scaled, y_train)
        
        # Modelos para treinar
        models = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'XGBoost': xgb.XGBClassifier(random_state=42, verbosity=0),
            'LightGBM': lgb.LGBMClassifier(random_state=42, verbosity=-1)
        }
        
        results = {}
        
        for name, model in models.items():
            logger.info(f"Treinando {name}...")
            
            # Treina modelo
            model.fit(X_train_balanced, y_train_balanced)
            
            # Avaliação
            y_pred = model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test, y_pred)
            cross_val_scores = cross_val_score(model, X_train_scaled, y_train, cv=5)
            
            # Guarda resultados
            results[name] = {
                'model': model,
                'accuracy': accuracy,
                'cross_val_mean': cross_val_scores.mean(),
                'cross_val_std': cross_val_scores.std(),
                'feature_importance': model.feature_importances_ if hasattr(model, 'feature_importances_') else None
            }
            
            self.models[name] = model
            self.feature_importance[name] = model.feature_importances_ if hasattr(model, 'feature_importances_') else None
            
            logger.info(f"{name} - Acurácia: {accuracy:.3f}, CV: {cross_val_scores.mean():.3f} ± {cross_val_scores.std():.3f}")
        
        # Salva modelos
        self.save_models()
        
        return results, X_test_scaled, y_test
    
    def predict_exoplanet(self, data_point):
        """Faz predição sobre um ponto de dados"""
        if not self.models:
            logger.error("Modelos não treinados ainda")
            return None
            
        # Escala o ponto de dados
        scaled_data = self.scaler.transform([data_point])
        
        # Predições de todos os modelos
        predictions = {}
        probabilities = {}
        
        for name, model in self.models.items():
            pred = model.predict(scaled_data)[0]
            prob = model.predict_proba(scaled_data)[0]
            
            predictions[name] = self.label_encoder.inverse_transform([pred])[0]
            probabilities[name] = dict(zip(self.label_encoder.classes_, prob))
        
        # Vote ensemble
        ensemble_pred = max(set(predictions.values()), key=list(predictions.values()).count)
        
        return {
            'ensemble_prediction': ensemble_pred,
            'individual_predictions': predictions,
            'probabilities': probabilities,
            'timestamp': datetime.now().isoformat()
        }
    
    def save_models(self):
        """Salva modelos treinados"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        for name, model in self.models.items():
            filename = f"models/{name.lower().replace(' ', '_')}_{timestamp}.joblib"
            joblib.dump(model, filename)
            logger.info(f"Modelo {name} salvo em {filename}")
    
    def load_models(self, model_path):
        """Carrega modelos salvos"""
        model = joblib.load(model_path)
        return model
    
    def get_feature_importance_df(self):
        """Retorna importância das características como DataFrame"""
        importance_data = {}
        
        for model_name, importance in self.feature_importance.items():
            importance_data[f'{model_name}_importance'] = importance
        
        if importance_data:
            return pd.DataFrame(importance_data)
        return None
    
    def get_model_performance_stats(self):
        """Retorna estatísticas de performance dos modelos"""
        stats = {
            'total_models': len(self.models),
            'training_time': datetime.now().isoformat(),
            'available_features': len(self.feature_importance[list(self.feature_importance.keys())[0]]) if self.feature_importance else 0
        }
        
        return stats

def main():
    """Função principal para demonstração"""
    detector = ExoplanetDetector()
    
    # Carrega dados de exemplo
    df = detector.prepare_sample_data()
    
    # Pré-processamento
    processed_df, features = detector.preprocess_data(df)
    
    # Treinamento
    results, X_test, y_test = detector.train_models(processed_df, features)
    
    # Exemplo de predição
    sample_data = processed_df[features].iloc[0].values
    prediction = detector.predict_exoplanet(sample_data)
    
    print("\n=== SISTEMA DE DETECÇÃO DE EXOPLANETAS ===")
    print(f"Modelos: {list(results.keys())}")
    print(f"Características utilizadas: {features}")
    print(f"\nExemplo de predição:")
    print(f"  Entrada: {sample_data}")
    print(f"  Predição: {prediction['ensemble_prediction']}")
    print(f"  Probabilidades: {prediction['probabilities']['Random Forest']}")

if __name__ == "__main__":
    main()
