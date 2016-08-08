# ioc_log_search

This script has been done to look for IOC in a huge number of logs.

**Usage :**

Assuming that /opt/iocdom.txt contains ioc domains and /opt/iocip.txt ioc ip.

Configure parsing:

Please adapt these settings to your log format.

- SPLIT_CHAR = ' ' # separator to split log file
- IP_POS = -4 # position of the IP in the split log array (you can use negative numbers to count from end)
- DOM_POS = 6 # url of the IP in the split log array

Parameters : 

- -l / --log : log file to analyse (text readable format)
OR
- -z / --zlog : Compressed log file (readable with zcat)

- -i / --ipioc : file that contains ioc ip (1 per line)
- -d / --domioc : file that contains ioc domains (1 per line)

ex:

```
/opt/ioc_log_search.py -d /opt/iocdom.txt -i /opt/iocip.txt -z /var/log/logs-20160808.gz
```

or to match multiple files:

```
ls /var/log/logs-*.gz --sshloginfile nodefile /opt/ioc_log_search.py -d /opt/iocdom.txt -i /opt/iocip.txt -z
```

**Parallel search :**

This script can be run with parallel in order to get result faster.

ex : 
```
ls /var/log/logs-*.gz | parallel --sshloginfile nodefile /opt/ioc_log_search.py -d /opt/iocdom.txt -i /opt/iocip.txt -z
```

**External Source :**

http://www.gnu.org/software/parallel/

O. Tange (2011): GNU Parallel - The Command-Line Power Tool,
;login: The USENIX Magazine, February 2011:42-47.
