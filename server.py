import time

import netifaces
import zeroconf
def get_ips_addresses():
    """
    获取本机所有IP地址
    """

    # 获取所有网络接口
    interfaces = netifaces.interfaces()
    # 遍历网络接口并获取IPv6地址
    ip_v6_addresses = []
    ip_v4_addresses = []

    for interface in interfaces:
        # 获取接口的详细信息
        interface_info = netifaces.ifaddresses(interface)
        try:
            # 判断接口是否激活
            if interface_info[netifaces.AF_INET6]:
                # 获取接口的IPv6地址
                ip_v6_addresses.append(interface_info[netifaces.AF_INET6][0]['addr'])
            if interface_info[netifaces.AF_INET]:
                # 获取接口的IPv4地址
                ip_v4_addresses.append(interface_info[netifaces.AF_INET][0]['addr'])
        except KeyError as e:
            print(e)
    return ip_v6_addresses,ip_v4_addresses
ips6,ips4 = get_ips_addresses()

# 获取本地ip地址转换为字节
def ipv4_types(ip):
    """
    字符串转换为字节
    :param ip:
    :return:
    """
    a = [ int(x) for x in ip.split(".")]
    return bytes([x for x in a])


ips4 = [ipv4_types(ip) for ip in ips4]

service_info = zeroconf.ServiceInfo(
    type_="_http._tcp.local.",
    name="noob_Service._http._tcp.local.",
    server="noob_Service.local.",
    properties={"path": "/foo"},
    addresses=ips4,
    weight=0,
    priority=0,
    interface_index=None,
    port=8080,
)


zeroconf = zeroconf.Zeroconf()

zeroconf.register_service(service_info)
print("Registration of a service, press Ctrl-C to exit...")
try:
    while True:
        time.sleep(600)
except KeyboardInterrupt:
    pass
finally:
    zeroconf.unregister_service(service_info)
    zeroconf.close()
