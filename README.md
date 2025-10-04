# Sistema de Detecção de Exoplanetas com IA/ML

Este projeto implementa um sistema de inteligência artificial para identificar e classificar exoplanetas utilizando dados das missões Kepler, K2 e TESS da NASA.

## Funcionalidades

- 🤖 Modelo de Machine Learning treinado com datasets da NASA
- 🌐 Interface web interativa com Streamlit
- 📊 Visualizações em tempo real do processo de análise
- 📈 Monitoramento de performance e acurácia do modelo
- 🔄 Upload de novos dados para análise
- 👥 Interface amigável para cientistas e pesquisadores

## Instalação

1. Clone o repositório
2. Instale as dependências:
```bash
pip install -r requirements.txt`
```

3. Execute a aplicação:
```bash
streamlit run streamlit_app.py
```

## Datasets Utilizados

- **Kepler Objects of Interest (KOI)**: Confirmados, candidatos e falsos positivos do Kepler
- **TESS Objects of Interest (TOI)**: Dados da missão TESS
- **K2 Planets and Candidates**: Dados da missão K2

## Modelos Implementados

- Random Forest Classifier
- XGBoost
- LightGBM
- Ensemble Methods

## Como Usar

1. Acesse a interface web
2. Visualize estatísticas do modelo em tempo real
3. Faça upload de dados novos para análise
4. Insira dados manualmente para classificação
5. Monitore a performance do modelo
