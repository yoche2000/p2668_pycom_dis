from p2668 import P2668
import time

print("[SYS] Welcome to P2668 Pycom Demo")
my2668 = P2668()
my2668.get_phy_dis()
my2668.get_sen_dis()

my2668.connect()

cnt = 0
while True:
    payload = b'test'
    my2668.socket.send(payload)
    print("Payload Sent: #"+ str(cnt))
    rx = my2668.socket.recv(256)
    if rx:
        print(rx)
    time.sleep(30)
    cnt += 1
