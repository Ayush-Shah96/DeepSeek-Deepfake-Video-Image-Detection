"""
Video Analysis Module using Gemini API
"""
import google.generativeai as genai
from PIL import Image
import json
import cv2
import tempfile
import os

class VideoAnalyzer:
    def __init__(self, api_key):
        """Initialize the video analyzer with Gemini API"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def analyze(self, video_path, max_frames=10):
        """
        Analyze a video for deepfake content by examining key frames
        
        Args:
            video_path: Path to the video file
            max_frames: Maximum number of frames to analyze
            
        Returns:
            dict: Analysis results containing confidence score and details
        """
        try:
            # Extract key frames
            frames = self._extract_frames(video_path, max_frames)
            
            if not frames:
                return {
                    'is_deepfake': False,
                    'confidence_score': 0,
                    'analysis': 'Could not extract frames from video',
                    'indicators': [],
                    'frame_analysis': {'total_frames': 0, 'suspicious_frames': 0}
                }
            
            # Analyze frames
            frame_results = []
            suspicious_count = 0
            
            for idx, frame_path in enumerate(frames):
                try:
                    img = Image.open(frame_path)
                    
                    prompt = f"""Analyze frame {idx+1}/{len(frames)} of this video for deepfake or AI-generated content.

Focus on:
1. Facial consistency and realism
2. Temporal artifacts (if comparing with previous context)
3. Unnatural movements or transitions
4. Lighting and shadow consistency
5. Background consistency
6. Signs of face-swapping or manipulation

Provide a brief analysis (2-3 sentences) and indicate if this frame seems suspicious."""

                    response = self.model.generate_content([prompt, img])
                    analysis_text = response.text
                    
                    is_suspicious = any(keyword in analysis_text.lower() for keyword in 
                                      ['suspicious', 'fake', 'manipulated', 'artificial', 'unnatural'])
                    
                    if is_suspicious:
                        suspicious_count += 1
                    
                    frame_results.append({
                        'frame_number': idx + 1,
                        'is_suspicious': is_suspicious,
                        'note': analysis_text[:200]  # Truncate for brevity
                    })
                    
                    # Clean up frame file
                    os.unlink(frame_path)
                    
                except Exception as e:
                    frame_results.append({
                        'frame_number': idx + 1,
                        'is_suspicious': False,
                        'note': f'Error analyzing frame: {str(e)}'
                    })
            
            # Generate overall analysis
            overall_prompt = f"""Based on analysis of {len(frames)} frames from a video, where {suspicious_count} frames showed suspicious characteristics:

Provide an overall assessment in JSON format:
{{
    "is_deepfake": true/false,
    "confidence_score": 0-100,
    "analysis": "Overall analysis of the video",
    "indicators": ["List of deepfake indicators found across frames"],
    "temporal_consistency": "Assessment of consistency across frames"
}}

Consider:
- Proportion of suspicious frames ({suspicious_count}/{len(frames)})
- Consistency of artifacts across frames
- Overall realism and coherence"""

            overall_response = self.model.generate_content(overall_prompt)
            overall_text = overall_response.text
            
            # Parse overall result
            try:
                json_start = overall_text.find('{')
                json_end = overall_text.rfind('}') + 1
                
                if json_start != -1 and json_end > json_start:
                    json_str = overall_text[json_start:json_end]
                    result = json.loads(json_str)
                else:
                    result = self._parse_text_response(overall_text, suspicious_count, len(frames))
            except json.JSONDecodeError:
                result = self._parse_text_response(overall_text, suspicious_count, len(frames))
            
            # Add frame analysis
            result['frame_analysis'] = {
                'total_frames': len(frames),
                'suspicious_frames': suspicious_count,
                'frame_details': frame_results
            }
            
            # Ensure required fields
            result.setdefault('is_deepfake', suspicious_count > len(frames) * 0.3)
            result.setdefault('confidence_score', min(95, (suspicious_count / len(frames)) * 100))
            result.setdefault('analysis', overall_text)
            result.setdefault('indicators', [])
            
            return result
            
        except Exception as e:
            return {
                'is_deepfake': False,
                'confidence_score': 0,
                'analysis': f'Error during video analysis: {str(e)}',
                'indicators': [],
                'frame_analysis': {'total_frames': 0, 'suspicious_frames': 0},
                'error': str(e)
            }
    
    def _extract_frames(self, video_path, max_frames):
        """Extract evenly spaced frames from video"""
        frames = []
        
        try:
            cap = cv2.VideoCapture(video_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            if total_frames == 0:
                return []
            
            # Calculate frame interval
            interval = max(1, total_frames // max_frames)
            
            frame_count = 0
            extracted = 0
            
            while extracted < max_frames and cap.isOpened():
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                if frame_count % interval == 0:
                    # Save frame to temp file
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                    cv2.imwrite(temp_file.name, frame)
                    frames.append(temp_file.name)
                    extracted += 1
                
                frame_count += 1
            
            cap.release()
            
        except Exception as e:
            print(f"Error extracting frames: {str(e)}")
        
        return frames
    
    def _parse_text_response(self, text, suspicious_count, total_frames):
        """Parse text response when JSON extraction fails"""
        ratio = suspicious_count / total_frames if total_frames > 0 else 0
        
        is_deepfake = ratio > 0.3 or any(keyword in text.lower() for keyword in 
                                         ['deepfake', 'fake', 'manipulated', 'ai-generated'])
        
        confidence = min(95, int(ratio * 100)) if is_deepfake else max(5, int((1 - ratio) * 100))
        
        indicators = []
        for sentence in text.split('.'):
            if any(keyword in sentence.lower() for keyword in 
                   ['inconsistent', 'unnatural', 'artifact', 'manipulation', 'suspicious']):
                indicators.append(sentence.strip())
        
        return {
            'is_deepfake': is_deepfake,
            'confidence_score': confidence,
            'analysis': text,
            'indicators': indicators[:5]
        }