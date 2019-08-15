import os
import traceback
from rs_utils import logger 

def run(common_tests, argv):
	try:
		"""-------------------------------------------------------------
		| Validate args. There should only be one "test_name" in argv[1].
		| If there are other args, log a warning. Check that the test_name
		| exists in "common_tests".
		-------------------------------------------------------------"""

		if len(argv) == 1:
			raise Exception("ERROR: Must provide a common test name.")
		if len(argv) > 2:
			logger.warning("WARNING: Expected only one argument: common_test_name.")
		common_test_name = argv[1]
		if common_test_name not in common_tests:
			raise Exception("ERROR: Invalid common_test_name.")

		"""-------------------------------------------------------------
		| Parse the test.
		| 	"cmd": 		Required
		| 	"note": 	Optional 
		| 	"gropus": 	Optional 
		-------------------------------------------------------------"""

		test = common_tests[common_test_name]
		cmd = test["cmd"]

		"""-----------------------------
		| Optional Note:
		-----------------------------"""
		note = None
		if "note" in test:
			note = test["note"]

		"""-----------------------------
		| Optional Groups:
		-----------------------------"""
		groups = None
		if "groups" in test:
			groups = ",".join(test["groups"])
			cmd += groups

		"""-------------------------------------------------------------
		| Log the test.
		| Log the note if it exists.
		| Log the cmd with logger.debug().
		-------------------------------------------------------------"""

		logger.message_big(
			"RUNNING COMMON TEST: '%s'" %
			common_test_name
		)
		if note is not None:	
			logger.message(note, line=True)
		logger.debug(cmd)
		os.system(cmd)
	except Exception as ex:
		logger.error_big("Unable to run common test.")
		logger.error(str(ex))
		traceback.print_tb(ex.__traceback__)
		raise SystemExit(1)
