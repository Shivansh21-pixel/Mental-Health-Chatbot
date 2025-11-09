import streamlit as st
from transformers import pipeline
import random

# ---------- LOAD MODEL ----------
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="microsoft/DialoGPT-medium")

generator = load_model()

# ---------- EMOTION DETECTOR ----------
def detect_emotion(text):
    text = text.lower()
    if any(word in text for word in ["sad", "depressed", "unhappy", "alone"]):
        return "sad", "🥲", random.choice([
            "I'm really sorry you're feeling low today. Remember, it's okay to express your feelings 💙",
            "It’s alright to feel sad sometimes. You’re not alone 💫",
            "Want to talk about what’s making you feel down? I’m here for you 🌙"
        ])
    elif any(word in text for word in ["angry", "mad", "furious", "annoyed"]):
        return "angry", "😡", random.choice([
            "Anger can be intense, but it often hides pain underneath ❤️",
            "Take a deep breath. You deserve peace and calm 🧘",
            "It’s okay to be angry. Let’s understand what caused it 💭"
        ])
    elif any(word in text for word in ["happy", "good", "great", "joy", "excited"]):
        return "happy", "😊", random.choice([
            "That's wonderful to hear! Keep spreading those positive vibes 🌟",
            "Happiness looks good on you 😄",
            "I'm so glad you're feeling good today! 🌈"
        ])
    elif any(word in text for word in ["scared", "afraid", "nervous", "anxious"]):
        return "anxious", "😰", random.choice([
            "It’s okay to feel anxious — breathe deeply, you're safe 💜",
            "You are stronger than your worries 🌻",
            "Let’s take things one step at a time, you’re doing fine 🌼"
        ])
    else:
        return "neutral", "💬", random.choice([
            "Tell me more about what’s on your mind 💭",
            "I’m listening, go ahead 👂",
            "That sounds interesting — how are you coping with it?"
        ])

# ---------- PAGE DESIGN ----------
st.set_page_config(page_title="AI Mental Health Chatbot", page_icon="🧠", layout="centered")

st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #667eea, #764ba2);
            color: white;
        }
        .chat-bubble-user {
            background-color: #4c6ef5;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px;
            max-width: 80%;
            color: white;
        }
        .chat-bubble-ai {
            background-color: #f3f3f3;
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px;
            max-width: 80%;
            color: black;
        }
        .stTextInput>div>div>input {
            background-color: #f5f5f5;
            color: black;
            border-radius: 10px;
        }
        .stButton>button {
            background-color: #4c6ef5;
            color: white;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align:center;'>🧠 AI Mental Health Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Your personal emotional support companion 💬</p>", unsafe_allow_html=True)

# ---------- CHAT HISTORY ----------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------- USER INPUT ----------
user_input = st.text_input("🧍 Tum:", placeholder="How are you feeling today...")

if st.button("💭 Send"):
    if user_input.strip():
        emotion, emoji, empathetic_reply = detect_emotion(user_input)

        # Generate AI continuation
        prompt = f"Human: {user_input}\nAI:"
        ai_raw = generator(prompt, max_length=80, pad_token_id=50256)[0]['generated_text']
        ai_reply = ai_raw.split("AI:")[-1].strip()

        # Clean AI output
        ai_reply = ai_reply.replace(user_input, "").strip()

        # Final response with empathy + AI tone
        final_reply = f"{empathetic_reply}\n\n{ai_reply}"

        # Store chat
        st.session_state.chat_history.append(("🧍 You", user_input))
        st.session_state.chat_history.append((f"🤖 AI ({emotion.title()}) {emoji}", final_reply))
    else:
        st.warning("Please type something first 💬")

# ---------- DISPLAY CHAT ----------
for speaker, message in st.session_state.chat_history:
    if "You" in speaker:
        st.markdown(f"<div class='chat-bubble-user'><b>{speaker}:</b> {message}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-ai'><b>{speaker}:</b> {message}</div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Made with ❤️ by Shivansh | Emotion-Aware AI Project")
