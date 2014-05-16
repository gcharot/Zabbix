# ZJSTAT


zjstat - Return number of java process matching user's input and send memory stats via zabbix_sender

Zjstat is zabbix probe that checks the number of java process running and optionally sends process JVM details (heap size and perm gen). 

## WHY


By default zabbix offers the proc.num check unfortunately this check is based on the process command line which is not very convinient for java processes. Concerning java process memory monitoring, this requires a JMX interface which is not nécessarely supported by all program or very contraignant to deploy.

zjstat uses only system command, there is nothing to install apart from the java utilities.


### WHAT CAN I DO

#### Number of process running

zjstat default feature is to return the number of java process matching the user input. The process must match the name returned by jps :
```
# jps
64422 Elasticsearch
```

In this case the process name is Elasticsearch

#### Memory stat

zjstat can also return memory statistics :
* HEAP MAX
* HEAP USED
* PERM MAX
* PERM USED

Memory stats are send through zabbix_sender in order to make sure all data are sent in the same time interval.  
If you want to return more stats, you can easily add your own data, see the Customization chapter.


### Requirements

There is no fancy requirements, only core system tools are required :

* Python >= 2.4
* jps
* jstat
* zabbix_sender (only for sending memory stats)

### USAGE

#### Pre-run configuration chek

There is a minimal configuration check required, open the zjstat.py and double check the "USER CONFIGURABLE PARAMETERS" section (line 18), you should ensure the following paths are corect : 
* jps
* jstat
* zabbix_sender (only for sending memory stats)
* zabbix agent configuration file (only for sending memory stats)
* send_to_zabbix : This values defines if memory stats are sent to zabbix through zabbix_sender. A value of 0 will disable zabbix_sender and also print debug output. Very handy for testing. A value > 0 will send stats to zabbix and disable debug output.

#### Command line

Best way to start using zjstats is to use command line.  
```
Usage :  /usr/local/scripts/zabbix/zjstat.py  process_name alive|all
process_name : java process name as seen in jps output
Modes :
        alive : Return number of running processs
        all : Send memory stats as well
```

zjstat requires two arguments, the process name as shown by jps and the mode which defines if you want to return the number of matching processes (alive) or send memory stats as well (all).

"alive" only print the number of process found which is handy for zabbix monitoring, "all" does the same thing but also send memory stat through zabbix_sender.

Let's say you have the following jps output :

```
# jps
64422 Elasticsearch
```

If you want zjstat to return number of elsaticsearch process you would type : 

```
./zjstat.py Elasticsearch alive
1
```

1 is printed as only one Elasticsearch process is running. This value will then be return to zabbix.

In order to avoid output garbage, zjstat silently send memory stats to zabbix; if you want to check the memory features locally you will need to set send_to_zabbix to 0 (see )

### TODO 

Limitation

What is monitored

key

intergration to zabbix

how to zabbix

variable configuration