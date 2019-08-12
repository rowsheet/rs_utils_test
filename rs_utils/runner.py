from rs_utils import logger
from rs_utils.response import Response 
from subprocess import PIPE, Popen

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
	"""
	if "template_vars" in kwargs:
		for template_var in kwargs:
			cmd
	"""
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
		#	success => False 
		response.ERROR = True
		response.SUCCESS = False
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
		#	success => True 
		response.ERROR = False
		response.SUCCESS = True
	return response

# Unit test.
if __name__ == "__main__":
	# All unit tests.
	tests = {
		# Test creating a file.
		"touch": {
			"actual": step(
				"touch test.txt",
				"Creating test file...",
			),
			"should": {
				"cmd": "touch test.txt",
				"msg": "Creating test file...",
				"stderr": None,
				"stdout": "",
				"success": True,
				"error": False
			}
		},
		# Test listing containers.
		"docker_ps": {
			"actual": step(
				"docker ps",
				"Listing running containers...",
			),
			"should": {
				"cmd": "",
				"msg": "",
				"stderr": None,
				"stdout": "",
				"success": True,
				"error": False
			}
		},
		# Test listing containers without "command" logging or return.
		"docker_ps_NO_CMD": {
			"actual": step(
				"docker ps",
				"Listing running containers... NO CMD",
				cmd_log = False,
				cmd_return = False,
			),
			"should": {
				"cmd": None, # Ensure "cmd" is None.
				"msg": "",
				"stderr": None,
				"stdout": "",
				"success": True,
				"error": False
			}
		},
		# Test listing containers without "stdout" logging or return.
		"docker_ps_NO_STDOUT": {
			"actual": step(
				"docker ps",
				"Listing running containers... NO STDOUT",
				stdout_log = False,
				stdout_return = False,
			),
			"should": {
				"cmd": "", 
				"msg": "",
				"stderr": None,
				"stdout": None, # Ensure "stdout" is None.
				"success": True,
				"error": False
			}
		},
		# Test removing a container that doesn't exist.
		"docker_rm_error": {
			"actual": step(
				"docker rm containerthatdoesntexist",
				"Listing running containers...",
			),
			"should": {
				"cmd": "", 
				"msg": "",
				"stderr": "", # Ensure "stderror" is not None.
				"stdout": None,
				"success": False,
				"error": True 
			}
		},
		# Test removing a container that doesn't exist without 
		# "stderr" logging or return.
		"docker_rm_error_NO_STDERR": {
			"actual": step(
				"docker rm containerthatdoesntexist",
				"Listing running containers... NO STDERR",
				stderr_log = False,
				stderr_return = False,
			),
			"should": {
				"cmd": "", 
				"msg": "",
				"stderr": None, # Ensure "stderror" is None.
				"stdout": None,
				"success": False,
				"error": True 
			}
		},
	}

	# Indicate Unit Tests output restults.
	print("\n")
	logger.message("----------------------------------TEST RESULTS:---------------------------------")
	print("\n")

	for test_key, test in tests.items():
		#---------------------------------------------------------------
		# Check response "cmd"
		#---------------------------------------------------------------
		# If "should" is None, make sure "actual" is None.
		if test["should"]["cmd"] is None:
			if test["actual"].CMD is not None:
				logger.error(test_key + ": TEST FAILED")
				continue
		# If "should" is not None, make sure "actual" is not None.
		else:
			if test["actual"].CMD is None:
				logger.error(test_key + ": TEST FAILED")
				continue

		#---------------------------------------------------------------
		# Check response "msg"
		#---------------------------------------------------------------
		# If "should" is None, make sure "actual" is None.
		if test["should"]["msg"] is None:
			if test["actual"].MSG is not None:
				logger.error(test_key + ": TEST FAILED")
				continue
		# If "should" is not None, make sure "actual" is not None.
		else:
			if test["actual"].MSG is None:
				logger.error(test_key + ": TEST FAILED")
				continue

		#---------------------------------------------------------------
		# Check response "stdout"
		#---------------------------------------------------------------
		# If "should" is None, make sure "actual" is None.
		if test["should"]["stdout"] is None:
			if test["actual"].STDOUT is not None:
				logger.error(test_key + ": TEST FAILED")
				continue
		# If "should" is not None, make sure "actual" is not None.
		else:
			if test["actual"].STDOUT is None:
				logger.error(test_key + ": TEST FAILED")
				continue

		#---------------------------------------------------------------
		# Check response "stderr"
		#---------------------------------------------------------------
		# If "should" is None, make sure "actual" is None.
		if test["should"]["stderr"] is None:
			if test["actual"].STDERR is not None:
				logger.error(test_key + ": TEST FAILED")
				continue
		# If "should" is not None, make sure "actual" is not None.
		else:
			if test["actual"].STDERR is None:
				logger.error(test_key + ": TEST FAILED")
				continue

		#---------------------------------------------------------------
		# Check response "success" and "error".
		#---------------------------------------------------------------
		if test["actual"].ERROR != test["should"]["error"]:
			logger.error(test_key + ": TEST FAILED")
			continue
		if test["actual"].SUCCESS != test["should"]["success"]:
			logger.error(test_key + ": TEST FAILED")
			continue

		#---------------------------------------------------------------
		# TEST PASSED if it got to here.
		#---------------------------------------------------------------
		logger.success(test_key + ": TEST PASSED")
