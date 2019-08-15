from termcolor import colored, cprint
import math
import re

"""
Message formatting.
"""

# Normal formatting.

def _warning(msg):
	cprint(msg, "yellow")

def _error(msg):
	cprint(msg, "red")

def _debug(msg):
	cprint(msg, "blue")

def _success(msg):
	cprint(msg, "green")

def _message(msg):
	cprint(msg, "white", "on_blue")

# Bold formatting.

def _error_bold(msg):
	print(colored(msg, 'white', 'on_red', attrs=['bold']))

def _message_bold(msg):
	print(colored(msg, attrs=['reverse', 'bold']))

# Logging utils.

def _fit_msg(msg_array, size):
	size -= 10
	all_messages = []
	for msg in msg_array:
		if (len(msg) > size):
			chunks = [msg[y-size:y] for y in range(size, len(msg)+size,size)]
			for chunk in chunks:
				all_messages.append(chunk)
		else:
			all_messages.append(msg)
	return all_messages 

def _print_line(msg,
		print_method,
		line=False,
		line_count=80,
		line_char="-",
		pad_top=False,
		pad_bottom=False,
		pad=False,
	):
	# Check if we should print the message in a line.
	if line == True:
		# Pad the message.
		msg = " " + msg + " "
		line_start = ""
		line_end = ""
		for i in range(line_count):
			line_start += line_char
			line_end += line_char
		# If the message is larger than the line_count, just
		# print the message on a separate line.
		if len(msg) >= line_count:
			if pad or pad_top:
				print("\n")
			print_method(line_start[0:line_count])
			print_method(msg)
			print_method(line_end[0:line_count])
			if pad or pad_bottom:
				print("\n")
			return
		start_len = math.floor((line_count - len(msg)) / 2)
		line_start = line_start[0:start_len]
		line_end = line_end[0: line_count - (len(line_start) + len(msg))]
		msg = line_start + msg + line_end
		if pad or pad_top:
			print("\n")
		print_method(msg)
		if pad or pad_bottom:
			print("\n")
		return
	# Print on blue background.
	if pad or pad_top:
		print("\n")
	print_method(msg)
	if pad or pad_bottom:
		print("\n")

def _log_big(messages, logging_function):
	logging_function("", line=True, line_char="- ")
	"""
	Messages may be either:
		1) A list of strings of messages.
		2) A single message.
	If it's not an array. Assume it's a string.
	"""
	if type(messages).__name__ == "list":
		for msg in _fit_msg(messages, 80):
			logging_function(msg, line=True, line_char=" ")
	else:
		msg = messages # Assume it's a string.
		logging_function(msg, line=True, line_char=" ")
	logging_function("", line=True, line_char="- ")

"""
Standard logging.
"""

def warning(msg,
		line=False,
		line_count=80,
		line_char="-",
		pad_top=False,
		pad_bottom=False,
		pad=False
	):
	_print_line(msg, _warning, line, line_count, line_char, pad_top, pad_bottom, pad)

def error(msg,
		line=False,
		line_count=80,
		line_char="-",
		pad_top=False,
		pad_bottom=False,
		pad=False
	):
	_print_line(msg, _error, line, line_count, line_char, pad_top, pad_bottom, pad)

def debug(msg,
		line=False,
		line_count=80,
		line_char="-",
		pad_top=False,
		pad_bottom=False,
		pad=False
	):
	_print_line(msg, _debug, line, line_count, line_char, pad_top, pad_bottom, pad)

def success(msg,
		line=False,
		line_count=80,
		line_char="-",
		pad_top=False,
		pad_bottom=False,
		pad=False
	):
	_print_line(msg, _success, line, line_count, line_char, pad_top, pad_bottom, pad)

def message(msg,
		line=False,
		line_count=80,
		line_char="-",
		pad_top=False,
		pad_bottom=False,
		pad=False
	):
	_print_line(msg, _message, line, line_count, line_char, pad_top, pad_bottom, pad)

"""
Bold logging.
"""

def error_bold(msg,
		line=False,
		line_count=80,
		line_char="-",
		pad_top=False,
		pad_bottom=False,
		pad=False
	):
	_print_line(msg, _error_bold, line, line_count, line_char, pad_top, pad_bottom, pad)

def message_bold(msg,
		line=False,
		line_count=80,
		line_char="-",
		pad_top=False,
		pad_bottom=False,
		pad=False
	):
	_print_line(msg, _message_bold, line, line_count, line_char, pad_top, pad_bottom, pad)

"""
Big logging.
"""

def error_big(msg_array):
	_log_big(msg_array, error_bold)

def message_big(msg_array):
	_log_big(msg_array, message_bold)

"""
Interactive.
"""

def confirm_continue():
	warning("Continue? [Y/N]")
	response = input("")
	if (response.lower() != "yes") and (response.lower()[0] != "y"):
		raise SystemExit
	return

#-------------------------------------------------------------------------------
# Unit tests.
#-------------------------------------------------------------------------------
if __name__ == "__main__":
	import os
	install_error = os.system("cd .. && sudo sh install.sh")
	if install_error:
		print("ERROR re-installing rs_utils.")
	else:
		os.system("python3 ../tests/logger.py")
