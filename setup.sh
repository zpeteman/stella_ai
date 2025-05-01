#!/bin/bash

# Color codes for better output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print error and exit
error_exit() {
    echo -e "${RED}Error: $1${NC}"
    exit 1
}

# Function to print success message
success() {
    echo -e "${GREEN}$1${NC}"
}

# Function to print warning message
warning() {
    echo -e "${YELLOW}$1${NC}"
}

# Check if script is run with sudo
if [[ $EUID -ne 0 ]]; then
   error_exit "This script must be run with sudo permissions"
fi

# Detect Linux distribution
detect_distro() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO=$ID
    else
        error_exit "Cannot detect Linux distribution"
    fi
}

# Install Python 3.10 based on distribution
install_python() {
    # Check if Python 3.10 is already installed
    if command -v python3.10 &> /dev/null; then
        success "Python 3.10 is already installed"
        return
    fi
    
    # Detect the operating system
    UNAME=$(uname -s)
    DISTRO=""
    
    case "$UNAME" in
        Linux)
            if [ -f /etc/os-release ]; then
                . /etc/os-release
                DISTRO=$ID
            else
                error_exit "Unsupported Linux distribution"
            fi
            ;;
        Darwin)
            DISTRO="macos"
            ;;
        *)
            error_exit "Unsupported operating system: $UNAME"
            ;;
    esac
    
    # Distribution-specific Python 3.10 installation
    case "$DISTRO" in
        ubuntu|debian|wsl)
            echo "[🐧] Detected Ubuntu/Debian/WSL"
            sudo apt-get update
            sudo apt-get install -y software-properties-common
            sudo add-apt-repository -y ppa:deadsnakes/ppa
            sudo apt-get update
            sudo apt-get install -y python3.10 python3.10-venv python3.10-dev
            ;;
        fedora)
            echo "[🐧] Detected Fedora"
            sudo dnf install -y python3.10 python3.10-devel
            ;;
        centos|rhel)
            echo "[🐧] Detected CentOS/RHEL"
            sudo yum install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
            sudo yum install -y python3.10
            ;;
        arch)
            echo "[🐧] Detected Arch Linux"
            sudo pacman -Sy --noconfirm python310
            ;;
        opensuse-leap|opensuse-tumbleweed)
            echo "[🐧] Detected openSUSE"
            sudo zypper install -y python310
            ;;
        alpine)
            echo "[🐧] Detected Alpine Linux"
            sudo apk add python3=~3.10
            ;;
        macos)
            echo "[🔴] Detected macOS"
            if ! command -v brew &> /dev/null; then
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            brew install python@3.10
            ;;
        *)
            warning "Unsupported distribution: $DISTRO. Attempting generic Python installation."
            if command -v python3 &> /dev/null; then
                PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
                if [[ "$PYTHON_VERSION" == 3.10* ]]; then
                    success "Using existing Python 3.10"
                    return
                fi
            fi
            error_exit "Cannot install Python 3.10 on $DISTRO"
            ;;
    esac
    
    # Verify Python 3.10 installation
    if ! command -v python3.10 &> /dev/null; then
        error_exit "Failed to install Python 3.10"
    fi
    
    success "Python 3.10 installed successfully"
}

# Create virtual environment
create_venv() {
    warning "Creating virtual environment"
    python3.10 -m venv ai
    source ai/bin/activate
}

# Install requirements
install_requirements() {
    warning "Installing project requirements"
    pip install --upgrade pip
    pip install -r requirements.txt
}

# Configure OpenRouter API
configure_openrouter() {
    read -p "Enter your OpenRouter API Key (or press Enter to skip): " OPENROUTER_KEY
    read -p "Choose a language model (default: openai/gpt-3.5-turbo): " LANGUAGE_MODEL
    
    # Use default if no model specified
    LANGUAGE_MODEL=${LANGUAGE_MODEL:-openai/gpt-3.5-turbo}
    
    if [ ! -z "$OPENROUTER_KEY" ]; then
        # Update configuration JSON
        jq --arg key "$OPENROUTER_KEY" --arg model "$LANGUAGE_MODEL" \
           '.openrouter_api_key = $key | .language_model = $model' config.json > temp.json && \
        mv temp.json config.json
        
        success "OpenRouter API Key and Language Model saved"
    else
        warning "Skipping OpenRouter API Key configuration"
    fi
}

# Personalize AI
personalize_ai() {
    read -p "Enter a name for your AI assistant: " AI_NAME
    read -p "Describe the personality of your AI (e.g., helpful, witty, serious): " AI_PERSONALITY
    
    # Update configuration JSON
    jq --arg name "$AI_NAME" --arg personality "$AI_PERSONALITY" \
       '.ai_name = $name | .ai_personality = $personality' config.json > temp.json && \
    mv temp.json config.json
    
    # Rename stella script to AI's name
    AI_SCRIPT_NAME=$(echo "$AI_NAME" | tr '[:upper:]' '[:lower:]' | sed 's/ /_/g')
    mv stella "$AI_SCRIPT_NAME"
    chmod +x "$AI_SCRIPT_NAME"
    
    # Update script content to use new name
    sed -i "s/Stella AI/$(echo "$AI_NAME" | sed 's/[/&]/\&/g') AI/g" "$AI_SCRIPT_NAME"
    
    success "AI personalized as $AI_NAME"
    echo "Your AI assistant script is now named: $AI_SCRIPT_NAME"
    echo "You can run it with: ./$AI_SCRIPT_NAME"
}

# Main setup function
main() {
    clear
    echo "🤖 AI Assistant Setup Script 🤖"
    
    warning "This comprehensive setup script will:"
    echo "1. Install Python 3.10"
    echo "2. Create a virtual environment"
    echo "3. Install project dependencies"
    echo "4. Configure OpenRouter AI"
    echo "5. Personalize your AI assistant"
    
    # Detailed usage instructions
    echo "
📘 Usage Guide:"
    echo "- This script helps you set up a personalized AI assistant"
    echo "- You'll be guided through configuration steps"
    echo "- Customize your AI's name, personality, and language model"
    echo "- Optional: Configure OpenRouter API for advanced interactions"
    
    # Confirm before proceeding
    read -p "
🚀 Do you want to continue with setup? (y/n): " confirm
    if [[ $confirm != [yY] && $confirm != [yY][eE][sS] ]]; then
        error_exit "Setup cancelled"
    fi
    
    # Run installation steps
    install_python
    create_venv
    install_requirements
    configure_openrouter
    personalize_ai
    
    # Post-setup instructions
    echo "
✅ Setup Complete!"
    echo "Activate virtual environment: source ai/bin/activate"
    echo "Run CLI: ./<your_ai_name_script>"
    echo "Optional: streamlit run app.py for web interface"
    
    # Additional guidance
    echo "
🔍 Next Steps:"
    echo "1. Explore your AI's capabilities"
    echo "2. Customize further in config.json"
    echo "3. Check README.md for advanced configuration"
}

# Make stella script executable
chmod +x stella

# Run the main setup function
main
