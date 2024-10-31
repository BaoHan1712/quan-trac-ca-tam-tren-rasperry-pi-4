from data_processing.data_processing import *
from cover.imports import *
from check_com.checkCom_global import *
from send_UART import *

# Xong
def get_setting_data():
    send_threshold_value_1  = send_packet(6, 0,0x54)
    send_threshold_value_2 = send_packet(6, 1,0x54)


def get_data_com(value, arr_avg, sensor):
    
    # Xử lý dữ liệu nhận được
    # Check dữ liệu từ cảm biến
    # print("❤️❤️❤️❤️❤️❤️❤️❤️", sensor)
    status = int
    data = int
    id = int
    if (len(sensor) > 4):
        status = sensor[3]
        data = sensor[4]
        id = sensor[1]
    else:
        status = sensor[2]
        data = sensor[3]
        id = sensor[1]

    if (data):
        if (status == 253):
            if (id == 0):
                save_data_excel_ngay(None, None, data, None)
            elif (id == 1):
                save_data_excel_ngay(None, None, None, data)
        elif (status == 254):
            value.set(data)
            arr_avg.append(data)
        elif (status == 192):
            if (id == 0):
                threshold_value_1.set(data)
            elif (id == 1):
                threshold_value_2.set(data)
        elif (status == 191):
            if (id == 0):
                sio.emit('threshold-device', {
                    "device": int(id),
                    "threshold": data,
                    "type": "S"
                })
            elif (id == 1):
                sio.emit('threshold-device', {
                    "device": int(id),
                    "status": 1,
                    "type": "S"
                })
        elif (status == 201):
            if (id == 0):
                sio.emit('time-clean', {
                    "device": int(id),
                    "timeClean": data,
                    "type": "S"
                })
            elif (id == 1):
                sio.emit('time-clean', {
                    "device": int(id),
                    "timeClean": data,
                    "type": "S"
                })
        elif (data == 204):
            print("Đã vào đây 😘😘😘😘😘😘😘😘😘😘😘")
            sio.emit('device-status-running', {
                "device": int(id),
                "status": 1,
                "type": "S"
            })




def get_data_button(sensor):
    data = sensor[4]
    button_status.set(data)
    if (data == 1):
        print("Nút bấm đã được nhấn")
        ring_status.set("Đang Tắt")
        turn_off_ring(port)

# Hàm bật chuông ||| xong
def turn_on_ring(port):
    print("Chuông báo 🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔")
    # data_send = cmdString_one(6, 9, 1)
    for _ in range(3):  # Gửi 3 lần
        data_send = send_packet(6,7,0x43,[0x62])
        time.sleep(3)

# Hàm tắt chuông||| Xong
def turn_off_ring(port):
    print("Tắt Chuông báo ❌❌❌❌❌❌❌❌🔔🔔🔔🔔🔔🔔🔔🔔")
    # data_send = cmdString_one(6, 9, 0)
    for _ in range(6):  
        data_send = send_packet(6,7,0x43,[0x74])
        time.sleep(4)

# Xong
def connect_COM():
    # Gửi dữ liệu cho cả hai cảm biến và đọc phản hồi liên tục
    for sensor_id in (0, 1):
        data_send = send_packet(6,sensor_id,0x54)
        time.sleep(2)



# Hàm kiểm tra cổng || Xong
def check_com():
    data_send = send_packet(6,0,0x54)
    print("đang chờ nhận tín hiệu để mở app")
    receive_packet_all()


# kiểm tra độ đục của nước từ 2CB, gửi thông báo về tình trạng nước.
def handle_check_mutate(port, value1, value2, avg1, avg2, threshold_value_1, threshold_value_2, status1, status2, ring_status):
    check_1 = False
    check_2 = False

# Kiểm tra và xử lý cảm biến 1
    value_compare_1 = value1.get() - avg1.get()
    if value_compare_1 > threshold_value_1.get():
        check_1 = True
        sio.emit('water-status', {
            "sensor": "0",
            "status": "D"
        })
        mutation_value_1.set(value_compare_1)
        status1.set("Nước Đục")
    else:
        status1.set("Bình Thường")
        sio.emit('water-status', {
            "sensor": "0",
            "status": "C"
        })
# Kiểm tra và xử lý cảm biến 2
    value_compare_2 = value2.get() - avg2.get()
    if value_compare_2 > threshold_value_2.get():
        check_2 = True
        sio.emit('water-status', {
            "sensor": "1",
            "status": "D"
        })
        mutation_value_1.set(value_compare_1)
        status2.set("Nước Đục")
    else:
        status2.set("Bình Thường")
        sio.emit('water-status', {
            "sensor": "1",
            "status": "C"
        })

    print("Giá trị trung bình cảm biến 1: ", avg1.get())
    print("Giá trị trung bình cảm biến 2: ", avg2.get())
    print("Giá trị đột biến 1: ", value_compare_1)
    print("Giá trị đột biến 2: ", value_compare_2)
    # print(check_1)
    # print(check_2)

    """Nếu phát hiện đục thì kích hoạt chuông"""
    
    if check_1 or check_2:
        print("Đột biến 💥💥💥💥💥💥💥💥💥💥💥💥")
        if button_status.get() == 0:
            print("Chuông báo đang bật")
            ring_status.set("Đang Bật")
            turn_on_ring(port)
            return

""" Hàm Khởi động cùng máy tính"""
# def add_to_startup():
#     shell = win32com.client.Dispatch("WScript.Shell")
#     startup = shell.SpecialFolders("Startup")
#     shortcut = shell.CreateShortCut(os.path.join(startup, "catam_gui.lnk"))
#     shortcut.Targetpath = os.path.abspath("catam_gui.exe")
#     shortcut.WorkingDirectory = os.path.dirname(
#         os.path.abspath("catam_gui.exe"))
#     shortcut.save()
