import streamlit as st
from streamlit.components.v1 import html

# Lightweight React banner (decorative, non-invasive)
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

# ---------- Page Header ----------
st.title("📘 About the Project")
st.markdown(
    "<h4 style='color:gray;'>AI Fire & Unknown Object Detection System</h4>",
    unsafe_allow_html=True
)

st.divider()

# ---------- Intro Section ----------
st.markdown("""
> 🔍 **An Intelligent Surveillance Solution for Real-World Safety**  
This project focuses on **real-time fire detection and unknown object identification**
using **Artificial Intelligence and Computer Vision**, designed for **high-risk and
security-critical environments**.
""")

st.divider()

# ---------- What the System Does ----------
st.subheader("⚙️ What Does This System Do?")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    🔥 **Fire Detection**  
    - Detects fire and flame-like regions in live video  
    - Works in indoor and outdoor environments  
    - Helps in early warning and damage prevention  
    """)

with col2:
    st.markdown("""
    👤 **Unknown Object Detection**  
    - Identifies unidentified persons or objects  
    - Flags suspicious movement or activity  
    - Supports intelligent surveillance systems  
    """)

st.divider()

# ---------- Technology Stack ----------
st.subheader("🧠 Technology Stack")

st.markdown("""
- **YOLOv8** – Real-time object detection  
- **OpenCV** – Video processing & image analysis  
- **HSV-based Fire Detection** – Color-space fire filtering  
- **Background Subtraction** – Motion analysis  
- **Streamlit** – Interactive web interface  
- **WebRTC** – Live camera streaming  
""")

st.divider()

# ---------- Application Domains ----------
st.subheader("🏭 Application Domains")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("🏙️ **Smart Cities**  \nTraffic, crowd & fire monitoring")

with col2:
    st.markdown("🏭 **Industrial Safety**  \nFactories, warehouses, plants")

with col3:
    st.markdown("🪖 **Defense & Military**  \nPerimeter & threat detection")

with col4:
    st.markdown("🏛️ **Government Use**  \nPublic infrastructure protection")

st.divider()

# ---------- Why This Project Matters ----------
st.subheader("🎯 Why This Project Matters")

st.info("""
- Enables **early fire hazard detection**  
- Enhances **public and industrial safety**  
- Reduces dependency on human monitoring  
- Scalable for large-area surveillance  
- Supports AI-driven decision making  
""")

st.divider()

# ---------- Footer ----------
st.markdown(
    "<p style='text-align:center; color:gray;'>"
    "🚀 Developed by Team AeroSpy | AI-Powered Safety & Surveillance System"
    "</p>",
    unsafe_allow_html=True
)
