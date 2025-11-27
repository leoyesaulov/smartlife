from data_handler import DataHandler

data_handler = DataHandler()
strip_ip = data_handler.get('strip_ip')

while not strip_ip:
    strip_ip = input("Please enter ip of your cololight strip: ")

data_handler.write("strip_ip", strip_ip)