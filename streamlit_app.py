"""
Symbiote Learning App - Streamlit Frontend

Main Streamlit application for the learning interface.
"""

import streamlit as st
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Symbiote Learning App",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown(
    """
    <style>
    .main { padding: 2rem; }
    .stButton>button { width: 100%; padding: 0.5rem; font-size: 1rem; border-radius: 0.5rem; }
    .points-display { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                      color: white; padding: 1rem; border-radius: 0.5rem; text-align: center; }
    .agent-message { background-color: #f0f2f6; padding: 1rem; border-radius: 0.5rem; 
                     margin: 0.5rem 0; border-left: 4px solid #667eea; }
    .user-message { background-color: #e8f4f8; padding: 1rem; border-radius: 0.5rem; 
                    margin: 0.5rem 0; border-left: 4px solid #764ba2; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Backend URL
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "points" not in st.session_state:
    st.session_state.points = 0


def page_intro():
    """Introduction page."""
    col1, col2 = st.columns([1, 1])

    with col1:
        st.image("https://via.placeholder.com/400x300?text=Symbiote+Learning")

    with col2:
        st.title("🧠 Symbiote Learning App")
        st.markdown(
            """
            ### Welcome to Your Personalized Learning Journey!

            **Symbiote** combines AI agents with proven learning science:
            - 🤖 **Multi-Agent System** - Four AI agents collaborate
            - 📚 **Adaptive Learning** - Personalized journey
            - 🎮 **Gamified** - Earn points and level up
            - 💡 **Socratic Method** - Learn through questions

            ### Your Learning Team:
            - **Socratic Tutor** - Guides with questions
            - **Virtual Peer** - Collaborates and learns
            - **Provocateur** - Challenges and engages
            - **Teachable Agent** - Learns from you
            """
        )

    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Learning", use_container_width=True):
            st.session_state.page = "profile"
            st.rerun()


def page_profile():
    """Profile creation page."""
    st.title("📋 Create Your Learning Profile")

    with st.form("profile_form"):
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Your Name", placeholder="Enter your name")
            age = st.number_input("Your Age", min_value=5, max_value=100, value=20)

        with col2:
            education_level = st.selectbox(
                "Your Level",
                ["Beginner", "Intermediate", "Advanced"],
            )
            purpose = st.selectbox(
                "Your Purpose",
                ["Learn", "Test Your Knowledge"],
            )

        subject = st.text_input(
            "Subject",
            placeholder="e.g., Python Programming, History...",
        )

        submitted = st.form_submit_button("✨ Create Profile", use_container_width=True)

        if submitted:
            if not name or not subject:
                st.error("Please fill in all fields!")
            else:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/api/v1/sessions/create",
                        json={
                            "name": name,
                            "age": age,
                            "education_level": education_level.lower(),
                            "subject": subject,
                            "purpose": purpose.lower().replace(" ", "_"),
                        },
                    )

                    if response.status_code == 200:
                        data = response.json()
                        st.session_state.session_id = data["session_id"]
                        st.session_state.messages = []
                        st.session_state.points = 0
                        st.session_state.page = "chat"
                        st.success("Profile created! 🎉")
                        st.rerun()
                    else:
                        st.error(f"Error: {response.text}")

                except Exception as e:
                    st.error(f"Connection error: {str(e)}")


def page_chat():
    """Chat interface page."""
    st.title("🎓 Your Learning Session")

    # Sidebar with progress
    with st.sidebar:
        st.markdown("### 📊 Your Progress")

        if st.session_state.session_id:
            try:
                response = requests.get(
                    f"{BACKEND_URL}/api/v1/analytics/points/{st.session_state.session_id}"
                )
                if response.status_code == 200:
                    data = response.json()["points_summary"]
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Points", data["current_points"])
                    with col2:
                        st.metric("Level", data["level"])

                    st.progress(data["progress_to_next_level"] / 100)
            except:
                pass

        if st.button("🏠 Back Home"):
            st.session_state.page = "intro"
            st.session_state.session_id = None
            st.rerun()

    # Chat display
    st.markdown("### 💬 Learning Conversation")

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(
                f'<div class="user-message"><strong>You:</strong><br>{message["content"]}</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f'<div class="agent-message"><strong>Agent:</strong><br>{message["content"]}</div>',
                unsafe_allow_html=True,
            )

    st.markdown("---")

    # Input area
    col1, col2 = st.columns([4, 1])

    with col1:
        user_input = st.text_area(
            "Your Response:",
            placeholder="Type your response...",
            height=100,
        )

    with col2:
        st.markdown("")
        st.markdown("")
        send_button = st.button("Send 📤", use_container_width=True)
        hint_button = st.button("Hint 💡", use_container_width=True)

    if send_button and user_input:
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/v1/chat/message",
                json={
                    "session_id": st.session_state.session_id,
                    "message": user_input,
                    "use_hint": False,
                },
            )

            if response.status_code == 200:
                data = response.json()
                agent_response = data["agent_response"]

                st.session_state.messages.append({"role": "user", "content": user_input})
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": agent_response.get("message", ""),
                    }
                )

                st.session_state.points = data["points_summary"]["current_points"]
                st.rerun()
            else:
                st.error(f"Error: {response.text}")

        except Exception as e:
            st.error(f"Connection error: {str(e)}")

    if hint_button:
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/v1/chat/hint",
                json={
                    "session_id": st.session_state.session_id,
                    "challenge_id": "current",
                },
            )

            if response.status_code == 200:
                data = response.json()
                st.warning(f"💡 Hint penalty: {data['hint_penalty']} points")
                st.rerun()

        except Exception as e:
            st.error(f"Connection error: {str(e)}")


# Page routing
if st.session_state.page == "intro":
    page_intro()
elif st.session_state.page == "profile":
    page_profile()
elif st.session_state.page == "chat":
    page_chat()

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 0.8rem;'>"
    "<p>Symbiote Learning App v2.0 | Clean Architecture | Multi-Agent System</p>"
    "</div>",
    unsafe_allow_html=True,
)
