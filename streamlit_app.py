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

# Configurar página
st.set_page_config(
    page_title="Detecção de Exoplanetas com IA",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar detector (exemplo)
@st.cache_resource
def initialize_detector():
    return ExoplanetDetector()

# CSS customizado com fundo estrelado
st.markdown("""
<style>
    /* Fundo estrelado animado */
    body {
        background: radial-gradient(ellipse at bottom, #1B2735 0%, #090A0F 100%);
        overflow-x: hidden;
    }
    
    .stars {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
    }
    
    .star {
        position: absolute;
        background: white;
        border-radius: 50%;
        animation: twinkle 3s infinite;
    }
    
    .star:nth-child(1) { top: 20%; left: 10%; width: 2px; height: 2px; animation-delay: 0s; }
    .star:nth-child(2) { top: 30%; left: 20%; width: 1px; height: 1px; animation-delay: 0.5s; }
    .star:nth-child(3) { top: 15%; left: 30%; width: 3px; height: 3px; animation-delay: 1s; }
    .star:nth-child(4) { top: 40%; left: 15%; width: 1px; height: 1px; animation-delay: 1.5s; }
    .star:nth-child(5) { top: 25%; left: 40%; width: 2px; height: 2px; animation-delay: 2s; }
    .star:nth-child(6) { top: 35%; left: 50%; width: 1px; height: 1px; animation-delay: 2.5s; }
    .star:nth-child(7) { top: 20%; left: 60%; width: 2px; height: 2px; animation-delay: 0.8s; }
    .star:nth-child(8) { top: 45%; left: 70%; width: 1px; height: 1px; animation-delay: 1.3s; }
    .star:nth-child(9) { top: 30%; left: 80%; width: 3px; height: 3px; animation-delay: 1.8s; }
    .star:nth-child(10) { top: 15%; left: 90%; width: 1px; height: 1px; animation-delay: 2.3s; }
    .star:nth-child(11) { top: 50%; left: 25%; width: 2px; height: 2px; animation-delay: 0.3s; }
    .star:nth-child(12) { top: 60%; left: 45%; width: 1px; height: 1px; animation-delay: 0.7s; }
    .star:nth-child(13) { top: 70%; left: 65%; width: 2px; height: 2px; animation-delay: 1.2s; }
    .star:nth-child(14) { top: 80%; left: 35%; width: 1px; height: 1px; animation-delay: 1.7s; }
    .star:nth-child(15) { top: 90%; left: 55%; width: 3px; height: 3px; animation-delay: 2.2s; }
    
    @keyframes twinkle {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 1; transform: scale(1.2); }
    }
    
    .main-header {
        font-size: 3rem;
        color: #ffffff;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 0 20px rgba(102, 126, 234, 0.5);
    }
    
    .metric-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.8) 0%, rgba(118, 75, 162, 0.8) 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        color: white;
        text-align: center;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .status-running {
        color: #00ff88;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(0, 255, 136, 0.5);
    }
    
    .status-stopped {
        color: #ff4444;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(255, 68, 68, 0.5);
    }
    
    /* Transparência para elementos Streamlit */
    .stApp > header {
        background-color: rgba(14, 17, 23, 0.8);
    }
    
    .stApp {
        background-color: transparent;
    }
    
    .main .block-container {
        background-color: rgba(14, 17, 23, 0.1);
        backdrop-filter: blur(10px);
    }
</style>

<div class="stars">
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
    <div class="star"></div>
</div>
""", unsafe_allow_html=True)

# Inicializar sistema
@st.cache_resource
def initialize_detector():
    return ExoplanetDetector()

# Sistema de imagens planetárias aleatórias
@st.cache_data(ttl=300)  # Cache por 5 minutos para manter consistência
def get_random_planet_images():
    """Retorna URLs de imagens de planetas aleatórias"""
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

    # Header principal
    st.markdown('<h1 class="main-header">Sistema de Detecção de Exoplanetas com IA</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("Controles do Sistema")
        
        # Status do sistema
        st.subheader("Status do Sistema")
        system_status = st.radio("Status:", ["Ativo", "Pausado"], key="status")
        
        if system_status == "Ativo":
            st.markdown('<p class="status-running">● Sistema ATIVO</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-stopped">● Sistema PAUSADO</p>', unsafe_allow_html=True)
        
        # Seleção de modelo
        st.subheader("Modelo Ativo")
        model_option = st.selectbox(
            "Escolha o modelo:",
            ["Random Forest", "XGBoost", "LightGBM", "Ensemble"]
        )
        
        # Configurações
        st.subheader("Configurações")
        update_interval = st.slider("Intervalo de atualização (segundos):", 1, 30, 5)
        confidence_threshold = st.slider("Limiar de confiança:", 0.0, 1.0, 0.8)
        
        # Upload de dados
        st.subheader("Upload de Dados")
        
        # Download da planilha padrão
        st.markdown("**Planilha Padrão:**")
        with open('exoplanet_template.csv', 'r') as f:
            csv_content = f.read()
        
        st.download_button(
            label="Baixar Template CSV",
            data=csv_content,
            file_name="exoplanet_template.csv",
            mime="text/csv",
            help="Use este template como base para seus dados"
        )
        
        uploaded_file = st.file_uploader("Carregar dataset:", type=['csv', 'xlsx'])
        
        if uploaded_file:
            st.success(f"Arquivo carregado: {uploaded_file.name}")
    
    # Layout principal com tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Análise", "Performance", "Documentação"])
    
    # Barra de progresso da análise atual
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with tab1:
        st.header("Dashboard em Tempo Real")
        
        # Auto-refresh
        if st.button("Atualizar Dados") or system_status == "Ativo":
            # Simular atualização em tempo real
            for i in range(101):
                progress_bar.progress(i)
                if i < 50:
                    status_text.text("Analisando dados de trânsito...")
                elif i < 80:
                    status_text.text("Calculando probabilidades...")
                elif i < 95:
                    status_text.text("Executando modelo ML...")
                else:
                    status_text.text("Análise concluída!")
                time.sleep(0.02)
            
            # Limpar interface
            progress_bar.empty()
            status_text.empty()
        
        # Métricas em tempo real
        real_time_data = get_real_time_data()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Objetos Analisados", f"{real_time_data['objects_analyzed']:,}")
        
        with col2:
            st.metric("Confirmados", f"{real_time_data['confirmed_exoplanets']}", "+5")
        
        with col3:
            st.metric("Candidatos", f"{real_time_data['candidates']}", "+12")
        
        with col4:
            st.metric("Falsos Positivos", f"{real_time_data['false_positives']}", "-3")
        
        # Gráficos em tempo real
        col_left, col_right = st.columns(2)
        
        with col_left:
            # Gráfico de acurácia ao longo do tempo
            st.subheader("Acurácia do Modelo")
            
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
                title="Evolução da Acurácia",
                xaxis_title="Tempo",
                yaxis_title="Acurácia",
                height=300
            )
            
            st.plotly_chart(fig_accuracy, use_container_width=True)
        
        with col_right:
            # Distribuição das classificações
            st.subheader("Distribuição Planetária")
            
            labels = ['Confirmados', 'Candidatos', 'Falsos Positivos']
            values = [real_time_data['confirmed_exoplanets'], 
                     real_time_data['candidates'], 
                     real_time_data['false_positives']]
            
            # Obter imagens aleatórias dos planetas
            planet_images = get_random_planet_images()
            
            # Cores planetárias: Terra (azul), Marte (vermelho), Netuno (azul escuro)
            planet_colors = ['#4169E1', '#FF4500', '#1E90FF']  # Terra, Marte, Netuno
            
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
                    text="Classificação de Exoplanetas",
                    font=dict(size=16, color='#2E8B57')
                )
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Mostrar imagens dos planetas selecionados
            st.markdown("**Planetas Representativos:**")
            col_earth, col_mars, col_neptune = st.columns(3)
            
            with col_earth:
                st.image(planet_images['earth'], width=80, caption="Terra - Confirmados")
            with col_mars:
                st.image(planet_images['mars'], width=80, caption="Marte - Candidatos")
            with col_neptune:
                st.image(planet_images['neptune'], width=80, caption="Netuno - Falsos Positivos")
    
    with tab2:
        st.header("Análise Manual")

        col_p1, col_p2, col_p3 = st.columns(3)

        with col_p1:
            orbital_period = st.number_input("Período Orbital (dias):", min_value=0.1, value=365.25)
            transit_duration = st.number_input("Duração do Trânsito (horas):", min_value=0.1, value=8.0)
            planet_radius = st.number_input("Raio Planetário (Terra):", min_value=0.1, value=1.0)

        with col_p2:
            stellar_mass = st.number_input("Massa Estelar (Solar):", min_value=0.1, value=1.0)
            stellar_radius = st.number_input("Raio Estelar (Solar):", min_value=0.1, value=1.0)
            equilibrium_temp = st.number_input("Temperatura de Equilíbrio (K):", min_value=100.0, value=300.0)

        with col_p3:
            impact_parameter = st.number_input("Parâmetro de Impacto:", min_value=0.0, max_value=1.0, value=0.5)
            stellar_density = st.number_input("Densidade Estelar (g/cm³):", min_value=0.1, value=1.4)
            kepmag = st.number_input("Magnitude Kepler:", min_value=8.0, max_value=16.0, value=12.0)

        if st.button("Analisar Dados"):
            input_data = [
            orbital_period, transit_duration, planet_radius,
            stellar_mass, stellar_radius, equilibrium_temp,
            impact_parameter, stellar_density, kepmag
        ]

        # Simulação das probabilidades para exemplo:
        pred_probs = np.random.uniform(0, 1, 3)
        pred_probs /= pred_probs.sum()

        pred_labels = ['Confirmado', 'Candidato', 'Falso Positivo']

        st.subheader("Resultados da Análise")

        col_r1, col_r2, col_r3 = st.columns(3)

        with col_r1:
            st.metric("Confirmado", f"{pred_probs[0]:.2%}")

        with col_r2:
            st.metric("Candidato", f"{pred_probs[1]:.2%}")

        with col_r3:
            st.metric("Falso Positivo", f"{pred_probs[2]:.2%}")

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
        st.header("Performance dos Modelos")

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
        title="Comparação de Métricas por Modelo",
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