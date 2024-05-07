# 🧙‍♂️ Opus Interpreter

Welcome to **Opus Interpreter**! 🚀 A magical Python data science environment where you can use **Anthropic's Claude** in tandem with a **secure sandbox** to generate and execute Python code on the fly. This project leverages Claude and the **Code Interpreter API by e2b** to create a seamless, interactive data science experience. Say goodbye to repetitive coding and hello to effortless productivity! 🎩✨

The script as well this readme were created entirely by **im-a-good-gpt2-chatbot**

## Features 🌟
### 1. **Claude as a Python Data Scientist**
- **Anthropic Claude API Integration**: Claude-3 is your AI data scientist.
- **Dynamic Code Generation**: Generate Python code based on your user message.
- **Interactive Execution**:
  - Execute Python code in a secure environment.
  - Fetch execution results, logs, and any visualizations.

### 2. **Powerful Code Interpreter API**
- **Execute Python Code**: Run Python code in a Jupyter notebook-like environment.
- **Files & Logs Management**: Save results, tracebacks, and logs for future reference.
- **Tools Integration**:
  - **execute_python**: Execute Python code in a separate cell.

### 3. **Secure Sandbox Execution**
- **Secure Python Sandbox**: Execute Python code in a controlled environment.
- **Filesystem Access**:
  - Read/write files.
  - Download files generated during execution.

## Getting Started 🛠️
### Prerequisites
1. **Python**: Ensure you have Python 3.8 or above installed.
2. **API Keys**:
   - **Anthropic Claude API Key**.
   - **E2B Code Interpreter API Key**.

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Doriandarko/opus-interpreter.git
   cd opus-interpreter
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` File**:
   Add your API keys to a `.env` file in the root directory:
   ```ini
   # .env file
   ANTHROPIC_API_KEY=<your_anthropic_api_key>
   E2B_API_KEY=<your_e2b_api_key>
   ```

### Usage
1. **Run the Script**:
   ```bash
   python opus-interpreter.py
   ```

2. **Chat with Claude**:
   - Enter your message to ask Claude for code snippets or analysis.
   - Use `quit` to exit.

## Sample Messages 💬
- **Data Analysis**: "Analyze this dataset and show me a summary."
- **Visualization**: "Create a scatter plot comparing columns X and Y."
- **Code Generation**: "Write a Python function to calculate Fibonacci numbers."

## Behind the Magic 🎩
### How It Works
1. **System Prompt**: Sets up Claude as a Python data scientist.
2. **Tool Definition**:
   - `execute_python`: Executes Python code in a secure environment.
3. **Chat Functionality**:
   - **chat**: Handles user messages and interprets Claude's response.
   - **code_interpret**: Executes Python code and manages results, logs, and files.


## Contributing
All wizards and data enthusiasts are welcome to contribute! Feel free to:
- Open issues for bugs or feature requests.
- Submit pull requests with improvements.

## License
This project is licensed under the MIT License.

Feel free to reach out with questions or suggestions. Remember, **Claude** and **Code Interpreter** are here to help you **level up your data science game**! 🎯
