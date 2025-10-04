"""
Visualizador de Dados para Análise de Exoplanetas
Gera gráficos e análises exploratórias dos datasets NASA
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

class ExoplanetVisualizer:
    """Classe para visualização de dados de exoplanetas"""
    
    def __init__(self):
        self.data = None
        self.features = None
        
    def load_nasa_datasets_sample(self):
        """Carrega dados de exemplo simulados baseados nos datasets NASA reais"""
        np.random.seed(42)
        
        # Simular dados realistas baseados nas características dos datasets NASA
        n_samples = 2000
        
        data = {
            # Identificadores
            'kepid': np.random.randint(1000000, 9999999, n_samples),
            'kepoi_name': [f'KIC-{1000000+i}' for i in range(n_samples)],
            
            # Disposições reais
            'koi_disposition': np.random.choice(
                ['CONFIRMED', 'CANDIDATE', 'FALSE POSITIVE'], 
                n_samples, 
                p=[0.2, 0.5, 0.3]
            ),
            
            # Parâmetros orbitais (baseados em distribuições astronômicas reais)
            'koi_period': np.random.lognormal(mean=1.5, sigma=1.5, size=n_samples),  # dias
            'koi_eccen': np.random.beta(2, 5, n_samples),  # Excentricidade
            
            # Parâmetros de trânsito
            'koi_impact': np.random.uniform(0, 1, n_samples),
            'koi_duration': np.random.gamma(2, 2, n_samples),  # horas
            'koi_depth': (
                10**(-4) * np.random.lognormal(mean=1, sigma=1, size=n_samples)
            ),  # Profundidade (%)
            
            # Parâmetros planetários
            'koi_prad': np.random.lognormal(mean=0.5, sigma=0.8, size=n_samples),  # Raios Terrestres
            'koi_mass': np.random.lognormal(mean=np.log(5.97), sigma=1.0, size=n_samples),  # kg
            'koi_density': np.random.uniform(0.5, 15, n_samples),  # g/cm³
            'koi_teq': np.random.uniform(200, 3000, n_samples),  # K
            
            # Insolação e habitabilidade
            'koi_insol': np.random.lognormal(mean=2, sigma=2, size=n_samples),
            'koi_steff': np.random.uniform(3000, 8000, n_samples),  # Temperatura estelar
            
            # Parâmetros estelares
            'koi_slogg': np.random.uniform(3.5, 5.5, n_samples),  # Log g
            'koi_smass': np.random.uniform(0.3, 3, n_samples),  # Massa solar
            'koi_srad': np.random.uniform(0.3, 5, n_samples),  # Raio solar
            'koi_kepmag': np.random.uniform(8, 16, n_samples),  # Magnitude
            
            # Probabilidade e qualidade
            'koi_maxsglerr': np.random.gamma(2, 0.1, n_samples),
            'koi_maxsnglerr': np.random.gamma(2, 0.1, n_samples),
            'koi_flag': np.random.choice([0, 1], n_samples, p=[0.7, 0.3])
        }
        
        self.data = pd.DataFrame(data)
        
        # Definir características importantes para ML
        self.features = [
            'koi_period', 'koi_impact', 'koi_duration', 'koi_depth', 
            'koi_prad', 'koi_density', 'koi_teq', 'koi_insol',
            'koi_steff', 'koi_slogg', 'koi_smass', 'koi_srad', 'koi_kepmag'
        ]
        
        return self.data
    
    def create_distribution_plots(self, data):
        """Cria gráficos de distribuição das variáveis"""
        fig, axes = plt.subplots(3, 3, figsize=(15, 12))
        axes = axes.ravel()
        
        feature_names = [
            ('koi_period', 'Período Orbital (dias)'),
            ('koi_duration', 'Duração do Trânsito (horas)'),
            ('koi_depth', 'Profundidade do Trânsito'),
            ('koi_prad', 'Raio Planetário (Terra = 1)'),
            ('koi_teq', 'Temperatura Equilibrio (K)'),
            ('koi_steff', 'Temperatura Estelar (K)'),
            ('koi_smass', 'Massa Estelar (Solar = 1)'),
            ('koi_srad', 'Raio Estelar (Solar = 1)'),
            ('koi_kepmag', 'Magnitude Kepler')
        ]
        
        for i, (feature, title) in enumerate(feature_names):
            if i < len(axes):
                axes[i].hist(data[feature], bins=30, alpha=0.7, color='skyblue', edgecolor='black')
                axes[i].set_title(title)
                axes[i].set_ylabel('Frequência')
        
        plt.tight_layout()
        return fig
    
    def create_classification_comparison(self, data):
        """Cria comparação entre classes de exoplanetas"""
        # Gráfico de dispersão condicionado pela disposição
        fig = px.scatter_matrix(
            data, 
            dimensions=['koi_period', 'koi_depth', 'koi_prad', 'koi_teq'],
            color='koi_disposition',
            title="Comparação de Variáveis por Classificação"
        )
        
        return fig
    
    def create_phase_space_plots(self, data):
        """Cria gráficos no espaço de fase de características astronômicas"""
        # Figura com subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['Period vs Radius', 'Depth vs Duration', 
                          'Temperature vs Insolation', 'Impact vs Duration'],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Period vs Radius
        fig.add_trace(
            go.Scatter(
                x=data['koi_period'], 
                y=data['koi_prad'],
                mode='markers',
                marker=dict(
                    color=data['koi_disposition'],
                    size=8,
                    opacity=0.7,
                    colorscale='viridis'
                ),
                name='Period vs Radius'
            ),
            row=1, col=1
        )
        
        # Depth vs Duration
        fig.add_trace(
            go.Scatter(
                x=data['koi_depth'], 
                y=data['koi_duration'],
                mode='markers',
                marker=dict(
                    color=data['koi_disposition'],
                    size=8,
                    opacity=0.7,
                    colorscale='plasma'
                ),
                name='Depth vs Duration'
            ),
            row=1, col=2
        )
        
        # Temperature vs Insolation
        fig.add_trace(
            go.Scatter(
                x=data['koi_teq'], 
                y=data['koi_insol'],
                mode='markers',
                marker=dict(
                    color=data['koi_disposition'],
                    size=8,
                    opacity=0.7,
                    colorscale='inferno'
                ),
                name='Temperature vs Insolation'
            ),
            row=2, col=1
        )
        
        # Impact vs Duration
        fig.add_trace(
            go.Scatter(
                x=data['koi_impact'], 
                y=data['koi_duration'],
                mode='markers',
                marker=dict(
                    color=data['koi_disposition'],
                    size=8,
                    opacity=0.7,
                    colorscale='cividis'
                ),
                name='Impact vs Duration'
            ),
            row=2, col=2
        )
        
        fig.update_layout(height=800, showlegend=False)
        
        return fig
    
    def create_correlation_heatmap(self, data):
        """Cria mapa de calor de correlações"""
        # Calcular matriz de correlação
        numeric_data = data[self.features].select_dtypes(include=[np.number])
        corr_matrix = numeric_data.corr()
        
        # Criar heatmap com Plotly
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0
        ))
        
        fig.update_layout(
            title='Matriz de Correlação das Características',
            width=800,
            height=800
        )
        
        return fig
    
    def create_class_balance_analysis(self, data):
        """Analisa o balanceamento das classes"""
        class_counts = data['koi_disposition'].value_counts()
        
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=['Distribuição das Classes', 'Proporções'],
            specs=[[{"type": "pie"}, {"type": "bar"}]]
        )
        
        # Pizza chart
        fig.add_trace(
            go.Pie(
                labels=class_counts.index,
                values=class_counts.values,
                name="Distribuição"
            ),
            row=1, col=1
        )
        
        # Bar chart
        fig.add_trace(
            go.Bar(
                x=class_counts.index,
                y=class_counts.values,
                text=class_counts.values,
                textposition='center',
                name="Contagens"
            ),
            row=1, col=2
        )
        
        fig.update_layout(height=400)
        
        return fig
    
    def create_dimensionality_reduction(self, data):
        """Mostra redução de dimensionalidade (PCA e t-SNE)"""
        # Preparar dados
        X = data[self.features].fillna(data[self.features].median())
        y = data['koi_disposition']
        
        # PCA
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X_scaled)
        
        # t-SNE
        tsne = TSNE(n_components=2, random_state=42)
        X_tsne = tsne.fit_transform(X_scaled)
        
        # Criar gráficos
        fig = make_subplots(
            rows=1, cols=2,
            subplot_titles=['PCA - Componentes Principais', 't-SNE - Embedding 2D']
        )
        
        colors = ['CONFIRMED', 'CANDIDATE', 'FALSE POSITIVE']
        color_map = {'CONFIRMED': '#2E8B57', 'CANDIDATE': '#FFA500', 'FALSE POSITIVE': '#DC143C'}
        
        for target in colors:
            mask = y == target
            
            # PCA plot
            fig.add_trace(
                go.Scatter(
                    x=X_pca[mask][:, 0],
                    y=X_pca[mask][:, 1],
                    mode='markers',
                    marker=dict(color=color_map[target], size=6, opacity=0.8),
                    name=f'{target} Burgers',
                    showlegend=i==0  # Mostrar legenda apenas na primeira iteração
                ),
                row=1, col=1
            )
            
            # t-SNE plot
            fig.add_trace(
                go.Scatter(
                    x=X_tsne[mask][:, 0],
                    y=X_tsne[mask][:, 1],
                    mode='markers',
                    marker=dict(color=color_map[target], size=6, opacity=0.8),
                    name=f'{target} Burgers',
                    showlegend=False
                ),
                row=1, col=2
            )
        
        fig.update_layout(height=500)
        
        return fig, pca.explained_variance_ratio_
    
    def generate_analysis_report(self, data):
        """Gera relatório completo de análise exploratória"""
        report = {}
        
        # Estatísticas básicas
        report['total_objects'] = len(data)
        report['features_count'] = len(self.features)
        report['missing_data'] = data[self.features].isnull().sum().sum()
        
        # Distribuição de classes
        class_dist = data['koi_disposition'].value_counts()
        report['class_distribution'] = class_dist.to_dict()
        report['class_balance'] = class_dist.min() / class_dist.max()
        
        # Correlações importantes
        numeric_data = data[self.features].select_dtypes(include=[np.number])
        corr_with_period = numeric_data.corr()['koi_period'].abs().sort_values(ascending=False)
        report['strong_correlations'] = corr_with_period.head(5).to_dict()
        
        # Valores extremos
        report['outliers_period'] = ((data['koi_period'] - data['koi_period'].median()).abs() > 3 * data['koi_period'].std()).sum()
        report['outliers_radius'] = ((data['koi_prad'] - data['koi_prad'].median()).abs() > 3 * data['koi_prad'].std()).sum()
        
        return report

def main():
    """Função principal para demonstrar o visualizador"""
    visualizer = ExoplanetVisualizer()
    
    print("🪐 Carregando dados NASA simulados...")
    data = visualizer.load_nasa_datasets_sample()
    
    print(f"📊 Dataset carregado: {len(data)} objetos analisados")
    print(f"🔬 Características analisadas: {len(visualizer.features)}")
    
    # Gerar relatório
    report = visualizer.generate_analysis_report(data)
    
    print("\n📋 RELATÓRIO DE ANÁLISE")
    print(f"Total de objetos: {report['total_objects']}")
    print(f"Dados faltantes: {report['missing_data']}")
    print(f"Balanceamento de classes: {report['class_balance']:.2f}")
    
    print("\n🎯 Distribuição por Classe:")
    for cls, count in report['class_distribution'].items():
        print(f"  {cls}: {count} ({count/report['total_objects']*100:.1f}%)")
    
    print("\n🔗 Correlações Fortes com Período Orbital:")
    for feature, corr in report['strong_correlations'].items():
        print(f"  {feature}: {corr:.3f}")
    
    print("\n✅ Visualizador pronto para uso!")
    print("Execute streamlit_app.py para ver as visualizações interativas")

if __name__ == "__main__":
    main()
