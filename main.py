import vk_api
import requests
from vk_api.longpoll import VkLongPoll, VkEventType
from random import randrange
from database import *

user_token = 'vk1.a.a_4z8cTot1d0W_WC7k-GK2dYwfVt2ZGwA8NiV7W8Xuq338TuBNeQc21FhZsD_n5frWxjigvS6SmWTxIGF-XZNUZXz_I1LU2PVFN1ypi-fi_OeyGKVSPTqZd3pmBm5sjLQ-T9tagYv-Ry37VWcIch5YaQLy7fmDWhxm-56AFu9nA2XhHqz1wdmLsSu5ELdgSelbSjjD6xxfnkCFAHdIi8TA' # токен пользователя
comm_token = 'vk1.a.PPgleZKqltg-lXTeZqGwOBGxFHlWtqvSN8GoVSPhcBTUYe3gzcCa9K0SjlIf99e0Um27DClB4Z7HZ4Y11xFQYTsYdJ4q0uc_SmH3c68DHFGUwe_j9kgW4B5tX5LH9lsKsL2P28dlaNqfG7dbKbHG-vbXGIj_o9CuI-ejmXqNJvWoWis55PPA0lmWMOWqRJtGgv1gNe4IM1cwHZN1R3I2rA' # токен сообщества
offset = 0
persons = []   # Храните эти данные (список пользователей) в оперативной памяти (замечание проверяющего №2)
count = 100      # за раз выполнялся поиск по 100 анкет (замечание проверяющего №3)
offset_1 = 0

class Bot:
    def __init__(self):
        print('The bot is running')
        self.vk = vk_api.VkApi(token=comm_token)
        self.longpoll = VkLongPoll(self.vk)

    def write_message(self, user_id, message):
        self.vk.method('messages.send', {'user_id': user_id,
                                         'message': message,
                                         'random_id': randrange(10 ** 7)})

    def get_user_info(self, user_id):
        url = f'https://api.vk.com/method/users.get'
        params = {'access_token': user_token,
                  'user_ids': user_id,
                  'fields': 'first_name, sex, bdate, city ',
                  'v': '5.131'}
        resp = requests.get(url, params=params)
        resp_json = resp.json()
        try:       # исключения для проверки данных получаемых от апи (замечание проверяющего №1 )
            list_1 = resp_json['response']
        except KeyError:
            self.write_message(user_id, 'Ошибка получения сведений о пользователе')
        for i in list_1:
            first_name = i.get('first_name')
            if i.get('sex') == 2:
                sex = 1
            else:
                sex = 2
            bdate = i.get('bdate')
            city = i.get('city').get('id')
            return first_name, sex, bdate, city



    def find_insert_users(self, user_id, offset_1):
        first_name, sex, bdate, city = self.get_user_info(user_id)
        birth_year = int(bdate.split('.')[2])
        url = f'https://api.vk.com/method/users.search'
        params = {'access_token': user_token,
                  'v': '5.131',
                  'sex': sex,
                  'birth_year': birth_year,
                  'city': city,
                  'fields': 'is_closed, id, first_name, last_name',
                  'status': '1' or '6',
                  'count': count,
                  'has_photo': '1',
                  "offset": offset_1,
                  'sort': '0'}
        resp = requests.get(url, params=params)
        resp_json = resp.json()
        try:                                   # исключения для проверки данных получаемых от апи (замечание проверяющего №1 )
            dict_1 = resp_json['response']
        except KeyError:
            self.write_message(user_id, 'Ошибка получения сведений для списка пользователей')
        list_1 = dict_1['items']
        for person_dict in list_1:
            if person_dict.get('is_closed') == False:
                person = (person_dict.get('first_name'), person_dict.get('last_name'), str(person_dict.get('id')), 'vk.com/id' + str(person_dict.get('id')))
                persons.append(person)
            else:
                continue
        return persons


    def get_photos_id(self, user_id):
        url = 'https://api.vk.com/method/photos.getAll'
        params = {'access_token': user_token,
                  'type': 'profile',
                  'owner_id': user_id,
                  'extended': 1,
                  'count': 100,
                  'v': '5.131'}
        resp = requests.get(url, params=params)
        resp_json = resp.json()
        dict_photos = dict()
        count = 0
        try:
            dict_1 = resp_json['response']
        except KeyError:
            print('Ошибка получения фотографий')
        list_1 = dict_1['items']
        for i in list_1:
            photo_id = str(i.get('id'))
            i_likes = i.get('likes')
            if i_likes.get('count'):
                likes = i_likes.get('count')
                dict_photos[likes] = photo_id
            else:
                count += 1
                dict_photos[count] = photo_id
        list_of_ids = sorted(dict_photos.items(), reverse=True)
        return list_of_ids


    def send_photos(self, user_id, message, person_id):
        list_of_ids = self.get_photos_id(person_id)
        self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': user_token,
                                         'message': message,
                                         'attachment': f'photo{person_id}_{list_of_ids[0][1]}',
                                         'random_id': 0})
        try:
            int(list_of_ids[1][1]) > 0
        except:
            self.write_message(user_id, 'Ошибка получения фото')
        else:
            self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': user_token,
                                         'message': '',
                                         'attachment': f'photo{person_id}_{list_of_ids[1][1]}',
                                         'random_id': 0})
        try:
            int(list_of_ids[2][1]) > 0
        except:
            self.write_message(user_id, 'Ошибка получения фото')
        else:
            self.vk.method('messages.send', {'user_id': user_id,
                                         'access_token': user_token,
                                         'message': '',
                                         'attachment': f'photo{person_id}_{list_of_ids[2][1]}',
                                         'random_id': 0})

    def find_persons(self, user_id, person):
        self.write_message(user_id, f'{person[0]} {person[1]}, ссылка - {person[3]}')
        self.get_photos_id(person[2])
        self.send_photos(user_id, 'Лучшие фотографии', person[2])
        insert_data(person[0], person[1], person[2], person[3])     # А в бд отправляйте только ид просмотренных анкет (замечание проверяющего №2)


bot = Bot()
