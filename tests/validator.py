import json
from rs_utils import unit_test 
from rs_utils.unit_test import TestResult
from rs_utils import validator
from rs_utils.response import Response

"""
Define the validator function that returns a response.
"""
def run_validator(
		ARG_CONFIG=None,
		EXCEPTION_FUNCTION=None,
		json=False,
		**kwargs
	):
	response = Response()
	try:
		validator.VALIDATE(
			ARG_CONFIG=ARG_CONFIG,
			EXCEPTION_FUNCTION=EXCEPTION_FUNCTION,
			json=json,
			**kwargs
		)
		return response
	except Exception as ex:
		response.ERROR = True
		response.STDERR = str(ex)
		return response


def custom_exception_function(ERROR_DATA = None):
	raise Exception(
		"Custom exception: %s" % str(ERROR_DATA)
	)

def assert_str(val=None):
	if type(val).__name__ != "str":
		raise Exception("Value is not a string.")

def assert_int(val=None):
	if type(val).__name__ != "int":
		raise Exception("Value is not an int.")

def assert_optional_str(val=None):
	if val is None:
		return	
	if type(val).__name__ != "str":
		raise Exception("Value is not a string.")

def assert_optional_int(val=None):
	if val is None:
		return	
	if type(val).__name__ != "int":
		raise Exception("Value is not an int.")

def assert_gcloud_machine_type(val=None):
	if val == "gmt_1" or val == "gmt_2":
		return
	raise Exception("Invalid assert gcloud machine type.")

def assert_gcloud_compute_zone(val=None):
	if val == "gcz_1" or val == "gcz_2":
		return
	raise Exception("Invalid assert gcloud compute zone.")

def assert_gcloud_project_id(val=None):
	if val == "gpi_1" or val == "gpi_2":
		return
	raise Exception("Invalid assert gcloud project id.")

def assert_aws_machine_type(val=None):
	if val == "amt_1" or val == "amt_2":
		return
	raise Exception("Invalid assert aws machine type.")

def assert_aws_compute_zone(val=None):
	if val == "acz_1" or val == "acz_2":
		return
	raise Exception("Invalid assert aws compute zone.")

def assert_aws_project_id(val=None):
	if val == "api_1" or val == "api_2":
		return
	raise Exception("Invalid assert aws project id.")


"""
Define the test function.
"""

def test(actual, should, cleanup=None):
	if actual.ERROR != should["ERROR"]:
		"""
		from rs_utils import logger
		logger.error("STDERR:")
		logger.error(actual.STDERR)
		"""
		return TestResult(
			PASSED=False,
			ERROR_MSG=actual.STDERR
		)
	else:
		if actual.ERROR == True:
			if "DATA" in should:
				if actual.STDERR != should["DATA"]:
					return TestResult(
						PASSED=False,
						ERROR_MSG="Should data mismatch, actual: '%s'" %
							actual.STDERR,
					)
				else:
					"""
					from rs_utils import logger 
					logger.error("STDERR:")
					logger.error(actual.STDERR)
					"""
		return TestResult(
			PASSED=True,
		)


"""
Define all the tests.
"""

tests = {
	"FOO_REQUIRED (VALID)": {
		"run": True,
		"actual": lambda: run_validator(
			ARG_CONFIG = {
				"FOO_REQUIRED": True,
				"FOO_OPTIONAL": False,
			},
			# Pass kwargs.
			FOO_REQUIRED = "foo",
		),
		"should": {
			"ERROR": False
		},
	},
	"FOO_REQUIRED (INVALID MISSING)": {
		"run": True,
		"actual": lambda: run_validator(
			ARG_CONFIG = {
				"FOO_REQUIRED": True,
				"FOO_OPTIONAL": False,
			},
			# Pass kwargs.
			# (MISSING) FOO_REQUIRED = "foo",
		),
		"should": {
			"ERROR": True
		},
	},
	"FOO_REQUIRED (CUSTOM EXCEPTION)": {
		"run": True,
		"actual": lambda: run_validator(
			ARG_CONFIG = {
				"FOO_REQUIRED": True,
				"FOO_OPTIONAL": False,
			},
			EXCEPTION_FUNCTION = custom_exception_function,
			# Pass kwargs.
			# (MISSING) FOO_REQUIRED = "foo",
		),
		"should": {
			"ERROR": True,
			"DATA": "Custom exception: 'FOO_REQUIRED' is required.",
		},
	},
	"BAR_REQUIRED (CUSTOM EXCEPTION)": {
		"run": True,
		"actual": lambda: run_validator(
			ARG_CONFIG = {
				"BAR_REQUIRED": True,
				"BAR_OPTIONAL": False,
			},
			EXCEPTION_FUNCTION = custom_exception_function,
			# Pass kwargs.
			# (MISSING) BAR_REQUIRED = "bar",
		),
		"should": {
			"ERROR": True,
			"DATA": "Custom exception: 'BAR_REQUIRED' is required.",
		},
	},
	"More random things": {
		"run": True,
		"actual": lambda: run_validator(
			ARG_CONFIG = {
				"foo": True,
				"bar": True,
				"baz": True,
				"BAR_REQUIRED": True,
				"BAR_OPTIONAL": False,
				"FOO_REQUIRED": True,
				"FOO_OPTIONAL": False,
			},
			EXCEPTION_FUNCTION = custom_exception_function,
			# Pass kwargs.
			# (MISSING) BAR_REQUIRED = "bar",
		),
		"should": {
			"ERROR": True,
			"DATA": "Custom exception: 'foo' is required. 'bar' is required. 'baz' is required. 'BAR_REQUIRED' is required. 'FOO_REQUIRED' is required.",
		},
	},
	"More random things (Provide values)": {
		"run": True,
		"actual": lambda: run_validator(
			ARG_CONFIG = {
				"foo": True,
				"bar": True,
				"baz": True,
				"BAR_REQUIRED": True,
				"BAR_OPTIONAL": False,
				"FOO_REQUIRED": True,
				"FOO_OPTIONAL": False,
			},
			EXCEPTION_FUNCTION = custom_exception_function,
			# Pass kwargs.
			foo = True,
			bar = True,
			baz = True,
			BAR_REQUIRED = True,
			FOO_REQUIRED = True,
		),
		"should": {
			"ERROR": False,
		},
	},
	"More random things (Assert types)": {
		"run": True,
		"actual": lambda: run_validator(
			ARG_CONFIG = {
				"foo": assert_str,
				"bar": assert_str,
				"baz": assert_str,
				"BAR_REQUIRED": assert_int,
				"FOO_REQUIRED": assert_int,
				"BAR_OPTIONAL": assert_optional_int,
				"FOO_OPTIONAL": assert_optional_int,
			},
			EXCEPTION_FUNCTION = custom_exception_function,
			# Pass kwargs.
			foo = None, # Not a string
			bar = None, # Not a string
			baz = None, # Not a string
			BAR_REQUIRED = "NOT AN INT",
			FOO_REQUIRED = "NOT AN INT",
		),
		"should": {
			"ERROR": True,
			"DATA": "Custom exception: Invalid param 'foo': Value is not a string. Invalid param 'bar': Value is not a string. Invalid param 'baz': Value is not a string. Invalid param 'BAR_REQUIRED': Value is not an int. Invalid param 'FOO_REQUIRED': Value is not an int.",
		},
	},
	"More random things (Assert optional types)": {
		"run": True,
		"actual": lambda: run_validator(
			ARG_CONFIG = {
				"FOO_OPTIONAL": assert_optional_int,
				"BAR_OPTIONAL": assert_optional_str,
			},
			EXCEPTION_FUNCTION = custom_exception_function,
			# Pass kwargs.
			# Missing BAR_OPTIONAL = None,
			# Missing FOO_OPTIONAL = None,
		),
		"should": {
			"ERROR": False,
		},
	},
	"More random things (Assert types, almost correct)": {
		"run": True,
		"actual": lambda: run_validator(
			ARG_CONFIG = {
				"foo": assert_str,
				"bar": assert_str,
				"baz": assert_str,
				"BAR_REQUIRED": assert_int,
				"FOO_REQUIRED": assert_int,
				"BAZ_REQUIRED": assert_optional_int,
			},
			EXCEPTION_FUNCTION = custom_exception_function,
			# Pass kwargs.
			foo = None, # Not a string
			bar = "a string",
			baz = "a string",
			BAR_REQUIRED = 123,
			FOO_REQUIRED = 123,
			# Missing BAZ_REQUIRED = 123,
		),
		"should": {
			"ERROR": True,
			"DATA": "Custom exception: Invalid param 'foo': Value is not a string.",
		},
	},
	"More random things (Assert types, JSON)": {
		"run": True,
		"actual": lambda: run_validator(
			ARG_CONFIG = {
				"foo": assert_str,
				"bar": assert_str,
				"baz": assert_str,
				"BAR_REQUIRED": assert_int,
				"FOO_REQUIRED": assert_int,
				"BAZ_REQUIRED": assert_optional_int,
			},
			EXCEPTION_FUNCTION = custom_exception_function,
			# Pass kwargs.
			foo = None, # Not a string
			bar = "a string",
			baz = "a string",
			BAR_REQUIRED = 123,
			FOO_REQUIRED = 123,
			# Missing BAZ_REQUIRED = 123,
			json = True,
		),
		"should": {
			"ERROR": True,
			"DATA": "Custom exception: %s" % json.dumps({
				"foo": "Invalid param 'foo': Value is not a string."
			},indent=4),
		},
	},
	"Arg groups (VALID, No active groups)": {
		"run": True,
		"actual": lambda: run_validator(
			ARG_CONFIG = {
				"foo": assert_str,
				"bar": assert_str,
				"baz": assert_str,
				"gcloud_machine_type": {
					"group": "gcloud",
					"condition": assert_gcloud_machine_type,
				},
				"gcloud_compute_zone": {
					"group": "gcloud",
					"condition": assert_gcloud_compute_zone,
				},
				"gcloud_project_id": {
					"group": "gcloud",
					"condition": assert_gcloud_project_id,
				},
				"aws_machine_type": {
					"group": "aws",
					"condition": assert_aws_machine_type,
				},
				"aws_compute_zone": {
					"group": "aws",
					"condition": assert_aws_compute_zone,
				},
				"aws_compute_project_id": {
					"group": "aws",
					"condition": assert_aws_project_id,
				},
			},
			EXCEPTION_FUNCTION = custom_exception_function,
			# Pass kwargs.
			foo = "a string",
			bar = "a string",
			baz = "a string",
		),
		"should": {
			"ERROR": False,
		},
		"group": "arg_groups",
	},
	"Arg groups (VALID, gcloud active groups)": {
		"run": True,
		"actual": lambda: run_validator(
			ARG_CONFIG = {
				"foo": assert_str,
				"bar": assert_str,
				"baz": assert_str,
				"gcloud_machine_type": {
					"group": "gcloud",
					"condition": assert_gcloud_machine_type,
				},
				"gcloud_compute_zone": {
					"group": "gcloud",
					"condition": assert_gcloud_compute_zone,
				},
				"gcloud_project_id": {
					"group": "gcloud",
					"condition": assert_gcloud_project_id,
				},
				"aws_machine_type": {
					"group": "aws",
					"condition": assert_aws_machine_type,
				},
				"aws_compute_zone": {
					"group": "aws",
					"condition": assert_aws_compute_zone,
				},
				"aws_compute_project_id": {
					"group": "aws",
					"condition": assert_aws_project_id,
				},
			},
			EXCEPTION_FUNCTION = custom_exception_function,
			# Pass kwargs.

			gcloud_machine_type = "gmt_1",
			gcloud_compute_zone = "gcz_1",
			gcloud_project_id = "gpi_1",

			foo = "a string",
			bar = "a string",
			baz = "a string",

			json = True,
		),
		"should": {
			"ERROR": False,
		},
		"group": "arg_groups",
	},
	"Arg groups (INVALID, gcloud active groups, missing machine-type)": {
		"run": True,
		"actual": lambda: run_validator(
			ARG_CONFIG = {
				"foo": assert_str,
				"bar": assert_str,
				"baz": assert_str,
				"gcloud_machine_type": {
					"group": "gcloud",
					"condition": assert_gcloud_machine_type,
				},
				"gcloud_compute_zone": {
					"group": "gcloud",
					"condition": assert_gcloud_compute_zone,
				},
				"gcloud_project_id": {
					"group": "gcloud",
					"condition": assert_gcloud_project_id,
				},
				"aws_machine_type": {
					"group": "aws",
					"condition": assert_aws_machine_type,
				},
				"aws_compute_zone": {
					"group": "aws",
					"condition": assert_aws_compute_zone,
				},
				"aws_compute_project_id": {
					"group": "aws",
					"condition": assert_aws_project_id,
				},
			},
			EXCEPTION_FUNCTION = custom_exception_function,
			# Pass kwargs.

			gcloud_compute_zone = "gcz_1",
			gcloud_project_id = "gpi_1",

			foo = "a string",
			bar = "a string",
			baz = "a string",
		),
		"should": {
			"ERROR": True,
			"DATA": "Active group is 'gcloud', but param 'gcloud_machine_type' in that group was not passed as a parameter.",
		},
		"group": "arg_groups",
	},
	"Arg groups (INVALID, gcloud active groups, invalid machine-type)": {
		"run": True,
		"actual": lambda: run_validator(
			ARG_CONFIG = {
				"foo": assert_str,
				"bar": assert_str,
				"baz": assert_str,
				"gcloud_machine_type": {
					"group": "gcloud",
					"condition": assert_gcloud_machine_type,
				},
				"gcloud_compute_zone": {
					"group": "gcloud",
					"condition": assert_gcloud_compute_zone,
				},
				"gcloud_project_id": {
					"group": "gcloud",
					"condition": assert_gcloud_project_id,
				},
				"aws_machine_type": {
					"group": "aws",
					"condition": assert_aws_machine_type,
				},
				"aws_compute_zone": {
					"group": "aws",
					"condition": assert_aws_compute_zone,
				},
				"aws_compute_project_id": {
					"group": "aws",
					"condition": assert_aws_project_id,
				},
			},
			EXCEPTION_FUNCTION = custom_exception_function,
			# Pass kwargs.

			gcloud_machine_type = "gmt_1_INVALID",
			gcloud_compute_zone = "gcz_1",
			gcloud_project_id = "gpi_1",

			foo = "a string",
			bar = "a string",
			baz = "a string",
		),
		"should": {
			"ERROR": True,
			"DATA": "Custom exception: Invalid param 'gcloud_machine_type': Invalid assert gcloud machine type.",
		},
		"group": "arg_groups",
	},
}

"""
Run all the tests.
"""
import sys
unit_test.run(tests, test, sys.argv)
