# Stella AI Assistant

Stella is an interactive AI assistant with advanced voice recognition and text-to-speech capabilities.

## Features

- 🎙️ Natural language voice input
- 🔊 Speech-to-text transcription
- 💬 Conversational AI responses
- 🛠️ Highly customizable AI assistant
- 🌐 Multiple interaction modes (CLI, Web)
- 🤖 Personalized AI personality

## Requirements

### Supported Platforms
#### Linux Distributions
- 🐧 Ubuntu/Debian
- 🐧 Fedora
- 🐧 CentOS/RHEL
- 🐧 Arch Linux
- 🐧 openSUSE
- 🐧 Alpine Linux
- 🐧 Windows Subsystem for Linux (WSL)

#### Other Platforms
- 🍎 macOS (Intel & Apple Silicon)
- 🪟 Windows (via WSL2)

### System Requirements
- Python 3.10
- PyTorch
- Whisper
- Silero VAD
- TensorFlow

### Minimum Hardware
- 4GB RAM
- 10GB Disk Space
- x86_64/ARM64 Architecture

## Installation

### Automated Setup
We've created a comprehensive, cross-platform setup script:

```bash
# Make the setup script executable
chmod +x setup.sh

# Run the setup script
./setup.sh
```

#### Cross-Platform Installation
- 🌐 Automatically detects your operating system
- 🐍 Installs Python 3.10 using native methods
  - Linux: Package managers
  - macOS: Homebrew
  - Windows: WSL package manager
- 🔧 Creates a virtual environment
- 📦 Installs all required dependencies
- 🔐 Helps you configure OpenRouter API
- 🤖 Allows personalization of your AI assistant

#### Troubleshooting
- 🛠️ Ensure you have necessary permissions
- 🔍 Check system requirements
- 💻 For Windows: Use WSL2 for best compatibility
- ❓ Unsupported platform? Check manual installation

### Manual Installation
If you prefer manual setup:

```bash
# Clone the repository
git clone https://github.com/yourusername/stella.git
cd stella

# Create a virtual environment
python3.10 -m venv ai
source ai/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Activate Virtual Environment
```bash
source ai/bin/activate
```

### Run CLI Application
```bash
# Activate virtual environment first
source ai/bin/activate

# Run the CLI (using the script named after your AI)
./<your_ai_name_script>
```

### CLI Usage Guide
- Simply run the script to start an interactive conversation
- Type your messages and receive AI responses
- Use voice commands (when implemented)
- Type 'exit' or 'quit' to end the conversation

#### Example Interaction
```
$ ./luna
Luna AI: Hello! How can I help you today?
You: Tell me a joke
Luna AI: Why don't scientists trust atoms? Because they make up everything! 😄
You: quit
```

### Optional: Streamlit Web App
```bash
streamlit run app.py
```

### Customization
- Use the setup script to configure:
  - AI Name
  - AI Personality
  - OpenRouter API Key
  - Language Model
- Configuration is stored in `config.json`
- Modify settings by running `./setup.sh` again

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
