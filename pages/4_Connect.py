import streamlit as st
from streamlit.components.v1 import html

st.title("📩 Contact Us")
st.markdown("### Get in touch with the AI Fire & Unknown Object Detection Team")

st.divider()

# ---------- General Info ----------
st.subheader("📧 General Contact")

st.info("""
For project demonstrations, academic queries, industrial collaboration,
or government & smart city deployment, please contact our team below.
""")

st.divider()

# ---------- Project Lead ----------
st.subheader("👨‍💻 Project Lead")

st.markdown("""
**Siddhant Pawale**  
*Project Lead | AI & Data Science Engineer*  

📧 **Email:** siddhantpawale@email.com  
📞 **Phone:** +91-XXXXXXXXXX  
🔗 **LinkedIn:** https://www.linkedin.com/in/siddhant-pawale  

🧠 *Primary contact for system design, AI models, and deployment*
""")

st.divider()

# ---------- Team Contacts ----------
st.subheader("🧑‍🔬 Team Members")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    **Jay Wagh**  
    *Computer Vision Engineer*  

    📧 jay.wagh@email.com  
    📞 +91-XXXXXXXXXX  

    🖼️ Image processing & motion detection
    """)

with col2:
    st.markdown("""
    **Rohan More**  
    *Deep Learning Engineer*  

    📧 rohan.more@email.com  
    📞 +91-XXXXXXXXXX  

    🎯 YOLO tuning & model optimization
    """)

with col3:
    st.markdown("""
    **Rutvik Copde**  
    *Frontend & Deployment Engineer*  

    📧 rutvik.copde@email.com  
    📞 +91-XXXXXXXXXX  

    🌐 UI design & application deployment
    """)

st.divider()

# ---------- EmailJS Contact Form ----------
st.subheader("Reach Out to AeroSpy")

EMAILJS_SERVICE_ID = "service_sk30rzg"
EMAILJS_TEMPLATE_ID = "template_0gqj9po"
EMAILJS_PUBLIC_KEY = "h6eoU2hEhxJvAfeuq"

contact_page_html = """
<div class="contact-page">
  <div class="contact-card">
    <div class="contact-panel">
      <h2>Send Us a Message</h2>
      <div id="contact-form-root"></div>
    </div>
  </div>
</div>

<script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
<script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
<script src="https://cdn.jsdelivr.net/npm/emailjs-com@3/dist/email.min.js"></script>
<script>
  const serviceID = 'EMAILJS_SERVICE_ID_PLACEHOLDER';
  const templateID = 'EMAILJS_TEMPLATE_ID_PLACEHOLDER';
  const publicKey = 'EMAILJS_PUBLIC_KEY_PLACEHOLDER';

  emailjs.init(publicKey);
  const e = React.createElement;

  function ContactForm() {
    const [form, setForm] = React.useState({ name: '', email: '', message: '' });
    const [status, setStatus] = React.useState('');

    const updateField = (field) => (event) => {
      setForm({ ...form, [field]: event.target.value });
    };

    const sendEmail = (event) => {
      event.preventDefault();

      if (!form.name || !form.email || !form.message) {
        setStatus('Please fill in all fields.');
        return;
      }

      setStatus('Sending message...');

      emailjs.send(serviceID, templateID, {
        from_name: form.name,
        from_email: form.email,
        message: form.message,
      }).then(
        () => {
          setStatus('✅ Message sent successfully!');
          setForm({ name: '', email: '', message: '' });
        },
        (error) => {
          setStatus('❌ Send failed. Please check your EmailJS credentials.');
          console.error('EmailJS error:', error);
        }
      );
    };

    return e('form', { id: 'contact_form', onSubmit: sendEmail },
      e('label', null, 'Name'),
      e('input', {
        type: 'text',
        value: form.name,
        onChange: updateField('name'),
        placeholder: 'Your name',
        required: true,
      }),
      e('label', null, 'Email'),
      e('input', {
        type: 'email',
        value: form.email,
        onChange: updateField('email'),
        placeholder: 'Your email',
        required: true,
      }),
      e('label', null, 'Message'),
      e('textarea', {
        value: form.message,
        onChange: updateField('message'),
        rows: 6,
        placeholder: 'How can we help?',
        required: true,
      }),
      e('button', { id: 'js-submit', type: 'submit' }, 'Send Message'),
      e('div', { id: 'js-status' }, status)
    );
  }

  ReactDOM.render(
    e(ContactForm),
    document.getElementById('contact-form-root')
  );
</script>

<style>
  .contact-page {
    display: flex;
    justify-content: center;
    width: 100%;
    margin-top: 12px;
  }
  .contact-card {
    width: min(900px, 100%);
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 45%, #0f172a 100%);
    border-radius: 24px;
    padding: 30px;
    color: #f8fafc;
    box-shadow: 0 24px 60px rgba(15, 23, 42, 0.28);
  }
  .contact-panel {
    max-width: 800px;
    margin: 0 auto;
  }
  .contact-panel h2 {
    margin-bottom: 12px;
    font-size: 2rem;
    letter-spacing: 0.02em;
  }
  .contact-panel p {
    margin-bottom: 24px;
    line-height: 1.6;
    color: #cbd5e1;
  }
  #contact_form {
    display: grid;
    gap: 16px;
  }
  label {
    font-weight: 600;
    color: #e2e8f0;
  }
  input, textarea {
    width: 100%;
    border-radius: 14px;
    border: 1px solid rgba(148, 163, 184, 0.35);
    background: rgba(255, 255, 255, 0.08);
    color: #f8fafc;
    padding: 14px 16px;
    font-size: 1rem;
    outline: none;
  }
  input:focus, textarea:focus {
    border-color: #38bdf8;
    box-shadow: 0 0 0 4px rgba(56, 189, 248, 0.15);
  }
  #js-submit {
    border: none;
    border-radius: 14px;
    background: #38bdf8;
    color: #0f172a;
    padding: 14px 22px;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
  }
  #js-submit:hover {
    transform: translateY(-1px);
    background: #22d3ee;
  }
  #js-status {
    min-height: 1.5rem;
    font-weight: 600;
  }
</style>
"""

contact_page_html = contact_page_html.replace(
    "EMAILJS_SERVICE_ID_PLACEHOLDER", EMAILJS_SERVICE_ID
).replace(
    "EMAILJS_TEMPLATE_ID_PLACEHOLDER", EMAILJS_TEMPLATE_ID
).replace(
    "EMAILJS_PUBLIC_KEY_PLACEHOLDER", EMAILJS_PUBLIC_KEY
)

html(contact_page_html, height=720)

st.divider()

st.success("🤝 Open for academic, industrial, military, and smart city collaborations.")
