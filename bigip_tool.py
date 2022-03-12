import os
import sys

tool_banner = '''
██████╗ ██╗ ██████╗ ██╗██████╗     ████████╗ ██████╗  ██████╗ ██╗     
██╔══██╗██║██╔════╝ ██║██╔══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║     
██████╔╝██║██║  ███╗██║██████╔╝       ██║   ██║   ██║██║   ██║██║     
██╔══██╗██║██║   ██║██║██╔═══╝        ██║   ██║   ██║██║   ██║██║     
██████╔╝██║╚██████╔╝██║██║            ██║   ╚██████╔╝╚██████╔╝███████╗  v0.0.1
╚═════╝ ╚═╝ ╚═════╝ ╚═╝╚═╝            ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝  By Boringboys
'''

tool_usage = '''Usage:
    Decode: python3 {0} d <Bigip String>
    Encode: python3 {0} e <Ip> <Port>
'''.format(os.path.basename(sys.argv[0]))

def ip_encode(ip):
    ip_list = [int(i) for i in ip.split('.')]
    # print(len(ip_list), ip_list)
    if len(ip_list) == 4:
        encode_ip = (
            256 * 256 * 256 * ip_list[3] +
            256 * 256 * ip_list[2] + 
            256 * ip_list[1] + 
            ip_list[0]
        )
    else:
        encode_ip = None
    return encode_ip


def ip_decode(encode_ip):
    ip_list = []
    _ = encode_ip
    for i in range(4):
        ip_list.append(_ % 256)
        _ = _ // 256
    # print(len(ip_list), ip_list)
    ip = '{0[0]}.{0[1]}.{0[2]}.{0[3]}'.format(ip_list)
    return ip


def port_encode(port):
    encode_port = (
        256 * ( port % 256) +
        port // 256
    )
    return encode_port


def port_decode(encode_port):
    port = (
        256 * (encode_port % 256) +
        encode_port // 256
    )
    return port


def big_ip_encode(ip, port):
    encode_ip = ip_encode(ip)
    encode_port = port_encode(port)
    big_ip_str = '{0}.{1}.{2}'.format(
        encode_ip, encode_port, '0000')
    return big_ip_str


def big_ip_decode(big_ip_str):
    big_ip_list = [int(i) for i in big_ip_str.split('.')]
    # print(len(big_ip_list), big_ip_list)
    if len(big_ip_list) == 3:
        ip = ip_decode(big_ip_list[0])
        port = port_decode(big_ip_list[1])
    else:
        return None
    return ip, port


if __name__ == '__main__':
    print(tool_banner)

    if len(sys.argv) == 3 and sys.argv[1] == 'd':
        try:
            print(
                '解码的Bigip String: {0}\n\n'\
                '解码结果：\n'\
                'ip: {1[0]}\n'\
                'port: {1[1]}'.format(
                    sys.argv[2],
                    big_ip_decode(sys.argv[2])
                )
            )
        except Exception as e:
            print('出错了，自己分析：\n{0}\n'\
                    '{1}'.format(e,tool_usage))
    elif len(sys.argv) == 4 and sys.argv[1] == 'e':
        try:
            print(
                '编码的Ip:Port: {0}:{1}\n\n'\
                '编码结果：\n'\
                'Bigip String: {2}'.format(
                    sys.argv[2],
                    sys.argv[3],
                    big_ip_encode(
                        sys.argv[2],
                        int(sys.argv[3])
                    )
                )
            )
        except Exception as e:
            print('出错了，自己分析：\n{0}\n'\
                    '{1}'.format(e,tool_usage))
    else:
        print(tool_usage)