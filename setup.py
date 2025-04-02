from data_handler import DataHandler

__data_handler = DataHandler()
__strip_ip = __data_handler.get('strip_ip')

while not __strip_ip:
    __strip_ip = input("Please enter ip of your cololight strip: ")

__data_handler.write("strip_ip", __strip_ip)