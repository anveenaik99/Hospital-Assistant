"""Parent Chat page with AI assistant."""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.agent.graph import create_agent, run_agent
from app.agent.prompts import INITIAL_MESSAGE
from app.db.crud import get_child_by_id

st.set_page_config(page_title="Parent Chat", page_icon="👪", layout="wide")

st.title("👪 Parent Chat Assistant")
st.markdown("AI-powered health guidance and appointment scheduling for your child")
st.markdown("---")

# Check for OpenAI API key
if not os.getenv("OPENAI_API_KEY"):
    st.error("⚠️ OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable.")
    st.stop()

# Initialize session state
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
    st.session_state.child_id_verified = False
    st.session_state.current_child_id = None

# Always create a fresh agent to avoid caching issues
with st.spinner("Initializing AI assistant..."):
    try:
        agent = create_agent()
    except Exception as e:
        st.error(f"Failed to initialize AI assistant: {str(e)}")
        st.stop()

# Display disclaimer
st.warning("⚠️ **IMPORTANT:** This is not medical advice. If symptoms are severe or urgent, seek immediate care.")

# Sidebar with child info
with st.sidebar:
    st.markdown("### 💬 Chat Info")
    
    if st.session_state.current_child_id:
        child = get_child_by_id(st.session_state.current_child_id)
        if child:
            st.success(f"**Child:** {child['child_name']}")
            st.info(f"**ID:** {child['child_id']}")
            st.info(f"**DOB:** {child['dob']}")
    
    st.markdown("---")
    
    if st.button("🔄 Start New Chat", use_container_width=True):
        st.session_state.chat_messages = []
        st.session_state.child_id_verified = False
        st.session_state.current_child_id = None
        st.rerun()
    
    st.markdown("---")
    st.markdown("### ℹ️ Tips")
    st.markdown("""
    - Provide your child's ID to start
    - Ask health-related questions
    - Request appointment booking
    - Say 'goodbye' or 'thanks' to end chat and see vaccine reminders
    """)

# Chat container
chat_container = st.container()

# Display chat messages
with chat_container:
    if not st.session_state.chat_messages:
        st.info(INITIAL_MESSAGE)
    else:
        for msg in st.session_state.chat_messages:
            if msg['role'] == 'user':
                with st.chat_message("user"):
                    st.write(msg['content'])
            else:
                with st.chat_message("assistant"):
                    st.write(msg['content'])

# Chat input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to display immediately
    st.session_state.chat_messages.append({
        'role': 'user',
        'content': user_input
    })
    
    # Display the user message right away
    with st.chat_message("user"):
        st.write(user_input)
    
    # Get agent response
    with st.spinner("Thinking..."):
        try:
            print(f"\n[CHAT] User input: {user_input}")
            
            # Prepare chat history for agent
            agent_history = []
            for msg in st.session_state.chat_messages[:-1]:  # Exclude the just-added user message
                if msg['role'] == 'user':
                    from langchain_core.messages import HumanMessage
                    agent_history.append(HumanMessage(content=msg['content']))
                else:
                    from langchain_core.messages import AIMessage
                    agent_history.append(AIMessage(content=msg['content']))
            
            print(f"[CHAT] Prepared {len(agent_history)} history messages")
            
            # Run agent
            print("[CHAT] Calling run_agent...")
            response, updated_messages = run_agent(
                agent,
                user_input,
                agent_history
            )
            print(f"[CHAT] Got response of length: {len(response)}")
            
            # Add assistant response to display
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'content': response
            })
            
            # Check if child_id was verified in the response
            # This is a simple heuristic - in production you'd want more robust state management
            if 'CH-' in user_input and not st.session_state.child_id_verified:
                # Extract potential child_id
                words = user_input.split()
                for word in words:
                    if word.startswith('CH-'):
                        potential_id = word.strip('.,!?')
                        child = get_child_by_id(potential_id)
                        if child:
                            st.session_state.child_id_verified = True
                            st.session_state.current_child_id = potential_id
                            break
            
            st.rerun()
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.session_state.chat_messages.append({
                'role': 'assistant',
                'content': f"I apologize, but I encountered an error: {str(e)}. Please try again."
            })
            st.rerun()
