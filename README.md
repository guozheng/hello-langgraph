# Running LangGraph with LMStudio and UV 🚀

A simple [LangGraph](https://langchain-ai.github.io/langgraph/) project demonstrating basic workflow creation and state management with a chatbot example using [LMStudio](https://lmstudio.ai/) local LLM. Package management uses [UV](https://github.com/indygreg/uv), the fastest package manager for Python.

## Features

- **Simple Chatbot Workflow**: Interactive conversation with state management
- **Demo Mode**: Predefined conversation flow for testing
- **State Management**: Maintains conversation history using LangGraph's state system
- **Error Handling**: Graceful handling of API errors and missing configurations

## Prerequisites

- Python 3.12 or higher
- [UV](https://github.com/indygreg/uv) installed and running
- [LMStudio](https://lmstudio.ai/) installed and running
- [qwen3-4b-2507](https://lmstudio.ai/models/qwen/qwen3-4b-2507) model loaded in LMStudio, if your computer has enough resources, you can also try [gpt-oos-20b](https://lmstudio.ai/models/openai/gpt-oos-20b)

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <your-repo-url>
   cd hello-langgraph
   ```

2. **Install dependencies**:
   - [LangGraph CLI](https://docs.langchain.com/langgraph-platform/langgraph-cli) is a tool for building and running LangGraph API server locally.
   - The official documentation installs `langgraph-cli` using `pip` or Homebrew, we use UV to install it here.
   - A UV tool is a self-contained executable that can be installed and run from the command line. We install `langgraph-cli` tool using UV, then update the shell to make it available in the PATH.
   ```bash
   uv tool install langgraph-cli
   uv tool update-shell
   ```

3. **Set up LMStudio**:
   - Download and install [LMStudio](https://lmstudio.ai/)
   - Load the qwen3-4b-2507 model in LMStudio
   - Start the local server (default port: 1234)

4. **[Optional] Register for a free LangSmith account to get an API key**:
   - This step is optional, but highly recommended to learn more about LangGraph and LangSmith. LangSmith is a platform for tracking and debugging LLM workflows
   - Follow [this documentation](https://docs.smith.langchain.com/administration/how_to_guides/organization_management/create_account_api_key) to create an account and get an API key

5. **Set up environment variables**:
   - Create a `.env` file in the root directory of the project (make sure you add it to `.gitignore`)
   - Add the following environment variables:
   ```
   # LMStudio Configuration
   LMSTUDIO_BASE_URL=http://localhost:1234/v1
   LMSTUDIO_MODEL=qwen3-4b-2507
   LMSTUDIO_API_KEY=lm-studio

   # LangSmith Configuration (optional - for tracing and monitoring)
   LANGCHAIN_TRACING_V2=true
   LANGCHAIN_API_KEY=<your-api-key>
   LANGCHAIN_PROJECT=hello-langgraph
   ```

## Usage

1. **Run the LangGraph app**:

```bash
uv run main.py
```

This is a standalone command line application. You'll be presented with three options:

   1. **Interactive Conversation**: Chat with the bot in real-time, type `quit`, `exit`, `bye`, or `q` (case insensitive) to exit
   2. **Demo Workflow**: Run a predefined conversation sequence
   3. **Exit**: Quit the application


2. **Run LangGraph API server and LangGraph Studio**:

If you are using Chrome browser, run:

```bash
$ langgraph dev

        Welcome to

╦  ┌─┐┌┐┌┌─┐╔═╗┬─┐┌─┐┌─┐┬ ┬
║  ├─┤││││ ┬║ ╦├┬┘├─┤├─┘├─┤
╩═╝┴ ┴┘└┘└─┘╚═╝┴└─┴ ┴┴  ┴ ┴

- 🚀 API: http://127.0.0.1:2024
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- 📚 API Docs: http://127.0.0.1:2024/docs

This in-memory server is designed for development and testing.
For production use, please use LangGraph Platform.
```

If you are using Safari or Brave browser, they block plain HTTP traffic on localhost. You need to pass in a special `--tunnel` flag to use Cloudflare Tunnel to expose your local server.

```bash
$ langgraph dev --tunnel

        Welcome to

╦  ┌─┐┌┐┌┌─┐╔═╗┬─┐┌─┐┌─┐┬ ┬
║  ├─┤││││ ┬║ ╦├┬┘├─┤├─┘├─┤
╩═╝┴ ┴┘└┘└─┘╚═╝┴└─┴ ┴┴  ┴ ┴

- 🚀 API: https://accurately-hydrogen-adware-batman.trycloudflare.com
- 🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=https://accurately-hydrogen-adware-batman.trycloudflare.com
- 📚 API Docs: https://accurately-hydrogen-adware-batman.trycloudflare.com/docs

```

   * API is where you can make API calls to the LangGraph application, e.g. we have included a `client.py` that shows how to interact through the API.
   * LangGraph Studio is the UI for interacting with the LangGraph application. For more details on how to use LangGraph Studio, see [LangGraph Studio Quickstart](https://docs.langchain.com/langgraph-platform/quick-start-studio) and [LangGraph Studio Documentation](https://docs.langchain.com/langgraph-platform/langgraph-studio).
   * API docs lists all the API endpoints and their parameters. You can directly test it out through the API docs UI.For more details on how to use the API, see [LangGraph API Documentation](https://docs.langchain.com/langgraph-platform/api).

After you are done, you can stop the LangGraph API server by pressing `Ctrl+C` in the terminal.


3. **Start the LangGraph API server, then run the client that sends requests through the API**

You can directly use LangGraph API to build your application we include a `client.py` that shows how to interact through the API.

First, start the LangGraph API server:
```bash
$ langgraph dev
```

Take a note of the API URL, it will be something like `http://localhost:2024`. You need to pass it to the client.

Then, in another terminal, start the client:
```bash
$ uv run client.py
```

Somehow you cannot connect to LangGraph API server if you run in tunnel mode (`--tunnel`), the tunnel server name cannot be resolved you will get an error: `Failed to connect to LangGraph API server: [Errno 8] nodename nor servname provided, or not known`. So you need to start the LangGraph API server without tunnel mode.

For more details on LangGraph API, see [LangGraph Python SDK Documentation](https://langchain-ai.github.io/langgraph/cloud/reference/sdk/python_sdk_ref/).

## Project Structure

```
hello-langgraph/
├── main.py              # Main application with LangGraph workflow
├── client.py            # Client for interacting with LangGraph API server through API/SDK
├── pyproject.toml       # Project dependencies and configuration
├── .env                 # Your environment variables (create this)
├── .gitignore           # Git ignore file
├── .python-version      # Python version file
├── langgraph.json       # LangGraph configuration
├── uv.lock              # UV lock file
├── README.md            # This file
└── LICENSE              # License file
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

4. **Local LangGraph API Server Issues**:
   - Safari and Brave browsers block plain HTTP traffic on localhost. When you run the LangGraph API server, instead of `langgraph dev`, use `langgraph dev --tunnel`. For more details, see this [troubleshooting guide](https://docs.langchain.com/langgraph-platform/troubleshooting-studio) and [langchain-cli manual](https://docs.langchain.com/langgraph-platform/cli).

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

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
   - [Quick start guide: run a LangGraph application locally](https://docs.langchain.com/langgraph-platform/local-server)
   - [LangGraph CLI reference](https://docs.langchain.com/langgraph-platform/cli#commands)
   - [LangGraph Server API Documentation](https://docs.langchain.com/langgraph-platform/server-api-ref)
   - [LangGraph Python SDK Documentation](https://langchain-ai.github.io/langgraph/cloud/reference/sdk/python_sdk_ref/)
   - [Other LangGraph Platform Documentation](https://docs.langchain.com/langgraph-platform/reference-overview)
   - [new-langgraph-project-python template github project](https://github.com/langchain-ai/new-langgraph-project), to use it, just run the command: `langgraph new <path_to_local_project> --template new-langgraph-project-python`
- [LMStudio Documentation](https://lmstudio.ai/docs)
- [Qwen Model Information](https://huggingface.co/Qwen)
- [UV package manager](https://docs.astral.sh/uv/)
- [UV tools](https://docs.astral.sh/uv/guides/tools/)
