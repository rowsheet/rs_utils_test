from rs_utils import runner
from rs_utils import logger 

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
	
	cleanup_rs_step_cmd = None
	cleanup_rs_step_msg = None
	cleanup_rs_step_args = None

	cleanup_step = None
	cleanup_step_args = {}

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
		cleanup_rs_step_cmd = None,
		cleanup_rs_step_msg = None,
		cleanup_rs_step_args = {},
		cleanup_step = None,
		cleanup_step_args = None,
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

		self.cleanup_rs_step_cmd = cleanup_rs_step_cmd
		self.cleanup_rs_step_msg = cleanup_rs_step_msg
		self.cleanup_rs_step_args = cleanup_rs_step_args

		self.cleanup_step = cleanup_step
		self.cleanup_step_args = cleanup_step_args

		self.stop_on_error = stop_on_error

	def _run_next_process(self):
		if self.next_process is not None:
			self.next_process.run()
		else:
			logger.message("All processes complete.")

	def _handle_cleanup(self):
		if self.cleanup_rs_step_cmd is not None:
			response = runner.step(
				self.cleanup_rs_step_cmd,
				self.cleanup_rs_step_msg,
				**self.cleanup_rs_step_args,
			)
			# Check the response.
			if response["error"] == True:
				logger.success(response["cmd"])
				logger.error_big([
					"Cleanup Step Error:",
					self.name,
					# If you're cleanup step fucked up, you have to do it yourself.
					"Unable to clean up. You'll have to do this yourself."
				])
				# Print the "stderr" if it exists.
				if response["stderr"] is not None:
					logger.error_bold("Last response stderr:")
					logger.error(response["stderr"])
				else:
					logger.error_bold("No stderr from last response:")
		elif self.cleanup_step is not None:
			try:
				response = self.cleanup_step(
					**self.step_args
				)
			except Exception as ex:
				# Print a big bold error.
				logger.error_big([
					"Cleanup Step Error:",
					self.name,
					# If you're cleanup step fucked up, you have to do it yourself.
					"Unable to clean up. You'll have to do this yourself."
				])
				# Print the exception message string.
				logger.error_bold("Last procedure exception:")
				logger.error_bold(str(ex))

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
		if self.rs_step_cmd is not None:
			response = runner.step(
				self.rs_step_cmd,
				self.rs_step_msg,
				**self.rs_step_args,
			)
			# Check the response.
			if response["error"] == True:
				# Print a big bold error.
				logger.error_big([
					"Itterator Step Error:",
					self.name,
				])
				# Print the "stderr" if it exists.
				if response["stderr"] is not None:
					logger.error_bold("Last response stderr:")
					logger.error(response["stderr"])
				else:
					logger.error_bold("No stderr from last response:")
				# Handle cleanup.
				self._handle_cleanup()
				# Exit after cleanup if "stop_on_error" is set.
				if self.stop_on_error == True:
					raise SystemExit
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
				# Handle cleanup.
				self._handle_cleanup()
				# Exit after cleanup if "stop_on_error" is set.
				if self.stop_on_error == True:
					raise SystemExit
		self._run_next_process()

class Itterator:

	processes = {}
	start_process = None

	# Save all process names for pre-flight checks.
	all_process_names = []

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
			# use "rs_step" for cleanup on failure.
			cleanup_rs_step_cmd = process["cleanup_rs_step_cmd"]
				if "cleanup_rs_step_cmd" in process else None,
			cleanup_rs_step_msg = process["cleanup_rs_step_msg"]
				if "cleanup_rs_step_msg" in process else None,
			cleanup_rs_step_args = process["cleanup_rs_step_args"]
				if "cleanup_rs_step_args" in process else {},
			# use normal "step" for cleanup on failure.
			cleanup_step = process["cleanup_step"]
				if "cleanup_step" in process else None,
			cleanup_step_args = process["cleanup_step_args"]
				if "cleanup_step_args" in process else None,
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
			# The "next_process" is assigned as a string on initialization, but if another process
			# with that name is actually added, the type of "next_process" will be _RSIProcess. If
			# it's a string, that means there's no valid next process. If it's none, it means it's
			# a stop process.
			if type(process.next_process).__name__ == "NoneType":
				continue
			if type(process.next_process).__name__ == "str":
				raise Exception("Invalid next process. Porcess with name '"
					+ process.next_process + "' was never assigned. Check that you haven't "
					+ "mispelled the process name.")
			if type(process.next_process).__name__ != "_RSIProcess":
				raise Exception("Invalid next process. Process is not of type '_RSIProcess' "
					+ "and probably wan't assigned correctly.")

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
		self.start_process.run()

# Unit test.
if __name__ == "__main__":

	# Example non rs_step process with args and possible failure.
	def POPULATE_FILE_STEP_ONE(**kwargs):
		if "filename" not in kwargs:
			raise Exception("Invalid POPULATE_FILE_STEP_ONE call: 'filename' not provided")
		filename = kwargs["filename"]
		import os
		if os.path.exists(filename) == False:
			raise Exception("Invalid POPULATE_FILE_STEP_ONE call: file '" + filename + "' does not exist.")
		with open(filename, "a") as f:
			for i in range(10):
				f.write("Populating line: " + str(i) + "\n")
		return 0

	# Example non rs_step process (more complex).
	def PROCESS_FILE_STEP_TWO(**kwargs):
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
		return 0

	# Example non rs_step process (print data from FINAL_REPORT.json file).
	def PRINT_FINAL_REPORT(**kwargs):
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

	# Commonly used cleanup procedures.

	cleanup_file_step_one_cmd = "rm file_step_one.txt"
	cleanup_file_step_one_msg = "Cleaning up, removing file_step_one.txt."

	cleanup_file_step_two_cmd = "rm file_step_two.txt && rm file_step_two.txt.json"
	cleanup_file_step_two_msg = "Cleaning up, removing file_step_two.txt."

	# Create the ittorator.

	rsi = Itterator()

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
		"next_process": "ECHO_TO_FILE_STEP_ONE",
		"stop_on_error": True,
	})

	# ECHO_TO_FILE_STEP_ONE
	#	Add 'something' to "file_step_one.txt".
	rsi.register_process({
		"name": "ECHO_TO_FILE_STEP_ONE",
		# "rs_step_cmd": "echob 'something' >> file_step_one.txt", # Test using an invalid command.
		"rs_step_cmd": "echo 'something' >> file_step_one.txt",
		"rs_step_msg": "Echoing to file_step_one.txt",
		"next_process": "POPULATE_FILE_STEP_ONE",
		# Cleanup by removing the file.
		"cleanup_rs_step_cmd": cleanup_file_step_one_cmd,
		"cleanup_rs_step_msg": cleanup_file_step_one_msg,
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
		"next_process": "COPY_FILE_STEP_ONE_TO_STEP_TWO",
		"cleanup_rs_step_cmd": cleanup_file_step_one_cmd,
		"cleanup_rs_step_msg": cleanup_file_step_one_msg,
		"stop_on_error": True,
	})

	# COPY_FILE_STEP_ONE_TO_STEP_TWO 
	#	Copy the file "file_step_one.txt" to "file_step_two.txt".
	rsi.register_process({
		"name": "COPY_FILE_STEP_ONE_TO_STEP_TWO",
		# "rs_step_cmd": "cp file_step_ones.txt file_step_two.txt", # Test using an invalid filename.
		"rs_step_cmd": "cp file_step_one.txt file_step_two.txt",
		"rs_step_msg": "Copying file_step_one.txt to file_step_two.txt",
		"next_process": "DELETE_FILE_STEP_ONE",
		"cleanup_rs_step_cmd": cleanup_file_step_one_cmd,
		"cleanup_rs_step_msg": cleanup_file_step_one_msg,
		"stop_on_error": True,
	})

	# DELETE_FILE_STEP_ONE.
	#	Delete the file "file_step_one.txt".
	rsi.register_process({
		"name": "DELETE_FILE_STEP_ONE",
		"rs_step_cmd": "rm file_step_one.txt",
		"rs_step_msg": "Deleting file_step_one.txt",
		"next_process": "PROCESS_FILE_STEP_TWO",
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
		"cleanup_rs_step_cmd": cleanup_file_step_two_cmd,
		"cleanup_rs_step_msg": cleanup_file_step_two_msg,
		# "require_confirmation": True, # Test requiring confirmation to continue.
		"next_process": "DELETE_FILE_STEP_TWO",
		"stop_on_error": True,
	})

	# DELETE_FILE_STEP_TWO.
	#	Delete the file "file_step_one.txt".
	rsi.register_process({
		"name": "DELETE_FILE_STEP_TWO",
		"rs_step_cmd": "rm file_step_two.txt",
		"rs_step_msg": "Deleting file_step_two.txt",
		"next_process": "PRINT_FINAL_REPORT",
	})

	# PRINT_FINAL_REPORT.
	#	Delete the file "file_step_one.txt".
	rsi.register_process({
		"name": "PRINT_FINAL_REPORT",
		"step": PRINT_FINAL_REPORT,
		"step_args": {
			"filename": "FINAL_REPORT.json"
		},
		# "next_process": "_DELETE_FINAL_REPORT", # Test with invalid next process.
		"next_process": "DELETE_FINAL_REPORT",
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
