import os
import subprocess
from google.genai import types



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs file in a specified directory relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,   
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional command-line arguments to pass to the Python file",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        abs_wdir_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_wdir_path, file_path))
        valid_file_path =  os.path.commonpath([abs_wdir_path,target_file]) == abs_wdir_path

        if not valid_file_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args != None:
            command.extend(args)

        complete_process = subprocess.run(
            command,
            cwd=working_directory,
            capture_output=True,
            text=True,
            timeout=30
        )
        output_string = ""
        if complete_process.returncode != 0:
            output_string += f'Process exited with code {complete_process.returncode}'
        if not complete_process.stdout and not complete_process.stderr:
            output_string += f'No output produced'
        if complete_process.stdout:
            output_string += f'STDOUT: {complete_process.stdout}'
        if complete_process.stderr:
            output_string += f'STDERR: {complete_process.stderr}'

        return output_string

    except Exception as e:
        return f"Error: executing Python file: {e}"    