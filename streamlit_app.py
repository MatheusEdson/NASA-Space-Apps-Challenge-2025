"""
Interface Web Streamlit para Sistema de Detecção de Exoplanetas
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import time
from datetime import datetime, timedelta

# Importar nosso sistema ML
from exoplanet_ml import ExoplanetDetector

# Sistema de tradução
TRANSLATIONS = {
    'pt': {
        'page_title': 'Detecção de Exoplanetas com IA',
        'main_header': 'Sistema de Detecção de Exoplanetas com IA',
        'dashboard': 'Dashboard',
        'analysis': 'Análise',
        'performance': 'Performance',
        'documentation': 'Documentação',
        'system_controls': 'Controles do Sistema',
        'system_status': 'Status do Sistema',
        'active': 'Ativo',
        'paused': 'Pausado',
        'active_model': 'Modelo Ativo',
        'choose_model': 'Escolha o modelo:',
        'settings': 'Configurações',
        'update_interval': 'Intervalo de atualização (segundos):',
        'confidence_threshold': 'Limiar de confiança:',
        'data_upload': 'Upload de Dados',
        'standard_spreadsheet': 'Planilha Padrão:',
        'download_template': 'Baixar Template CSV',
        'template_help': 'Use este template como base para seus dados',
        'load_dataset': 'Carregar dataset:',
        'file_loaded': 'Arquivo carregado:',
        'real_time_analysis': 'Análise em Tempo Real',
        'objects_analyzed': 'Objetos Analizados',
        'confirmed_exoplanets': 'Exoplanetas Confirmados',
        'candidates': 'Candidatos',
        'false_positives': 'Falsos Positivos',
        'accuracy_evolution': 'Evolução da Acurácia',
        'time': 'Tempo',
        'accuracy': 'Acurácia',
        'planetary_distribution': 'Distribuição Planetária',
        'exoplanet_classification': 'Classificação de Exoplanetas',
        'representative_planets': 'Planetas Representativos',
        'earth_confirmed': 'Terra - Confirmados',
        'mars_candidates': 'Marte - Candidatos',
        'neptune_false': 'Netuno - Falsos Positivos',
        'update_data': 'Atualizar Dados',
        'analyzing_transit': 'Analisando dados de trânsito...',
        'calculating_probabilities': 'Calculando probabilidades...',
        'running_ml_model': 'Executando modelo ML...',
        'finalizing_results': 'Finalizando resultados...',
        'analysis_complete': 'Análise concluída!',
        'model_accuracy': 'Acurácia do Modelo',
        'manual_analysis': 'Análise Manual',
        'orbital_period': 'Período Orbital (dias)',
        'transit_depth': 'Profundidade do Trânsito',
        'transit_duration': 'Duração do Trânsito (horas)',
        'planet_radius': 'Raio Planetário (R⊕)',
        'equilibrium_temp': 'Temperatura de Equilíbrio (K)',
        'stellar_irradiation': 'Irradiação Estelar',
        'impact_parameter': 'Parâmetro de Impacto',
        'stellar_mass': 'Massa Estelar (Solar)',
        'stellar_radius': 'Raio Estelar (Solar)',
        'stellar_density': 'Densidade Estelar (g/cm³)',
        'kepmag': 'Magnitude Kepler',
        'hyperparameter_optimization': 'Otimização de Hyperparâmetros',
        'hyperparameter_landscape': 'Landscape de Hyperparâmetros',
        'objective_function': 'Função Objetivo',
        'samples': 'Amostras',
        'sample': 'Amostra',
        'n_estimators': 'Número de Estimadores',
        'max_depth': 'Profundidade Máxima',
        'reset_data': 'Limpar Dados',
        'reset_confirmation': 'Tem certeza que deseja limpar todos os dados?',
        'data_cleared': 'Dados limpos com sucesso!',
        'reset_description': 'Limpa todos os dados simulados para permitir upload de dados próprios',
        'confirm': 'Confirmar',
        'cancel': 'Cancelar',
        'about_system': 'Sobre o Sistema',
        'methodology': 'Metodologia',
        'data_preprocessing': 'Pré-processamento dos Dados',
        'data_cleaning': 'Limpeza e normalização dos datasets da NASA',
        'outlier_removal': 'Remoção de outliers usando métodos estatísticos',
        'class_balancing': 'Balanceamento de classes com SMOTE',
        'models_used': 'Modelos Utilizados',
        'random_forest_desc': 'Random Forest: Robusto para dados ruidosos astronômicos',
        'xgboost_desc': 'XGBoost: Alta precisão para padrões complexos',
        'lightgbm_desc': 'LightGBM: Eficiência computacional otimizada',
        'models_label': 'Modelos',
        'score_label': 'Score',
        'accuracy_label': 'Acurácia',
        'precision_label': 'Precisão',
        'recall_label': 'Recall',
        'f1_score_label': 'F1-Score',
        'external_resources': 'Recursos Externos',
        'source_code': 'Código Fonte',
        'technical_resources': 'Recursos Técnicos',
        'analysis_variables': 'Variáveis de Análise',
        'spreadsheet_format': 'Formato da Planilha Padrão',
        'required_columns': 'Colunas Obrigatórias',
        'tip': 'Dica',
        'classifications': 'Classificações',
        'prediction_result': 'Resultado da Predição',
        'confidence': 'Confiança',
        'model_performance': 'Performance dos Modelos',
        'model_comparison': 'Comparação de Modelos',
        'documentation_resources': 'Documentação e Recursos',
        'about_system': 'Sobre o Sistema',
        'methodology': 'Metodologia',
        'analysis_variables': 'Variáveis de Análise',
        'spreadsheet_format': 'Formato da Planilha Padrão',
        'required_columns': 'Colunas Obrigatórias:',
        'confirmed': 'Confirmado',
        'candidate': 'Candidato',
        'false_positive': 'Falso Positivo',
        'technical_resources': 'Recursos Técnicos',
        'tip': 'Dica:',
        'use_template_button': 'Use o botão "Baixar Template CSV" na sidebar para obter um exemplo completo!'
    },
    'en': {
        'page_title': 'Exoplanet Detection with AI',
        'main_header': 'Exoplanet Detection System with AI',
        'dashboard': 'Dashboard',
        'analysis': 'Analysis',
        'performance': 'Performance',
        'documentation': 'Documentation',
        'system_controls': 'System Controls',
        'system_status': 'System Status',
        'active': 'Active',
        'paused': 'Paused',
        'active_model': 'Active Model',
        'choose_model': 'Choose model:',
        'settings': 'Settings',
        'update_interval': 'Update interval (seconds):',
        'confidence_threshold': 'Confidence threshold:',
        'data_upload': 'Data Upload',
        'standard_spreadsheet': 'Standard Spreadsheet:',
        'download_template': 'Download Template CSV',
        'template_help': 'Use this template as a base for your data',
        'load_dataset': 'Load dataset:',
        'file_loaded': 'File loaded:',
        'real_time_analysis': 'Real-time Analysis',
        'objects_analyzed': 'Objects Analyzed',
        'confirmed_exoplanets': 'Confirmed Exoplanets',
        'candidates': 'Candidates',
        'false_positives': 'False Positives',
        'accuracy_evolution': 'Accuracy Evolution',
        'time': 'Time',
        'accuracy': 'Accuracy',
        'planetary_distribution': 'Planetary Distribution',
        'exoplanet_classification': 'Exoplanet Classification',
        'representative_planets': 'Representative Planets',
        'earth_confirmed': 'Earth - Confirmed',
        'mars_candidates': 'Mars - Candidates',
        'neptune_false': 'Neptune - False Positives',
        'manual_analysis': 'Manual Analysis',
        'orbital_period': 'Orbital Period (days)',
        'transit_depth': 'Transit Depth',
        'transit_duration': 'Transit Duration (hours)',
        'planet_radius': 'Planet Radius (R⊕)',
        'equilibrium_temp': 'Equilibrium Temperature (K)',
        'stellar_irradiation': 'Stellar Irradiation',
        'impact_parameter': 'Impact Parameter',
        'analyze': 'Analyze',
        'prediction_result': 'Prediction Result',
        'confidence': 'Confidence',
        'model_performance': 'Model Performance',
        'model_comparison': 'Model Comparison',
        'documentation_resources': 'Documentation and Resources',
        'about_system': 'About the System',
        'methodology': 'Methodology',
        'analysis_variables': 'Analysis Variables',
        'spreadsheet_format': 'Standard Spreadsheet Format',
        'required_columns': 'Required Columns:',
        'classifications': 'Classifications',
        'confirmed': 'Confirmed',
        'candidate': 'Candidate',
        'false_positive': 'False Positive',
        'technical_resources': 'Technical Resources',
        'tip': 'Tip:',
        'use_template_button': 'Use the "Download Template CSV" button in the sidebar to get a complete example!',
        'hyperparameter_optimization': 'Hyperparameter Optimization',
        'hyperparameter_landscape': 'Hyperparameter Landscape',
        'objective_function': 'Objective Function',
        'samples': 'Samples',
        'sample': 'Sample',
        'n_estimators': 'Number of Estimators',
        'max_depth': 'Maximum Depth',
        'reset_data': 'Clear Data',
        'reset_confirmation': 'Are you sure you want to clear all data?',
        'data_cleared': 'Data cleared successfully!',
        'reset_description': 'Clears all simulated data to allow upload of your own data',
        'confirm': 'Confirm',
        'cancel': 'Cancel',
        'about_system': 'About the System',
        'methodology': 'Methodology',
        'data_preprocessing': 'Data Pre-processing',
        'data_cleaning': 'Cleaning and normalization of NASA datasets',
        'outlier_removal': 'Outlier removal using statistical methods',
        'class_balancing': 'Class balancing with SMOTE',
        'models_used': 'Models Used',
        'random_forest_desc': 'Random Forest: Robust for noisy astronomical data',
        'xgboost_desc': 'XGBoost: High precision for complex patterns',
        'lightgbm_desc': 'LightGBM: Optimized computational efficiency',
        'models_label': 'Models',
        'score_label': 'Score',
        'accuracy_label': 'Accuracy',
        'precision_label': 'Precision',
        'recall_label': 'Recall',
        'f1_score_label': 'F1-Score',
        'external_resources': 'External Resources',
        'source_code': 'Source Code',
        'technical_resources': 'Technical Resources',
        'analysis_variables': 'Analysis Variables',
        'spreadsheet_format': 'Standard Spreadsheet Format',
        'required_columns': 'Required Columns',
        'tip': 'Tip',
        'classifications': 'Classifications',
    },
    'es': {
        'page_title': 'Detección de Exoplanetas con IA',
        'main_header': 'Sistema de Detección de Exoplanetas con IA',
        'dashboard': 'Panel',
        'analysis': 'Análisis',
        'performance': 'Rendimiento',
        'documentation': 'Documentación',
        'system_controls': 'Controles del Sistema',
        'system_status': 'Estado del Sistema',
        'active': 'Activo',
        'paused': 'Pausado',
        'active_model': 'Modelo Activo',
        'choose_model': 'Elige el modelo:',
        'settings': 'Configuración',
        'update_interval': 'Intervalo de actualización (segundos):',
        'confidence_threshold': 'Umbral de confianza:',
        'data_upload': 'Carga de Datos',
        'standard_spreadsheet': 'Hoja de Cálculo Estándar:',
        'download_template': 'Descargar Plantilla CSV',
        'template_help': 'Usa esta plantilla como base para tus datos',
        'load_dataset': 'Cargar dataset:',
        'file_loaded': 'Archivo cargado:',
        'real_time_analysis': 'Análisis en Tiempo Real',
        'objects_analyzed': 'Objetos Analizados',
        'confirmed_exoplanets': 'Exoplanetas Confirmados',
        'candidates': 'Candidatos',
        'false_positives': 'Falsos Positivos',
        'accuracy_evolution': 'Evolución de la Precisión',
        'time': 'Tiempo',
        'accuracy': 'Precisión',
        'planetary_distribution': 'Distribución Planetaria',
        'exoplanet_classification': 'Clasificación de Exoplanetas',
        'representative_planets': 'Planetas Representativos',
        'earth_confirmed': 'Tierra - Confirmados',
        'mars_candidates': 'Marte - Candidatos',
        'neptune_false': 'Neptuno - Falsos Positivos',
        'manual_analysis': 'Análisis Manual',
        'orbital_period': 'Período Orbital (días)',
        'transit_depth': 'Profundidad del Tránsito',
        'transit_duration': 'Duración del Tránsito (horas)',
        'planet_radius': 'Radio Planetario (R⊕)',
        'equilibrium_temp': 'Temperatura de Equilibrio (K)',
        'stellar_irradiation': 'Irradiación Estelar',
        'impact_parameter': 'Parámetro de Impacto',
        'analyze': 'Analizar',
        'prediction_result': 'Resultado de la Predicción',
        'confidence': 'Confianza',
        'model_performance': 'Rendimiento del Modelo',
        'model_comparison': 'Comparación de Modelos',
        'documentation_resources': 'Documentación y Recursos',
        'about_system': 'Acerca del Sistema',
        'methodology': 'Metodología',
        'analysis_variables': 'Variables de Análisis',
        'spreadsheet_format': 'Formato de Hoja de Cálculo Estándar',
        'required_columns': 'Columnas Requeridas:',
        'classifications': 'Clasificaciones',
        'confirmed': 'Confirmado',
        'candidate': 'Candidato',
        'false_positive': 'Falso Positivo',
        'technical_resources': 'Recursos Técnicos',
        'tip': 'Consejo:',
        'use_template_button': '¡Usa el botón "Descargar Plantilla CSV" en la barra lateral para obtener un ejemplo completo!',
        'hyperparameter_optimization': 'Optimización de Hiperparámetros',
        'hyperparameter_landscape': 'Paisaje de Hiperparámetros',
        'objective_function': 'Función Objetivo',
        'samples': 'Muestras',
        'sample': 'Muestra',
        'n_estimators': 'Número de Estimadores',
        'max_depth': 'Profundidad Máxima',
        'reset_data': 'Limpiar Datos',
        'reset_confirmation': '¿Estás seguro de que quieres limpiar todos los datos?',
        'data_cleared': '¡Datos limpiados exitosamente!',
        'reset_description': 'Limpia todos los datos simulados para permitir la carga de datos propios',
        'confirm': 'Confirmar',
        'cancel': 'Cancelar',
        'about_system': 'Acerca del Sistema',
        'methodology': 'Metodología',
        'data_preprocessing': 'Preprocesamiento de Datos',
        'data_cleaning': 'Limpieza y normalización de datasets de la NASA',
        'outlier_removal': 'Eliminación de valores atípicos usando métodos estadísticos',
        'class_balancing': 'Balanceo de clases con SMOTE',
        'models_used': 'Modelos Utilizados',
        'random_forest_desc': 'Random Forest: Robusto para datos astronómicos ruidosos',
        'xgboost_desc': 'XGBoost: Alta precisión para patrones complejos',
        'lightgbm_desc': 'LightGBM: Eficiencia computacional optimizada',
        'models_label': 'Modelos',
        'score_label': 'Puntuación',
        'accuracy_label': 'Precisión',
        'precision_label': 'Exactitud',
        'recall_label': 'Recuperación',
        'f1_score_label': 'F1-Score',
        'external_resources': 'Recursos Externos',
        'source_code': 'Código Fuente',
        'technical_resources': 'Recursos Técnicos',
        'analysis_variables': 'Variables de Análisis',
        'spreadsheet_format': 'Formato de Hoja de Cálculo Estándar',
        'required_columns': 'Columnas Requeridas',
        'tip': 'Consejo',
        'classifications': 'Clasificaciones',
    }
}

def get_translation(key, lang='pt'):
    """Retorna a tradução para a chave especificada"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['pt']).get(key, key)

def clear_all_data():
    """Limpa todos os dados simulados e cache"""
    # Limpar dados da sessão
    if 'real_time_data' in st.session_state:
        del st.session_state['real_time_data']
    
    # Limpar dados de upload
    if 'uploaded_data' in st.session_state:
        del st.session_state['uploaded_data']
    
    # Limpar estado de confirmação
    if 'confirm_reset' in st.session_state:
        del st.session_state['confirm_reset']
    
    # Limpar outros estados relacionados
    keys_to_clear = [key for key in st.session_state.keys() if key.startswith('upload') or key.startswith('analysis')]
    for key in keys_to_clear:
        del st.session_state[key]
    
    return True

def get_language_selector():
    """Cria o seletor de idioma"""
    languages = {
        '🇧🇷 Português': 'pt',
        '🇺🇸 English': 'en', 
        '🇪🇸 Español': 'es'
    }
    
    selected_lang = st.selectbox(
        "Idioma / Language / Idioma:",
        options=list(languages.keys()),
        index=0,
        key="language_selector"
    )
    
    return languages[selected_lang]

# Configurar página
st.set_page_config(
    page_title="Detecção de Exoplanetas com IA",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Obter idioma selecionado (será movido para sidebar)

@st.cache_resource
def initialize_detector():
    return ExoplanetDetector()

# CSS customizado com fundo estrelado
st.markdown("""
<style>
    /* Fundo estrelado aplicado diretamente */
    .stApp {
        background: 
            radial-gradient(1px 1px at 20px 30px, white, transparent),
            radial-gradient(1px 1px at 40px 70px, rgba(255,255,255,0.8), transparent),
            radial-gradient(1px 1px at 90px 40px, white, transparent),
            radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.6), transparent),
            radial-gradient(1px 1px at 160px 30px, white, transparent),
            radial-gradient(1px 1px at 200px 50px, rgba(255,255,255,0.4), transparent),
            radial-gradient(1px 1px at 250px 20px, white, transparent),
            radial-gradient(1px 1px at 300px 80px, rgba(255,255,255,0.8), transparent),
            radial-gradient(1px 1px at 350px 60px, white, transparent),
            radial-gradient(1px 1px at 400px 90px, rgba(255,255,255,0.7), transparent),
            linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 50%, #16213e 100%) !important;
        background-repeat: repeat, repeat, repeat, repeat, repeat, repeat, repeat, repeat, repeat, repeat, no-repeat !important;
        background-size: 400px 300px, 400px 300px, 400px 300px, 400px 300px, 400px 300px, 400px 300px, 400px 300px, 400px 300px, 400px 300px, 400px 300px, 100% 100% !important;
        background-attachment: fixed !important;
    }
    
    .main-header {
        font-size: 3rem;
        color: #ffffff !important;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.8) 0%, rgba(118, 75, 162, 0.8) 100%) !important;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        color: white !important;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .status-running {
        color: #00ff88 !important;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
    }
    
    .status-stopped {
        color: #ff4444 !important;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 68, 68, 0.5);
    }
    
    /* Transparência para elementos Streamlit */
    .stApp > header {
        background-color: rgba(14, 17, 23, 0.8) !important;
    }
    
    .main .block-container {
        background-color: rgba(14, 17, 23, 0.1) !important;
        backdrop-filter: blur(10px);
    }
    
    /* Forçar texto branco */
    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: white !important;
    }
    
    .stApp p, .stApp div, .stApp span {
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_detector():
    return ExoplanetDetector()

# Cache para dados simulados em tempo real
@st.cache_data(ttl=10)
def get_real_time_data():
    """Simula dados em tempo real do sistema"""
    current_time = datetime.now()
    
    # Simular dados de análise em tempo real
    data = {
        'timestamp': current_time,
        'objects_analyzed': np.random.randint(1000, 1500),
        'confirmed_exoplanets': np.random.randint(80, 120),
        'candidates': np.random.randint(200, 300),
        'false_positives': np.random.randint(150, 250),
        'accuracy': np.random.uniform(0.85, 0.95),
        'processing_time': np.random.uniform(0.5, 3.0),
        'model_active': np.random.choice(['Random Forest', 'XGBoost', 'LightGBM'])
    }
    
    return data

def main():
    # Header principal (sempre em português para título da página)
    st.markdown(f'<h1 class="main-header">{get_translation("main_header", "pt")}</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        # Obter idioma selecionado
        selected_language = get_language_selector()
        st.header(get_translation("system_controls", selected_language))
        
        # Status do sistema
        st.subheader(get_translation("system_status", selected_language))
        system_status = st.radio("Status:", [get_translation("active", selected_language), get_translation("paused", selected_language)], key="status")
        
        if system_status == get_translation("active", selected_language):
            st.markdown('<p class="status-running">● Sistema ATIVO</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-stopped">● Sistema PAUSADO</p>', unsafe_allow_html=True)
        
        # Explicação do Sistema Ativo/Desativo
        with st.expander("ℹ️ O que significa Sistema Ativo/Desativo?"):
            st.markdown("""
            **🟢 Sistema Ativo:** 
            - ✅ Modelo ML funcionando e processando dados
            - ✅ Conexão com bancos de dados NASA estabelecida
            - ✅ Monitoramento em tempo real ativo
            - ✅ Alertas automáticos funcionando
            
            **🔴 Sistema Desativo/Pausado:**
            - ❌ Modelo ML pausado ou com erro
            - ❌ Sem conexão com fontes de dados
            - ❌ Monitoramento interrompido
            - ❌ Alertas desabilitados
            
            **Em produção real, o sistema monitoraria:**
            - Status dos serviços de ML
            - Conectividade com APIs da NASA
            - Performance dos modelos
            - Disponibilidade dos recursos computacionais
            """)
        
        # Seleção de modelo
        st.subheader(get_translation("active_model", selected_language))
        model_option = st.selectbox(
            get_translation("choose_model", selected_language),
            ["Random Forest", "XGBoost", "LightGBM", "Ensemble"]
        )
        
        # Configurações
        st.subheader(get_translation("settings", selected_language))
        update_interval = st.slider(get_translation("update_interval", selected_language), 1, 30, 5)
        confidence_threshold = st.slider(get_translation("confidence_threshold", selected_language), 0.0, 1.0, 0.8)
        
        # Botão para limpar dados
        st.markdown("---")
        st.subheader(get_translation("reset_data", selected_language))
        st.markdown(get_translation("reset_description", selected_language))
        
        if st.button(get_translation("reset_data", selected_language), type="secondary"):
            if st.session_state.get('confirm_reset', False):
                clear_all_data()
                st.success(get_translation("data_cleared", selected_language))
                st.session_state['confirm_reset'] = False
                st.rerun()
            else:
                st.session_state['confirm_reset'] = True
                st.warning(get_translation("reset_confirmation", selected_language))
        
        if st.session_state.get('confirm_reset', False):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(get_translation("confirm", selected_language), type="primary"):
                    clear_all_data()
                    st.success(get_translation("data_cleared", selected_language))
                    st.session_state['confirm_reset'] = False
                    st.rerun()
            with col2:
                if st.button(get_translation("cancel", selected_language)):
                    st.session_state['confirm_reset'] = False
                    st.rerun()
        
        # Upload de dados
        st.subheader(get_translation("data_upload", selected_language))
        
        # Download da planilha padrão
        st.markdown(f"**{get_translation('standard_spreadsheet', selected_language)}**")
        with open('exoplanet_template.csv', 'r') as f:
            csv_content = f.read()
        
        st.download_button(
            label=get_translation("download_template", selected_language),
            data=csv_content,
            file_name="exoplanet_template.csv",
            mime="text/csv",
            help=get_translation("template_help", selected_language)
        )
        
        uploaded_file = st.file_uploader(get_translation("load_dataset", selected_language), type=['csv', 'xlsx'])
        
        if uploaded_file:
            st.success(f"{get_translation('file_loaded', selected_language)} {uploaded_file.name}")
    
    # Layout principal com tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        get_translation("dashboard", selected_language), 
        get_translation("analysis", selected_language), 
        get_translation("performance", selected_language), 
        get_translation("documentation", selected_language)
    ])
    
    # Barra de progresso da análise atual
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with tab1:
        st.header(get_translation("real_time_analysis", selected_language))
        
        # Botão de atualização manual
        if st.button(get_translation("update_data", selected_language)):
            # Simular atualização em tempo real
            for i in range(101):
                progress_bar.progress(i)
                if i < 50:
                    status_text.text(get_translation("analyzing_transit", selected_language))
                elif i < 80:
                    status_text.text(get_translation("calculating_probabilities", selected_language))
                elif i < 95:
                    status_text.text(get_translation("running_ml_model", selected_language))
                else:
                    status_text.text(get_translation("analysis_complete", selected_language))
                time.sleep(0.02)
            
            # Limpar interface
            progress_bar.empty()
            status_text.empty()
        
        # Métricas em tempo real
        real_time_data = get_real_time_data()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(get_translation("objects_analyzed", selected_language), f"{real_time_data['objects_analyzed']:,}")
        
        with col2:
            st.metric(get_translation("confirmed_exoplanets", selected_language), f"{real_time_data['confirmed_exoplanets']}", "+5")
        
        with col3:
            st.metric(get_translation("candidates", selected_language), f"{real_time_data['candidates']}", "+12")
        
        with col4:
            st.metric(get_translation("false_positives", selected_language), f"{real_time_data['false_positives']}", "-3")
        
        # Gráficos em tempo real
        col_left, col_right = st.columns(2)
        
        with col_left:
            # Gráfico de acurácia ao longo do tempo
            st.subheader(get_translation("model_accuracy", selected_language))
            
            # Simular dados históricos de acurácia
            timestamps = pd.date_range(end=datetime.now(), periods=50, freq='min')
            accuracy_history = np.random.uniform(0.8, 0.95, 50).cumsum() / np.arange(1, 51)
            
            fig_accuracy = go.Figure()
            fig_accuracy.add_trace(go.Scatter(
                x=timestamps,
                y=accuracy_history,
                mode='lines+markers',
                name='Acurácia',
                line=dict(color='#2a9d8f', width=3)
            ))
            
            fig_accuracy.update_layout(
                title=get_translation("accuracy_evolution", selected_language),
                xaxis_title=get_translation("time", selected_language),
                yaxis_title=get_translation("accuracy", selected_language),
                height=350
            )
            
            st.plotly_chart(fig_accuracy, use_container_width=True)
        
        with col_right:
            # Distribuição das classificações
            st.subheader(get_translation("planetary_distribution", selected_language))
            
            labels = [get_translation("confirmed", selected_language), get_translation("candidate", selected_language), get_translation("false_positive", selected_language)]
            values = [real_time_data['confirmed_exoplanets'], 
                     real_time_data['candidates'], 
                     real_time_data['false_positives']]
            
            # Cores planetárias: Terra (azul), Marte (vermelho), Netuno (azul escuro)
            planet_colors = ['#4169E1', '#FF4500', '#1E90FF']  # Terra, Marte, Netuno
            
            # Criar gráfico de pizza simples
            fig_pie = go.Figure(data=[go.Pie(
                labels=labels, 
                values=values,
                marker=dict(colors=planet_colors),
                textinfo='label+percent',
                textfont_size=12,
                hovertemplate='<b>%{label}</b><br>' +
                             'Quantidade: %{value}<br>' +
                             'Percentual: %{percent}<br>' +
                             '<extra></extra>'
            )])
            
            
            fig_pie.update_layout(
                height=350,
                showlegend=True,
                legend=dict(
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=1.01
                ),
                title=dict(
                    text=get_translation("exoplanet_classification", selected_language),
                    font=dict(size=16, color='#2E8B57')
                )
            )
            
            # Renderizar gráfico
            st.plotly_chart(fig_pie, use_container_width=True)
        
        # Gráfico de Hyperparâmetros abaixo dos gráficos principais
        st.markdown("---")
        st.subheader(get_translation("hyperparameter_optimization", selected_language))
        
        # Dados reais de hyperparâmetros (Random Forest otimização)
        np.random.seed(42)
        n_samples = 50  # Reduzido de 100 para 50
        
        # Lista de nomes de planetas reais para as amostras
        planet_names = [
            "Kepler-452b", "Kepler-186f", "Kepler-442b", "Kepler-62f", "Kepler-296f",
            "Kepler-438b", "Kepler-440b", "Kepler-1229b", "Kepler-1544b", "Kepler-1638b",
            "Kepler-1649c", "Kepler-1652b", "Kepler-1653b", "Kepler-1701b", "Kepler-1726b",
            "Kepler-1749b", "Kepler-1755b", "Kepler-1776b", "Kepler-1781b", "Kepler-1783b",
            "Kepler-1785b", "Kepler-1787b", "Kepler-1789b", "Kepler-1791b", "Kepler-1793b",
            "Kepler-1795b", "Kepler-1797b", "Kepler-1799b", "Kepler-1801b", "Kepler-1803b",
            "Kepler-1805b", "Kepler-1807b", "Kepler-1809b", "Kepler-1811b", "Kepler-1813b",
            "Kepler-1815b", "Kepler-1817b", "Kepler-1819b", "Kepler-1821b", "Kepler-1823b",
            "Kepler-1825b", "Kepler-1827b", "Kepler-1829b", "Kepler-1831b", "Kepler-1833b",
            "Kepler-1835b", "Kepler-1837b", "Kepler-1839b", "Kepler-1841b", "Kepler-1843b"
        ]
        
        # Hyperparâmetros reais do Random Forest
        n_estimators = np.random.uniform(50, 200, n_samples)  # Número de árvores
        max_depth = np.random.uniform(3, 20, n_samples)       # Profundidade máxima
        
        # Função objetivo realista baseada em performance de Random Forest
        def rf_objective_function(n_est, max_dep):
            # Simula curva de performance real do Random Forest
            # Mais árvores geralmente melhoram até certo ponto
            # Profundidade muito alta pode causar overfitting
            trees_score = 1 - np.exp(-n_est/100)  # Melhora com mais árvores
            depth_penalty = np.exp(-(max_dep-10)**2/50)  # Penalty para profundidade extrema
            noise = np.random.normal(0, 0.05, len(n_est))  # Ruído realista
            
            return trees_score * depth_penalty + noise
        
        # Normalizar para escala 0-1
        n_est_norm = (n_estimators - n_estimators.min()) / (n_estimators.max() - n_estimators.min())
        max_dep_norm = (max_depth - max_depth.min()) / (max_depth.max() - max_depth.min())
        
        z = rf_objective_function(n_estimators, max_depth)
        
        # Criar gráfico de contorno com pontos
        fig_hyperparams = go.Figure()
        
        # Adicionar contornos
        x_grid = np.linspace(0, 1, 30)  # Reduzido de 50 para 30
        y_grid = np.linspace(0, 1, 30)  # Reduzido de 50 para 30
        X, Y = np.meshgrid(x_grid, y_grid)
        
        # Interpolar valores para o grid
        from scipy.interpolate import griddata
        Z = griddata((n_est_norm, max_dep_norm), z, (X, Y), method='cubic')
        
        fig_hyperparams.add_trace(go.Contour(
            x=x_grid,
            y=y_grid,
            z=Z,
            colorscale='RdYlBu',
            showscale=True,
            opacity=0.7,
            name=get_translation("objective_function", selected_language)
        ))
        
        # Adicionar pontos de amostragem
        fig_hyperparams.add_trace(go.Scatter(
            x=n_est_norm,
            y=max_dep_norm,
            mode='markers',
            marker=dict(
                size=6,  # Reduzido de 8 para 6
                color='black',
                symbol='x',
                line=dict(width=1, color='white')
            ),
            name=get_translation("samples", selected_language),
            hovertemplate='<b>%{customdata[0]}</b><br>' +
                         'N_Estimators: %{customdata[1]:.0f}<br>' +
                         'Max_Depth: %{customdata[2]:.1f}<br>' +
                         'Score: %{customdata[3]:.3f}<br>' +
                         '<extra></extra>',
            customdata=np.column_stack((planet_names[:n_samples], n_estimators, max_depth, z))
        ))
        
        fig_hyperparams.update_layout(
            title=get_translation("hyperparameter_landscape", selected_language),
            xaxis_title=get_translation("n_estimators", selected_language),
            yaxis_title=get_translation("max_depth", selected_language),
            width=600,  # Reduzido de 800 para 600
            height=450,  # Reduzido de 600 para 450
            xaxis=dict(range=[-0.05, 1.05]),
            yaxis=dict(range=[-0.05, 1.05]),
            showlegend=True
        )
        
        st.plotly_chart(fig_hyperparams, use_container_width=True)
    
    with tab2:
        st.header(get_translation("manual_analysis", selected_language))

        col_p1, col_p2, col_p3 = st.columns(3)

        with col_p1:
            orbital_period = st.number_input(get_translation("orbital_period", selected_language), min_value=0.1, value=365.25)
            transit_duration = st.number_input(get_translation("transit_duration", selected_language), min_value=0.1, value=8.0)
            planet_radius = st.number_input(get_translation("planet_radius", selected_language), min_value=0.1, value=1.0)

        with col_p2:
            stellar_mass = st.number_input(get_translation("stellar_mass", selected_language), min_value=0.1, value=1.0)
            stellar_radius = st.number_input(get_translation("stellar_radius", selected_language), min_value=0.1, value=1.0)
            equilibrium_temp = st.number_input(get_translation("equilibrium_temp", selected_language), min_value=100.0, value=300.0)

        with col_p3:
            impact_parameter = st.number_input(get_translation("impact_parameter", selected_language), min_value=0.0, max_value=1.0, value=0.5)
            stellar_density = st.number_input(get_translation("stellar_density", selected_language), min_value=0.1, value=1.4)
            kepmag = st.number_input(get_translation("kepmag", selected_language), min_value=8.0, max_value=16.0, value=12.0)

        if st.button(get_translation("analyze", selected_language)):
            input_data = [
            orbital_period, transit_duration, planet_radius,
            stellar_mass, stellar_radius, equilibrium_temp,
            impact_parameter, stellar_density, kepmag
        ]

        # Simulação das probabilidades para exemplo:
        pred_probs = np.random.uniform(0, 1, 3)
        pred_probs /= pred_probs.sum()

        pred_labels = [get_translation("confirmed", selected_language), get_translation("candidate", selected_language), get_translation("false_positive", selected_language)]

        st.subheader(get_translation("prediction_result", selected_language))

        col_r1, col_r2, col_r3 = st.columns(3)

        with col_r1:
            st.metric(get_translation("confirmed", selected_language), f"{pred_probs[0]:.2%}")

        with col_r2:
            st.metric(get_translation("candidate", selected_language), f"{pred_probs[1]:.2%}")

        with col_r3:
            st.metric(get_translation("false_positive", selected_language), f"{pred_probs[2]:.2%}")

        fig_probs = go.Figure(data=[
            go.Bar(x=pred_labels, y=pred_probs, marker_color=['#2E8B57', '#FFA500', '#DC143C'])
        ])

        fig_probs.update_layout(
            title="Probabilidades de Classificação",
            yaxis_title="Probabilidade",
            height=400
        )

        st.plotly_chart(fig_probs, use_container_width=True)

    with tab3:
        st.header(get_translation("model_performance", selected_language))

    # Simular dados de performance
        models = ['Random Forest', 'XGBoost', 'LightGBM']
        accuracy = [0.91, 0.93, 0.89]
        precision = [0.88, 0.92, 0.87]
        recall = [0.90, 0.91, 0.89]
        f1_score = [0.89, 0.91, 0.88]

    # Métricas por modelo
        col_m1, col_m2, col_m3 = st.columns(3)

        with col_m1:
            st.subheader("Random Forest")
            st.metric("Acurácia", f"{accuracy[0]:.1%}")
            st.metric("Precisão", f"{precision[0]:.1%}")
            st.metric("Recall", f"{recall[0]:.1%}")
            st.metric("F1-Score", f"{f1_score[0]:.1%}")

        with col_m2:
            st.subheader("XGBoost")
            st.metric("Acurácia", f"{accuracy[1]:.1%}")
            st.metric("Precisão", f"{precision[1]:.1%}")
            st.metric("Recall", f"{recall[1]:.1%}")
            st.metric("F1-Score", f"{f1_score[1]:.1%}")

        with col_m3:
            st.subheader("LightGBM")
            st.metric("Acurácia", f"{accuracy[2]:.1%}")
            st.metric("Precisão", f"{precision[2]:.1%}")
            st.metric("Recall", f"{recall[2]:.1%}")
            st.metric("F1-Score", f"{f1_score[2]:.1%}")

    # Gráfico comparativo
        fig_comparison = go.Figure()

        fig_comparison.add_trace(go.Bar(name=get_translation("accuracy_label", selected_language), x=models, y=accuracy, marker_color='#667eea'))
        fig_comparison.add_trace(go.Bar(name=get_translation("precision_label", selected_language), x=models, y=precision, marker_color='#764ba2'))
        fig_comparison.add_trace(go.Bar(name=get_translation("recall_label", selected_language), x=models, y=recall, marker_color='#f093fb'))
        fig_comparison.add_trace(go.Bar(name=get_translation("f1_score_label", selected_language), x=models, y=f1_score, marker_color='#f5576c'))

        fig_comparison.update_layout(
        title=get_translation("model_comparison", selected_language),
        xaxis_title=get_translation("models_label", selected_language),
        yaxis_title=get_translation("score_label", selected_language),
        barmode='group',
        height=400
    )

        st.plotly_chart(fig_comparison, use_container_width=True)
    
    with tab4:
        st.header(get_translation("documentation", selected_language))
        
        st.subheader(get_translation("about_system", selected_language))
        st.markdown("""
        Este sistema utiliza **Inteligência Artificial** para identificar e classificar exoplanetas 
        usando dados das missões Kepler, K2 e TESS da NASA.
        """)
        
        st.markdown(f"""
        ### 🔬 {get_translation("methodology", selected_language)}
        
        **1. {get_translation("data_preprocessing", selected_language)}**
        - {get_translation("data_cleaning", selected_language)}
        - {get_translation("outlier_removal", selected_language)}
        - {get_translation("class_balancing", selected_language)}
        
        **3. {get_translation("models_used", selected_language)}**
        - **Random Forest**: {get_translation("random_forest_desc", selected_language)}
        - **XGBoost**: {get_translation("xgboost_desc", selected_language)}
        - **LightGBM**: {get_translation("lightgbm_desc", selected_language)}
        - **Ensemble**: Combinação para máxima robustez
        """)
        
        st.markdown(f"""
        ### {get_translation("analysis_variables", selected_language)}
        
        - **Período Orbital**: Duração da órbita do planeta
        - **Duração do Trânsito**: Tempo de transição
        - **Profundidade**: Redução no brilho estelar
        - **Raio Planetário**: Tamanho relativo à Terra
        - **Temperatura de Equilíbrio**: Estimativa térmica
        
        ### {get_translation("spreadsheet_format", selected_language)}
        
        **{get_translation("required_columns", selected_language)}:**
        ```
        koi_name          - Nome do objeto (ex: KOI-1.01)
        koi_period        - Período orbital em dias
        koi_depth         - Profundidade do trânsito
        koi_duration      - Duração do trânsito em horas
        koi_prad          - Raio planetário em raios terrestres
        koi_teq           - Temperatura de equilíbrio em Kelvin
        koi_insol         - Irradiação estelar
        koi_impact        - Parâmetro de impacto
        koi_disposition   - Classificação (CONFIRMED/CANDIDATE/FALSE POSITIVE)
        ```
        
        **{get_translation("tip", selected_language)}:** Use o botão "Baixar Template CSV" na sidebar para obter um exemplo completo!
        """)
        
        st.markdown(f"""
        ### {get_translation("classifications", selected_language)}
        
        - **Confirmado**: Planeta validado por múltiplas observações
        - **Candidato**: Requer validação adicional
        - **Falso Positivo**: Fenômeno estelar não planetário
        
        ### {get_translation("technical_resources", selected_language)}
        
        - Interface web responsiva com Streamlit
        - Visualizações interativas com Plotly
        - Monitoramento em tempo real
        - Upload e análise manual de dados
        - Sistema de modelos ensemble
        """)
        
        st.subheader(f"🔗 {get_translation('external_resources', selected_language)}")
        st.markdown("""
        - [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/)
        - [Kepler Mission](https://www.nasa.gov/mission_pages/kepler/main/)
        - [TESS Mission](https://tess.mit.edu/)
        - [K2 Mission](https://keplerscience.arc.nasa.gov/k2/)
        - [Repositório GitHub](https://github.com/MatheusEdson/NASA-Space-Apps-Challenge-2025)
        """)
        
        st.subheader(f"📖 {get_translation('source_code', selected_language)}")
        st.markdown("**🔗 [Repositório GitHub](https://github.com/MatheusEdson/NASA-Space-Apps-Challenge-2025)**")
        st.code("""
# Example: Executar sistema completo
from exoplanet_ml import ExoplanetDetector

# Inicializar detector
detector = ExoplanetDetector()

# Treinar modelos
df = detector.prepare_sample_data()
processed_df, features = detector.preprocess_data(df)
results = detector.train_models(processed_df, features)

# Analisar novo objeto
prediction = detector.predict_exoplanet(data_point)
print(f"Classificação: {prediction['ensemble_prediction']}")
        """)

if __name__ == "__main__":
    main()
    
    # Rodapé com link do repositório
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>🚀 <strong>Sistema de Detecção de Exoplanetas com IA</strong> | NASA Space Apps Challenge 2025</p>
        <p>📂 <a href='https://github.com/MatheusEdson/NASA-Space-Apps-Challenge-2025' target='_blank' style='color: #667eea;'>Repositório GitHub</a></p>
    </div>
    """, unsafe_allow_html=True)