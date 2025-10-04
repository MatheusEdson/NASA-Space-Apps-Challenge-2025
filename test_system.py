"""
Teste rápido do sistema de detecção de exoplanetas
"""

print("=== TESTE DO SISTEMA DE DETECCAO DE EXOPLANETAS ===")

try:
    from exoplanet_ml import ExoplanetDetector
    print("✅ Módulo exoplanet_ml importado com sucesso!")
    
    detector = ExoplanetDetector()
    print("✅ Detector inicializado!")
    
    data = detector.prepare_sample_data()
    print(f"📊 Dataset carregado: {len(data)} registros")
    
    processed_data, features = detector.preprocess_data(data)
    print(f"🔧 Dados processados: {len(processed_data)} registros")
    print(f"🎯 Características: {len(features)} features")
    
    print("🚀 TESTE CONLETO COM SUCESSO!")
    print("✨ Sistema pronto para uso!")
    
except Exception as e:
    print(f"❌ Erro no teste: {str(e)}")
