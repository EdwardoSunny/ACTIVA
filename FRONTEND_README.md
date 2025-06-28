# 🎬 Frontend Usage Guide

This project now includes a simple web-based frontend built with Chainlit for easy testing and interaction with the ACTIVA Code Generation Agent.

## Quick Start

### Option 1: Using the run script (Recommended)
```bash
python run_frontend.py
```

### Option 2: Direct Chainlit command
```bash
# Install chainlit if not already installed
pip install chainlit>=1.0.0

# Run the frontend
chainlit run frontend.py --port 8000
```

## Features

The frontend provides:

- **Simple Chat Interface**: Just type your animation request
- **Code Generation**: Automatic Manim code generation with error handling
- **Progress Updates**: Clear status messages during generation and execution
- **Code Display**: Formatted code output with syntax highlighting
- **File Saving**: Generated code is automatically saved with timestamps in organized directory
- **Animation Execution**: Optional button to run the generated animation
- **File Location Display**: Shows exactly where code and animation files are saved
- **Interactive Buttons**: Easy navigation between actions
- **Retry Logic**: Built-in retry mechanisms for failed generations
- **Error Handling**: Detailed error messages and debugging information

## Usage Flow

1. **Start the frontend** using one of the methods above
2. **Open your browser** to `http://localhost:8000`
3. **Describe your animation** in the chat (e.g., "Create a bouncing ball animation")
4. **Wait for generation** - you'll see progress updates
5. **Review the code** displayed in the chat
6. **Check file locations** - the app shows where everything is saved
7. **Choose next action**:
   - 🚀 Run Animation: Execute the code to see the result
   - 🔄 New Prompt: Try a different animation
   - 🔄 Rerun Same: Retry the same prompt

## File Output

- **Code files**: Saved as `generated_code/manim_animation_TIMESTAMP.py` (organized directory)
- **Animation files**: Generated in the `media/` directory (default Manim output)
- **File locations**: Clearly displayed in the chat interface
- **Directory structure**: Keeps your project root clean and organized

## Example Prompts

- "Create an animation showing a bouncing ball"
- "Visualize the sine wave function with a moving point"
- "Show a rotating cube in 3D space"
- "Animate a growing circle that changes color"
- "Create a bar chart animation showing data over time"

## Progress Updates

The frontend now provides:
- ✅ Status messages during code generation
- ✅ Progress updates during animation execution
- ✅ Clear indication of where files are saved
- ✅ Detailed success/error messages
- ✅ File location information for both code and animations

## Troubleshooting

- **Port already in use**: Change the port in `run_frontend.py` or use a different port
- **Chainlit not found**: The run script will automatically install it
- **Agent errors**: Check the console output for detailed error messages
- **File locations**: The app shows exactly where files are saved
- **Generated code directory**: Automatically created if it doesn't exist

## Requirements

- Python 3.10+
- All dependencies from `pyproject.toml`
- Chainlit (automatically installed by the run script)

## What's New

- **Progress Updates**: No more blank screens during execution
- **File Location Display**: Clear indication of where code and animations are saved
- **Better Error Handling**: More detailed error messages and debugging info
- **Timestamped Files**: Generated code files include timestamps to avoid conflicts
- **Media File Detection**: Automatically finds and displays generated animation files
- **Organized File Structure**: Generated code saved in `generated_code/` directory

---

*The frontend makes it easy to test and experiment with the ACTIVA Code Generation Agent without writing any code!* 