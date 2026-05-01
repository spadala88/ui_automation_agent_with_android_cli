# 🤖 UI Automation Agent (Android CLI Edition)

An intelligent, LLM-powered Android UI automation framework that replaces traditional OCR and brittle coordinate-based clicking with native, direct Android CLI layout parsing.

Designed specifically for **Agentic Orchestration** on local Windows machines, this tool allows local AI models to navigate Android applications autonomously using a "Reason-Act-Observe" cognitive loop.

## ✨ Key Features

* **🔍 Direct Layout Parsing:** Utilizes the `android layout -p` command to fetch the exact semantic UI tree. This completely eliminates the "hallucinations" and inaccuracies common with OCR-based text detection (like EasyOCR).
* **🧠 Agentic Orchestration:** Operates on a continuous "Reason-Act-Observe" loop. The LLM reads the live UI state, reasons about its objective, decides which button to click, and observes the result.
* **🔄 Repetitive Workflow Engine:** Built-in support for executing complex, multi-step navigation cycles automatically (e.g., *Home → Favorites → Profile*).
* **⚡ Local-First AI (Gemma Integration):** Optimized out-of-the-box for the `gemma4:e4b` model via **Ollama**, allowing for high-speed, offline local reasoning. Perfectly tuned for execution on standard 32GB RAM developer laptops.

## 📂 Repository Structure

```text
📦 ui_automation_agent_with_android_cli
 ┣ 📂 agentic_automation/   # Core Python agent logic and tools
 ┣ 📜 app-debug.apk         # Sample target application for testing
 ┣ 📜 requirements.txt      # Python dependencies
 ┗ 📜 README.md             # Project documentation
🛠️ Prerequisites
Before running the agent, ensure your environment meets the following requirements:

Python 3.10+ installed on your system.

Android Studio / Android SDK installed, with an emulator running or a physical device connected via USB.

ADB & Android CLI added to your system PATH.

Ollama installed and running locally.

🚀 Installation & Setup
1. Clone the repository

Bash
git clone [https://github.com/spadala88/ui_automation_agent_with_android_cli.git](https://github.com/spadala88/ui_automation_agent_with_android_cli.git)
cd ui_automation_agent_with_android_cli
2. Install Python dependencies
We recommend using a virtual environment.

Bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
3. Pull the local AI model
Ensure Ollama is running in the background, then pull the optimized Gemma model:

Bash
ollama pull gemma4:e4b
🎮 Usage
Step 1: Launch your Android Emulator or connect your physical device. Verify the connection:

Bash
adb devices
Step 2: (Optional) If you want to test the agent on the provided sample app, install it using ADB:

Bash
adb install app-debug.apk
Step 3: Run the autonomous agent:

Bash
cd agentic_automation
python main.py  # (Or the specific entrypoint script in this folder)
🏗️ How It Works (The Agent Loop)
Instead of relying on visual pixels, this framework reads the code.

Observe: The agent runs android layout -p to dump the current application state as a structured JSON/XML tree.

Reason: The local Gemma model ingests this tree, understands the semantic hierarchy (knowing exactly what is a Button vs. a TextView), and cross-references it with your assigned objective.

Act: The agent uses the android screen resolve CLI command to calculate the exact geometric center of the target UI node and injects an adb shell input tap command.

Repeat: The cycle starts over to verify the action succeeded or to perform the next step.

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

📝 License
Distributed under the MIT License. See LICENSE for more information.
