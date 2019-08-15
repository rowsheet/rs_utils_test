from rs_utils import logger

"""
Interactive tests.
"""
logger.confirm_continue()

"""
Warning tests.
"""
logger.message("message")
logger.warning("warning")
logger.debug("debug")
logger.success("success")
logger.error("error")

"""
Extra Message tests.
"""
logger.message_bold("Example message bold")
logger.message_big([
	"EXAMPLE MESSAGE BIG:",
	"Yo dog wadup"
])
logger.message_big("EXAMPLE MESSAGE BIG: no_array")

"""
Extra Error tests.
"""
logger.error_bold("Example error bold")
logger.error_big([
	"EXAMPLE ERROR BIG:",
	"You fucked up!"
])
logger.error_big("EXAMPLE ERROR BIG: no_array")
logger.error_big([
	'EXAMPLE ERROR BIG:',
	'Some really long error message that will be more than the number of',
	' lines than is in the box space.',
])
logger.error_big([
	"EXAMPLE ERROR BIG:",
	"Some really long error message that will be more than the number of lines than is in the box space."
])

"""
Line tests.
"""
logger.message("message with line 80", line=True)
logger.message("message with line 81", line=True, line_count=81)
logger.message("message with line 82", line=True, line_count=82)
logger.message("message with line 83", line=True, line_count=83)
logger.message("message with line 83 but really long message", line=True, line_count=83)
logger.message("really long message but really short line", line=True, line_count=40)
logger.message("message with line 80 but with = charachters", line=True, line_char="=")
logger.message("message with line 80 but with * charachters", line=True, line_char="*")
logger.message("message with line 80 but with '.-' charachters", line=True, line_char=".-")
logger.message("really long message but really short line and '.-' charachters",
	line=True, line_count=40, line_char=".-")
logger.message("really long message message with line 80 but with '.-' charachters and pad top only",
	line=True, line_char=".-", pad_top=True)
logger.message("message with line 80", line=True)
logger.message("message with line 80 pad top only", line=True, pad_top=True)
logger.message("message with line 80", line=True)
logger.message("message with line 80", line=True)
logger.message("message with line 80 pad both top and bottom", line=True, pad=True)
logger.message("message with line 80", line=True)
logger.message("message with line 80", line=True)
logger.message("message with line 80", line=True)
logger.warning("warning with line 80 pad top only", line=True, pad_top=True)
logger.error("error with line 80", line=True)
logger.error("error with line 80 pad both top and bottom", line=True, pad=True)
logger.success("success with line 80", line=True)
logger.debug("debug with line 80", line=True)
