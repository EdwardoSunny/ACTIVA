# ACTIVA: Accounting Concepts Taught Interactively with Visual Animations

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

### Install Manim

The main instructions are located on [this official documentation page](https://docs.manim.community/en/stable/installation/uv.html). 

If you are on any Linux distribution, make sure you have `cairo` and `pango` installed.

```bash
# debian/apt
sudo apt install build-essential python3-dev libcairo2-dev libpango1.0-dev

# fedora/dnf
sudo dnf install python3-devel pkg-config cairo-devel pango-devel

# arch/pacman
sudo pacman -Syu base-devel cairo pango
```

To check if you installed Manim correctly, run:
```bash
manim checkhealth
```

### 1. Install Dependencies
```bash
git clone https://github.com/EdwardoSunny/ACTIVA
cd ACTIVA
pip install -e .
```

### 2. Set Up API Access
ACTIVA requires an API key from one of the supported LLM providers. You'll need to:

**Get API Keys:**
- **OpenAI**: Visit [platform.openai.com](https://platform.openai.com) and create an account
- **Claude (Anthropic)**: Visit [console.anthropic.com](https://console.anthropic.com) and sign up
- **Gemini (Google)**: Visit [makersuite.google.com](https://makersuite.google.com) and get an API key

**Configure ACTIVA:**
```bash
python scripts/setup_config.py
```
Choose your preferred provider and enter your API key when prompted.

### 3. Supported Models
ACTIVA works with the following models:

- **OpenAI**: GPT-4o (recommended), GPT-4-turbo, GPT-3.5-turbo
- **Claude**: Claude 3.5 Sonnet (recommended), Claude 3 Opus, Claude 3 Sonnet  
- **Gemini**: Gemini 1.5 Pro (recommended), Gemini 1.5 Flash, Gemini Pro

The interactive setup will guide you through model selection. For best results, we recommend using the latest models (GPT-4o, Claude 3.5 Sonnet, or Gemini 1.5 Pro).

### 4. Run ACTIVA
**Frontend (Recommended):**
```bash
python scripts/run_frontend.py
```
Then open `http://localhost:8000` in your browser.

**Command Line:**
```bash
python main.py
```

📖 **See [docs/FRONTEND_README.md](docs/FRONTEND_README.md) for detailed frontend usage.**

## 🎯 What is ACTIVA?

**ACCOUNTING CONCEPTS TAUGHT INTERACTIVELY WITH VISUAL ANIMATIONS (ACTIVA)** is an LLM-based animation tool that generates custom accounting visualizations from natural language prompts. It uses a multi-agent framework to automatically create Manim animations for accounting education, helping students understand complex accounting concepts through visual representations.

## ✨ Key Features

- **Natural Language Input**: Describe accounting concepts in plain English
- **Multi-Agent System**: Intelligent planning, coding, execution, and error recovery
- **Multiple LLM Support**: Works with OpenAI, Claude, and Gemini
- **Error Recovery**: Automatic debugging and code correction
- **Cost-Effective**: Much cheaper than manual animation production
- **Accounting-Focused**: Specialized for accounting education and concept visualization

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
VisualsGeneration/
├── docs/                  # 📚 Documentation
│   ├── README.md         # Main project documentation (this file)
│   └── FRONTEND_README.md # Frontend usage guide
├── scripts/               # 🔧 Utility Scripts
│   ├── setup_config.py   # LLM provider setup
│   └── run_frontend.py   # Frontend launcher
├── config/                # ⚙️ Configuration
│   ├── config.py         # Configuration management
│   └── config.json       # LLM provider settings (auto-created)
├── .chainlit/             # 🌐 Chainlit Configuration
│   └── config.toml       # Frontend timeout and server settings
├── activa/                # 🧠 Core Agent System
│   ├── agent/            # Multi-agent framework
│   │   ├── graph.py      # Agent workflow definition
│   │   ├── nodes.py      # Individual agent implementations
│   │   └── state.py      # State management
│   └── utils/            # Manim execution utilities
│       └── manim_tools.py # Code execution and error handling
├── frontend.py           # 🌐 Web interface (Chainlit)
├── main.py               # 🖥️ Command line entry point
├── chainlit.md           # 📋 Chainlit sidebar content
├── pyproject.toml        # 📦 Project dependencies
├── LICENSE               # 📄 License information
└── generated_code/       # 📁 Generated animation files
```

## 🎬 Example Prompts

- "Create an animation showing how to calculate depreciation expense using the straight-line method"
- "Visualize the accounting equation: Assets = Liabilities + Equity"
- "Show a cash flow statement with animated transitions between operating, investing, and financing activities"
- "Animate a journal entry showing the purchase of equipment on credit"

## 🔧 Configuration

### Interactive Setup
```bash
python scripts/setup_config.py
```

### Manual Configuration
Edit `config/config.json`:
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

### Frontend Configuration
The frontend includes extended timeout settings (5 minutes) for long-running operations:
- **Agent Generation**: Up to 5 minutes for code generation
- **Animation Execution**: Up to 5 minutes for Manim rendering
- **Progress Updates**: Real-time status during operations

## 🚀 Usage Examples

### Quick Test
```bash
# 1. Setup (one-time)
python scripts/setup_config.py

# 2. Run frontend
python scripts/run_frontend.py

# 3. Open browser to http://localhost:8000
# 4. Type: "Create an animation showing how to calculate accrued salaries expense"
```

### Command Line Usage
```bash
# Run the example in main.py (accounting salaries expense example)
python main.py
```

## 🔧 Troubleshooting

### Common Issues
- **Timeout Errors**: The frontend is configured with 5-minute timeouts for long operations
- **Connection Issues**: Check your internet connection and API key validity
- **Generation Failures**: Try simpler prompts first, then increase complexity

### Frontend Issues
- **Server Won't Start**: Run `python scripts/run_frontend.py` from the project root
- **Timeout During Generation**: The system automatically handles long operations
- **Animation Execution Fails**: Check the generated code in `generated_code/` directory

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

## 🆘 Support

- Open an issue on GitHub
- Check the documentation
- Review example implementations
