from cover.imports import *
from data_processing.data_processing import *
from serial_communication import *
from display.monitor import create_frame
from threads import *
from check_com.checkCom_global import *


def main():
    """ Tạo UI chính"""
    global root, frame
    # root.geometry(f"1920x1000+{scrW//2-970}+{scrH//2-540}")
    root.geometry(f"1920x1000+{scrW//2-2000}+{scrH//2-500}")
    root.iconbitmap("assets/icon.ico")
    img_save = Image.open("assets/save.png")
    button_save_img = ctk.CTkImage(img_save, size=(200, 100))

    img_header = Image.open("assets/header.png")
    img_header = img_header.resize((1920, 100))
    header_photo = ImageTk.PhotoImage(img_header)
    header = tk.Canvas(frame_header, bg="white",
                       highlightthickness=0, height=100)
    header.pack(fill="x")
    header.create_image(40, 0, image=header_photo, anchor="nw")

    chart_img = Image.open("assets/chart.png")
    chart_img = chart_img.resize((880, 640))
    chart_photo = ImageTk.PhotoImage(chart_img)
    chart = tk.Canvas(frame_chart_1, bg="white",
                      highlightthickness=0, height=640)
    chart.pack(fill="both", expand=True)
    chart.create_image(0, 0, image=chart_photo, anchor="nw")

    img_footer = Image.open("assets/footer.png")
    img_footer = img_footer.resize((1920, 60))
    footer_photo = ImageTk.PhotoImage(img_footer)
    footer = tk.Canvas(frame_footer, bg="white",
                       highlightthickness=0, height=100)
    footer.pack(fill="x")
    footer.create_image(0, 20, image=footer_photo, anchor="nw")

    L1 = ctk.CTkLabel(frame_status_2, text="Trạng thái cảm biến 1",
                      font=("Monserrat", 22, "bold"), fg_color="#FF911A", text_color="white")
    L1.grid(row=0, column=0, sticky="w", pady=7, ipady=7, padx=10, ipadx=10)
    L2 = ctk.CTkLabel(frame_status_2, text="Giá trị cảm biến 1",
                      font=("Monserrat", 22, "bold"), fg_color="#FF911A", text_color="white")
    L2.grid(row=1, column=0, sticky="w", pady=7, ipady=7, padx=10, ipadx=10)
    L3 = ctk.CTkLabel(frame_status_2, text="Trạng thái cảm biến 2",
                      font=("Monserrat", 22, "bold"), fg_color="#FF911A", text_color="white")
    L3.grid(row=2, column=0, sticky="w", pady=7, ipady=7, padx=10, ipadx=10)
    L4 = ctk.CTkLabel(frame_status_2, text="Giá trị cảm biến 2",
                      font=("Monserrat", 22, "bold"), fg_color="#FF911A", text_color="white")
    L4.grid(row=3, column=0, sticky="w", pady=7, ipady=7, padx=10, ipadx=10)
    L5 = ctk.CTkLabel(frame_status_1, text="Chuông báo",
                      font=("Monserrat", 22, "bold"), fg_color="#FF911A", text_color="white")
    L5.pack(fill="both", side="left", pady=7, ipady=7, padx=10, ipadx=10)

    entry = ctk.CTkLabel(
        frame_status_2, textvariable=status1, text_color="white", font=("Monserrat", 22, "bold"))
    entry.grid(row=0, column=1, sticky="e", padx=10, pady=10)
    entry1 = ctk.CTkLabel(
        frame_status_2, textvariable=value1, text_color="white", font=("Monserrat", 22, "bold"))
    entry1.grid(row=1, column=1, sticky="e", padx=10, pady=10)
    entry3 = ctk.CTkLabel(
        frame_status_2, textvariable=status2, text_color="white", font=("Monserrat", 22, "bold"))
    entry3.grid(row=2, column=1, sticky="e", padx=10, pady=10)
    entry4 = ctk.CTkLabel(
        frame_status_2, textvariable=value2, text_color="white", font=("Monserrat", 22, "bold"))
    entry4.grid(row=3, column=1, sticky="e", padx=10, pady=10)
    entry5 = ctk.CTkLabel(
        frame_status_1, textvariable=ring_status, text_color="white", font=("Monserrat", 22, "bold"))
    entry5.pack(fill="both", side="right", padx=10, pady=10)


    button_save = ctk.CTkButton(
        frame_chart_2,
        text="",
        image=button_save_img,
        command=export_excel,
        fg_color="white",
        hover=False,
    ).pack(side="left")

   
    # Hàm gửi giá trị đột biến và thời gian vệ sinh cảm biến
    frame1 = create_frame(frame_setting, threshold_value_1, time_clean1, port, sensor_id=0)

    frame1.pack(fill="both", expand=True, side="left", padx=5)

    # Hàm gửi giá trị đột biến và thời gian vệ sinh cảm biến
    frame2 = create_frame( frame_setting, threshold_value_2, time_clean2, port, sensor_id=1 )

    frame2.pack(fill="both", expand=True, side="right", padx=5)

    frame_main.pack(fill="both", expand=True)
    frame_header.pack_propagate(0)
    frame_header.pack(fill="x", side="top")
    frame_body_main.pack_propagate(0)
    frame_body_main.pack(fill="both", expand=True, pady=20)
    frame.pack_propagate(0)
    frame.pack(fill="both", side="right", padx=20)
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