# -*- Mode: Python -*-
# vi:si:et:sw=4:sts=4:ts=4

import re

class SnmpBaseObject:
    # hrSystem
    uptime_pattern = (re.compile("Uptime\.(\d+)"),"uptime")
    date_pattern = (re.compile("Date\.(\d+)"),"date")
    initial_load_device_pattern = (re.compile("InitialLoadDevice\.(\d+)"),"initial_load_device")
    initial_load_parameters_pattern = (re.compile("InitialLoadParameters\.(\d+)"),"initial_load_parameters")
    num_users_pattern = (re.compile("NumUsers\.(\d+)"),"num_users")
    processes_pattern = (re.compile("Processes\.(\d+)"),"processes")
    max_processes_pattern = (re.compile("MaxProcesses\.(\d+)"),"max_processes")
    # hrMemory
    memory_size_pattern = (re.compile("Size\.(\d+)"),"memory_size")

    # Common
    index_patten = (re.compile("Index\.(\d+)"),"index")
    descr_pattern = (re.compile("Descr\.(\d+)"),"descr")
    type_pattern = (re.compile("Type\.(\d+)"),"type")
    # hrStorage
    allocation_units_pattern = (re.compile("AllocationUnits\.(\d+)"),"allocation_units")
    size_pattern = (re.compile("Size\.(\d+)"),"size")
    used_pattern = (re.compile("Used\.(\d+)"),"used")

    # hrDevice
    status_pattern = (re.compile("Status\.(\d+)"),"status")
    # hrProcessor
    load_pattern   = (re.compile("Load\.(\d+)"),"load")
    # hrFS
    mount_point_pattern   = (re.compile("hrFSMountPoint\.(\d+)"),"mount_point")
    remote_mount_point_pattern   = (re.compile("hrFSRemoteMountPoint\.(\d+)"),"remote_mount_point")
    access_pattern   = (re.compile("Access\.(\d+)"),"access")
    bootable_pattern   = (re.compile("Bootable\.(\d+)"),"bootable")
    storage_index_pattern = (re.compile("StorageIndex\.(\d+)"),"storage_index")

    # hrSWRun
    name_pattern = (re.compile("Name\.(\d+)"),"name")


    def __init__(self,line):
        self.line = line

        self.data_patterns = [ SnmpBaseObject.index_patten,SnmpBaseObject.descr_pattern ]
        self.data_converters = {
            "index" : lambda x: int(x),
            "allocation_units" : lambda x: int(x.split(' ',1)[0]),
            "memory_size" : lambda x: int(x.split(' ',1)[0]),
            "size" : lambda x: int(x),
            "type" : lambda x: x.split('::',1)[1],
        }

    def __str__(self):
        return "str:index: %s,descr: %s" %( self.index,self.descr)

    def __repr__(self):
        return "repr:index: %s,descr: %s" %( self.index,self.descr)

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

class SnmpSystem(SnmpBaseObject):

    def __init__(self,line):
        SnmpBaseObject.__init__(self,line)
        self.data_patterns = []
        self.index = 0
        self.data_patterns.append(SnmpBaseObject.uptime_pattern)
        self.data_patterns.append(SnmpBaseObject.date_pattern)
        self.data_patterns.append(SnmpBaseObject.initial_load_device_pattern)
        self.data_patterns.append(SnmpBaseObject.initial_load_parameters_pattern)
        self.data_patterns.append(SnmpBaseObject.num_users_pattern)
        self.data_patterns.append(SnmpBaseObject.processes_pattern)
        self.data_patterns.append(SnmpBaseObject.max_processes_pattern)

    def __repr__(self):
        return "repr:uptime: %s,date: %s,initial_load_device: %s,initial_load_parameters: %s,num_users: %s" %(
                self.uptime,self.date,self.initial_load_device,self.initial_load_parameters,self.num_users)

class SnmpMemory(SnmpBaseObject):
    def __init__(self,line):
        SnmpBaseObject.__init__(self,line)
        self.index = 0
        self.data_patterns.append(SnmpBaseObject.memory_size_pattern)

    def total(self):
        return self.size

    def __repr__(self):
        return "repr:size: %s" % (self.memory_size)

class SnmpStorage(SnmpBaseObject):
    def __init__(self,line):
        SnmpBaseObject.__init__(self,line)
        self.data_patterns.append(SnmpBaseObject.type_pattern)
        self.data_patterns.append(SnmpBaseObject.allocation_units_pattern)
        self.data_patterns.append(SnmpBaseObject.size_pattern)
        self.data_patterns.append(SnmpBaseObject.used_pattern)

    def total(self,readable):
        total_bytes = self.allocation_units * self.size
        return total_bytes

    def __repr__(self):
        return "repr:index: %s,descr: %s,size: %s,allocation_units: %s,type: %s,total: %s" % (
                self.index,self.descr,self.size,self.allocation_units,self.type,self.total())

class SnmpDevice(SnmpBaseObject):
    def __init__(self,line):
        SnmpBaseObject.__init__(self,line)
        self.data_patterns.append(SnmpBaseObject.type_pattern)
        self.data_patterns.append(SnmpBaseObject.status_pattern)
        self.data_patterns.append(SnmpBaseObject.load_pattern)
        self.status = None
        self.load   = None

    def __repr__(self):
        return "repr:index: %s,descr: %s,type: %s,status: %s,load: %s" %( self.index,self.descr,self.type,self.status,self.load)

class SnmpFS(SnmpBaseObject):
    def __init__(self,line):
        SnmpBaseObject.__init__(self,line)
        self.data_patterns[0] = (re.compile("hrFSIndex\.(\d+)"),"index")
        self.data_patterns.append(SnmpBaseObject.mount_point_pattern)
        self.data_patterns.append(SnmpBaseObject.remote_mount_point_pattern)
        self.data_patterns.append(SnmpBaseObject.access_pattern)
        self.data_patterns.append(SnmpBaseObject.bootable_pattern)
        self.data_patterns.append(SnmpBaseObject.storage_index_pattern)
        self.data_patterns.append(SnmpBaseObject.type_pattern)
        self.descr = None
        self.mount_point = None
        self.remote_mount_point = None
        self.access = None

    def __repr__(self):
        return "repr:index: %s,descr: %s,mount_point: %s,remote_mount_point: %s,access: %s,storage_index: %s,bootable: %s, type: %s" % (
                self.index,self.descr,self.mount_point,self.remote_mount_point,self.access,self.storage_index,self.bootable,self.type)

class SnmpSWRun(SnmpBaseObject):
    def __init__(self,line):
        SnmpBaseObject.__init__(self,line)
        self.data_patterns = [ SnmpBaseObject.index_patten ]
        self.data_patterns.append(SnmpBaseObject.name_pattern)

    def __repr__(self):
        return "repr:index: %s,name: %s" % ( self.index,self.name )

class SnmpParser:
    def __init__(self):
        self.system_pattern = re.compile("hrSystem\w+\.(\d+)")
        self.memory_pattern = re.compile("hrMemory\w+\.(\d+)")
        self.storage_pattern = re.compile("hrStorage\w+\.(\d+)")
        self.device_pattern = re.compile("hrDevice\w+\.(\d+)")
        self.processor_pattern = re.compile("hrProcessor\w+\.(\d+)")
        self.fs_pattern = re.compile("hrFS\w+\.(\d+)")
        self.swrun_pattern = re.compile("hrSWRun\w+\.(\d+)")
        self.pattern_list= (
            (self.system_pattern, SnmpSystem),
            (self.memory_pattern, SnmpMemory),
            (self.storage_pattern, SnmpStorage),
            (self.device_pattern, SnmpDevice),
            (self.processor_pattern, SnmpDevice),
            (self.fs_pattern, SnmpFS),
            (self.swrun_pattern, SnmpSWRun),
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
            SnmpSystem: {},
            SnmpMemory: {},
            SnmpStorage : {},
            SnmpDevice  : {},
            SnmpFS: {},
            SnmpSWRun: {},
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
