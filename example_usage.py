"""
Exemplo de Uso do Sistema de Detecção de Exoplanetas
Demonstra todas as funcionalidades principais do sistema
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from exoplanet_ml import ExoplanetDetector
from data_visualizer import ExoplanetVisualizer
from transit_analyzer import TransitAnalyzer
import json

def demonstrate_ml_classification():
    """Demonstra classificação ML de exoplanetas"""
    
    print("🤖 DEMONSTRAÇÃO: Classificação ML de Exoplanetas")
    print("=" * 60)
    
    # Inicializar detector
    detector = ExoplanetDetector()
    
    # Carregar e processar dados
    print("📊 Carregando dados de exemplo...")
    df = detector.prepare_sample_data()
    print(f"   Dataset: {len(df)} objetos")
    
    processed_df, features = detector.preprocess_data(df)
    print(f"   Características analisadas: {len(features)}")
    
    # Treinar modelos
    print("\n🚀 Treinando modelos ML...")
    results, X_test, y_test = detector.train_models(processed_df, features)
    
    print(f"\n📈 RESULTADOS DO TREINAMENTO:")
    for model_name, metrics in results.items():
        print(f"  {model_name}:")
        print(f"    • Acurácia: {metrics['accuracy']:.1%}")
        print(f"    • CV Score: {metrics['cross_val_mean']:.1%} ± {metrics['cross_val_std']:.1%}")
    
    # Predições de exemplo
    print(f"\n🔮 EXEMPLOS DE PREDIÇÕES:")
    
    # Selecionar alguns casos interessantes
    interesting_cases = []
    
    # Caso 1: Potencial planeta habitável (período longo, tamanho similar à Terra)
    case1_idx = processed_df[
        (processed_df['koi_prad'] > 0.8) & (processed_df['koi_prad'] < 1.2) &
        (processed_df['koi_period'] > 200) & (processed_df['koi_period'] < 400)
    ].index[0] if len(processed_df) > 0 else 0
    
    # Caso 2: Hot Jupiter (períodos curtos)
    case2_idx = processed_df[
        (processed_df['koi_period'] < 10) & (processed_df['koi_prad'] > 10)
    ].index[0] if len(processed_df) > 0 else 1
    
    cases = [
        (case1_idx, "Potencial Planeta Habitável"),
        (case2_idx, "Hot Jupiter Candidate")
    ]
    
    for idx, description in cases:
        if idx < len(processed_df):
            data_point = processed_df[features].iloc[idx]
            true_label = processed_df['target'].iloc[idx]
            
            # Buscar palavra descritiva original
            true_class_name = detector.label_encoder.inverse_transform([true_label])[0]
            
            # Fazer predição
            prediction = detector.predict_exoplanet(data_point.values)
            
            print(f"\n  {description}:")
            print(f"    Período: {data_point['koi_period']:.1f} dias")
            print(f"    Raio: {data_point['koi_prad']:.1f} Raio Terra")
            print(f"    Temperatura: {data_point['koi_teq']:.0f} K")
            print(f"    Classificação Real: {true_class_name}")
            print(f"    IA Analisa Como: {prediction['ensemble_prediction']}")
            
            # Mostra probabilidades detalhadas
            for model_name, probs in prediction['probabilities'].items():
                print(f"    {model_name}:")
                for class_name, prob in probs.items():
                    print(f"      {class_name}: {prob:.1%}")
    
    return detector, results

def demonstrate_data_visualization():
    """Demonstra visualização de dados"""
    
    print("\n\n📊 DEMONSTRAÇÃO: Visualização de Dados Astronômicos")
    print("=" * 60)
    
    visualizer = ExoplanetVisualizer()
    
    # Carregar dados
    print("🔭 Gerando dados astronômicos sintéticos...")
    data = visualizer.load_nasa_datasets_sample()
    
    # Gerar relatório de análise
    print("📋 Gerando relatório de análise exploratória...")
    report = visualizer.generate_analysis_report(data)


    print("\n📈 ESTATÍSTICAS GERAIS:")
    print(f"  Total de objetos: {report['total_objects']:,}")
    print(f"  Características analisadas: {report['features_count']}")
    print(f"  Dados faltantes: {report['missing_data']}")
    print(f"  Balanceamento de classes: {report['class_balance']:.2f}")
    
    print(f"\n🎯 DISTRIBUIÇÃO POR CLASSE:")
    for class_name, count in report['class_distribution'].items():
        percentage = count / report['total_objects'] * 100
        print(f"  {class_name}: {count:,} ({percentage:.1f}%)")
    
    print(f"\n🔗 CORRELAÇÕES IMPORTANTES:")
    print("  (Com período orbital - baseado em dados astronômicos)")
    for feature, correlation in report['strong_correlations'].items():
        print(f"  {feature}: {correlation:.3f}")
    
    print(f"\n⚠️  OUTLIERS DETECTADOS:")
    print(f"  Períodos orbitais: {report['outliers_period']}")
    print(f"  Raios planetários: {report['outliers_radius']}")
    
    print("\n💡 INSIGHTS ASTRONÔMICOS:")
    print("  • Períodos orbitais seguem distribuição log-normal")
    print("  • Planetas terrestres concentrados em 0.8-1.5 raios terrestres")
    print("  • Temperaturas de equilíbrio correlacionadas com insolação")
    print("  • Distribuição de massa estelar afeta detectabilidade")
    
    return visualizer, data

def demonstrate_transit_analysis():
    """Demonstra análise de trânsitos"""
    
    print("\n\n⏰ DEMONSTRAÇÃO: Análise de Trânsitos Planetários")
    print("=" * 60)
    
    analyzer = TransitAnalyzer()
    
    print("🌟 Simulando diferentes cenários planetários...")
    
    # Cenários planetários interessantes
    scenarios = [
        {
            'name': '🌍 Terra-Like',
            'período_real': 365.25,
            'duração_real': 13.0,
            'profundidade_real': 0.01,
            'descrição': 'Órbita anual, trânsito ~13h, redução de 0.01%'
        },
        {
            'name': '🔥 Hot Jupiter',
            'período_real': 3.0,
            'duração_real': 2.5,
            'profundidade_real': 1.0,
            'descrição': 'Órbita rápida 3 dias, trânsito ~2.5h, redução de 1%'
        },
        {
            'name': '🌙 Super-Lua',
            'período_real': 28.0,
            'duração_real': 8.0,
            'profundidade_real': 0.05,
            'descrição': 'Planeta pequeno, órbita de 28 dias, detectável'
        }
    ]
    
    results = []
    
    for scenario in scenarios:
        print(f"\n📋 Analisando {scenario['name']}:")
        print(f"   {scenario['descrição']}")
        
        # Simular curva de luz
        light_curve = analyzer.generate_synthetic_transit(
            period_days=scenario['período_real'],
            duration_hours=scenario['duração_real'],
            depth_percent=scenario['profundidade_real'],
            noise_level=0.001
        )
        
        # Detectar trânsito
        detection = analyzer.detect_transits(light_curve)
        
        # Analisar formato
        shape_analysis = analyzer.analyze_transit_shape(light_curve)
        
        # Calcular precisão
        period_error = abs(scenario['período_real'] - detection['detected_period_days'])
        period_error_percent = period_error / scenario['período_real'] * 100
        
        depth_error = abs(scenario['profundidade_real'] - detection['estimated_depth_percent'])
        depth_error_percent = depth_error / scenario['profundidade_real'] * 100
        
        result = {
            'cenario': scenario['name'],
            'periodo_real': scenario['período_real'],
            'periodo_detectado': detection['detected_period_days'],
            'periodo_erro': period_error_percent,
            'profundidade_real': scenario['profundidade_real'],
            'profundidade_detectada': detection['estimated_depth_percent'],
            'profundidade_erro': depth_error_percent,
            'confianca': detection['confidence'],
            'duração_detectada': shape_analysis['transit_duration_hours'] if shape_analysis else 0
        }
        
        results.append(result)
        
        print(f"   ✅ Período detectado: {detection['detected_period_days']:.1f} dias (erro: {period_error_percent:.1f}%)")
        print(f"   📉 Profundidade detectada: {detection['estimated_depth_percent']:.4f}% (erro: {depth_error_percent:.1f}%)")
        print(f"   ⏱️  Duração detectada: {shape_analysis['transit_duration_hours']:.1f}h" if shape_analysis else "   ⏱️  Duração não detectada")
        print(f"   🎯 Confiança: {detection['confidence']:.1f}")
    
    # Resumo comparativo
    print(f"\n📊 RESUMO COMPARATIVO:")
    print(f"{'Cenário':<15} {'Período Erro':<12} {'Profund. Erro':<12} {'Confiança':<10}")
    print("-" * 50)
    
    for result in results:
        print(f"{result['cenario']:<15} {result['periodo_erro']:<12.1f}% {result['profundidade_erro']:<12.1f}% {result['confianca']:<10.1f}")
    
    return analyzer, results

def generate_synthetic_research_dataset():
    """Gera dataset sintético para pesquisa"""
    
    print("\n\n🔬 GERANDO DATASET SINTÉético PARA PESQUISA")
    print("=" * 60)
    
    # Usar o detector para gerar dados pesquisáveis
    detector = ExoplanetDetector()
    
    print("📊 Gerando dataset expandido (5,000 objetos)...")
    
    # Expandir dataset base
    base_data = detector.prepare_sample_data()
    
    # Replicar e modificar dados para criar consistência e padrões
    expanded_data = []
    
    planet_types = [
        {'name': 'Rocky Planets', 'radius_range': (0.5, 1.5), 'period_range': (50, 400), 'weight': 0.4},
        {'name': 'Gas Giants', 'radius_range': (8, 12), 'period_range': (300, 2000), 'weight': 0.3},
        {'name': 'Hot Jupiters', 'radius_range': (8, 12), 'period_range': (1, 10), 'weight': 0.2},
        {'name': 'Mini Neptunes', 'radius_range': (2, 4), 'period_range': (20, 150), 'weight': 0.1}
    ]
    
    samples_per_type = [int(5000 * pt['weight']) for pt in planet_types]
    
    for planet_type, n_samples in zip(planet_types, samples_per_type):
        print(f"  🌍 Gerando {n_samples} {planet_type['name']}...")
        
        for _ in range(n_samples):
            sample = base_data.iloc[np.random.randint(0, len(base_data))].copy()
            
            # Modificar características baseadas no tipo planetário
            sample['koi_prad'] = np.random.uniform(*planet_type['radius_range'])
            sample['koi_period'] = np.random.uniform(*planet_type['period_range'])
            
            # Correlações realistas
            sample['koi_depth'] = (sample['koi_prad'] ** 2) * np.random.uniform(0.0005, 0.001)
            sample['koi_teq'] = 278 * (sample['koi_period']) ** (-0.4) * np.random.uniform(0.8, 1.2)
            
            # Modificar disposição baseada em características
            radius = sample['koi_prad']
            if 0.8 <= radius <= 1.2 and 100 <= sample['koi_period'] <= 400:
                sample['koi_disposition'] = 'CONFIRMED'
            elif radius > 8 and sample['koi_period'] < 20:
                sample['koi_disposition'] = 'CONFIRMED'
            else:
                sample['koi_disposition'] = np.random.choice(
                    ['CANDIDATE', 'FALSE POSITIVE'], 
                    p=[0.7, 0.3]
                )
            
            expanded_data.append(sample)
    
    final_dataset = pd.DataFrame(expanded_data)
    
    # Estatísticas finais
    print(f"\n✅ Dataset pesquisável gerado:")
    print(f"   Total de objetos: {len(final_dataset):,}")
    
    disposition_counts = final_dataset['koi_disposition'].value_counts()
    print(f"   Distribuição por classe:")
    for disp, count in disposition_counts.items():
        print(f"     {disp}: {count:,} ({count/len(final_dataset)*100:.1f}%)")
    
    # Salvar dataset
    output_file = 'data/synthetic_research_dataset.csv'
    final_dataset.to_csv(output_file, index=False)
    print(f"   💾 Salvo em: {output_file}")
    
    return final_dataset

def demonstrate_full_workflow():
    """Demonstra workflow completo do sistema"""
    
    print("\n\n🚀 WORKFLOW COMPLETO DO SISTEMA")
    print("=" * 60)
    
    print("1️⃣ Carregando dataset pesquisável...")
    research_data = generate_synthetic_research_dataset()
    
    print("\n2️⃣ Treinando modelos com dataset expandido...")
    detector = ExoplanetDetector()
    processed_data, features = detector.preprocess_data(research_data)
    results, _, _ = detector.train_models(processed_data, features)
    
    print(f"\n3️⃣ MODELOS OTIMIZADOS:")
    best_model = max(results.items(), key=lambda x: x[1]['accuracy'])
    print(f"   🏆 Melhor modelo: {best_model[0]} ({best_model[1]['accuracy']:.1%})")
    
    print("\n4️⃣ Analisando importância das características...")
    feature_importance = detector.feature_importance
    if feature_importance:
        best_features = sorted(
            zip(features, feature_importance[best_model[0]]), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        
        print("   🎯 Top 5 características:")
        for feature, importance in best_features:
            print(f"     {feature}: {importance:.3f}")
    
    print("\n5️⃣ Simulando análise de novo objeto...")
    
    # Simular análise de objeto potencialmente interessante
    simulation_data = {
        'koi_period': 365.25,    # Órbita terrestre
        'koi_prad': 1.05,        # Ligeiramente menor que Terra
        'koi_teq': 288,          # Temperatura adequada
        'koi_insol': 1.0,        # Insolação terrestre
        'koi_depth': 0.0001,    # Profundidade detectável
        'koi_duration': 13.0,    # Duração do trânsito
        'koi_impact': 0.5,       # Ângulo moderado
        'koi_steff': 5778,       # Temperatura solar
        'koi_smass': 1.0,        # Massa solar
        'koi_srad': 1.0,         # Raio solar
        'koi_kepmag': 12.5       # Magnitude moderada
    }
    
    prediction = detector.predict_exoplanet(list(simulation_data.values()))
    
    print(f"       Objeto simulado:")
    print(f"       Período: {simulation_data['koi_period']} dias")
    print(f"       Raio: {simulation_data['koi_prad']} Raio Terra")
    print(f"       Temperatura: {simulation_data['koi_teq']} K")
    print(f"\n   🤖 Predição IA: {prediction['ensemble_prediction']}")
    print(f"   🎯 Probabilidades:")
    
    for model_name, probs in prediction['probabilities'].items():
        best_class = max(probs.items(), key=lambda x: x[1])
        print(f"     {model_name}: {best_class[0]} ({best_class[1]:.1%})")
    
    print(f"\n✨ SISTEMA PRONTO PARA PESQUISA CIENTÍFICA!")
    print(f"   📊 Dataset: {len(research_data):,} objetos")
    print(f"   🤖 Modelos: {len(results)} treinados")
    print(f"   🎯 Melhor Acurácia: {best_model[1]['accuracy']:.1%}")
    
    return detector, research_data, results

def main():
    """Função principal de demonstração"""
    
    print("DEMONSTRACAO COMPLETA DO SISTEMA DE DETECCAO DE EXOPLANETAS")
    print("NASA Missions Data Analysis with AI/ML")
    print("=" * 80)
    
    try:
        # Demonstração das capacidades principais
        detector, ml_results = demonstrate_ml_classification()
        
        visualizer, viz_data = demonstrate_data_visualization()
        
        analyzer, transit_results = demonstrate_transit_analysis()
        
        # Workflow completo
        final_detector, research_data, final_results = demonstrate_full_workflow()
        
        print("\n\n🎉 TODAS AS DEMONSTRAÇÕES CONCLUÍDAS COM SUCESSO!")
        print("🚀 O sistema está pronto para:")
        print("   🌐 Interface Web Interativa")
        print("   🔬 Pesquisa científica avançada")
        print("   📊 Análise de dados NASA")
        print("   🎯 Classificação automatizada")
        print("   ⚡ Processamento em tempo real")
        
        print(f"\n📋 Para iniciar a interface web, execute:")
        print(f"   python run_system.py")
        print(f"   ou")
        print(f"   streamlit run streamlit_app.py")
        
    except Exception as e:
        print(f"❌ Erro durante demonstração: {str(e)}")
        print("🔧 Execute 'python run_system.py' para diagnóstico completo")

if __name__ == "__main__":
    main()
