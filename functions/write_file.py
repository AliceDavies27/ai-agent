import os
from google.genai import types

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        elif os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs('/'.join(target_file.split('/')[:-1]), exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except OSError as err:
        return f"Error: {err}"
    
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the supplied content to the specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content that should be written to the file."
            )
        },
        required=["file_path", "content"],
    ),
)