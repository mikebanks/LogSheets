#!/bin/sh
cd /home/kippo/kippo/
touch all extract attemptLog
> all
> extract

find /home/kippo/kippo/log/ >> all
grep -v "/home/kippo/kippo/log/tty/" all > extract; mv extract all
grep -v "/home/kippo/kippo/log/tty" all > extract; mv extract all
grep -v "/home/kippo/kippo/log/archive/" all > extract; mv extract all
grep -v "/home/kippo/kippo/log/archive" all > extract; mv extract all
grep -Fvxf exclude all > extract

while read -r line
do
        grep -hr "attempt" $line >> attemptLog
	    sudo mv $line /home/kippo/kippo/log/archive/
done < extract
