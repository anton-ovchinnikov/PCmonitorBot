import wmi
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random

# OpenHardwareMonitor
w = wmi.WMI(namespace="root\OpenHardwareMonitor")
# vk
id_vk = ***id***
token = "***token***"
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

#  Hardware Types:
#  Mainboard
#  CPU
#  GpuNvidia
#  GpuAti
#  HDD

# dev
def get_hw(hardware):
	hw_info = w.Hardware()
	hardw = {}
	for hw in hw_info:
		if hw.HardwareType==str(hardware):
			hardw.update({hardware : str(hw.Name)})
	return hardw

def get_temp():
	sens_info = w.Sensor()
	sens_values = {}
	i = 0
	for sensor in sens_info:
		sens = sensor.Identifier.split('/')
		if sens[3]==u'temperature':
			i = i + 1
			sens_values.update({sens[1] + str(i) : sensor.Value})
	return sens_values

sens_info = get_temp()
for sensor in sens_info.items():
	print(sensor)

# vk longpoll event
# for event in longpoll.listen():
#     if event.type == VkEventType.MESSAGE_NEW:
#         if event.to_me and event.user_id == id_vk:
#             msg = event.text
#             if msg == 'Temp':
#             	sens_info = get_temp()
#             	for sensor in sens_info.items():
#             		vk.messages.send(user_id = id_vk, message = str(sensor.keys()) + ': ' + (str(int(sensor.values()))) + '°C'), random_id = random.randint(0, 999999))
#             elif msg == 'Load':
#             	sens_info = w.Sensor()
#             	for sensor in sens_info:
#             		if sensor.SensorType==u'Load':
#             			vk.messages.send(user_id = id_vk, message = str(sensor.Name) + ': ' + (str(int(sensor.Value)) + '%'), random_id = random.randint(0, 999999))
