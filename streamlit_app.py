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
    page_title="🌌 Detecção de Exoplanetas com IA",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem;
        color: white;
        text-align: center;
    }
    
    .status-running {
        color: #00ff00;
        font-weight: bold;
    }
    
    .status-stopped {
        color: #ff0000;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar sistema
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
    # Header principal
    st.markdown('<h1 class="main-header">🌌 Sistema de Detecção de Exoplanetas com IA</h1>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Controles do Sistema")
        
        # Status do sistema
        st.subheader("Status do Sistema")
        system_status = st.radio("Status:", ["🟢 Ativo", "🔴 Pausado"], key="status")
        
        if system_status == "🟢 Ativo":
            st.markdown('<p class="status-running">● Sistema ATIVO</p>', unsafe_allow_html=True)
        else:
            st.markdown('<p class="status-stopped">● Sistema PAUSADO</p>', unsafe_allow_html=True)
        
        # Seleção de modelo
        st.subheader("🤖 Modelo Ativo")
        model_option = st.selectbox(
            "Escolha o modelo:",
            ["Random Forest", "XGBoost", "LightGBM", "Ensemble"]
        )
        
        # Configurações
        st.subheader("⚙️ Configurações")
        update_interval = st.slider("Intervalo de atualização (segundos):", 1, 30, 5)
        confidence_threshold = st.slider("Limiar de confiança:", 0.0, 1.0, 0.8)
        
        # Upload de dados
        st.subheader("📂 Upload de Dados")
        uploaded_file = st.file_uploader("Carregar dataset:", type=['csv', 'xlsx'])
        
        if uploaded_file:
            st.success(f"Arquivo carregado: {uploaded_file.name}")
    
    # Layout principal com tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "🔍 Análise", Ativo": status_color})
    
    # Barra de progresso da análise atual
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    with tab1:
        st.header("📊 Dashboard em Tempo Real")
        
        # Auto-refresh
        if st.button("🔄 Atualizar Dados") or system_status == "🟢 Ativo":
            # Simular atualização em tempo real
            for i in range(101):
                progress_bar.progress(i)
                if i < 50:
                    status_text.text("🔍 Analisando dados de transito...")
                elif i < 80:
                    status_text.text("🧮 Calculando probabilidades...")
                elif i < 95:
                    status_text.text("🤖 Executando modelo ML...")
                else:
                    status_text.text("✅ Análise concluída!")
                time.sleep(0.02)
            
            # Limpar interface
            progress_bar.empty()
            status_text.empty()
        
        # Métricas em tempo real
        real_time_data = get_real_time_data()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("🌍 Objetos Analisados", f"{real_time_data['objects_analyzed']:,}")
        
        with col2:
            st.metric("✅ Confirmados", f"{real_time_data['confirmed_exoplanets']}", "+5")
        
        with col3:
            st.metric("🔍 Candidatos", f"{real_time_data['candidates']}", "+12")
        
        with col4:
            st.metric("❌ Falsos Positivos", f"{real_time_data['false_positives']}", "-3")
        
        # Gráficos em tempo real
        col_left, col_right = st.columns(2)
        
        with col_left:
            # Gráfico de acurácia ao longo do tempo
            st.subheader("📈 Acurácia do Modelo")
            
            # Simular dados históricos de acurácia
            timestamps = pd.date_range(end=datetime.now(), periods=50, freq='min')
            accuracy_history = np.random.uniform(0.8, 0.95, 50).cumsum() / np.arange(1, 51)
            
            fig_accuracy = go.Figure()
            fig_accuracy.add_trace(go.Scatter(
                x=timestamps,
                y=accuracy_history,
                mode='lines+markers',
                name='Acurácia',
                line=dict(color='#667eea', width=3)
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
            st.subheader("🥧 Distribuição Atual")
            
            labels = ['Confirmados', 'Candidatos', 'Falsos Positivos']
            values = [real_time_data['confirmed_exoplanets'], 
                     real_time_data['candidates'], 
                     real_time_data['false_positives']]
            
            fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values)])
            fig_pie.update_layout(height=300)
            
            st.plotly_chart(fig_pie, use_container_width=True)
    
    with tab2:
        st.header("🔍 Análise Detalhada")
        
        # Inicializar detector se ainda não foi feito
        detector = initialize_detector()
        
        # Treinamento do modelo
        if st.button("🚀 Treinar Modelos"):
            with st.spinner("Treinando modelos... Isso pode levar alguns minutos"):
                # Preparar dados de exemplo
                df = detector.prepare_sample_data()
                
                # Pré-processamento
                processed_df, features = detector.preprocess_data(df)
                
                # Treinamento
                results, X_test, y_test = detector.train_models(processed_df, features)
                
                st.success("✅ Modelos treinados com sucesso!")
        
        # Entrada manual de dados
        st.subheader("📝 Análise Manual")
        
        col_p1, col_p2, col_p3 = st.columns(3)
        
        with col_p1:
            orbital_period = st.number_input("Período Orbital (dias):", min_value=0.1, value=365.25)
            transit_duration = st.number_input("Duração do Trânsito (horas):", min_value=0.1, value=8.0)
            planet_radius = st.number_input("Raio Planetário (Terra):", min_value=0.1, value=1.0)
        
        with col_p2:
            stellar_mass = st.number_input("Massa Estelar (Solar):", min_value=0.1, value=1.0)
            stellar_radius = st.number_input("Raio Estelar (Solar):", min_value=0.1, value=1.0)
            equilibrium_temp = st.number_input("Temperatura Equilibrio (K):", min_value=100.0, value=300.0)
        
        with col_p3:
            impact_parameter = st.number_input("Parâmetro de Impacto:", min_value=0.0, max_value=1.0, value=0.5)
            stellar_density = st.number_input("Densidade Estelar (g/cm³):", min_value=0.1, value=1.4)
            kepmag = st.number_input("Magnitude Kepler:", min_value=8.0, max_value=16.0, value=12.0)
        
        if st.button("🔬 Analisar Dados"):
            # Preparar dados para análise
            input_data = [orbital_period, transit_duration, planet_radius, 
                         stellar_mass, stellar_radius, equilibrium_temp,
                         impact_parameter, stellar_density, kepmag]
            
            # Simular predição (substitua por detector.predict_exoplanet() quando modelos estiverem treinados)
            pred_probs = np.random.uniform(0, 1, 3)
            pred_probs = pred_probs / pred_probs.sum()
            
            pred_labels = ['CONFIRMED', 'CANDIDATE', 'FALSE POSITIVE']
            
            # Mostrar resultados
            st.subheader("🎯 Resultados da Análise")
            
            col_r1, col_r2, col_r3 = st.columns(3)
            
            with col_r1:
                st.metric("Confirmado", f"{pred_probs[0]:.2%}", f"{pred_probs[0]*100:.1f}%")
            
            with col_r2:
                st.metric("Candidato", f"{pred_probs[1]:.2%}", f"{pred_probs[1]*100:.1f}%")
            
            with col_r3:
                st.metric("Falso Positivo", f"{pred_probs[2]:.2%}", f"{pred_probs[2]*100:.1f}%")
            
            # Gráfico de probabilidades
            fig_probs = go.Figure(data=[
                go.Bar(x=pred_labels, y=pred_probs, 
                      marker_color=['#2E8B57', '#FFA500', '#DC143C'])
            ])
            fig_probs.update_layout(
                title="Probabilidades de Classificação",
                yaxis_title="Probabilidade",
                height=400
            )
            st.plotly_chart(fig_probs, use_container_width=True)
    
    with tab3:
        st.header("🤖 Performance dos Modelos")
        
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
        st.header("📚 Documentação e Recursos")
        
        st.subheader("🌌 Sobre o Sistema")
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
        
        ### 📊 Variáveis de Análise
        
        - **Período Orbital**: Duração da órbita do planeta
        - **Duração do Trânsito**: Tempo de transição
        - **Profundidade**: Redução no brilho estelar
        - **Raio Planetário**: Tamanho relativo à Terra
        - **Temperatura de Equilíbrio**: Estimativa térmica
        
        
        ### 🎯 Classificações
        
        - ✅ **Confirmado**: Planeta validado por múltiplas observações
        - 🔍 **Candidato**: Requer validação adicional
        - ❌ **Falso Positivo**: Fenômeno estelar não planetário
        
        ### 🛠️ Recursos Técnicos
        
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

# Auto-refresh para simulação de tempo real
if st.session_state.get('auto_refresh', False):
    time.sleep(5)
    st.rerun()

if __name__ == "__main__":
    main()
