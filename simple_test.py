"""
Teste simples do sistema
"""

print("=== TESTE DO SISTEMA ===")

try:
    from exoplanet_ml import ExoplanetDetector
    print("OK: Modulo importado!")
    
    detector = ExoplanetDetector()
    print("OK: Detector inicializado!")
    
    data = detector.prepare_sample_data()
    print(f"Dados: {len(data)} registros")
    
    print("SUCESSO!")
    
except Exception as e:
    print(f"ERRO: {str(e)}")
