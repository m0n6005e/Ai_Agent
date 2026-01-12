
import os

def get_files_info(working_directory, directory="."):
	try:
		wdir_path = os.path.abspath(working_directory)
		target_directory = os.path.normpath(os.path.join(wdir_path, directory))
		valid_target_directory = os.path.commonpath([wdir_path, target_directory]) == wdir_path
	
		if not valid_target_directory:
			return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
		if not os.path.isdir(target_directory):
			return f'Error: "{directory}" is not a directory'
	

		lines = []
		for name in os.listdir(target_directory):
			full_path = os.path.join(target_directory, name)
			lines.append(f"- {name}: file_size={os.path.getsize(full_path)} bytes, is_dir={os.path.isdir(full_path)}")
		
		return "\n".join(lines)

	except Exception as e:
		return f"Error: {e}"
