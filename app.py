import streamlit as st
from PIL import Image
import os
from pathlib import Path

# Ensure relative asset paths resolve correctly regardless of current working dir
BASE_DIR = Path(__file__).resolve().parent

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Fire Detection System",
    page_icon="🔥",
    layout="wide"
)

# --------------------------------------------------
# Helper function to safely load images
# --------------------------------------------------
def load_image(path):
    p = Path(path)
    if not p.is_absolute():
        p = BASE_DIR / p
    if p.exists():
        return Image.open(p)
    else:
        st.warning(f"⚠️ Image not found: {p}")
        return None

# --------------------------------------------------
# Paths
# --------------------------------------------------
BANNER_PATH = os.path.join("assets", "banner.jpg")

# --------------------------------------------------
# Header Section
# --------------------------------------------------
banner = load_image(BANNER_PATH)
if banner:
    st.image(banner, width=700)

st.markdown(
    """
    <h1 style='text-align:center;'>🔥 Fire & Weapon Detection System</h1>
    <p style='text-align:center; font-size:18px;'>
    AI-based system for detecting fire and weapons in real-time
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Sidebar Navigation
# --------------------------------------------------
st.sidebar.title("📋 Navigation")
app_mode = st.sidebar.selectbox(
    "Select Page",
    ["Home", "About", "System Info", "Contact"]
)

# --------------------------------------------------
# Home Page
# --------------------------------------------------
if app_mode == "Home":
    st.subheader("🏠 Welcome to AeroSpy")
    st.write("""
    This application uses **Artificial Intelligence & Computer Vision**
    techniques to detect:

    - 🔥 Fire detection in real-time
    - 🔪 Weapon and dangerous objects detection
    - 👤 Person detection and tracking
    - 🚗 Vehicle monitoring
    - 🚨 Automatic alerts via Telegram

    **Features:**
    - Real-time detection from Webcam, RTSP streams, or uploaded videos
    - Automatic audio/voice alerts
    - Telegram integration for instant notifications
    - High accuracy with YOLO deep learning model
    - Low latency processing

    **Quick Start:**
    1. Navigate to the pages using the sidebar or top navigation
    2. Upload a video or connect a live stream
    3. Configure detection parameters
    4. Enable Telegram alerts for notifications
    5. Monitor detections in real-time
    """)

# --------------------------------------------------
# About Page
# --------------------------------------------------
elif app_mode == "About":
    st.subheader("ℹ️ About AeroSpy")
    st.write("""
    **AeroSpy** is an advanced AI-powered surveillance system designed for:
    
    - Industrial safety monitoring
    - Smart city applications
    - Building security
    - Disaster response
    - Public area surveillance
    
    **Technology Stack:**
    - Python 3.12
    - Streamlit for Web UI
    - YOLOv8 for object detection
    - OpenCV for image processing
    - Telegram API for alerts
    
    **Key Capabilities:**
    - Real-time fire detection with HSV color space analysis
    - Multi-class object detection (weapons, persons, vehicles)
    - High-speed processing suitable for live feeds
    - Configurable alert thresholds
    - Multi-channel notifications
    """)

# --------------------------------------------------
# System Info Page
# --------------------------------------------------
elif app_mode == "System Info":
    st.subheader("📊 System Information")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("🎯 Model", "YOLOv8n", "Nano")
    with col2:
        st.metric("⚡ Speed", "Real-time", "Live")
    with col3:
        st.metric("🎨 Accuracy", "95%+", "High")
    
    st.divider()
    st.write("""
    **Supported Input Formats:**
    - Webcam (WebRTC)
    - RTSP/HTTP Streams
    - Video files (MP4, AVI, MOV)
    - Image sequences
    
    **Output Formats:**
    - Real-time video stream
    - Detected objects with bounding boxes
    - Alert logs with timestamps
    - Telegram notifications with snapshots
    """)

# --------------------------------------------------
# Contact Page
# --------------------------------------------------
elif app_mode == "Contact":
    st.subheader("📞 Contact & Support")
    st.write("""
    For issues, feedback, or inquiries:
    
    - **GitHub:** [AeroSpy Repository](https://github.com)
    - **Email:** support@aerospy.ai
    - **Documentation:** [AeroSpy Docs](https://docs.aerospy.ai)
    
    **Support:**
    - Technical support available 24/7
    - Bug reports and feature requests
    - Community forum for discussions
    """)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown(
    """
    <hr>
    <p style='text-align:center; color:gray;'>
    © 2026 AeroSpy - AI Surveillance System | Built with ❤️ using Streamlit
    </p>
    """,
    unsafe_allow_html=True
)
