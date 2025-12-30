"""
The Glass Box: An exploratory AI agents learning app
Visualizes the ReAct Loop (Reasoning + Acting) in real-time
"""

import streamlit as st
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()

st.set_page_config(page_title="The Glass Box", layout="wide")

# ============================================================================
# SIDEBAR: CONFIG & LEARNING CONTROLS
# ============================================================================

with st.sidebar:
    st.title("⚙️ Agent Settings")
    
    # Model selection
    model_choice = st.radio(
        "Choose Model:",
        ["OpenAI (GPT-4o)", "Anthropic (Claude 3.5)"]
    )
    
    # Temperature slider
    temperature = st.slider(
        "Temperature (Randomness):",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        help="Lower = more deterministic. Higher = more creative/random."
    )
    
    # System prompt editor
    st.subheader("System Prompt")
    default_system = "You are a helpful AI assistant. Answer questions clearly and concisely."
    system_prompt = st.text_area(
        "Edit the system prompt:",
        value=default_system,
        height=150,
        help="The system prompt sets the agent's personality and instructions."
    )
    
    # Learning insights
    st.divider()
    st.subheader("📚 Learning Goal (Phase 1)")
    st.info(
        "**Understand:**\n"
        "- System Prompt vs User Prompt\n"
        "- How Temperature affects outputs\n"
        "- The difference between chat history and single responses"
    )

# ============================================================================
# MAIN UI: TWO-COLUMN LAYOUT (THE GLASS BOX)
# ============================================================================

col_chat, col_brain = st.columns([1, 1])

# ============================================================================
# LEFT COLUMN: THE CHAT INTERFACE
# ============================================================================

with col_chat:
    st.title("💬 The Chat")
    
    # Initialize session state
    if "messages" in st.session_state:
        messages = st.session_state.messages
    else:
        messages = []
        st.session_state.messages = messages
    
    # Display chat history
    chat_container = st.container()
    with chat_container:
        for msg in messages:
            if isinstance(msg, dict):
                role = msg["role"]
                content = msg["content"]
            else:
                role = msg.type if hasattr(msg, 'type') else 'unknown'
                content = msg.content if hasattr(msg, 'content') else str(msg)
            
            if role == "user":
                st.chat_message("user").write(content)
            elif role == "assistant":
                st.chat_message("assistant").write(content)
    
    # Input area
    user_input = st.chat_input("Ask the agent something...")

# ============================================================================
# RIGHT COLUMN: THE BRAIN (INTERNAL MONOLOGUE)
# ============================================================================

with col_brain:
    st.title("🧠 The Brain")
    
    brain_container = st.container()
    with brain_container:
        st.subheader("Agent's Internal State")
        
        # Display system prompt in use
        with st.expander("📋 System Prompt (in use)", expanded=True):
            st.code(system_prompt, language="markdown")
        
        # Display chat history as JSON
        with st.expander("💾 Message History (Memory)", expanded=True):
            if st.session_state.messages:
                for i, msg in enumerate(st.session_state.messages):
                    if isinstance(msg, dict):
                        st.json(msg)
                    else:
                        st.json({"type": msg.type, "content": msg.content})
            else:
                st.info("No messages yet. Start a conversation!")
        
        # Display settings in use
        with st.expander("⚙️ Current Settings", expanded=True):
            settings = {
                "model": model_choice,
                "temperature": temperature,
                "system_prompt_length": len(system_prompt),
                "messages_in_history": len(st.session_state.messages)
            }
            st.json(settings)

# ============================================================================
# PROCESS USER INPUT
# ============================================================================

if user_input:
    # Initialize LLM
    if "OpenAI" in model_choice:
        llm = ChatOpenAI(
            model="gpt-4o",
            temperature=temperature,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    else:
        llm = ChatAnthropic(
            model="claude-3-5-sonnet-20241022",
            temperature=temperature,
            api_key=os.getenv("ANTHROPIC_API_KEY")
        )
    
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Prepare messages for LLM (convert to LangChain format)
    langchain_messages = [SystemMessage(content=system_prompt)]
    for msg in st.session_state.messages:
        if isinstance(msg, dict):
            if msg["role"] == "user":
                langchain_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                langchain_messages.append(AIMessage(content=msg["content"]))
    
    # Get response from LLM
    with st.spinner("Agent thinking..."):
        response = llm.invoke(langchain_messages)
    
    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": response.content})
    
    # Rerun to update UI
    st.rerun()
