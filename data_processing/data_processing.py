from cover.imports import *
from check_com.checkCom_global import *

#------------- ----TRUYỀN VÀ NHẬN XỬ LÝ TÍN HIỆU----------------------------------


# Hàm truyền thành dạng byte
def cmdString_two(fromId=6, toId=None, data1=None, data2=None):
    return f"T,{fromId},{toId},{data1},{data2};".encode()


# Tính arr rồi chuyển thành int
def handleAvg(arr):
    if (len(arr) > 1):
        return int(np.mean(arr))


#---------------------------------- Lưu DỮU LIỆU VÀO EXCEL-----------------------------

def save_data_excel_tb(avg1, avg2, arr_avg1, arr_avg2, value1, value2, threshold_value_1, threshold_value_2, time_clean1, time_clean2):
    data = {
        "time_save": [datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")],
        "average_sensor_1": [avg1.get() or "No data"],
        "average_sensor_2": [avg2.get() or "No data"],
        "array_average_1": [arr_avg1 if arr_avg1 is not None else "No data"],
        "array_average_2": [arr_avg2 if arr_avg2 is not None else "No data"],
        "mutation_value_1": [mutation_value_1.get() or "No data"],
        "mutation_value_2": [mutation_value_2.get() or "No data"],
        "threshold_value_sensor_1": [threshold_value_1.get() or "No data"],
        "threshold_value_sensor_2": [threshold_value_2.get() or "No data"],
        "time_clean_1": [time_clean1.get() or "No data"],
        "time_clean_2": [time_clean2.get() or "No data"]
    }
    # desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    # Lưu ở đâu đó
    output_dir = "C:\cai_dat_catam"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    df = pd.DataFrame(data)
    df.fillna("No data", inplace=True)  # Thay thế giá trị NaN bằng "No data"
    df.to_excel(os.path.join(output_dir, "cai_dat_catam.xlsx"), index=False)
    print("Thông báo", "Lưu dữ liệu vào file data_ca_tam_tb.xlsx thành công")


    # Tạo DataFrame toàn cục để lưu trữ dữ liệu
df_global = pd.DataFrame(columns=["time_save", "sensor_1", "sensor_2", "mutation_value_1", "mutation_value_2"])


def save_data_excel_ngay(value_1=1, value_2=1, mutation_value_1=None, mutation_value_2=None):
    global df_global
    data = {
        "time_save": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        "sensor_1": value_1 if value_1 is None else value1.get(),
        "sensor_2": value_2 if value_2 is None else value2.get(),
        "mutation_value_1": "" if mutation_value_1 is None else mutation_value_1,
        "mutation_value_2": "" if mutation_value_2 is None else mutation_value_2,
    }
    if value_1 is None or value_2 is None:
        print("Co dot bien", mutation_value_1, mutation_value_2)
    else:
        print("Khong co dot bien", value1.get(), value2.get())
    # Create DataFrame from new data
    df_new_data = pd.DataFrame([data])

    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    output_dir = os.path.join(desktop, 'data_catam_ngay')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = datetime.datetime.now().strftime("data_ca_tam_ngay_%Y-%m-%d.xlsx")
    filepath = os.path.join(output_dir, filename)

    if os.path.exists(filepath):
        df_existing = pd.read_excel(filepath)

        # Filter empty/all-NA columns
        df_existing = df_existing.dropna(axis=1, how='all')
        df_existing = df_existing.loc[:, df_existing.notna().any()]
        df_new_data = df_new_data.dropna(axis=1, how='all')
        df_new_data = df_new_data.loc[:, df_new_data.notna().any()]

        # Concatenate
        df_global = pd.concat([df_existing, df_new_data], ignore_index=True)
    else:
        df_global = df_new_data

    df_global.to_excel(filepath, index=False)
    print("Thông báo!!! Lưu dữ liệu thành công vào Desktop")
    # print(df_global)

# Hàm xuất excel
def export_excel():
    global df_global

    if df_global.empty:
        messagebox.showwarning("Thông báo", "Không có dữ liệu để xuất!")
        return

    filepath = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        initialfile=datetime.datetime.now().strftime("catam_ngay_%Y_%m_%d.xlsx"),
        filetypes=[("Excel files", "*.xlsx")],
    )
    if not filepath:
        return  # Người dùng đã hủy chọn file

    try:
        df_global.to_excel(filepath, index=False)
        messagebox.showinfo("Thông báo", "Xuất dữ liệu thành công!")
        df_global = df_global.iloc[0:0]  # Xóa dữ liệu sau khi xuất
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi khi xuất file: {e}")

# Hàm đọc dữ liệu từ file
def get_data_from_file():
    # desktop = os.path.join(os.path.join(os.environ["USERPROFILE"]), "Desktop")
    output_dir = "C:\cai_dat_catam"

    df = pd.read_excel(os.path.join(output_dir, "cai_dat_catam.xlsx"))
    avg1.set(df.iloc[0, 1])
    avg2.set(df.iloc[0, 2])
    threshold_value_1.set(df.iloc[0, 7])
    threshold_value_2.set(df.iloc[0, 8])
    time_clean1.set(df.iloc[0, 9])
    time_clean1.set(df.iloc[0, 10])
    print(threshold_value_1.get(), threshold_value_2.get(), time_clean1.get(),time_clean2.get(), avg1.get(), avg2.get())
