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
        animation: floatTitle 3s ease-in-out infinite alternate, glowPulse 2s ease-in-out infinite;
    }
    @keyframes floatTitle {
        0% { transform: translateY(0px) rotate(-1deg);}
        100% { transform: translateY(-10px) rotate(1deg);}
    }
    @keyframes glowPulse {
        0% { text-shadow: 0 0 24px #00ccff, 3px 3px 6px #000d1a; }
        50% { text-shadow: 0 0 36px #00ccff, 4px 4px 8px #000d1a; }
        100% { text-shadow: 0 0 24px #00ccff, 3px 3px 6px #000d1a; }
    }
    .subtitle {
        font-size: 1.8rem;
        color: #66d9ff;
        text-align: center;
        margin-bottom: 2rem;
        font-style: italic;
        text-shadow: 0 0 12px #66d9ff;
        animation: subtitleFloat 4s ease-in-out infinite alternate;
    }
    @keyframes subtitleFloat {
        0% { transform: translateY(0) scale(1); opacity: 0.8; }
        100% { transform: translateY(-5px) scale(1.02); opacity: 1; }
    }
    .form-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ffffff;
        margin-bottom: 1rem;
        text-align: center;
        letter-spacing: 1px;
        text-shadow: 1px 1px 8px #00ccff;
        animation: formTitlePulse 2s ease-in-out infinite;
    }
    @keyframes formTitlePulse {
        0% { letter-spacing: 1px; }
        50% { letter-spacing: 2px; }
        100% { letter-spacing: 1px; }
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
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        animation: glassBoxAppear 0.6s ease-out;
    }
    @keyframes glassBoxAppear {
        from { 
            opacity: 0;
            transform: translateY(20px) scale(0.98);
        }
        to { 
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    .glass-box:hover {
        box-shadow: 0 12px 48px 0 #00ccff55, 0 2px 12px 0 #001a33;
        transform: translateY(-5px) scale(1.01);
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
        animation: chatContainerAppear 0.5s ease-out;
    }
    @keyframes chatContainerAppear {
        from { 
            opacity: 0;
            transform: scale(0.95);
        }
        to { 
            opacity: 1;
            transform: scale(1);
        }
    }
    .chat-message {
        margin: 16px 0;
        padding: 18px 26px;
        border-radius: 22px;
        font-size: 1.12rem;
        line-height: 1.7;
        box-shadow: 0 2px 16px 0 #000d1a33, 0 0.5px 4px 0 #00ccff33;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        display: flex;
        align-items: center;
        gap: 12px;
        border: 3px solid transparent;
        background-clip: padding-box;
        animation: messageSlideIn 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }
    @keyframes messageSlideIn {
        from { 
            opacity: 0;
            transform: translateY(20px) scale(0.95);
        }
        to { 
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    .user-message {
        background: linear-gradient(120deg, #003366 80%, #00ccff22 100%);
        margin-left: 16%;
        border: 3px solid;
        border-image: linear-gradient(90deg, #00ccff, #003366) 1;
        text-align: right;
        color: #e6ffff;
        box-shadow: 0 0 12px #00ccff44;
        justify-content: flex-end;
        animation: userMessageGlow 2s linear infinite alternate;
    }
    .bot-message {
        background: linear-gradient(120deg, #004080 80%, #66d9ff22 100%);
        margin-right: 16%;
        border: 3px solid;
        border-image: linear-gradient(90deg, #66d9ff, #004080) 1;
        text-align: left;
        color: #ffffff;
        box-shadow: 0 0 12px #66d9ff44;
        justify-content: flex-start;
        animation: botMessageGlow 2s linear infinite alternate;
    }
    @keyframes userMessageGlow {
        0% { box-shadow: 0 0 12px #00ccff44, 0 0 0px #00ccff; }
        50% { box-shadow: 0 0 24px #00ccff88, 0 0 8px #00ccff; }
        100% { box-shadow: 0 0 12px #00ccff44, 0 0 0px #00ccff; }
    }
    @keyframes botMessageGlow {
        0% { box-shadow: 0 0 12px #66d9ff44, 0 0 0px #66d9ff; }
        50% { box-shadow: 0 0 24px #66d9ff88, 0 0 8px #66d9ff; }
        100% { box-shadow: 0 0 12px #66d9ff44, 0 0 0px #66d9ff; }
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
        animation: avatarFloat 2.5s ease-in-out infinite alternate, avatarPulse 2s ease-in-out infinite;
    }
    @keyframes avatarFloat {
        0% { transform: translateY(0px) rotate(0deg); }
        100% { transform: translateY(-6px) rotate(5deg); }
    }
    @keyframes avatarPulse {
        0% { box-shadow: 0 0 8px #00ccff88; }
        50% { box-shadow: 0 0 16px #00ccffaa; }
        100% { box-shadow: 0 0 8px #00ccff88; }
    }
    .user-message .chat-avatar {
        background: #003366;
        color: #00ccff;
        margin-left: 8px;
        margin-right: 0;
        animation: userAvatarFloat 2.5s ease-in-out infinite alternate;
    }
    .bot-message .chat-avatar {
        background: #00ccff;
        color: #003366;
        margin-right: 8px;
        margin-left: 0;
        animation: botAvatarFloat 2.5s ease-in-out infinite alternate;
    }
    @keyframes userAvatarFloat {
        0% { transform: translateY(0px) rotate(0deg); }
        100% { transform: translateY(-6px) rotate(-5deg); }
    }
    @keyframes botAvatarFloat {
        0% { transform: translateY(0px) rotate(0deg); }
        100% { transform: translateY(-6px) rotate(5deg); }
    }
    .chat-input-row {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-top: 22px;
        margin-bottom: 12px;
        animation: inputRowAppear 0.4s ease-out;
    }
    @keyframes inputRowAppear {
        from { 
            opacity: 0;
            transform: translateY(10px);
        }
        to { 
            opacity: 1;
            transform: translateY(0);
        }
    }
    .stTextInput>div>input {
        background-color: #00264d;
        color: #ffffff;
        border: 2px solid #00ccff;
        border-radius: 12px;
        padding: 16px;
        font-size: 1.15rem;
        box-shadow: 0 2px 12px 0 #000d1a33;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .stTextInput>div>input:focus {
        border: 2.5px solid #00ccff;
        background-color: #003366;
        transform: scale(1.02);
        box-shadow: 0 4px 16px 0 #00ccff44;
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
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        outline: none;
        text-shadow: 0 0 8px #00ccff88;
        position: relative;
        overflow: hidden;
    }
    .stButton>button:after {
        content: '';
        position: absolute;
        left: 50%;
        top: 50%;
        width: 0;
        height: 0;
        background: rgba(0,204,255,0.2);
        border-radius: 100%;
        transform: translate(-50%, -50%);
        transition: width 0.3s, height 0.3s;
        z-index: 0;
    }
    .stButton>button:hover:after {
        width: 200%;
        height: 500%;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #003366 60%, #00ccff 100%);
        color: #e6ffff;
        transform: scale(1.07) translateY(-2px);
        box-shadow: 0 0 24px #00ccffcc;
    }
    .stButton>button:active {
        transform: scale(0.98) translateY(1px);
    }
    .divider {
        border: none;
        height: 2.5px;
        background: linear-gradient(90deg, #00ccff 0%, #001a33 100%);
        margin: 36px 0 28px 0;
        border-radius: 2px;
        opacity: 0.8;
        animation: shimmer 2.5s linear infinite, dividerPulse 3s ease-in-out infinite;
    }
    @keyframes shimmer {
        0% { filter: brightness(1); }
        50% { filter: brightness(1.5); }
        100% { filter: brightness(1); }
    }
    @keyframes dividerPulse {
        0% { transform: scaleX(1); }
        50% { transform: scaleX(1.02); }
        100% { transform: scaleX(1); }
    }
    label {
        color: #fff !important;
        font-size: 1.12rem;
        font-weight: bold;
        letter-spacing: 0.5px;
        text-shadow: 0 0 8px #fff, 0 0 2px #00ccff;
        animation: labelPulse 2s ease-in-out infinite;
    }
    @keyframes labelPulse {
        0% { text-shadow: 0 0 8px #fff, 0 0 2px #00ccff; }
        50% { text-shadow: 0 0 12px #fff, 0 0 4px #00ccff; }
        100% { text-shadow: 0 0 8px #fff, 0 0 2px #00ccff; }
    }

    /* Interactive Button Styles */
    .interactive-button {
        background: linear-gradient(135deg, #00ccff22 0%, #00336688 100%);
        border: 2px solid #00ccff44;
        border-radius: 12px;
        padding: 12px 24px;
        color: #ffffff;
        font-weight: 600;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 12px #000d1a33;
        position: relative;
        overflow: hidden;
    }
    .interactive-button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 6px 16px #00ccff44;
        border-color: #00ccff88;
    }
    .interactive-button:active {
        transform: translateY(1px) scale(0.98);
    }
    .interactive-button::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: #00ccff22;
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.3s, height 0.3s;
    }
    .interactive-button:hover::after {
        width: 200%;
        height: 200%;
    }

    /* Info Box Styles */
    .info-box {
        background: rgba(0, 38, 77, 0.8);
        border: 2px solid #00ccff44;
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
        box-shadow: 0 4px 16px #000d1a33;
        animation: infoBoxAppear 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    @keyframes infoBoxAppear {
        from {
            opacity: 0;
            transform: translateY(10px) scale(0.98);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    /* Section Header Styles */
    .section-header {
        color: #00ccff;
        font-size: 1.2rem;
        font-weight: 600;
        margin: 16px 0 8px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #00ccff44;
        animation: headerGlow 2s ease-in-out infinite alternate;
    }
    @keyframes headerGlow {
        from { text-shadow: 0 0 8px #00ccff44; }
        to { text-shadow: 0 0 16px #00ccff88; }
    }

    /* List Item Styles */
    .info-list-item {
        background: rgba(0, 51, 102, 0.4);
        border-left: 3px solid #00ccff;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
        transition: all 0.3s ease;
    }
    .info-list-item:hover {
        background: rgba(0, 51, 102, 0.6);
        transform: translateX(4px);
    }

    /* Divider Styles */
    .fancy-divider {
        height: 2px;
        background: linear-gradient(90deg, 
            transparent 0%, 
            #00ccff44 20%, 
            #00ccff88 50%, 
            #00ccff44 80%, 
            transparent 100%
        );
        margin: 24px 0;
        animation: dividerFlow 3s linear infinite;
    }
    @keyframes dividerFlow {
        from { background-position: 0% 50%; }
        to { background-position: 100% 50%; }
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

# Rename global attack_info to attack_info_dict
attack_info_dict = {
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

# Add attack explanations dictionary with interactive elements
attack_explanations = {
    "CDP Attack": {
        "description": "A CDP (Cisco Discovery Protocol) attack is a network attack that exploits the CDP protocol to gather information about network devices. Attackers can use this information to map the network and potentially launch more targeted attacks.",
        "details": {
            "How it works": "• Attacker sends crafted CDP packets\n• Exploits the information-sharing nature of CDP\n• Can reveal network topology and device details",
            "Impact": "• Network mapping exposure\n• Potential for targeted attacks\n• Security policy compromise",
            "Real-world example": "Attackers can use CDP information to identify critical network devices and plan more sophisticated attacks."
        }
    },
    "OSPF Attack": {
        "description": "OSPF (Open Shortest Path First) attacks target the routing protocol to manipulate routing tables. Attackers can inject false routes or disrupt network communication by sending malicious OSPF packets.",
        "details": {
            "How it works": "• Attacker injects malicious OSPF packets\n• Manipulates routing tables\n• Can redirect traffic through attacker-controlled paths",
            "Impact": "• Traffic redirection\n• Network instability\n• Potential data interception",
            "Real-world example": "Attackers can force traffic through their systems by advertising false routes with better metrics."
        }
    },
    "ICMP Attack": {
        "description": "ICMP (Internet Control Message Protocol) attacks involve flooding a network with ICMP packets, causing network congestion and potential denial of service. Common examples include ping floods and ICMP redirect attacks.",
        "details": {
            "How it works": "• Floods network with ICMP packets\n• Overwhelms network resources\n• Can cause service disruption",
            "Impact": "• Network congestion\n• Service unavailability\n• Resource exhaustion",
            "Real-world example": "Ping floods can overwhelm servers and network devices, causing them to become unresponsive."
        }
    },
    "DHCP Attack": {
        "description": "DHCP (Dynamic Host Configuration Protocol) attacks involve rogue DHCP servers or DHCP starvation. Attackers can assign malicious IP configurations or exhaust the DHCP pool, preventing legitimate devices from getting IP addresses.",
        "details": {
            "How it works": "• Rogue DHCP server deployment\n• DHCP pool exhaustion\n• Malicious IP configuration assignment",
            "Impact": "• Network access issues\n• Man-in-the-middle potential\n• Service disruption",
            "Real-world example": "Attackers can set up rogue DHCP servers to assign malicious DNS servers to clients."
        }
    },
    "MAC Flood Attack": {
        "description": "MAC flooding is a network attack where an attacker floods a switch with fake MAC addresses, causing the switch's MAC address table to overflow. This can lead to the switch behaving like a hub, allowing the attacker to see all network traffic.",
        "details": {
            "How it works": "• Floods switch with fake MAC addresses\n• Overflows MAC address table\n• Forces switch into hub mode",
            "Impact": "• Traffic visibility to attacker\n• Network performance degradation\n• Potential data exposure",
            "Real-world example": "Attackers can capture sensitive data by forcing switches to broadcast all traffic."
        }
    }
}

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Add a key counter to session state
if 'chat_input_key' not in st.session_state:
    st.session_state.chat_input_key = 0

# Function to get chatbot response
def get_chatbot_response(message, prediction_result=None):
    gratitude_responses = [
        "you're welcome!",
        "Glad to help you.",
        "Anytime! Feel free to ask more questions!"
    ]
    
    if prediction_result:
        if prediction_result in attack_info_dict:
            label, tips, _ = attack_info_dict[prediction_result]
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
        elif "explain" in msg:
            for attack_name in attack_explanations.keys():
                if attack_name.lower() in msg:
                    attack_info = attack_explanations[attack_name]
                    response = f'<div class="section-header">🔍 {attack_name}</div>\n\n'
                    response += f'<div class="info-box">'
                    response += f'<div class="section-header">📝 Description</div>'
                    response += f'<div class="info-list-item">{attack_info["description"]}</div>'
                    response += '</div>\n\n'
                    
                    response += '<div class="section-header">📚 Details</div>'
                    for section, content in attack_info['details'].items():
                        response += f'<div class="info-box">'
                        response += f'<div class="section-header">{section}</div>'
                        response += f'<div class="info-list-item">{content}</div>'
                        response += '</div>\n\n'
                    
                    response += '<div class="fancy-divider"></div>'
                    
                    response += '<div class="section-header">💡 Interactive Elements</div>'
                    response += '<div class="info-box">'
                    response += '<div class="info-list-item">• Click "Show Prevention" for protection tips</div>'
                    response += '<div class="info-list-item">• Click "Show Example" for a detailed scenario</div>'
                    response += '<div class="info-list-item">• Click "Show Impact" for potential consequences</div>'
                    response += '</div>'
                    
                    return response
            return "I can explain different types of network attacks. Just ask me to 'explain' followed by the attack type (e.g., 'explain CDP Attack' or 'explain DHCP Attack')."
        else:
            return "I'm here to help with network security. You can ask me to 'explain' different attack types or request tips for protection."

# Function to render interactive explanation
def render_interactive_explanation(attack_name):
    if attack_name in attack_explanations:
        attack_info = attack_explanations[attack_name]
        
        # Create columns for interactive elements
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🛡️ Show Prevention", key=f"prevent_{attack_name}"):
                st.markdown(
                    f'<div class="info-box">'
                    f'<div class="section-header">Prevention Tips</div>'
                    f'<div class="info-list-item">' + 
                    '</div><div class="info-list-item">'.join([f"• {tip}" for tip in attack_info.get("prevention", [])]) +
                    f'</div></div>',
                    unsafe_allow_html=True
                )
        
        with col2:
            if st.button("📋 Show Example", key=f"example_{attack_name}"):
                st.markdown(
                    f'<div class="info-box">'
                    f'<div class="section-header">Real-world Example</div>'
                    f'<div class="info-list-item">{attack_info["details"]["Real-world example"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        
        with col3:
            if st.button("⚠️ Show Impact", key=f"impact_{attack_name}"):
                st.markdown(
                    f'<div class="info-box">'
                    f'<div class="section-header">Impact Analysis</div>'
                    f'<div class="info-list-item">{attack_info["details"]["Impact"]}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        
        # Add fancy divider
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

# Update the chat display section
def display_chat_message(message):
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
        
        # Check if the message contains an attack explanation
        for attack_name in attack_explanations.keys():
            if attack_name in message["content"]:
                render_interactive_explanation(attack_name)

# Update the chat history display
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for message in st.session_state.chat_history:
    display_chat_message(message)
st.markdown('</div>', unsafe_allow_html=True)

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

            if pred_class in attack_info_dict:
                label, tips, _ = attack_info_dict[pred_class]
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
    user_input = st.text_input("Type your message here...", key=f"chat_input_{st.session_state.chat_input_key}")
    send_col, _ = st.columns([1, 5])
    with send_col:
        if st.button("Send", key="send_btn", help="Send your message to the assistant"):
            if user_input:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                bot_response = get_chatbot_response(user_input)
                st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
                # Increment key to clear input
                st.session_state.chat_input_key += 1
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

if not hide_send:
    render_chat_input()

st.markdown('</div>', unsafe_allow_html=True)  # Close glass-box