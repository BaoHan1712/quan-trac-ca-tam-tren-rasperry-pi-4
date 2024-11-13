
#sudo fc-cache -fv

# Arial: Một font sans-serif phổ biến.
# Times New Roman: Một font serif truyền thống.
# Tahoma: Một font sans-serif rõ ràng.
# Verdana: Font sans-serif dễ đọc trên màn hình.
# Noto Sans: Font sans-serif hiện đại, hỗ trợ nhiều ngôn ngữ.
# Noto Serif: Font serif hiện đại, hỗ trợ nhiều ngôn ngữ.
# Liberation Sans: Font sans-serif thay thế cho Arial.
# Liberation Serif: Font serif thay thế cho Times New Roman.
# Roboto: Font sans-serif hiện đại, thường được sử dụng trong thiết kế.
# Open Sans: Font sans-serif với kiểu dáng đơn giản, dễ đọc.
# VNI-Times: Font serif, một trong những font truyền thống hỗ trợ tiếng Việt.
# VNI-Helve: Font sans-serif hỗ trợ tiếng Việt.
# Arial Unicode MS: Font hỗ trợ nhiều ngôn ngữ, bao gồm cả tiếng Việt.
# Comic Sans MS: Font với kiểu dáng vui tươi, dễ đọc.
# Droid Sans: Font sans-serif hiện đại, thường được sử dụng trong các ứng dụng Android.

import tkinter as tk
from tkinter import font

def show_fonts(index=0):
    # Nếu đã hiển thị hết các font, dừng chương trình
    if index >= len(available_fonts):
        print("Đã hiển thị tất cả các font có sẵn.")
        return
    
    # Tạo cửa sổ mới để hiển thị font hiện tại
    font_name = available_fonts[index]
    new_window = tk.Toplevel(root)
    new_window.title(f"Font: {font_name}")

    # Hiển thị label với font hiện tại
    label = tk.Label(new_window, text=f"Cài đặt giá trị đột biến, Đây là font  {font_name}", font=(font_name, 22))
    label.pack(padx=20, pady=20)

    # Đặt hành động đóng cửa sổ để hiển thị font tiếp theo
    new_window.protocol("WM_DELETE_WINDOW", lambda: (new_window.destroy(), show_fonts(index + 1)))

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Ứng Dụng Tiếng Việt")

# Lấy danh sách các font có sẵn sau khi cửa sổ chính được tạo
available_fonts = font.families()
print("Các font có sẵn:", available_fonts)

# Bắt đầu hiển thị các font
show_fonts()

# Chạy vòng lặp chính của tkinter
root.mainloop()

