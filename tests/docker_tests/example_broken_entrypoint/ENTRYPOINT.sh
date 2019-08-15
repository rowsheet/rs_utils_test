#!/bin/bash
# Example Service

#-------------------------------------------------------------------------------
# Custom:
#	Enter custom script procedures here.
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Common: Docker entrypoint.
# 	Dail nothing forever so the container doesn't immidiatley exit.
#-------------------------------------------------------------------------------
# Remove tail -f /dev/null so the container fails and restarts constantly.
# tail -f /dev/null
