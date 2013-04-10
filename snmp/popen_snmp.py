# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

import subprocess
import sys
import select


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
                yield [ '"%s"' % v for v in read.strip().split(' ',1)]
            if fd == pipe.stderr.fileno():
                read = pipe.stderr.readline()
                stderr.append(read)

        if pipe.poll() != None:
            break
    return (pipe.returncode,stderr)

#print 'stdout:', "".join(stdout)
#print 'stderr:', "".join(stderr)
