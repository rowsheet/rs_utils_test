import json
from rs_utils import logger

class Response:

	CMD = None 
	MSG = None 
	STDOUT = None 
	STDERR = None 
	ERROR_MSG = None
	DATA = None

	"""
	Do not change this default value or I will kill you.
	"""
	ERROR = False

	def debug(self, msg=None):
		logger.warning(
			"Response Debug: %s" % str(msg),
			line=True
		)
		logger.debug(
			json.dumps(
				self.__dict__,
				indent=4,
			)
		)
