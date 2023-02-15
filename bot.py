from keyboard import sender
from main import *


for event in bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = str(event.user_id)
        msg = event.text.lower()
        sender(user_id, msg.lower())
        first_name, sex, bdate, city = bot.get_user_info(user_id)
        if request == 'поиск':
            creating_database()
            bot.write_message(user_id, f'Привет, {first_name}')
            bot.find_insert_users(user_id)
            bot.write_message(event.user_id, f'Нашёл для тебя пару, жми на кнопку "Далее"')
            bot.find_persons(user_id, offset)

        elif request == 'далее':
            for i in range(0, 1000):
                offset += 1
                bot.find_persons(user_id, offset)
                break

        else:
            bot.write_message(event.user_id, 'Твоё сообщение непонятно')
