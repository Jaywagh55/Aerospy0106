import streamlit as st
from streamlit.components.v1 import html

react_banner = """
<div id="aerospy-banner-root"></div>
<script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
<script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
<script>
    const e = React.createElement;
    function Banner(){
        return e('div', {style: {padding: '8px', textAlign: 'center', background: '#061826', color: '#fff', borderRadius: '8px'}}, e('strong', null, 'AeroSpy — AI Surveillance'))
    }
    ReactDOM.render(e(Banner), document.getElementById('aerospy-banner-root'));
</script>
<style>#aerospy-banner-root{margin-bottom:12px;}</style>
"""
html(react_banner, height=72)

st.title("⚙️ System Information")
st.markdown("### AI Fire & Unknown Object Detection – Technical Overview")

st.divider()

# ---------- System Overview ----------
st.subheader("🧠 System Overview")

st.markdown("""
This AI-powered surveillance system performs **real-time fire detection and unknown object identification**
using **Deep Learning, Computer Vision, and intelligent motion analysis**.
It is designed for **high reliability, fast response, and real-world deployment**.
""")

st.info("⚡ Real-time | 🎯 Accurate | 🔒 Reliable | 🌐 Scalable")

st.divider()

# ---------- Architecture ----------
st.subheader("🏗️ System Architecture")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Input Sources**
    - 🎥 Live Webcam (WebRTC)
    - 📡 RTSP / CCTV Streams
    - 📁 Uploaded Video Files
    """)

with col2:
    st.markdown("""
    **Processing Pipeline**
    - 🧠 YOLOv8 Object Detection
    - 🔥 Fire Detection (HSV + Flicker)
    - ❓ Unknown Object Detection
    - 🖼️ Frame Annotation
    """)

st.divider()

# ---------- Detection Modules ----------
st.subheader("🔍 Detection Modules")

col1, col2, col3 = st.columns(3)

with col1:
    st.success("""
    🔥 **Fire Detection**
    - HSV color segmentation  
    - Flickering motion analysis  
    - Contour & solidity checks  
    - Early hazard alerts
    """)

with col2:
    st.warning("""
    ❓ **Unknown Object Detection**
    - Background subtraction (MOG2)  
    - Motion-based detection  
    - IoU filtering with known objects  
    - Intrusion identification
    """)

with col3:
    st.info("""
    🎯 **YOLOv8 Detection**
    - Real-time object recognition  
    - Optimized confidence & IoU  
    - Lightweight YOLOv8n model  
    - High-speed inference
    """)

st.divider()

# ---------- Performance ----------
st.subheader("🚀 Performance & Optimization")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    **Performance Features**
    - Real-time frame processing  
    - Dynamic frame resizing  
    - GPU acceleration (optional)  
    - Low-latency WebRTC streaming
    """)

with col2:
    st.markdown("""
    **Optimization Techniques**
    - Lightweight model selection  
    - Efficient OpenCV pipelines  
    - Frame skipping & scaling  
    - Background modeling
    """)

st.divider()

# ---------- Deployment ----------
st.subheader("☁️ Deployment & Scalability")

st.markdown("""
- Deployable on **local machines**, **edge devices**, and **cloud servers**
- Compatible with **Smart City**, **Industrial Safety**, and **Defense systems**
- Easily extendable with **alerts, dashboards, and IoT integration**
""")

st.success("✅ Designed for real-world surveillance, safety, and emergency response systems.")
