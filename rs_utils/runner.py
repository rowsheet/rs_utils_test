from rs_utils import logger
from rs_utils.response import Response 
from subprocess import PIPE, Popen
from multiprocessing import Pool

def step(cmd, msg=None, **kwargs):
	#-----------------------------------------------------------------------
	# Check for kwargs options.
	#-----------------------------------------------------------------------

	# Default logging set to True.
	cmd_log = True # Log the command with logger.debug colored printing.
	msg_log = True # Log the message with logger.message colored printing.
	stderr_log = True # Log the stderr with logger.error colored printing.
	stdout_log = True # Log the stdout with normal printing.

	# Default response set to True.
	cmd_return = True # Return the command ran in the "cmd" of the response.
	msg_return = True # Return the command ran in the "msg" of the response.
	stderr_return = True # Return the stderr in the "stderr" of the response.
	stdout_return = True # Return the stdout in the "stdout" of the response.

	# Check for response options. Make sure the values are there to avoid
	# key errors. Also affermitivly check for False in case other stupid
	# shit like strings are passed in; we're only checking for bools.
	if "cmd_log" in kwargs:
		if kwargs["cmd_log"] == False:
			cmd_log = False
	if "msg_log" in kwargs:
		if kwargs["msg_log"] == False:
			msg_log = False
	if "stderr_log" in kwargs:
		if kwargs["stderr_log"] == False:
			stderr_log = False
	if "stdout_log" in kwargs:
		if kwargs["stdout_log"] == False:
			stdout_log = False

	if "cmd_return" in kwargs:
		if kwargs["cmd_return"] == False:
			cmd_return = False
	if "msg_return" in kwargs:
		if kwargs["msg_return"] == False:
			msg_return = False
	if "stderr_return" in kwargs:
		if kwargs["stderr_return"] == False:
			stderr_return = False
	if "stdout_return" in kwargs:
		if kwargs["stdout_return"] == False:
			stdout_return = False
	#-----------------------------------------------------------------------
	# Replace the "cmd" template vars with all template vars passed in
	# through kwarges.
	#-----------------------------------------------------------------------
	if "template_vars" in kwargs:
		for template_var_name, template_var_info  in kwargs["template_vars"].items():
			cmd = cmd.replace(
				"<%" + template_var_name + "%>",
				str(template_var_info["value"])
			) 
	#-----------------------------------------------------------------------
	# Save the response and command so we can return it in case we want to
	# use it for something else.
	#-----------------------------------------------------------------------
	response = Response()
	# Set the response for the command and message depending on options.
	if cmd_return == True:
		response.CMD = cmd
	if msg_return == True:
		response.MSG = msg
	#-----------------------------------------------------------------------
	# Print the message with logger.message  if it exists and options
	# are set to true.
	#-----------------------------------------------------------------------
	if msg is not None:
		if msg_log == True:
			logger.message(msg)
	#-----------------------------------------------------------------------
	# Print the command with logger.debug if options are set to true.
	#-----------------------------------------------------------------------
	if cmd_log == True:
		logger.debug(cmd)

	#-----------------------------------------------------------------------
	# Run the command.
	#-----------------------------------------------------------------------
	process = Popen(
		cmd,
		shell=True,
		stdout=PIPE, # Pipe stdout so we can read it.
		stderr=PIPE # Pipe stderr so we can read it.
	)
	stdout, stderr = process.communicate()
	# Check the returncode. If it's not zero, stderr should exist so
	# show the message in red.
	if process.returncode != 0:
		# Decode UTF-8 so newlines and tabs show correctly.
		utf8_err = stderr.decode('UTF-8')
		# Log the stderr in red with logger.error if options are set
		# to true.
		if stderr_log == True:
			logger.error(utf8_err)
		# Set the stderr response if options are set to true.
		if stderr_return == True:
			response.STDERR = utf8_err
		# You must set the returned response status, in this case with
		#	error => True
		response.ERROR = True
	# If it's okay, just print the output like normal.
	else:

		# Decode UTF-8 so newlines and tabs show correctly.
		utf8_out = stdout.decode('UTF-8')
		# Log the stdout in red with normal printing if options are set
		# to true.
		if stdout_log == True:
			print(utf8_out)
		# Set the stdout response if options are set to true.
		if stdout_return == True:
			response.STDOUT = utf8_out
		# You must set the returned response status, in this case with
		#	error => False 
		response.ERROR = False
	return response

def _validate_timeout_step_response(name, response):
        if type(response).__name__ != "Response":
                raise Exception(
                        (
                                """%s returned a non Response type object """ +
                                """of type '%s'"""
                        ) % (
                                name,
                                type(response).__name__
                        )
                )

def timeout_step(
	PRIMARY_PROCESS=None,
	TIMEOUT_PROCESS=None,
	PRIMARY_PROCESS_ARGS={},
	TIMEOUT_PROCESS_ARGS={},
	PRIMARY_PROCESS_TIMEOUT=30,
	TIMEOUT_PROCESS_TIMEOUT=60):

	response = Response()
	try:

		"""-------------------------------------------------------------
		Validate args.
		Make sure PRIMARY_PROCESS and TIMEOUT_PROCESS are defined and
		are either methods of functions.
		-------------------------------------------------------------"""
		errors = []
		if PRIMARY_PROCESS is None:
			errors.append("PRIMARY_PROCESS must be a function.")
		if (
			(type(PRIMARY_PROCESS).__name__ != "function") and
			(type(PRIMARY_PROCESS).__name__ != "method")):
			errors.append("PRIMARY_PROCESS must be a function.")
		if TIMEOUT_PROCESS is None:
			errors.append("TIMEOUT_PROCESS must be a function.")
		if (
			(type(TIMEOUT_PROCESS).__name__ != "function") and
			(type(TIMEOUT_PROCESS).__name__ != "method")):
			errors.append("TIMEOUT_PROCESSmust be a function.")
		if len(errors) > 0:
			raise Exception(
				"Invalid timeout_step usage: " +
				". ".join(errors)
			)
		"""-------------------------------------------------------------
		Set a pool of async functions of size 2 for both:
			1) PRIMARY_PROCESS
			2) TIMEOUT_PROCESS
		Try to run the primary process and return the response, until
		the timeout. If the primary timeout occurs, do the same with
		the timeout process.
		Make sure response are rs_utils.response.Response() objects.
		-------------------------------------------------------------"""
		with Pool(processes=2) as pool:
			primary_process = pool.apply_async(
				PRIMARY_PROCESS,
				kwds=PRIMARY_PROCESS_ARGS,
			)
			try:
				primary_response = primary_process.get(
					timeout=PRIMARY_PROCESS_TIMEOUT
				)
				_validate_timeout_step_response(
					"PRIMARY_PROCESS",
					primary_response,
				)
				return primary_response
			except Exception as ex:
				logger.error("TIMEOUT:")
				logger.error(str(ex))
				"""---------------------------------------------
				If it's a timeout exception, the str(ex) == "",
				otherwise it's another underlying exception that
				needs to be bubbled up.
				---------------------------------------------"""
				if str(ex) == "":
					timeout_process = pool.apply_async(
						TIMEOUT_PROCESS,
						kwds=TIMEOUT_PROCESS_ARGS,
					)
					timeout_response = timeout_process.get(
						timeout=TIMEOUT_PROCESS_TIMEOUT
					)
					_validate_timeout_step_response(
						"TIMEOUT_RESPONSE",
						timeout_response,
					)
					return timeout_response
				else:
					raise Exception(str(ex))
	except Exception as ex:
		response.ERROR = True
		response.STDERR = str(ex)
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
		os.system("python3 ../tests/runner.py")
