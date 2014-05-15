ZJSTAT
============

zjstat - Return number of java process matching user's input and send memory stats via zabbix_sender

Zjstat is zabbix probe that checks the number of java process running and optionally, send process JVM details (heap size and perm gen). 

WHY
------------

By default zabbix offers the proc.num check unfortunately this check is based on the process command line which is not appropriate for java processes.


TODO : Finish readme