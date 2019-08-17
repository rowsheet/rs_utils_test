import fire
import json
from rs_utils.abstract import RSObject

from rs_utils import logger
import traceback 

class Validator(RSObject):

	ARGS = {}
	ARG_ERRORS = {}
	_ERROR = False

	"""
	The validator can be used by using it's public methods, or it can all
	be used in the constructor. If ARG_CONFIG is passed to the constructor,
	self.validate() will use that ARG_CONFGI. If EXCEPTION_FUNCTION is passed
	to the constructor, EXCEPTION_FUNCTION will be called if self.validate()
	sets a non-False self.ERROR(). If EXCEPTION_FUNCTION does not raise an
	exception when called, self.raise_generic_exception() will be called using
	the message produced from EXCEPTION_FUNCTION.
	"""
	def __init__(self,
		ARG_CONFIG=None,
		EXCEPTION_FUNCTION=None,
		json=False,
		**kwargs
	):
		# Make sure to set these values on __init__ otherwise the module
		# function VALIDATE will use old values if the object has already
		# been initialized in the same script.
		self._ERROR = False
		self.ARG_ERRORS = {}
		if ARG_CONFIG is not None:
			self.validate(ARG_CONFIG=ARG_CONFIG, **kwargs)
			if self.ERROR():
				ERROR_DATA = str(self.ERROR(return_json=json))
				if EXCEPTION_FUNCTION is None:
					EXCEPTION_FUNCTION = self.raise_generic_exception
				"""
				EXCEPTION_FUNCTION can either raise an exception or return an
				exception message. If it doesn't raise an exception, use
				self.raise_generic_exception() with the return of the custom
				EXCEPTION_FUNCTION as the ERROR_DATA.
				"""
				ERROR_DATA = EXCEPTION_FUNCTION(ERROR_DATA)
				self.raise_generic_exception(ERROR_DATA)

	def add_error(self, param_name, error_msg):
		self.ARG_ERRORS[param_name] = error_msg

	def ERROR(self, return_json=False):
		if self.ARG_ERRORS == {}:
			return False
		self._ERROR = True
		if return_json == True:
			return json.dumps(
				self.ARG_ERRORS,
				indent=4
			)
		return " ".join([
			self.ARG_ERRORS[param_name]
				for param_name, err_msg
				in self.ARG_ERRORS.items()
			])

	def raise_generic_exception(self, ERROR_DATA="No error message availible."):
		raise Exception(
			"Invalid arguments: %s" % str(ERROR_DATA)
		)

	def _validate_condition(self, param_name, condition, **kwargs):
		try:
			"""
			The param value might be passed a function, but
			it doesn't necessarily mean it's required. If we
			declare it as None now, condition functions will
			have to check for NoneType. Instead, we can just
			call condition() without any parameters if the
			param_name is not in kwargs, that way condition
			functions can just check:

				if param is None:
			"""
			param_value = None
			if param_name in kwargs:
				param_value = kwargs[param_name]
			
				response = condition(param_value)
			else:
				response = condition()
			if type(response).__name__ == "Response":
				if response.ERROR == True:
					raise Exception(
						response.STDERR
					)
		except Exception as ex:
			self.add_error(
				param_name,
				"Invalid param '%s': %s" % (
					param_name,
					str(ex)
				)
			)

	def _validate_active_group(self, 
			active_groups,
			param_name,
			condition,
			**kwargs
		):
		if "group" not in condition:
			raise Exception("Recieved group condition, but no " +
				"'group' name provided. Must pass 'group' to " +
				"condition dict.")
		if "condition" not in condition:
			raise Exception("Recieved group condition, but no " +
				"'condition' function provided. Must pass " +
				"'condition' to condition dict.")
		if active_groups is None:
			raise Exception("active_groups is None for some reason.")	
		group = condition["group"]
		if group in active_groups:
			if active_groups[group] == True:
				if param_name not in kwargs:
					raise Exception(("""Active group is '%s', """ +
					"""but param '%s' in that group was not passed """ +
					"""as a parameter.""") % (
						group, 
						param_name
					))
				else:
					self._validate_condition(
						param_name,
						condition["condition"],
						**kwargs
					)

	"""
	First, go through ARG_CONFIG and find the distict groups.

	Next, Go through the ARG_CONFIG and **kwargs and see which **kwargs are not
	None. If they're not none, find the group that param_name is part of and
	mark the gropu as active.
	"""
	def _parse_active_groups(self, ARG_CONFIG, **kwargs):
		"""
		Find distinct groups.
		"""
		grouped_params = []
		grouped_params = list(
			filter(
				lambda key:
				type(ARG_CONFIG[key]).__name__ == "dict",
				[
					key for key, val in ARG_CONFIG.items()
				]
			)
		)
		"""
		Find groups that are active, indicated by params being passed
		in kwargs.
		"""
		active_groups = {}
		for grouped_param in grouped_params:
			if grouped_param in kwargs:
				active_groups[ARG_CONFIG[grouped_param]["group"]] = True
		return active_groups

	"""
	kwargs for validation params:
		True 	 => required.
		function => raise exception means invalid, capture str(ex).
	"""
	def validate(self, ARG_CONFIG={}, **kwargs):
		"""
		Track the active group condition if it exists.
		"""
		active_groups = self._parse_active_groups(
			ARG_CONFIG=ARG_CONFIG,
			**kwargs,
		)
		for param_name, condition in ARG_CONFIG.items():
			"""
			Check if condition passed is a method of function.
			"""
			if (
				(type(condition).__name__ == "method") or
				(type(condition).__name__ == "function")
			):
				self._validate_condition(
					param_name,
					condition,
					**kwargs,
				)
			"""
			Check if condition is part of a group. If any members of
			the group are present, they're all required per their
			conditions.
			"""
			if type(condition).__name__ == "dict":
				self._validate_active_group(
					active_groups,
					param_name,
					condition,
					**kwargs
				)
			"""
			Check if condition passed is 'True', this means it's
			required.
			"""
			if condition == True:
				if param_name not in kwargs:
					self.add_error(
						param_name,
						"'%s' is required." % param_name
					)

	#-----------------------------------------------------------------------
	# UNIT TESTS (PUBLIC)
	#-----------------------------------------------------------------------

	def test(self,
			test_groups=None,
			test_file_path="../tests/validator.py",
		):
		self._test(
			test_file_path=test_file_path,
			test_groups=test_groups,
		)


def VALIDATE(
		ARG_CONFIG=None,
		EXCEPTION_FUNCTION=None,
		json=False,
		**kwargs
	):
	validator = Validator(
		ARG_CONFIG=ARG_CONFIG,
		EXCEPTION_FUNCTION=EXCEPTION_FUNCTION,
		json=json,
		**kwargs
	)

def main():
	fire.Fire(Validator())

if __name__ == '__main__':
	main()
