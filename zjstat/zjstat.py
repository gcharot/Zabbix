#!/usr/bin/python

""" Return number of java process matching user's input and send memory stats via zabbix_sender """

import subprocess
import sys
import os
import re

__author__ = "Gregory Charot"
__copyright__ = "Copyright 2014, Gregory Charot"
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Gregory Charot"
__email__ = "gregory.charot@gmail.com"
__status__ = "Production"


### USER CONFIGURABLE PARAMETERS

# As JAVA_HOME might not be defined - Configure paths to jps and jstat below
jps = '/usr/java/default/bin/jps'
jstat = '/usr/java/default/bin/jstat'

# Zabbix parameters
zabbix_key = 'custom.proc.java'						# Zabbix key root - Full key is zabbix_key.process_name[metric]
zabbix_sender = "/usr/bin/zabbix_sender"			# Path to zabbix_sender binary
zabbix_conf = "/etc/zabbix/zabbix_agentd.conf"		# Path to Zabbix agent configuration
send_to_zabbix = 1									# Send data to zabbix ? > 0 is yes / 0 is No + debug output. Used for memory stats only

### End of user configurable variable

def usage():
	"""Display program usage"""

	print "\nUsage : ", sys.argv[0], " process_name alive|all"
	print "process_name : java process name as seen in jps output"
	print "Modes : \n\talive : Return number of running processs\n\tall : Send memory stats as well"
	sys.exit(1)


class Jprocess:
	"""Check java process presence and get memory stats"""

	def __init__(self, arg):
		"""Initialize default values"""

		self.pdict = {		# Java process dictonary, put all process info inside
		"jpname": arg, 		# Process name as seen in jps output
		"nproc": 0,			# Number of process found - default is 0
		}

		self.zdict = {		# Contains only data that will be sent to Zabbix
	    "heap_new_used" : 0,
		"heap_new_capacity" : 0,
		"heap_new_max" : 0,
		"heap_old_used" : 0,
		"heap_old_capacity" : 0,
		"heap_old_max" : 0,
		"heap_used" : 0,
		"heap_capacity" : 0,
		"heap_max" : 0,
		"off_heap_perm_used" : 0,
		"off_heap_perm_capacity" : 0,
		"off_heap_perm_max" : 0,
		"off_heap_meta_used" : 0,
		"off_heap_meta_capacity" : 0,
		"off_heap_meta_max" : 0,
		"off_heap_ccs_used" : 0,
		"off_heap_ccs_capacity" : 0,
		"off_heap_ccs_max" : 0,
		"off_heap_used" : 0,
		"off_heap_capacity" : 0,
		"off_heap_max" : 0,
		}

		

	def chk_proc(self):
		"""Check if java process is running / Get its PID"""

# Get jps output
		jpsout = subprocess.Popen(['sudo', jps], stdout=subprocess.PIPE)

# Parse every lines
		for line in jpsout.stdout:
			line = line.rstrip('\n')
			pid, name = line.split(' ',1)
# If name matches user's input, record PID and increment nproc
			if name == self.pdict['jpname']:
				self.pdict['pid'] = pid
				if send_to_zabbix == 0: print "Process found :", name, "with pid :", self.pdict['pid']
				self.pdict['nproc'] += 1

	def get_jstats(self):
		"""Check if java process is running"""

# Do nothing if no process were found - Default values are 0		
		if self.pdict['nproc'] == 0:
			return False
# Get gc and gccapacity from jstat and put them in pdict dictionary		
		self.pdict.update(self.fill_jstats("-gc"))
		self.pdict.update(self.fill_jstats("-gccapacity"))

		if send_to_zabbix == 0: print "\nDumping collected stat dictionary\n-----\n", self.pdict, "\n-----\n"
		


	def fill_jstats(self, opts):
		"""Return a dictionary with jstat values"""

		if send_to_zabbix == 0: print "Getting", opts, "stats for process", self.pdict['pid'], "with command : sudo", jstat, opts, self.pdict['pid']
# Get jstat output
		jstatout = subprocess.Popen(['sudo', jstat, opts, self.pdict['pid']], stdout=subprocess.PIPE)
		stdout, stderr = jstatout.communicate()
# Build dictionary
		legend, data = stdout.split('\n',1)
		mydict = dict(zip(legend.split(), data.split()))

		return mydict

	def compute_jstats(self):
		"""Compute stats not given directly by jstat"""

# Do nothing if no process were found - Default values are 0
		if self.pdict['nproc'] == 0:
			return False

# Compute off-heap size used/capacity/max = Perm + Meta + CCS
	# JAVA 8 uses MU & MCMX for metaspace
		if java_version >= '8':
			self.zdict['off_heap_meta_used'] = round(float(self.pdict['MU']) * 1024,2)
			self.zdict['off_heap_meta_capacity'] = round(float(self.pdict['MC']) * 1024,2)
			self.zdict['off_heap_meta_max'] = round(float(self.pdict['MCMX']) * 1024,2)
			self.zdict['off_heap_ccs_used'] = round(float(self.pdict['CCSU']) * 1024,2)
			self.zdict['off_heap_ccs_capacity'] = round(float(self.pdict['CCSC']) * 1024,2)
			self.zdict['off_heap_ccs_max'] = round(float(self.pdict['CCSMX']) * 1024,2)
	# Prior Java 8 it was PU & PGCMX		
		else:
			self.zdict['off_heap_perm_used'] = round(float(self.pdict['PU']) * 1024,2)
			self.zdict['off_heap_perm_max'] = round(float(self.pdict['PGCMX']) * 1024,2)
	# Off-heap size = Perm + Meta + CCS
		self.zdict['off_heap_used'] = self.zdict['off_heap_perm_used'] + self.zdict['off_heap_meta_used'] + self.zdict['off_heap_ccs_used']
		self.zdict['off_heap_capacity'] = self.zdict['off_heap_perm_capacity'] + self.zdict['off_heap_meta_capacity'] + self.zdict['off_heap_ccs_capacity']
		self.zdict['off_heap_max'] = self.zdict['off_heap_perm_max'] + self.zdict['off_heap_meta_max'] + self.zdict['off_heap_ccs_max']

# Compute heap size used/capacity/max = Eden + Survivor + Old space
		self.zdict['heap_new_used'] = round((float(self.pdict['EU']) + float(self.pdict['S0U']) + float(self.pdict['S1U'])) * 1024,2)
		self.zdict['heap_new_capacity'] = round(float(self.pdict['NGC']) * 1024,2)
		self.zdict['heap_new_max'] = round(float(self.pdict['NGCMX']) * 1024,2)
		self.zdict['heap_old_used'] = round(float(self.pdict['OU']) * 1024,2)
		self.zdict['heap_old_capacity'] = round(float(self.pdict['OGC']) * 1024,2)
		self.zdict['heap_old_max'] = round(float(self.pdict['OGCMX']) * 1024,2)
		self.zdict['heap_used'] = self.zdict['heap_new_used'] + self.zdict['heap_old_used']
		self.zdict['heap_capacity'] = self.zdict['heap_new_capacity'] + self.zdict['heap_old_capacity']
		self.zdict['heap_max'] = self.zdict['heap_new_max'] + self.zdict['heap_old_max']

		if send_to_zabbix == 0: print "Dumping zabbix stat dictionary\n-----\n", self.zdict, "\n-----\n"


	def send_to_zabbix(self, metric):
		"""Send stat to zabbix via zabbix_sender"""

# Generate zabbix key => zabbix_key.process_name[metric]
		key = zabbix_key  + '.' + self.pdict['jpname'].lower() + "[" + metric + "]"

# Call zabbix_sender if send_to_zabbix > 0
		if send_to_zabbix > 0:
		 	try:
		   		subprocess.call([zabbix_sender, "-c", zabbix_conf, "-k", key, "-o", str(self.zdict[metric])], stdout=FNULL, stderr=FNULL, shell=False)		# Call zabbix_sender
		 	except OSError, detail:
   				print "Something went wrong while exectuting zabbix_sender : ", detail
   		else:
   			print "Simulation: the following command would be execucted :\n", zabbix_sender, "-c", zabbix_conf, "-k", key, "-o", str(self.zdict[metric]), "\n"



def check_java_version():
	""" Check JVM version in order to get the proper stats """
# Exec java -version
	jd = subprocess.check_output(["java", "-version"],
		stderr=subprocess.STDOUT)

	match = re.search('version \"\d\.(\d)\.', jd)

	java_version = match.group(1)

# Check we did received a proper value
	try: 
		int(java_version)
		if send_to_zabbix == 0: print "Found Java version : ", java_version
		return java_version
	except ValueError:
		print "Unable to found Java version, check your java installation, value found was :", java_version
		sys.exit(1)


# List of accepted mode --- alive : Return number of running process - all : Send mem stats as well

accepted_modes = ['alive', 'all']

# Check/initialize user input args

if len(sys.argv) == 3 and sys.argv[2] in accepted_modes:
	procname = sys.argv[1]
	mode = sys.argv[2]
else:
	usage()

# Get running Java version
java_version = check_java_version()

# Check if process is running / Get PID
jproc = Jprocess(procname) 
jproc.chk_proc()

# Print number of process found so zabbix get the value as it is an active check,
print jproc.pdict["nproc"]
if send_to_zabbix == 0: print "There is ", jproc.pdict['nproc'], "running process named", jproc.pdict['jpname']

# If mode is all & process is found - Get memory stats and send them to zabbix.
if mode == "all" and jproc.pdict['nproc'] != 0:
	jproc.get_jstats()					# Get values from jstat
	jproc.compute_jstats()				# Compute stats that will be sent to zabbix
	FNULL = open(os.devnull, 'w')		# Open devnull to redirect zabbix_sender output
	for key in jproc.zdict:
		jproc.send_to_zabbix(key)		# Send data to zabbix via zabbix_sender
	FNULL.close()

