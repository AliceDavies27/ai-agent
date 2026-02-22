import os

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        files_str = ""
        for file in os.listdir(target_dir):
            file_path = os.path.join(target_dir, file)
            is_dir = os.path.isdir(file_path)
            file_size = os.path.getsize(file_path)
            files_str += f"- {file}: file_size={file_size} bytes, is_dir={is_dir}\n"
        return files_str[:-1]
    except OSError as err:
        return f"Error: {err}"