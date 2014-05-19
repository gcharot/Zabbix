# ZJSTAT


zjstat - Return number of java process matching user's input and send memory stats via zabbix_sender

Zjstat is zabbix probe that checks the number of java process running and optionally sends process JVM details (heap size and perm gen). 

## WHY


By default zabbix offers the proc.num check unfortunately this check is based on the process command line which is not very convinient for java processes. Concerning java process memory monitoring, this requires a JMX interface which is not necessarily supported by all program or very contraignant to deploy.

zjstat uses only system commands, there is nothing to install apart from the java utilities.


## WHAT CAN I DO

### Number of process running

zjstat default feature is to return the number of java process matching the user input. The process must match the name returned by jps :
```
# jps
64422 Elasticsearch
```

In this case the process name is Elasticsearch

### Memory stat

zjstat can also return memory statistics :
* HEAP MAX
* HEAP USED
* PERM MAX
* PERM USED

Memory stats are send through zabbix_sender in order to make sure all data are sent in the same time interval.  
If you want to return more stats, you can easily add your own data, see the Customization chapter.


## Requirements

There is no fancy requirements, only core system tools are required :

* Python >= 2.4
* jps
* jstat
* zabbix_sender (only for sending memory stats)

## USAGE

### Pre-run configuration chek

There is a minimal configuration check required, open the zjstat.py and double check the "USER CONFIGURABLE PARAMETERS" section (line 18), you should ensure the following paths are correct : 
* jps
* jstat
* zabbix_sender (only for sending memory stats)
* zabbix agent configuration file (only for sending memory stats)
* send_to_zabbix : This values defines if memory stats are sent to zabbix through zabbix_sender. A value of 0 will disable zabbix_sender and also print debug output. Very handy for testing. A value > 0 will send stats to zabbix and disable debug output.
* Add execution permission (at least for user root and zabbix)

### Command line

Best way to start using zjstats is to use command line.  
```
Usage : zjstat.py  process_name alive|all
process_name : java process name as seen in jps output
Modes :
        alive : Return number of running processs
        all : Send memory stats as well
```

zjstat requires two arguments, the __process name__ as shown by jps and the __mode__ which defines if you want to return the number of matching processes (alive) or send memory stats as well (all).

"alive" only prints the number of process found which is handy for zabbix monitoring, "all" does the same thing but also send memory stat through zabbix_sender.

Let's say you have the following jps output :

```
# jps
64422 Elasticsearch
```

If you want zjstat to return number of elsaticsearch process you would type : 

```
# ./zjstat.py Elasticsearch alive
1
```

"1" is printed as only one Elasticsearch process is running. This value will then be return to zabbix.

In order to avoid output garbage, zjstat silently send memory stats to zabbix; if you want to check the memory features locally you will need to set send_to_zabbix variable to 0 (see "Pre-run configuration chek" section). Then use the following command line : 

```
# ./zjstat.py Elasticsearch all
Process found : Elasticsearch with pid : 64422
1
There is  1 running process named Elasticsearch
Getting -gc stats for process 64422 with command : sudo /usr/java/default/bin/jstat -gc 64422
Getting -gccapacity stats for process 64422 with command : sudo /usr/java/default/bin/jstat -gccapacity 64422

Dumping collected stat dictionary
-----
{'NGC': '1107520.0', 'NGCMN': '1107520.0', 'pid': '64422', 'S0U': '0.0', 'EC': '886080.0', 'S1C': '110720.0', 'S1U': '30084.9', 'GCT': '54.874', 'nproc': 1, 'EU': '231343.5', 'FGCT': '0.000', 'S0C': '110720.0', 'jpname': 'Elasticsearch', 'NGCMX': '1107520.0', 'OGCMN': '15669696.0', 'PGCMX': '262144.0', 'YGC': '1399', 'YGCT': '54.874', 'PU': '38273.9', 'PGC': '38336.0', 'OC': '15669696.0', 'PC': '38336.0', 'OGCMX': '15669696.0', 'PGCMN': '21248.0', 'OU': '10927194.0', 'OGC': '15669696.0', 'FGC': '0'}
-----

Dumping zabbix stat dictionary
-----
{'perm_max': 268435456.0, 'heap_max': 17179869184.0, 'perm_used': 39192473.600000001, 'heap_used': 11426342400.0}
-----

Simulation: the following command would be execucted :
/usr/bin/zabbix_sender -c /etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[perm_max] -o 268435456.0

Simulation: the following command would be execucted :
/usr/bin/zabbix_sender -c /etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[heap_max] -o 17179869184.0

Simulation: the following command would be execucted :
/usr/bin/zabbix_sender -c /etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[perm_used] -o 39192473.6

Simulation: the following command would be execucted :
/usr/bin/zabbix_sender -c /etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[heap_used] -o 11426342400.0
```

As you can see, setting send_to_zabbix to 0 added debug output, the "all" option also enabled memory reporting. The output is splitted in 4 sections : 

* The first section shows if process(es) matching user input are running on the system
* The second section shows the commands used to get memory statistics
* The third section shows the process collected data (collected stat dictionary) and the values that would be sent to zabbix (zabbix stat dictionary).
* The fourth section shows the zabbix_sender commands that would be executed if sent_to_zabbix > 0


__BE AWARE__ that the "collected stat dictionary" values are in KB (as reported by jstat) and "zabbix stat dictionary" values are in Bytes as it is much simpler to process by Zabbix.  

If you're happy with the result, you can set send_to_zabbix back to 1 and proceed with zabbix integration !


## Zabbix integration

### Principles

zjstat monitoring is splitted in two phases :
* Number of java process running which is retrieve with classical zabbix agent check
* Memory stats which are sent via zabbix_sender once the number of process are returned.

Memory stats are send through zabbix_sender in order to make sure all data are sent in the same time interval.

For every process you would like to monitor, you need to ask yourself if you want to monitor only the number of process running or send the memory stats as well. This will decide which zabbix configuration to use.


### Requirements

* User zabbix is able to sudo jps as root without password
* User zabbix is able to sudo jstat as root without password (memory stats only)
* Host is able to send data to zabbix through zabbix_serder (zabbix trapper)

### Zabbix agent configuration

First thing to do is to configure zabbix agent so it can be called from zabbix server.

Create a /etc/zabbix/zabbix_agentd.d/jstat.conf file and add the following line (assuming zjstat is in /usr/local/bin/) or get the [jstat.conf](/zjstat/zabbix_agentd.d/jstat.conf) file from github:

```
UserParameter=custom.proc.num.java[*],/usr/local/bin/zjstat.py $1 $2
```

You can of course set whatever zabbix key you like, default is "custom.proc.num.java"

Then restart zabbix agent. You can test your configuration from your zabbix server with the zabbix_get command :
```
$ zabbix_get -s  hostname  -k custom.proc.num.java[Elasticsearch,alive]
1

$ zabbix_get -s  hostname  -k custom.proc.num.java[blablabla,alive]
0
```

From the example above you can see that there is 1 "Elasticsearch" process running and 0 "blablabla" process.

### Zabbix server configuration

For a quick start-up use the ElasticSearch [Zabbix template](/zjstat/zabbix template/zbx_template_elastisearch.xml) and adapt it to your needs.

#### Number of process running

To monitor the number of process through Zabbix you need to add a new zabbix item with the following properties :

![alt text](/zjstat/images/zabbix_java_process_item_alive.png  "zjstat item configuration")

You can add this item on a template (recommended) or directly on the host to monitor.

Next thing is to create a trigger based on this item :

![alt text](/zjstat/images/zabbix_java_process_trigger.png  "zjstat trigger configuration")

From now on a high severity alert will be triggered if the number of elasticsearch process is not equal to 1.

### Memory

Memory stats are sent through zabbix_sender after the number of process have been returned. You also need to change the __mode from alive to all__

Change the zabbix item defined above so it include the "all" switch :

![alt text](/zjstat/images/zabbix_java_process_item_all.png  "zjstat item configuration")


## TODO 

Limitation


key

intergration to zabbix

how to zabbix

variable configuration