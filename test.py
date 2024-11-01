from send_UART import *

while True:
    send_packet(6, 0, 0x54)
    print("đã gửi")
    time.sleep(1)
    data = receive_packet_all()
    print("đã nhận",data)