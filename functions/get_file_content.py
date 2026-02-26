import os
from google.genai import types

def get_file_content(working_directory, file_path):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            file_content = f.read(10000)
            if f.read(1) != "":
                file_content += f'[...File "{file_path}" truncated at 10000 characters]'
        return file_content
    except OSError as err:
        return f"Error: {err}"

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the contents of a specified file relative to the working directory, truncated to 10000 characters for longer files.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)