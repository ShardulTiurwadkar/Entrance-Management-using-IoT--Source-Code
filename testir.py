from smbus2 import SMBus
from mlx90614 import MLX90614
bus = SMBus(1)
sensor = MLX90614(bus,address = 0x5A)
print("Ambient Temp: ",sensor.get_ambient())
print("Obj Temp: ",sensor.get_object_1())
bus.close()