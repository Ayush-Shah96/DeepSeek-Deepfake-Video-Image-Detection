# 🔍 Deepfake Detection System

A comprehensive AI-powered system for detecting deepfakes and AI-generated content in images and videos using Google's Gemini API.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [API Key Setup](#api-key-setup)
- [Technologies Used](#technologies-used)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- 🖼️ **Image Analysis**: Detect deepfakes and AI-generated images
- 🎥 **Video Analysis**: Frame-by-frame video deepfake detection
- 📊 **Confidence Scoring**: Detailed confidence percentages for each analysis
- 🔍 **Detailed Reports**: Comprehensive analysis with specific indicators
- 🎯 **Indicator Detection**: Identifies specific signs of manipulation
- 📈 **Visual Dashboard**: Clean, intuitive Streamlit interface
- ⚡ **Real-time Processing**: Fast analysis powered by Gemini AI
- 🛡️ **Multiple Format Support**: JPG, PNG, WEBP, MP4, AVI, MOV, and more

## 📁 Project Structure

```
deepfake-detector/
│
├── app.py                     # 🔷 Main Streamlit application
├── requirements.txt           # 📦 Python dependencies
├── README.md                  # 📘 Documentation
│
├── analyze/                   # 🧠 Analysis modules
│   ├── __init__.py
│   ├── image_analyzer.py      # Image analysis with Gemini
│   └── video_analyzer.py      # Video analysis with Gemini
│
├── model/                     # 🧪 Model integration
│   ├── __init__.py
│   ├── main.py                # Model loading and inference
│   └── deepfake_model.pt      # (Optional) Custom model weights
│
└── utils/                     # 🛠️ Utility functions
    ├── __init__.py
    ├── detect.py              # Detection orchestrator
    └── media_io.py            # File handling and validation
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Google Gemini API key ([Get one here](https://makersuite.google.com/app/apikey))

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd deepfake-detector
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create Required Directories

```bash
# Create empty __init__.py files
touch analyze/__init__.py
touch model/__init__.py
touch utils/__init__.py
```

## 💻 Usage

### Running the Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the Interface

1. **Enter API Key**: Paste your Gemini API key in the sidebar
2. **Select Media Type**: Choose between Image or Video
3. **Upload File**: Upload your media file
4. **Analyze**: Click the "Analyze Media" button
5. **View Results**: Review the detailed analysis and confidence scores

### Command Line Usage (Optional)

You can also use the detection system programmatically:

```python
from utils.detect import DeepfakeDetector

# Initialize detector
detector = DeepfakeDetector(api_key="your-api-key")

# Analyze an image
result = detector.analyze_image("path/to/image.jpg")
print(f"Is Deepfake: {result['is_deepfake']}")
print(f"Confidence: {result['confidence_score']}%")

# Analyze a video
result = detector.analyze_video("path/to/video.mp4")
print(f"Suspicious Frames: {result['frame_analysis']['suspicious_frames']}")
```

## 🔬 How It Works

### Image Analysis

1. **Upload**: User uploads an image file
2. **Validation**: System validates the file format and integrity
3. **AI Analysis**: Image is sent to Gemini API for analysis
4. **Detection**: AI examines facial features, lighting, artifacts, and inconsistencies
5. **Scoring**: System generates confidence score and detailed report
6. **Display**: Results shown with indicators and recommendations

### Video Analysis

1. **Upload**: User uploads a video file
2. **Frame Extraction**: System extracts key frames (up to 10 frames)
3. **Frame Analysis**: Each frame is analyzed individually
4. **Aggregation**: Results are combined for overall assessment
5. **Temporal Analysis**: Consistency across frames is evaluated
6. **Reporting**: Comprehensive report with frame-by-frame details

### Detection Criteria

The system analyzes multiple aspects:

- **Facial Features**: Eye reflections, teeth, skin texture, symmetry
- **Lighting**: Consistency, shadows, light sources
- **Artifacts**: Digital artifacts, warping, blending errors
- **Background**: Coherence and realism
- **Temporal Consistency**: (Videos) Frame-to-frame consistency
- **Fine Details**: Hair, jewelry, reflections

## 🔑 API Key Setup

### Getting Your Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated key
5. Paste it in the application sidebar

### Security Note

- Never commit your API key to version control
- Store it securely in environment variables for production
- Use `.env` files with `.gitignore` for local development

## 🛠️ Technologies Used

- **Streamlit**: Web interface and UI components
- **Google Gemini AI**: Core AI analysis engine
- **OpenCV**: Video processing and frame extraction
- **Pillow (PIL)**: Image processing and validation
- **Python 3.8+**: Core programming language

## 🚀 Future Enhancements

### Planned Features

- [ ] Custom PyTorch model integration
- [ ] Batch processing for multiple files
- [ ] Export reports as PDF
- [ ] API endpoint for integration
- [ ] Real-time webcam analysis
- [ ] Audio deepfake detection
- [ ] Enhanced temporal analysis for videos
- [ ] Metadata extraction and analysis
- [ ] Cloud storage integration
- [ ] Multi-language support

### Model Integration

The `model/` directory is structured to support custom trained models:

```python
# Example integration
import torch
from model.main import DeepfakeModel

model = DeepfakeModel("model/deepfake_model.pt")
model.load_model()
result = model.predict_image(image_array)
```

## 📊 Performance Notes

- **Image Analysis**: 5-15 seconds per image
- **Video Analysis**: 30-60 seconds for 10 frames
- **Accuracy**: Depends on Gemini API capabilities
- **File Size Limits**: Recommended <50MB for optimal performance

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Disclaimer

This tool is for educational and research purposes. While it uses advanced AI for detection:

- No detection system is 100% accurate
- Always verify important content through multiple sources
- Use as one tool among many in your verification toolkit
- Not a substitute for professional forensic analysis

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powerful analysis capabilities
- Streamlit for excellent UI framework
- OpenCV community for video processing tools
- All contributors and users of this project

## 📧 Support

For issues, questions, or contributions:
- Open an issue on GitHub
- Check existing documentation
- Review closed issues for solutions

---

**Made with ❤️ for a safer digital world**
