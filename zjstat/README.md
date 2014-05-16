# ZJSTAT


zjstat - Return number of java process matching user's input and send memory stats via zabbix_sender

Zjstat is zabbix probe that checks the number of java process running and optionally, send process JVM details (heap size and perm gen). 

## WHY


By default zabbix offers the proc.num check unfortunately this check is based on the process command line which is not very convinient for java processes. Concerning java process memory monitoring, this requires a JMX interface which is not nécessarely supported by all program or very contraignant to deploy.

zjstat uses only system command, there is nothing to install apart from the java utilities.


### WHAT CAN I DO

#### Number of process running

zjstat default feature is to return the number of java process matching the user input. The process must match the name returned by jps :
```bash
# jps
64422 Elasticsearch
```

In this case the process name is Elasticsearch

zjstat can also return

TODO : Finish readme

Limitation

What is monitored

key

intergration to zabbix

req : sudo + jstat + jps