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

zapache return the number of unique IP that hit your webserver.


TODO README

logtail2 install
template
add module
cron
LogFormat "%h %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-agent}i\"" zabbix

CustomLog logs/ssl_zabbix_evenium_prod_access_log zabbix


PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Apache zabbix probe
* * * * * root /usr/local/scripts/zabbix/zapache.py /var/log/httpd/ssl_zabbix_evenium_prod_access_log
