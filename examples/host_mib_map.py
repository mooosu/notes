top_keys =[ "hrSystem","hrStorageTable","hrDevice","hrSWRun","hrSWRunPerf"]
entry = {
        "hrSystem": {
            # The amount of time since this host was last initialized.
            # Note that this is different from sysUpTime in the SNMPv2-MIB [RFC1907]
            # because sysUpTime is the uptime of the network management portion of the system.
            "hrSystemUptime": None,
            # The host's notion of the local date and time of day.
            "hrSystemDate": None,
            "hrSystemInitialLoadDevice": None,
            "hrSystemInitialLoadParameters": None,
            # The number of user sessions for which this host is
            # storing state information.  A session is a collection
            # of processes requiring a single act of user
            # authentication and possibly subject to collective job control
            "hrSystemNumUsers": None, #
            # The number of process contexts currently loaded or running on this system
            "hrSystemProcesses": None,
            "hrSystemMaxProcesses": None,
        }
        "hrStorageTable" : {
            "hrStorageEntry" : {
                "hrStorageType" : None,
                "hrStorageDescr" : None,
                "hrStorageAllocationUnits" : None,
                "hrStorageSize" : None,
                "hrStorageUsed" : None,
                "hrStorageAllocationFailures" : None,
            }
        "hrMemorySize",
        #
        "hrStorageIndex",
        "hrStorageType",
        "hrStorageDescr",
        "hrStorageAllocationUnits",
        "hrStorageSize",
        "hrStorageUsed",
        "hrDeviceIndex",
        "hrDeviceType",
        "hrDeviceDescr",
        "hrDeviceID",
        "hrDeviceStatus",
        "hrDeviceErrors",
        "hrProcessorFrwID",
        "hrProcessorLoad",
        "hrNetworkIfIndex",
        "hrFSIndex",
        "hrFSMountPoint",
        "hrFSRemoteMountPoint",
        "hrFSType",
        "hrFSAccess",
        "hrFSBootable",
        "hrFSStorageIndex",
        "hrFSLastFullBackupDate",
        "hrFSLastPartialBackupDate",
        "hrSWRunIndex",
        "hrSWRunName",
        "hrSWRunID",
        "hrSWRunPath",
        "hrSWRunParameters",
        "hrSWRunType",
        "hrSWRunStatus",
        "hrSWRunPerfCPU",
        "hrSWRunPerfMem",
        }
