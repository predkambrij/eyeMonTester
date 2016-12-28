#!/bin/bash
touch /eyeMonTester/logfiles/testlog.txt
touch /eyeMonTester/logfiles/eyemonpy.log

docker run -i --rm --device /dev/tty0 --cap-add SYS_TTY_CONFIG -v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=$DISPLAY -v $DIRPREF/eyeMon:/eyeMon -u developer -v $DIRPREF/eyeMonTester/logfiles/eyemonpy.log:/tmp/eyemonpy.log -v $DIRPREF/eyeMonTester/logfiles/testlog.txt:/tmp/testlog.txt predkambrij/eyemon bash -c "cd eyeMon; $1"
