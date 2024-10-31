from cover.imports import *
from data_processing.data_processing import *
import time as t
from send_UART import *

# hàm tạo nút nhấn
def create_ctk_button(
    root,
    command,
    width,
    height,
    fg_color="#FFF",
    text_color="",
    image="",
    text="",
    border_color="",
    hover_color="",
    imgW=30,
    imgH=30,
):
    pil_image = Image.open(image) if image else None
    img = ctk.CTkImage(pil_image, size=(imgW, imgH)) if pil_image else None
    button = ctk.CTkButton(
        root,
        text=text,
        command=command,
        width=width,
        height=height,
        font=("Consolas", 12, "bold"),
        fg_color=fg_color,
        text_color=text_color,
        border_color=border_color,
        border_width=1,
        image=img,
        hover_color=hover_color,
    )
    return button

# gửi giá trị đột biến và thời gian vệ sinh cảm biến và cập nhật thông tin từ tệp Excel.
def create_frame(root, threshold_value, time_clean, port, sensor_id):

    def send_mutate(new_threshold_value):
        # Set giá trị đột biến cảm biến 1
        data_send = cmdString_two(6, sensor_id, 191, new_threshold_value)
        port.write(data_send)
        t.sleep(2)
        port.write(data_send)
        t.sleep(2)
        port.write(data_send)
        print("Gui gia tri nguong dot bien")

    def send_change_clean(time):
        data_send = cmdString_two(6, sensor_id, 200, time)
        port.write(data_send)
        t.sleep(2)
        port.write(data_send)
        t.sleep(2)
        port.write(data_send)
        print(data_send)
        print("Gui ve sinh")

    def onSubmit():
        try:
            # desktop = os.path.join(os.path.join(
            #     os.environ["USERPROFILE"]), "Desktop")
            output_dir = "C:\cai_dat_catam"
            df = pd.read_excel(os.path.join(output_dir, "cai_dat_catam.xlsx"))

            new_threshold_value = entry3.get()
            if new_threshold_value:
                new_threshold_value = int(new_threshold_value)
                threshold_value.set(new_threshold_value)
            else:
                new_threshold_value = 0
            if new_threshold_value and time.get():
                send_change_clean(time.get())
                send_mutate(new_threshold_value)
                if (sensor_id == 0):
                    df.iloc[0, 7] = int(new_threshold_value)
                    df.iloc[0, 9] = int(time.get())
                else:
                    df.iloc[0, 8] = int(new_threshold_value)
                    df.iloc[0, 10] = int(time.get())
            elif new_threshold_value or time.get():
                if new_threshold_value:
                    send_mutate(new_threshold_value)
                    if (sensor_id == 0):
                        df.iloc[0, 7] = int(new_threshold_value)
                    else:
                        df.iloc[0, 8] = int(new_threshold_value)
                elif time.get():
                    send_change_clean(time.get())
                    if (sensor_id == 0):
                        print("save time clean 1")
                        df.iloc[0, 9] = int(time.get())
                    else:
                        print("save time clean 1")
                        df.iloc[0, 10] = int(time.get())
            if not new_threshold_value and not time.get():
                messagebox.showwarning("Thông báo", f"Không thể lưu giá trị!")
                return
            df.to_excel(os.path.join(
                output_dir, "cai_dat_catam.xlsx"), index=False)
            messagebox.showinfo(
                "Thông báo", f"Đã lưu cài đặt cảm biến { sensor_id + 1} thành công!")
            frame.destroy()
        except Exception as e:
            print(e)

    def onCancel():
        frame.destroy()

    def send_clean():
        send_packet(6,sensor_id,0x53)
        print("đang vệ sinh")
        show_countdown_dialog(
            "Thông báo", f"Đang vệ sinh cảm biến {sensor_id+1}!", 3)

    def show_countdown_dialog(title, message, countdown_time):
        def countdown(count):
            # change text in label        
            label.configure(text=f"{message}\n\n\nClosing in {count} seconds...")
            if count > 0:
                # call countdown again after 1000ms (1s)
                root.after(1000, countdown, count-1)
            else:
                # destroy the window after countdown
                root.destroy()

        root = tk.Toplevel()
        root.geometry(f"320x160+{scrW//2+150}+{scrH//2-200}")
        root.title(title)
        label = ctk.CTkLabel(root, text="", font=("Monserrat", 20, "bold"), text_color="#F78F1E")
        label.pack(fill="both", expand=True, padx=20, pady=40)
        # start countdown
        countdown(countdown_time)
        root.mainloop()

    def handleTake():
        entry2.configure(textvariable=threshold_value)

    frame = ctk.CTkFrame(root, fg_color="white", border_width=1)
    # Điều khiển vệ sinh
    label0 = ctk.CTkLabel(frame, text=f"Cài đặt cảm biến {sensor_id+1}", font=("Monserrat", 30, "bold"), text_color="#2DBD91")
    label0.grid(row=0, column=1, padx=40, pady=20, sticky="w")
    label1 = ctk.CTkLabel(frame, text="Điều khiển vệ sinh", font=(
        "Monserrat", 20, "bold"), text_color="#2DBD91")
    label1.grid(row=1, column=1, padx=40, pady=5, sticky="w")

    buttonClean = create_ctk_button(
        frame,
        command=send_clean,
        width=45,
        height=45,
        text_color="#2DBD91",
        border_color="#2DBD91",
        image="assets/clean.png",
        hover_color="#1b5946",
    )
    buttonClean.grid(row=1, column=2, padx=40, pady=5)
    # Hẹn giờ vệ sinh cảm biến
    label2 = ctk.CTkLabel(frame, text="Hẹn giờ vệ sinh cảm biến", font=(
        "Monserrat", 20, "bold"), text_color="#2DBD91")
    label2.grid(row=2, column=1, padx=40, pady=10, sticky="w")
    # entry1 = ctk.CTkEntry(frame)
    # entry1.grid(row=2, column=1, padx=10, ipadx=50)
    time = ctk.CTkEntry(frame, placeholder_text="  Hẹn giờ vệ sinh cảm biến", state="normal",
                        fg_color="white", font=("Monserrat", 13, "bold"), text_color="#000", height=40)
    time.grid(row=3, column=1, padx=40, pady=10, ipadx=50, sticky="w")
    # Lấy giá trị đột biến
    label3 = ctk.CTkLabel(frame, text="Lấy giá trị đột biến", font=(
        "Monserrat", 20, "bold"), text_color="#2DBD91")
    label3.grid(row=4, column=1, padx=40, pady=10, sticky="w")
    entry2 = ctk.CTkEntry(frame, textvariable="", state="readonly",
                          fg_color="white", font=("Monserrat", 13, "bold"), text_color="#000", height=40)
    entry2.grid(row=5, column=1, padx=40, pady=10, ipadx=50, sticky="w")

    buttonTakeData = create_ctk_button(
        frame,
        command=handleTake,
        width=45,
        height=45,
        text_color="#2DBD91",
        border_color="#2DBD91",
        image="assets/take.png",
        hover_color="#1b5946",
    )

    buttonTakeData.grid(row=5, column=2, padx=40)

    # Cài đặt giá trị đột biến
    label4 = ctk.CTkLabel(frame, text="Cài đặt giá trị đột biến", font=(
        "Monserrat", 20, "bold"), text_color="#2DBD91")
    label4.grid(row=6, column=1, padx=40, ipady=10, sticky="w")
    entry3 = ctk.CTkEntry(frame, placeholder_text="  Cài đặt giá trị đột biến",
                          fg_color="white", font=("Monserrat", 13, "bold"), text_color="#000", height=40)
    entry3.grid(row=7, column=1, padx=40, pady=10, ipadx=50, sticky="w")


    buttonSubmit = create_ctk_button(
        frame,
        image="assets/check.png",
        command=onSubmit,
        width=90,
        height=40,
        imgW=80,
        imgH=40,
        fg_color="#2DBD91",
        text_color="#FFFFFF",
        hover_color="#1b5946",
    )
    buttonSubmit.grid(row=7, column=2)

    return frame
