import streamlit as st
from streamlit.components.v1 import html
from pathlib import Path

# Resolve assets directory relative to this file so images load regardless
# of the current working directory where Streamlit was started.
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"

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

st.title("👥 Our Team")
st.markdown("### Meet the minds behind the AI Fire & Unknown Object Detection System")

st.divider()

# ---- Project Lead ----
col1, col2 = st.columns([1, 3])

with col1:
    try:
        st.image(str(ASSETS_DIR / "siddhant.png"), width=150)
    except:
        st.info("📷 Team photo")

with col2:
    st.markdown("""
    ### 👨‍💻 Siddhant Pawale  
    **Project Lead | AI & Data Science Engineer**

    - System architecture & design  
    - YOLOv8 integration and optimization  
    - Fire & unknown object detection logic  
    - Streamlit + WebRTC integration  
    - Model evaluation and deployment  

    **Academic Background:**  
    B.Tech – Artificial Intelligence 
    """)

st.divider()

# ---- Team Members ----
st.markdown("### 🧑‍🔬 Team Members")

col1, col2, col3 = st.columns(3)

with col1:
    try:
        st.image(str(ASSETS_DIR / "Jay.jpeg"), width=150)
    except:
        st.info("📷 Jay's photo")
    st.markdown("""
    **Jay Wagh**  
    *Computer Vision Engineer*

    - OpenCV image processing  
    - Motion detection algorithms  
    - Background subtraction techniques  
    - Performance optimization

    **Academic Background:**  
    B.Tech – Artificial Intelligence
    """)

with col2:
    try:
        st.image(str(ASSETS_DIR / "rohan pic.png"), width=150)
    except:
        st.info("📷 Rohan's photo")
    st.markdown("""
    **Rohan More**  
    *Deep Learning Engineer*

    - YOLO model tuning  
    - Confidence & IoU optimization  
    - Dataset handling & testing  
    - Accuracy improvement


   **Academic Background:**  
    B.Tech – Artificial Intelligence
    """)

with col3:
    try:
        st.image(str(ASSETS_DIR / "rutvik.jpeg"), width=150)
    except:
        st.info("📷 Rutvik's photo")
    st.markdown("""
    **Rutvik Copde**  
    *Frontend & Deployment Engineer*

    - Streamlit UI design  
    - Multi-page app structure  
    - User interaction & UX  
    - Deployment & testing



    **Academic Background:**  
    B.Tech – Artificial Intelligence
    """)

st.divider()

st.success(
    "🤝 This project is a collaborative effort combining AI, vision, and web technologies for real-world safety solutions."
)
