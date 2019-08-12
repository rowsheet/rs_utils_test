from rs_utils import rs_runner
from rs_utils import rs_logger 

class _RSIProcess:

	name = None

	rs_step = None
	rs_step_cmd = None
	rs_step_msg = None
	rs_step_args = None

	step = None
	step_args = {} 

	next_process = None

	require_confirmation = False 
	
	cleanup_rs_step = None
	cleanup_rs_step_cmd = None
	cleanup_rs_step_msg = None
	cleanup_rs_step_args = None

	cleanup_step = None
	cleanup_step_args = {} 

	def __init__(self,
		name = None,
		rs_step = None,
		rs_step_cmd = None,
		rs_step_msg = None,
		rs_step_args = {},
		step = None,
		step_args = None,
		next_process = None,
		require_confirmation = None,
		cleanup_rs_step = None,
		cleanup_rs_step_cmd = None,
		cleanup_rs_step_msg = None,
		cleanup_rs_step_args = {},
		cleanup_step = None,
		cleanup_step_args = None,
		):

		# Assign vals to self attributes.
		self.name = name

		self.rs_step = rs_step
		self.rs_step_cmd = rs_step_cmd
		self.rs_step_msg = rs_step_msg
		self.rs_step_args = rs_step_args

		self.step = step
		self.step_args = step_args

		self.next_process = next_process

		self.require_confirmation = require_confirmation 

		self.cleanup_rs_step = cleanup_rs_step
		self.cleanup_rs_step_cmd = cleanup_rs_step_cmd
		self.cleanup_rs_step_msg = cleanup_rs_step_msg
		self.cleanup_rs_step_args = cleanup_rs_step_args

		self.cleanup_step = cleanup_step
		self.cleanup_step_args = cleanup_step_args

	def _run_next_process(self):
		if self.next_process is not None:
			# The "next_process" is assigned as a string on initialization, but if another process
			# with that name is actually added, the type of "next_process" will be _RSIProcess. If
			# it's a string, that means there's no valid next process.
			if type(self.next_process).__name__ == "str":
				raise Exception("Invalid next process. Porcess with name '"
					+ self.next_process + "' was never assigned. Check that you haven't "
					+ "mispelled the process name.")
			if type(self.next_process).__name__ != "_RSIProcess":
				raise Exception("Invalid next process. Process is not of type '_RSIProcess' "
					+ "and probably wan't assigned correctly.")

			self.next_process.run()
		else:
			rs_logger.message("All processes complete.")

	def _handle_cleanup(self):
		if self.cleanup_rs_step is not None:
			response = self.cleanup_rs_step(
				self.cleanup_rs_step_cmd,
				self.cleanup_rs_step_msg,
				**self.cleanup_rs_step_args,
			)
			# Check the response.
			if response["error"] == True:
				rs_logger.success(response["cmd"])
				rs_logger.error_big([
					"Cleanup Step Error:",
					self.name,
					# If you're cleanup step fucked up, you have to do it yourself.
					"Unable to clean up. You'll have to do this yourself."
				])
				# Print the "stderr" if it exists.
				if response["stderr"] is not None:
					rs_logger.error_bold("Last response stderr:")
					rs_logger.error(response["stderr"])
				else:
					rs_logger.error_bold("No stderr from last response:")

	def run(self):
		# Print a big, padded, bold message for each step.
		rs_logger.message_big([
			"Running Itterator Step:",
			self.name,
		])
		# We might get an "rs_step" or just a regular step that's a function.
		if self.rs_step is not None:
			response = self.rs_step(
				self.rs_step_cmd,
				self.rs_step_msg,
				**self.rs_step_args,
			)
			# Check the response.
			if response["error"] == True:
				# Print a big bold error.
				rs_logger.error_big([
					"Itterator Step Error:",
					self.name,
				])
				# Print the "stderr" if it exists.
				if response["stderr"] is not None:
					rs_logger.error_bold("Last response stderr:")
					rs_logger.error(response["stderr"])
				else:
					rs_logger.error_bold("No stderr from last response:")
				# Handle cleanup.
				self._handle_cleanup()
				raise SystemExit
		elif self.step is not None:
			try:
				response = self.step(
					**self.step_args
				)
			except Exception as ex:
				# Print a big bold error.
				rs_logger.error_big([
					"Itterator Step Error:",
					self.name,
				])
				# Print the exception message string.
				rs_logger.error_bold("Last procedure exception:")
				rs_logger.error_bold(str(ex))
				# Handle cleanup.
				self._handle_cleanup()
				raise SystemExit
		# Before running the next step, check if we should get confirmation.
		if self.require_confirmation == True:
			rs_logger.confirm_continue()
		self._run_next_process()

class RS_Itterator:

	processes = {}
	start_process = None

	def __init__(self):
		rs_logger.message("Creating new RS_Itterator...", line=True)	
	
	def register_process(self, process):

		# Make sure the process has a "name".
		if "name" not in process:
			raise Exception("Unable to register process: 'name' must be set.")
		process_name = process["name"]

		# Create the process and egister the process.
		rsi_process = _RSIProcess(
			# specify process name.
			name = process_name,
			# use "rs_step".
			rs_step = process["rs_step"] 
				if "rs_step" in process else None,
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
			cleanup_rs_step = process["cleanup_rs_step"]
				if "cleanup_rs_step" in process else None,
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

	def run(self):
		rs_logger.message("Running itterator...")
		if self.start_process is None:
			rs_logger.error("Error: Could not start itterator with no start_process.")
			return
		self.start_process.run()

# Unit test.
if __name__ == "__main__":

	# Example non rs_step process with args and possible failure.
	def POPULATE_FILE(**kwargs):
		if "filename" not in kwargs:
			raise Exception("Invalid POPULATE_FILE call: 'filename' not provided")
		filename = kwargs["filename"]
		import os
		if os.path.exists(filename) == False:
			raise Exception("Invalid POPULATE_FILE call: file '" + filename + "' does not exist.")
		with open(filename, "a") as f:
			for i in range(10):
				f.write("Populating line: " + str(i) + "\n")
		return 0

	# Commonly used cleanup procedures.
	cleanup_testfile_cmd = "rm testfile.txt"
	cleanup_testfile_msg = "Cleaning up, removing textfile.txt"

	rsi = RS_Itterator()

	# CREATE_FILE.
	# 	Create a file called "textfile.txt".
	rsi.register_process({
		"name": "CREATE_FILE",
		"rs_step": rs_runner.step,
		"rs_step_cmd": "touch testfile.txt",
		"rs_step_msg": "Creating testfile.txt",
		"rs_step_args": {
			"cmd_log": True,
			"cmd_return": True,
		},
		"start_process": True,
		"next_process": "ECHO_TO_FILE",
	})

	# ECHO_TO_FILE
	#	Add 'something' to "testfile.txt".
	rsi.register_process({
		"name": "ECHO_TO_FILE",
		"rs_step": rs_runner.step,
		# "rs_step_cmd": "echob 'something' >> testfile.txt", # Test using an invalid command.
		"rs_step_cmd": "echo 'something' >> testfile.txt",
		"rs_step_msg": "Echoing to testfile.txt",
		"next_process": "POPULATE_FILE",
		# Cleanup by removing the file.
		"cleanup_rs_step": rs_runner.step,
		"cleanup_rs_step_cmd": cleanup_testfile_cmd,
		"cleanup_rs_step_msg": cleanup_testfile_msg,
	})

	# POPULATE_FILE 
	#	Populate "textfile.txt" with a custom function.
	rsi.register_process({
		"name": "POPULATE_FILE",
		"step": POPULATE_FILE,
		"step_args": {
			# "filename": "testfiles.txt" # Test using an invalid filename.
			"filename": "testfile.txt"
		},
		"next_process": "COPY_FILE",
		"cleanup_rs_step": rs_runner.step,
		"cleanup_rs_step_cmd": cleanup_testfile_cmd,
		"cleanup_rs_step_msg": cleanup_testfile_msg,
	})

	# COPY_FILE 
	#	Copy the file "textfile.txt" to "other.txt".
	rsi.register_process({
		"name": "COPY_FILE",
		"rs_step": rs_runner.step,
		# "rs_step_cmd": "cp testfiles.txt other.txt", # Test using an invalid filename.
		"rs_step_cmd": "cp testfile.txt other.txt",
		"rs_step_msg": "Copying testfile.txt to other.txt",
		"next_process": "DELETE_FILE",
		"cleanup_rs_step": rs_runner.step,
		"cleanup_rs_step_cmd": cleanup_testfile_cmd,
		"cleanup_rs_step_msg": cleanup_testfile_msg,
	})

	# DELETE_FILE.
	#	Delete the file "other.txt".
	rsi.register_process({
		"name": "DELETE_FILE",
		"rs_step": rs_runner.step,
		"rs_step_cmd": "rm testfile.txt",
		"rs_step_msg": "Deleting testfile.txt",
	})

	# Run the itterator.
	rsi.run()
