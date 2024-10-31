from check_com.checkCom_global import *
import struct

# Constants
START_BYTE = 0x02

def calculate_checksum(fromID, to, title, data):
    checksum = fromID + to + title
    for value in data:
        checksum += (value >> 8) & 0xFF  
        checksum += value & 0xFF         
    return checksum & 0xFFFF  

# Hàm gửi dữ liệu xuống
def send_packet(fromID, toID, title, data=[]):
    global START_BYTE 
    data_size = len(data)  
    packet_size = 5 + data_size * 2 
    checksum = calculate_checksum(fromID, toID, title, data)
    
    packet = struct.pack('B', START_BYTE)              
    packet += struct.pack('B', packet_size)             
    packet += struct.pack('B', fromID)                     
    packet += struct.pack('B', toID)                       
    packet += struct.pack('B', title)                 
    
    for value in data:
        packet += struct.pack('>H', value)             

    packet += struct.pack('>H', checksum)            
    port.write(packet)
    print("Packet sent:", packet)

# Hàm nhận dữ liệu trả lên

def receive_packet_all():
    while True:
        # Tìm START_BYTE
        start_byte = port.read(1)
        if start_byte != struct.pack('B', START_BYTE):
            continue  

        # Đọc kích thước gói tin
        packet_size_byte = port.read(1)
        if len(packet_size_byte) == 0:
            print("Lỗi: không nhận được kích thước gói tin")
            continue
        
        packet_size = struct.unpack('B', packet_size_byte)[0]

        # Đảm bảo kích thước gói tin hợp lệ
        if packet_size < 5:  
            print("Lỗi: kích thước gói tin không hợp lệ:", packet_size)
            continue

        header = port.read(3)
        if len(header) != 3:
            print("Lỗi: không nhận đủ header, đã nhận:", len(header), "bytes")
            continue  
        
        fromID, toID, title = struct.unpack('BBB', header)

        # Đọc dữ liệu
        data = []
        data_size = (packet_size - 5) // 2 
        
        for _ in range(data_size):
            data_bytes = port.read(2)
            if len(data_bytes) < 2:
                print("Lỗi: không nhận đủ dữ liệu cho item, đã nhận:", len(data_bytes), "bytes")
                break
            
            value = struct.unpack('>H', data_bytes)[0]
            data.append(value)

        # Đọc checksum
        checksum_bytes = port.read(2)
        if len(checksum_bytes) < 2:
            print("Lỗi: không nhận đủ checksum, đã nhận:", len(checksum_bytes), "bytes")
            continue  
            
        received_checksum = struct.unpack('>H', checksum_bytes)[0]

        # Tính toán checksum và so sánh
        calculated_checksum = calculate_checksum(fromID, toID, title, data)
        if calculated_checksum != received_checksum:
            print("Checksum không khớp! Dữ liệu bị lỗi.")
            continue 

        print("Gói tin nhận thành công:", fromID, toID, title, data)
        
        return fromID, toID, title, data
    