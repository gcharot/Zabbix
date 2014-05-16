# ZJSTAT


zjstat - Return number of java process matching user's input and send memory stats via zabbix_sender

Zjstat is zabbix probe that checks the number of java process running and optionally, send process JVM details (heap size and perm gen). 

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

#### Command line

Best way to start using zjstats is to use command line.


### TODO 

Limitation

What is monitored

key

intergration to zabbix

req : sudo + jstat + jps

how to zabbix

variable configuration