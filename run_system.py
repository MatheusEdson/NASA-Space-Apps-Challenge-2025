"""
Script de Inicialização do Sistema de Detecção de Exoplanetas
Configra e executa todos os componentes do sistema
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def print_banner():
    """Exibe banner do sistema"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════╗
║                    🌌 SISTEMA DE DETECÇÃO DE EXOPLANETAS 🌌               ║
║                            NASA Missions AI/ML                          ║
║                                                                          ║
║  🚀 Kepler • K2 • TESS Data Analysis                                    ║
║  🤖 Machine Learning Classification                                      ║
║  📊 Real-time Monitoring Dashboard                                       ║
║  🔬 Scientific Research Interface                                       ║
╚══════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    required_packages = [
        'numpy', 'pandas', 'scikit-learn', 'streamlit', 'plotly',
        'matplotlib', 'seaborn', 'xgboost', 'lightgbm', 'requests'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package} - FALTANDO")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Instalando pacotes faltantes: {', '.join(missing_packages)}")
        install_command = f"pip install {' '.join(missing_packages)}"
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages)
        print("✅ Instalação concluída!")
    else:
        print("✅ Todas as dependências estão instaladas!")
    
    return len(missing_packages) == 0

def setup_directories():
    """Configura diretórios necessários"""
    print("📁 Configurando estrutura de diretórios...")
    
    directories = ['models', 'data', 'results', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"  📂 Criado: {directory}/")
    
    print("✅ Estrutura de diretórios configurada!")

def initialize_models():
    """Inicializa e treina modelos de ML"""
    print("🤖 Inicializando modelos de Machine Learning...")
    
    try:
        from exoplanet_ml import ExoplanetDetector
        
        detector = ExoplanetDetector()
        
        print("  📊 Gerando dados de treinamento...")
        df = detector.prepare_sample_data()
        
        print("  🔧 Pré-processando dados...")
        processed_df, features = detector.preprocess_data(df)
        
        print("  🚀 Treinando modelos...")
        results, X_test, y_test = detector.train_models(processed_df, features)
        
        print("  ✅ Modelos treinados com sucesso!")
        
        for model_name, metrics in results.items():
            print(f"    {model_name}: {metrics['accuracy']:.1%} accuracy")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erro ao inicializar modelos: {str(e)}")
        return False

def launch_web_interface():
    """Lança interface web Streamlit"""
    print("🌐 Lançando interface web...")
    
    # Aguardar um pouco para o servidor inicializar
    time.sleep(2)
    
    # Tentar abrir no navegador padrão
    try:
        streamlit_url = "http://localhost:8501"
        print(f"🔗 Interface disponível em: {streamlit_url}")
        print("🌍 Abrindo navegador...")
        webbrowser.open(streamlit_url)
    except:
        print("🌍 Navegador não pôde ser aberto automaticamente. Acesse manualmente: http://localhost:8501")
    
    # Executar Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.port", "8501"])
    except KeyboardInterrupt:
        print("\n🛑 Sistema interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar Streamlit: {str(e)}")

def run_system_diagnostics():
    """Executa diagnósticos do sistema"""
    print("🔬 Executando diagnósticos do sistema...")
    
    diagnostics = {
        'Python version': sys.version,
        'Working directory': os.getcwd(),
        'Available modules': len(list(Path('.').glob('*.py'))),
        'Models directory': os.path.exists('models'),
        'Data directory': os.path.exists('data')
    }
    
    print("\n📋 DIAGNÓSTICOS:")
    for key, value in diagnostics.items():
        if isinstance(value, bool):
            status = "✅" if value else "❌"
            print(f"  {status} {key}: {value}")
        else:
            print(f"  ℹ️  {key}: {value}")

def show_usage_guide():
    """Mostra guia de uso do sistema"""
    guide = """
📚 GUIA DE USO DO SISTEMA

🎛️  CONTROLES WEB:
  • Dashboard: Monitoramento em tempo real
  • Análise: Classificação manual de objetos
  • Performance: Métricas dos modelos
  • Documentação: Recursos e APIs

🔬 FUNCIONALIDADES:
  • Upload de datasets da NASA
  • Análise manual de parâmetros
  • Predição em tempo real
  • Visualizações interativas
  • Monitoramento de performance

🚀 FUNCIONAMENTO:
  1. Modelos são treinados automaticamente
  2. Interface atualiza dados em tempo real
  3. Suporta múltiplos algoritmos (RF, XGB, LGBM)
  4. Visualizações com Plotly
  5. Cache inteligente para performance

📊 DATASETS SUPORTADOS:
  • Kepler Objects of Interest (KOI)
  • TESS Objects of Interest (TOI)  
  • K2 Planets and Candidates
  • Dados sintéticos realistas

🎯 CLASSIFICAÇÕES:
  • CONFIRMED: Planetas validados
  • CANDIDATE: Requerem mais análise
  • FALSE POSITIVE: Ruídos/fenômenos estelares
    """
    print(guide)

def main():
    """Função principal do sistema"""
    print_banner()
    
    print("🚀 Iniciando Sistema de Detecção de Exoplanetas...\n")
    
    # Verificar dependências
    if not check_dependencies():
        print("❌ Falha na verificação de dependências. Verifique a instalação.")
        return
    
    print()
    
    # Configurar diretórios
    setup_directories()
    print()
    
    # Executar diagnósticos
    run_system_diagnostics()
    print()
    
    # Inicializar modelos
    init_check = input("🤖 Deseja inicializar e treinar os modelos agora? (S/N): ").upper().strip()
    if init_check in ['S', 'SIM', 'Y', 'YES']:
        initialize_models()
        print()
    else:
        print("⏭️  Modelos serão treinados quando necessário\n")
    
    # Mostrar guia de uso
    show_guide = input("📚 Exibir guia de uso? (S/N): ").upper().strip()
    if show_guide in ['S', 'SIM', 'Y', 'YES']:
        show_usage_guide()
        print()
    
    # Perguntar se quer lançar interface web
    launch_check = input("🌐 Lançar interface web Streamlit? (S/N): ").upper().strip()
    if launch_check in ['S', 'SIM', 'Y', 'YES']:
        launch_web_interface()
    else:
        print("🏁 Sistema configurado! Execute 'streamlit run streamlit_app.py' para iniciar a interface.")
    
    print("✨ Sistema preparado com sucesso!")

if __name__ == "__main__":
    main()
