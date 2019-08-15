from datetime import datetime

RS_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%SZ"

def ts_to_str(timestamp):
	return timestamp.strftime(RS_TIMESTAMP_FORMAT)

def str_to_ts(timestamp):
	return datetime.strptime(timestamp, RS_TIMESTAMP_FORMAT)

def _check_want_string(type):
	if type == "string" or type == "str":
		return True
	elif type == "timestamp" or type == "ts":
		return False
	else:
		raise Exception("Invalid timestamp.now() option, type must be "
			+ "either 'string', 'str', 'timestamp', or 'ts'.")

def now(want="string"):
	now = datetime.utcnow()
	want_string = _check_want_string(want)
	if want_string == True:
		return ts_to_str(now)
	else:
		return now

def _always_ts(ts_or_str):
	if type(ts_or_str).__name__ == "str":
		return str_to_ts(ts_or_str)
	elif type(ts_or_str).__name__ == "datetime":
		return ts_or_str
	else:
		raise Exception("Invalid timestamp.now() option, type must be "
			+ "either 'string', 'str', 'timestamp', or 'ts'.")

def diff_now(old, want="string"):
	if type(old).__name__ == "str":
		old = str_to_ts(old)
	_now = now(want="ts")
	diff = _now - old
	want_string = _check_want_string(want)
	if want_string == True:
		return str(diff)
	else:
		return diff

def diff(old, new, want="string"):
	old = _always_ts(old)
	new = _always_ts(new)
	diff = new - old
	want_string = _check_want_string(want)
	if want_string == True:
		return str(diff)
	else:
		return diff
	

#-------------------------------------------------------------------------------
# Unit tests.
#-------------------------------------------------------------------------------
if __name__ == "__main__":
	import os
	install_error = os.system("cd .. && sudo sh install.sh")
	if install_error:
		print("ERROR re-installing rs_utils.")
	else:
		os.system("python3 ../tests/timestamp.py")
