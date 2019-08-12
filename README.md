# RowSheet Utils

Install:

	python3 setup.py install

Usage:

	>>> # Example command using the runner.
	... 
	>>> from rs_utils import rs_runner
	>>> response = rs_runner.step("docker ps", "Listing containers...")
	Listing containers...
	docker ps
	CONTAINER ID        IMAGE                                COMMAND                  CREATED             STATUS              PORTS                                                NAMES
	56e898c09b3e        rowsheet/public_docker_base:v0.0.1   "/bin/bash"              3 days ago          Up 8 hours          0.0.0.0:4000->4000/tcp                               api
	9f5208c25737        b7585da104a5                         "/bin/bash"              13 days ago         Up 2 days           0.0.0.0:8888->8888/tcp                               base

	>>> 
	>>> 
	>>> 
	>>> # Example command using the logger.
	... 	
	>>> from rs_utils import rs_logger
	>>> rs_logger.success("Success! Logger Works!", line=True, line_count=80)
	---------------------------- Success! Logger Works! ----------------------------

### By RowSheet
