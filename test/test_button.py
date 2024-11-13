import RPi.GPIO as GPIO
import time

# Cấu hình các chân GPIO
BUTTON_PIN = 16  # Chân kết nối với nút nhấn
LED_PIN = 18     # Chân kết nối với đèn LED
btnSateBefore = False
# Thiết lập chế độ chân GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)       # Thiết lập chân LED là output
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Thiết lập chân nút nhấn là input với pull-up

try:
    while True:
        # Đọc trạng thái của nút nhấn
        button_state = GPIO.input(BUTTON_PIN)
        if button_state != btnSateBefore and button_state == True:
            GPIO.output(LED_PIN,GPIO.HIGH)
            print("Chuyen doi trang thai Dang bat")
        elif button_state != btnSateBefore and button_state == False :
            GPIO.output(LED_PIN,GPIO.LOW)
            print("Chuyen doi trang thai Dang tat")
        # if button_state == GPIO.LOW:  # Nút được nhấn
        #     GPIO.output(LED_PIN, GPIO.HIGH)  # Bật đèn LED
        #     print("Đang giữ nút")
        # else:  # Nút được thả
        #     GPIO.output(LED_PIN, GPIO.LOW)   # Tắt đèn LED
        #     print("Đã thả nút")
        btnSateBefore = button_state
        time.sleep(0.1)  # Giảm tải CPU
        
except KeyboardInterrupt:
    print("Kết thúc chương trình")
finally:
    GPIO.cleanup()  # Đặt lại trạng thái GPIO
