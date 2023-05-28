import serial

port = '/dev/serial1'  # 시리얼 포트
baudrate = 115200  # 전송 속도

# 시리얼 포트 열기
ser = serial.Serial(port, baudrate)

# 문자 데이터 전송
data = 'Hello, serial!'
ser.write(data.encode())

data = '10'
ser.write(data.encode())

# 시리얼 포트 닫기
ser.close()