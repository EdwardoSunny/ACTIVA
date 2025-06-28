# 🎬 Frontend Usage Guide

Web-based interface for the ACTIVA Code Generation Agent built with Chainlit.

## 🚀 Quick Start

### Prerequisites
1. **Install dependencies**: `pip install -e .`
2. **Configure LLM provider**: `python setup_config.py`
3. **Run frontend**: `python run_frontend.py`
4. **Open browser**: `http://localhost:8000`

## ✨ Features

- **Chat Interface**: Type animation requests in plain English
- **Progress Updates**: Real-time status during generation and execution
- **Code Display**: Formatted Python code with syntax highlighting
- **File Organization**: Generated code saved in `generated_code/` directory
- **Interactive Buttons**: Run animations, retry, or create new prompts
- **Error Handling**: Automatic retry with detailed error messages
- **Multi-LLM Support**: Works with OpenAI, Claude, and Gemini

## 📋 Usage

1. **Send a prompt**: "Create a bouncing ball animation"
2. **Wait for generation**: See progress updates
3. **Review code**: Check the generated Manim code
4. **Run animation**: Click "Run Animation" to execute
5. **Repeat**: Use buttons to retry or create new animations

## 📁 File Output

- **Code files**: `generated_code/manim_animation_TIMESTAMP.py`
- **Animation files**: `media/` directory (Manim default)
- **Paths displayed**: Full file locations shown in chat

## 🎯 Example Prompts

- "Create an animation showing a bouncing ball"
- "Visualize the sine wave function"
- "Show a rotating cube in 3D"
- "Animate a growing circle that changes color"

## 🔧 Configuration

### LLM Provider Setup
Before using the frontend, configure your preferred LLM provider:

```bash
python setup_config.py
```

**Supported Providers:**
- **OpenAI**: GPT-4o, GPT-4-turbo, GPT-3.5-turbo
- **Claude**: Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Sonnet
- **Gemini**: Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini Pro

### Manual Configuration
Edit `config.json`:
```json
{
  "provider": "openai",
  "model": "gpt-4o",
  "api_key": "your-api-key-here"
}
```

## 🔧 Troubleshooting

- **Port in use**: Change port in `run_frontend.py`
- **Chainlit missing**: Automatically installed by run script
- **File locations**: Check chat for exact paths
- **LLM errors**: Verify API key and provider settings in `config.json`
- **Missing dependencies**: Run `pip install -e .`

## 📖 Requirements

- Python 3.10+
- Dependencies from `pyproject.toml`
- Chainlit (auto-installed)
- Valid API key for chosen LLM provider 