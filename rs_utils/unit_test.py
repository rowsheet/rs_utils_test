from rs_utils import logger 

class TestResult:
	PASSED = None
	ERROR_MSG = None
	SKIPPED = False 
	def __init__(self, PASSED=False, ERROR_MSG="NA", SKIPPED=False):
		self.PASSED = PASSED
		self.ERROR_MSG = ERROR_MSG
		self.SKIPPED = SKIPPED 

def _run_test(test_name, test, test_function):
	logger.debug("%s: Running..." % test_name)
	actual = test["actual"]()
	should = test["should"]
	cleanup = None
	if "cleanup" in test:
		cleanup = test["cleanup"]
	return test_function(actual, should, cleanup)

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
