import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="writes content to file in a specified directory relative to the working directory. Output truncated at 10000 charactors.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
		required=["file_path", "content"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Truncated content of file from path to file relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content being read by function",
            )
        },
    ),
)




def write_file(working_directory, file_path, content):
    try:
        abs_wdir_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_wdir_path, file_path))
        valid_file_path =  os.path.commonpath([abs_wdir_path,target_file]) == abs_wdir_path

        if not valid_file_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
	
        path_dir = os.path.dirname(target_file)
        os.makedirs(path_dir, exist_ok=True)
        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}"({len(content)} characters written)'
    
    
    except Exception as e:
        return f"Error: {e}"