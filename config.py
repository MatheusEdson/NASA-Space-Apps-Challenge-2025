"""
Configurações do Sistema de Detecção de Exoplanetas
"""

# URLs dos datasets NASA
NASA_DATA_SOURCES = {
    'kepler_koi': {
        'url': 'https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI',
        'table': 'cumulative',
        'params': 'select=*&where=&format=csv',
        'description': 'Kepler Objects of Interest - Confirmados, candidatos e falsos positivos'
    },
    'tess_toi': {
        'url': 'https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI', 
        'table': 'TIC',
        'params': 'select=*&where=&format=csv',
        'description': 'TESS Objects of Interest - Missão TESS'
    },
    'k2_vizier': {
        'url': 'https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI',
        'table': 'exomult', 
        'params': 'select=*&where=&format=csv',
        'description': 'K2 Planets and Candidates - Missão K2'
    }
}

# Características astronômicas importantes
ASTRONOMICAL_FEATURES = {
    'orbital_parameters': [
        'koi_period',      # Período orbital (dias)
        'koi_eccen',       # Excentricidade orbital
        'koi_sep',         # Distância orbital (AU)
        'koi_time0bk'      # Tempo de referência do trânsito
    ],
    'transit_parameters': [
        'koi_duration',    # Duração do trânsito (horas)
        'koi_depth',       # Profundidade do trânsito (%)
        'koi_impact',      # Parâmetro de impacto
        'koi_transit_duration'
    ],
    'planetary_properties': [
        'koi_prad',        # Raio planetário (Terra = 1)
        'koi_mass',        # Massa planetária (kg)
        'koi_density',     # Densidade planetária (g/cm³)
        'koi_teq',         # Temperatura de equilíbrio (K)
        'koi_insol'        # Insolação planetária
    ],
    'stellar_properties': [
        'koi_steff',       # Temperatura efetiva estelar (K)
        'koi_slogg',       # Log da gravidade superficial estelar
        'koi_smass',       # Massa estelar (Solar = 1)
        'koi_srad',        # Raio estelar (Solar = 1)
        'koi_kepmag'       # Magnitude Kepler
    ],
    'quality_flags': [
        'koi_flag',        # Flag de qualidade
        'koi_maxsglerr',   # Erro máximo da gravidade estelar
        'koi_maxsnglerr'   # Erro máximo da densidade estelar
    ]
}

# Configurações de ML
ML_CONFIG = {
    'models': {
        'RandomForest': {
            'n_estimators': 100,
            'max_depth': None,
            'min_samples_split': 2,
            'min_samples_leaf': 1,
            'random_state': 42
        },
        'XGBoost': {
            'n_estimators': 100,
            'max_depth': 6,
            'learning_rate': 0.1,
            'random_state': 42,
            'verbosity': 0
        },
        'LightGBM': {
            'n_estimators': 100,
            'max_depth': 6,
            'learning_rate': 0.1,
            'random_state': 42,
            'verbosity': -1
        }
    },
    'preprocessing': {
        'train_test_split': 0.2,
        'cross_validation_folds': 5,
        'scale_features': True,
        'handle_outliers': True,
        'smote_sampling': True
    },
    'thresholds': {
        'confidence_threshold': 0.8,
        'transit_depth_minimum': 0.0001,  # Mínimo para detectar trânsito
        'orbital_period_max': 1000,       # Período máximo em dias
        'impact_parameter_max': 1.0       # Parâmetro de impacto máximo
    }
}

# Configurações da interface web
WEB_CONFIG = {
    'streamlit': {
        'page_title': '🌌 Sistema de Detecção de Exoplanetas',
        'page_icon': '🚀',
        'layout': 'wide',
        'initial_sidebar_state': 'expanded'
    },
    'dashboard': {
        'update_interval_seconds': 5,
        'max_data_points': 1000,
        'chart_height': 400,
        'color_scheme': {
            'CONFIRMED': '#2E8B57',    # Verde
            'CANDIDATE': '#FFA500',    # Laranja  
            'FALSE POSITIVE': '#DC143C' # Vermelho
        }
    },
    'file_upload': {
        'max_file_size_mb': 50,
        'allowed_formats': ['csv', 'xlsx', 'txt'],
        'sample_rate_limit': 0.1  # Máximo 10% para upload rápido
    }
}

# Configurações de visualização científica
VISUALIZATION_CONFIG = {
    'plot_styles': {
        'figure_size': (12, 8),
        'dpi': 100,
        'style': 'seaborn-v0_8',
        'color_palette': 'viridis'
    },
    'scientific_plots': {
        'transit_light_curves': True,
        'periodogram_analysis': True,
        'correlation_matrices': True,
        'dimensionality_reduction': True,
        'feature_importance': True
    },
    'static_plots': {
        'matplotlib_backend': 'Agg',  # Para servidores
        'figure_cache': True,
        'cache_size_mb': 100
    }
}

# Configurações de análise de trânsitos
TRANSIT_CONFIG = {
    'synthetic_data': {
        'default_period_days': 365.25,
        'default_duration_hours': 8.0,
        'default_depth_percent': 0.01,
        'noise_level': 0.001,
        'sampling_rate_per_hour': 20  # Pontos por hora
    },
    'detection': {
        'minimum_period_hours': 6,
        'transit_threshold_sigma': 2,
        'periodgram_npoints': 1000,
        'confidence_cutoff': 0.5
    },
    'physical_constraints': {
        'stephani_botzmann': 5.670374e-8,  # W m⁻² K⁻⁴
        'stellar_constant': 1361,           # W m⁻²
        'solar_mass': 1.989e30,           # kg
        'earth_mass': 5.97e24,            # kg  
        'earth_radius': 6371000           # m
    }
}

# Casos de uso específicos
EXOPLANET_CASES = {
    'habitable_zone': {
        'description': 'Planetas na zona habitável',
        'criteria': {
            'orbital_period_days': (100, 500),
            'equilibrium_temp_k': (200, 350),
            'stellar_mass': (0.5, 1.5),
            'planet_radius': (0.8, 1.5)
        }
    },
    'hot_jupiters': {
        'description': 'Jupiters quentes',
        'criteria': {
            'orbital_period_days': (1, 10),
            'planet_radius': (8, 15),
            'transit_depth_percent': (0.5, 5.0),
            'bright_star': True
        }
    },
    'super_earths': {
        'description': 'Super-Terras',
        'criteria': {
            'planet_radius': (1.25, 2.0),
            'orbital_period_days': (10, 100),
            'transit_depth_percent': (0.01, 0.1),
            'equilibrium_temp_k': (150, 500)
        }
    }
}

# Configurações de logging
LOGGING_CONFIG = {
    'level': 'INFO',
    'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'file': 'logs/exoplanet_system.log',
    'max_size_mb': 10,
    'backup_count': 3
}

# Configurações de cache
CACHE_CONFIG = {
    'models_cache_dir': 'models/cache/',
    'data_cache_dir': 'data/cache/',
    'visualization_cache_dir': 'results/cache/',
    'cache_timeout_hours': 24,
    'max_cache_size_gb': 2
}

# Configurações de performance
PERFORMANCE_CONFIG = {
    'multiprocessing_cores': 4,
    'memory_limit_gb': 8,
    'batch_size_training': 1000,
    'prefetch_data': True,
    'use_gpu_xgboost': False,
    'profile_execution': False
}

def get_nasa_dataset_url(source_name, custom_params=None):
    """Gera URL completa para dataset NASA"""
    source = NASA_DATA_SOURCES.get(source_name)
    if not source:
        raise ValueError(f"Dataset não encontrado: {source_name}")
    
    params = custom_params or source['params']
    return f"{source['url']}?table={source['table']}&{params}"

def get_feature_categories():
    """Retorna todas as categorias de características"""
    return list(ASTRONOMICAL_FEATURES.keys())

def get_all_features():
    """Retorna todas as características em uma lista"""
    all_features = []
    for category in ASTRONOMICAL_FEATURES.values():
        all_features.extend(category)
    return all_features

def get_ml_model_config(model_name):
    """Retorna configuração específica do modelo ML"""
    return ML_CONFIG['models'].get(model_name, {})

def get_confidence_threshold():
    """Retorna limiar de confiança atual"""
    return ML_CONFIG['thresholds']['confidence_threshold']

def validate_exoplanet_criteria(obj_data, case_type='all'):
    """Valida se objeto atende critérios específicos"""
    if case_type == 'all':
        return True
    
    criteria = EXOPLANET_CASES.get(case_type, {}).get('criteria', {})
    
    for param, (min_val, max_val) in criteria.items():
        value = obj_data.get(param)
        if value is not None and not (min_val <= value <= max_val):
            return False
    
    return True
