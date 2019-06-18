"""
 chat room
 客户端
"""
from socket import *
import os, sys

# 服务端地址
ADDR = ('127.0.0.1', 1888)


# 发送消息
def send_msg(sockfd, name):
    while True:
        try:
            text = input("请开始你的演讲:")
        except KeyboardInterrupt:
            text = "quit"
        if text.strip() == 'quit':
            msg = "Q " + name
            sockfd.sendto(msg.encode(), ADDR)
            sys.exit("退出聊天室")
        msg = "C %s %s" % (name, text)
        sockfd.sendto(msg.encode(), ADDR)


# 接收消息
def recv_msg(sockfd):
    while True:
        try: # 服务器意外终端,则各个客户端都会退出
            data, addr = sockfd.recvfrom(4096)
        except KeyboardInterrupt:
            sys.exit()
        # 服务端发送EXIT退出
        if data.decode() == "EXIT":
            sys.exit()
        print(data.decode() + '\n请开始你的演讲:', end='')


# 启动客户端
def main():
    sockfd = socket(AF_INET, SOCK_DGRAM)
    while True:
        name = input("请输入姓名:")
        msg = "L " + name
        sockfd.sendto(msg.encode(), ADDR)
        # 等待反馈
        data, addr = sockfd.recvfrom(1024)
        if data.decode() == 'OK':
            print("成功加入法拉利车队")
            break
        else:
            print(data.decode())

    # 创建新的进程
    pid = os.fork()
    if pid < 0:
        sys.exit("Error!")
    elif pid == 0:
        send_msg(sockfd, name)
    else:
        recv_msg(sockfd)


if __name__ == "__main__":
    main()
