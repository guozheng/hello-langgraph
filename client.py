"""
LangGraph SDK Client Example

This client demonstrates how to interact with a LangGraph application
running via the LangGraph API server using the langgraph-sdk.

First, start the LangGraph API server:
```bash
$ langgraph dev
```

Take a note of the API URL, it will be something like `http://localhost:2024`. You need to pass it to the client.

Then, in another terminal, start the client:
```bash
$ uv run client.py
```
"""
import os
import asyncio
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from langgraph_sdk import get_client

# Load environment variables
load_dotenv()


class LangGraphClient:
    """Client for interacting with LangGraph API server."""
    
    def __init__(self, api_url: Optional[str] = None):
        """Initialize the LangGraph client.
        
        Args:
            api_url: The URL of the LangGraph API server. 
                    Defaults to http://localhost:2024 if not provided.
        """
        self.api_url = api_url or os.getenv("LANGGRAPH_API_URL", "http://localhost:2024")
        self.client = get_client(url=self.api_url)
        
    async def create_thread(self) -> str:
        """Create a new conversation thread.
        
        Returns:
            Thread ID for the new conversation.
        """
        try:
            thread = await self.client.threads.create()
            return thread["thread_id"]
        except Exception as e:
            print(f"Error creating thread: {e}")
            raise
    
    async def send_message(self, thread_id: str, message: str, graph_id: str = "agent") -> Dict[str, Any]:
        """Send a message to the LangGraph application.
        
        Args:
            thread_id: The thread ID for the conversation
            message: The message to send
            graph_id: The graph ID (defaults to "agent")
            
        Returns:
            The response from the LangGraph application
        """
        try:
            # Send the message and get the run
            input_data = {"messages": [{"role": "user", "content": message}]}
            
            run = await self.client.runs.create(
                thread_id=thread_id,
                assistant_id=graph_id,
                input=input_data
            )
            
            # Wait for the run to complete
            await self.client.runs.join(thread_id=thread_id, run_id=run["run_id"])
            
            # Get the final state
            state = await self.client.threads.get_state(thread_id=thread_id)
            
            # Extract the latest AI message
            messages = state["values"]["messages"]
            if messages:
                latest_message = messages[-1]
                if latest_message.get("type") == "ai":
                    return {
                        "content": latest_message["content"],
                        "run_id": run["run_id"],
                        "thread_id": thread_id
                    }
            
            return {"content": "No response received", "run_id": run["run_id"], "thread_id": thread_id}
            
        except Exception as e:
            print(f"Error sending message: {e}")
            raise
    
    async def get_thread_history(self, thread_id: str) -> list:
        """Get the conversation history for a thread.
        
        Args:
            thread_id: The thread ID
            
        Returns:
            List of messages in the conversation
        """
        try:
            state = await self.client.threads.get_state(thread_id=thread_id)
            return state["values"]["messages"]
        except Exception as e:
            print(f"Error getting thread history: {e}")
            raise
    
    async def list_threads(self) -> list:
        """List all available threads.
        
        Returns:
            List of thread information
        """
        try:
            threads = await self.client.threads.search()
            return threads
        except Exception as e:
            print(f"Error listing threads: {e}")
            raise


async def interactive_chat():
    """Run an interactive chat session with the LangGraph application."""
    print("🤖 LangGraph SDK Client")
    print("Make sure your LangGraph API server is running with: langgraph dev")
    print("Type 'quit', 'exit', 'bye', or 'q' to exit\n")
    
    client = LangGraphClient()
    print(f"Client initialized with API URL: {client.api_url}")
    
    try:
        # Create a new thread
        thread_id = await client.create_thread()
        print(f"Created new conversation thread: {thread_id}\n")
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("Goodbye! 👋")
                break
            
            if not user_input:
                continue
            
            try:
                # Send message and get response
                response = await client.send_message(thread_id, user_input)
                print(f"Bot: {response['content']}\n")
                
            except Exception as e:
                print(f"Error: {e}\n")
                
    except Exception as e:
        print(f"Failed to connect to LangGraph API server: {e}")
        print("Make sure the server is running with: langgraph dev")


async def demo_conversation():
    """Run a demo conversation with predefined messages."""
    print("🔄 Running LangGraph SDK Client Demo")
    print("-" * 40)
    
    client = LangGraphClient()
    
    try:
        # Create a new thread
        thread_id = await client.create_thread()
        print(f"Created thread: {thread_id}\n")
        
        # Demo messages
        demo_messages = [
            "Hello! Can you introduce yourself?",
            "What is LangGraph?",
            "Can you explain state management in workflows?"
        ]
        
        for message in demo_messages:
            print(f"User: {message}")
            
            try:
                response = await client.send_message(thread_id, message)
                print(f"Bot: {response['content']}\n")
                
            except Exception as e:
                print(f"Error: {e}\n")
                break
                
        # Show conversation history
        print("📝 Conversation History:")
        print("-" * 30)
        history = await client.get_thread_history(thread_id)
        for i, msg in enumerate(history, 1):
            role = "User" if msg.get("type") == "human" else "Bot"
            content = msg.get("content", "")
            print(f"{i}. {role}: {content}")
            
    except Exception as e:
        print(f"Demo failed: {e}")
        print("Make sure the LangGraph API server is running with: langgraph dev")


def main():
    """Main function to run the LangGraph SDK client."""
    print("🚀 LangGraph SDK Client")
    print("Choose an option:")
    print("1. Interactive conversation")
    print("2. Demo conversation")
    print("3. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            asyncio.run(interactive_chat())
            break
        elif choice == "2":
            asyncio.run(demo_conversation())
            break
        elif choice == "3":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()