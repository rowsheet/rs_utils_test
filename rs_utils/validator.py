import json

class Validator:

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

	"""
	kwargs for validation params:
		True 	 => required.
		function => raise exception means invalid, capture str(ex).
	"""
	def validate(self, ARG_CONFIG={}, **kwargs):
		for param_name, condition in ARG_CONFIG.items():
			if (
				(type(condition).__name__ == "method") or
				(type(condition).__name__ == "function")
			):
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
			# Check if required.
			if condition == True:
				if param_name not in kwargs:
					self.add_error(
						param_name,
						"'%s' is required." % param_name
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

#-------------------------------------------------------------------------------
# Unit tests.
#-------------------------------------------------------------------------------
if __name__ == "__main__":
	import os
	install_error = os.system("cd .. && sudo sh install.sh")
	if install_error:
		print("ERROR re-installing rs_utils.")
	else:
		os.system("python3 ../tests/validator.py")
