import traceback
from rs_utils import logger

class TestResult:
	PASSED = None
	ERROR_MSG = None
	SKIPPED = False 
	def __init__(self, PASSED=False, ERROR_MSG="NA", SKIPPED=False):
		self.PASSED = PASSED
		self.ERROR_MSG = ERROR_MSG
		self.SKIPPED = SKIPPED 

def _log_cleanup_warning():
	logger.warning("Warning: test 'cleanup' is not a function. Should be passed as:")
	logger.warning("\t...")
	logger.warning("\t\tcleanup: lambda: function,")
	logger.warning("\t...")
	logger.warning("Running test without cleanup")

def _log_auto_cleanup_warning():
	logger.warning("Warning: test 'auto_cleanup' is not a function. Should be passed as:")
	logger.warning("\t...")
	logger.warning("\t\tauto_cleanup: lambda: function,")
	logger.warning("\t...")
	logger.warning("Running test without auto_cleanup")

"""
A unit test requires a number of things:

	Required:

	1) Condition for test to be run at all.
		"run": True (OR) "skip": False
	2) The Response (rs_utils.response) of the process in "actual".
		"actual": [some response]
	3) The "should" values of the response to be checked.
		"should": [some dict]

	Optional:

	4) Cleanup function to be passed back to the test function.
	   It must be called in the test function to be used at all.
	   This should be of type "function".
		"cleanup": lambda: [some cleanup function]
	5) Auto-Cleanup function.
	   This is called on every step automatically if specified.
	   This should be of type "function".
		"auto_cleanup": lambda: [some auto-cleanup function]
"""
def _run_test(test_name=None, test=None, test_function=None):
	# logger.success("test_function:" + type(test_function).__name__)
	# logger.success("test_name:" + type(test_name).__name__)
	# logger.success("test:" + type(test).__name__)


	logger.debug("%s: Running..." % test_name)

	"""
	Collect the spec of "should" and run "actual" so we can
	compare the values with the test_function().
	"""
	actual = test["actual"]()
	should = test["should"]

	"""
	Parse possible cleanup and auto-cleanup functions. Check
	and make sure they're valid. Record their validities or errors
	so we don't run them if they're invalid.
	"""
	cleanup = None
	run_cleanup_function = False
	bad_cleanup_function = False

	auto_cleanup = None
	run_auto_cleanup_function = False
	bad_auto_cleanup_function = False

	if "cleanup" in test:
		cleanup = test["cleanup"]
		if type(cleanup).__name__ != "function":
			bad_cleanup_function = True
		else:
			run_cleanup_function = True

	if "auto_cleanup" in test:
		auto_cleanup = test["auto_cleanup"]
		if type(auto_cleanup).__name__ != "function":
			bad_auto_cleanup_function = True
		else:
			run_auto_cleanup_function = True

	"""
	Run the test function:
		> without cleanup if cleanup is invalid.
		> without cleanup cleanup is None.
		> with cleanup cleanup valid.
	"""

	if bad_cleanup_function == True:
		_log_cleanup_warning()
		test_result = test_function(
			actual,
			should,
		)
	elif run_cleanup_function == True:
		test_result = test_function(
			actual,
			should,
			cleanup,
		)
	else:
		test_result = test_function(
			actual,
			should,
		)

	"""
	Run the auto-cleanup function if it's valid.
	"""

	if bad_auto_cleanup_function == True:
		_log_auto_cleanup_warning()
	elif run_auto_cleanup_function == True:
		auto_cleanup()

	"""
	Return the test result.
	"""

	return test_result

def _parse_groups(groups, skip_first_arg=False):
	start_index = 0
	if type(groups).__name__ == "str":
		return list(filter(lambda x: x != "", groups.split(",")))
	if skip_first_arg == True:
		start_index = 1
	if groups is None:
		return None
	if skip_first_arg == True and len(groups) == 1:
		return None
	if len(groups) == (start_index + 1):
		return list(filter(lambda x: x != "", groups[start_index].split(",")))
	else:
		return list(filter(lambda x: x != "", groups[start_index:]))

def _test_in_group(test, groups, test_name):
	test_groups = []
	if "group" in test:
		test_groups = _parse_groups(test["group"])
	elif "groups" in test:
		test_groups = _parse_groups(test["groups"])
	for group in groups:
		for test_group in test_groups:
			if group == test_group:
				return True
	return False

"""
Running tests uses this function in unit test files.
Test files should be able to be run by simply running:

	python /path/to/test.py 

Additionally, tests can be skipped by passing a test group or comma separated
list of test groups to argv of the test file, i.e.

	pytong /path/to/test.py group1,group2,group3

If a group is passed, tests that do not have that group will
be skipped.

Tests can also be skipped if in the test definition, iether:

	1) "skip": True
	2) "run": False

Tests are run with "skip" => False and "run" => True by default.
"""
def run(tests=None, test_function=None, argv=None):
	summary = {}
	groups = _parse_groups(argv, skip_first_arg=True)
	try:
		for test_name, test in tests.items():
			"""
			Determine if the test should be skipped. It should be skipped
			if "run" => False, "skip" => True, or groups are not null and
			the test is not in the group.
			"""
			skip = False
			if "run" in test:
				if test["run"] == False:
					skip = True
			if "skip" in test:
				if test["skip"] == True:
					skip = True
			if (skip == False) and (groups is not None):
				test_in_group = _test_in_group(test, groups, test_name)
				if test_in_group == False:
					skip = True
			"""
			Create the test result by either running the test or creating
			a blank TestResult with SKIPPED=True, then append the test_result
			to the summary so we can print them out later.
			"""
			test_result = None
			if skip == True:
				test_result = TestResult(SKIPPED=True)
			else:
				test_result = _run_test(
					test_name=test_name,
					test=test,
					test_function=test_function
				)
			summary[test_name] = test_result
		logger.message_big("Test Summary:")
		for test_name, test_result in summary.items():
			if test_result.SKIPPED == True:
				logger.warning("%s: Test skipped." % test_name)
			elif test_result.PASSED == True:
				logger.success("%s: Test passed." % test_name)
			else:
				logger.error("%s: Test failed." % test_name)
				logger.error("\t\t%s." % test_result.ERROR_MSG)
	except Exception as ex:
		logger.error_big("Unable to run tests.")
		logger.error(str(ex))
		traceback.print_tb(ex.__traceback__)



# Unit test
if __name__ == "__main__":
	from rs_utils import runner

	def test_function(actual, should):
		return TestResult(
			PASSED=True
		)

	cmd_log = False
	msg_log = False
	stdout_log = False

	tests = {
		"TEST_SKIP_TRUE": {
			"skip": True,
			"actual": lambda: runner.step(
				"echo TEST_SKIP_TRUE",
				"Running TEST_SKIP_TRUE",
				cmd_log = cmd_log,
				msg_log = msg_log,
				stdout_log = stdout_log,
			),
			"should": {
				"ERROR": False
			},
		},
		"TEST_SKIP_FALSE": {
			"skip": False,
			"actual": lambda: runner.step(
				"echo TEST_SKIP_FALSE",
				"Running TEST_SKIP_FALSE",
				cmd_log = cmd_log,
				msg_log = msg_log,
				stdout_log = stdout_log,
			),
			"should": {
				"ERROR": False
			},
		},
		"TEST_RUN_TRUE": {
			"run": True,
			"actual": lambda: runner.step(
				"echo TEST_RUN_TRUE",
				"Running TEST_RUN_TRUE",
				cmd_log = cmd_log,
				msg_log = msg_log,
				stdout_log = stdout_log,
			),
			"should": {
				"ERROR": False
			},
		},
		"TEST_RUN_FALSE": {
			"run": False,
			"actual": lambda: runner.step(
				"echo TEST_RUN_FALSE",
				"Running TEST_RUN_FALSE",
				cmd_log = cmd_log,
				msg_log = msg_log,
				stdout_log = stdout_log,
			),
			"should": {
				"ERROR": False
			},
		},
		"TEST_GROUP_FOO": {
			"actual": lambda: runner.step(
				"echo TEST_GROUP_FOO",
				"Running TEST_GROUP_FOO",
				cmd_log = cmd_log,
				msg_log = msg_log,
				stdout_log = stdout_log,
			),
			"should": {
				"ERROR": False
			},
			"group": "FOO",
		},
		"TEST_GROUP_BAR": {
			"actual": lambda: runner.step(
				"echo TEST_GROUP_BAR",
				"Running TEST_GROUP_BAR",
				cmd_log = cmd_log,
				msg_log = msg_log,
				stdout_log = stdout_log,
			),
			"should": {
				"ERROR": False
			},
			"group": "BAR",
		},
		"TEST_GROUP_BAZ": {
			"actual": lambda: runner.step(
				"echo TEST_GROUP_BAZ",
				"Running TEST_GROUP_BAZ",
				cmd_log = cmd_log,
				msg_log = msg_log,
				stdout_log = stdout_log,
			),
			"should": {
				"ERROR": False
			},
			"group": "BAZ",
		},
		"TEST_MULTI_GROUP_LIST": {
			"actual": lambda: runner.step(
				"echo TEST_MULTI_GROUP_LIST",
				"Running TEST_MULTI_GROUP_LIST",
				cmd_log = cmd_log,
				msg_log = msg_log,
				stdout_log = stdout_log,
			),
			"should": {
				"ERROR": False
			},
			"group": ["FOO", "BAR", "BAZ"],
		},
		"TEST_MULTI_GROUP_CSV": {
			"actual": lambda: runner.step(
				"echo TEST_MULTI_GROUP_CSV",
				"Running TEST_MULTI_GROUP_CSV",
				cmd_log = cmd_log,
				msg_log = msg_log,
				stdout_log = stdout_log,
			),
			"should": {
				"ERROR": False
			},
			"group": "FOO,BAR,BAZ",
		},
		"TEST_MULTI_GROUPS_LIST_NO_BAZ": {
			"actual": lambda: runner.step(
				"echo TEST_MULTI_GROUPS_LIST",
				"Running TEST_MULTI_GROUPS_LIST",
				cmd_log = cmd_log,
				msg_log = msg_log,
				stdout_log = stdout_log,
			),
			"should": {
				"ERROR": False
			},
			"groups": ["FOO", "BAR"]
		},
		"TEST_MULTI_GROUPS_CSV_NO_BAZ": {
			"actual": lambda: runner.step(
				"echo TEST_MULTI_GROUPS_CSV",
				"Running TEST_MULTI_GROUPS_CSV",
				cmd_log = cmd_log,
				msg_log = msg_log,
				stdout_log = stdout_log,
			),
			"should": {
				"ERROR": False
			},
			"groups": "FOO,BAR",
		},
	}

	"""
	Simulate argv:
		python test.py
	"""
	logger.message_big("Testing Normal")
	fake_argv = ["unit_test.py"]
	run(
		tests=tests,
		test_function=test_function,
		argv=fake_argv
	)
	"""
	Simulate argv:
		python test.py FOO,BAZ
	"""
	logger.message_big("Testing Multi Group (csv): FOO,BAZ")
	fake_argv = ["unit_test.py", "FOO,BAZ,"]
	run(
		tests=tests,
		test_function=test_function,
		argv=fake_argv
	)
	"""
	Simulate argv:
		python test.py FOO BAR BAZ
	"""
	logger.message_big("Testing Multi Group (list): FOO BAR BAZ")
	fake_argv = ["unit_test.py", "FOO", "BAR", "BAZ"]
	run(
		tests=tests,
		test_function=test_function,
		argv=fake_argv
	)
	"""
	Simulate argv:
		python test.py FOO
	"""
	logger.message_big("Testing Group: FOO")
	fake_argv = ["unit_test.py", "FOO"]
	run(
		tests=tests,
		test_function=test_function,
		argv=fake_argv
	)
	"""
	Simulate argv:
		python test.py BAR 
	"""
	logger.message_big("Testing Group: BAR")
	fake_argv = ["unit_test.py", "BAR"]
	run(
		tests=tests,
		test_function=test_function,
		argv=fake_argv
	)
	"""
	Simulate argv:
		python test.py BAZ 
	"""
	logger.message_big("Testing Group: BAZ")
	fake_argv = ["unit_test.py", "BAZ"]
	run(
		tests=tests,
		test_function=test_function,
		argv=fake_argv
	)
