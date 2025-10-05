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
        'analyze': 'Analisar',
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
        'classifications': 'Classificações',
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
        'use_template_button': 'Use the "Download Template CSV" button in the sidebar to get a complete example!'
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
        'use_template_button': '¡Usa el botón "Descargar Plantilla CSV" en la barra lateral para obtener un ejemplo completo!'
    }
}

def get_translation(key, lang='pt'):
    """Retorna a tradução para a chave especificada"""
    return TRANSLATIONS.get(lang, TRANSLATIONS['pt']).get(key, key)

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
    /* Fundo estrelado simples e eficaz */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%) !important;
        background-attachment: fixed !important;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(1px 1px at 20px 30px, white, transparent),
            radial-gradient(1px 1px at 40px 70px, rgba(255,255,255,0.8), transparent),
            radial-gradient(1px 1px at 90px 40px, white, transparent),
            radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.6), transparent),
            radial-gradient(1px 1px at 160px 30px, white, transparent),
            radial-gradient(1px 1px at 200px 50px, rgba(255,255,255,0.4), transparent),
            radial-gradient(1px 1px at 250px 20px, white, transparent),
            radial-gradient(1px 1px at 300px 80px, rgba(255,255,255,0.8), transparent);
        background-repeat: repeat;
        background-size: 300px 200px;
        animation: twinkle 3s ease-in-out infinite alternate;
        pointer-events: none;
        z-index: -1;
    }
    
    @keyframes twinkle {
        0% { opacity: 0.3; }
        100% { opacity: 1; }
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

@st.cache_data(ttl=300)
def get_random_planet_images():
    planet_images = {
        'earth': [
            'https://upload.wikimedia.org/wikipedia/commons/thumb/9/97/The_Earth_seen_from_Apollo_17.jpg/200px-The_Earth_seen_from_Apollo_17.jpg',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Earth_from_Space.jpg/200px-Earth_from_Space.jpg',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Earth_Western_Hemisphere.jpg/200px-Earth_Western_Hemisphere.jpg'
        ],
        'mars': [
            'https://upload.wikimedia.org/wikipedia/commons/thumb/0/02/OSIRIS_Mars_true_color.jpg/200px-OSIRIS_Mars_true_color.jpg',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/5/58/Mars_23_aug_2003_hubble.jpg/200px-Mars_23_aug_2003_hubble.jpg',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/7/76/Mars_Hubble.jpg/200px-Mars_Hubble.jpg'
        ],
        'neptune': [
            'https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Neptune_-_Voyager_2_%2829347980845%29_flatten_crop.jpg/200px-Neptune_-_Voyager_2_%2829347980845%29_flatten_crop.jpg',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/5/56/Neptune_Full.jpg/200px-Neptune_Full.jpg',
            'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b4/Neptune.jpg/200px-Neptune.jpg'
        ]
    }
    
    # Selecionar imagens aleatórias para cada categoria
    import random
    selected_images = {}
    for planet_type, urls in planet_images.items():
        selected_images[planet_type] = random.choice(urls)
    
    return selected_images

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
    # Obter idioma selecionado
    selected_language = get_language_selector()

    # Header principal
    st.markdown(f'<h1 class="main-header">{get_translation("main_header", selected_language)}</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
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
            
            # Obter imagens aleatórias dos planetas
            planet_images = get_random_planet_images()
            
            # Cores planetárias: Terra (azul), Marte (vermelho), Netuno (azul escuro)
            planet_colors = ['#4169E1', '#FF4500', '#1E90FF']  # Terra, Marte, Netuno
            
            # Criar gráfico de pizza simples sem annotations problemáticas
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
            
            # Mostrar imagens dos planetas abaixo do gráfico
            st.markdown(f"**{get_translation('representative_planets', selected_language)}:**")
            col_earth, col_mars, col_neptune = st.columns(3)
            
            with col_earth:
                st.image(planet_images['earth'], width=80, caption=get_translation("earth_confirmed", selected_language))
            with col_mars:
                st.image(planet_images['mars'], width=80, caption=get_translation("mars_candidates", selected_language))
            with col_neptune:
                st.image(planet_images['neptune'], width=80, caption=get_translation("neptune_false", selected_language))
    
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

        fig_comparison.add_trace(go.Bar(name='Acurácia', x=models, y=accuracy, marker_color='#667eea'))
        fig_comparison.add_trace(go.Bar(name='Precisão', x=models, y=precision, marker_color='#764ba2'))
        fig_comparison.add_trace(go.Bar(name='Recall', x=models, y=recall, marker_color='#f093fb'))
        fig_comparison.add_trace(go.Bar(name='F1-Score', x=models, y=f1_score, marker_color='#f5576c'))

        fig_comparison.update_layout(
        title=get_translation("model_comparison", selected_language),
        xaxis_title="Modelos",
        yaxis_title="Score",
        barmode='group',
        height=400
    )

        st.plotly_chart(fig_comparison, use_container_width=True)
    
    with tab4:
        st.header("Documentação e Recursos")
        
        st.subheader("Sobre o Sistema")
        st.markdown("""
        Este sistema utiliza **Inteligência Artificial** para identificar e classificar exoplanetas 
        usando dados das missões Kepler, K2 e TESS da NASA.
        
        ### 🔬 Metodologia
        
        **1. Pré-processamento dos Dados**
        - Limpeza e normalização dos datasets da NASA
        - Remoção de outliers usando métodos estatísticos
        - Balanceamento de classes com SMOTE
        
        
        **3. Modelos Utilizados**
        - **Random Forest**: Robust para dados ruidosos astronômicos
        - **XGBoost**: Alta precisão para padrões complexos
        - **LightGBM**: Eficiência computacional otimizada
        - **Ensemble**: Combinação para máxima robustez
        
        ### Variáveis de Análise
        
        - **Período Orbital**: Duração da órbita do planeta
        - **Duração do Trânsito**: Tempo de transição
        - **Profundidade**: Redução no brilho estelar
        - **Raio Planetário**: Tamanho relativo à Terra
        - **Temperatura de Equilíbrio**: Estimativa térmica
        
        ### Formato da Planilha Padrão
        
        **Colunas Obrigatórias:**
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
        
        **Dica:** Use o botão "Baixar Template CSV" na sidebar para obter um exemplo completo!
        
        
        ### Classificações
        
        - **Confirmado**: Planeta validado por múltiplas observações
        - **Candidato**: Requer validação adicional
        - **Falso Positivo**: Fenômeno estelar não planetário
        
        ### Recursos Técnicos
        
        - Interface web responsiva com Streamlit
        - Visualizações interativas com Plotly
        - Monitoramento em tempo real
        - Upload e análise manual de dados
        - Sistema de modelos ensemble
        """)
        
        st.subheader("🔗 Recursos Externos")
        st.markdown("""
        - [NASA Exoplanet Archive](https://exoplanetarchive.ipac.caltech.edu/)
        - [Kepler Mission](https://www.nasa.gov/mission_pages/kepler/main/)
        - [TESS Mission](https://tess.mit.edu/)
        - [K2 Mission](https://keplerscience.arc.nasa.gov/k2/)
        """)
        
        st.subheader("📖 Código Fonte")
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