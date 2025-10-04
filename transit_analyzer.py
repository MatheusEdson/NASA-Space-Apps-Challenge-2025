"""
Analisador de Séries Temporais de Trânsito de Exoplanetas
Simula análise de dados de fotometria como capturados pelo Kepler/TESS
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import signal
from scipy.optimize import curve_fit
# from astropy.modeling.models import Box1D  # Removido para simplificar dependências
import plotly.express as px

class TransitAnalyzer:
    """Classe para análise de dados de trânsito planetário"""
    
    def __init__(self):
        self.light_curves = {}
        self.transit_params = {}
        
    def generate_synthetic_transit(self, period_days=365.25, duration_hours=8, 
                                 depth_percent=0.01, noise_level=0.001):
        """Gera curva de luz sintética de um trânsito planetário"""
        
        # Parâmetros do trânsito
        period_seconds = period_days * 24 * 3600
        duration_seconds = duration_hours * 3600
        
        # Criar timeline
        total_time = period_days * 24  # horas
        time_points = np.arange(0, total_time, 0.05)  # Resolução de 3 minutos
        
        # Converter profundidade para magnitude
        depth_mag = -2.5 * np.log10(1 - depth_percent/100)
        
        # Gerar curva de luz base
        light_curve = np.ones_like(time_points)
        
        # Adicionar trânsitos
        transit_times = np.arange(0, total_time, period_days * 24)
        
        for transit_time in transit_times:
            # Definir janela do trânsito
            start_time = transit_time - duration_seconds / 3600 / 2
            end_time = transit_time + duration_seconds / 3600 / 2
            
            # Aplicar modelo de trânsito simplificado (caixa)
            transit_mask = (time_points >= start_time) & (time_points <= end_time)
            
            # Aplicar profundidade gradual (simulando formato real de trânsito)
            if np.any(transit_mask):
                transit_indices = np.where(transit_mask)[0]
                n_points = len(transit_indices)
                
                # Criar perfil suave de trânsito
                t_normalized = np.linspace(0, 1, n_points)
                
                # Modelar ingressos/egressos com função sigmoid
                ingress = 1 / (1 + np.exp(-50 * (t_normalized - 0.2)))
                egress = 1 / (1 + np.exp(50 * (t_normalized - 0.8)))
                
                # Profundidade do trânsito
                transit_depth_shape = ingress * (1 - egress)
                transit_depth_value = depth_percent / 100 * transit_depth_shape
                
                light_curve[transit_mask] -= transit_depth_value
        
        # Adicionar ruído realista
        noise = np.random.normal(0, noise_level, len(time_points))
        light_curve += noise
        
        # Armazenar dados
        transit_data = {
            'time': time_points,
            'flux': light_curve,
            'period_days': period_days,
            'duration_hours': duration_hours,
            'depth_percent': depth_percent,
            'noise_level': noise_level
        }
        
        self.light_curves[f"P{period_days:.1f}d_D{depth_percent:.2f}%"] = transit_data
        
        return transit_data
    
    def detect_transits(self, light_curve_data, min_period_hours=6):
        """Detecta trânsitos usando análise de período"""
        
        time = light_curve_data['time']
        flux = light_curve_data['flux']
        
        # Calcular período usando Scargle periodogram
        frequencies = np.logspace(np.log10(1/(24*24)), np.log10(1/(min_period_hours)), 1000)
        
        # Lomb-Scargle periodogram
        power = signal.lombscargle(time, flux, frequencies)
        
        # Find peak frequency
        peak_freq_idx = np.argmax(power)
        detected_period_hours = 24 / frequencies[peak_freq_idx]
        
        # Estimate transit depth
        base_flux = np.median(flux)
        temp_deeper, temp_shallow = np.percentile(flux, [5, 50])
        depth_percent = (temp_shallow - base_flux) / base_flux * 100
        
        return {
            'detected_period_hours': detected_period_hours,
            'detected_period_days': detected_period_hours / 24,
            'power': power,
            'frequencies': frequencies,
            'confidence': power[peak_freq_idx] / np.std(power),
            'estimated_depth_percent': abs(depth_percent)
        }
    
    def analyze_transit_shape(self, light_curve_data):
        """Analisa formato do trânsito"""
        
        time = light_curve_data['time']
        flux = light_curve_data['flux']
        
        # Remover tendência linear
        poly_coefs = np.polyfit(time, flux, 1)
        detrended_flux = flux - np.polyval(poly_coefs, time)
        
        # Normalizar
        detrended_flux = (detrended_flux - np.mean(detrended_flux)) / np.std(detrended_flux)
        
        # Encontrar mergulhadas significativas
        threshold = -2 * np.std(detrended_flux)  # 2-sigma threshold
        
        # Identificar pontos de trânsito
        transit_points = detrended_flux < threshold
        
        if np.any(transit_points):
            transit_indices = np.where(transit_points)[0]
            
            # Calcular estatísticas do trânsito
            transit_start = time[transit_indices[0]]
            transit_end = time[transit_indices[-1]]
            transit_duration = transit_end - transit_start
            
            # Centro do trânsito
            transit_center = (transit_start + transit_end) / 2
            
            # Profundidade máxima
            max_depth_idx = np.argmin(detrended_flux)
            max_depth_time = time[max_depth_idx]
            max_depth_flux = detrended_flux[max_depth_idx]
            
            return {
                'transit_start_time': transit_start,
                'transit_end_time': transit_end,
                'transit_duration_hours': transit_duration,
                'transit_center': transit_center,
                'max_depth_time': max_depth_time,
                'max_depth_flux': max_depth_flux,
                'detrended_flux': detrended_flux
            }
        
        return None
    
    def create_transit_visualization(self, light_curve_data, detection_results=None, shape_analysis=None):
        """Cria visualização completa do trânsito"""
        
        time = light_curve_data['time']
        flux = light_curve_data['flux']
        
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=['Curva de Luz Original', 'Periodograma', 'Analise de Formato'],
            vertical_spacing=0.1
        )
        
        # Curva de luz original
        fig.add_trace(
            go.Scatter(
                x=time,
                y=flux,
                mode='lines',
                name='Curva de Luz',
                line=dict(width=1),
                opacity=0.8
            ),
            row=1, col=1
        )
        
        # Se temos detecção, marcar trânsitos detectados
        if detection_results:
            period_days = detection_results['detected_period_days']
            period_hours = detection_results['detected_period_hours']
            
            # Marcar períodos esperados
            transit_times = np.arange(0, max(time), period_hours)
            for t in transit_times:
                fig.add_vline(x=t, line=dict(color="red", width=2, dash="dash"), 
                             annotation_text=f"T", row=1, col=1)
        
        # Periodograma
        if detection_results:
            frequencies_hours = 24 / detection_results['frequencies']
            
            fig.add_trace(
                go.Scatter(
                    x=frequencies_hours,
                    y=detection_results['power'],
                    mode='lines',
                    name='Periodograma',
                    line=dict(color='blue')
                ),
                row=2, col=1
            )
            
            # Marcar pico detectado
            detected_period = detection_results['detected_period_hours']
            fig.add_vline(x=detected_period, line=dict(color="red", width=3),
                         annotation_text=f"Período detectado: {detected_period:.1f}h", row=2, col=1)
        
        # Análise de formato
        if shape_analysis and 'detrended_flux' in shape_analysis:
            fig.add_trace(
                go.Scatter(
                    x=time,
                    y=shape_analysis['detrended_flux'],
                    mode='lines',
                    name='Formato Normalizado',
                    line=dict(color='green')
                ),
                row=3, col=1
            )
            
            # Marcar características do trânsito
            if 'transit_start_time' in shape_analysis:
                fig.add_vline(x=shape_analysis['transit_start_time'], 
                             line=dict(color="orange", dash="dot"), row=3, col=1)
                fig.add_vline(x=shape_analysis['transit_end_time'], 
                             line=dict(color="orange", dash="dot"), row=3, col=1)
        
        fig.update_layout(height=900, showlegend=True)
        fig.update_xaxes(title_text="Tempo (horas)", row=3, col=1)
        fig.update_yaxes(title_text="Fluxo", row=1, col=1)
        fig.update_yaxes(title_text="Poder", row=2, col=1)
        fig.update_yaxes(title_text="Fluxo Normalizado", row=3, col=1)
        
        return fig
    
    def simulate_multiple_transits(self, n_transits=3):
        """Simula múltiplos trânsitos com parâmetros diferentes"""
        
        transit_scenarios = [
            {'period': 365.25, 'duration': 8, 'depth': 0.01, 'noise': 0.001, 'name': 'Terra-like'},
            {'period': 88, 'duration': 4, 'depth': 0.03, 'noise': 0.002, 'name': 'Mercurio-like'},
            {'period': 12, 'duration': 2, 'depth': 0.005, 'noise': 0.0005, 'name': 'Hot-Jupiter'}
        ]
        
        results = {}
        
        for scenario in transit_scenarios[:n_transits]:
            # Gerar dados sintéticos
            light_curve = self.generate_synthetic_transit(
                period_days=scenario['period'],
                duration_hours=scenario['duration'],
                depth_percent=scenario['depth'],
                noise_level=scenario['noise']
            )
            
            # Detectar trânsitos
            detection = self.detect_transits(light_curve)
            
            # Analisar formato
            shape_analysis = self.analyze_transit_shape(light_curve)
            
            results[scenario['name']] = {
                'light_curve': light_curve,
                'detection': detection,
                'shape': shape_analysis,
                'target_params': scenario
            }
        
        return results
    
    def create_comparison_matrix(self, multi_transit_results):
        """Cria matriz de comparação entre diferentes trânsitos"""
        
        scenarios = list(multi_transit_results.keys())
        n_scenarios = len(scenarios)
        
        fig = make_subplots(
            rows=n_scenarios, cols=1,
            subplot_titles=[f'Cenário: {scenario}' for scenario in scenarios]
        )
        
        colors = ['red', 'blue', 'green', 'orange', 'purple']
        
        for i, scenario in enumerate(scenarios):
            data = multi_transit_results[scenario]
            light_curve = data['light_curve']
            
            fig.add_trace(
                go.Scatter(
                    x=light_curve['time'],
                    y=light_curve['flux'],
                    mode='lines',
                    name=scenario,
                    line=dict(color=colors[i % len(colors)], width=1)
                ),
                row=i+1, col=1
            )
            
            # Adicionar informações sobre detecção
            if 'detection' in data:
                detected_period = data['detection']['detected_period_hours']
                estimated_depth = data['detection']['estimated_depth_percent']
                
                fig.add_annotation(
                    x=0.02, y=0.95,
                    xref=f"x{i+1 if i+1 > 1 else ''}",
                    yref=f"y{i+1 if i+1 > 1 else ''}",
                    text=f"Período: {detected_period:.1f}h<br>Profundidade: {estimated_depth:.3f}%",
                    showarrow=False,
                    font=dict(size=10),
                    bgcolor="rgba(255,255,255,0.8)",
                    bordercolor="black",
                    borderwidth=1
                )
        
        fig.update_layout(
            height=300 * n_scenarios,
            showlegend=False
        )
        
        return fig

def main():
    """Demonstração do analisador de trânsitos"""
    analyzer = TransitAnalyzer()
    
    print("🔍 Simulando análise de trânsitos planetários...")
    
    # Simular um caso Terra-like
    earth_scenario = analyzer.generate_synthetic_transit(
        period_days=365.25,
        duration_hours=8,
        depth_percent=0.01,
        noise_level=0.001
    )
    
    print("📊 Analisando curva de luz...")
    
    # Detectar trânsitos
    detection_results = analyzer.detect_transits(earth_scenario)
    
    # Analisar formato
    shape_analysis = analyzer.analyze_transit_shape(earth_scenario)
    
    print(f"✅ Período detectado: {detection_results['detected_period_days']:.2f} dias")
    print(f"📏 Duração estimada: {shape_analysis['transit_duration_hours']:.1f} horas")
    print(f"📉 Profundidade detectada: {detection_results['estimated_depth_percent']:.4f}%")
    
    # Simular múltiplos cenários
    print("\n🌍 Simulando múltiplos cenários planetários...")
    multiple_results = analyzer.simulate_multiple_transits(n_transits=3)
    
    print("📋 RESULTADOS COMPARATIVOS:")
    for scenario, results in multiple_results.items():
        detection = results['detection']
        target = results['target_params']
        
        print(f"\n{scenario}:")
        print(f"  Período real: {target['period']:.1f} dias")
        print(f"  Período detectado: {detection['detected_period_days']:.1f} dias")
        print(f"  Erro relativo: {abs(target['period'] - detection['detected_period_days'])/target['period']*100:.1f}%")
        print(f"  Confiança: {detection['confidence']:.1f}")
    
    print("\n✅ Análise de trânsitos concluída!")
    print("Execute streamlit_app.py para visualizações interativas")

if __name__ == "__main__":
    main()
