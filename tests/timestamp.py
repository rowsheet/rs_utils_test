from rs_utils import timestamp
from rs_utils import logger

logger.message("UTC Now: default")
logger.debug(timestamp.now())

logger.message("UTC Now: want='string'")
logger.debug(timestamp.now(want="string"))

logger.message("UTC Now: want='str'")
logger.debug(timestamp.now(want="str"))

logger.message("UTC Now: want='timestamp'")
logger.debug(timestamp.now(want="timestamp"))

logger.message("UTC Now: want='ts'")
logger.debug(timestamp.now(want="ts"))

logger.message("ts_to_str")
ts = timestamp.now(want="ts")
logger.debug(timestamp.ts_to_str(ts))

logger.message("str_to_ts")
ts_str = timestamp.now(want="str")
logger.debug(timestamp.str_to_ts(ts_str))

logger.message("str_to_ts")
ts_str = timestamp.now(want="str")
logger.debug(timestamp.str_to_ts(ts_str))

"""
timestamp.diff_now()
	USING:		string	
	RETURNING:	string
"""

logger.message_big("Testing time-delta from NOW, using 'string', returing 'string'")

ts_str_old = "2019-08-15 08:20:58Z"
logger.message("diff_now: '%s': want='str'" % ts_str_old)
ts_result = timestamp.diff_now(ts_str_old, want="str")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_str_old = "2019-08-14 08:20:58Z"
logger.message("diff_now: '%s': want='str'" % ts_str_old)
ts_result = timestamp.diff_now(ts_str_old, want="str")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_str_old = "2019-07-14 08:20:58Z"
logger.message("diff_now: '%s': want='str'" % ts_str_old)
ts_result = timestamp.diff_now(ts_str_old, want="str")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_str_old = "2018-07-14 08:20:58Z"
logger.message("diff_now: '%s': want='str'" % ts_str_old)
ts_result = timestamp.diff_now(ts_str_old, want="str")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

"""
timestamp.diff_now()
	USING:		string	
	RETURNING:	timestamp	
"""

logger.message_big("Testing time-delta from NOW, using 'string', returing 'timestamp'")

ts_str_old = "2019-08-15 08:20:58Z"
logger.message("diff_now: '%s': want='ts'" % ts_str_old)
ts_result = timestamp.diff_now(ts_str_old, want="ts")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_str_old = "2019-08-14 08:20:58Z"
logger.message("diff_now: '%s': want='ts'" % ts_str_old)
ts_result = timestamp.diff_now(ts_str_old, want="ts")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_str_old = "2019-07-14 08:20:58Z"
logger.message("diff_now: '%s': want='ts'" % ts_str_old)
ts_result = timestamp.diff_now(ts_str_old, want="ts")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_str_old = "2018-07-14 08:20:58Z"
logger.message("diff_now: '%s': want='ts'" % ts_str_old)
ts_result = timestamp.diff_now(ts_str_old, want="ts")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

"""
timestamp.diff_now()
	USING:		timestamp
	RETURNING:	string	
"""

logger.message_big("Testing time-delta from NOW, using 'timestamp', returing 'string'")

ts_old = timestamp.str_to_ts("2019-08-15 08:20:58Z")
logger.message("diff_now: '%s': want='str'" % ts_old)
ts_result = timestamp.diff_now(ts_old, want="str")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_old = timestamp.str_to_ts("2019-08-14 08:20:58Z")
logger.message("diff_now: '%s': want='str'" % ts_old)
ts_result = timestamp.diff_now(ts_old, want="str")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_old = timestamp.str_to_ts("2019-07-14 08:20:58Z")
logger.message("diff_now: '%s': want='str'" % ts_old)
ts_result = timestamp.diff_now(ts_old, want="str")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_old = timestamp.str_to_ts("2018-07-14 08:20:58Z")
logger.message("diff_now: '%s': want='str'" % ts_old)
ts_result = timestamp.diff_now(ts_old, want="str")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

"""
timestamp.diff_now()
	USING:		timestamp
	RETURNING:	timestamp
"""

logger.message_big("Testing time-delta from NOW, using 'timestamp', returing 'timestamp'")

ts_old = timestamp.str_to_ts("2019-08-15 08:20:58Z")
logger.message("diff_now: '%s': want='ts'" % ts_old)
ts_result = timestamp.diff_now(ts_old, want="ts")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_old = timestamp.str_to_ts("2019-08-14 08:20:58Z")
logger.message("diff_now: '%s': want='ts'" % ts_old)
ts_result = timestamp.diff_now(ts_old, want="ts")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_old = timestamp.str_to_ts("2019-07-14 08:20:58Z")
logger.message("diff_now: '%s': want='ts'" % ts_old)
ts_result = timestamp.diff_now(ts_old, want="ts")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_old = timestamp.str_to_ts("2018-07-14 08:20:58Z")
logger.message("diff_now: '%s': want='ts'" % ts_old)
ts_result = timestamp.diff_now(ts_old, want="ts")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

"""
timestamp.diff(first, second)
	USING:		timestamp
	RETURNING:	timestamp
"""

logger.message_big("Testing time-delta from OLD, NEW, using 'timestamp', returing 'timestamp'")

ts_old = timestamp.str_to_ts("2019-08-15 08:20:58Z")
ts_new = timestamp.now(want="ts")
logger.message("diff('%s', '%s'): want='ts'" % (ts_old, ts_new))
ts_result = timestamp.diff(ts_old, ts_new, want="ts")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_old = timestamp.str_to_ts("2019-08-14 08:20:58Z")
ts_new = timestamp.now(want="ts")
logger.message("diff('%s', '%s'): want='ts'" % (ts_old, ts_new))
ts_result = timestamp.diff(ts_old, ts_new, want="ts")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_old = timestamp.str_to_ts("2019-07-14 08:20:58Z")
ts_new = timestamp.now(want="ts")
logger.message("diff('%s', '%s'): want='ts'" % (ts_old, ts_new))
ts_result = timestamp.diff(ts_old, ts_new, want="ts")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_old = timestamp.str_to_ts("2018-07-14 08:20:58Z")
ts_new = timestamp.now(want="ts")
logger.message("diff('%s', '%s'): want='ts'" % (ts_old, ts_new))
ts_result = timestamp.diff(ts_old, ts_new, want="ts")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

"""
timestamp.diff(first, second)
	USING:		timestamp
	RETURNING:	string
"""

logger.message_big("Testing time-delta from OLD, NEW, using 'timestamp', returing 'string'")

ts_old = timestamp.str_to_ts("2019-08-15 08:20:58Z")
ts_new = timestamp.now(want="ts")
logger.message("diff('%s', '%s'): want='str'" % (ts_old, ts_new))
ts_result = timestamp.diff(ts_old, ts_new, want="str")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_old = timestamp.str_to_ts("2019-08-14 08:20:58Z")
ts_new = timestamp.now(want="ts")
logger.message("diff('%s', '%s'): want='str'" % (ts_old, ts_new))
ts_result = timestamp.diff(ts_old, ts_new, want="str")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_old = timestamp.str_to_ts("2019-07-14 08:20:58Z")
ts_new = timestamp.now(want="ts")
logger.message("diff('%s', '%s'): want='str'" % (ts_old, ts_new))
ts_result = timestamp.diff(ts_old, ts_new, want="str")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_old = timestamp.str_to_ts("2018-07-14 08:20:58Z")
ts_new = timestamp.now(want="ts")
logger.message("diff('%s', '%s'): want='str'" % (ts_old, ts_new))
ts_result = timestamp.diff(ts_old, ts_new, want="str")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

"""
timestamp.diff(first, second)
	USING:		string
	RETURNING:	timestamp
"""

logger.message_big("Testing time-delta from OLD, NEW, using 'string', returing 'timestamp'")

ts_old = timestamp.ts_to_str(timestamp.str_to_ts("2019-08-15 08:20:58Z"))
ts_new = timestamp.ts_to_str(timestamp.now(want="ts"))
logger.message("diff('%s', '%s'): want='ts'" % (ts_old, ts_new))
ts_result = timestamp.diff(ts_old, ts_new, want="ts")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_old = timestamp.ts_to_str(timestamp.str_to_ts("2019-08-14 08:20:58Z"))
ts_new = timestamp.ts_to_str(timestamp.now(want="ts"))
logger.message("diff('%s', '%s'): want='ts'" % (ts_old, ts_new))
ts_result = timestamp.diff(ts_old, ts_new, want="ts")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_old = timestamp.ts_to_str(timestamp.str_to_ts("2019-07-14 08:20:58Z"))
ts_new = timestamp.ts_to_str(timestamp.now(want="ts"))
logger.message("diff('%s', '%s'): want='ts'" % (ts_old, ts_new))
ts_result = timestamp.diff(ts_old, ts_new, want="ts")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_old = timestamp.ts_to_str(timestamp.str_to_ts("2018-07-14 08:20:58Z"))
ts_new = timestamp.ts_to_str(timestamp.now(want="ts"))
logger.message("diff('%s', '%s'): want='ts'" % (ts_old, ts_new))
ts_result = timestamp.diff(ts_old, ts_new, want="ts")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

"""
timestamp.diff(first, second)
	USING:		string
	RETURNING:	string
"""

logger.message_big("Testing time-delta from OLD, NEW, using 'string', returing 'string'")

ts_old = timestamp.ts_to_str(timestamp.str_to_ts("2019-08-15 08:20:58Z"))
ts_new = timestamp.ts_to_str(timestamp.now(want="ts"))
logger.message("diff('%s', '%s'): want='str'" % (ts_old, ts_new))
ts_result = timestamp.diff(ts_old, ts_new, want="str")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_old = timestamp.ts_to_str(timestamp.str_to_ts("2019-08-14 08:20:58Z"))
ts_new = timestamp.ts_to_str(timestamp.now(want="ts"))
logger.message("diff('%s', '%s'): want='str'" % (ts_old, ts_new))
ts_result = timestamp.diff(ts_old, ts_new, want="str")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_old = timestamp.ts_to_str(timestamp.str_to_ts("2019-07-14 08:20:58Z"))
ts_new = timestamp.ts_to_str(timestamp.now(want="ts"))
logger.message("diff('%s', '%s'): want='str'" % (ts_old, ts_new))
ts_result = timestamp.diff(ts_old, ts_new, want="str")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)

ts_old = timestamp.ts_to_str(timestamp.str_to_ts("2018-07-14 08:20:58Z"))
ts_new = timestamp.ts_to_str(timestamp.now(want="ts"))
logger.message("diff('%s', '%s'): want='str'" % (ts_old, ts_new))
ts_result = timestamp.diff(ts_old, ts_new, want="str")
logger.debug(ts_result)
logger.warning("\tTYPE: " + type(ts_result).__name__)
