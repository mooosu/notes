from ns import Namespace,SnmpObject

class HostResource(SnmpObject):
    namespace = "HOST-RESOURCES-MIB"

Namespace.register(HostResource)

class HostResourceObject(object):
    def __init__(self,data):
        self.strs = []
        for key,v in data.items():
            setattr(self,key,v)
            self.strs.append("%s:%s" % ( key ,v ))

    def __repr__(self):
        return ','.join(self.strs) + "\n"
    @classmethod
    def register(self):
        HostResource.register(self)

    @classmethod
    def parse(self,data):
        indcies = []
        self.objects = []
        for i in data[self.index]:
            indcies.append(i)
        for i in indcies:
            pairs = {}
            for key in self.keys:
                pairs[key] = data[key].get(i,None)
            obj = self(pairs)
            self.objects.append(obj)

        return self.objects

class Device(HostResourceObject):
    name = "Device"
    index = "hrDeviceIndex"
    keys = ["hrDeviceType","hrDeviceDescr","hrDeviceID","hrDeviceStatus"]
    subtypes = {}

    @classmethod
    def parse(self,data):
        indcies = []
        self.objects = []
        for i in data[self.index]:
            indcies.append(i)
        for i in indcies:
            pairs = {}
            for key in self.keys:
                pairs[key] = data[key].get(i,None)
            device_type = pairs["hrDeviceType"]
            klass = self.subtypes.get(device_type,None)
            if not klass:
                raise Exception("Unknown device type")
            for key in klass.extra_keys:
                pairs[key] = data[key].get(i,None)
            obj = klass(pairs)
            self.objects.append(obj)

        return self.objects

    @classmethod
    def register_subtype(self):
        devicet_type = "HOST-RESOURCES-TYPES::%s" % self.name
        self.subtypes[devicet_type] = self


Device.register()

class hrDeviceProcessor(Device):
    name = "hrDeviceProcessor"
    extra_keys = ["hrProcessorFrwID","hrProcessorLoad"]

hrDeviceProcessor.register_subtype()

class hrDeviceCoprocessor(Device):
    name = "hrDeviceCoprocessor"
    extra_keys = []

hrDeviceCoprocessor.register_subtype()

class hrDeviceNetwork(Device):
    name = "hrDeviceNetwork"
    extra_keys = ["hrDeviceErrors"]

hrDeviceNetwork.register_subtype()
class hrFs(HostResourceObject):
    name = "hrFs"
    index = "hrFSIndex"
    keys = ["hrFSMountPoint","hrFSRemoteMountPoint","hrFSType","hrFSAccess","hrFSBootable","hrFSStorageIndex","hrFSLastFullBackupDate","hrFSLastPartialBackupDate"]

hrFs.register()

class hrMemory(HostResourceObject):
    name = "hrMemory"
    index = "hrMemorySize"
    keys = ["hrMemorySize"]

hrMemory.register()

class hrStorage(HostResourceObject):
    name = "hrStorage"
    index = "hrStorageIndex"
    keys = ["hrStorageType","hrStorageDescr","hrStorageAllocationUnits","hrStorageSize","hrStorageUsed"]

hrStorage.register()

class hrSWRun(HostResourceObject):
    name = "hrSWRun"
    index = "hrSWRunIndex"
    keys = ["hrSWRunName","hrSWRunID","hrSWRunPath","hrSWRunParameters","hrSWRunType","hrSWRunStatus","hrSWRunPerfCPU","hrSWRunPerfMem",]

hrSWRun.register()

class hrSystem(HostResourceObject):
    name = "hrSystem"
    index = "hrSystemUptime"
    keys = ["hrSystemUptime","hrSystemDate","hrSystemInitialLoadDevice","hrSystemInitialLoadParameters","hrSystemNumUsers","hrSystemProcesses","hrSystemMaxProcesses",]

hrSystem.register()

if __name__ == "__main__":
    print HostResource._registered_objects
    print HostResource._indices
