from cover.imports import *
from data_processing.data_processing import *
from serial_communication import *
from display.monitor import create_frame
from threads import *
from check_com.checkCom_global import *



def main():
    """ Tạo UI chính"""
    global root, frame
    # root.geometry(f"1890x1000+{scrW//2-970}+{scrH//2-540}")
    root.geometry(f"1890x1000+{(scrW-1890)//2}+{(scrH-1000)//2}")

    # root.iconphoto("assets/icon.ico")
    img_save = Image.open("assets/save.png")
    button_save_img = ctk.CTkImage(img_save, size=(200, 100))

    img_header = Image.open("assets/header.png")
    img_header = img_header.resize((1890, 100))
    header_photo = ImageTk.PhotoImage(img_header)
    header = tk.Canvas(frame_header, bg="white",
                       highlightthickness=0, height=80)
    header.pack(fill="x")
    header.create_image(40, 0, image=header_photo, anchor="nw")

    chart_img = Image.open("assets/chart.png")
    chart_img = chart_img.resize((820, 660))
    chart_photo = ImageTk.PhotoImage(chart_img)
    chart = tk.Canvas(frame_chart_1, bg="white",
                      highlightthickness=0, height=640)
    chart.pack(fill="both", expand=True)
    chart.create_image(0, 0, image=chart_photo, anchor="nw")

    img_footer = Image.open("assets/footer.png")
    img_footer = img_footer.resize((1890, 60))
    footer_photo = ImageTk.PhotoImage(img_footer)
    footer = tk.Canvas(frame_footer, bg="white",
                       highlightthickness=0, height=100)
    footer.pack(fill="x")
    footer.create_image(0, 20, image=footer_photo, anchor="nw")

    # Header labels
    L1 = ctk.CTkLabel(frame_status_2, 
                      text="Do Duc",
                      font=("Arial", 25, "bold"),
                      text_color="white",
                      width=150,
                      anchor="center")
    L1.grid(row=0, column=0, sticky="ew", pady=5, padx=10)

    L2 = ctk.CTkLabel(frame_status_2, 
                      text="Trang Thai",
                      font=("Arial", 25, "bold"),
                      text_color="white", 
                      width=150,
                      anchor="center")
    L2.grid(row=0, column=1, sticky="ew", pady=5, padx=10)

    L3 = ctk.CTkLabel(frame_status_2, 
                      text="Pin",
                      font=("Arial", 25, "bold"),
                      text_color="white",
                      width=150,
                      anchor="center")
    L3.grid(row=0, column=2, sticky="ew", pady=5, padx=10)

    # Sensor 1 label
    L4 = ctk.CTkLabel(frame_status_2, 
                      text="Cam bien 1",
                      font=("Arial", 20, "bold"),
                      fg_color="#FF911A",
                      text_color="white",
                      width=150,
                      anchor="center")
    L4.grid(row=1, column=1, sticky="ew", pady=5, padx=10)
    
    ring = ctk.CTkLabel(frame_status_1, 
                        text="Chuông báo",
                        font=("Arial", 20, "bold"), 
                        fg_color="#FF911A", 
                        text_color="white",
                        width=150,
                        anchor="center")
    ring.pack(fill="x", side="left", pady=5, padx=10)

    # Sensor 1 values
    entry1 = ctk.CTkLabel(frame_status_2,
                          textvariable=value1,
                          text_color="white",
                          font=("Arial", 20, "bold"),
                          width=150,
                          anchor="center")
    entry1.grid(row=3, column=0, sticky="ew", padx=10, pady=8)

    entry2 = ctk.CTkLabel(frame_status_2,
                          textvariable=status1,
                          text_color="white", 
                          font=("Arial", 20, "bold"),
                          width=150,
                          anchor="center")
    entry2.grid(row=3, column=1, sticky="ew", padx=10, pady=8)

    entry3 = ctk.CTkLabel(frame_status_2,
                          textvariable=pin_CB_1,
                          text_color="white",
                          font=("Arial", 20, "bold"),
                          width=150,
                          anchor="center")
    entry3.grid(row=3, column=2, sticky="ew", padx=10, pady=8)

    # Sensor 2 label
    L5 = ctk.CTkLabel(frame_status_2, 
                      text="Cam bien 2",
                      font=("Arial", 20, "bold"),
                      fg_color="#FF911A",
                      text_color="white",
                      width=150,
                      anchor="center")
    L5.grid(row=4, column=1, sticky="ew", pady=5, padx=10)

    # Sensor 2 values
    entry4 = ctk.CTkLabel(frame_status_2,
                         textvariable=value2,
                         text_color="white",
                         font=("Arial", 20, "bold"),
                         width=150,
                         anchor="center")
    entry4.grid(row=6, column=0, sticky="ew", padx=10, pady=8)

    entry5 = ctk.CTkLabel(frame_status_2,
                         textvariable=status2,
                         text_color="white",
                         font=("Arial", 20, "bold"),
                         width=150,
                         anchor="center")
    entry5.grid(row=6, column=1, sticky="ew", padx=10, pady=8)

    entry6 = ctk.CTkLabel(frame_status_2,
                         textvariable=pin_CB_2,
                         text_color="white",
                         font=("Arial", 20, "bold"),
                         width=150,
                         anchor="center")
    entry6.grid(row=6, column=2, sticky="ew", padx=10, pady=8)

    entry_ring = ctk.CTkLabel(frame_status_1,
                             textvariable=ring_status,
                             text_color="white",
                             font=("Arial", 20, "bold"),
                             width=150,
                             anchor="center")
    entry_ring.pack(fill="both", side="right", padx=12, pady=8)

    button_save = ctk.CTkButton(
        frame_chart_2,
        text="",
        image=button_save_img,
        command=export_excel, 
        fg_color="white",
        hover=False,
    ).pack(side="left")

    # Hàm gửi giá trị đột biến và thời gian vệ sinh cảm biến
    frame1 = create_frame(frame_setting, threshold_value_1, time_clean1, port, 0)

    frame1.pack(fill="both", expand=True, side="left", padx=5)

    # Hàm gửi giá trị đột biến và thời gian vệ sinh cảm biến
    frame2 = create_frame( frame_setting, threshold_value_2, time_clean2, port, 1 )

    frame2.pack(fill="both", expand=True, side="right", padx=5)

    frame_main.pack(fill="both", expand=True)
    frame_header.pack_propagate(0)
    frame_header.pack(fill="x", side="top")
    frame_body_main.pack_propagate(0)
    frame_body_main.pack(fill="both", expand=True, pady=20)
    frame.pack_propagate(0)

    # Bố cục bên phải
    frame.pack(fill="both", side="right", padx=50)
    frame_body.pack(fill="both", expand=True, side="right")
    frame_status.pack(fill="both", side="top", padx=5)
    frame_status_1.pack(fill="both")
    frame_status_2.pack(fill="both", expand=True, pady=20)
    frame_setting.pack(fill="both", expand=True, side="bottom")
    frame_chart.pack_propagate(0)
    frame_chart.pack(fill="both", expand=True, side="left", padx=20)
    frame_chart_1.pack(fill="both", side="top")
    frame_chart_2.pack(fill="both", side="bottom")
    frame_footer.pack_propagate(0)
    frame_footer.pack(fill="both", side="bottom")

    def on_closing():
        global port
        if port is not None and port.is_open:
            port.close()
            print("on clossing")
        root.destroy()

    if port and port.is_open:
        for i in range(2):
            if first_run_bool.get():

            # Tự động chạy khi máy được bật
                # add_to_startup()
            
        # Hàm chờ nhận tín hiệu từ dưới gửi lên mới mở app
                first_run()
                first_run_bool.set(False)
            else:
        # Nếu khong kết nối được thì restart lại
        # Còn cần sửa tiếp
                # check_button_on(port)
                listen_data_thread(restart_app)
                websocket_thread.start(socketio_thread)
                start_thread()
                listen_off.start(check_sensor_status)
                button_dung.start(press_button)
                break
    else:
        print("fail")

    frame_status_1.grid_columnconfigure("all", weight=1)
    frame_status_2.grid_columnconfigure("all", weight=1)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


# Gán hàm on_closing cho sự kiện đóng cửa sổ
if __name__ == "__main__":
    main()

# Cần sửa lại đường dẫn ở threads và monitor, data_processing|| cai_dat_catam
