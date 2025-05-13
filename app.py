import os
from gtts import gTTS
import streamlit as st
import pandas as pd
from src.pipeline.predict_pipeline import CustomData, PredictPipeline
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(page_title="NetKeeper", layout="centered")

# Add custom CSS for styling (enhanced glassmorphism, glow, animated buttons, divider)
st.markdown(
    """
    <style>
    body, .stApp {
        background: linear-gradient(-45deg, #001a33, #00264d, #003366, #00ccff22);
        background-size: 400% 400%;
        animation: gradientBG 18s ease infinite;
        color: #ffffff;
        font-family: 'Poppins', sans-serif;
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    .title {
        font-size: 3.5rem;
        font-weight: bold;
        color: #00ccff;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 0 24px #00ccff, 3px 3px 6px #000d1a;
        filter: drop-shadow(0 0 12px #00ccff);
        animation: floatTitle 3s ease-in-out infinite alternate;
    }
    @keyframes floatTitle {
        0% { transform: translateY(0px);}
        100% { transform: translateY(-10px);}
    }
    .subtitle {
        font-size: 1.8rem;
        color: #66d9ff;
        text-align: center;
        margin-bottom: 2rem;
        font-style: italic;
        text-shadow: 0 0 12px #66d9ff;
    }
    .form-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 1rem;
        text-align: center;
        letter-spacing: 1px;
        text-shadow: 1px 1px 8px #00ccff;
    }
    .glass-box {
        background: rgba(0, 38, 77, 0.55);
        border-radius: 22px;
        box-shadow: 0 8px 32px 0 #001a33, 0 1.5px 8px 0 #00ccff55;
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 2px solid rgba(0, 204, 255, 0.25);
        padding: 28px;
        margin-bottom: 28px;
        transition: box-shadow 0.3s;
    }
    .glass-box:hover {
        box-shadow: 0 12px 48px 0 #00ccff55, 0 2px 12px 0 #001a33;
    }
    .chat-container {
        background: rgba(0, 38, 77, 0.8);
        border-radius: 22px;
        padding: 32px;
        margin: 24px 0;
        max-height: 400px;
        overflow-y: auto;
        box-shadow: 0 4px 32px 0 #001a33, 0 1.5px 8px 0 #00ccff55;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 2px solid #00ccff33;
    }
    .chat-message {
        margin: 16px 0;
        padding: 18px 26px;
        border-radius: 22px;
        font-size: 1.12rem;
        line-height: 1.7;
        box-shadow: 0 2px 16px 0 #000d1a33, 0 0.5px 4px 0 #00ccff33;
        transition: background 0.2s;
        position: relative;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .user-message {
        background: linear-gradient(120deg, #003366 80%, #00ccff22 100%);
        margin-left: 16%;
        border: 2px solid #00ccff;
        text-align: right;
        color: #e6ffff;
        box-shadow: 0 0 12px #00ccff44;
        justify-content: flex-end;
    }
    .bot-message {
        background: linear-gradient(120deg, #004080 80%, #66d9ff22 100%);
        margin-right: 16%;
        border: 2px solid #66d9ff;
        text-align: left;
        color: #ffffff;
        box-shadow: 0 0 12px #66d9ff44;
        justify-content: flex-start;
    }
    .chat-avatar {
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #00ccff;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.3rem;
        color: #001a33;
        box-shadow: 0 0 8px #00ccff88;
        margin-right: 8px;
        margin-left: 8px;
    }
    .user-message .chat-avatar {
        background: #003366;
        color: #00ccff;
        margin-left: 8px;
        margin-right: 0;
    }
    .bot-message .chat-avatar {
        background: #00ccff;
        color: #003366;
        margin-right: 8px;
        margin-left: 0;
    }
    .chat-input-row {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-top: 22px;
        margin-bottom: 12px;
    }
    .stTextInput>div>input {
        background-color: #00264d;
        color: #ffffff;
        border: 2px solid #00ccff;
        border-radius: 12px;
        padding: 16px;
        font-size: 1.15rem;
        box-shadow: 0 2px 12px 0 #000d1a33;
        transition: border 0.2s, background 0.2s;
    }
    .stTextInput>div>input:focus {
        border: 2.5px solid #00ccff;
        background-color: #003366;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00ccff 60%, #003366 100%);
        color: #ffffff;
        font-size: 1.15rem;
        font-weight: bold;
        border-radius: 12px;
        padding: 16px 36px;
        border: none;
        box-shadow: 2px 2px 12px #000d1a;
        transition: background 0.2s, color 0.2s, transform 0.1s, box-shadow 0.2s;
        outline: none;
        text-shadow: 0 0 8px #00ccff88;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #003366 60%, #00ccff 100%);
        color: #e6ffff;
        transform: scale(1.07);
        box-shadow: 0 0 24px #00ccffcc;
    }
    .divider {
        border: none;
        height: 2.5px;
        background: linear-gradient(90deg, #00ccff 0%, #001a33 100%);
        margin: 36px 0 28px 0;
        border-radius: 2px;
        opacity: 0.8;
    }
    label {
        color: #fff !important;
        font-size: 1.12rem;
        font-weight: bold;
        letter-spacing: 0.5px;
        text-shadow: 0 0 8px #fff, 0 0 2px #00ccff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Center the logo using Streamlit's `st.image` with a centered layout
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image("notebook/logo prj.jpg", width=400)

# Set the title of the app
st.markdown('<div class="title">NetKeeper</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Predict the Protocol Type Based on Network Traffic Data</div>', unsafe_allow_html=True)

# Mapping predictions to labels, tips, and images
attack_info = {
    0.0: ("🔴 CDP Attack", [
        "Disable unused CDP services on all network devices.",
        "Segment your network and limit CDP to trusted interfaces only.",
        "Regularly audit Layer 2 configurations.",
        "Use secure management protocols like SSH instead of CDP-based discovery."
    ], None),

    2.0: ("🔴 OSPF Attack", [
        "Use MD5 or SHA authentication for OSPF messages.",
        "Implement passive interfaces where routing updates are not needed.",
        "Monitor routing tables for sudden or suspicious changes.",
        "Use route filtering and summarization to control routing updates."
    ], None),

    1.0: ("🔴 ICMP Attack", [
        "Restrict ICMP traffic using firewall rules.",
        "Limit ICMP rate using router access control lists (ACLs).",
        "Monitor for ICMP floods or ping sweeps using IDS.",
        "Disable ICMP redirect messages on gateways."
    ], None),

    3.0: ("🔴 DHCP Attack", [
        "Enable DHCP snooping on switches to filter rogue servers.",
        "Use port security to limit MAC addresses per port.",
        "Configure trusted ports only for legitimate DHCP servers.",
        "Monitor logs for multiple DHCP OFFER messages."
    ], None),

    4.0: ("🟢 Safe", [], None),

    5.0: ("🔴 MAC Flood Attack", [
        "Enable port security to restrict dynamic MAC addresses.",
        "Limit the number of MAC addresses per interface.",
        "Use dynamic ARP inspection to validate MAC-IP mappings.",
        "Deploy IDS/IPS to detect abnormal MAC behavior."
    ], None)
}

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Function to get chatbot response
def get_chatbot_response(message, prediction_result=None):
    gratitude_responses = [
        "you're welcome!",
        "Glad I could help! Let me know if you need anything else.",
        "Anytime! Feel free to ask more questions."
    ]
    if prediction_result:
        if prediction_result in attack_info:
            label, tips, _ = attack_info[prediction_result]
            if tips:
                return f"Based on the prediction of {label}, here are some tips to protect your network:\n" + "\n".join([f"• {tip}" for tip in tips])
            else:
                return f"Great news! The prediction shows {label}. No specific protection measures are needed."
        else:
            return "I'm not sure about this prediction type. Please consult with a network security expert."
    else:
        msg = message.lower()
        if any(word in msg for word in ["thank you", "thanks", "thx", "appreciate"]):
            import random
            return random.choice(gratitude_responses)
        if "hello" in msg or "hi" in msg:
            return "Hello! I'm your network security assistant. How can I help you today?"
        elif "help" in msg:
            return "I can help you understand network security predictions and provide tips for protection. Just ask me about specific attack types or general security advice."
        else:
            return "I'm here to help with network security. You can ask me about specific attack types or request tips for protection."

# --- Glassmorphism Form Box ---
st.markdown('<div class="glass-box">', unsafe_allow_html=True)
# Create the form using Streamlit widgets
st.markdown('<div class="form-title">Please fill out the details below:</div>', unsafe_allow_html=True)
with st.form("prediction_form"):
    no = st.number_input("Packet Number (No.)", min_value=1, step=1)
    time = st.number_input("Time (in seconds)", min_value=0.0, step=0.01)
    protocol = st.selectbox(
        "Protocol",
        ["Select Protocol", "CDP", "ICMP", "STP", "OSPF", "DHCP", "IPv4", "TCP"]
    )
    length = st.number_input("Packet Length (in bytes)", min_value=1, step=1)
    source_type = st.selectbox(
        "Source Type", ["Select Source Type", "MAC_Address", "IP_Address"]
    )
    destination_type = st.selectbox(
        "Destination Type",
        [
            "Select Destination Type",
            "Network_Protocol",
            "Other_Destination",
            "Multicast",
            "Broadcast",
            "Spanning_Tree_Protocol",
        ]
    )

    submitted = st.form_submit_button("Predict Protocol Type")

# Handle form submission
if submitted:
    if (
        protocol == "Select Protocol"
        or source_type == "Select Source Type"
        or destination_type == "Select Destination Type"
    ):
        st.error("Please fill out all the fields correctly.")
    else:
        data = CustomData(
            no=no,
            time=time,
            protocol=protocol,
            length=length,
            source_type=source_type,
            destination_type=destination_type,
        )

        pred_df = data.get_data_as_data_frame()

        predict_pipeline = PredictPipeline()
        st.write("Starting Prediction...")
        try:
            results = predict_pipeline.predict(pred_df)
            pred_class = float(results[0])

            if pred_class in attack_info:
                label, tips, _ = attack_info[pred_class]
                st.markdown(f'<div class="success">Prediction: {label}</div>', unsafe_allow_html=True)
                
                # Generate and play audio for the prediction
                tts = gTTS(text=f"The prediction is {label}", lang='en')
                audio_file = "prediction_audio.mp3"
                tts.save(audio_file)
                st.audio(audio_file, format="audio/mp3")

                # Add prediction to chat history
                st.session_state.chat_history.append({"role": "assistant", "content": f"Prediction: {label}"})
                
                # Get chatbot response for the prediction
                bot_response = get_chatbot_response("", pred_class)
                st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
            else:
                st.warning("⚠️ Unknown prediction result.")
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")
st.markdown('</div>', unsafe_allow_html=True)  # Close glass-box

# --- Divider ---
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# --- Glassmorphism Chat Box ---
st.markdown('<div class="glass-box">', unsafe_allow_html=True)
st.markdown('<div class="form-title">Chat with Security Assistant</div>', unsafe_allow_html=True)

# Display chat history with avatars
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(
            f'<div class="chat-message user-message">'
            f'<span class="chat-avatar">🧑</span>'
            f'<b>You:</b> {message["content"]}</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f'<div class="chat-message bot-message">'
            f'<span class="chat-avatar">🤖</span>'
            f'<b>Bot:</b> {message["content"]}</div>',
            unsafe_allow_html=True
        )
st.markdown('</div>', unsafe_allow_html=True)

# Check if last bot message was a gratitude response
hide_send = False
gratitude_keywords = ["you're welcome", "glad i could help", "anytime!"]
if st.session_state.chat_history:
    last_msg = st.session_state.chat_history[-1]
    if last_msg["role"] == "assistant" and any(x in last_msg["content"].lower() for x in gratitude_keywords):
        hide_send = True

# Only show input and send button if not hiding
def render_chat_input():
    st.markdown('<div class="chat-input-row">', unsafe_allow_html=True)
    user_input = st.text_input("Type your message here...", key="chat_input")
    send_col, _ = st.columns([1, 5])
    with send_col:
        if st.button("Send", key="send_btn", help="Send your message to the assistant"):
            if user_input:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                bot_response = get_chatbot_response(user_input)
                st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
    st.markdown('</div>', unsafe_allow_html=True)

if not hide_send:
    render_chat_input()

st.markdown('</div>', unsafe_allow_html=True)  # Close glass-box