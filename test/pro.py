
# import RPi.GPIO as GPIO

# # Constants won't change. They're used here to set pin numbers:
# BUTTON_PIN = 16  # The number of the pushbutton pin
# LED_PIN = 18     # The number of the LED pin

# # Variables will change:
# button_state = 0  # Variable for reading the pushbutton status

# # Set up GPIO
# GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering
# GPIO.setup(LED_PIN, GPIO.OUT)           # Initialize the LED pin as an output
# GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Initialize the pushbutton pin as a pull-up input

# try:
#     while True:
#         # Read the state of the pushbutton value:
#         button_state = GPIO.input(BUTTON_PIN)

#         # Control LED according to the state of the button
#         if button_state == GPIO.LOW:  # If the button is pressed
#             GPIO.output(LED_PIN, GPIO.HIGH)  # Turn on LED
#         else:  # Otherwise, the button is not pressed
#             GPIO.output(LED_PIN, GPIO.LOW)  # Turn off LED

# except KeyboardInterrupt:
#     # Clean up GPIO on program exit
#     GPIO.cleanup()

# import os
# import pandas as pd
# import datetime

# def save_data_excel_tb(avg1, avg2, arr_avg1, arr_avg2, value1, value2, threshold_value_1, threshold_value_2, time_clean1, time_clean2):
#     data = {
#         "time_save": [datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")],
#         "average_sensor_1": [avg1.get() if avg1 else "No data"],
#         "average_sensor_2": [avg2.get() if avg2 else "No data"],
#         "array_average_1": [arr_avg1 if arr_avg1 is not None else "No data"],
#         "array_average_2": [arr_avg2 if arr_avg2 is not None else "No data"],
#         "mutation_value_1": [value1.get() if value1 else "No data"],
#         "mutation_value_2": [value2.get() if value2 else "No data"],
#         "threshold_value_sensor_1": [threshold_value_1.get() if threshold_value_1 else "No data"],
#         "threshold_value_sensor_2": [threshold_value_2.get() if threshold_value_2 else "No data"],
#         "time_clean_1": [time_clean1.get() if time_clean1 else "No data"],
#         "time_clean_2": [time_clean2.get() if time_clean2 else "No data"]
#     }

#     output_dir = "/home/ailab/Downloads/luu_ca_tam"

#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
#     df = pd.DataFrame(data)
#     df.fillna("No data", inplace=True)  # Thay thế giá trị NaN bằng "No data"
#     df.to_excel(os.path.join(output_dir, "cai_dat_catam.xlsx"), index=False)
#     print("Thông báo: Lưu dữ liệu vào file cai_dat_catam.xlsx thành công")


# # Tạo DataFrame toàn cục để lưu trữ dữ liệu
# df_global = pd.DataFrame(columns=["time_save", "sensor_1", "sensor_2", "mutation_value_1", "mutation_value_2"])

# def save_data_excel_ngay(value_1=1, value_2=1, mutation_value_1=None, mutation_value_2=None):
#     global df_global
#     data = {
#         "time_save": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
#         "sensor_1": value_1 if value_1 is None else value1.get(),
#         "sensor_2": value_2 if value_2 is None else value2.get(),
#         "mutation_value_1": "" if mutation_value_1 is None else mutation_value_1,
#         "mutation_value_2": "" if mutation_value_2 is None else mutation_value_2,
#     }

#     if value_1 is None or value_2 is None:
#         print("Co dot bien tu CB", mutation_value_1, mutation_value_2)
#     else:
#         print("Khong co dot bien", value1.get(), value2.get())

#     # Tạo DataFrame từ dữ liệu mới
#     df_new_data = pd.DataFrame([data])

#     # Đường dẫn lưu file trên Raspberry Pi
#     output_dir = "/home/pi/Desktop/data_catam_ngay"
#     if not os.path.exists(output_dir):
#         os.makedirs(output_dir)
#     filename = datetime.datetime.now().strftime("data_ca_tam_ngay_%Y-%m-%d.xlsx")
#     filepath = os.path.join(output_dir, filename)

#     if os.path.exists(filepath):
#         df_existing = pd.read_excel(filepath)

#         # Loại bỏ các cột trống hoặc toàn bộ giá trị NA
#         df_existing = df_existing.dropna(axis=1, how='all')
#         df_existing = df_existing.loc[:, df_existing.notna().any()]
#         df_new_data = df_new_data.dropna(axis=1, how='all')
#         df_new_data = df_new_data.loc[:, df_new_data.notna().any()]

#         # Gộp dữ liệu
#         df_global = pd.concat([df_existing, df_new_data], ignore_index=True)
#     else:
#         df_global = df_new_data

#     # Lưu vào file Excel
#     df_global.to_excel(filepath, index=False)
#     print("Thông báo: Lưu dữ liệu thành công vào Raspberry pi 4")

