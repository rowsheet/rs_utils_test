from rs_utils import docker
from rs_utils import logger 
from rs_utils import runner 
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

def test(actual, should, cleanup):
	if actual.ERROR != should["ERROR"]:
		if cleanup is not None:
			cleanup()
		return TestResult(
			PASSED=False,
			ERROR_MSG=actual.ERROR_MSG
		)
	else:
		if cleanup is not None:
			cleanup()
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
		"cleanup": lambda: runner.step(
			"docker service rm example_service",
			"Cleaning up example_service"
		),
	},
	"Example Missing Dockerfile": {
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
		"cleanup": lambda: runner.step(
			"docker service rm example_missing_dockerfile_service",
			"Cleaning up example_service"
		),
	},
	"Example Missing Entrypoint": {
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
		"cleanup": lambda: runner.step(
			"docker service rm example_missing_entrypoint_service",
			"Cleaning up example_service"
		),
	},
	"Example Broken Entrypoint": {
		"skip": True,
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
		"cleanup": lambda: runner.step(
			"docker service rm example_broken_entrypoint_service",
			"Cleaning up example_service"
		),
	},
}

"""
Run all the tests.
"""
unit_test.run(tests, test)
