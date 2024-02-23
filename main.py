import time

from zeroconf import ServiceBrowser, Zeroconf


class MyListener:

    def __init__(self):
        self.addresses = {}
        self.name_func = {}

    #注册函数，当服务被发现时调用
    def Sign_func(self,server_name,funtion):
        self.name_func[server_name] = funtion

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        print("Service %s added, service info: %s" % (name, info))
        if info:
            ip_add = info.parsed_addresses()
            port = info.port
            server_name = name.split(".")[0]
            self.addresses[name] = {"ip_add": ip_add, "port": port}
            if server_name in self.name_func:
                self.name_func[name](ip_add,port)
        else:
            print(f"No info={name}")

    def update_service(self, zeroconf, type, name):
        # This method can be empty for now, but might be needed in future versions
        print("Service %s updated" % (name))
    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name))
        try:
            del self.addresses[name]
        except Exception as e:
            print(e)


zeroconf = Zeroconf()
listener = MyListener()
browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
time.sleep(20)
zeroconf.close()

print(listener.addresses)

