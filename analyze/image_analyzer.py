"""
Image Analysis Module using Gemini API
"""
import google.generativeai as genai
from PIL import Image
import json

class ImageAnalyzer:
    def __init__(self, api_key):
        """Initialize the image analyzer with Gemini API"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
    def analyze(self, image_path):
        """
        Analyze an image for deepfake/AI-generated content
        
        Args:
            image_path: Path to the image file
            
        Returns:
            dict: Analysis results containing confidence score and details
        """
        try:
            # Load image
            img = Image.open(image_path)
            
            # Create detailed prompt for deepfake detection
            prompt = """Analyze this image for signs of being a deepfake or AI-generated content. 

Please examine the following aspects:
1. **Facial Features**: Irregularities in eyes, teeth, skin texture, facial symmetry
2. **Lighting & Shadows**: Inconsistent lighting, unnatural shadows, mismatched light sources
3. **Background**: Blurry or inconsistent backgrounds, unrealistic elements
4. **Artifacts**: Digital artifacts, blending errors, warping, unnatural edges
5. **Details**: Hair texture, jewelry, reflections, fine details that AI often struggles with
6. **Context**: Overall scene coherence and realism

Provide your analysis in the following JSON format:
{
    "is_deepfake": true/false,
    "confidence_score": 0-100,
    "analysis": "Detailed explanation of your findings",
    "indicators": ["List of specific indicators found"],
    "suspicious_areas": ["Areas that seem manipulated or artificial"]
}

Be thorough and specific in your analysis. Consider both obvious and subtle signs."""

            # Generate analysis
            response = self.model.generate_content([prompt, img])
            
            # Parse response
            result_text = response.text
            
            # Try to extract JSON from response
            try:
                # Clean the response text
                json_start = result_text.find('{')
                json_end = result_text.rfind('}') + 1
                
                if json_start != -1 and json_end > json_start:
                    json_str = result_text[json_start:json_end]
                    result = json.loads(json_str)
                else:
                    # Fallback: create structured result from text
                    result = self._parse_text_response(result_text)
            except json.JSONDecodeError:
                result = self._parse_text_response(result_text)
            
            # Ensure all required fields exist
            result.setdefault('is_deepfake', False)
            result.setdefault('confidence_score', 0)
            result.setdefault('analysis', result_text)
            result.setdefault('indicators', [])
            result.setdefault('suspicious_areas', [])
            
            return result
            
        except Exception as e:
            return {
                'is_deepfake': False,
                'confidence_score': 0,
                'analysis': f'Error during analysis: {str(e)}',
                'indicators': [],
                'suspicious_areas': [],
                'error': str(e)
            }
    
    def _parse_text_response(self, text):
        """Parse text response when JSON extraction fails"""
        # Simple heuristic parsing
        is_deepfake = any(keyword in text.lower() for keyword in 
                          ['deepfake', 'ai-generated', 'artificial', 'synthetic', 'fake', 'manipulated'])
        
        # Estimate confidence based on strength of language
        confidence = 0
        if any(word in text.lower() for word in ['likely', 'probably', 'appears']):
            confidence = 65
        if any(word in text.lower() for word in ['definitely', 'clearly', 'obvious']):
            confidence = 85
        if any(word in text.lower() for word in ['possibly', 'might', 'could']):
            confidence = 40
        
        # Extract indicators (simple sentence splitting)
        indicators = []
        for sentence in text.split('.'):
            if any(keyword in sentence.lower() for keyword in 
                   ['inconsistent', 'unnatural', 'artifact', 'blurr', 'warp', 'irregular']):
                indicators.append(sentence.strip())
        
        return {
            'is_deepfake': is_deepfake,
            'confidence_score': confidence if is_deepfake else 100 - confidence,
            'analysis': text,
            'indicators': indicators[:5],  # Limit to top 5
            'suspicious_areas': []
        }