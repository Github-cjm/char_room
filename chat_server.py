"""
 chat room
 env: python 3.5
 socket udp fork  练习
"""

from socket import *
import os

# 服务器地址
ADDR = ('0.0.0.0', 1888)

# 存储用户 {name:address}
user = {}


# 登录
# 设计/学习函数从三个方面:功能,参数,返回值
def do_login(sockfd, name, addr):
    if name in user or '管理员' in name:
        sockfd.sendto("该用户已存在".encode(), addr)
        return
    sockfd.sendto(b'OK', addr)

    # 通知其他人
    msg = "\n欢迎%s进入法拉利车队聊天室" % name
    for i in user:
        sockfd.sendto(msg.encode(), user[i])
    # 将用户信息插入字典
    user[name] = addr
    print(msg)


# 消息内容
def do_chat(sockfd, name, text):
    msg = "\n%s : %s" % (name, text)
    for i in user:
        if i != name:
            sockfd.sendto(msg.encode(), user[i])
            print(msg)


# 退出
def do_quit(sockfd, name):
    msg = "\n%s 退出了聊天室" % name
    for i in user:
        if i != name:
            sockfd.sendto(msg.encode(), user[i])
        else:
            sockfd.sendto(b'EXIT', user[i])
    del user[name]


# 循环接收客户端请求函数
def do_request(sockfd):
    while True:
        data, addr = sockfd.recvfrom(1024)
        tmp = data.decode().split(' ')  # 拆分请求
        if tmp[0] == 'L':  # 根据请求类型执行不同内容
            do_login(sockfd, tmp[1], addr)  # 完成具体服务端登录工作
        elif tmp[0] == 'C':
            text = ' '.join(tmp[2:])  # 拼接消息内容
            do_chat(sockfd, tmp[1], text)
        elif tmp[0] == 'Q':
            if tmp[1] not in user:
                sockfd.sendto(b'EXIT', addr)
                continue
            do_quit(sockfd, tmp[1])


# 搭建udp网络
def main():
    # udp套接字
    sockfd = socket(AF_INET, SOCK_DGRAM)
    # 绑定地址
    sockfd.bind(ADDR)

    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        while True:
            msg = input("管理员消息:")
            msg = 'C 管理员消息 ' + msg
            sockfd.sendto(msg.encode(), ADDR)
    else:
        # 请求处理函数
        do_request(sockfd)


if __name__ == "__main__":
    main()
