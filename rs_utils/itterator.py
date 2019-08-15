from rs_utils import runner
from rs_utils import logger 
from rs_utils.response import Response

class _RSIProcess:

	name = None
	rs_step = runner.step

	rs_step_cmd = None
	rs_step_msg = None
	rs_step_args = {} 

	step = None
	step_args = {} 

	next_process = None

	require_confirmation = False 


	def __init__(self,
		name = None,
		rs_step_cmd = None,
		rs_step_msg = None,
		rs_step_args = {},
		step = None,
		step_args = {},
		next_process = None,
		require_confirmation = False,
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
				response.ERROR = True
				response.ERROR_MSG = str(ex)

		# Make sure the step registered returns a response.
		# If it doesn't, that's a problem worth an actual ERROR
		if type(response).__name__ != "Response":
			response = Response()
			response.ERROR = True
			err_msg = (
				"""Iterator error. Step return '%s' type object."""
				"""Exepected rsutls.response.Response object.""" % (
					type(response).__name__
				)
			)
			logger.error_big(err_msg)
			response.ERROR_MSG = (err_msg)

		return {
			"next_process": self.next_process,
			"response": response,
		}

class Itterator:

	processes = {}
	start_process = None

	# Save all process names for pre-flight checks.
	all_process_names = []

	# Target processes and response.
	target_process = None
	process_responses = {}

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
				if "step_args" in process else {},
			# specify next process.
			next_process = process["next_process"] 
				if "next_process" in process else None,
			# specify confirmation requirment.
			require_confirmation = process["require_confirmation"]
				if "require_confirmation" in process else None,
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
		response = Response()
		try:
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
				err_msg = "Error: Could not start itterator: No start_process specified."
				raise Exception(err_msg)

			self.target_process = self.start_process

			while True:
				# Get the process run result. It has:
				#	1) response
				#	2) next_process
				process_result = self.target_process.run()

				# Log the target_process response keyed by the process name.
				target_process_response = process_result["response"]
				self.process_responses[self.target_process.name] = target_process_response

				# Get conditions from next_process
				next_process = process_result["next_process"]

				# If the next process is none, we're done.
				if next_process is None:
					done = "All processes complete."
					logger.message(done, line=True)
					# Set the DATA to be all process_responses.
					# target_process_response.DATA = self.process_responses
					return target_process_response

				# Find the next process with matching conditions.
				for process_name, conditions in next_process.items():
					false_condition = False
					for condition, value in conditions.items():
						if target_process_response.__dict__[condition] != value:
							false_condition = True
					if false_condition == False:
						self.target_process = self.processes[process_name]

				# Populate the target_process template_values at runtime.
				if self.target_process.rs_step_args is not None:
					rs_step_args = self.target_process.rs_step_args
					if "template_vars" in rs_step_args:
						template_vars = rs_step_args["template_vars"]
						for template_var_name, template_var_info in template_vars.items():
							from_step = template_var_info["from_step"]
							step_process = self.process_responses[from_step]
							data_key = template_var_info["data_key"]
							value = step_process.DATA[data_key]
							self.target_process.rs_step_args["template_vars"][template_var_name]["value"] = value
		except Exception as ex:
			logger.error(str(ex))
			response.ERROR = True
			response.ERROR_MSG = str(ex)
			return response

#-------------------------------------------------------------------------------
# Unit tests.
#-------------------------------------------------------------------------------
if __name__ == "__main__":
	import os
	install_error = os.system("cd .. && sudo sh install.sh")
	if install_error:
		print("ERROR re-installing rs_utils.")
	else:
		os.system("python3 ../tests/itterator.py")
