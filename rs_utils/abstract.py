from rs_utils import logger 

class RSObject(object):

	def __init__(self, test_file_path=None):
		pass

	def _test(self, test_file_path=None):
		try:
			logger.message_big("Re-installing package modules...")
			if test_file_path is None:
				raise Exception(
					"Unable to run test: no test_file_path provided."
				)
			import os
			if os.path.exists("../install.sh") == False:
				raise Exception(
					"Unable to install package:" +
					"../install.sh doesn't exist."
				)
			install_error = os.system("cd .. && sudo sh install.sh")
			if install_error:
				raise Exception("ERROR re-installing module.")
			else:
				logger.success(
					"Successfully re-installed package modules..."
				)
				logger.message_big("Starting unit tests...")
				os.system("python3 %s" % test_file_path)
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
