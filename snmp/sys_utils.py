import sys
import netifaces
import subprocess
import re
class SysUtils(object):
    def __init__(self):
        pass

    @staticmethod
    def is_macosx():
        return sys.platform == "darwin";

    @staticmethod
    def is_linux():
        return sys.platform == "linux2";

    @staticmethod
    def get_first_ip():
        if SysUtils.is_macosx():
            eth_prefix = 'en'
        elif SysUtils.is_linux():
            eth_prefix = 'eth'
        else:
            raise Exception("Not support platform: %s" % sys.platform)
        for i in xrange(0,255):
            try:
                ret = netifaces.ifaddresses("%s%s" % ( eth_prefix,i))
                print ret[netifaces.AF_INET]
                break
            except ValueError:
                pass

    @staticmethod
    def get_hostname()

        netifaces.interfaces()

    @staticmethod
    def get_ips_with_cidr():
        output = subprocess.check_output("ip addr show  | grep 'inet '| grep -v '127.0.0.1'", shell=True)
        for line in output.split("\n"):
            res = re.match(r'\s+inet\s+(\d+\.\d+\.\d+\.\d).+(eth\d+)',line)
            print res.groups()[1],res.groups()[0]

""""
# ip scope with cidr
get_ip_scope_with_cidr()
{
            ips=`ip addr show  | grep 'inet '| grep -v '127.0.0.1' |  sed 's/ \+inet \([0-9]\+\.[0-9]\+\.[0-9]\+\)\.[0-9]\+\(\/[0-9]\+\)\(.\+\)/\1.0\2/'`
                echo importps
                }
    def
"""

if __name__ == "__main__":
    SysUtils.get_first_ip()
