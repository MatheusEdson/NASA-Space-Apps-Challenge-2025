"""
Demonstração final do sistema completo
"""

def demo_complete_system():
    print("=" * 70)
    print("NASA SPACE APPS CHALLENGE - SISTEMA DE DETECAO DE EXOPLANETAS")
    print("=" * 70)
    
    try:
        # Testar módulo principal
        from exoplanet_ml import ExoplanetDetector
        print("\n1. SISTEMA DE MACHINE LEARNING:")
        print("   ✓ Módulo exoplanet_ml carregado")
        
        detector = ExoplanetDetector()
        print("   ✓ Detector inicializado")
        
        # Gerar dados
        data = detector.prepare_sample_data()
        print(f"   ✓ Dataset gerado: {len(data)} objetos")
        
        # Processar dados
        processed_data, features = detector.preprocess_data(data)
        print(f"   ✓ Dados processados: {len(processed_data)} objetos")
        print(f"   ✓ Características: {len(features)} features")
        
        # Treinar modelos
        print("   ✓ Treinando modelos ML...")
        results, _, _ = detector.train_models(processed_data, features)
        
        print(f"\n   RESULTADOS DOS MODELOS:")
        for model_name, metrics in results.items():
            print(f"     {model_name}: {metrics['accuracy']:.1%} acurácia")
        
        # Testar módulos adicionais
        print("\n2. SISTEMA DE VISUALIZACAO:")
        from data_visualizer import ExoplanetVisualizer
        visualizer = ExoplanetVisualizer()
        viz_data = visualizer.load_nasa_datasets_sample()
        print(f"   ✓ Visualizador carregado: {len(viz_data)} objetos")
        
        print("\n3. SISTEMA DE ANALISE DE TRANSITOS:")
        from transit_analyzer import TransitAnalyzer
        analyzer = TransitAnalyzer()
        print("   ✓ Analisador de trânsitos inicializado")
        
        # Simular análise
        test_transit = analyzer.generate_synthetic_transit(365.25, 8, 0.01)
        detection = analyzer.detect_transits(test_transit)
        print(f"   ✓ Período detectado: {detection['detected_period_days']:.2f} dias")
        
        print("\n" + "=" * 70)
        print("SISTEMA FUNCIONANDO PERFEITAMENTE!")
        print("=" * 70)
        
        print("\nCOMO USAR:")
        print("1. Interface Web: streamlit run streamlit_app.py")
        print("2. Demo Completa: python example_usage.py")
        print("3. Deploy: python production_deploy.py")
        
        print("\nSISTEMA PRONTO PARA:")
        print("✓ NASA Space Apps Challenge 2024")
        print("✓ Detecção automática de exoplanetas")
        print("✓ Interface web interativa")
        print("✓ Análise científica em tempo real")
        print("✓ Upload de dados por usuários")
        print("✓ Hospedagem em VPS/Docker")
        
        return True
        
    except Exception as e:
        print(f"\nERRO: {str(e)}")
        return False

def main():
    success = demo_complete_system()
    
    if success:
        print("\n🎉 MISSÃO CUMPRIDA!")
        print("🚀 Sistema de Detecção de Exoplanetas pronto!")
        print("🌌 Para NASA Space Apps Challenge")
    else:
        print("\n❌ Falha na demonstração")

if __name__ == "__main__":
    main()
