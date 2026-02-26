import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if target_file.split('.')[-1] != "py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args:
            command.extend(args)

        completed_process = subprocess.run(command, cwd=working_dir_abs, capture_output=True, timeout=30, text=True)
        output_string = ""
        if completed_process.returncode != 0:
            output_string += f"Process exited with code {completed_process.returncode}\n"
        if completed_process.stdout == "" and completed_process.stderr == "":
            output_string += f"No output produced\n"
        else:
            if completed_process.stdout != "":
                output_string += f"STDOUT: {completed_process.stdout}\n"
            if completed_process.stderr != "":
                output_string += f"STDERR: {completed_process.stderr}\n"
        return output_string
    except Exception as err:
        return f"Error: executing Python file: {err}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the code in the specified python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the python file, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional arguments to pass to the python script."
            )
        },
        required=["file_path"],
    ),
)