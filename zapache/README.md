# ZAPACHE - Monitor Apache traffic

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
