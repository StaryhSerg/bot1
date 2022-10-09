from flask import Flask, render_template, request, json
import vk
import vk_api
from vk_api import VkUpload
import gspread
from oauth2client.service_account import ServiceAccountCredentials  # ипортируем ServiceAccountCredentials
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random

#Функции
def klava1(keyboard):
    keyboard.add_button('Органика', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Неорганика', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Физха', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Рандом', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Отключить бота', color=VkKeyboardColor.NEGATIVE)

def klava2(keyboard):
    keyboard.add_button('О Изи', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('О Ср', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('О Хард', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Н Изи', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Н Ср', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Н Хард', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Ф Изи', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Ф Ср', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button('Ф Хард', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Выйти', color=VkKeyboardColor.SECONDARY)

def klava3(keyboard):
    keyboard.add_button('Изи', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Средне', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Хард', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button('Назад', color=VkKeyboardColor.SECONDARY)

#Переменные
stok = '72a85c89'
token = '67e4484e8c32e69e579de8e319366e64cabdc16fb5b5b75a85d4de3a14ae1f140888e35e1982d190f7595'
bot = vk_api.VkApi(token=token)
upload = VkUpload(bot)
app = Flask(__name__)


#Тело
with open('gl.json', 'r') as file:
    on=json.load(file)

with open('basa.json', 'r') as file:
    mode=json.load(file)

@app.route('/', methods=['POST'])
def processing():
    # Распаковываем json из пришедшего POST-запроса
    data = json.loads(request.data)
    # Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return stok
    elif data['object']['message']['peer_id'] == 2000000001:
        return 'ok'
    elif data['type'] == 'message_new' and data['object']['message']['peer_id'] != 2000000001:
        session = vk.Session()
        api = vk.API(session, v='5.131')
        user_id = data['object']['message']['from_id']
        user_data = on.get(str(user_id))

        if data['object']['message']['text'] != 'Начать' and user_data == None:
            return 'ok'
        elif data['object']['message']['text'] == 'Начать' and user_data == None:
            with open('gl.json', 'w') as outfile:
                on1={'status':'on'}
                on2={'lesson':None}
                on3={'key':None}
                on[str(user_id)]=on1
                on[str(user_id)].update(on2)
                on[str(user_id)].update(on3)
                json.dump(on, outfile)
            keyboard = VkKeyboard(one_time=False)
            klava1(keyboard)
            api.messages.send(access_token=token, user_id=user_id, random_id=get_random_id(), message='Бот включен', keyboard=keyboard.get_keyboard())
            return 'ok'
        elif data['object']['message']['text'] == 'Отключить бота' and user_data != None:
            with open('gl.json', 'w') as outfile:
                del on[str(user_id)]
                json.dump(on, outfile)
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button('Начать', color=VkKeyboardColor.POSITIVE)
            api.messages.send(access_token=token, user_id=user_id, random_id=get_random_id(),
                              message='Бот отключен', keyboard=keyboard.get_keyboard())
            return 'ok'
        elif on[str(user_id)]['status'] == 'on' and on[str(user_id)]['lesson'] == None and user_data['key'] == None:

            if data['object']['message']['text'] == 'Рандом':
                s_id=mode['o izi']+mode['o sr']+mode['o hard']+mode['n izi']+mode['n sr']+mode['n hard']+mode['f izi']+mode['f sr']+mode['f hard']
                keyboard = VkKeyboard(one_time=False)
                klava1(keyboard)
                api.messages.send(access_token=token, user_id=user_id, random_id=get_random_id(),
                                  forward_messages=int(random.choice(s_id)), keyboard=keyboard.get_keyboard())

            elif data['object']['message']['text'] == 'код':
                with open('gl.json', 'w') as outfile:
                    on3={'key':'on'}
                    on[str(user_id)].update(on3)
                    json.dump(on, outfile)
                keyboard = VkKeyboard(one_time=False)
                klava2(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='меню разработчика',
                                  random_id=get_random_id(), keyboard=keyboard.get_keyboard())

            elif data['object']['message']['text'] == 'Органика' or data['object']['message']['text'] == 'Неорганика' or data['object']['message']['text'] == 'Физха':
                with open('gl.json', 'w') as outfile:
                    on2={'lesson':data['object']['message']['text']}
                    on[str(user_id)].update(on2)
                    json.dump(on, outfile)
                keyboard = VkKeyboard(one_time=False)
                klava3(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message=str(data['object']['message']['text']), random_id=get_random_id(),
                                  keyboard=keyboard.get_keyboard())

            else:
                keyboard = VkKeyboard(one_time=False)
                klava1(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='Хехе', random_id=get_random_id(),
                                  keyboard=keyboard.get_keyboard())
            return 'ok'
        elif on[str(user_id)]['lesson'] == 'Органика' and user_data['key'] == None:

            if data['object']['message']['text'] == 'Изи':
                with open('gl.json', 'w') as outfile:
                    on[str(user_id)]['lesson'] = None
                    json.dump(on, outfile)
                keyboard = VkKeyboard(one_time=False)
                klava1(keyboard)
                s_id=mode['o izi']
                api.messages.send(access_token=token, user_id=user_id, random_id=get_random_id(),
                                  forward_messages=int(random.choice(s_id)), keyboard=keyboard.get_keyboard())

            elif data['object']['message']['text'] == 'Средне':
                with open('gl.json', 'w') as outfile:
                    on[str(user_id)]['lesson'] = None
                    json.dump(on, outfile)
                keyboard = VkKeyboard(one_time=False)
                klava1(keyboard)
                s_id=mode['o sr']
                api.messages.send(access_token=token, user_id=user_id, random_id=get_random_id(),
                                  forward_messages=int(random.choice(s_id)), keyboard=keyboard.get_keyboard())

            elif data['object']['message']['text'] == 'Хард':
                with open('gl.json', 'w') as outfile:
                    on[str(user_id)]['lesson'] = None
                    json.dump(on, outfile)
                keyboard = VkKeyboard(one_time=False)
                klava1(keyboard)
                s_id=mode['o hard']
                api.messages.send(access_token=token, user_id=user_id, random_id=get_random_id(),
                                  forward_messages=int(random.choice(s_id)), keyboard=keyboard.get_keyboard())
            elif data['object']['message']['text'] == 'Назад':
                with open('gl.json', 'w') as outfile:
                    on[str(user_id)]['lesson'] = None
                    json.dump(on, outfile)
                keyboard = VkKeyboard(one_time=False)
                klava1(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='Главное меню',
                                  random_id=get_random_id(), keyboard=keyboard.get_keyboard())
            else:
                keyboard = VkKeyboard(one_time=False)
                klava3(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='Хехе', random_id=get_random_id(),
                                  keyboard=keyboard.get_keyboard())
            return 'ok'
        elif on[str(user_id)]['lesson'] == 'Неорганика' and user_data['key'] == None:

            if  data['object']['message']['text'] == 'Изи':
                with open('gl.json', 'w') as outfile:
                    on[str(user_id)]['lesson'] = None
                    json.dump(on, outfile)
                keyboard = VkKeyboard(one_time=False)
                klava1(keyboard)
                s_id=mode['n izi']
                api.messages.send(access_token=token, user_id=user_id, random_id=get_random_id(),
                                  forward_messages=int(random.choice(s_id)), keyboard=keyboard.get_keyboard())

            elif data['object']['message']['text'] == 'Средне':
                with open('gl.json', 'w') as outfile:
                    on[str(user_id)]['lesson'] = None
                    json.dump(on, outfile)
                keyboard = VkKeyboard(one_time=False)
                klava1(keyboard)
                s_id=mode['n sr']
                api.messages.send(access_token=token, user_id=user_id, random_id=get_random_id(),
                                  forward_messages=int(random.choice(s_id)), keyboard=keyboard.get_keyboard())

            elif data['object']['message']['text'] == 'Хард':
                with open('gl.json', 'w') as outfile:
                    on[str(user_id)]['lesson'] = None
                    json.dump(on, outfile)
                keyboard = VkKeyboard(one_time=False)
                klava1(keyboard)
                s_id=mode['n hard']
                api.messages.send(access_token=token, user_id=user_id, random_id=get_random_id(),
                                  forward_messages=int(random.choice(s_id)), keyboard=keyboard.get_keyboard())
            elif data['object']['message']['text'] == 'Назад':
                with open('gl.json', 'w') as outfile:
                    on[str(user_id)]['lesson'] = None
                    json.dump(on, outfile)
                keyboard = VkKeyboard(one_time=False)
                klava1(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='Главное меню',
                                  random_id=get_random_id(), keyboard=keyboard.get_keyboard())
            else:
                keyboard = VkKeyboard(one_time=False)
                klava3(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='Хехе', random_id=get_random_id(),
                                  keyboard=keyboard.get_keyboard())
            return 'ok'
        elif on[str(user_id)]['lesson'] == 'Физха' and user_data['key'] == None:

            if data['object']['message']['text'] == 'Изи':
                with open('gl.json', 'w') as outfile:
                    on[str(user_id)]['lesson'] = None
                    json.dump(on, outfile)
                keyboard = VkKeyboard(one_time=False)
                klava1(keyboard)
                s_id=mode['f izi']
                api.messages.send(access_token=token, user_id=user_id, random_id=get_random_id(),
                                  forward_messages=int(random.choice(s_id)), keyboard=keyboard.get_keyboard())

            elif data['object']['message']['text'] == 'Средне':
                with open('gl.json', 'w') as outfile:
                    on[str(user_id)]['lesson'] = None
                    json.dump(on, outfile)
                keyboard = VkKeyboard(one_time=False)
                klava1(keyboard)
                s_id=mode['f sr']
                api.messages.send(access_token=token, user_id=user_id, random_id=get_random_id(),
                                  forward_messages=int(random.choice(s_id)), keyboard=keyboard.get_keyboard())

            elif data['object']['message']['text'] == 'Хард':
                with open('gl.json', 'w') as outfile:
                    on[str(user_id)]['lesson'] = None
                    json.dump(on, outfile)
                keyboard = VkKeyboard(one_time=False)
                klava1(keyboard)
                s_id=mode['f hard']
                api.messages.send(access_token=token, user_id=user_id, random_id=get_random_id(),
                                  forward_messages=int(random.choice(s_id)), keyboard=keyboard.get_keyboard())

            elif data['object']['message']['text'] == 'Назад':
                with open('gl.json', 'w') as outfile:
                    on[str(user_id)]['lesson'] = None
                    json.dump(on, outfile)
                keyboard = VkKeyboard(one_time=False)
                klava1(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='Главное меню',
                                  random_id=get_random_id(), keyboard=keyboard.get_keyboard())

            else:
                keyboard = VkKeyboard(one_time=False)
                klava3(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='Хехе', random_id=get_random_id(),
                                  keyboard=keyboard.get_keyboard())
            return 'ok'
        elif user_data['key'] == 'on':
            link = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']  # задаем ссылку на Гугл таблици
            my_creds = ServiceAccountCredentials.from_json_keyfile_name('telega1.json',
                                                                        link)  # формируем данные для входа из нашего json файла
            client = gspread.authorize(my_creds)  # запускаем клиент для связи с таблицами
            sheet = client.open('Телега').sheet1  # открываем нужную на таблицу и лист

            if data['object']['message']['text'] == 'Выйти':
                with open('gl.json', 'w') as outfile:
                    key={'key':None}
                    on[str(user_id)].update(key)
                    json.dump(on, outfile)
                with open('basa.json', 'w') as outfile:
                    text=data['object']['message']['text']
                    sav={'sav':None}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                keyboard = VkKeyboard(one_time=False)
                klava1(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='Главное меню',
                                  random_id=get_random_id(), keyboard=keyboard.get_keyboard())
            elif data['object']['message']['text'] == 'О Изи':
                with open('basa.json', 'w') as outfile:
                    text=data['object']['message']['text']
                    sav={'sav':str(text)}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                api.messages.send(access_token=token, user_id=str(user_id),
                                  message='добавьте сообщение с задачей (файл + описание)', random_id=get_random_id())
            elif data['object']['message']['text'] == 'О Ср':
                with open('basa.json', 'w') as outfile:
                    text=data['object']['message']['text']
                    sav={'sav':str(text)}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                api.messages.send(access_token=token, user_id=str(user_id),
                                  message='добавьте сообщение с задачей (файл + описание)', random_id=get_random_id())
            elif data['object']['message']['text'] == 'О Хард':
                with open('basa.json', 'w') as outfile:
                    text=data['object']['message']['text']
                    sav={'sav':str(text)}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                api.messages.send(access_token=token, user_id=str(user_id),
                                  message='добавьте сообщение с задачей (файл + описание)', random_id=get_random_id())
            elif data['object']['message']['text'] == 'Н Изи':
                with open('basa.json', 'w') as outfile:
                    text=data['object']['message']['text']
                    sav={'sav':str(text)}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                api.messages.send(access_token=token, user_id=str(user_id),
                                  message='добавьте сообщение с задачей (файл + описание)', random_id=get_random_id())
            elif data['object']['message']['text'] == 'Н Ср':
                with open('basa.json', 'w') as outfile:
                    text=data['object']['message']['text']
                    sav={'sav':str(text)}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                api.messages.send(access_token=token, user_id=str(user_id),
                                  message='добавьте сообщение с задачей (файл + описание)', random_id=get_random_id())
            elif data['object']['message']['text'] == 'Н Хард':
                with open('basa.json', 'w') as outfile:
                    text=data['object']['message']['text']
                    sav={'sav':str(text)}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                api.messages.send(access_token=token, user_id=str(user_id),
                                  message='добавьте сообщение с задачей (файл + описание)', random_id=get_random_id())
            elif data['object']['message']['text'] == 'Ф Изи':
                with open('basa.json', 'w') as outfile:
                    text=data['object']['message']['text']
                    sav={'sav':str(text)}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                api.messages.send(access_token=token, user_id=str(user_id),
                                  message='добавьте сообщение с задачей (файл + описание)', random_id=get_random_id())
            elif data['object']['message']['text'] == 'Ф Ср':
                with open('basa.json', 'w') as outfile:
                    text=data['object']['message']['text']
                    sav={'sav':str(text)}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                api.messages.send(access_token=token, user_id=str(user_id),
                                  message='добавьте сообщение с задачей (файл + описание)', random_id=get_random_id())
            elif data['object']['message']['text'] == 'Ф Хард':
                with open('basa.json', 'w') as outfile:
                    text=data['object']['message']['text']
                    sav={'sav':str(text)}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                api.messages.send(access_token=token, user_id=str(user_id),
                                  message='добавьте сообщение с задачей (файл + описание)', random_id=get_random_id())

            #гребаная залупа
            elif mode[str(user_id)]['sav'] == 'О Изи' and data['object']['message']['text'] !='О Изи':
                l = len(sheet.col_values(1))
                sheet.update_cell(l + 1, 1, data['object']['message']['id'])
                with open('basa.json', 'w') as outfile:
                    nomer=mode['o izi']
                    nomer.append(str(data['object']['message']['id']))
                    index={'o izi':nomer}
                    mode.update(index)
                    sav={'sav':None}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                keyboard = VkKeyboard()
                klava2(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='задача загружена',
                                  random_id=get_random_id(), keyboard=keyboard.get_keyboard())
            elif mode[str(user_id)]['sav'] == 'О Ср' and data['object']['message']['text'] != 'О Ср':
                l = len(sheet.col_values(2))
                sheet.update_cell(l + 1, 2, data['object']['message']['id'])
                with open('basa.json', 'w') as outfile:
                    nomer=mode['o sr']
                    nomer.append(str(data['object']['message']['id']))
                    index={'o sr':nomer}
                    mode.update(index)
                    sav={'sav':None}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                keyboard = VkKeyboard()
                klava2(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='задача загружена',
                                  random_id=get_random_id(), keyboard=keyboard.get_keyboard())
            elif mode[str(user_id)]['sav'] == 'О Хард' and data['object']['message']['text'] != 'О Хард':
                l = len(sheet.col_values(3))
                sheet.update_cell(l + 1, 3, data['object']['message']['id'])
                with open('basa.json', 'w') as outfile:
                    nomer=mode['o hard']
                    nomer.append(str(data['object']['message']['id']))
                    index={'o hard':nomer}
                    mode.update(index)
                    sav={'sav':None}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                keyboard = VkKeyboard()
                klava2(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='задача загружена',
                                  random_id=get_random_id(), keyboard=keyboard.get_keyboard())
            elif mode[str(user_id)]['sav'] == 'Н Изи' and data['object']['message']['text'] != 'Н Изи':
                l = len(sheet.col_values(4))
                sheet.update_cell(l + 1, 4, data['object']['message']['id'])
                with open('basa.json', 'w') as outfile:
                    nomer=mode['n izi']
                    nomer.append(str(data['object']['message']['id']))
                    index={'n izi':nomer}
                    mode.update(index)
                    sav={'sav':None}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                keyboard = VkKeyboard()
                klava2(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='задача загружена',
                                  random_id=get_random_id(), keyboard=keyboard.get_keyboard())
            elif mode[str(user_id)]['sav'] == 'Н Ср' and data['object']['message']['text'] != 'Н Ср':
                l = len(sheet.col_values(5))
                sheet.update_cell(l + 1, 5, data['object']['message']['id'])
                with open('basa.json', 'w') as outfile:
                    nomer=mode['n sr']
                    nomer.append(str(data['object']['message']['id']))
                    index={'n sr':nomer}
                    mode.update(index)
                    sav={'sav':None}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                keyboard = VkKeyboard()
                klava2(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='задача загружена',
                                  random_id=get_random_id(), keyboard=keyboard.get_keyboard())
            elif mode[str(user_id)]['sav'] == 'Н Хард' and data['object']['message']['text'] != 'Н Хард':
                l = len(sheet.col_values(6))
                sheet.update_cell(l + 1, 6, data['object']['message']['id'])
                with open('basa.json', 'w') as outfile:
                    nomer=mode['n hard']
                    nomer.append(str(data['object']['message']['id']))
                    index={'n hard':nomer}
                    mode.update(index)
                    sav={'sav':None}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                keyboard = VkKeyboard()
                klava2(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='задача загружена',
                                  random_id=get_random_id(), keyboard=keyboard.get_keyboard())
            elif mode[str(user_id)]['sav'] == 'Ф Изи' and data['object']['message']['text'] != 'Ф Изи':
                l = len(sheet.col_values(7))
                sheet.update_cell(l + 1, 7, data['object']['message']['id'])
                with open('basa.json', 'w') as outfile:
                    nomer=mode['f izi']
                    nomer.append(str(data['object']['message']['id']))
                    index={'f izi':nomer}
                    mode.update(index)
                    sav={'sav':None}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                keyboard = VkKeyboard()
                klava2(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='задача загружена',
                                  random_id=get_random_id(), keyboard=keyboard.get_keyboard())
            elif mode[str(user_id)]['sav'] == 'Ф Ср' and data['object']['message']['text'] != 'Ф Ср':
                l = len(sheet.col_values(8))
                sheet.update_cell(l + 1, 8, data['object']['message']['id'])
                with open('basa.json', 'w') as outfile:
                    nomer=mode['f sr']
                    nomer.append(str(data['object']['message']['id']))
                    index={'f sr':nomer}
                    mode.update(index)
                    sav={'sav':None}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                keyboard = VkKeyboard()
                klava2(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='задача загружена',
                                  random_id=get_random_id(), keyboard=keyboard.get_keyboard())
            elif mode[str(user_id)]['sav'] == 'Ф Хард' and data['object']['message']['text'] != 'Ф Хард':
                l = len(sheet.col_values(9))
                sheet.update_cell(l + 1, 9, data['object']['message']['id'])
                with open('basa.json', 'w') as outfile:
                    nomer=mode['f hard']
                    nomer.append(str(data['object']['message']['id']))
                    index={'f hard':nomer}
                    mode.update(index)
                    sav={'sav':None}
                    mode[str(user_id)]=sav
                    json.dump(mode, outfile)
                keyboard = VkKeyboard()
                klava2(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='задача загружена',
                                  random_id=get_random_id(), keyboard=keyboard.get_keyboard())
            else:
                keyboard = VkKeyboard(one_time=False)
                klava2(keyboard)
                api.messages.send(access_token=token, user_id=str(user_id), message='Хехе', random_id=get_random_id(),
                                  keyboard=keyboard.get_keyboard())
            return 'ok'
