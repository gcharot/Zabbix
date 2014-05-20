# ZAPACHE - Monitor Apache traffic

zapache - Return traffic and HTTP requests statistics via zabbix_sender

![alt text](/zapache/images/zapache_screen.png "zjstat item configuration")


## WHAT CAN I DO

### Number of requests

zapache returns the average request per second as well as the number of GET/PUT requests.

### Type of request

zapache can be configured to return the number of http request based on their HTTP status code. 

Defaults are : "200", "401", "402", "403", "404", "405", "406", "408", "409", "410", "411", "412", "413", "414", "417", "500", "501", "502", "503", "504".

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

There is a minimal configuration check required, open the zapache.py and double check the "User defined variables" section (line 22), you should ensure the following paths are correct : 
* zabbix_sender
* zabbix agent configuration file
* send_to_zabbix : This values defines if memory stats are sent to zabbix through zabbix_sender. A value of 0 will disable zabbix_sender.
* debug : This values defines if debug ouput is printed. Very handy for testing. A value > 0 will print debug output.
* Add execution permission on apache.py file (at least for user root)
* my_resp_code : This defines which HTTP reponse code stats will be sent to zabbix. Add / remove to fit your needs
* my_req_type : This defines which type of request will be sent to zabbix. Add / remove to fit your needs. Default is GET & POST

### Command line

Best way to start using zapache is to use command line.  



TODO README

template
add module
cron
LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"" zabbix

CustomLog logs/ssl_zabbix_evenium_prod_access_log zabbix


PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Apache zabbix probe
* * * * * root /usr/local/scripts/zabbix/zapache.py /var/log/httpd/ssl_zabbix_evenium_prod_access_log