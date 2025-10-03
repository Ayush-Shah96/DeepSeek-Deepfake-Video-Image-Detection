

# model/__init__.py
"""
Model module for custom ML model integration
"""
from .main import DeepfakeModel, get_model, MODEL_CONFIG

__all__ = ['DeepfakeModel', 'get_model', 'MODEL_CONFIG']