from termcolor import colored, cprint
import math
import re

def _warning(msg):
	cprint(msg, "yellow")

def _error(msg):
	cprint(msg, "red")

def _error_bold(msg):
	print(colored(msg, 'white', 'on_red', attrs=['bold']))

def _debug(msg):
	cprint(msg, "cyan")

def _success(msg):
	cprint(msg, "green")

def _message(msg):
	cprint(msg, "white", "on_blue")

def _message_bold(msg):
	print(colored(msg, attrs=['reverse', 'bold']))

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

def error_bold(msg,
		line=False,
		line_count=80,
		line_char="-",
		pad_top=False,
		pad_bottom=False,
		pad=False
	):
	_print_line(msg, _error_bold, line, line_count, line_char, pad_top, pad_bottom, pad)

def error_big(msg_array):
	error_bold("", line=True, line_char="- ")
	for msg in _fit_msg(msg_array, 80):
		error_bold(msg, line=True, line_char=" ")
	error_bold("", line=True, line_char="- ")

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

def message_bold(msg,
		line=False,
		line_count=80,
		line_char="-",
		pad_top=False,
		pad_bottom=False,
		pad=False
	):
	_print_line(msg, _message_bold, line, line_count, line_char, pad_top, pad_bottom, pad)

def message_big(msg_array):
	message_bold("", line=True, line_char="- ")
	for msg in _fit_msg(msg_array, 80):
		message_bold(msg, line=True, line_char=" ")
	message_bold("", line=True, line_char="- ")

def confirm_continue():
	warning("Continue? [Y/N]")
	response = input("")
	if (response.lower() != "yes") and (response.lower()[0] != "y"):
		raise SystemExit
	return

# Unit tests.
if __name__ == "__main__":
	confirm_continue()
	message_bold("Example message bold")
	message_big([
		"EXAMPLE MESSAGE BIG:",
		"Yo dog wadup"
	])
	warning("warning")
	error("error")
	error_bold("Example error bold")
	error_big([
		"EXAMPLE ERROR BIG:",
		"You fucked up!"
	])
	error_big([
		'EXAMPLE ERROR BIG:',
		'Some really long error message that will be more than the number of',
		' lines than is in the box space.',
	])
	error_big([
		"EXAMPLE ERROR BIG:",
		"Some really long error message that will be more than the number of lines than is in the box space."
	])
	debug("debug")
	success("success")
	message("message")
	message("message with line 80", line=True)
	message("message with line 81", line=True, line_count=81)
	message("message with line 82", line=True, line_count=82)
	message("message with line 83", line=True, line_count=83)
	message("message with line 83 but really long message", line=True, line_count=83)
	message("really long message but really short line", line=True, line_count=40)
	message("message with line 80 but with = charachters", line=True, line_char="=")
	message("message with line 80 but with * charachters", line=True, line_char="*")
	message("message with line 80 but with '.-' charachters", line=True, line_char=".-")
	message("really long message but really short line and '.-' charachters",
		line=True, line_count=40, line_char=".-")
	message("really long message message with line 80 but with '.-' charachters and pad top only",
		line=True, line_char=".-", pad_top=True)
	message("message with line 80", line=True)
	message("message with line 80 pad top only", line=True, pad_top=True)
	message("message with line 80", line=True)
	message("message with line 80", line=True)
	message("message with line 80 pad both top and bottom", line=True, pad=True)
	message("message with line 80", line=True)
	message("message with line 80", line=True)
	message("message with line 80", line=True)
	warning("warning with line 80 pad top only", line=True, pad_top=True)
	error("error with line 80", line=True)
	error("error with line 80 pad both top and bottom", line=True, pad=True)
	success("success with line 80", line=True)
	debug("debug with line 80", line=True)
