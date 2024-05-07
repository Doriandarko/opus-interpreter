import os
import base64
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np
from anthropic import Anthropic
from typing import List, Tuple
from e2b_code_interpreter import CodeInterpreter, Result
from e2b_code_interpreter.models import Logs
from e2b import Sandbox

# Load the .env file
load_dotenv()

# Set up the Anthropic client
client = Anthropic()

# Initialize the Sandbox
sandbox = Sandbox(template="base")

# Define the model name, system prompt, and tools
MODEL_NAME = "claude-3-opus-20240229"

SYSTEM_PROMPT = """
## your job & context
you are a python data scientist. you are given tasks to complete and you run python code to solve them.
- the python code runs in jupyter notebook.
- every time you call `execute_python` tool, the python code is executed in a separate cell. it's okay to make multiple calls to `execute_python`.
- display visualizations using matplotlib or any other visualization library directly in the notebook. don't worry about saving the visualizations to a file.
- you have access to the internet and can make api requests.
- you also have access to the filesystem and can read/write files.
- you can install any pip package (if it exists) if you need to but the usual packages for data analysis are already preinstalled.
- you can run any python code you want, everything is running in a secure sandbox environment.
"""

tools = [
    {
        "name": "execute_python",
        "description": "Execute python code in a Jupyter notebook cell and returns any result, stdout, stderr, display_data, and error.",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The python code to execute in a single cell."
                }
            },
            "required": ["code"]
        }
    }
]

def code_interpret(code_interpreter: CodeInterpreter, code: str):
    print(f"\n{'='*50}\n> Running following AI-generated code:\n{code}\n{'='*50}")
    execution = code_interpreter.notebook.exec_cell(code)

    if execution.error:
        error_message = f"There was an error during execution: {execution.error.name}: {execution.error.value}.\n{execution.error.traceback}"
        print("[Code Interpreter error]", error_message)
        return [], Logs(), error_message, []

    result_message = ""
    saved_files = []

    if execution.results:
        result_message = "These are results of the execution:\n"
        counter = 1
        for result in execution.results:
            result_message += f"Result {counter}:\n"
            if result.is_main_result:
                result_message += f"[Main result]: {result.text}\n"
            else:
                result_message += f"[Display data]: {result.text}\n"

            # Check if the result has any file data and dynamically decide the filename and format
            file_saved = False
            for file_type in ['png', 'jpeg', 'svg', 'pdf', 'html', 'json', 'javascript', 'markdown', 'latex']:
                if getattr(result, file_type, None):
                    file_extension = file_type
                    file_data = getattr(result, file_type)
                    file_path = f"/home/user/output_file_{counter}.{file_extension}"
                    local_filename = f"output_file_{counter}.{file_extension}"
                    
                    try:
                        # Write file inside sandbox if it's not already a downloadable type
                        if not file_saved:
                            sandbox_path = f"/home/user/output_file_{counter}.{file_extension}"
                            sandbox.filesystem.write_bytes(sandbox_path, base64.b64decode(file_data))
                            file_saved = True

                        # Download file
                        file_in_bytes = sandbox.download_file(sandbox_path)
                        with open(local_filename, "wb") as file:
                            file.write(file_in_bytes)
                        saved_files.append(local_filename)
                        print(f"Saved locally: {local_filename}")
                    except Exception as e:
                        print(f"Failed to download {sandbox_path}: {str(e)}")

            counter += 1

        print(result_message)

    if execution.logs.stdout or execution.logs.stderr:
        log_message = "Logs:\n"
        if execution.logs.stdout:
            log_message += f"Stdout: {' '.join(execution.logs.stdout)}\n"
        if execution.logs.stderr:
            log_message += f"Stderr: {' '.join(execution.logs.stderr)}\n"
        result_message += log_message
        print(log_message)

    if not result_message:
        result_message = "There was no output of the execution."
        print(result_message)

    return execution.results, execution.logs, result_message, saved_files

def chat(code_interpreter: CodeInterpreter, user_message: str) -> Tuple[List[Result], Logs, str, List[str]]:
    print(f"\n{'='*50}\nUser Message: {user_message}\n{'='*50}")

    message = client.beta.tools.messages.create(
        model=MODEL_NAME,
        system=SYSTEM_PROMPT,
        max_tokens=4096,
        messages=[{"role": "user", "content": user_message}],
        tools=tools,
    )

    print(f"\n{'='*50}\nModel response: {message.content}\n{'='*50}")

    if message.stop_reason == "tool_use":
        tool_use = next(block for block in message.content if block.type == "tool_use")
        tool_name = tool_use.name
        tool_input = tool_use.input

        print(f"\n{'='*50}\nUsing tool: {tool_name}\n{'='*50}")

        if tool_name == "execute_python":
            return code_interpret(code_interpreter, tool_input["code"])
    return [], Logs(), "No code execution requested.", []

def main():
    try:
        while True:
            user_message = input("Enter your message (or 'quit' to exit): ")
            if user_message.lower() == 'quit':
                break

            with CodeInterpreter() as code_interpreter:
                try:
                    code_interpreter_results, code_interpreter_logs, result_message, saved_files = chat(
                        code_interpreter,
                        user_message,
                    )
                except ValueError as e:
                    print(f"Error unpacking results: {e}")
                    continue

                print(code_interpreter_logs)
                print(result_message)

                if saved_files:
                    print("Saved files:")
                    for file in saved_files:
                        print(f"- {file}")
    finally:
        sandbox.close()

if __name__ == "__main__":
    main()
