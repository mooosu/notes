from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from time import sleep

io_loop = IOLoop.instance()
def handle_request(response):
    if response.error:
        print "Error:", response.error
    else:
        print response.body

http_client = AsyncHTTPClient()
for i in xrange(2,254):
    print i
    sleep(0.012)
    http_client.fetch("http://ip.taobao.com/service/getIpInfo.php?ip=119.147.215." + str(i), handle_request)
io_loop.start()
