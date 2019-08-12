from rs_utils import logger
from rs_utils.itterator import Itterator
from rs_utils.response import Response
import os
import json

def cleanup_parse_docker_config():
	logger.error_big([
		"Unable to parse docker_config."
	])

def parse_docker_config(config_file="./CONFIG.json"):
	response = Response()
	try:
		container_config = {}

		# Log the filepath we're getting the config from.
		logger.debug("Loading configuration fil at: '" + config_file + "'.")

		# Check if the file exists.
		if not os.path.exists(config_file):
			raise Exception("Unable to parse config: '" + config_file + "' does not exist.")

		with open(config_file) as config_file:
			raw_config = config_file.read()
			config = json.loads(raw_config)

			if "HOST_PORT" in config:
				container_config["HOST_PORT"] = config["HOST_PORT"]
			if "CONTAINER_PORT" in config:
				container_config["CONTAINER_PORT"] = config["CONTAINER_PORT"]
			if "SERVICE_NAME" in config:
				container_config["SERVICE_NAME"] = config["SERVICE_NAME"]
			if "CONTAINER_NAME" in config:
				container_config["CONTAINER_NAME"] = config["CONTAINER_NAME"]
			if "DOCKERFILE_PATH" in config:
				container_config["DOCKERFILE_PATH"] = config["DOCKERFILE_PATH"]
			if "IMAGE_NAME" in config:
				container_config["IMAGE_NAME"] = config["IMAGE_NAME"]

		# Mark the response as valid.
		response.ERROR = False
		response.DATA = container_config
		return response
	except Exception as ex:
		response.ERROR = True
		response.ERROR_MSG = str(ex)
		return response

def start_service(config_file="./CONFIG.json"):
	rsi = Itterator()

	# CLEANUP_PARSE_DOCKER_CONFIG
	rsi.register_process({
		"name": "CLEANUP_PARSE_DOCKER_CONFIG",
		"step": cleanup_parse_docker_config,
		"next_process": None
	})

	# PARSE_DOCKER_CONFIG
	rsi.register_process({
		"name": "PARSE_DOCKER_CONFIG",
		"step": parse_docker_config,
		"step_args": {
			# @TODO
			# "config_file": "../tests/CONFIG.json.badfile" # Test with broken file.
			"config_file": config_file,
		},
		"start_process": True,
		"next_process": {
			"BUILD_DOCKER_IMAGE": {
				"ERROR": False,
			},
			"CLEANUP_PARSE_DOCKER_CONFIG": {
				"ERROR": True,
			}
		}
	})

	# BUILD_DOCKER_IMAGE
	rsi.register_process({
		"name": "BUILD_DOCKER_IMAGE",
		"rs_step_cmd": "docker build -t <%image_name%> <%dockerfile_path%>",
		"rs_step_args": {
			"template_vars": {
				"container_name": {
					"from_step": "PARSE_DOCKER_CONFIG",
					"data_key": "CONTAINER_NAME",
				},
				"dockerfile_path": {
					"from_step": "PARSE_DOCKER_CONFIG",
					"data_key": "DOCKERFILE_PATH",
				},
				"image_name": {
					"from_step": "PARSE_DOCKER_CONFIG",
					"data_key": "IMAGE_NAME",
				},
			}
		},
		"next_process": {
			"START_DOCKER_SERVICE": {
				"ERROR": False,
			},
			"CLEANUP_PARSE_DOCKER_CONFIG": {
				"ERROR": True,
			}
		}
	})

	# REMOVE_DOCKER_SERVICE
	rsi.register_process({
		"name": "REMOVE_DOCKER_SERVICE",
		"rs_step_cmd": "docker service rm <%service_name%>",
		"rs_step_args": {
			"template_vars": {
				"service_name": {
					"from_step": "PARSE_DOCKER_CONFIG",
					"data_key": "SERVICE_NAME",
				},
			}
		},
		"next_process": {
			"START_DOCKER_SERVICE": {
				"ERROR": False,
			},
			"REMOVE_DOCKER_SERVICE": {
				"ERROR": True,
			}
		}
	})

	# START_DOCKER_SERVICE
	rsi.register_process({
		"name": "START_DOCKER_SERVICE",
		"rs_step_cmd": "docker service create " + 
			"--name <%service_name%> " + 
			"-p <%host_port%>:<%container_port%> " + 
			"<%image_name%>",
		"rs_step_args": {
			"template_vars": {
				"host_port": {
					"from_step": "PARSE_DOCKER_CONFIG",
					"data_key": "HOST_PORT",
				},
				"container_port": {
					"from_step": "PARSE_DOCKER_CONFIG",
					"data_key": "CONTAINER_PORT",
				},
				"service_name": {
					"from_step": "PARSE_DOCKER_CONFIG",
					"data_key": "SERVICE_NAME",
				},
				"image_name": {
					"from_step": "PARSE_DOCKER_CONFIG",
					"data_key": "IMAGE_NAME",
				},
			}
		},
		"next_process": {
			"DONE": {
				"ERROR": False,
			},
			"REMOVE_DOCKER_SERVICE": {
				"ERROR": True,
			}
		}
	})

	# DONE 
	rsi.register_process({
		"name": "DONE",
		"rs_step_cmd": "echo 'DONE'",
		"rs_step_msg": "DONE",
		"next_process": None
	})

	rsi.run()

# Unit tests.
if __name__ == "__main__":
	start_service()
