from rs_utils import docker
from rs_utils import logger 
from rs_utils import unit_test 
from rs_utils.unit_test import TestResult
import os

"""
Make sure to include the paths for all the Dockerfiles, etc.
"""

rs_util_dev_path = os.environ['RS_UTIL_DEV_PATH']


"""
Define the test function.
"""

def test(actual, should):
	if actual.ERROR != should["ERROR"]:
		return TestResult(
			PASSED=False,
			ERROR_MSG=actual.ERROR_MSG
		)
	else:
		return TestResult(
			PASSED=True,
		)

"""
Define all the tests.
"""

tests = {
	"Example Service": {
		"run": True,
		"actual": lambda: docker.start_service(
			os.path.join(
				rs_util_dev_path,
				"tests",
				"docker_tests",
				"example_service",
			)
		),
		"should": {
			"ERROR": False
		},
	},
	"Example Missing Dockerfile": {
		"run": True,
		"actual": lambda: docker.start_service(
			os.path.join(
				rs_util_dev_path,
				"tests",
				"docker_tests",
				"example_missing_dockerfile",
			)
		),
		"should": {
			"ERROR": True 
		},
	},
	"Example Missing Entrypoint": {
		"run": True,
		"actual": lambda: docker.start_service(
			os.path.join(
				rs_util_dev_path,
				"tests",
				"docker_tests",
				"example_missing_entrypoint",
			)
		),
		"should": {
			"ERROR": True 
		},
	},
	"Example Broken Entrypoint": {
		"run": False,
		"actual": lambda: docker.start_service(
			os.path.join(
				rs_util_dev_path,
				"tests",
				"docker_tests",
				"example_broken_entrypoint",
			)
		),
		"should": {
			"ERROR": True 
		},
	},
}

"""
Run all the tests.
"""
unit_test.run(tests, test)
