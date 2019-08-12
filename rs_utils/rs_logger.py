from termcolor import cprint
import math

def warning(msg):
	cprint(msg, "yellow")

def error(msg):
	cprint(msg, "red")

def debug(msg):
	cprint(msg, "cyan")

def message(msg,
		line=False,
		line_count=80,
		line_char="-",
		pad_top=False,
		pad_bottom=False,
		pad=False
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
			cprint(line_start[0:line_count], "white", "on_blue")
			cprint(msg, "white", "on_blue")
			cprint(line_end[0:line_count], "white", "on_blue")
			if pad or pad_bottom:
				print("\n")
			return
		start_len = math.floor((line_count - len(msg)) / 2)
		line_start = line_start[0:start_len]
		line_end = line_end[0: line_count - (len(line_start) + len(msg))]
		msg = line_start + msg + line_end
		if pad or pad_top:
			print("\n")
		cprint(msg, "white", "on_blue")
		if pad or pad_bottom:
			print("\n")
		return
	# Print on blue background.
	if pad or pad_top:
		print("\n")
	cprint(msg, "white", "on_blue")
	if pad or pad_bottom:
		print("\n")

def success(msg):
	cprint(msg, "green")

# Unit tests.
if __name__ == "__main__":
	warning("warning")
	error("error")
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
