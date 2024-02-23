import time
import netifaces
import zeroconf


class ZeroconfSD:
    def get_ips_addresses(self):
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
                # print(e)
                pass
        return ip_v6_addresses,ip_v4_addresses

    def ipv4_types(self,ip):
        """
        字符串转换为字节
        :param ip:
        :return:
        """
        a = [ int(x) for x in ip.split(".")]
        return bytes([x for x in a])

    def run(self,server_name,port):
        ips6, ips4 = self.get_ips_addresses()
        ips4_types = [self.ipv4_types(ip) for ip in ips4]

        service_info = zeroconf.ServiceInfo(
            type_="_http._tcp.local.",
            name=f"{server_name}._http._tcp.local.",
            server="noob_Service.local.",
            properties={"path": "/foo"},
            addresses=ips4_types,
            weight=0,
            priority=0,
            interface_index=None,
            port=port,
        )


        zeroconf_ = zeroconf.Zeroconf()

        zeroconf_.register_service(service_info)
        print("Registration of a service, press Ctrl-C to exit...")
        try:
            while True:
                time.sleep(600)
        except KeyboardInterrupt:
            pass
        finally:
            zeroconf_.unregister_service(service_info)
            zeroconf_.close()


if __name__ == '__main__':
    zeroconf = ZeroconfSD()
    zeroconf.run("noob_Service",2101)