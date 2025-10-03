
# utils/__init__.py
"""
Utility functions for the deepfake detection system
"""
from .detect import DeepfakeDetector
from .media_io import MediaHandler

__all__ = ['DeepfakeDetector', 'MediaHandler']