from kazoo.client import KazooClient
from kazoo.client import KazooState,KeeperState

zk = KazooClient(hosts='127.0.0.1:2181')
@zk.add_listener
def my_listener(state):
    if state == KazooState.CONNECTED:
        if zk.client_state == KeeperState.CONNECTED_RO:
            print("Read only mode!")
        else:
            print("Read/Write mode!")

    elif state == KazooState.LOST:
        # Register somewhere that the session was lost
        print("KazooState.LOST")
    elif state == KazooState.SUSPENDED:
        # Handle being disconnected from Zookeeper
        print("KazooState.SUSPENDED")
        pass
    else:
        print("other state")


zk.start()
@zk.ChildrenWatch('/my')
def my_func(children):
        print "Children are %s" % children

zk.ensure_path("/my")
zk.ensure_path("/my/n1")
zk.ensure_path("/my/n2/n21")
print("after zk.ensure_path")
zk.stop()
# Create a node with data
#if( zk.exists(
#zk.create("/my/favorite/node", b"a value")
