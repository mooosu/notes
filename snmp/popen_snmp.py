# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

import subprocess
import sys
import select
from snmp_parser import SnmpAnalyser

def read_snmp(hostname = "localhost",community="public"):
    pipe = subprocess.Popen(
        ["snmpbulkwalk","-Oq", "-v", "2c", "-c", community, hostname, "HOST-RESOURCES-MIB::host"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stderr = []
    while True:
        reads = [pipe.stdout.fileno(), pipe.stderr.fileno()]
        ret = select.select(reads, [], [])

        for fd in ret[0]:
            if fd == pipe.stdout.fileno():
                read = pipe.stdout.readline()
                yield read.strip().split(' ',1)
            if fd == pipe.stderr.fileno():
                read = pipe.stderr.readline()
                stderr.append(read)

        if pipe.poll() != None:
            break
    if pipe.returncode != 0:
        raise IOError(pipe.returncode,"".join(stderr))

def read_from_file(file):
    f = open(file)
    try:
        for line in f:
            yield line.strip().split(' ',1)
    finally:
        f.close()

analyser = SnmpAnalyser()
analyser.analyse(read_from_file(sys.argv[1]))
print analyser.objects.values()

