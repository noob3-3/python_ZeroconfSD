
import netifaces



if __name__ == '__main__':
    # 测试
    ips6, ips4 = get_ips_addresses()
    print(f"本机所有IPv6地址：{ips6} \n本机所有IPv4地址：{ips4}")


