"""
Media Input/Output Handler - File operations and validation
"""
import os
from pathlib import Path
from PIL import Image
import cv2

class MediaHandler:
    """Handles media file operations, validation, and processing"""
    
    # Supported file extensions
    IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.gif'}
    VIDEO_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv'}
    
    def __init__(self):
        """Initialize media handler"""
        pass
    
    def validate_image(self, file_path):
        """
        Validate if file is a valid image
        
        Args:
            file_path: Path to the file
            
        Returns:
            bool: True if valid image, False otherwise
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return False
            
            # Check extension
            if not self.is_image(file_path):
                return False
            
            # Try to open with PIL
            img = Image.open(file_path)
            img.verify()
            
            return True
            
        except Exception as e:
            print(f"Image validation error: {str(e)}")
            return False
    
    def validate_video(self, file_path):
        """
        Validate if file is a valid video
        
        Args:
            file_path: Path to the file
            
        Returns:
            bool: True if valid video, False otherwise
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                return False
            
            # Check extension
            if not self.is_video(file_path):
                return False
            
            # Try to open with OpenCV
            cap = cv2.VideoCapture(file_path)
            
            if not cap.isOpened():
                return False
            
            # Try to read first frame
            ret, frame = cap.read()
            cap.release()
            
            return ret
            
        except Exception as e:
            print(f"Video validation error: {str(e)}")
            return False
    
    def is_image(self, file_path):
        """
        Check if file is an image based on extension
        
        Args:
            file_path: Path to the file
            
        Returns:
            bool: True if image extension
        """
        ext = Path(file_path).suffix.lower()
        return ext in self.IMAGE_EXTENSIONS
    
    def is_video(self, file_path):
        """
        Check if file is a video based on extension
        
        Args:
            file_path: Path to the file
            
        Returns:
            bool: True if video extension
        """
        ext = Path(file_path).suffix.lower()
        return ext in self.VIDEO_EXTENSIONS
    
    def get_image_info(self, file_path):
        """
        Get image metadata
        
        Args:
            file_path: Path to the image
            
        Returns:
            dict: Image information
        """
        try:
            img = Image.open(file_path)
            
            return {
                'format': img.format,
                'mode': img.mode,
                'size': img.size,
                'width': img.width,
                'height': img.height,
                'file_size': os.path.getsize(file_path)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def get_video_info(self, file_path):
        """
        Get video metadata
        
        Args:
            file_path: Path to the video
            
        Returns:
            dict: Video information
        """
        try:
            cap = cv2.VideoCapture(file_path)
            
            if not cap.isOpened():
                return {'error': 'Could not open video'}
            
            info = {
                'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
                'fps': cap.get(cv2.CAP_PROP_FPS),
                'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
                'duration': int(cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)) if cap.get(cv2.CAP_PROP_FPS) > 0 else 0,
                'file_size': os.path.getsize(file_path)
            }
            
            cap.release()
            return info
            
        except Exception as e:
            return {'error': str(e)}
    
    def extract_frame(self, video_path, frame_number, output_path=None):
        """
        Extract a specific frame from video
        
        Args:
            video_path: Path to the video
            frame_number: Frame number to extract
            output_path: Path to save the frame (optional)
            
        Returns:
            numpy.ndarray or str: Frame array or path to saved frame
        """
        try:
            cap = cv2.VideoCapture(video_path)
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
            
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                return None
            
            if output_path:
                cv2.imwrite(output_path, frame)
                return output_path
            
            return frame
            
        except Exception as e:
            print(f"Frame extraction error: {str(e)}")
            return None
    
    def resize_image(self, image_path, max_size=(1920, 1080), output_path=None):
        """
        Resize image while maintaining aspect ratio
        
        Args:
            image_path: Path to the image
            max_size: Maximum dimensions (width, height)
            output_path: Path to save resized image (optional)
            
        Returns:
            str or PIL.Image: Path to saved image or Image object
        """
        try:
            img = Image.open(image_path)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            if output_path:
                img.save(output_path)
                return output_path
            
            return img
            
        except Exception as e:
            print(f"Image resize error: {str(e)}")
            return None
    
    def get_file_extension(self, file_path):
        """
        Get file extension
        
        Args:
            file_path: Path to the file
            
        Returns:
            str: File extension (lowercase)
        """
        return Path(file_path).suffix.lower()