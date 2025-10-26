"""
Simple LangGraph workflow example demonstrating a basic chatbot with state management.
"""
import os
from typing import TypedDict, Annotated
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()

# Define the state structure
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Initialize the LLM
def get_llm():
    """Initialize and return the language model."""

    # Use LMStudio to run local LLM model, it provides OpenAI compatible API
    base_url = os.getenv("LMSTUDIO_BASE_URL", "http://localhost:1234/v1")
    model_name = os.getenv("LMSTUDIO_MODEL", "qwen3-4b-2507")
    api_key = os.getenv("LMSTUDIO_API_KEY", "lm-studio")
    
    try:
        return ChatOpenAI(
            base_url=base_url,
            api_key=api_key,
            model=model_name,
            temperature=0.7
        )
    except Exception as e:
        print(f"Warning: Could not connect to LMStudio at {base_url}")
        print("Please ensure LMStudio is running and the server is started.")
        print(f"Error: {e}")
        return None

# Define workflow nodes
def chatbot_node(state: State):
    """Main chatbot node that processes messages and generates responses."""
    llm = get_llm()
    if not llm:
        return {"messages": [AIMessage(content="Error: Could not connect to LMStudio. Please ensure LMStudio is running.")]}
    
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Define workflow
def create_workflow():
    """Create and compile the LangGraph workflow."""
    # Create the graph
    workflow = StateGraph(State)
    
    # Add nodes
    workflow.add_node("chatbot", chatbot_node)
    
    # Define the flow
    workflow.add_edge(START, "chatbot")
    workflow.add_edge("chatbot", END)
    
    # Compile the graph
    return workflow.compile()

def run_conversation():
    """Run an interactive conversation with the chatbot."""
    app = create_workflow()
    
    print("🤖 Simple LangGraph Chatbot")
    print("Type 'quit' to exit\n")
    
    # Initialize conversation state
    state = {"messages": []}
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
            print("Goodbye! 👋")
            break
        
        if not user_input:
            continue
        
        # Add user message to state
        state["messages"].append(HumanMessage(content=user_input))
        
        try:
            # Process through the workflow
            result = app.invoke(state)
            
            # Get the latest AI response
            ai_response = result["messages"][-1].content
            print(f"Bot: {ai_response}\n")
            
            # Update state with the result
            state = result
            
        except Exception as e:
            print(f"Error: {e}\n")

def demo_workflow():
    """Run a simple demo of the workflow with predefined messages."""
    print("🔄 Running LangGraph Workflow Demo")
    print("-" * 40)
    
    app = create_workflow()
    
    # Demo messages
    demo_messages = [
        "Hello! Can you introduce yourself?",
        "What is LangGraph?",
        "Can you explain state management in workflows?"
    ]
    
    state = {"messages": []}
    
    for message in demo_messages:
        print(f"User: {message}")
        
        # Add user message
        state["messages"].append(HumanMessage(content=message))
        
        try:
            # Process through workflow
            result = app.invoke(state)
            ai_response = result["messages"][-1].content
            print(f"Bot: {ai_response}\n")
            
            # Update state
            state = result
            
        except Exception as e:
            print(f"Error: {e}\n")
            break

def main():
    """Main function to run the LangGraph example."""
    print("🚀 Hello from LangGraph!")
    print("Choose an option:")
    print("1. Interactive conversation")
    print("2. Demo workflow")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            run_conversation()
            break
        elif choice == "2":
            demo_workflow()
            break
        elif choice == "3":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
