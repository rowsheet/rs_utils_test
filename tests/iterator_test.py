from rs_utils import runner
from rs_utils import logger
from rs_utils.itterator import Itterator
from rs_utils.response import Response

# Example non rs_step process with args and possible failure.
def POPULATE_FILE_STEP_ONE(**kwargs):
	response = Response()
	try:
		if "filename" not in kwargs:
			raise Exception("Invalid POPULATE_FILE_STEP_ONE call: 'filename' not provided")
		filename = kwargs["filename"]
		import os
		if os.path.exists(filename) == False:
			raise Exception("Invalid POPULATE_FILE_STEP_ONE call: file '" + filename + "' does not exist.")
		with open(filename, "a") as f:
			for i in range(10):
				f.write("Populating line: " + str(i) + "\n")
		response.ERROR = False
		return response
	except Exception as ex:
		response.ERROR = True
		response.ERROR_MSG = str(ex)
		return response

# Example non rs_step process (more complex).
def PROCESS_FILE_STEP_TWO(**kwargs):
	response = Response()
	try:
		if "filename" not in kwargs:
			raise Exception("Invalid PROCESS_FILE_STEP_TWO call: 'filename' not provided")
		filename = kwargs["filename"]
		import os
		if os.path.exists(filename) == False:
			raise Exception("Invalid PROCESS_FILE_STEP_TWO call: file '" + filename + "' does not exist.")
		with open(filename, "r") as f:
			lines = f.readlines()
		import json
		obj = {}
		for i in range(len(lines)):
			obj["line_" + str(i)] = lines[i]
		obj_json = json.dumps(obj)
		with open("FINAL_REPORT.json", "w") as f:
			f.write(obj_json)
		response.ERROR = False
		return response
	except Exception as ex:
		response.ERROR = True
		response.ERROR_MSG = str(ex)
		return response

# Example non rs_step process (print data from FINAL_REPORT.json file).
def PRINT_FINAL_REPORT(**kwargs):
	response = Response()
	try:
		if "filename" not in kwargs:
			raise Exception("Invalid PRINT_FINAL_REPORT call: 'filename' not provided")
		filename = kwargs["filename"]
		import os
		if os.path.exists(filename) == False:
			raise Exception("Invalid PRINT_FINAL_REPORTcall: file '" + filename + "' does not exist.")
		with open(filename, "r") as f:
			raw_data = f.read()
		import json
		data = json.loads(raw_data)
		logger.success("FINAL REPORT:", line=True, line_char="*")
		import pprint as pp
		pp.pprint(data)
		response.ERROR = False
		return response
	except Exception as ex:
		response.ERROR = True
		response.ERROR_MSG = str(ex)
		return response

# Commonly used cleanup procedures.

cleanup_file_step_one_cmd = "rm file_step_one.txt"
cleanup_file_step_one_msg = "Cleaning up, removing file_step_one.txt."

cleanup_file_step_two_cmd = "rm file_step_two.txt && rm file_step_two.txt.json"
cleanup_file_step_two_msg = "Cleaning up, removing file_step_two.txt."

# Create the ittorator.

rsi = Itterator()

# CLEAN_UP_FILE_STEP_ONE.
# 	Create a file called "file_step_one.txt".
rsi.register_process({
	"name": "CLEAN_UP_FILE_STEP_ONE",
	"rs_step_cmd": cleanup_file_step_one_cmd,
	"rs_step_msg": cleanup_file_step_one_msg,
	"next_process": None,
	"stop_on_error": True,
})

# CLEAN_UP_FILE_STEP_TWO.
# 	Create a file called "file_step_one.txt".
rsi.register_process({
	"name": "CLEAN_UP_FILE_STEP_TWO",
	"rs_step_cmd": cleanup_file_step_two_cmd,
	"rs_step_msg": cleanup_file_step_two_msg,
	"next_process": None,
	"stop_on_error": True,
})

# CREATE_FILE_STEP_ONE.
# 	Create a file called "file_step_one.txt".
rsi.register_process({
	"name": "CREATE_FILE_STEP_ONE",
	"rs_step_cmd": "touch file_step_one.txt",
	"rs_step_msg": "Creating file_step_one.txt",
	"rs_step_args": {
		"cmd_log": True,
		"cmd_return": True,
	},
	"start_process": True,
	"next_process": {
		"ECHO_TO_FILE_STEP_ONE": {
			"ERROR": False,
		},
		"CLEAN_UP_FILE_STEP_ONE": {
			"ERROR": True,
		},
	},
	"stop_on_error": True,
})

# ECHO_TO_FILE_STEP_ONE
#	Add 'something' to "file_step_one.txt".
rsi.register_process({
	"name": "ECHO_TO_FILE_STEP_ONE",
	# "rs_step_cmd": "echob 'something' >> file_step_one.txt", # Test using an invalid command.
	"rs_step_cmd": "echo 'something' >> file_step_one.txt",
	"rs_step_msg": "Echoing to file_step_one.txt",
	"next_process": {
		"POPULATE_FILE_STEP_ONE": {
			"ERROR": False,
		},
		"CLEAN_UP_FILE_STEP_ONE": {
			"ERROR": True,
		},
	},
	"stop_on_error": True,
})

# POPULATE_FILE_STEP_ONE 
#	Populate "file_step_one.txt" with a custom function.
rsi.register_process({
	"name": "POPULATE_FILE_STEP_ONE",
	"step": POPULATE_FILE_STEP_ONE,
	"step_args": {
		# "filename": "file_step_ones.txt" # Test using an invalid filename.
		"filename": "file_step_one.txt"
	},
	"next_process": {
		"COPY_FILE_STEP_ONE_TO_STEP_TWO": {
			"ERROR": False,
		},
		"CLEAN_UP_FILE_STEP_ONE": {
			"ERROR": True,
		},
	},
	"stop_on_error": True,
})

# COPY_FILE_STEP_ONE_TO_STEP_TWO 
#	Copy the file "file_step_one.txt" to "file_step_two.txt".
rsi.register_process({
	"name": "COPY_FILE_STEP_ONE_TO_STEP_TWO",
	# "rs_step_cmd": "cp file_step_ones.txt file_step_two.txt", # Test using an invalid filename.
	"rs_step_cmd": "cp file_step_one.txt file_step_two.txt",
	"rs_step_msg": "Copying file_step_one.txt to file_step_two.txt",
	"next_process": {
		"DELETE_FILE_STEP_ONE": {
			"ERROR": False,
		},
		"CLEAN_UP_FILE_STEP_ONE": {
			"ERROR": True,
		},
	},
	"stop_on_error": True,
})

# DELETE_FILE_STEP_ONE.
#	Delete the file "file_step_one.txt".
rsi.register_process({
	"name": "DELETE_FILE_STEP_ONE",
	"rs_step_cmd": "rm file_step_one.txt",
	"rs_step_msg": "Deleting file_step_one.txt",
	"next_process": {
		"PROCESS_FILE_STEP_TWO": {
			"ERROR": False,
		},
		"CLEAN_UP_FILE_STEP_ONE": {
			"ERROR": True,
		},
	},
	"stop_on_error": True,
})

# PROCESS_FILE_STEP_TWO.
#	Delete the file "file_step_one.txt".
rsi.register_process({
	"name": "PROCESS_FILE_STEP_TWO",
	"step": PROCESS_FILE_STEP_TWO,
	"step_args": {
		"filename": "file_step_two.txt"
	},
	# "require_confirmation": True, # Test requiring confirmation to continue.
	"next_process": {
		"DELETE_FILE_STEP_TWO": {
			"ERROR": False,
		},
		"CLEAN_UP_FILE_STEP_TWO": {
			"ERROR": True,
		},
	},
	"stop_on_error": True,
})

# DELETE_FILE_STEP_TWO.
#	Delete the file "file_step_one.txt".
rsi.register_process({
	"name": "DELETE_FILE_STEP_TWO",
	"rs_step_cmd": "rm file_step_two.txt",
	"rs_step_msg": "Deleting file_step_two.txt",
	"next_process": {
		"PRINT_FINAL_REPORT": {
			"ERROR": False,
		},
		"CLEAN_UP_FILE_STEP_TWO": {
			"ERROR": True,
		},
	},
	"stop_on_error": True,
})

# PRINT_FINAL_REPORT.
#	Delete the file "file_step_one.txt".
rsi.register_process({
	"name": "PRINT_FINAL_REPORT",
	"step": PRINT_FINAL_REPORT,
	"step_args": {
		"filename": "FINAL_REPORT.json"
	},
	"next_process": {
		"DELETE_FINAL_REPORT": {
			"ERROR": False,
		},
		"CLEAN_UP_FILE_STEP_TWO": {
			"ERROR": True,
		},
	},
	"stop_on_error": True,
})

# DELETE_FINAL_REPORT.
#	Delete the file "file_step_one.txt".
rsi.register_process({
	"name": "DELETE_FINAL_REPORT",
	"name": "DELETE_FINAL_REPORT",
	"rs_step_cmd": "rm FINAL_REPORT.json",
	"rs_step_msg": "Deleting final report.",
	"require_confirmation": True,
	"stop_on_error": True,
})

# Run the itterator.
rsi.run()
