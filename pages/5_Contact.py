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

# ---------- Page Header ----------
st.title("📩 Contact Us")
st.markdown(
    "<h4 style='color:gray;'>AI Fire & Unknown Object Detection System</h4>",
    unsafe_allow_html=True
)

st.divider()

# ---------- Intro Section ----------
st.markdown("""
> 🤝 **We’d Love to Hear From You**  
> Team **AeroSpy** is open to academic discussions, project collaborations,
> smart city integration, and industrial safety solutions.
""")

st.divider()

# ---------- Main Contact Card ----------
st.subheader("📌 Team Contact Information")

st.success("""
### 🚀 Team AeroSpy  

📧 **Email:** team.aerospy@gmail.com  
📞 **Contact Number:** +91-XXXXXXXXXX  

📍 **Location:** Maharashtra, India  

🧠 *Specialized in AI-based surveillance, fire detection, and unknown object recognition systems*
""")

st.divider()

# ---------- Use Case Section ----------
st.subheader("💼 Suitable For")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("🏙️ **Smart Cities**  \nPublic safety & monitoring")

with col2:
    st.markdown("🏭 **Industries**  \nFire hazard & restricted area detection")

with col3:
    st.markdown("🪖 **Defense & Security**  \nThreat & anomaly detection")

st.divider()

# ---------- Footer ----------
st.markdown(
    "<p style='text-align:center; color:gray;'>"
    "📡 Team AeroSpy | AI-Powered Safety & Surveillance Solutions"
    "</p>",
    unsafe_allow_html=True
)
