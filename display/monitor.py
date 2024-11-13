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
        font=("Arial", 12, "bold"),
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
        # data_send = cmdString_two(6, sensor_id, 191, new_threshold_value)

        send_packet(6, sensor_id, 0x44, [new_threshold_value])
 
        print(f"😁Gui gia tri nguong dot bien 😁, new_threshold_value: {new_threshold_value}")

    def send_change_clean(time_change_lean):

        # data_send = cmdString_two(6, sensor_id, 200, time_clean_button)
        send_packet(6, sensor_id, 0x61,[time_change_lean])

        print(f"😁 Gui thoi gian ve sinh 😁, time_change_lean: {time_change_lean}")

    def onSubmit():
        try:

            output_dir = "/home/ailab/Downloads/luu_ca_tam"
            df = pd.read_excel(os.path.join(output_dir, "cai_dat_catam.xlsx"))

            new_threshold_value = entry3.get()
            if new_threshold_value:
                new_threshold_value = int(new_threshold_value)
            else:
                new_threshold_value = 0
            time_clean_change = time_clean_button.get()
            
            if time_clean_change.isdigit():  
                time_clean_change = int(time_clean_change) 

            if new_threshold_value and time_clean_change:

                send_change_clean(time_clean_change)

                send_mutate(new_threshold_value)

                if (sensor_id == 0):
                    df.iloc[0, 7] = int(new_threshold_value)
                    df.iloc[0, 9] = int(time_clean_change)
                else:
                    df.iloc[0, 8] = int(new_threshold_value)
                    df.iloc[0, 10] = int(time_clean_change)

                    
            elif new_threshold_value or time_clean_change:
                if new_threshold_value:
                    send_mutate(new_threshold_value)
                    if (sensor_id == 0):
                        df.iloc[0, 7] = int(new_threshold_value)
                    else:
                        df.iloc[0, 8] = int(new_threshold_value)
                elif time_clean_change:
                    send_change_clean(time_clean_change)
                    if (sensor_id == 0):
                        print("save time clean 1")
                        df.iloc[0, 9] = int(time_clean_change)
                    else:
                        print("save time clean 1")
                        df.iloc[0, 10] = int(time_clean_change)

            if not new_threshold_value and not time_clean_change:
                messagebox.showwarning("Thong bao", f"Khong the luu gia tri!")
                return
        ## Lưu Dữ liệu mới vào cài đặt excel
            df.to_excel(os.path.join(
                output_dir, "cai_dat_catam.xlsx"), index=False)
            messagebox.showinfo(
                "Thong bao", f"Da luu { sensor_id + 1} thanh cong!")
            # frame.destroy()
        except Exception as e:
            print(e)
            messagebox.showerror("Loi", f"Da xay ra loi: {e}")


    def onCancel():
        frame.destroy()

    def send_clean():
        send_packet(6,sensor_id,0x53)
        print("dang ve sinh")
        show_countdown_dialog(
            "Thong bao", f"Dang ve sinh cam bien {sensor_id+1}!", 3)

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
        label = ctk.CTkLabel(root, text="", font=("Arial", 20, "bold"), text_color="#F78F1E")
        label.pack(fill="both", expand=True, padx=20, pady=40)
        # start countdown
        countdown(countdown_time)
        root.mainloop()

    def handleTake():
        entry2.configure(textvariable=threshold_value)

    frame = ctk.CTkFrame(root, fg_color="white", border_width=1)

    # Điều khiển vệ sinh
    label0 = ctk.CTkLabel(frame, text=f"Cai dat cam bien {sensor_id+1}", font=("Arial", 20, "bold"), text_color="#2DBD91")
    label0.grid(row=0, column=1, padx=20, pady=20, sticky="w")
    label1 = ctk.CTkLabel(frame, text="Đieu khien ve sinh", font=(
        "Arial", 20, "bold"), text_color="#2DBD91")
    label1.grid(row=1, column=1, padx=20, pady=5, sticky="w")

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
    buttonClean.grid(row=1, column=2, padx=20, pady=5)

    # Hẹn giờ vệ sinh cảm biến
    label2 = ctk.CTkLabel(frame, text="Hen gio ve sinh cam bien", font=("Arial", 20, "bold"), text_color="#2DBD91")
    label2.grid(row=2, column=1, padx=20, pady=10, sticky="w")
    
    time_clean_button = ctk.CTkEntry(frame, placeholder_text="  Hen gio ve sinh cam bien", state="normal",
                        fg_color="white", font=("Arial", 13, "bold"), text_color="#000", height=40)
    time_clean_button.grid(row=3, column=1, padx=20, pady=10, ipadx=50, sticky="w")

    # Lấy giá trị đột biến
    label3 = ctk.CTkLabel(frame, text="Lay gia tri dot bien", font=(
        "Arial", 20, "bold"), text_color="#2DBD91")
    label3.grid(row=4, column=1, padx=20, pady=10, sticky="w")

    entry2 = ctk.CTkEntry(frame, textvariable="", state="readonly",fg_color="white", font=("Arial", 13, "bold"), text_color="#000", height=40)
    entry2.grid(row=5, column=1, padx=20, pady=10, ipadx=50, sticky="w")

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

    buttonTakeData.grid(row=5, column=2, padx=20)

    # Cài đặt giá trị đột biến
    label4 = ctk.CTkLabel(frame, text="Cai dat gia tri dot bien", font=("Arial", 25, "bold"), text_color="#2DBD91")
    label4.grid(row=6, column=1, padx=20, ipady=10, sticky="w")

    entry3 = ctk.CTkEntry(frame, placeholder_text="  Cai dat gia tri dot bien",fg_color="white", font=("Arial", 13, "bold"), text_color="#000", height=40)
    entry3.grid(row=7, column=1, padx=20, pady=10, ipadx=50, sticky="w")


    buttonSubmit = create_ctk_button(
        frame,
        image="assets/check.png",
        command=onSubmit,
        width=70,
        height=40,
        imgW=70,
        imgH=40,
        fg_color="#2DBD91",
        text_color="#FFFFFF",
        hover_color="#1b5946",
    )
    buttonSubmit.grid(row=7, column=2)


    return frame
