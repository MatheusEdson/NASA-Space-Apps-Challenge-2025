# 🌌 NASA Space Apps Challenge - Sistema de Detecção de Exoplanetas

## 🚀 Visão Geral

Sistema de **Inteligência Artificial/Machine Learning** para análise de dados de exoplanetas das missões Kepler, K2 e TESS, desenvolvido para o NASA Space Apps Challenge.

## ✅ Funcionalidades Implementadas

### 🤖 Machine Learning
- **Modelos treinados**: Random Forest, XGBoost, LightGBM, Ensemble
- **Classificação automática**: Confirmado, Candidato, Falso Positivo
- **Análise em tempo real** com visualizações dinâmicas
- **Upload de dados** por usuários (CSV/Excel)

### 🌐 Interface Web
- **Dashboard interativo** com métricas em tempo real
- **Visualizações científicas** com Plotly
- **Análise manual** de parâmetros astronômicos
- **Gráfico de hyperparâmetros** para otimização
- **Interface multilíngue** (Português, Inglês, Espanhol)

### 🎨 Interface Visual
- **Fundo estrelado animado** com efeito espacial
- **Gráfico de pizza** com imagens de planetas integradas
- **Landscape de otimização** com contornos e pontos de amostragem
- **Design responsivo** e profissional

## 🛠️ Tecnologias

### Backend
- **Python 3.10+**
- **scikit-learn, XGBoost, LightGBM** (ML)
- **pandas, numpy** (processamento de dados)
- **joblib** (serialização de modelos)

### Frontend
- **Streamlit** (framework web)
- **Plotly** (visualizações interativas)
- **CSS customizado** (estilização espacial)

### Deploy
- **Easypanels** (VPS deployment)
- **Buildpacks** (containerização)
- **Git** (controle de versão)

## 🚀 Como Executar

### Instalação Local
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Deploy em Produção
- Configurado para Easypanels
- Buildpacks automático
- Domínio: `spaceappschallenge.matheusedson.com`

## 📊 Datasets NASA

- **Kepler KOI**: Objetos de interesse da missão Kepler
- **TESS TOI**: Objetos de interesse da missão TESS  
- **K2**: Planetas e candidatos da missão K2

## 🎯 Casos de Uso

### Para Cientistas
- Upload de novos datasets para análise
- Classificação automática de candidatos
- Análise manual de parâmetros específicos
- Monitoramento de performance dos modelos

### Para Pesquisadores
- Visualização de landscapes de hyperparâmetros
- Análise de distribuições planetárias
- Comparação entre diferentes algoritmos ML
- Exportação de resultados para publicação

## 🌟 Características Únicas

- **Interface espacial** com fundo estrelado animado
- **Planetas integrados** nos gráficos de classificação
- **Otimização visual** de hyperparâmetros
- **Multilíngue** para acesso global
- **Tempo real** para análise contínua

---

**🌌 NASA Space Apps Challenge 2024**  
**Categoria**: Machine Learning/Artificial Intelligence  
**Status**: ✅ Implementado e em produção