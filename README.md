# Hello LangGraph 🚀

A simple LangGraph project demonstrating basic workflow creation and state management with a chatbot example using LMStudio local LLM.

## Features

- **Simple Chatbot Workflow**: Interactive conversation with state management
- **Demo Mode**: Predefined conversation flow for testing
- **State Management**: Maintains conversation history using LangGraph's state system
- **Error Handling**: Graceful handling of API errors and missing configurations

## Prerequisites

- Python 3.12 or higher
- LMStudio installed and running
- qwen3-4b-2507 model loaded in LMStudio

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <your-repo-url>
   cd hello-langgraph
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```

3. **Set up LMStudio**:
   - Download and install [LMStudio](https://lmstudio.ai/)
   - Load the qwen3-4b-2507 model in LMStudio
   - Start the local server (default port: 1234)

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   The default configuration should work if LMStudio is running on localhost:1234:
   ```
   LMSTUDIO_BASE_URL=http://localhost:1234/v1
   LMSTUDIO_MODEL=qwen3-4b-2507
   LMSTUDIO_API_KEY=lm-studio
   ```

## Usage

Run the main script:

```bash
python main.py
```

You'll be presented with three options:

1. **Interactive Conversation**: Chat with the bot in real-time
2. **Demo Workflow**: Run a predefined conversation sequence
3. **Exit**: Quit the application

## Project Structure

```
hello-langgraph/
├── main.py              # Main application with LangGraph workflow
├── pyproject.toml       # Project dependencies and configuration
├── .env.example         # Environment variables template
├── .env                 # Your environment variables (create this)
├── README.md           # This file
└── LICENSE             # License file
```

## How It Works

### LangGraph Workflow

The project demonstrates a simple LangGraph workflow with:

- **State Definition**: Uses `TypedDict` to define conversation state with message history
- **Workflow Graph**: Creates a simple linear flow: START → chatbot → END
- **State Management**: Automatically handles message accumulation using `add_messages`

### Key Components

1. **State Class**: Defines the structure of data flowing through the workflow
2. **Chatbot Node**: Processes messages and generates AI responses
3. **Workflow Creation**: Builds and compiles the LangGraph workflow
4. **Interactive Interface**: Provides user-friendly interaction modes

## Customization

### Adding New Nodes

To extend the workflow, you can add new nodes:

```python
def new_node(state: State):
    # Your node logic here
    return {"messages": [AIMessage(content="Response from new node")]}

# Add to workflow
workflow.add_node("new_node", new_node)
workflow.add_edge("chatbot", "new_node")
workflow.add_edge("new_node", END)
```

### Modifying State

Extend the state structure:

```python
class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]
    user_info: dict  # Add custom fields
    context: str
```

## Troubleshooting

### Common Issues

1. **LMStudio Connection Issues**:
   - Ensure LMStudio is running and the server is started
   - Check that the correct model (qwen3-4b-2507) is loaded
   - Verify the server URL in `.env` matches LMStudio's server address

2. **Import Errors**:
   - Make sure all dependencies are installed: `pip install -e .`
   - Check Python version compatibility (3.12+)

3. **Model Loading Issues**:
   - Ensure qwen3-4b-2507 is properly downloaded in LMStudio
   - Check LMStudio logs for any model loading errors
   - Verify sufficient system resources (RAM/VRAM) for the model

## Dependencies

- `langgraph>=0.2.0`: Core workflow framework
- `langchain>=0.3.0`: LangChain integration
- `langchain-openai>=0.2.0`: OpenAI-compatible API integration (used for LMStudio)
- `python-dotenv>=1.0.0`: Environment variable management
- `requests>=2.31.0`: HTTP client for API calls

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the terms specified in the LICENSE file.

## Resources

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [LangChain Documentation](https://python.langchain.com/)
- [LMStudio Documentation](https://lmstudio.ai/docs)
- [Qwen Model Information](https://huggingface.co/Qwen)
