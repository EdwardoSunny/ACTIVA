# ACTIVA: Accounting Concepts Taught Interactively with Visual Animations

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

### 1. Install Dependencies
```bash
git clone https://github.com/yourusername/activa.git
cd activa
pip install -e .
```

### 2. Configure LLM Provider
```bash
python setup_config.py
```
Choose from OpenAI, Claude, or Gemini and enter your API key.

### 3. Run ACTIVA
**Frontend (Recommended):**
```bash
python run_frontend.py
```
Then open `http://localhost:8000` in your browser.

**Command Line:**
```bash
python main.py
```

📖 **See [FRONTEND_README.md](FRONTEND_README.md) for detailed frontend usage.**

## 🎯 What is ACTIVA?

**ACCOUNTING CONCEPTS TAUGHT INTERACTIVELY WITH VISUAL ANIMATIONS (ACTIVA)** is an LLM-based animation tool that generates custom accounting visualizations from natural language prompts. It uses a multi-agent framework to automatically create Manim animations for accounting education.

## ✨ Key Features

- **Natural Language Input**: Describe accounting concepts in plain English
- **Multi-Agent System**: Intelligent planning, coding, execution, and error recovery
- **Multiple LLM Support**: Works with OpenAI, Claude, and Gemini
- **Real-time Generation**: Automated creation of accounting process animations
- **Error Recovery**: Automatic debugging and code correction
- **Cost-Effective**: Much cheaper than manual animation production

## 🤖 Supported LLM Providers

ACTIVA supports multiple LLM providers through a flexible configuration system:

### OpenAI
- **Models**: GPT-4o, GPT-4-turbo, GPT-3.5-turbo
- **Setup**: Requires OpenAI API key
- **Best for**: General purpose, code generation

### Claude (Anthropic)
- **Models**: Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Sonnet
- **Setup**: Requires Anthropic API key
- **Best for**: Complex reasoning, detailed explanations

### Gemini (Google)
- **Models**: Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini Pro
- **Setup**: Requires Google API key
- **Best for**: Cost-effective, fast responses

## 🏗️ How It Works

ACTIVA uses four specialized agents working together:

1. **Planning Agent**: Analyzes your prompt and searches for implementation examples
2. **Code Writing Agent**: Generates Manim Python code based on the task
3. **Execution Agent**: Runs the animation and checks for success
4. **Error Search Agent**: Finds fixes if execution fails

The system iterates until successful execution or reaches the maximum attempts.

## 📁 Project Structure

```
activa/
├── agent/                 # Multi-agent framework
│   ├── graph.py          # Agent workflow definition
│   ├── nodes.py          # Individual agent implementations
│   └── state.py          # State management
├── utils/                 # Manim execution utilities
│   └── manim_tools.py    # Code execution and error handling
├── frontend.py           # Web interface (Chainlit)
├── main.py               # Command line entry point
├── run_frontend.py       # Frontend launcher
├── setup_config.py       # LLM provider setup
├── config.py             # Configuration management
├── config.json           # LLM provider settings (auto-created)
└── generated_code/       # Generated animation files
```

## 🎬 Example Prompts

- "Create an animation showing a bouncing ball"
- "Visualize the sine wave function"
- "Show a rotating cube in 3D"
- "Animate a growing circle that changes color"

## 🔧 Configuration

### Interactive Setup
```bash
python setup_config.py
```

### Manual Configuration
Edit `config.json`:
```json
{
  "provider": "openai",
  "model": "gpt-4o",
  "api_key": "your-api-key-here",
  "base_url": null
}
```

### Environment Variables (Alternative)
```bash
export ACTIVA_PROVIDER="claude"
export ACTIVA_MODEL="claude-3-5-sonnet-20241022"
export ACTIVA_API_KEY="your-api-key"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

## 📖 Documentation

- **[Frontend Guide](FRONTEND_README.md)** - Web interface usage
- **Code Comments** - Detailed implementation documentation
- **Example in main.py** - Sample usage and customization

## 🆘 Support

- Open an issue on GitHub
- Check the documentation
- Review example implementations