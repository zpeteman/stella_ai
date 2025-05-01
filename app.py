import streamlit as st
import base64
from io import BytesIO

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

from core.api import chat_with_rima
from voice.listener import listen
from voice.speaker import speak

# Page configuration
st.set_page_config(page_title="Stella AI", page_icon="🤖", layout="wide")

# Custom CSS for ChatGPT-like interface
st.markdown("""<style>
body {
    color: black !important;
}
.chat-message {
    display: block;
    margin: 10px 0;
    padding: 15px;
    border-radius: 10px;
    max-width: 90%;
    word-wrap: break-word;
    white-space: pre-wrap;
    color: black !important;
    font-size: 16px;
    line-height: 1.5;
    clear: both;
}
.user-message {
    background-color: #e6f2ff;
    float: right;
    text-align: right;
}
.ai-message {
    background-color: #f1f1f1;
    float: left;
    text-align: left;
}
.stTextInput > div > div > input {
    color: black;
}
.chat-container {
    max-height: 400px;
    overflow-y: auto;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 10px;
    margin-bottom: 20px;
    background-color: #f9f9f9;
    clear: both;
}
.chat-message p {
    margin: 0;
    color: black !important;
}
</style>""", unsafe_allow_html=True)

def get_audio_base64(text):
    """Convert text to audio and return base64 encoded audio."""
    tts = gTTS(text=text, lang='en')
    mp3_fp = BytesIO()
    tts.write_to_fp(mp3_fp)
    mp3_fp.seek(0)
    audio_base64 = base64.b64encode(mp3_fp.read()).decode('utf-8')
    return audio_base64

def main():
    st.title("💬 Stella AI")
    
    # Initialize conversation history if not exists
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    
    # Conversation mode selection
    mode = st.sidebar.radio("Interaction Mode", ["Text Chat", "Voice Chat"])
    
    # Input area
    if mode == "Text Chat":
        # Text input with send button
        user_input = st.text_input("Your message:", key="unique_text_input")
        send_button = st.button("Send")
        
        if send_button and user_input:
            # Get AI response
            response = chat_with_rima(user_input, st.session_state.conversation_history)
            
            # Add to conversation history
            st.session_state.conversation_history.append({
                "user": user_input,
                "assistant": response
            })
    
    else:  # Voice Chat
        st.write("🎤 Click 'Start Recording' and speak")
        if st.button("Start Recording"):
            voice_input = listen()
            if voice_input and voice_input.strip():
                # Get AI response
                response = chat_with_rima(voice_input, st.session_state.conversation_history)
                
                # Add to conversation history
                st.session_state.conversation_history.append({
                    "user": voice_input,
                    "assistant": response
                })
    
    # Create a container for chat history
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display conversation history
    for conv in st.session_state.conversation_history:
        # User message
        st.markdown(f'<div class="chat-message user-message"><p>👤 {conv["user"]}</p></div>', unsafe_allow_html=True)
        # AI message
        st.markdown(f'<div class="chat-message ai-message"><p>🤖 {conv["assistant"]}</p></div>', unsafe_allow_html=True)
    
    # Close chat container
    st.markdown('</div>', unsafe_allow_html=True)

# Run the app
main()
