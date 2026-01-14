import os

def write_file(working_directory, file_path, content):
    try:
        abs_wdir_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_wdir_path, file_path))
        print(repr(target_file))
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