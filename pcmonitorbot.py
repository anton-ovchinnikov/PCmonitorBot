import wmi
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import random
import json
import re
import pyautogui
import requests
from pywinauto import Desktop

# OpenHardwareMonitor
w = wmi.WMI(namespace="root\OpenHardwareMonitor")
# vk
id_vk = ***id***
token = "***token***"
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
# vk keyboard
keyboard = {
"one_time": False,
"buttons": [
    [{
        "action": {
            "type": "text",
            "payload": "{\"button\": \"1\"}",
            "label": "Temp🌡"
        },
        "color": "negative"
    },
	{
        "action": {
            "type": "text",
            "payload": "{\"button\": \"3\"}",
            "label": "Load🖥",
        },
        "color": "positive"
    }],
    [{
        "action": {
            "type": "text",
            "payload": "{\"button\": \"3\"}",
            "label": "Take Screenshot🖼",
        },
        "color": "secondary"
    }],
    [{
        "action": {
            "type": "text",
            "payload": "{\"button\": \"1\"}",
            "label": "Settings⚙"
        },
        "color": "primary"
    }],
  ]
}
keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
keyboard = str(keyboard.decode('utf-8'))
# vk keyboard settings section
keyboard_settings = {
"one_time": False,
"buttons": [
    [{
        "action": {
            "type": "text",
            "payload": "{\"button\": \"1\"}",
            "label": "Hardware🛠"
        },
        "color": "positive"
    },
    {
        "action": {
            "type": "text",
            "payload": "{\"button\": \"1\"}",
            "label": "About🔍"
        },
        "color": "positive"
    }],
    [{
        "action": {
            "type": "text",
            "payload": "{\"button\": \"1\"}",
            "label": "Back🔙"
        },
        "color": "primary"
    }],
  ]
}
keyboard_settings = json.dumps(keyboard_settings, ensure_ascii=False).encode('utf-8')
keyboard_settings = str(keyboard_settings.decode('utf-8'))

#  Hardware Types:
#  Mainboard
#  CPU
#  GpuNvidia
#  GpuAti
#  HDD

def get_hw():
    hw_info = w.Hardware()
    hardw = {}
    i = 0
    for hardware in hw_info:
        hw = hardware.Identifier.split('/')
        i = i + 1
        hardw.update({str(hw[1]) + str(i) : str(hardware.Name)})
    return hardw

# I don't know how to describe it :)
def translate(text):
    text_out = ''
    if text == 'atigpu' or text == 'nvidiagpu':
        text_out = 'GPU'
    elif text == 'amdcpu' or text == 'intelcpu':
        text_out = 'CPU'
    elif text == 'hdd':
        text_out = 'HDD'
    elif text == 'lpc':
        text_out = 'LPC'
    elif text == 'ram':
        text_out = 'RAM'
    elif text == 'mainboard':
        text_out = 'MainBoard'
    return text_out

# function for get temperature
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

# function for get load
def get_load():
    sens_info = w.Sensor()
    sens_values = {}
    i = 0
    for sensor in sens_info:
        sens = sensor.Identifier.split('/')
        if sens[3]==u'load':
            i = i + 1
            sens_values.update({sens[1] + str(i) : sensor.Value})
    return sens_values

# windows = Desktop(backend="uia").windows()
# print([w.window_text() for w in windows])

# vk longpoll event
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW:
        # if message from me
        if event.to_me and event.user_id == id_vk:
            msg = event.text
            # if message text is temp
            if msg == 'Temp🌡':
                sens_info = get_temp()
                for sensor in sens_info.items():
                    vk.messages.send(user_id = id_vk, keyboard = keyboard, message = str(translate(sensor[0][:-1])) + ': ' + str(int(sensor[1])) + '°C', random_id = random.randint(0, 999999))
            # if message text is load
            elif msg == 'Load🖥':
                sens_inf = get_load()
                for sens in sens_inf.items():
                    vk.messages.send(user_id = id_vk, keyboard = keyboard, message = str(translate(sens[0][:-1])) + ': ' + str(int(sens[1])) + '%', random_id = random.randint(0, 999999))
            elif msg == 'Take Screenshot🖼':
                img = pyautogui.screenshot()
                img.save('screenshot.png')
                upload_url = vk.photos.getMessagesUploadServer()
                upload_file = requests.post(upload_url['upload_url'], files={'photo': open('screenshot.png', 'rb')}).json()
                c = vk.photos.saveMessagesPhoto(photo=upload_file['photo'], server=upload_file['server'], hash=upload_file['hash'])[0]
                d = "photo{0}_{1}".format(c['owner_id'], c['id'])
                vk.messages.send(user_id = id_vk, keyboard = keyboard, message = 'Screenshot:', attachment = d, random_id = random.randint(0, 999999))
            elif msg == 'Settings⚙':
                vk.messages.send(user_id = id_vk, keyboard = keyboard_settings, message = 'You have gone to the settings section', random_id = random.randint(0, 999999))
            elif msg == 'Hardware🛠':
                hardware = get_hw()
                for hard in hardware.items():
                    vk.messages.send(user_id = id_vk, keyboard = keyboard, message = str(translate(hard[0][:-1])) + ': ' + str(hard[1]), random_id = random.randint(0, 999999))
            elif msg == 'About🔍':
                vk.messages.send(user_id = id_vk, keyboard = keyboard_settings, message = '> PCmonitorBot\n> A bot for monitoring the state of the PC.\n> Repository: https://github.com/anton-ovchinnikov/PCmonitorBot\n> Author: Anton Ovchinnikov', random_id = random.randint(0, 999999))
            elif msg == 'Back🔙':
                vk.messages.send(user_id = id_vk, keyboard = keyboard, message = 'You have gone to the main section', random_id = random.randint(0, 999999))
            else:
                vk.messages.send(user_id = id_vk, keyboard = keyboard, message = "I didn't understand the command.", random_id = random.randint(0, 999999))
