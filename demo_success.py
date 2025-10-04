"""
Demonstracao final - SEM emojis
"""

def demo_system():
    print("=" * 70)
    print("NASA SPACE APPS CHALLENGE - SISTEMA DE DETECAO DE EXOPLANETAS")
    print("=" * 70)
    
    try:
        # Testar sistema principal
        from exoplanet_ml import ExoplanetDetector
        print("\n1. SISTEMA DE MACHINE LEARNING:")
        print("   OK - Modulo carregado")
        
        detector = ExoplanetDetector()
        print("   OK - Detector inicializado")
        
        data = detector.prepare_sample_data()
        print(f"   OK - Dataset gerado: {len(data)} objetos")
        
        processed_data, features = detector.preprocess_data(data)
        print(f"   OK - Dados processados: {len(processed_data)} objetos")
        print(f"   OK - Caracteristicas: {len(features)} features")
        
        print("   Processando modelos ML...")
        results, _, _ = detector.train_models(processed_data, features)
        
        print(f"\n   RESULTADOS:")
        for model_name, metrics in results.items():
            print(f"     {model_name}: {metrics['accuracy']:.1%} acuracia")
        
        # Acessar outras funcionalidades
        print("\n2. MODULOS ADICIONAIS:")
        from data_visualizer import ExoplanetVisualizer
        visualizer = ExoplanetVisualizer()
        print("   OK - Visualizador")
        
        from transit_analyzer import TransitAnalyzer  
        analyzer = TransitAnalyzer()
        print("   OK - Analisador de transitos")
        
        print("\n" + "=" * 70)
        print("SISTEMA FUNCIONANDO PERFEITAMENTE!")
        print("=" * 70)
        
        print("\nCOMO USAR:")
        print("1. Interface Web: streamlit run streamlit_app.py")
        print("2. Demo Completa: python example_usage.py")
        print("3. Deploy Produção: python production_deploy.py")
        
        print("\nFUNCIONALIDADES:")
        print("- Deteccao automatica de exoplanetas")
        print("- Interface web interativa")
        print("- Analise cientifica em tempo real")
        print("- Upload de dados por usuarios")
        print("- Hospedagem VPS/Docker")
        
        return True
        
    except Exception as e:
        print(f"\nERRO: {str(e)}")
        return False

if __name__ == "__main__":
    success = demo_system()
    
    if success:
        print("\nSUCESSO! Sistema pronto para NASA Space Apps Challenge!")
    else:
        print("\nFALHA na demonstracao")
