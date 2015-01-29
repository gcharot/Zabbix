# ZAPACHE - Monitor Apache traffic

zapache - Return traffic and HTTP requests statistics via zabbix_sender

![alt text](/zapache/images/zapache_screen.png "zapache screen")


## WHAT CAN I DO

### Number of requests

zapache returns the average request per second as well as the number of GET/POST requests.

### Type of request

zapache can be configured to return the number of HTTP requests based on their HTTP status code. 

Defaults are : 
```
"400", "401", "402", "403", "404", "405", "406", "408", "409", "410", "411", "412", "413", "414", "417", "500", "501", "502", "503", "504".
```

### Unique IPs

zapache returns the number of unique IP that hit your webserver.


## Requirements

The following elements are required for zapache to work :

* Python >= 2.6
* logtail2
* zabbix_sender
* Apache Logs in CLF format, the following format is supported :
```
LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\""
```
If different you need to change the code line 57, 71 and 78.

## USAGE

### Pre-run configuration chek

There is a minimal configuration check required, open the zapache.py and double check the "User defined variables" section (line 22), you should ensure the following are correct : 
* path to zabbix_sender
* path to zabbix agent configuration file
* send_to_zabbix : This values defines if stats are sent to zabbix through zabbix_sender. A value of 0 will disable zabbix_sender.
* debug : This values defines if debug ouput is printed. Very handy for testing. A value > 0 will print debug output.
* my_resp_code : This defines which HTTP reponse code stats will be sent to zabbix. Add / remove to fit your needs
* my_req_type : This defines which type of HTTP request will be sent to zabbix. Add / remove to fit your needs. Default is GET & POST
* Add execution permission on apache.py file (at least for user root)

### Command line

Best way to start using zapache is to use command line.  
```
Usage : zapache.py logfile
```

Set debug to 1 and send_to_zabbix to 0 then execute zapache :
```
# ./zapache2.py /var/log/httpd/access_log
Logtailing file  /var/log/httpd/access_log with offset  /tmp/zapache-logtail.offset sending delta to  /tmp/zapache-logtail.data
sending key :  apache[ip_count]  - value :  53
sending key :  apache[nr_req]  - value :  7853
sending key :  apache[GET]  - value :  6403
sending key :  apache[406]  - value :  0
sending key :  apache[405]  - value :  0
sending key :  apache[404]  - value :  15
sending key :  apache[403]  - value :  12
sending key :  apache[402]  - value :  0
sending key :  apache[401]  - value :  0
sending key :  apache[504]  - value :  0
sending key :  apache[502]  - value :  0
sending key :  apache[503]  - value :  0
sending key :  apache[500]  - value :  4
sending key :  apache[501]  - value :  0
sending key :  apache[200]  - value :  7323
sending key :  apache[POST]  - value :  1432
sending key :  apache[409]  - value :  0
sending key :  apache[414]  - value :  0
sending key :  apache[417]  - value :  0
sending key :  apache[410]  - value :  0
sending key :  apache[411]  - value :  0
sending key :  apache[412]  - value :  0
sending key :  apache[413]  - value :  0
sending key :  apache[408]  - value :  0
```

Debug shows what keys/values will be sent to zabbix, as send_to_zabbix is 0 nothing will be sent. Execute the same command again after one minute you should have the delta values.

__CAUTION__ : As zapache is based on logtail, the first execution will parse your entire log !

If everything is fine, reset debug and send_to_zabbix to their original values and proceed with zabbix integration.

## Zabbix integration

### Zabbix Template

Import the [Zabbix template](/zapache/zabbix template/zbx_template_apache.xml), this template includes all default values and is ready to use :

* HTTP total requests per second

* HTTP GET/POST requests per second

* HTTP Status Code :  "400", "401", "402", "403", "404", "405", "406", "408", "409", "410", "411", "412", "413", "414", "417", "500", "501", "502", "503", "504".

* Number of Unique IPs

* Monitoring of Apache process (via proc.num)

* Triggers on Apache process and 500 Status

* Graphs and screen  


Then link the template to the host you want to monitor.

### Cron Job

Final step is to create a cron job to execute zapache every minute :

```
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
# Apache zabbix probe
* * * * * root /usr/local/bin/zapache.py /var/log/httpd/kibana_access_log
```
Adapt the paths to fit you own needs.

### Final check

To check if Zabbix receives the data go to "Monitoring -> Latest Data", choose your host and select the "Apache" application. You should see new values comming every minute.


## I need more stats

If you need more status code / request type, you just need to add your own values in the python lists.  
For example, I want to monitor status code 200 and HEAD requests.

* Add "200" and "HEAD" to the lists :

```python
my_resp_code = ("200", "400", "401", "402", "403", "404", "405", "406", "408", "409", "410", "411", "412", "413", "414", "417", "500", "501", "502", "503", "504")				# Wanted status code.
my_req_type = ("GET", "POST", "HEAD")		
```

* Create the corresponding Zabbix items with the following keys :

```
apache[200]
apache[HEAD]
```
And you're done !

If you have any issue enable debug mode and run zapache manually.

