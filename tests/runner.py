from rs_utils import runner
from rs_utils import logger

# All unit tests.
tests = {
	# Test creating a file.
	"touch": {
		"actual": runner.step(
			"touch test.txt",
			"Creating test file...",
		),
		"should": {
			"cmd": "touch test.txt",
			"msg": "Creating test file...",
			"stderr": None,
			"stdout": "",
			"error": False
		}
	},
	# Test removing a file.
	"touch": {
		"actual": runner.step(
			"rm test.txt",
			"Creating test file...",
		),
		"should": {
			"cmd": "touch test.txt",
			"msg": "Creating test file...",
			"stderr": None,
			"stdout": "",
			"error": False
		}
	},
	# Test listing containers.
	"docker_ps": {
		"actual": runner.step(
			"docker ps",
			"Listing running containers...",
		),
		"should": {
			"cmd": "",
			"msg": "",
			"stderr": None,
			"stdout": "",
			"error": False
		}
	},
	# Test listing containers without "command" logging or return.
	"docker_ps_NO_CMD": {
		"actual": runner.step(
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
			"error": False
		}
	},
	# Test listing containers without "stdout" logging or return.
	"docker_ps_NO_STDOUT": {
		"actual": runner.step(
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
			"error": False
		}
	},
	# Test removing a container that doesn't exist.
	"docker_rm_error": {
		"actual": runner.step(
			"docker rm containerthatdoesntexist",
			"Listing running containers...",
		),
		"should": {
			"cmd": "",
			"msg": "",
			"stderr": "", # Ensure "stderror" is not None.
			"stdout": None,
			"error": True
		}
	},
	# Test removing a container that doesn't exist without
	# "stderr" logging or return.
	"docker_rm_error_NO_STDERR": {
		"actual": runner.step(
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
	# TEST PASSED if it got to here.
	#---------------------------------------------------------------
	logger.success(test_key + ": TEST PASSED")
