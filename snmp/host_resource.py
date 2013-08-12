from snmp import Namespace
class HostResource(object):
    _registered_objects = {}
    _indices = {}
    namespace = "HOST-RESOURCES-MIB"
    @classmethod
    def get_objects():
        return self._objects

    @classmethod
    def register(self,klass):
        name = klass.name
        if name in self._registered_objects:
            if self._registered_objects[name] != klass:
                raise "Conflict"
        else:
            self._registered_objects[name] = klass
            self._indices[klass.index] = name

    def __init__(self):
        pass
Namespace.register(HostResource)

class HostResourceObject(object):
    name = None
    @classmethod
    def register(self):
        HostResource.register(self)

class Device(HostResourceObject):
    name = "Device"
    index = "hrDeviceIndex"
    keys = ["hrDeviceType","hrDeviceDescr","hrDeviceID","hrDeviceStatus"]
    def __init__(self):
        self.objects = {}
        self.processors = []
        self.network_interfaces = []

Device.register()

class Processor(Device):
    name = "Processor"
    extra_keys = ["hrProcessorFrwID","hrProcessorLoad"]
    def __init__(self):
        pass

Processor.register()

class NetworkInterface(Device):
    name = "NetworkInterface"
    extra_keys = ["hrDeviceErrors"]
    def __init__(self):
        pass

NetworkInterface.register()

class Fs(HostResourceObject):
    name = "Fs"
    index = "hrFSIndex"
    keys = ["hrFSMountPoint","hrFSRemoteMountPoint","hrFSType","hrFSAccess","hrFSBootable","hrFSStorageIndex","hrFSLastFullBackupDate","hrFSLastPartialBackupDate"]
    def __init__(self):
        pass

Fs.register()

class Memory(HostResourceObject):
    name = "Memory"
    index = "hrMemorySize"
    def __init__(self):
        pass

Memory.register()

class Storage(HostResourceObject):
    name = "Storage"
    index = "hrStorageIndex"
    keys = ["hrStorageType","hrStorageDescr","hrStorageAllocationUnits","hrStorageSize","hrStorageUsed"]
    def __init__(self):
        pass

Storage.register()

class SWRun(HostResourceObject):
    name = "SWRun"
    index = "hrSWRunIndex"
    keys = ["hrSWRunName","hrSWRunID","hrSWRunPath","hrSWRunParameters","hrSWRunType","hrSWRunStatus","hrSWRunPerfCPU","hrSWRunPerfMem",]
    def __init__(self):
        pass

SWRun.register()

class System(HostResourceObject):
    name = "System"
    index = "hrSystemUptime"
    keys = ["hrSystemDate","hrSystemInitialLoadDevice","hrSystemInitialLoadParameters","hrSystemNumUsers","hrSystemProcesses","hrSystemMaxProcesses",]
    def __init__(self):
        pass

System.register()
if __name__ == "__main__":
    print HostResource._registered_objects
    print HostResource._indices
