import io
import time
import requests
import threading
import datetime
import base64

import cv2
import numpy as np
import os
from pathlib import Path
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
from streamlit.components.v1 import html
from ultralytics import YOLO

# Placeholder used to show live webcam alerts during detection.
ALERT_ACTIVE_KEY = "active_alert_label"
VOICE_ALERT_HTML = """
<audio id='fire-alert-sound' autoplay hidden>
        <source src='data:audio/wav;base64,{}' type='audio/wav' />
</audio>
<script>
    const audio = document.getElementById('fire-alert-sound');
    if (audio) {{
        // Try to play the tone first, then speak. If play is blocked, still attempt speech.
        setTimeout(() => {{
            audio.play().then(() => {{
                try {{
                    const msg = new SpeechSynthesisUtterance('{}');
                    msg.rate = 0.9;
                    msg.pitch = 1.1;
                    window.speechSynthesis.cancel();
                    window.speechSynthesis.speak(msg);
                }} catch (e) {{ console.log('Speech error', e); }}
            }}).catch((err) => {{
                console.log('Autoplay blocked', err);
                try {{
                    const msg = new SpeechSynthesisUtterance('{}');
                    msg.rate = 0.9;
                    msg.pitch = 1.1;
                    window.speechSynthesis.cancel();
                    window.speechSynthesis.speak(msg);
                }} catch (e) {{ console.log('Speech error', e); }}
            }});
        }}, 200);
    }}
</script>
"""

def generate_alert_message(label: str):
    if label == "fire":
        return "Emergency. Fire detected. Please evacuate and alert people immediately."
    if label == "weapon":
        return "Warning. Weapon or dangerous object detected. Please stay away and alert authorities immediately."
    return f"Alert. {label.capitalize()} detected."

def generate_alert_tone(duration=1.0, freq=880, sample_rate=44100):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    # slightly higher amplitude for better audibility
    tone = 0.8 * np.sin(2 * np.pi * freq * t)
    wav = np.int16(tone * 32767)
    buf = io.BytesIO()
    import wave
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(wav.tobytes())
    return base64.b64encode(buf.getvalue()).decode('ascii')

def _audio_mime_for_path(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".mp3":
        return "audio/mpeg"
    if suffix == ".ogg":
        return "audio/ogg"
    return "audio/wav"

# Prefer a project-level custom alert file if present: assets/alert.wav|mp3|ogg
def _load_project_alert():
    custom_path = Path(r"C:\Users\rohan\Downloads\Final-Aerospy-main\Final-Aerospy-main\31736081-emergency-warning-system-united-states-313128.mp3")
    if custom_path.is_file():
        try:
            data = custom_path.read_bytes()
            return base64.b64encode(data).decode('ascii'), _audio_mime_for_path(custom_path)
        except Exception:
            pass
    root = Path(__file__).resolve().parents[1]
    for ext in ("wav", "mp3", "ogg"):
        p = root / "assets" / f"alert.{ext}"
        if p.is_file():
            try:
                data = p.read_bytes()
                return base64.b64encode(data).decode('ascii'), _audio_mime_for_path(p)
            except Exception:
                continue
    return None, "audio/wav"

_custom_b64, ALERT_AUDIO_MIME = _load_project_alert()
if _custom_b64 is not None:
    ALERT_AUDIO_BASE64 = _custom_b64
else:
    ALERT_AUDIO_BASE64 = generate_alert_tone()
    ALERT_AUDIO_MIME = "audio/wav"


def play_alert_in_browser(audio_b64: str, text: str):
    # Safely escape single quotes in the text
    safe_text = text.replace("'", "\\'")
    script = f"<script>if(window.playAeroSpyAlert){{window.playAeroSpyAlert('{audio_b64}','{ALERT_AUDIO_MIME}','{safe_text}');}}else{{console.log('AeroSpy alert not initialized');}}</script>"
    html(script, height=0)

def handle_alert_playback(alert_label: str):
    prev_alert_label = st.session_state.get(ALERT_ACTIVE_KEY)
    if alert_label in ("fire", "weapon"):
        if sound_alerts and alert_label != prev_alert_label:
            play_alert_in_browser(ALERT_AUDIO_BASE64, generate_alert_message(alert_label))
            st.session_state[ALERT_ACTIVE_KEY] = alert_label
    else:
        st.session_state[ALERT_ACTIVE_KEY] = None

# ================= PAGE CONFIG (MUST BE FIRST) =================
st.set_page_config(page_title="Operate System", layout="wide")

# ================= REACT BANNER =================
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

# Initialize a persistent hidden audio element and a JS helper on the page.
INIT_ALERT_JS = """
<div id='aerospy-audio-root'></div>
<script>
// Create a persistent audio element and a global function to play alerts.
;(function(){
    try {
        const root = document.getElementById('aerospy-audio-root');
        if (!root) return;
        if (!window.playAeroSpyAlert) {
            const audio = document.createElement('audio');
            audio.id = 'aerospy-alert-audio';
            audio.hidden = true;
            root.appendChild(audio);
            window.playAeroSpyAlert = function(b64, mime, text) {
                try {
                    audio.src = 'data:' + mime + ';base64,' + b64;
                    audio.play().then(() => {
                        try {
                            const msg = new SpeechSynthesisUtterance(text);
                            msg.rate = 0.9; msg.pitch = 1.1;
                            window.speechSynthesis.cancel();
                            window.speechSynthesis.speak(msg);
                        } catch (e) { console.log('Speech error', e); }
                    }).catch((err) => {
                        console.log('Audio play blocked', err);
                        try {
                            const msg = new SpeechSynthesisUtterance(text);
                            msg.rate = 0.9; msg.pitch = 1.1;
                            window.speechSynthesis.cancel();
                            window.speechSynthesis.speak(msg);
                        } catch (e) { console.log('Speech error', e); }
                    });
                } catch (e) { console.log('playAeroSpyAlert error', e); }
            };
        }
    } catch (e) { console.log('aerospy init error', e); }
})();
</script>
"""
html(INIT_ALERT_JS, height=0)

st.title("🎥 Operate AI Surveillance System")
st.markdown(
    "<h4 style='color:gray;'>Fire • Person • Vehicle • Weapon Detection</h4>",
    unsafe_allow_html=True
)
st.divider()

# ================= SIDEBAR =================
with st.sidebar:
    st.header("🎛 System Controls")

    source = st.selectbox(
        "Input Source",
        ["Webcam (WebRTC)", "RTSP / HTTP Stream", "Upload Video"]
    )

    st.markdown("### 🎯 Detection Modules")
    enable_fire    = st.checkbox("🔥 Fire Detection",    True)
    enable_person  = st.checkbox("👤 Person Detection",  True)
    enable_vehicle = st.checkbox("🚗 Vehicle Detection", True)
    enable_weapon  = st.checkbox("🔪 Weapon Detection",  True)

    st.markdown("### ⚙ Model Parameters")
    conf_th = st.slider("YOLO Confidence", 0.1, 0.9, 0.35)
    iou_th  = st.slider("YOLO IoU",        0.1, 0.9, 0.5)

    st.divider()
    st.markdown("### 📡 Telegram Alert Settings")

    tg_enabled = st.toggle("Enable Telegram Alerts", value=False)

    tg_token   = st.text_input(
        "Bot Token",
        placeholder="123456789:ABCdef...",
        type="password",
        help="Get from @BotFather on Telegram"
    )
    tg_chat_id = st.text_input(
        "Chat ID",
        placeholder="-100xxxxxxxxxx  or  your user ID",
        help="Send a message to your bot then visit: https://api.telegram.org/bot<TOKEN>/getUpdates"
    )

    alert_cooldown = st.slider(
        "Alert Cooldown (seconds)",
        min_value=5, max_value=120, value=30,
        help="Minimum gap between two alerts for the same threat type"
    )

    alert_on = st.multiselect(
        "Send alert when detected:",
        ["fire", "weapon", "person", "vehicle"],
        default=["fire", "weapon"]
    )

    sound_alerts = st.checkbox("Enable Sound/Voice Alerts", True)

    if st.button("🔔 Test Telegram Connection"):
        if tg_token and tg_chat_id:
            try:
                url  = f"https://api.telegram.org/bot{tg_token}/sendMessage"
                resp = requests.post(url, data={
                    "chat_id": tg_chat_id,
                    "text": "✅ AeroSpy Alert System connected successfully!"
                }, timeout=8)
                if resp.status_code == 200:
                    st.success("✅ Connected! Check your Telegram.")
                else:
                    st.error(f"❌ Failed: {resp.json().get('description','Unknown error')}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.warning("⚠️ Enter Bot Token and Chat ID first.")

# ================= TELEGRAM SENDER =================
_last_alert: dict = {}
_alert_lock = threading.Lock()

def send_telegram_alert(frame_bgr: np.ndarray, label: str):
    if not tg_enabled or not tg_token or not tg_chat_id:
        return
    if label not in alert_on:
        return

    now = time.time()
    with _alert_lock:
        if now - _last_alert.get(label, 0) < alert_cooldown:
            return
        _last_alert[label] = now

    def _send():
        try:
            ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            caption = (
                f"🚨 *AeroSpy Alert*\n"
                f"⚠️ Detected: *{label.upper()}*\n"
                f"🕐 Time: {ts}"
            )
            requests.post(
                f"https://api.telegram.org/bot{tg_token}/sendMessage",
                data={
                    "chat_id": tg_chat_id,
                    "text": f"🚨 AeroSpy Alert: {label.upper()} detected at {ts}",
                    "parse_mode": "Markdown",
                },
                timeout=8,
            )
            _, buf = cv2.imencode(".jpg", frame_bgr, [cv2.IMWRITE_JPEG_QUALITY, 85])
            img_bytes = io.BytesIO(buf.tobytes())
            img_bytes.name = "alert.jpg"

            requests.post(
                f"https://api.telegram.org/bot{tg_token}/sendPhoto",
                data={"chat_id": tg_chat_id, "caption": caption, "parse_mode": "Markdown"},
                files={"photo": img_bytes},
                timeout=10
            )
        except Exception as ex:
            print(f"[Telegram] Send error: {ex}")

    threading.Thread(target=_send, daemon=True).start()

# ================= COLORS =================
COLORS = {
    "person":     (0, 255, 0),
    "car":        (255, 255, 0),
    "motorcycle": (255, 200, 0),
    "bus":        (255, 150, 0),
    "truck":      (255, 100, 0),
    "bicycle":    (255, 220, 100),
    "knife":      (0, 0, 255),
    "weapon":     (0, 0, 255),
    "fire":       (0, 140, 255),
}

PERSON_CLASSES  = ["person"]
VEHICLE_CLASSES = ["car", "bus", "truck", "motorcycle", "bicycle"]
WEAPON_CLASSES  = [
    "knife",
    "scissors",
    "baseball bat",
]

# ================= DRAW FUNCTION =================
def draw_box(img, box, label):
    x1, y1, x2, y2 = map(int, box)
    color = COLORS.get(label, (200, 200, 200))
    cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
    cv2.putText(
        img, label.upper(), (x1, y1 - 6),
        cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2,
    )

# ================= FIRE DETECTOR =================
class FireDetector:
    def detect(self, frame):
        hsv   = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask1 = cv2.inRange(hsv, (0,   80, 180), (50,  255, 255))
        mask2 = cv2.inRange(hsv, (160, 80, 150), (179, 255, 255))
        mask  = cv2.bitwise_or(mask1, mask2)
        mask  = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        boxes = []
        for c in contours:
            if cv2.contourArea(c) > 800:
                x, y, w, h = cv2.boundingRect(c)
                boxes.append((x, y, x + w, y + h))
        return boxes

fire_detector = FireDetector()

# ================= YOLO WRAPPER =================
@st.cache_resource
def load_yolo():
    # Prefer a project-local weights file (located next to the app root) to avoid
    # attempting to download from the internet when running offline.
    root = Path(__file__).resolve().parents[1]
    local_weights = root / "yolov8n.pt"
    try:
        if local_weights.is_file():
            print(f"[AeroSpy] Loading local YOLO weights from: {local_weights}")
            return YOLO(str(local_weights))
        # If local file missing, attempt to load by name (may download)
        print("[AeroSpy] Local weights not found; falling back to YOLO('yolov8n.pt')")
        return YOLO("yolov8n.pt")
    except Exception as e:
        # Log and continue gracefully: return None so app can keep running
        print(f"[AeroSpy] Failed to load YOLO model: {e}")
        return None

yolo_model = load_yolo()

def yolo_detect(frame):
    height, width = frame.shape[:2]
    scale = 1.0
    if max(width, height) > 640:
        scale = 640.0 / max(width, height)
        frame = cv2.resize(frame, (int(width * scale), int(height * scale)))
    if yolo_model is None:
        # Model failed to load; skip detection
        return [], []
    results = yolo_model.predict(frame, conf=conf_th, iou=iou_th, verbose=False)
    boxes, labels = [], []
    if results:
        for b in results[0].boxes:
            label = yolo_model.names[int(b.cls[0])]
            if label in PERSON_CLASSES  and enable_person:
                box = b.xyxy[0].cpu().numpy()
                if scale != 1.0:
                    box = box / scale
                boxes.append(box); labels.append(label)
            elif label in VEHICLE_CLASSES and enable_vehicle:
                box = b.xyxy[0].cpu().numpy()
                if scale != 1.0:
                    box = box / scale
                boxes.append(box); labels.append(label)
            elif label in WEAPON_CLASSES  and enable_weapon:
                box = b.xyxy[0].cpu().numpy()
                if scale != 1.0:
                    box = box / scale
                boxes.append(box); labels.append("weapon")
    return boxes, labels

# ================= PROCESS FRAME =================
def process_frame(img: np.ndarray):
    boxes, labels = [], []
    if enable_person or enable_vehicle or enable_weapon:
        boxes, labels = yolo_detect(img)
    sent_labels = set()
    for box, label in zip(boxes, labels):
        draw_box(img, box, label)
        if label not in sent_labels:
            send_telegram_alert(img, label)
            sent_labels.add(label)

    alert_label = None
    if enable_fire:
        fire_boxes = fire_detector.detect(img)
        fire_alert_sent = False
        for fb in fire_boxes:
            draw_box(img, fb, "fire")
            if not fire_alert_sent:
                send_telegram_alert(img, "fire")
                fire_alert_sent = True
            alert_label = "fire"

    if alert_label == "fire":
        cv2.putText(
            img,
            "EMERGENCY: FIRE DETECTED!",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 0, 255),
            3,
            cv2.LINE_AA,
        )
        return img, alert_label
    weapon_detected = any(label == "weapon" for label in labels)
    if weapon_detected and alert_label is None:
        alert_label = "weapon"
        cv2.putText(
            img,
            "WARNING: WEAPON DETECTED!",
            (10, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.0,
            (0, 0, 255),
            3,
            cv2.LINE_AA,
        )
    return img, alert_label

# ================= WEBRTC PROCESSOR =================
class VideoProcessor(VideoTransformerBase):
    def __init__(self):
        self.current_alert_label = None

    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        img, alert_label = process_frame(img)
        self.current_alert_label = alert_label
        return img

# ================= RTC CONFIG =================
rtc_config = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# ================= ALERT STATUS PANEL =================
st.markdown("### 📡 Alert Status")
col1, col2, col3 = st.columns(3)
col1.metric("Telegram Alerts", "🟢 ON" if tg_enabled else "🔴 OFF")
col2.metric("Cooldown", f"{alert_cooldown}s")
col3.metric("Alert Triggers", ", ".join(alert_on) if alert_on else "None")
st.divider()

fire_alert_placeholder = st.empty()
fire_alert_placeholder.info("⏳ Waiting for video input to start detection...")
fire_audio_placeholder = st.empty()

# ================= MAIN VIEW =================
if source == "Webcam (WebRTC)":
    st.subheader("📷 Live Webcam Detection")
    webrtc_ctx = webrtc_streamer(
        key="webcam-detect",
        video_processor_factory=VideoProcessor,
        rtc_configuration=rtc_config,
        media_stream_constraints={"video": True, "audio": False},
    )

    if webrtc_ctx.video_processor:
        alert_label = webrtc_ctx.video_processor.current_alert_label
        prev_alert_label = st.session_state.get(ALERT_ACTIVE_KEY)

        if alert_label == "fire":
            fire_alert_placeholder.error("🔥 Emergency alert: Fire detected in live webcam feed!")
        elif alert_label == "weapon":
            fire_alert_placeholder.error("⚠️ Weapon detected in live webcam feed!")
        else:
            fire_alert_placeholder.info("✅ Live webcam feed is clear.")
            fire_audio_placeholder.empty()
        handle_alert_playback(alert_label)

elif source == "RTSP / HTTP Stream":
    st.subheader("🌐 RTSP / HTTP Stream")
    stream_url = st.text_input("Enter Stream URL")

    if stream_url:
        cap = cv2.VideoCapture(stream_url)
        frame_area = st.empty()
        stop_btn = st.button("⏹ Stop Stream")

        while cap.isOpened() and not stop_btn:
            ret, frame = cap.read()
            if not ret:
                st.warning("⚠️ Stream ended or could not be read.")
                break
            frame, alert_label = process_frame(frame)
            handle_alert_playback(alert_label)
            frame_area.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        cap.release()

else:
    st.subheader("📁 Upload Video")
    video = st.file_uploader("Upload Video File", type=["mp4", "avi", "mov"])

    if video:
        try:
            import av
        except Exception as e:
            st.error(
                "PyAV is not installed or failed to load. Video upload/decoding is disabled. "
                "Install PyAV and ffmpeg (recommended via conda): `conda install -c conda-forge av ffmpeg`, "
                "or `pip install av` and make sure ffmpeg is on your PATH."
            )
        else:
            container = av.open(video)
            frame_area = st.empty()

            for frame in container.decode(video=0):
                img = frame.to_ndarray(format="bgr24")
                img, alert_label = process_frame(img)
                handle_alert_playback(alert_label)
                frame_area.image(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
