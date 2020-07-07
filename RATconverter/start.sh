#!/bin/sh
RUNDIR=$(dirname $0)
echo $RUNDIR

eval "python $RUNDIR/ratConvert.py"

#chmod +rx pw_RATconverter.sh
