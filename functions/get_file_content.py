import os
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets and displays a files content in a specified directory relative to the working directory. Output truncated at 10000 charactors.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
		required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Truncated content of file from path to file relative to the working directory",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
	try:
		abs_wdir_path = os.path.abspath(working_directory)
		target_file = os.path.normpath(os.path.join(abs_wdir_path, file_path))
		valid_file_path =  os.path.commonpath([abs_wdir_path,target_file]) == abs_wdir_path

		if not valid_file_path:
			return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
		if not os.path.isfile(target_file):
			return f'Error: File not found or is not a regular file: "{file_path}"'
	

		Max_Char = 10000
		open_file = open(target_file)
		content = open_file.read(Max_Char)

		if open_file.read(1):
			content += f'[...File "{file_path}" truncated at {Max_Char} characters]'
	
		return content

	except Exception as e:
		return f"Error: {e}"
