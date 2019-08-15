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
def _run_test(test_name, test, test_function):

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

def run(tests, test_function):
	summary = {}
	try:
		for test_name, test in tests.items():
			skip = False
			if "run" in test:
				if test["run"] == False:
					skip = True
			if "skip" in test:
				if test["skip"] == True:
					skip = True
			if skip == True:
				summary[test_name] = TestResult(SKIPPED=True)
			else:
				summary[test_name] = _run_test(test_name, test, test_function)
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
