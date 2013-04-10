# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

import subprocess
import sys
import select
import re


class SnmpBaseObject:
    def __init__(self,line):
        self.line = line
        self._index = None
        self.descr = None

        self.data_patterns = [
            (re.compile("Index\.(\d+)"),"index"),
            (re.compile("Descr\.(\d+)"),"descr"),
        ]
        self.data_converters = {
            "index" : lambda x: int(x),
        }

    def __str__(self):
        return "str:index: %s,descr: %s" %( self.index,self.descr)

    def __repr__(self):
        return "repr:index: %s,descr: %s" %( self.index,self.descr)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self,value):
        self._index = int(value)

    def parse(self,line=None):
        if line == None:
            line = self.line
        name,value = line
        for pattern , attr  in self.data_patterns:
            res = re.search(pattern,name)
            if res:
                converter = self.data_converters.get(attr,None)
                if converter:
                    value = converter(value)
                setattr(self,attr,value)

class SnmpStorage(SnmpBaseObject):
    def __init__(self,line):
        SnmpBaseObject.__init__(self,line)
        self.data_patterns.append((re.compile("Type\.(\d+)"),"type"))

class SnmpDevice(SnmpBaseObject):
    def __init__(self,line):
        SnmpBaseObject.__init__(self,line)
        self.data_patterns.append((re.compile("Type\.(\d+)"),"type"))

class SnmpParser:
    def __init__(self):
        self.storage_pattern = re.compile("hrStorage\w+\.(\d+)")
        self.device_pattern = re.compile("hrDevice\w+\.(\d+)")
        self.fs_pattern = re.compile("hrFS\w+\.(\d+)")
        self.swrun_pattern = re.compile("hrSWRun\w+\.(\d+)")
        self.pattern_list= (
            (self.storage_pattern, SnmpStorage),
            (self.device_pattern, SnmpDevice)
        )

        self.bytes_pattern = re.compile("(\d+) KBytes")

    def parse(self,line):
        for pattern,cls in self.pattern_list:
            res = re.search(pattern,line)
            if res:
                return cls,int(res.group(1))

        return None


    def parse_bytes(line):
        #"HOST-RESOURCES-MIB::hrSWRunPerfMem.1" , "1900 KBytes"

        pass

    def parse_type(line):
        #"HOST-RESOURCES-MIB::hrStorageType.1" , "HOST-RESOURCES-MIB::hrStorageTypes.2"
        pass
    def parse_descr(line):
        #"HOST-RESOURCES-MIB::hrStorageDescr.1" , "Physical memory"
        pass


class SnmpAnalyser:
    def __init__(self):
        self.objects= {
            SnmpStorage : {},
            SnmpDevice  : {}
        }
        self.parser = SnmpParser()

    def analyse(self,snmp_lines):
        for line in snmp_lines:
            res  = self.parser.parse(line[0])
            if res :
                cls , index = res
                obj = self.objects[cls].get(index,None)
                if obj:
                    obj.parse(line)
                else:
                    obj = cls(line)
                    obj.parse()
                    self.objects[cls][obj.index] = obj

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
analyser = SnmpAnalyser()
analyser.analyse(read_snmp())
print analyser.objects.values()

#print 'stdout:', "".join(stdout)
#print 'stderr:', "".join(stderr)
