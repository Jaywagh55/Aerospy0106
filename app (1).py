import streamlit as st
from PIL import Image
import os

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
    if os.path.exists(path):
        return Image.open(path)
    else:
        st.warning(f"⚠️ Image not found: {path}")
        return None

# --------------------------------------------------
# Paths
# --------------------------------------------------
BANNER_PATH = "assets/banner.jpg"

# --------------------------------------------------
# Header Section
# --------------------------------------------------
banner = load_image(BANNER_PATH)
if banner:
    st.image(banner, width=700)

st.markdown(
    """
    <h1 style='text-align:center;'>🔥 Fire & Unknown Object Detection System</h1>
    <p style='text-align:center; font-size:18px;'>
    AI-based system for detecting fire and unknown objects from images
    </p>
    <hr>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.title("⚙️ Options")
app_mode = st.sidebar.selectbox(
    "Choose Mode",
    ["Home", "Fire Detection", "Unknown Detection", "About"]
)

# --------------------------------------------------
# Home Page
# --------------------------------------------------
if app_mode == "Home":
    st.subheader("🏠 Home")
    st.write("""
    This application uses **Artificial Intelligence & Computer Vision**
    techniques to detect:

    - 🔥 Fire in images
    - ❓ Unknown or suspicious objects
    - 🚨 Early warnings for safety systems

    **Use the sidebar to get started.**
    """)

# --------------------------------------------------
# Fire Detection Page
# --------------------------------------------------
elif app_mode == "Fire Detection":
    st.subheader("🔥 Fire Detection")

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=700)

# --------------------------------------------------
# Unknown Detection Page
# --------------------------------------------------
elif app_mode == "Unknown Detection":
    st.subheader("❓ Unknown Object Detection")

    uploaded_file = st.file_uploader(
        "Upload an image",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=700)

# --------------------------------------------------
# About Page
# --------------------------------------------------
elif app_mode == "About":
    st.subheader("ℹ️ About This Project")
    st.write("""
    **Project Name:** Fire & Unknown Detection System  
    **Domain:** Artificial Intelligence, Computer Vision  
    **Use Cases:**
    - Smart cities
    - Industrial safety
    - Surveillance systems
    - Disaster management

    **Developer:** Siddhant Pawale  
    **Tech Stack:** Python, Streamlit, Deep Learning
    """)

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown(
    """
    <hr>
    <p style='text-align:center;'>
    © 2026 Fire Detection System | Built with ❤️ using Streamlit
    </p>
    """,
    unsafe_allow_html=True
)
