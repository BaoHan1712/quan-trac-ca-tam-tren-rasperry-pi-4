from cover.imports import tk, serial, ctk, time, threading
import socketio
from cover.imports import *

#--Nếu mất kết nối,sẽ tự động cố gắng kết nối lại với cổng------------------

# Tìm cổng  và kêt nối
def connect_to_first_comport():
    ports = serial.tools.list_ports.comports()
    if ports:
        if ports[0].device:
            return ports[0].device
    print("Không tìm thấy cổng COM")
    return None  # Trả về None nếu không tìm thấy cổng

"""" Hàm restart app """
def restart_app():
    python = sys.executable
    os.execl(python, python, * sys.argv)

port = None

# Hàm kiểm tra kết nối và cố gắng kết nối lại
def check_connection():
    while True:
        comport = connect_to_first_comport()
        if comport: 
            if comport == "COM8":
                try:
                    port = serial.Serial(comport, 9600, timeout=1, bytesize=serial.EIGHTBITS)
                    print(f"Đã kết nối đến {port}")
                    restart_app()  
                    return port  
                except serial.SerialException as e:
                    print(f"Lỗi khi mở cổng {comport}: {e}")
                    time.sleep(3)  
            else:
                print(f"Cổng {comport} không phải là COM8. Kết nối lại!!!")
                time.sleep(3)  
        else:
            print("Không tìm thấy cổng COM nào. Thử lại sau 3 giây...")
            time.sleep(3)  

try:
    port = serial.Serial("COM8", 9600, timeout=1, bytesize=serial.EIGHTBITS)
except serial.SerialException as e:
    connect_thread = threading.Thread(target=check_connection, daemon=True)
    connect_thread.start()



sio = None
port_lock = threading.Lock()
event = threading.Event()
url = 'http://192.168.1.75:3005'
id_center = '669f780fccd89d46cefb5735'

try:
    sio = socketio.SimpleClient()

    """ Server Deploy IP: https://api.catam.thomi.com.vn  """
    """ Server Local IP: http://192.168.1.75:3005  """
    """ Local IP: http://192.168.1.42:5005  """

    sio.connect('https://api.catam.thomi.com.vn',
                transports=['websocket'], namespace='/center')
    sio.emit('connection', id_center)
    print(sio.connected)
    print("Connected successfully")
except socketio.exceptions.ConnectionError as e:
    print(f"Connection failed: {e}")



#-------------------------------------------Giao Diện------------------------------------------------
root = ctk.CTk()
time_loop = 5 * 1000
time_ask_loop = 2 * 1000
scrW = root.winfo_screenwidth()
scrH = root.winfo_screenheight()
root.title("APP CÁ TẦM")

# Biến trạng thái
threshold_value_1 = tk.IntVar(value=40)
threshold_value_2 = tk.IntVar(value=40)
status1 = tk.StringVar(value="Bình thường")
status2 = tk.StringVar(value="Bình thường")
value1 = tk.IntVar()
value2 = tk.IntVar()
mutation_value_1 = tk.IntVar()
mutation_value_2 = tk.IntVar()

# Các biến khác
arr_avg1 = []
arr_avg2 = []

avg1 = tk.IntVar(value=212)
avg2 = tk.IntVar(value=220)
count = tk.IntVar(value=0)
ring_status = tk.StringVar(value="Đang Tắt")
button_status = tk.IntVar()
time_clean1 = tk.IntVar(value=10)
time_clean2 = tk.IntVar(value=10)
first_run_bool = tk.BooleanVar(root, True)
pass_login = tk.StringVar(value="ctydaphu")

frame_main = ctk.CTkFrame(root, fg_color="white", bg_color="white", height=1080, width=1920)
frame_body_main = ctk.CTkFrame(frame_main, fg_color="white", height=780, width=1920)
frame = ctk.CTkFrame(frame_body_main, fg_color="white", bg_color="white", width=960)
frame_header = ctk.CTkFrame(frame_main, fg_color="white", bg_color="white", height=100)
frame_body = ctk.CTkFrame(frame, fg_color="white", bg_color="white", width=960)
frame_status = ctk.CTkFrame(frame_body, fg_color="white", bg_color="white", width=960, height=780,)
frame_status_1 = ctk.CTkFrame(frame_status, fg_color="#FF911A", corner_radius=10)
frame_status_2 = ctk.CTkFrame(frame_status, fg_color="#FF911A", height=500, width=960, corner_radius=10)
frame_chart = ctk.CTkFrame(frame_body_main, fg_color="white")
frame_chart_1 = ctk.CTkFrame(frame_chart)
frame_chart_2 = ctk.CTkFrame(frame_chart, fg_color="white", bg_color="white")
frame_footer = ctk.CTkFrame(frame_main, fg_color="white", bg_color="white", height=100, width=1920)
frame_setting = ctk.CTkFrame(frame_body, fg_color="white", bg_color="white")
