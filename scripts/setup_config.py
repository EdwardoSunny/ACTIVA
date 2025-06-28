#!/usr/bin/env python3
"""
Setup script for ACTIVA configuration.
Helps users set up their preferred LLM provider.
"""

import json
import os

def setup_config():
    """Interactive setup for ACTIVA configuration."""
    print("🎬 ACTIVA Configuration Setup")
    print("=" * 40)
    
    # Provider selection
    print("\n📋 Select your LLM provider:")
    print("1. OpenAI (GPT-4o, GPT-4, etc.)")
    print("2. Claude (Anthropic)")
    print("3. Gemini (Google)")
    
    while True:
        choice = input("\nEnter your choice (1-3): ").strip()
        if choice == "1":
            provider = "openai"
            break
        elif choice == "2":
            provider = "claude"
            break
        elif choice == "3":
            provider = "gemini"
            break
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
    
    # Model selection based on provider
    if provider == "openai":
        print("\n🤖 Select OpenAI model:")
        print("1. gpt-4o (recommended)")
        print("2. gpt-4-turbo")
        print("3. gpt-3.5-turbo")
        print("4. Custom model name")
        
        model_choice = input("Enter your choice (1-4): ").strip()
        if model_choice == "1":
            model = "gpt-4o"
        elif model_choice == "2":
            model = "gpt-4-turbo"
        elif model_choice == "3":
            model = "gpt-3.5-turbo"
        elif model_choice == "4":
            model = input("Enter custom model name: ").strip()
        else:
            model = "gpt-4o"
    
    elif provider == "claude":
        print("\n🤖 Select Claude model:")
        print("1. claude-3-5-sonnet-20241022 (recommended)")
        print("2. claude-3-opus-20240229")
        print("3. claude-3-sonnet-20240229")
        print("4. Custom model name")
        
        model_choice = input("Enter your choice (1-4): ").strip()
        if model_choice == "1":
            model = "claude-3-5-sonnet-20241022"
        elif model_choice == "2":
            model = "claude-3-opus-20240229"
        elif model_choice == "3":
            model = "claude-3-sonnet-20240229"
        elif model_choice == "4":
            model = input("Enter custom model name: ").strip()
        else:
            model = "claude-3-5-sonnet-20241022"
    
    elif provider == "gemini":
        print("\n🤖 Select Gemini model:")
        print("1. gemini-1.5-pro (recommended)")
        print("2. gemini-1.5-flash")
        print("3. gemini-pro")
        print("4. Custom model name")
        
        model_choice = input("Enter your choice (1-4): ").strip()
        if model_choice == "1":
            model = "gemini-1.5-pro"
        elif model_choice == "2":
            model = "gemini-1.5-flash"
        elif model_choice == "3":
            model = "gemini-pro"
        elif model_choice == "4":
            model = input("Enter custom model name: ").strip()
        else:
            model = "gemini-1.5-pro"
    
    # API Key input
    print(f"\n🔑 Enter your {provider.upper()} API key:")
    api_key = input("API Key: ").strip()
    
    if not api_key:
        print("❌ API key is required!")
        return
    
    # Optional base URL (for custom endpoints)
    print("\n🌐 Base URL (optional, press Enter to skip):")
    print("Leave empty for default endpoints, or enter custom URL for local/alternative endpoints")
    base_url = input("Base URL: ").strip()
    if not base_url:
        base_url = None
    
    # Create config
    config_data = {
        "provider": provider,
        "model": model,
        "api_key": api_key,
        "base_url": base_url,
        "_comment": "Supported providers: openai, claude, gemini"
    }
    
    # Save config
    config_path = os.path.join("..", "config", "config.json")
    with open(config_path, 'w') as f:
        json.dump(config_data, f, indent=2)
    
    print("\n✅ Configuration saved to config.json!")
    print(f"📋 Provider: {provider}")
    print(f"🤖 Model: {model}")
    print(f"🔑 API Key: {'*' * (len(api_key) - 4) + api_key[-4:] if len(api_key) > 4 else '***'}")
    if base_url:
        print(f"🌐 Base URL: {base_url}")
    
    print("\n🚀 You can now run ACTIVA with:")
    print("   python run_frontend.py")
    print("   or")
    print("   python main.py")

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    missing_deps = []
    
    try:
        import langchain_openai
        print("✅ langchain-openai")
    except ImportError:
        missing_deps.append("langchain-openai")
        print("❌ langchain-openai")
    
    try:
        import langchain_anthropic
        print("✅ langchain-anthropic")
    except ImportError:
        missing_deps.append("langchain-anthropic")
        print("❌ langchain-anthropic")
    
    try:
        import langchain_google_genai
        print("✅ langchain-google-genai")
    except ImportError:
        missing_deps.append("langchain-google-genai")
        print("❌ langchain-google-genai")
    
    if missing_deps:
        print(f"\n⚠️ Missing dependencies: {', '.join(missing_deps)}")
        print("Install with: pip install -e .")
        return False
    
    print("\n✅ All dependencies are installed!")
    return True

if __name__ == "__main__":
    print("🎬 ACTIVA Setup")
    print("=" * 20)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Please install missing dependencies before continuing.")
        exit(1)
    
    # Run setup
    setup_config() 