# ACTIVA Frontend Guide

> **Note**: This README is located in the `docs/` folder. The project has been reorganized for better structure.

## 🚀 Quick Start

### 1. Setup Configuration
```bash
python scripts/setup_config.py
```

### 2. Launch Frontend
```bash
python scripts/run_frontend.py
```

### 3. Open Browser
Navigate to `http://localhost:8000`

## 🎯 Features

- **Natural Language Input**: Describe accounting concepts in plain English
- **Real-time Progress**: See generation steps as they happen
- **Persistent Actions**: Rerun and execute animations without losing context
- **Auto-rerun**: Automatically retry failed generations
- **File Management**: Generated code saved to `generated_code/` directory
- **Extended Timeouts**: 5-minute timeout for long-running operations
- **Non-blocking Operations**: Thread pool execution for smooth performance

## 🎮 How to Use

### 1. Send a Prompt
Type your accounting concept description in the chat input:
```
"Create an animation showing how to calculate depreciation using the straight-line method"
```

### 2. Watch Progress
The system will show:
- 🔍 **Planning**: Analyzing your request
- 📝 **Code Generation**: Creating Manim code (up to 5 minutes)
- ⚡ **Execution**: Running the animation (up to 5 minutes)
- 🔧 **Error Recovery**: Fixing issues if needed

### 3. Use Action Buttons
After generation, you'll see persistent buttons:
- **🔄 Rerun**: Generate new code for the same prompt
- **▶️ Run Animation**: Execute the current code
- **📁 View Code**: See the generated Python file

### 4. Start Fresh
Send a new prompt to clear the current context and start over.

## 📁 Generated Files

All generated code is saved in the `generated_code/` directory:
- `manim_animation_TIMESTAMP.py` - Latest successful code with timestamp
- Individual generation attempts are saved automatically

## ⚙️ Configuration

The frontend uses the same configuration system as the command-line tool:

### Supported Providers
- **OpenAI**: GPT-4o, GPT-4-turbo, GPT-3.5-turbo
- **Claude**: Claude 3.5 Sonnet, Claude 3 Opus
- **Gemini**: Gemini 1.5 Pro, Gemini 1.5 Flash

### Setup
```bash
python scripts/setup_config.py
```

### Frontend Configuration
The frontend includes optimized settings in `.chainlit/config.toml`:
- **Server Timeout**: 5 minutes for all operations
- **WebSocket Timeout**: 5 minutes for real-time updates
- **HTTP Timeout**: 5 minutes for API calls
- **Non-blocking Execution**: Thread pool for smooth performance

## 🔧 Troubleshooting

### Frontend Won't Start
```bash
# Check if Chainlit is installed
pip install chainlit

# Try running directly
chainlit run frontend.py

# Check for configuration file
ls .chainlit/config.toml
```

### Configuration Issues
```bash
# Reset configuration
rm config/config.json
python scripts/setup_config.py

# Recreate Chainlit config if needed
mkdir -p .chainlit
# Copy config.toml from repository
```

### Generated Code Issues
- Check the `generated_code/` directory for saved files
- Review error messages in the chat
- Try the "Rerun" button for automatic error recovery

### Timeout Issues
The frontend is configured with extended timeouts (5 minutes) to handle long-running operations:
- **Agent Generation**: Up to 5 minutes for code generation
- **Animation Execution**: Up to 5 minutes for Manim rendering
- **Progress Updates**: Real-time status during long operations
- **Non-blocking**: Operations run in background threads

If you still experience timeouts:
1. Check your internet connection
2. Try simpler prompts first
3. Restart the frontend: `python scripts/run_frontend.py`
4. Check the Chainlit configuration: `.chainlit/config.toml`

### Performance Issues
- **Slow Generation**: Normal for complex animations, system handles up to 5 minutes
- **Browser Freezing**: Operations run in background, browser should remain responsive
- **Memory Issues**: Check available system memory for large animations

## 📖 Example Prompts

### Basic Animations
- "Create a bouncing ball animation"
- "Show a rotating square"
- "Animate a growing circle"

### Accounting Concepts
- "Visualize the accounting equation: Assets = Liabilities + Equity"
- "Show how to calculate compound interest over time"
- "Animate the double-entry bookkeeping process"

### Mathematical Concepts
- "Create a sine wave animation"
- "Show the derivative of a function"
- "Visualize a 3D coordinate system"

## 🎨 Customization

### Modify Sidebar
Edit `chainlit.md` to change the sidebar content.

### Adjust Generation Settings
Modify the agent parameters in `activa/agent/nodes.py`.

### Change File Locations
Update paths in `frontend.py` to change where files are saved.

### Modify Timeouts
Edit `.chainlit/config.toml` to adjust timeout settings:
```toml
[server]
timeout = 300  # 5 minutes
max_http_timeout = 300
max_websocket_timeout = 300
```

## 🔗 Related Files

- **`frontend.py`** - Main frontend application with thread pool execution
- **`scripts/run_frontend.py`** - Frontend launcher script with error handling
- **`chainlit.md`** - Sidebar content
- **`.chainlit/config.toml`** - Frontend timeout and server configuration
- **`config/config.py`** - Configuration management
- **`activa/agent/`** - Core agent system 