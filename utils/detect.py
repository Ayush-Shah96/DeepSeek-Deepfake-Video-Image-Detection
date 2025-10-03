"""
Detection Orchestrator - Coordinates image and video analysis
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from analyze.image_analyzer import ImageAnalyzer
from analyze.video_analyzer import VideoAnalyzer
from utils.media_io import MediaHandler

class DeepfakeDetector:
    """Main detector class that orchestrates the analysis"""
    
    def __init__(self, api_key):
        """
        Initialize detector with Gemini API key
        
        Args:
            api_key: Google Gemini API key
        """
        self.api_key = api_key
        self.image_analyzer = ImageAnalyzer(api_key)
        self.video_analyzer = VideoAnalyzer(api_key)
        self.media_handler = MediaHandler()
    
    def analyze_image(self, image_path):
        """
        Analyze an image for deepfake content
        
        Args:
            image_path: Path to the image file
            
        Returns:
            dict: Analysis results
        """
        # Validate file
        if not self.media_handler.validate_image(image_path):
            return {
                'is_deepfake': False,
                'confidence_score': 0,
                'analysis': 'Invalid image file',
                'indicators': [],
                'error': 'File validation failed'
            }
        
        # Perform analysis
        results = self.image_analyzer.analyze(image_path)
        
        # Add metadata
        results['media_type'] = 'image'
        results['file_path'] = image_path
        
        return results
    
    def analyze_video(self, video_path, max_frames=10):
        """
        Analyze a video for deepfake content
        
        Args:
            video_path: Path to the video file
            max_frames: Maximum number of frames to analyze
            
        Returns:
            dict: Analysis results
        """
        # Validate file
        if not self.media_handler.validate_video(video_path):
            return {
                'is_deepfake': False,
                'confidence_score': 0,
                'analysis': 'Invalid video file',
                'indicators': [],
                'frame_analysis': {'total_frames': 0, 'suspicious_frames': 0},
                'error': 'File validation failed'
            }
        
        # Perform analysis
        results = self.video_analyzer.analyze(video_path, max_frames)
        
        # Add metadata
        results['media_type'] = 'video'
        results['file_path'] = video_path
        
        return results
    
    def batch_analyze(self, file_paths, media_type='auto'):
        """
        Analyze multiple files
        
        Args:
            file_paths: List of file paths
            media_type: 'image', 'video', or 'auto' (detect from extension)
            
        Returns:
            list: List of analysis results
        """
        results = []
        
        for file_path in file_paths:
            if media_type == 'auto':
                if self.media_handler.is_image(file_path):
                    result = self.analyze_image(file_path)
                elif self.media_handler.is_video(file_path):
                    result = self.analyze_video(file_path)
                else:
                    result = {
                        'error': 'Unknown file type',
                        'file_path': file_path
                    }
            elif media_type == 'image':
                result = self.analyze_image(file_path)
            else:
                result = self.analyze_video(file_path)
            
            results.append(result)
        
        return results