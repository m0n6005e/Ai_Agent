def get_files_info(working_directory, directory="."):
	wdir_path = os.path.abspath(working_directory)
	target_directory = os.path.normpath(os.path.join(wdir_path, directory))
	target_directory = os.path.commonpath([woking_directory, target_directory]) == wdir_path
	
	if target_directory == False:
		return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
	if not directory os.path.isdir(directory):
		return f'Error: "{directory}" is not a directory'
	for i in target_directory:
	# work in progress
