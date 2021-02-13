#!/bin/sh

FILE=/var/opt/app-root/src/data/sticky_user_ps
cp /usr/bin/ps $FILE  # Use ps executable as test
chmod u+s $FILE       # Runs as the user that runs this
chmod g+x $FILE       # Runnable by the user group (FSGroup)
