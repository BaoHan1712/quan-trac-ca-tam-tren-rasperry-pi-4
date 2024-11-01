from data_processing.data_processing import *
from cover.imports import *
from check_com.checkCom_global import *
from send_UART import *

# Đặt khoảng giá trị đột biến
def get_setting_data():
    send_packet(6, 0,0x44)
    send_packet(6, 1,0x44)

# def check_button_on(port):
#     data_send = cmdString_one(6, 7, 255)
    


# Hàm quan trọng nhận dữ liệu rôi xử lý
def get_data_com(value, arr_avg, sensor):
    # Check dữ liệu từ cảm biến
    print("❤️❤️❤️❤️❤️❤️❤️❤️", sensor)
 
    fromID, toID, title, data_receive = sensor
    data = data_receive[0]
    id = fromID
    status = title
    
    if (data):
        if (status == 0x57):
            if (id ==  0):
                print("da luu vao excel  ❤️   voi id 0")
                hi =save_data_excel_ngay(None, None, data, None)

            elif (id == 1):
                print("da luu vao excel  ❤️   voi id 1")
                save_data_excel_ngay(None, None, None, data)

    #Cảm biến gửi giá trị khi được gateway hỏi
        elif (status == 0x54):
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
    data = sensor[3]
    button_status.set(data)
    if (data == 1):
        print("Nút bấm đã được nhấn")
        ring_status.set("Đang Tắt")
        turn_off_ring()

# Hàm bật chuông ||| xong
def turn_on_ring():
    print("Chuông báo 🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔🔔")
    # data_send = cmdString_one(6, 9, 1)
    for _ in range(3):  # Gửi 3 lần
        send_packet(6,7,0x43,0x62)
        time.sleep(3)

# Hàm tắt chuông||| Xong
def turn_off_ring():
    print("Tắt Chuông báo ❌❌❌❌❌❌❌❌🔔🔔🔔🔔🔔🔔🔔🔔")
    # data_send = cmdString_one(6, 9, 0)
    for _ in range(6):  
        data_send = send_packet(6,7,0x43,[0x74])
        time.sleep(4)

# Xong
def connect_COM():
    # Gửi dữ liệu cho cả hai cảm biến và đọc phản hồi liên tục
    for sensor_id in (0, 1):
        send_packet(6, sensor_id, 0x54)
        time.sleep(2)



# Hàm kiểm tra cổng || Xong
def check_com():
    data_send = send_packet(6, 0, 0x54)
    print("đang chờ nhận tín hiệu để mở app")
    data =receive_packet_all()
    if data:
        fromID = data[0]
        if (fromID == 7):
            print("Check chuông báo lần đầu!!!")
            return


def handle_check_mutate(port, value1, value2, avg1, avg2, threshold_value_1, threshold_value_2, status1, status2, ring_status):
    check_1 = False
    check_2 = False

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
