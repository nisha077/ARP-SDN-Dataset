import os
import subprocess
import sys
import csv

hostname ="10.0.0.1"
targetips = ["10.0.0.2", "10.0.0.3", "10.0.0.4"]

# Executing Command
def run_cmd(cmd):
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        print(str(output))
        return str(output)
        #return subprocess.check_output(cmd, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as ex:
        if ex.returncode == 255:
            raise RuntimeWarning(ex.output.strip())
        raise RuntimeError('cmd execution returned exit status %d:\n%s'
                % (ex.returncode, ex.output.strip()))

def init_csv():
    fname = "rtt_stats.csv"
    writ = csv.writer(open(fname, 'a', buffering=1), delimiter=',')
    header = ["src", "dst", "rtt",]
    writ.writerow(header)
init_csv()
def update_csv(row):
    fname = "rtt_stats.csv"
    writ = csv.writer(open(fname, 'a', buffering=1), delimiter=',')
    writ.writerow(row)

def parse_latency(src, dst, result):
    rttstr = 'rtt min/avg/max/mdev = '
    lenrttstr = len(rttstr)
    index = lenrttstr + result.find(rttstr)
    rtt = result[index:]
    result = rtt.split('/')[0]
    update_csv([src,dst,result])

for targetip in targetips:
	#cmd1 = 'ping -c 1 ' + targetip
	cmd1 = ['ping', '-c', '1', targetip]
	result = run_cmd(cmd1)
	#print("Pinging from hostname ", hostname)
	#print("result",result)
	parse_latency(hostname, targetip,result)
