from rs_utils import rs_logger

rs_logger.confirm_continue()
rs_logger.message_bold("Example message bold")
rs_logger.message_big([
	"EXAMPLE MESSAGE BIG:",
	"Yo dog wadup"
])
rs_logger.warning("warning")
rs_logger.error("error")
rs_logger.error_bold("Example error bold")
rs_logger.error_big([
	"EXAMPLE ERROR BIG:",
	"You fucked up!"
])
rs_logger.error_big([
	'EXAMPLE ERROR BIG:',
	'Some really long error message that will be more than the number of',
	' lines than is in the box space.',
])
rs_logger.error_big([
	"EXAMPLE ERROR BIG:",
	"Some really long error message that will be more than the number of lines than is in the box space."
])
rs_logger.debug("debug")
rs_logger.success("success")
rs_logger.message("message")
rs_logger.message("message with line 80", line=True)
rs_logger.message("message with line 81", line=True, line_count=81)
rs_logger.message("message with line 82", line=True, line_count=82)
rs_logger.message("message with line 83", line=True, line_count=83)
rs_logger.message("message with line 83 but really long message", line=True, line_count=83)
rs_logger.message("really long message but really short line", line=True, line_count=40)
rs_logger.message("message with line 80 but with = charachters", line=True, line_char="=")
rs_logger.message("message with line 80 but with * charachters", line=True, line_char="*")
rs_logger.message("message with line 80 but with '.-' charachters", line=True, line_char=".-")
rs_logger.message("really long message but really short line and '.-' charachters",
	line=True, line_count=40, line_char=".-")
rs_logger.message("really long message message with line 80 but with '.-' charachters and pad top only",
	line=True, line_char=".-", pad_top=True)
rs_logger.message("message with line 80", line=True)
rs_logger.message("message with line 80 pad top only", line=True, pad_top=True)
rs_logger.message("message with line 80", line=True)
rs_logger.message("message with line 80", line=True)
rs_logger.message("message with line 80 pad both top and bottom", line=True, pad=True)
rs_logger.message("message with line 80", line=True)
rs_logger.message("message with line 80", line=True)
rs_logger.message("message with line 80", line=True)
rs_logger.warning("warning with line 80 pad top only", line=True, pad_top=True)
rs_logger.error("error with line 80", line=True)
rs_logger.error("error with line 80 pad both top and bottom", line=True, pad=True)
rs_logger.success("success with line 80", line=True)
rs_logger.debug("debug with line 80", line=True)
