import os
from rs_utils import logger 

class RSObject(object):

	def __init__(self, test_file_path=None):
		pass

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
		if test_groups is not None:
			return ",".join(list(filter(lambda x: x != "", test_groups.split(","))))
		return ""

	def _test(self, test_file_path=None, test_groups=None):
		try:
			self._reinstall_module()
			self._validate_test_file_path(test_file_path)
			parsed_groups = self._parse_groups(test_groups)
			logger.message_big("Starting unit tests...")
			logger.warning("GROUPS:")
			logger.warning(parsed_groups)
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
			raise SystemExit(1)

#-------------------------------------------------------------------------------
# Unit tests.
#-------------------------------------------------------------------------------
if __name__ == "__main__":
	import os
	install_error = os.system("cd .. && sudo sh install.sh")
	if install_error:
		print("ERROR re-installing rs_utils.")
