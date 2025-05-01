# Stella AI Assistant

Stella is an interactive AI assistant with advanced voice recognition and text-to-speech capabilities.

## Features

- Natural language voice input
- Speech-to-text transcription
- Conversational AI responses
- Customizable interaction modes

## Requirements

- Python 3.10
- PyTorch
- Whisper
- Silero VAD
- TensorFlow

## Installation

### Automated Setup
We've created a comprehensive setup script to make installation easy:

```bash
# Make the setup script executable
chmod +x setup.sh

# Run the setup script with sudo
sudo ./setup.sh
```

The setup script will:
- Install Python 3.10
- Create a virtual environment
- Install all required dependencies
- Help you configure OpenRouter API
- Allow you to personalize your AI assistant

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

### Run Streamlit Web App
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
