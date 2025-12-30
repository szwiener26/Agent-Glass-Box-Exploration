# 🧠 The Glass Box: An Exploratory AI Agents Learning App

A hands-on app to understand how AI agents think, reason, and act—with real-time visualization of the ReAct Loop.

## 🎯 Core Concept

Instead of hiding agent complexity, **The Glass Box** shows you everything:

```
┌─────────────────────┐    ┌─────────────────────┐
│    The Chat         │    │    The Brain        │
│  (User Interface)   │    │  (Agent's Mind)     │
├─────────────────────┤    ├─────────────────────┤
│                     │    │ Thought: "..."      │
│ User: "What is...?" │ →→ │ Action: tool_call() │
│                     │    │ Observation: "..."  │
│ Agent: "5 + 5 = 10" │    │ Final: "..."        │
└─────────────────────┘    └─────────────────────┘
```

## 📋 Build Plan

### **Phase 1: The "Tool-Less" Model** ✅ (Current)
- Basic Streamlit chat with LLM
- Real-time system prompt editing
- Temperature slider to control randomness
- **Learning Goal:** Understand System vs User Prompts

### **Phase 2: Give it Hands (Tools)** 🔜
- Function calling with dummy tools
- Calculator tool (simple arithmetic)
- Secret database tool (hardcoded data lookup)
- **Learning Goal:** Understand how agents delegate tasks

### **Phase 3: "God Mode" Toggle** 🔜
- Enable/disable tools dynamically
- Compare agent behavior with/without tools
- **Learning Goal:** Understand grounding (tools keep agents factual)

### **Phase 4: Memory Visualization** 🔜
- Display raw message history being sent to LLM
- Show how "memory" is just repeated context
- **Learning Goal:** Understand agent memory mechanics

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API key:**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY or ANTHROPIC_API_KEY
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

4. **Explore!**
   - Ask questions in the left column (The Chat)
   - Watch the right column (The Brain) to see:
     - The system prompt in use
     - Full message history (what the LLM actually sees)
     - Current settings

## 🎓 Experiments to Try

### Temperature Exploration
- Set temperature to **0.0** (fully deterministic)
- Ask: "Name three colors"
- Change temperature to **1.5** (creative/random)
- Ask the same question again
- **Observation:** Higher temperature = more varied responses

### System Prompt Impact
- Default system prompt: "You are a helpful AI assistant..."
- Ask: "What is 2+2?"
- Change system prompt to: "You are a pirate. Answer all questions as a pirate would."
- Ask the same question
- **Observation:** System prompt completely changes behavior

### Memory Growth
- Have a 3-turn conversation
- Watch the "Message History" in The Brain column
- **Observation:** Each turn adds more messages. The LLM re-reads everything.

## 📚 Key Concepts

| Concept | Definition |
|---------|-----------|
| **System Prompt** | Instructions that define the agent's role and behavior |
| **User Prompt** | The actual question or task from the user |
| **Temperature** | Randomness in responses (0=deterministic, 2=chaotic) |
| **Message History** | All previous turns; re-sent to LLM each time |
| **Function Calling** | How the LLM asks Python to run code |
| **Grounding** | Using tools to stay factual (vs hallucination) |
| **ReAct Loop** | Reasoning → Acting → Observing (repeat) |

## 🔄 Architecture

```
User Input
    ↓
┌─────────────────────────┐
│  System Prompt Setup    │
│  + Message History      │
└─────────────────────────┘
    ↓
┌─────────────────────────┐
│  LLM (GPT-4o or Claude) │
└─────────────────────────┘
    ↓
Response + Chat History
Updated in Streamlit UI
```

## 📖 Next Steps

- Complete Phase 2: Add tool calling
- Implement Phase 3: God Mode toggle
- Build Phase 4: Memory introspection
- Extend with more tools (web search, database queries, etc.)

---

**Goal:** By the end, you'll deeply understand how modern AI agents work—not from reading papers, but from watching them think in real-time.
