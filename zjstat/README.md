Stat# ZJSTAT


zjstat - Return number of java process matching user's input and send stats via zabbix_sender

Zjstat is zabbix probe that checks the number of java process running and optionally sends process JVM details (heap size and perm gen) without the need to enable JMX

__Note :__ Zjstat can return JVM details without JMX, however if you can enable JMX __it is preferable to use it as it is much more flexible/efficient__. Zjstat is useful __whenever you can't or don't want to enable JMX__.

![alt text](/zjstat/images/zabbix_java_process_graphs.png  "JVM Stats")

## WHY


By default zabbix offers the proc.num check unfortunately this check is based on the process command line which is not very convinient for java processes. Concerning java process monitoring, this requires a JMX interface which is not necessarily supported by all program or very contraignant to deploy. Again, if you can enable JMX, just use zjstat for process running checks.

zjstat only uses system commands, there is nothing to install apart from the java utilities. No need to modify your java applications.


## WHAT CAN I DO

### Number of process running

zjstat default feature is to return the number of java process matching the user input. The process must match the name returned by jps :
```
# jps
64422 Elasticsearch
```

In this case the process name is "Elasticsearch" (case is important).

### Stat

zjstat can also return statistics :
* HEAP MAX
* HEAP CAPACITY
* HEAP USED
* HEAP NEW MAX
* HEAP NEW CAPACITY
* HEAP NEW USED
* HEAP OLD MAX
* HEAP OLD CAPACITY
* HEAP OLD USED
* OFF-HEAP MAX
* OFF-HEAP CAPACITY
* OFF-HEAP USED
* OFF-HEAP PERM MAX
* OFF-HEAP PERM CAPACITY
* OFF-HEAP PERM USED
* OFF-HEAP META MAX
* OFF-HEAP META CAPACITY
* OFF-HEAP META USED
* OFF-HEAP CCS MAX
* OFF-HEAP CCS CAPACITY
* OFF-HEAP CCS USED

zjstat can also return GC statistics :
* YOUNG GC COUNT
* FULL GC COUNT
* YOUNG GC TIME
* FULL GC TIME

Stats are send through zabbix_sender in order to make sure all data are sent in the same time interval.  
If you want to return more stats, you can easily add your own data, see [I need more stats](#i-need-more-stats) section. However if you need very detailed stats it might be a better idea to use a JMX interface instead.


## Limitations / TODO

* No regular expression, process name __must__ match the name as returned by jps
* If more than one matching java process is found, stats will only be sent for the last process found (last process listed by jps).
* Zabbix support only
* Heap / Off-Heap stats only. See [I need more stats](#i-need-more-stats) section for adding more stats.
* As JAVA_HOME might not be always defined, system commands path are configured statically inside the code

## Requirements

There is no fancy requirements, only core system tools are required :

* Python >= 2.7
* sudo
* jps
* jstat (only for sending stats)
* Java command (to check java version)
* zabbix_sender (only for sending stats)
* Tested with SUN JRE 7 & 8 other version may work.

## USAGE

### Pre-run configuration chek

There is a minimal configuration check required, open the zjstat.py and double check the "USER CONFIGURABLE PARAMETERS" section (line 18), you should ensure the following are correct : 
* Path to jps
* Path to jstat (only for sending stats)
* Path to zabbix_sender (only for sending stats)
* Path to zabbix agent configuration file (only for sending stats)
* send_to_zabbix : This values defines if stats are sent to zabbix through zabbix_sender. A value of 0 will disable zabbix_sender and also print debug output. Very handy for testing. A value > 0 will send stats to zabbix and disable debug output.
* Add execution permission on zjstat.py file (at least for users root and zabbix)

### Command line

Best way to start using zjstat is to use command line.  
```
Usage : zjstat.py  process_name alive|all
process_name : java process name as seen in jps output
Modes :
        alive : Return number of running processs
        all : Send stats as well
```

zjstat requires two arguments, the __process name__ as returned by jps and the __mode__ which defines if you want to return the number of matching processes (alive) or send stats as well (all).

"alive" only prints the number of process found which is handy for zabbix monitoring, "all" does the same thing but also send stat through zabbix_sender.

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

In order to avoid output garbage, zjstat silently sends stats to zabbix; if you want to check the features locally you need to set send_to_zabbix variable to 0 (see [Pre-run configuration chek](#pre-run-configuration-chek) section). Then use the following command line : 

```
# ./zjstat.py Elasticsearch all
Found Java version :  7
Process found : Elasticsearch with pid : 64422
1
There is  1 running process named Elasticsearch
Getting -gc stats for process 64422 with command : sudo /usr/java/default/bin/jstat -gc 64422
Getting -gccapacity stats for process 64422 with command : sudo /usr/java/default/bin/jstat -gccapacity 64422

Dumping collected stat dictionary
-----
{'NGC': '87360.0', 'NGCMN': '87360.0', 'pid': '59156', 'S0U': '0.0', 'EC': '69952.0', 'S1C': '8704.0', 'S1U': '297.5', 'GCT': '29.768', 'nproc': 1, 'EU': '16781.7', 'FGCT': '8.450', 'S0C': '8704.0', 'jpname': 'Elasticsearch', 'NGCMX': '349504.0', 'OGCMN': '174784.0', 'CCSC': '6908.0', 'CCSMX': '1048576.0', 'YGC': '1439', 'YGCT': '21.317', 'MC': '58864.0', 'MCMN': '0.0', 'OC': '174784.0', 'MU': '57197.3', 'OGCMX': '699072.0', 'CCSMN': '0.0', 'CCSU': '6492.3', 'OU': '113223.2', 'MCMX': '1101824.0', 'OGC': '174784.0', 'FGC': '94'} 
-----

Dumping zabbix stat dictionary
-----
{'off_heap_perm_max': 0, 'off_heap_meta_used': 58570035.2, 'young_gc_count': 1439, 'off_heap_perm_used': 0, 'heap_max': 1073741824.0, 'off_heap_ccs_capacity': 7073792.0, 'off_heap_capacity': 67350528.0, 'off_heap_used': 65218150.400000006, 'heap_old_capacity': 178978816.0, 'heap_used': 133429657.6, 'heap_capacity': 268435456.0, 'heap_old_max': 715849728.0, 'heap_new_used': 17489100.8, 'off_heap_ccs_used': 6648115.2, 'off_heap_perm_capacity': 0, 'heap_old_used': 115940556.8, 'off_heap_meta_capacity': 60276736.0, 'heap_new_max': 357892096.0, 'off_heap_max': 2202009600.0, 'off_heap_meta_max': 1128267776.0, 'full_gc_time': 8.45, 'full_gc_count': 94, 'off_heap_ccs_max': 1073741824.0, 'heap_new_capacity': 89456640.0, 'young_gc_time': 21.32} 
-----

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[off_heap_perm_max] -o 0 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[off_heap_meta_used] -o 58570035.2 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[young_gc_count] -o 1439 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[off_heap_perm_used] -o 0 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[heap_max] -o 1073741824.0 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[off_heap_ccs_capacity] -o 7073792.0 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[off_heap_capacity] -o 67350528.0 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[off_heap_used] -o 65218150.4 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[heap_old_capacity] -o 178978816.0 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[heap_used] -o 133429657.6 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[heap_capacity] -o 268435456.0 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[heap_old_max] -o 715849728.0 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[heap_new_used] -o 17489100.8 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[off_heap_ccs_used] -o 6648115.2 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[off_heap_perm_capacity] -o 0 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[heap_old_used] -o 115940556.8 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[off_heap_meta_capacity] -o 60276736.0 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[heap_new_max] -o 357892096.0 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[off_heap_max] -o 2202009600.0 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[off_heap_meta_max] -o 1128267776.0 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[full_gc_time] -o 8.45 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[full_gc_count] -o 94 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[off_heap_ccs_max] -o 1073741824.0 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[heap_new_capacity] -o 89456640.0 

Simulation: the following command would be execucted :
/usr/local/opt/zabbix/bin/zabbix_sender -c /usr/local/etc/zabbix/zabbix_agentd.conf -k custom.proc.java.elasticsearch[young_gc_time] -o 21.32
```

As you can see, setting send_to_zabbix to 0 added debug output, the "all" option also enabled reporting. The output is splitted in 4 sections : 

* The first section shows if process(es) matching user's input are running on the system
* The second section shows the commands used to get statistics
* The third section shows the process collected data (collected stat dictionary) and the values that would be sent to zabbix (zabbix stat dictionary).
* The fourth section shows the zabbix_sender commands that would be executed if sent_to_zabbix > 0


__BE AWARE__ that the "collected stat dictionary" values are in KB (as reported by jstat) and "zabbix stat dictionary" values are in Bytes as it is much simpler to process by Zabbix.  

If you're happy with the result, you can set send_to_zabbix back to 1 and proceed with zabbix integration !


## Zabbix integration

### Principles

zjstat monitoring is splitted in two phases :
* Number of java process running which is retrieved with classical zabbix agent check
* Stats which are sent via zabbix_sender once the number of process is returned.

Stats are send through zabbix_sender in order to make sure all data are sent in the same time interval.

For every process you want to monitor, you need to ask yourself if you want to monitor only the number of process running or send the stats as well. This will decide which zabbix configuration to use.


### Requirements

* User zabbix is able to sudo jps as root without password + "!requiretty" parameter
* User zabbix is able to sudo jstat as root without password + "!requiretty" parameter (stats only)
* Host is able to send data to zabbix through zabbix_serder (zabbix trapper)

### Zabbix agent configuration

First thing to do is to configure zabbix agent so it can be called from the Zabbix server.

Create a /etc/zabbix/zabbix_agentd.d/jstat.conf file and add the following line (assuming zjstat is in /usr/local/bin/) or get the [jstat.conf](/zjstat/zabbix_agentd.d/jstat.conf) file from github:

```
UserParameter=custom.proc.num.java[*],/usr/local/bin/zjstat.py $1 $2
```

You can of course set whatever zabbix key you like, default is "custom.proc.num.java"

Then restart zabbix agent. You can test your configuration from your Zabbix server with the zabbix_get command :
```
$ zabbix_get -s  hostname  -k custom.proc.num.java[Elasticsearch,alive]
1

$ zabbix_get -s  hostname  -k custom.proc.num.java[blablabla,alive]
0
```

From the example above you can see that there is 1 "Elasticsearch" process running and 0 "blablabla" process.

### Zabbix server configuration

For a quick start-up use the sample ElasticSearch [Zabbix template](/zjstat/zabbix template/zbx_template_elastisearch.xml) and adapt it to your needs.

#### Number of process running

To monitor the number of process through Zabbix you need to add a new zabbix item with the following properties :

![alt text](/zjstat/images/zabbix_java_process_item_alive.png  "zjstat item configuration")

You can add this item on a template (recommended) or directly on the host to monitor.

Next thing is to create a trigger based on this item :

![alt text](/zjstat/images/zabbix_java_process_trigger.png  "zjstat trigger configuration")

From now on a high severity alert will be triggered if the number of elasticsearch process is not equal to 1.

### Stats

Stats are sent through zabbix_sender after the number of process have been returned. To enable stats, you need to change the __mode from "alive" to "all"__.

Change the zabbix item defined above so it include the "all" switch :

![alt text](/zjstat/images/zabbix_java_process_item_all.png  "zjstat item configuration")

Do the same thing for the corresponding trigger.  

You then need to add following zabbix trapper items one for each value :
* Heap Used (heap_used)
* Heap Capacity (heap_capacity)
* Heap Max (heap_max)
* Heap New Used (heap_new_used)
* Heap New Capacity (heap_new_capacity)
* Heap New Max (heap_new_max)
* Heap Old Used (heap_old_used)
* Heap Old Capacity (heap_old_capacity)
* Heap Old Max (heap_old_max)
* Off-Heap Used (off_heap_used)
* Off-Heap Capacity (off_heap_capacity)
* Off-Heap Max (off_heap_max)
* Off-Heap Perm Used (off_heap_perm_used)
* Off-Heap Perm Capacity (off_heap_perm_capacity)
* Off-Heap Perm Max (off_heap_perm_max)
* Off-Heap Meta Used (off_heap_meta_used)
* Off-Heap Meta Capacity (off_heap_meta_capacity)
* Off-Heap Meta Max (off_heap_meta_max)
* Off-Heap CCS Used (off_heap_ccs_used)
* Off-Heap CCS Capacity (off_heap_ccs_capacity)
* Off-Heap CCS Max (off_heap_ccs_max)
* Young GC Count (young_gc_count)
* Full GC Count (full_gc_count)
* Young GC Time (young_gc_time)
* Full GC Time (full_gc_time)

This time keys are based on the following convention : 
```
custom.proc.java.processname[metric]
```

For example, the elasticsearch heap used key is :
```
custom.proc.java.elasticsearch[heap_used]
```

__Caution__ : process_name is the process name as returned by jps __without__ capital letters.

At the end your 26 items should look like :

![alt text](/zjstat/images/zabbix_java_process_items.png  "zjstat items list")


Finally you can create graphs and screens (see [Zabbix template](/zjstat/zabbix template/zbx_template_elastisearch.xml)) : 

![alt text](/zjstat/images/zabbix_java_process_graphs.png  "JVM Stats")


## I need more stats

Heap and GC are not enough ? No problem, you can easily add you own stat with minimal knowledge in python !

zjstat gathers values from the jstat command, each time you request stats a python dictionary is created with the values return by :
```
jstat -gc PID
jstat -gccapacity PID
```

The diffent values are explained in the [jstat documentation](http://docs.oracle.com/javase/1.5.0/docs/tooldocs/share/jstat.html). The collected data are put in a python dictionary called "pdict", this dictionary keeps the same keys => value as jstat which means if you need to get the "Total garbage collection time" (GCT), you can access it with :


```python
self.pdict['GCT']
```

This being said, all values sent to zabbix are stored in a different dictionnary called "zdict", if you want to send "Total garbage collection time" to Zabbix you need to add the following line in the "compute_jstats" method.
```python
self.zdict['total_gb_time'] = round(float(self.pdict['GCT']),2)
```

If you want to return Suvivor Space utilization (S0U + S1U) you would add :
```python
self.zdict['survivor_used'] = round(((float(self.pdict['S0U']) + float(self.pdict['S1U'])) * 1024),2)
```

* 1024 is to convert KBytes in Bytes, the round(...,2) is to keep only 2 digits after the comma.

To test your patch, set send_to_zabbix variable to 0 and run zjstat, check the zabbix stat dictionary dump values, you should see your new value and the corresponding zabbix_sender command.

Last thing to do is create a zabbix item to store the data, in the example above we would create two zabbix trapper items with the following keys :

* custom.proc.java.processname[total_gb_time] : for the Total garbage collection time
* custom.proc.java.processname[survivor_used] : for the Suvivor Space utilization

That's all !

