# ACTIVA: Accounting Concepts Taught Interactively with Visual Animations

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

**ACCOUNTING CONCEPTS TAUGHT INTERACTIVELY WITH VISUAL ANIMATIONS (ACTIVA)** is a novel Large Language Model (LLM)-based animation tool designed to enhance accounting education through automated visualizations. Grounded in cognitive theory of multimedia learning, ACTIVA bridges the gap between abstract accounting constructs and practical applications by generating custom animations from natural language prompts.

## 🎯 Key Features

- **Multi-Agent Framework**: Sophisticated agent-based system for intelligent animation generation
- **Natural Language Processing**: Convert accounting problems into visual animations using simple text prompts
- **Real-time Generation**: Dynamic, automated creation of accounting process demonstrations
- **LLM Compatibility**: Works seamlessly with both ChatGPT and Claude
- **Error Recovery**: Intelligent error detection and automatic code correction
- **Cost-Effective**: Significantly more affordable than manually produced animations

## 🏗️ Architecture

ACIVA employs a sophisticated multi-agent framework built with LangGraph that orchestrates four specialized agents working in sequence:

**Planning & Search Agent**: The workflow begins with this agent analyzing the natural language task and searching for relevant Manim implementation examples to guide the code generation process.

**Code Writing Agent**: This agent generates the initial Manim Python code based on the task description and implementation guide. It creates complete, executable animation scripts following Manim best practices.

**Execution Agent**: The generated code is then executed by this agent, which runs the Manim animation and captures the output. It determines whether the animation was successful or encountered errors.

**Error Search Agent**: If execution fails, this agent searches for specific solutions to the encountered errors using web search capabilities and provides targeted fixes.

The system operates in an iterative loop where the Error Search Agent feeds solutions back to the Code Writing Agent for code revision, continuing until successful execution or reaching the maximum attempt limit. This self-correcting mechanism ensures robust animation generation even for complex accounting concepts.

## 📋 Prerequisites

- Python 3.10 or higher
- OpenAI API key (for GPT-4o integration)
- Manim library for animation generation

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/activa.git
   cd activa
   ```

2. **Install dependencies**:
   ```bash
   pip install -e .
   ```

3. **Set up your API key**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

## 💻 Usage

### Basic Usage

Run the main script with a predefined accounting problem:

```bash
python main.py
```

### Custom Usage

Modify the `task` variable in `main.py` to create animations for your specific accounting concepts:

```python
task = """
Please create an animation visualization to explain accrual accounting 
for Lind Co.'s salaries expense of $10,000 paid every other Friday.
"""
```

### Example Use Cases

#### 1. Accrual Accounting Animation
```python
task = """
Create an animation showing how to calculate accrued salaries expense 
for a company that pays $10,000 every other Friday, with the last 
payment on June 18th and month-end on June 30th.
"""
```

#### 2. Depreciation Methods Animation
```python
task = """
Generate an animation demonstrating straight-line vs. declining 
balance depreciation methods for a $50,000 asset with 5-year life.
"""
```

## 🔧 Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for LLM access
- `MANIM_QUALITY`: Animation quality setting (default: `-pql` for preview quality)

### Customization Options

Modify the agent configuration in `activa/agent/graph.py`:

```python
config = {
    "recursion_limit": 50,  # Maximum attempts for code generation
    "timeout": 45,          # Execution timeout in seconds
}
```

## 📁 Project Structure

```
activa/
├── agent/
│   ├── graph.py          # Main agent workflow definition
│   ├── nodes.py          # Individual agent node implementations
│   └── state.py          # State management for agent workflow
├── utils/
│   └── manim_tools.py    # Manim execution and error handling utilities
├── main.py               # Entry point for the application
├── pyproject.toml        # Project dependencies and metadata
└── README.md            # This file
```

## 🎬 Animation Examples

ACIVA can generate various types of accounting animations:

- **Journal Entry Visualizations**: Animated T-accounts and ledger entries
- **Financial Statement Animations**: Dynamic income statement and balance sheet presentations
- **Process Flow Diagrams**: Step-by-step accounting procedure demonstrations
- **Calculation Animations**: Visual representations of complex accounting formulas
- **Timeline Visualizations**: Temporal aspects of accrual and deferral accounting

## 🔍 Error Handling

The system includes intelligent error recovery:

1. **Automatic Error Detection**: Identifies Manim execution errors
2. **Solution Search**: Searches for relevant fixes using web search
3. **Code Revision**: Automatically revises code based on error analysis
4. **Iterative Improvement**: Continues until successful execution or max attempts reached

## 🧪 Testing

Run the included example to test the system:

```bash
python main.py
```

The system will generate an animation for the sample accrual accounting problem and save the successful code to `final_manim_animation.py`.

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Open an issue on GitHub
- Check the documentation in the code comments
- Review the example implementations

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) for agent orchestration
- Powered by [Manim](https://github.com/ManimCommunity/manim) for mathematical animations
- Enhanced with OpenAI's GPT-4o for intelligent code generation

---

**ACIVA** - Transforming accounting education through intelligent visual animations.
