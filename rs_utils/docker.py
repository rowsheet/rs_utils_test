from rs_utils import logger
from rs_utils.itterator import Itterator
from rs_utils.response import Response
import os
import json

def LOG_ERROR__VALIDATE_RS_DOCKER_CONFIG():
	response = Response()
	err_msg = "Invalid RowSheet Docker config."
	logger.error_big(err_msg)
	response.ERROR = True
	response.ERROR_MSG = err_msg
	return response

def LOG_ERROR__VALIDATE_DOCKERFILE():
	response = Response()
	err_msg = "Invalid Dockerfile."
	logger.error_big(err_msg)
	response.ERROR = True
	response.ERROR_MSG = err_msg
	return response

def _validate_rs_docker_config(rs_docker_config_file_path):
	response = Response()
	try:
		container_config = {}

		# Log the filepath we're getting the config from.
		logger.debug("Loading configuration file at: '"
			+ rs_docker_config_file_path + "'.")

		# Check if the file exists.
		if not os.path.exists(rs_docker_config_file_path):
			raise Exception("Unable to parse config: '" 
				+ rs_docker_config_file_path+ "' does not exist.")

		with open(rs_docker_config_file_path) as config_file:
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
			if "IMAGE_NAME" in config:
				container_config["IMAGE_NAME"] = config["IMAGE_NAME"]

		# Mark the response as valid.
		response.ERROR = False
		response.DATA = container_config
		return response
	except Exception as ex:
		logger.error(str(ex))
		response.ERROR = True
		response.ERROR_MSG = str(ex)
		return response

def _validate_dockerfile(docker_container_repo_path):
	response = Response()
	try:
		data = {}

		dockerfile_path = os.path.join(
			docker_container_repo_path,
			"Dockerfile"
		)

		# Log the filepath we're getting the config from.
		logger.debug("Loading dockerfile at: '%s'" % dockerfile_path)

		# Check if the file exists.
		if not os.path.exists(dockerfile_path):
			raise Exception("Unable to read Dockerfile: '%s' does not exist." %
				dockerfile_path)

		data["DOCKERFILE_PATH"] = docker_container_repo_path

		# Mark the response as valid.
		response.ERROR = False
		response.DATA = data 
		return response
	except Exception as ex:
		logger.error(str(ex))
		response.ERROR = True
		response.ERROR_MSG = str(ex)
		return response

def start_service(docker_container_repo_path="./",
	rs_docker_config_file_name="RS_DOCKER_CONFIG.json"):

	response = Response()
	try:
		data = {}

		rs_docker_config_file_path = os.path.join(
			docker_container_repo_path,
			rs_docker_config_file_name
		)

		rsi = Itterator()

		"""
		Validate Rowsheet Docker Config
		"""

		# CLEANUP__VALIDATE_RS_DOCKER_CONFIG
		rsi.register_process({
			"name": "CLEANUP__VALIDATE_RS_DOCKER_CONFIG",
			"step": LOG_ERROR__VALIDATE_RS_DOCKER_CONFIG,
			"next_process": None,
			"failure_process": True
		})

		# VALIDATE_RS_DOCKER_CONFIG
		rsi.register_process({
			"name": "VALIDATE_RS_DOCKER_CONFIG",
			"step": _validate_rs_docker_config,
			"step_args": {
				# @TODO
				# Test with broken file.
				# "rs_docker_config_file_path": "../tests/CONFIG.json.badfile"
				"rs_docker_config_file_path": rs_docker_config_file_path,
			},
			"start_process": True,
			"next_process": {
				"VALIDATE_DOCKERFILE": {
					"ERROR": False,
				},
				"CLEANUP__VALIDATE_RS_DOCKER_CONFIG": {
					"ERROR": True,
				}
			}
		})

		"""
		Validate Dockerfile
		"""

		# CLEANUP__VALIDATE_DOCKERFILE
		rsi.register_process({
			"name": "CLEANUP__VALIDATE_DOCKERFILE",
			"step": LOG_ERROR__VALIDATE_DOCKERFILE,
			"next_process": None,
			"failure_process": True
		})

		# VALIDATE_DOCKERFILE
		rsi.register_process({
			"name": "VALIDATE_DOCKERFILE",
			"step": _validate_dockerfile,
			"step_args": {
				"docker_container_repo_path": docker_container_repo_path,
			},
			"next_process": {
				"BUILD_DOCKER_IMAGE": {
					"ERROR": False,
				},
				"CLEANUP__VALIDATE_DOCKERFILE": {
					"ERROR": True,
				}
			}
		})

		"""
		Validate Dockerfile
		"""

		# CLEANUP__BUILD_DOCKER_IMAGE
		rsi.register_process({
			"name": "CLEANUP__BUILD_DOCKER_IMAGE",
			"rs_step_cmd": "docker rmi <%image_name%>",
			"rs_step_args": {
				"template_vars": {
					"image_name": {
						"from_step": "VALIDATE_RS_DOCKER_CONFIG",
						"data_key": "IMAGE_NAME",
					},
				}
			},
			"next_process": None,
			"failure_process": True
		})

		"""
		Build Docker Image	
		"""

		# BUILD_DOCKER_IMAGE
		rsi.register_process({
			"name": "BUILD_DOCKER_IMAGE",
			"rs_step_cmd": "docker build -t <%image_name%> <%dockerfile_path%>",
			"rs_step_args": {
				"template_vars": {
					"dockerfile_path": {
						"from_step": "VALIDATE_DOCKERFILE",
						"data_key": "DOCKERFILE_PATH",
					},
					"container_name": {
						"from_step": "VALIDATE_RS_DOCKER_CONFIG",
						"data_key": "CONTAINER_NAME",
					},
					"image_name": {
						"from_step": "VALIDATE_RS_DOCKER_CONFIG",
						"data_key": "IMAGE_NAME",
					},
				}
			},
			"next_process": {
				"START_DOCKER_SERVICE": {
					"ERROR": False,
				},
				"CLEANUP__BUILD_DOCKER_IMAGE": {
					"ERROR": True,
				}
			}
		})

		"""
		Start Docker Service
		"""

		# REMOVE_DOCKER_SERVICE
		rsi.register_process({
			"name": "REMOVE_DOCKER_SERVICE",
			"rs_step_cmd": "docker service rm <%service_name%>",
			"rs_step_args": {
				"template_vars": {
					"service_name": {
						"from_step": "VALIDATE_RS_DOCKER_CONFIG",
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
						"from_step": "VALIDATE_RS_DOCKER_CONFIG",
						"data_key": "HOST_PORT",
					},
					"container_port": {
						"from_step": "VALIDATE_RS_DOCKER_CONFIG",
						"data_key": "CONTAINER_PORT",
					},
					"service_name": {
						"from_step": "VALIDATE_RS_DOCKER_CONFIG",
						"data_key": "SERVICE_NAME",
					},
					"image_name": {
						"from_step": "VALIDATE_RS_DOCKER_CONFIG",
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

		"""
		Finish up.
		"""

		# DONE 
		rsi.register_process({
			"name": "DONE",
			"rs_step_cmd": "echo 'DONE'",
			"rs_step_msg": "DONE",
			"next_process": None
		})

		"""
		Run the itterator. If nothing goes wrong, return the RowSheet docker
		config data as the DATA for response of this procedure.
		"""
		return rsi.run()
	except Exception as ex:
		logger.error(str(ex))
		response.ERROR = True
		response.ERROR_MSG = str(ex)
		return response

#-------------------------------------------------------------------------------
# Unit tests.
#-------------------------------------------------------------------------------
if __name__ == "__main__":
	import os
	install_error = os.system("cd .. && sudo sh install.sh")
	if install_error:
		print("ERROR re-installing rs_utils.")
	else:
		os.system("python3 ../tests/docker.py")
