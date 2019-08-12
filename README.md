# RowSheet Utils

Install:

	python3 setup.py install

Runner Usage:

	>>> from rs_utils import runner
	>>> response = runner.step("docker ps", "Listing containers...")
	Listing containers...
	docker ps
	CONTAINER ID        IMAGE                                COMMAND                  CREATED             STATUS              PORTS                                                NAMES
	56e898c09b3e        rowsheet/public_docker_base:v0.0.1   "/bin/bash"              3 days ago          Up 8 hours          0.0.0.0:4000->4000/tcp                               api
	9f5208c25737        b7585da104a5                         "/bin/bash"              13 days ago         Up 2 days           0.0.0.0:8888->8888/tcp                               base

Logger Usage:

	>>> from rs_utils import logger
	>>> logger.success("Success! Logger Works!", line=True, line_count=80)
	---------------------------- Success! Logger Works! ----------------------------

Itterator Usage:

	>>> from rs_utils.itterator import Itterator
	>>> cleanup_file_step_one_cmd = "rm file_step_one.txt"
	>>> cleanup_file_step_one_msg = "Cleaning up, removing file_step_one.txt."
	>>> # Create the itterator.
	... 
	>>> rsi = Itterator()
	- - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - -
				   Starting new Itterator...                            
	- - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - -
	>>> 
	>>> # CREATE_FILE_STEP_ONE.
	... #       Create a file called "file_step_one.txt".
	... rsi.register_process({
	...         "name": "CREATE_FILE_STEP_ONE",
	...         "rs_step_cmd": "touch file_step_one.txt",
	...         "rs_step_msg": "Creating file_step_one.txt",
	...         "rs_step_args": {
	...                 "cmd_log": True,
	...                 "cmd_return": True,
	...         },
	...         "start_process": True,
	...         "next_process": "ECHO_TO_FILE_STEP_ONE",
	...         "stop_on_error": True,
	... })
	>>> # ECHO_TO_FILE_STEP_ONE
	... #       Add 'something' to "file_step_one.txt".
	... rsi.register_process({
	...         "name": "ECHO_TO_FILE_STEP_ONE",
	...         # "rs_step_cmd": "echob 'something' >> file_step_one.txt", # Test using an invalid command.
	...         "rs_step_cmd": "echo 'something' >> file_step_one.txt",
	...         "rs_step_msg": "Echoing to file_step_one.txt",
	...         # Cleanup by removing the file.
	...         "cleanup_rs_step_cmd": cleanup_file_step_one_cmd,
	...         "cleanup_rs_step_msg": cleanup_file_step_one_msg,
	...         "stop_on_error": True,
	... })
	>>> # Run the itterator.
	... rsi.run()
	------------------------- Running pre-flight checks... -------------------------
	----------------------------- Running itterator... -----------------------------
	- - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - -
				    Running Itterator Step:                             
				      CREATE_FILE_STEP_ONE                              
	- - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - -
	Creating file_step_one.txt
	touch file_step_one.txt

	- - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - -
				    Running Itterator Step:                             
				     ECHO_TO_FILE_STEP_ONE                              
	- - - - - - - - - - - - - - - - - - - -  - - - - - - - - - - - - - - - - - - - -
	Echoing to file_step_one.txt
	echo 'something' >> file_step_one.txt

	All processes complete.

### By RowSheet
