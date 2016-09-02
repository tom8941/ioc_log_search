# ioc_log_search

This script has been done to look for big number of IOC in a huge number of logs.
It loads in memory the list of IOC and use the python set structure for it's fast search functionalities.

- proxy_ioc_search.py is able to look for ip ioc and domains ioc.
- simple_ioc_search.py takes only an ioc file and do a simple search in the logs without any specific treatments.

## proxy_ioc_search.py

### Usage

Assuming that /opt/iocdom.txt contains ioc domains and /opt/iocip.txt ioc ip.

**Configure parsing:**

Please adapt these settings to your log format.

- SPLIT_CHAR = ' ' # separator to split log file
- IP_POS = -4 # index of the IP in the split log array (you can use negative numbers to count from end)
- DOM_POS = 6 # index of the url in the split log array

**Parameters :**

- -l / --log : log file to analyse (text readable format)
- -z / --zlog : Compressed log file (readable with zcat)
- -i / --ipioc : file that contains ioc ip (1 per line)
- -d / --domioc : file that contains ioc domains (1 per line)

-l and -z are not usable at the same time

ex:
```
/opt/proxy_ioc_search.py -d /opt/iocdom.txt -i /opt/iocip.txt -z /var/log/logs-20160808.gz
```

**Parallel search :**

This script can be run with parallel in order to get result faster.

ex : 
```
ls /var/log/logs-*.gz | parallel --sshloginfile nodefile /opt/proxy_ioc_search.py -d /opt/iocdom.txt -i /opt/iocip.txt -z 
```

##simple_ioc_search.py

### Usage

Assuming that /opt/ioc.txt contains ioc.

**Configure parsing:**

**Parameters :**

- -l / --log : log file to analyse (text readable format)
- -z / --zlog : Compressed log file (readable with zcat)
- -i / --ioc : file that contains ioc (1 per line)
- -s / --split : character to use to split the log
- -p / --position : index of attibute search among the split log

-l and -z are not usable at the same time

ex:

```
/opt/simple_ioc_search.py -i /opt/ioclist.txt -s " " -p -4 -z /var/log/log-20160808
```

**Parallel search :**

This script can be run with parallel in order to get result faster.

ex : 
```
ls /var/log/log-201608* |  parallel --sshloginfile nodefile '/opt/simple_ioc_search.py -i /opt/ioclist.txt -s " " -p -4 -z '
```

## Get data from checkioc project

ex:
```
#Get data from last 10 days
checkioc.py -l 10d -o domain hostname ip-src ip-dst -v > /opt/$(date +%Y%m%d)_ioc

#cut the syslog format to get the ioc
cat /opt/$(date +%Y%m%d)_ioc | grep cs5=OK | grep '|domain\||hostname' | egrep -o 'msg=.* act=' | sed 's/msg=//g' | sed 's/ act=//g' | sort | uniq > /opt/$(date +%Y%m%d)ioc_dom_host.txt

#cut the syslog format to get the ioc
cat /opt/$(date +%Y%m%d)_ioc | grep cs5=OK | grep '|ip-src\||ip-dst' | egrep -o 'msg=(.*) act=' | sed 's/msg=//g' | sed 's/ act=//g' | sort | uniq > /opt/$(date +%Y%m%d)ioc_ip.txt
```

## Performances

Some tests have been done on virtual hosts with proxy_ioc_search.py .
Storage was reaching 5000 IOPS.
log files used are gzip files (200Mb compressed for one file)

```
#of IOC     #of log files      #of core      #of virtual servers    time
164951       1                 1             1                      48sec        ---
164951       468               42            6                      4min39        --- with parallel
164951       5667              42            6                      1H05          --- with parallel
```

## External Source

http://www.gnu.org/software/parallel/

O. Tange (2011): GNU Parallel - The Command-Line Power Tool,
;login: The USENIX Magazine, February 2011:42-47.
