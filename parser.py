import re

f = open('attemptLog','r')
for line in f.xreadlines():
   print line
   date = line.split(' ', 1)[0]
   print date
   time = line.split(' ', )[1]
   print time
   ip_temp =  re.search(',(.+?)]', line.split(' ',)[5])
   ip_temp2 = ip_temp.group(1)
   ip = ip_temp2.split(",",1)[1]
   print ip
   username_temp = line.split(' ',)[8]
   username_temp2 = username_temp.split('[',)[1]
   username = username_temp2.split('/',)[0]
   print username
   password_temp = username_temp2.split('/',)[1]
   password = password_temp.split(']',)[0]
   print password
   result  = line.split(' ', )[9]
   print result
   f2=open('attemptLog.done','a')
   f2.write(line)
   f2.close()
f.close()
