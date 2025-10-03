"""
Deepfake Detection System - Main Streamlit Application
"""
import streamlit as st
import os
from pathlib import Path
from utils.detect import DeepfakeDetector
from utils.media_io import MediaHandler
import tempfile

# Page configuration
st.set_page_config(
    page_title="Deepfake Detection System",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'analysis_complete' not in st.session_state:
    st.session_state.analysis_complete = False
if 'results' not in st.session_state:
    st.session_state.results = None

def main():
    # Header
    st.title("🔍 Deepfake Detection System")
    st.markdown("### Analyze images and videos for AI-generated or manipulated content")
    
    # Sidebar for API key
    with st.sidebar:
        st.header("⚙️ Configuration")
        api_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Enter your Google Gemini API key"
        )
        
        st.markdown("---")
        st.markdown("### 📖 About")
        st.info(
            "This system uses Google's Gemini AI to analyze media files "
            "for signs of deepfake manipulation or AI generation."
        )
        
        st.markdown("### 🎯 Features")
        st.markdown("""
        - Image analysis
        - Video analysis
        - Frame-by-frame detection
        - Confidence scoring
        - Detailed reports
        """)
    
    # Main content
    if not api_key:
        st.warning("⚠️ Please enter your Gemini API key in the sidebar to continue.")
        st.markdown("""
        ### How to get your API key:
        1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Create or select a project
        3. Generate an API key
        4. Paste it in the sidebar
        """)
        return
    
    # Media type selection
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        media_type = st.radio(
            "📁 Select Media Type",
            ["Image", "Video"],
            help="Choose the type of media you want to analyze"
        )
    
    with col2:
        st.markdown(f"### Upload {media_type}")
        
        if media_type == "Image":
            uploaded_file = st.file_uploader(
                "Choose an image file",
                type=["jpg", "jpeg", "png", "webp"],
                help="Supported formats: JPG, PNG, WEBP"
            )
        else:
            uploaded_file = st.file_uploader(
                "Choose a video file",
                type=["mp4", "avi", "mov", "mkv"],
                help="Supported formats: MP4, AVI, MOV, MKV"
            )
    
    # Analysis section
    if uploaded_file is not None:
        st.markdown("---")
        
        # Display uploaded media
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("### 📎 Uploaded Media")
            if media_type == "Image":
                st.image(uploaded_file, use_container_width=True)
            else:
                st.video(uploaded_file)
        
        with col2:
            st.markdown("### 🔬 Analysis")
            
            # Analyze button
            if st.button("🚀 Analyze Media", type="primary", use_container_width=True):
                with st.spinner("🔍 Analyzing media... This may take a moment."):
                    try:
                        # Save uploaded file temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_path = tmp_file.name
                        
                        # Initialize detector
                        detector = DeepfakeDetector(api_key)
                        
                        # Perform analysis
                        if media_type == "Image":
                            results = detector.analyze_image(tmp_path)
                        else:
                            results = detector.analyze_video(tmp_path)
                        
                        # Store results
                        st.session_state.results = results
                        st.session_state.analysis_complete = True
                        
                        # Clean up temp file
                        os.unlink(tmp_path)
                        
                        st.success("✅ Analysis complete!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Error during analysis: {str(e)}")
                        if os.path.exists(tmp_path):
                            os.unlink(tmp_path)
        
        # Display results
        if st.session_state.analysis_complete and st.session_state.results:
            st.markdown("---")
            display_results(st.session_state.results, media_type)

def display_results(results, media_type):
    """Display analysis results in a formatted manner"""
    st.markdown("## 📊 Analysis Results")
    
    # Overall verdict
    is_fake = results.get('is_deepfake', False)
    confidence = results.get('confidence_score', 0)
    
    # Color-coded verdict
    if is_fake:
        verdict_color = "🔴"
        verdict_text = "LIKELY DEEPFAKE/AI-GENERATED"
        alert_type = "error"
    else:
        verdict_color = "🟢"
        verdict_text = "LIKELY AUTHENTIC"
        alert_type = "success"
    
    # Display verdict
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if alert_type == "error":
            st.error(f"{verdict_color} **{verdict_text}**")
        else:
            st.success(f"{verdict_color} **{verdict_text}**")
    
    # Metrics
    st.markdown("### 📈 Detection Metrics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Confidence Score", f"{confidence:.1f}%")
    
    with col2:
        st.metric("Authenticity", f"{100 - confidence:.1f}%")
    
    with col3:
        risk_level = "High" if confidence > 70 else "Medium" if confidence > 40 else "Low"
        st.metric("Risk Level", risk_level)
    
    # Detailed analysis
    st.markdown("### 🔍 Detailed Analysis")
    
    with st.expander("📝 Full Analysis Report", expanded=True):
        st.markdown(results.get('analysis', 'No detailed analysis available.'))
    
    # Indicators found
    if 'indicators' in results and results['indicators']:
        with st.expander("⚠️ Deepfake Indicators Detected"):
            for idx, indicator in enumerate(results['indicators'], 1):
                st.markdown(f"**{idx}.** {indicator}")
    
    # Video-specific results
    if media_type == "Video" and 'frame_analysis' in results:
        with st.expander("🎬 Frame-by-Frame Analysis"):
            frame_data = results['frame_analysis']
            st.markdown(f"**Total Frames Analyzed:** {frame_data.get('total_frames', 0)}")
            st.markdown(f"**Suspicious Frames:** {frame_data.get('suspicious_frames', 0)}")
            
            if frame_data.get('frame_details'):
                st.markdown("#### Sample Frames:")
                for frame_info in frame_data['frame_details'][:5]:
                    st.markdown(f"- Frame {frame_info.get('frame_number', 'N/A')}: {frame_info.get('note', 'N/A')}")
    
    # Recommendations
    st.markdown("### 💡 Recommendations")
    
    if is_fake:
        st.warning("""
        **This media shows signs of manipulation or AI generation. Consider:**
        - Verifying the source
        - Looking for corroborating evidence
        - Checking metadata
        - Consulting additional verification tools
        - Being cautious about sharing
        """)
    else:
        st.info("""
        **This media appears authentic, but:**
        - No detection system is 100% accurate
        - Always verify important content through multiple sources
        - Check the original source when possible
        """)
    
    # Reset button
    if st.button("🔄 Analyze Another File", use_container_width=True):
        st.session_state.analysis_complete = False
        st.session_state.results = None
        st.rerun()

if __name__ == "__main__":
    main()