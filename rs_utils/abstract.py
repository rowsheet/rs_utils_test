from abc import ABC
import traceback
import json
import sys
import os
from rs_utils import logger 
from rs_utils.response import Response

class RSObject(object):

	"""=====================================================================
		 __         __                  __                         __     __
	  ____ _/ /_  _____/ /__________ ______/ /_   ____ ___  ____  ____/ /__  / /
	 / __ `/ __ \/ ___/ __/ ___/ __ `/ ___/ __/  / __ `__ \/ __ \/ __  / _ \/ / 
	/ /_/ / /_/ (__  ) /_/ /  / /_/ / /__/ /_   / / / / / / /_/ / /_/ /  __/ /  
	\__,_/_.___/____/\__/_/   \__,_/\___/\__/  /_/ /_/ /_/\____/\__,_/\___/_/   
										    
	====================================================================="""

	_LOG_LEVEL = "ERROR"
	_EXIT_ON_ERROR = False
	_LOG_PARAMS = False

	"""
	Parse dir(self) until you hit "__class__", all the functions
	are defined on the other side of dir, but if JSON passes
	something with the same val a a method, it collides, so we
	have to check that it's not in the method_list.
	"""
	def __init__(self, **kwargs):
		method_list = [func for func in dir(self) if callable(getattr(self, func))]
		for var in dir(self):
			if var == "__class__":
				break
			"""
			Check for values in kwargs. If it's there,
			set the attribute.
			"""
			if var not in method_list:
				if var in kwargs:
					setattr(self, var, kwargs[var])

	"""
	Initialize yourself with JSON.
	"""
	@classmethod
	def from_json(cls, json_str):
		json_dict = json.loads(json_str)
		return cls(**json_dict)

	def to_json(self, indent=True):
		if indent == True:
			return json.dumps(
				self.__dict__,
				indent = 4
			)
		return json.dumps(
			self.__dict__,
		)

	def _extract_calling_method_name(self):
		"""
		We have to call traceback.extract_stack() to get frame summary
		data, but we'll get it as a string.

		if we pp.pprint(repr_es), repr_es will be a string of something like
		this:

		[
			<FrameSummary file foo.py, line 92 in <module>>,
			<FrameSummary file foo.py, line 77 in foo>,
			<FrameSummary file foo.py, line 64 in _step>,
			<FrameSummary file foo.py, line 56 in _extract_calling_method_name>
		]

		"""
		stack = traceback.extract_stack()
		repr_es = repr(stack)
		"""
		We need to take the above repr_es string and remove the array brackets,
		then split the rest by the sepparating ">, <" brackets.
		"""
		stack_messages = repr_es[1:-1].split(">, <")
		"""
		Because this method is called by a method of an extended class of
		this class, the first FrameSummary is always the module, so it's always
		the second FrameSummary, so we need to fetch by the index (1)
		"""
		calling_frame_summary = stack_messages[1]
		"""
		Finally, the method name is the last word at the end of the FrameSummary,
		and since the FrameSummary is actually a string serialization, it's just
		a string that we split by " ".
		"""
		calling_method_name = calling_frame_summary.split(" ")[-1]
		"""
		Return the calling method name.
		"""
		return calling_method_name

	"""
	Log the kwarg params for extended public functions only if:
		1) _LOG_PARAMS == True
		2) FROM_ERROR == True
	Don't log the params if _LOG_PARAMS are set to False, but if it's from an
	error, log the params anyway and print the label as red.
	"""
	def _log_params(self, FROM_ERROR=False, **kwargs):

		# By default, the log function is debug.
		log_func = logger.debug

		# Check if it's from an error. set _LOG_PARAMS = True if this was
		# called from an error.
		if FROM_ERROR == True:
			log_func = logger.error
			self._LOG_PARAMS = True
		args_msg = json.dumps(
			kwargs,
			indent = 4
		)

		# Only log if _LOG_PARAMS == True.
		if self._LOG_PARAMS == True:
			log_func("ARGS: ")
			logger.debug(args_msg)

	"""
	Get the class name  and method name.
	"""
	def _get_stack_info(self):
		return {
			"method_name": self._extract_calling_method_name(),
			"class_name": self.__class__.__name__,
		}

	"""
	Check the _LOG_LEVEL.
	If it's set to debug:
		1) Log the class and method that it came from.
		2) Log the params if _LOG_PARAMS == True.
	"""
	def _log_debug(self, **kwargs):
		if self._LOG_LEVEL == "DEBUG":

			# Get the class name  and method name. Log it in "debug" color.
			stack_info = self._get_stack_info()
			logger.debug("RUNNING: %s.%s()" % (
				stack_info["class_name"],
				stack_info["method_name"],
			))

			# Conditionally log the params based on _LOG_PARAMS.
			self._log_params(
				FROM_ERROR=False,
				**kwargs
			)

	"""
	Check the _LOG_LEVEL.
	If it's set to ERROR or DEBUG:
		1) Log the class and method that it came from.
		2) Alway log the params.
	"""
	def _log_error(self, ex, **kwargs):
		if self._LOG_LEVEL == "ERROR" or self._LOG_LEVEL == "DEBUG":

			# Get the class name  and method name. Log it in "error" color.
			stack_info = self._get_stack_info()
			logger.error_big("ERROR RUNNING: %s.%s()" % (
				stack_info["class_name"],
				stack_info["method_name"],
			))

			# Log the params and set FROM_ERROR=True so that
			# _log_params will always log and log in "error" color.
			self._log_params(
				FROM_ERROR=True,
				**kwargs
			)
			logger.error("EXCEPTION from %s.%s(): %s" % (
				stack_info["class_name"],
				stack_info["method_name"],
				str(ex),
			))
			traceback.print_tb(ex.__traceback__)
			if self._EXIT_ON_ERROR == True:
				raise SystemExit(1)

	"""
	Run Common functions implemented in this base class. This requires
	that extended classes must implement the "underscore" version of common
	methods, or an error will be raised, i.e.

		obj = Obj()
		obj.CREATE(**kwargs)

	Requires:

		class Obj(RSObject):
			def _CREATE(self, **kwargs):
				...
				return "some_data"

	Whatever is returned in _CREATE(**kwargs) will be availble by calling
	the DATA of the Response of CREATE(**kwargs), i.e.:

		response = obj.CREATE(**kwargs)
		response.DATA == "some_data"
		> True
	"""
	def _RUN_COMMON(self, func, **kwargs):
		response = Response()
		try:
			self._log_debug(**kwargs)
			if func not in dir(self):
				raise Exception((
					"Unable to execute method '%s': " +
					"Method '%s' of class '%s' needs to " +
					"be implemented in class '%s'." ) % (
					func[1:],
					func,
					self.__class__.__name__,
					self.__class__.__name__,
				))
			result = getattr(self, func)(**kwargs)
			response.DATA = result
			return response
		except Exception as ex:
			self._log_error(ex, **kwargs)
			response.ERROR = True
			response.STDERR = str(ex)
			return response

	"""
	Common methods are CRUD operations.
	"""
	def CREATE(self, **kwargs):
		return self._RUN_COMMON("_CREATE", **kwargs)

	def READ(self, **kwargs):
		return self._RUN_COMMON("_READ", **kwargs)

	def UPDATE(self, **kwargs):
		return self._RUN_COMMON("_UPDATE", **kwargs)

	def DELETE(self, **kwargs):
		return self._RUN_COMMON("_DELETE", **kwargs)

	"""=====================================================================
	   __            __  _                      __  _ __    
	  / /____  _____/ /_(_)___  ____ _   __  __/ /_(_) /____
	 / __/ _ \/ ___/ __/ / __ \/ __ `/  / / / / __/ / / ___/
	/ /_/  __(__  ) /_/ / / / / /_/ /  / /_/ / /_/ / (__  ) 
	\__/\___/____/\__/_/_/ /_/\__, /   \__,_/\__/_/_/____/  
				 /____/                         
	====================================================================="""

	def _reinstall_module(self):
		logger.message_big("Re-installing package modules...")
		if os.path.exists("../install.sh") == False:
			raise Exception(
				"Unable to install package:" +
				"../install.sh doesn't exist."
			)
		install_error = os.system("cd .. && sudo sh install.sh")
		if install_error:
			raise Exception("ERROR re-installing module.")
		logger.success(
			"Successfully re-installed package modules..."
		)

	def _validate_test_file_path(self, test_file_path):
		if test_file_path is None:
			raise Exception(
				"Unable to run test: no test_file_path provided."
			)

	def _parse_groups(self, test_groups):

		# Fix parsing from CLI args from fire.
		# Sometimes it's a tuple, sometimes it's a string.

		if type(test_groups).__name__ == "tuple":
			test_groups = ",".join(list(test_groups))

		# Process the csv again, but this time filter empty ones.

		if test_groups is not None:
			return ",".join(list(filter(lambda x: x != "", test_groups.split(","))))
		return ""

	def _test(self, test_file_path=None, test_groups=None):
		try:
			self._reinstall_module()
			self._validate_test_file_path(test_file_path)
			parsed_groups = self._parse_groups(test_groups)
			logger.message_big("Starting unit tests...")
			if parsed_groups != "":
				logger.message("Only running test for groups: '%s'" %
					parsed_groups)
			os.system("python3 %s %s" % (
					test_file_path,
					parsed_groups,
				)
			)
		except Exception as ex:
			logger.error_big([
				"Error re-installing module on unit test:",
				str(ex)
			])
			traceback.print_tb(ex.__traceback__)
			raise SystemExit(1)

#-------------------------------------------------------------------------------
# Unit tests.
#-------------------------------------------------------------------------------
if __name__ == "__main__":
	import os
	install_error = os.system("cd .. && sudo sh install.sh")
	if install_error:
		print("ERROR re-installing rs_utils.")
