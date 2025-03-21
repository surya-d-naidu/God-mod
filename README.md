# God Mod - AI-Powered Code Generation Assistant

A powerful desktop application that automatically generates and types code using Google's Gemini AI models. Built with Python and CustomTkinter for a modern, sleek interface.

## Authors

- [Murky Shelf](https://github.com/murkyshelf)
- [Surya D Naidu](https://github.com/surya-d-naidu)

## Features

- 🤖 Multiple Gemini AI model support:
  - Gemini 1.5 Flash (Fast and efficient)
  - Gemini 1.5 Pro (More accurate but slower)
  - Gemini 2.0 Flash (Latest model with improved performance)
- ⌨️ Human-like typing simulation with adjustable speed
- 🔒 Secure API key storage with encryption
- 💾 Automatic preference saving
- 🎨 Modern, dark-themed UI with CustomTkinter
- 🌐 Support for any programming language
- 📝 Custom prefix prompt support
- 🔄 Real-time clipboard monitoring
- ⚡ Fast typing mode for quick code generation

## Installation

### Option 1: Using the Executable (Recommended)

1. Download the latest release from the releases page
2. Extract the zip file
3. Run `GodMod.exe` (Windows) or `GodMod.app` (macOS)

### Option 2: Building from Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/god-mod.git
cd god-mod
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create the application icon:
```bash
python create_icon.py
```

5. Build the executable:
```bash
pyinstaller godmod.spec
```

The executable will be created in the `dist` folder.

## Usage

1. Launch the application
2. Enter your Google API key in the settings
3. Select a programming language or enter a custom one
4. Enter your code in the input box
5. Click "Start Typing" to begin the simulation
6. Use the speed slider to adjust typing speed
7. Click "Stop" to end the simulation

## Requirements

- Python 3.8 or higher
- Google API key
- Windows 10/11 (for the executable)

## Development

To modify the application:

1. Install development dependencies:
```bash
pip install -r requirements-dev.txt
```

2. Make your changes
3. Test the application
4. Rebuild the executable using the spec file

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Generative AI for providing the API
- customtkinter for the modern UI components
- All contributors and users of the application 