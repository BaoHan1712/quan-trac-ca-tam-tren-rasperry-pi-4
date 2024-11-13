from data_processing.data_processing import *
from cover.imports import *
from check_com.checkCom_global import *
from send_UART import *
import RPi.GPIO as GPIO


# Đặt khoảng giá trị đột biến
def get_setting_data():
    send_packet(6, 0,0x44)
    send_packet(6, 1,0x44)


# Biến toàn cục để theo dõi trạng thái
SENSOR1_STATUS = "Online"
SENSOR2_STATUS = "Online"
last_update_times = [None] * 6

def update_sensor_time(sensor_id):
    """Cập nhật thời gian nhận tín hiệu cuối cùng của cảm biến"""
    global last_update_times
    last_update_times[sensor_id] = time.time()

def check_led_status():
    global LOW_BATTERY_LED
    
    # Kiểm tra pin
    battery_ok = pin_CB_1.get() >= 15 and pin_CB_2.get() >= 15
    battery_low = pin_CB_1.get() < 15 or pin_CB_2.get() < 15
    
    # Kiểm tra trạng thái offline
    sensors_offline = (status1.get() == "Offline" or status2.get() == "Offline")
    
    # Kiểm tra trạng thái bình thường
    sensors_normal = (status1.get() == "Bình Thuong" and status2.get() == "Bình Thuong")
    
    # Bật đèn khi:
    # 1. Một trong hai cảm biến offline
    # 2. Cả 1 trong 2 pin đều yếu (<15)
    if sensors_offline or battery_low:
        turn_on_led()
        LOW_BATTERY_LED = True
        print("Bật đèn do:")
        if sensors_offline:
            print(f"Có cảm biến offline - CB1={status1.get()}, CB2={status2.get()}")
        if battery_low:
            print(f"Pin yếu - CB1={pin_CB_1.get()}, CB2={pin_CB_2.get()}")
        return False
        
    # Tắt đèn khi tất cả điều kiện bình thường
    if battery_ok and sensors_normal:
        turn_off_led()
        LOW_BATTERY_LED = False
        print("Tất cả trạng thái bình thường - Tắt đèn")
        print(f"Trạng thái cảm biến: CB1={status1.get()}, CB2={status2.get()}")
        print(f"Pin cảm biến: CB1={pin_CB_1.get()}, CB2={pin_CB_2.get()}")
        return True
        
    # Giữ nguyên trạng thái đèn trong các trường hợp khác
    return False

time_offline =(time_loop/1000 * 2 + 5)
def check_sensor_status():
    global SENSOR1_STATUS, SENSOR2_STATUS
    while True:
        current_time = time.time()
        status_changed = False
        
        for i, last_time in enumerate(last_update_times):
            if last_time is None or current_time - last_time > time_offline:
                if i == 0:
                    SENSOR1_STATUS = "Offline"
                    # Luôn set offline khi mất kết nối, kể cả đang ở trạng thái nước đục
                    status1.set("Offline")
                    status_changed = True
                elif i == 1:
                    SENSOR2_STATUS = "Offline"
                    # Luôn set offline khi mất kết nối, kể cả đang ở trạng thái nước đục  
                    status2.set("Offline")
                    status_changed = True
            else:
                if i == 0 and status1.get() == "Offline":
                    SENSOR1_STATUS = "Online"
                    status1.set("Bình Thuong")
                    status_changed = True
                elif i == 1 and status2.get() == "Offline":
                    SENSOR2_STATUS = "Online" 
                    status2.set("Bình Thuong")
                    status_changed = True
                    
        # Chỉ kiểm tra LED khi có thay đổi trạng thái
        if status_changed:
            check_led_status()
            
        time.sleep(1)

# Hàm quan trọng nhận dữ liệu rôi xử lý
def get_data_com(value, arr_avg, sensor, pin_cb):
    # Check dữ liệu từ cảm biến
    print("❤️❤️❤️❤️❤️❤️❤️❤️", sensor)
 
    fromID, toID, title, data_receive = sensor
    
    # # Thêm kiểm tra data_receive
    # if not data_receive or len(data_receive) < 2:
    #     print("Không nhận được dữ liệu hợp lệ từ cảm biến")
    #     return
        
    data = data_receive[0]
    pin = data_receive[1]
    id = fromID
    status = title
    
    if (data):
        update_sensor_time(id)
        if (status == 0x57):
            if (id ==  0):
                print("da luu vao excel  ❤️   voi id 0")
                save_data_excel_ngay(None, None, data, None)

            elif (id == 1):
                print("da luu vao excel  ❤️   voi id 1")
                save_data_excel_ngay(None, None, None, data)

    #______________________________ Thông Báo sáng đèn khi gần hết pin___________________
        elif (status == 0x54):
           
            if (id == 0):
                value.set(data)
                arr_avg.append(data)
                pin_CB_1.set(pin)
                if (pin_CB_1.get()) < 15:
                    turn_on_led()
                    print("💥Thông báo gần hết pin CB1 💥")
                else:
                    check_led_status()

            elif (id == 1):
                value.set(data)
                arr_avg.append(data)
                pin_CB_2.set(pin)
                if pin_CB_2.get() < 15:
                    turn_on_led()
                    print("💥Thông báo gần hết pin CB2 💥")
                else:
                    check_led_status()

        elif (status == 192):
            if (id == 0):
                threshold_value_1.set(data)
            elif (id == 1):
                threshold_value_2.set(data)

        elif (status == 0x44):
            if (id == 0):
                print("Da nhan duoc gia tri nguong dot bien CB1 😁😁")
                sio.emit('threshold-device', {
                    "device": int(id),
                    "threshold": data,
                    "type": "S"
                })
            elif (id == 1):
                print("Da nhan duoc gia tri nguong dot bien CB2 😁😁")
                sio.emit('threshold-device', {
                    "device": int(id),
                    "threshold": data,
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
            print("Đã vào đây 😘😘😘😘😘😘😘😘😘😘")
            sio.emit('device-status-running', {
                "device": int(id),
                "status": 1,
                "type": "S"
            })

# Thiết lập GPIO
BUTTON_PIN = 16  # The number of the pushbutton pin
LED_PIN = 18     # The number of the LED pin

pressed_once = False
BUTTON_PRESSED = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)          
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.output(LED_PIN, GPIO.LOW)  # Khởi tạo LED ở trạng thái tắt

# Xong
def press_button():
    global pressed_once, LOW_BATTERY_LED, BUTTON_PRESSED
    try:    
        while True:
            button_state = GPIO.input(BUTTON_PIN)
            
            # Khi nút được nhấn và trạng thái trước đó là False (chưa nhấn)
            if button_state != pressed_once and button_state == True:
                BUTTON_PRESSED = True
                turn_off_ring()
                ring_status.set("Đang Tat")
                print("Chuyen doi trang thai sang bat")
                
            # Khi nút được thả ra    
            elif button_state != pressed_once and button_state == False:
                BUTTON_PRESSED = False
                print("Chuyển đổi trạng thái Đang tắt")
                
                
            time.sleep(0.1)
            pressed_once = button_state

    except KeyboardInterrupt:
        print("kết thúc")
    finally:
        GPIO.cleanup()

# Thêm các biến toàn cục mới
RING_ACTIVE = False

# Hàm bật chuông ||| xong
def turn_on_ring():
    global RING_ACTIVE, BUTTON_PRESSED
    
    # Kiểm tra nút nhấn trước khi bật chuông
    if BUTTON_PRESSED == True:
        print("Không gửi lệnh bật chuông vì nút đang được nhấn")
        return
        
    # Chỉ bật chuông nếu chưa được bật
    if not RING_ACTIVE:
        RING_ACTIVE = True
        send_packet(6, 7, 0x6F)
        ring_status.set("Đang Bat")
        print("Gửi lệnh bật chuông 🔔")
    else:
        print("Không gửi lệnh bật chuông vì trạng thái chuông đang bật")

LOW_BATTERY_LED = False
def turn_off_led():
    global LOW_BATTERY_LED
    LOW_BATTERY_LED = False
    GPIO.output(LED_PIN, GPIO.LOW)
    print("Tắt đèn - LOW_BATTERY_LED:", LOW_BATTERY_LED)

def turn_on_led():
    global LOW_BATTERY_LED
    LOW_BATTERY_LED = True
    GPIO.output(LED_PIN, GPIO.HIGH)



# Hàm tắt chuông||| Xong
def turn_off_ring():
    global RING_ACTIVE
    if RING_ACTIVE:
        send_packet(6, 7, 0x66)
        ring_status.set("Đang Tat")
        print("Tắt Chuông báo ❌🔔")
        
        # Reset trạng thái chuông về ban đầu
        RING_ACTIVE = False


# Xong ||| Gửi dữ liệu cho cả hai cảm biến và đọc phản hồi liên tục
def connect_COM():
    for sensor_id in (0, 1):
        send_packet(6, sensor_id, 0x54)
        time.sleep(2)


# Hàm kiểm tra cng || Xong
def check_com():
    send_packet(6, 0, 0x54)
    print("đang chờ nhận tín hiệu để mở app")
    receive_packet_all()
    

value_compare_list_1 = []


def handle_check_mutate(value1, value2, avg1, avg2, threshold_value_1, threshold_value_2, status1, status2, ring_status, pin_cb1, pin_cb2):
    check_1 = False
    check_2 = False
    value_compare_1 = 0
    value_compare_2 = 0
    global value_compare_list_1 
    global value_compare_list_2

    # Xử lý cảm biến 1 độc lập
    if SENSOR1_STATUS == "Online":
        value_compare_1 = value1.get() - avg1.get()
        if value_compare_1 > threshold_value_1.get():
            print("❌CB1 Da nhan ĐB lan 1 ")
            value_compare_list_1.append(value_compare_1)
        else:
            status1.set("Bình Thuong")
            sio.emit('water-status', {
                "sensor": "0",
                "status": "C" 
            })
    
        if len(value_compare_list_1) == 2:
            if all(value > threshold_value_1.get() for value in value_compare_list_1):
                check_1 = True
                sio.emit('water-status', {
                    "sensor": "0", 
                    "status": "D"
                })
                mutation_value_1.set(value_compare_1)
                status1.set("Nuoc Duc")
                print("Cảm biến 1: Cả hai lần hỏi đều vượt ngưỡng 🔔🔔")
                value_compare_list_1.clear()
                
    if SENSOR2_STATUS == "Offline" and check_1:
        print("Cảm biến 1 đột biến, cảm biến 2 offline - Bật chuông và đèn") 
        turn_on_ring()
        turn_on_led()


    # Xử lý cảm biến 2 - chỉ cần 1 lần vượt ngưỡng
    value_compare_2 = value2.get() - avg2.get()
    if value_compare_2 > threshold_value_2.get():
        check_2 = True
        sio.emit('water-status', {
            "sensor": "1",
            "status": "D"
        })
        mutation_value_2.set(value_compare_2)
        status2.set("Nuoc Duc")
        print("Cảm biến 2: Đã vượt ngưỡng 🔔")
        
        if SENSOR1_STATUS == "Offline":
            print("Cảm biến 2 đột biến, cảm biến 1 offline - Bật chuông và đèn") 
            turn_on_ring()
            turn_on_led()
    else:
        if SENSOR2_STATUS == "Online":
            status2.set("Bình Thuong")
            sio.emit('water-status', {
                "sensor": "1", 
            "status": "C"
        })

    # Bật chuông nếu cả 2 cảm biến cùng đục
    if check_1 and check_2:
        print("Cả 2 cảm biến đều đột biến 💥💥💥💥💥💥💥💥💥💥💥💥")
        ring_status.set("Đang Bat")
        turn_on_ring()
        turn_on_led()

    print("Giá trị trung bình cảm biến 1:", avg1.get())
    print("Giá trị trung bình cảm biến 2:", avg2.get()) 
    print("Giá trị đột biến 1:", value_compare_1)
    print("Giá trị đột biến 2:", value_compare_2)

""" Hàm Khởi động cùng máy tính"""

# Thay bằng đường dẫn Python.
def add_to_startup():
    # Tạo thư mục autostart nếu chưa tồn tại
    autostart_dir = os.path.expanduser("~/.config/autostart")
    if not os.path.exists(autostart_dir):
        os.makedirs(autostart_dir)

    # Tạo file .desktop
    desktop_entry = os.path.join(autostart_dir, "catam_gui.desktop")
    with open(desktop_entry, "w") as file:
        file.write(f"""[Desktop Entry]
Type=Application
Name=App_Ca_tam
Exec=python3 {os.path.abspath("main.py")}  
StartupNotify=false
Terminal= True
""")
    print("File startup đã được tạo thành công tại", desktop_entry)




