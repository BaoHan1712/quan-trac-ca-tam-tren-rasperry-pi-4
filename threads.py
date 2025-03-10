from cover.imports import *
from data_processing.data_processing import *
from serial_communication import *
from check_com.checkCom_global import *
from cover.models import Threading
from send_UART import *


connect = Threading()
handle_data = Threading()
check = Threading()
websocket_thread = Threading()
data_queue = queue.Queue()
button_dung = Threading()
listen_off = Threading()


# Hàm gửi data
def send_data(device, status):
    if device in [0, 1]:
        # data_send = cmdString_one(6, device, 204)
        data_send = send_packet(6, device, 0x53)
        
    elif device in [2, 3, 4, 5]:
        for _ in range(3):
            data_send = send_packet(6, device, status)
            time.sleep(2)
    else:
        return 'không xác định'
    
    print("Data send từ socket: ", data_send)



# Hàm đọc port 
def read_from_port( data_queue, restart_app):
    while True:
        try:
            data = receive_packet_all()
            if data:
                data_queue.put(data)
                print("đã đưa vào hàng đợi")

        except serial.SerialException as e:
            print(f"Error: {e}")
            root.after(4000, restart_app)
       


def filter_data(event):
    device = int(event.get('device'))
    status = int()
    timeClean = int()
    threshold = int()
    output_dir = "/home/ailab/Downloads/luu_ca_tam"
    df = pd.read_excel(os.path.join(output_dir, "cai_dat_catam.xlsx"))

# Thời gian dọn vệ sinh
    if event.get('timeClean') is not None and event.get('threshold') is not None:
        timeClean = int(event.get('timeClean'))
        threshold = int(event.get('threshold'))
        df.iloc[0, 7] = int(threshold)
        df.iloc[0, 9] = int(timeClean)

        # data_send1 = cmdString_two(6, device, 200, timeClean)
        # port.write(data_send1)

        # Thay đổi thời gian vệ sinh
        data_send1 = send_packet(6, device, 0x61, [timeClean])
        # data_send2 = cmdString_two(6, device, 191, threshold)
        # port.write(data_send2)
        send_packet(6, device, 0x44, [threshold])
        return

    if event.get('action') is not None and event.get('action') != '':
        status = int(event.get('action'))
        return send_data(device, status)

    if event.get('timeClean') is not None:
        timeClean = event.get('timeClean')
        df.iloc[0, 7] = int(timeClean)
        send_packet(6, device, 0x61, [timeClean])

        # data_send = cmdString_two(6, device, 200, timeClean)
        # port.write(data_send)

    if event.get('threshold') is not None and event.get('threshold') != '':
        threshold = int(event.get('threshold'))
        df.iloc[0, 7] = int(threshold)

        # data_send = cmdString_two(6, device, 191, threshold)
        # port.write(data_send)

    print("Event: ", event)


def socketio_thread():
    while True:
        if sio.connected:
            events = sio.receive()
            print("SocketIO , events: ", events[1])
            # for event in events:
            #     print("SocketIO event: ", event)
            filter_data(events[1])
        else:
            print("SocketIO not connected, retrying...")
            time.sleep(2)  

# Xong
# Hàm sẽ đọc dữ liệu từ excel trước, nếu đọc không được thì tryền data xuống và lưu vào excel
def first_run():
    
    try:
        get_data_from_file()

    except Exception as e:
        get_setting_data()
        save_data_excel_tb(avg1, avg2, arr_avg1, arr_avg2, value1, value2,threshold_value_1, threshold_value_2, time_clean1,time_clean2)
    # CHờ nhận tín hiệu xong chạy app
    check.start(check_com)
    check.stop()


# Hàm xử lý dữ liệu
def process_data( data_queue):
    while True:
        # Lấy gói dữ liệu từ hàng đợi
        data = data_queue.get()
        if data:
        
            fromID, toID, title, data_receive = data
            

            print("😁😁😁😁😁😁😁😁😁😁😁😁 sensor data: ", data)

            # Xử lý theo toID
    
            if fromID == 0:
             
                sio.emit('device-status-connect', {
                    "device": "0",
                    "isConnected": True,
                    "type": "S"
                })
            
                get_data_com(value1, arr_avg1, data, pin_CB_1)
                print("Data gửi từ cảm biến 1:", value1.get(), pin_CB_1.get(), arr_avg1)
                event.set()

            elif fromID == 1:
                sio.emit('device-status-connect', {
                    "device": "1",
                    "isConnected": True,
                    "type": "S"
                })
                get_data_com(value2, arr_avg2, data, pin_CB_2)
                print("Data gửi từ cảm biến 2: ", value2.get(), pin_CB_2.get(), arr_avg2)
                event.set()

            # Code nhận tín hiệu chuông cũ
            # elif fromID == 7:
            #     print("Check tín hiệu chuông báo!!!")
            #     get_data_button(data)

            elif fromID in [2, 4, 3, 5]:
                print('Dữ liệu chuông báo 👌👌👌👌👌')
                sio.emit('device-status-connect', {
                    "device": int(fromID),
                    "isConnected": True,
                    "type": "B"
                })
                data_send = title
                sio.emit('device-status-running', {
                    "device": int(fromID),
                    "status": data_send,
                    "type": "B"
                })
        else:
            sio.emit('device-status-connect',
                     {
                         "device": "0",
                         "isConnected": False,
                         "type": "S"
                     })
            sio.emit('device-status-connect',
                     {
                         "device": "1",
                         "isConnected": False,
                         "type": "S"
                     })
        data_queue.task_done()


# Hàm nghe tín hiệu,  và xử lý tín hiệu gửi lên
def listen_data_thread(restart_app):
    threading.Thread(target=read_from_port, args=(data_queue, restart_app), daemon=True).start()
    threading.Thread(target=process_data, args=(data_queue,), daemon=True).start()
    

def handle_data_mutate():
    event.wait()
    # Hàm kiểm tra nếu 2 danh sách không trống
    if arr_avg1 or arr_avg2:
        handle_check_mutate( value1, value2, avg1, avg2, threshold_value_1,
                            threshold_value_2, status1, status2, ring_status, pin_CB_1, pin_CB_2)
    event.clear()

# Hàm liên tục thu thập dữ liệu,tính TB khi đủ số lượng
def start_thread():
    if count.get() < 10:
        # Tính trung bình cho mảng đủ độ dài
        if len(arr_avg1) >= 10:
            avg1.set(handleAvg(arr_avg1))
            arr_avg1.clear()
            
        if len(arr_avg2) >= 10:
            avg2.set(handleAvg(arr_avg2))
            arr_avg2.clear()
            
        # Tiếp tục thu thập dữ liệu
        count.set(count.get() + 1)
        connect.start(connect_COM)
        handle_data.start(handle_data_mutate)
        save_data_excel_ngay()
        frame_status.after(time_loop, start_thread)
        
    else:
        handle_data.start(handle_data_mutate)
        
        # Tính trung bình cho từng mảng độc lập
        if len(arr_avg1) >= 10:
            avg1.set(handleAvg(arr_avg1))
            arr_avg1.clear()
        else:
            send_packet(6, 0, 0x54)
            
        if len(arr_avg2) >= 10:
            avg2.set(handleAvg(arr_avg2))
            arr_avg2.clear() 
        else:
            send_packet(6, 1, 0x54)
            
        # Lưu dữ liệu và reset count
        save_data_excel_tb(avg1, avg2, arr_avg1, arr_avg2, value1, value2,
                          threshold_value_1, threshold_value_2, time_clean1, time_clean2)
        count.set(0)
        
        # Đặt thời gian lặp lại phù hợp
        if len(arr_avg1) < 10 or len(arr_avg2) < 10:
            frame_status.after(time_ask_loop, start_thread)
        else:
            frame_status.after(time_loop, start_thread)
            
    print("----------------------------------------------", count.get(),
          "-----------------------------------------------")
    


#   ("Da vao day 🤣🤣🤣🤣🤣🤣🤣🤣🤣🤣🤣🤣🤣🤣🤣")

