import rs_logger
import subprocess

def step(cmd, msg=None, **kwargs):
	#-----------------------------------------------------------------------
	# Check for kwargs options.
	#-----------------------------------------------------------------------

	# Default logging set to True.
	cmd_log = True # Log the command with rs_logger.debug colored printing.
	msg_log = True # Log the message with rs_logger.message colored printing.
	stderr_log = True # Log the stderr with rs_logger.error colored printing.
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
	# Save the response and command so we can return it in case we want to
	# use it for something else.
	#-----------------------------------------------------------------------
	response = {
		# Returning cmd, msg, stdout, stderr are optional.
		"cmd": None,
		"msg": None,
		"stdout": None,
		"stderr": None,
		# You must return either success or failure.
		"success": None,
		"error": None,
	}
	# Set the response for the command and message depending on options.
	if cmd_return == True:
		response["cmd"] = cmd
	if msg_return == True:
		response["msg"] = msg
	#-----------------------------------------------------------------------
	# Print the message with rs_logger.message  if it exists and options
	# are set to true.
	#-----------------------------------------------------------------------
	if msg is not None:
		if msg_log == True:
			rs_logger.message(msg)
	#-----------------------------------------------------------------------
	# Print the command with rs_logger.debug if options are set to true.
	#-----------------------------------------------------------------------
	if cmd_log == True:
		rs_logger.debug(cmd)

	#-----------------------------------------------------------------------
	# Run the subprocess.
	#-----------------------------------------------------------------------
	process = subprocess.Popen(
		cmd.split(), # Split the commands so subprocess can run it.
		stdout=subprocess.PIPE, # Pipe stdout so we can read it.
		stderr=subprocess.PIPE # Pipe stderr so we can read it.
	)
	process.wait() # Wait for the command to finish.
	stdout, stderr = process.communicate()
	# Check the returncode. If it's not zero, stderr should exist so
	# show the message in red.
	if process.returncode != 0:
		# Decode UTF-8 so newlines and tabs show correctly.
		utf8_err = stderr.decode('UTF-8')
		# Log the stderr in red with rs_logger.error if options are set
		# to true.
		if stderr_log == True:
			rs_logger.error(utf8_err)
		# Set the stderr response if options are set to true.
		if stderr_return == True:
			response["stderr"] = utf8_err
		# You must set the returned response status, in this case with
		#	error => True
		#	success => False 
		response["error"] = True
		response["success"] = False
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
			response["stdout"] = utf8_out
		# You must set the returned response status, in this case with
		#	error => False 
		#	success => True 
		response["error"] = False
		response["success"] = True
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
	rs_logger.message("----------------------------------TEST RESULTS:---------------------------------")
	print("\n")

	for test_key, test in tests.items():
		#---------------------------------------------------------------
		# Check response "cmd"
		#---------------------------------------------------------------
		# If "should" is None, make sure "actual" is None.
		if test["should"]["cmd"] is None:
			if test["actual"]["cmd"] is not None:
				rs_logger.error(test_key + ": TEST FAILED")
				continue
		# If "should" is not None, make sure "actual" is not None.
		else:
			if test["actual"]["cmd"] is None:
				rs_logger.error(test_key + ": TEST FAILED")
				continue

		#---------------------------------------------------------------
		# Check response "msg"
		#---------------------------------------------------------------
		# If "should" is None, make sure "actual" is None.
		if test["should"]["msg"] is None:
			if test["actual"]["msg"] is not None:
				rs_logger.error(test_key + ": TEST FAILED")
				continue
		# If "should" is not None, make sure "actual" is not None.
		else:
			if test["actual"]["msg"] is None:
				rs_logger.error(test_key + ": TEST FAILED")
				continue

		#---------------------------------------------------------------
		# Check response "stdout"
		#---------------------------------------------------------------
		# If "should" is None, make sure "actual" is None.
		if test["should"]["stdout"] is None:
			if test["actual"]["stdout"] is not None:
				rs_logger.error(test_key + ": TEST FAILED")
				continue
		# If "should" is not None, make sure "actual" is not None.
		else:
			if test["actual"]["stdout"] is None:
				rs_logger.error(test_key + ": TEST FAILED")
				continue

		#---------------------------------------------------------------
		# Check response "stderr"
		#---------------------------------------------------------------
		# If "should" is None, make sure "actual" is None.
		if test["should"]["stderr"] is None:
			if test["actual"]["stderr"] is not None:
				rs_logger.error(test_key + ": TEST FAILED")
				continue
		# If "should" is not None, make sure "actual" is not None.
		else:
			if test["actual"]["stderr"] is None:
				rs_logger.error(test_key + ": TEST FAILED")
				continue

		#---------------------------------------------------------------
		# Check response "success" and "error".
		#---------------------------------------------------------------
		if test["actual"]["error"] != test["should"]["error"]:
			rs_logger.error(test_key + ": TEST FAILED")
			continue
		if test["actual"]["success"] != test["should"]["success"]:
			rs_logger.error(test_key + ": TEST FAILED")
			continue

		#---------------------------------------------------------------
		# TEST PASSED if it got to here.
		#---------------------------------------------------------------
		rs_logger.success(test_key + ": TEST PASSED")
