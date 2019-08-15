#!/bin/bash
# Example Service (Auto Cleanup Test)

#-------------------------------------------------------------------------------
# Custom:
#	Enter custom script procedures here.
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Common: Docker entrypoint.
# 	Dail nothing forever so the container doesn't immidiatley exit.
#-------------------------------------------------------------------------------
tail -f /dev/null
