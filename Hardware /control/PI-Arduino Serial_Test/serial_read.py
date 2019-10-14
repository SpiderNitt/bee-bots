ser = serial.Serial('COM18')
flush_value = ser.read(4)
control = 'l'
while(1):
    p = ser.read(4)
    p.decode("utf-8")
    f = float(p)
    print(f)
