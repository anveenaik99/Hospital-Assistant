"""LangGraph ReAct agent implementation."""
import os
from typing import Sequence
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from app.agent.tools import ALL_TOOLS
from app.agent.prompts import get_system_prompt


def create_agent():
    """
    Create and return a LangGraph ReAct agent.
    
    ReAct Pattern:
    - Reason: Agent thinks about the problem
    - Act: Agent takes action using tools
    - Observe: Agent observes tool results
    - Repeat until task is complete
    
    Returns:
        A compiled LangGraph ReAct agent
    """
    
    # Initialize OpenAI model
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    
    print("[ReAct Agent] Creating ChatOpenAI model...")
    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        api_key=api_key
    )
    
    # Get system prompt with current date/time
    system_prompt = get_system_prompt()
    
    # Create ReAct agent using LangGraph
    print("[ReAct Agent] Creating LangGraph ReAct agent...")
    
    # For LangGraph 0.0.69, we need to pass system prompt differently
    # We'll prepend it to messages in run_agent instead
    agent = create_react_agent(
        model=model,        
        tools=ALL_TOOLS,
        messages_modifier=system_prompt,
    )
    
    print("[ReAct Agent] Agent created successfully")
    return agent


def run_agent(agent, user_message: str, chat_history: list = None):
    """
    Run the LangGraph ReAct agent.
    
    The ReAct agent automatically:
    1. THOUGHT: Reasons about what action to take
    2. ACTION: Executes tools as needed
    3. OBSERVATION: Processes tool results
    4. Repeats until it has a final answer
    
    Args:
        agent: Compiled LangGraph ReAct agent
        user_message: User's message
        chat_history: Previous chat messages (optional)
        
    Returns:
        Tuple of (response_text, updated_messages)
    """
    print(f"\n{'='*80}")
    print(f"[ReAct Agent] Starting new interaction")
    print(f"[ReAct Agent] User Query: {user_message}")
    print(f"{'='*80}")
    
    if chat_history is None:
        chat_history = []
    
    print(f"[ReAct Agent] Chat history: {len(chat_history)} messages")
    
    # Prepare messages for the agent
    messages = chat_history + [HumanMessage(content=user_message)]
    
    try:
        # Invoke the LangGraph ReAct agent
        # The agent will automatically handle the ReAct loop
        print(f"[ReAct Agent] Invoking agent...")
        
        result = agent.invoke(
            {"messages": messages}
        )
        
        # Extract the final messages from the result
        final_messages = result["messages"]
        
        # Get the last AI message as the response
        response_text = None
        for msg in reversed(final_messages):
            if isinstance(msg, AIMessage):
                response_text = msg.content
                break
        
        if response_text is None:
            response_text = "I apologize, but I couldn't generate a response. Please try again."
        
        # Show response preview
        preview = response_text
        print(f"[ReAct Agent] Response: {preview}")
        print(f"[ReAct Agent] Total messages in result: {len(final_messages)}")
        
        # Log tool usage summary
        tool_uses = [msg for msg in final_messages if hasattr(msg, 'tool_calls') and msg.tool_calls]
        if tool_uses:
            print(f"[ReAct Agent] Tools used in this interaction: {len(tool_uses)} tool call(s)")
            for msg in tool_uses:
                for tool_call in msg.tool_calls:
                    print(f"[ReAct Agent]   - {tool_call['name']}")
        
        print(f"{'='*80}\n")
        
        return response_text, final_messages
        
    except Exception as e:
        print(f"\n[ReAct Agent] ❌ ERROR: {type(e).__name__}: {str(e)}")
        import traceback
        print(f"[ReAct Agent] Traceback:\n{traceback.format_exc()}")
        print(f"{'='*80}\n")
        raise
