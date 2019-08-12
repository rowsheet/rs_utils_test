from rs_utils import runner
from rs_utils import logger 
from rs_utils.response import Response

class _RSIProcess:

	name = None
	rs_step = runner.step

	rs_step_cmd = None
	rs_step_msg = None
	rs_step_args = None

	step = None
	step_args = {} 

	next_process = None

	require_confirmation = False 

	stop_on_error = True


	def __init__(self,
		name = None,
		rs_step_cmd = None,
		rs_step_msg = None,
		rs_step_args = {},
		step = None,
		step_args = None,
		next_process = None,
		require_confirmation = None,
		stop_on_error = True,
		):

		# Assign vals to self attributes.
		self.name = name

		self.rs_step_cmd = rs_step_cmd
		self.rs_step_msg = rs_step_msg
		self.rs_step_args = rs_step_args

		self.step = step
		self.step_args = step_args

		self.next_process = next_process

		self.require_confirmation = require_confirmation 

		self.stop_on_error = stop_on_error

	def run(self):
		# Print a big, padded, bold message for each step.
		logger.message_big([
			"Running Itterator Step:",
			self.name,
		])
		# Before running the step, check if we should get confirmation.
		if self.require_confirmation == True:
			logger.confirm_continue()
		# We might get an "rs_step" or just a regular step that's a function.
		# We'll checkfor the rs_step_cmd.
		response = None
		if self.rs_step_cmd is not None:
			response = runner.step(
				self.rs_step_cmd,
				self.rs_step_msg,
				**self.rs_step_args,
			)
			# Check the response.
			if response.ERROR == True:
				# Print a big bold error.
				logger.error_big([
					"Itterator Step Error:",
					self.name,
				])
				# Print the "stderr" if it exists.
				if response.STDERR is not None:
					logger.error_bold("Last response stderr:")
					logger.error(response.STDERR)
				else:
					logger.error_bold("No stderr from last response:")
				"""
				if self.stop_on_error == True:
					raise SystemExit
				"""
		elif self.step is not None:
			try:
				response = self.step(
					**self.step_args
				)
			except Exception as ex:
				# Print a big bold error.
				logger.error_big([
					"Itterator Step Error:",
					self.name,
				])
				# Print the exception message string.
				logger.error_bold("Last procedure exception:")
				logger.error_bold(str(ex))
		return {
			"next_process": self.next_process,
			"response": response
		}

class Itterator:

	processes = {}
	start_process = None

	# Save all process names for pre-flight checks.
	all_process_names = []

	# Target processes and response.
	target_process = None
	target_process_responses = {}

	def __init__(self):
		logger.message_big([
			"Starting new Itterator..."
		])
	
	def register_process(self, process):

		# Make sure the process has a "name".
		if "name" not in process:
			raise Exception("Unable to register process: 'name' must be set.")
		process_name = process["name"]

		# Save all process names for pre-flight checks.
		self.all_process_names.append(process_name)

		# Create the process and egister the process.
		rsi_process = _RSIProcess(
			# specify process name.
			name = process_name,
			# use "rs_step".
			rs_step_cmd = process["rs_step_cmd"]
				if "rs_step_cmd" in process else None,
			rs_step_msg = process["rs_step_msg"]
				if "rs_step_msg" in process else None,
			rs_step_args = process["rs_step_args"]
				if "rs_step_args" in process else {},
			# use normal "step".
			step = process["step"]
				if "step" in process else None,
			step_args = process["step_args"]
				if "step_args" in process else None,
			# specify next process.
			next_process = process["next_process"] 
				if "next_process" in process else None,
			# specify confirmation requirment.
			require_confirmation = process["require_confirmation"]
				if "require_confirmation" in process else None,
			# specify stop_on_error option.
			stop_on_error = process["stop_on_error"]
				if "stop_on_error" in process else None,
		)

		# Check if the process is the "start_process".
		if "start_process" in process and process["start_process"] == True:
			self.start_process = rsi_process

		# Check if the process has the "name" that is the "next_process" of any previously registered
		# process.
		self._register_next_process(rsi_process)

		self.processes[process_name] = rsi_process

	# Check if the process has the "name" that is the "next_process" of any previously registered
	# process.
	def _register_next_process(self, rsi_process):
		for process_name, process in self.processes.items():
			if rsi_process.name == process.next_process:
				process.next_process = rsi_process

	def _run_pre_flight_checks(self):
		logger.message("Running pre-flight checks...", line=True)
		# Go through each process and make sure that it's "next_process" exists in all_process_names.
		for process_name, process in self.processes.items():
			if process.next_process is None:
				continue
			for next_process_name, conditions in process.next_process.items():
				if next_process_name not in self.processes:
					raise Exception("Invalid next process. Porcess with name '"
						+ process.next_process + "' was never assigned. "
						+ "Check that you haven't mispelled the process name.")

	def run(self):
		try:
			self._run_pre_flight_checks()
		except Exception as ex:
			logger.error_big([
				"Invalid itterator step configuration:",
				str(ex)
			])
			raise SystemExit

		logger.message("Running itterator...", line=True)
		if self.start_process is None:
			logger.error("Error: Could not start itterator with no start_process.")
			return

		self.target_process = self.start_process

		while True:
			# Get the process run result. It has:
			#	1) response
			#	2) next_process
			process_result = self.target_process.run()

			# Log the target_process response keyed by the process name.
			target_process_response = process_result["response"]
			self.target_process_responses[self.target_process.name] = target_process_response

			# Get conditions from next_process
			next_process = process_result["next_process"]

			# If the next process is none, we're done.
			if next_process is None:
				logger.message("All processes complete.")
				return False
			for process_name, conditions in next_process.items():
				false_condition = False
				for condition, value in conditions.items():
					if target_process_response.__dict__[condition] != value:
						false_condition = True
				if false_condition == False:
					self.target_process = self.processes[process_name]

# Unit test.
if __name__ == "__main__":

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
