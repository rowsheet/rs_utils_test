class RSObject(object):

        def __init__(self, test_file_path=None):
                pass

        def _test(self, test_file_path=None):
                import os
                if test_file_path is None:
                        raise Exception("Unable to run test: no test_file_path provided.")
                if os.path.exists("../install.sh") == False:
                        raise Exception("Unable to install package: "
                                + " ../install.sh doesn't exist.")
                install_error = os.system("cd .. && sudo sh install.sh")
                if install_error:
                        print("ERROR re-installing rs_ops.")
                else:
                        os.system("python3 %s" % test_file_path)

#-------------------------------------------------------------------------------
# Unit tests.
#-------------------------------------------------------------------------------
if __name__ == "__main__":
	import os
	install_error = os.system("cd .. && sudo sh install.sh")
	if install_error:
		print("ERROR re-installing rs_utils.")
