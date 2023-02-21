from keyboard import sender
from main import *


for event in bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = str(event.user_id)
        msg = event.text.lower()
        sender(user_id, msg.lower())
        create_table()
        first_name, sex, bdate, city = bot.get_user_info(user_id)
        try:                           # а когда эти 100 анкет будут просмотрены автоматически (незаметно для пользователя) должен выполняться новый поиск (замечание проверяющего №3)
            int(persons[offset + 1][2]) > 0
        except:
            persons = bot.find_insert_users(user_id, offset_1)
            offset_1 = offset_1 + count

        if request == 'новый кандидат':
            for i in range(0, 1000):
                if search_id(persons[offset][2]) == 0:  # условий задания, которое требует, чтобы пользователю повторно одна и та же анкета не приходила (замечание проверяющего №4)
                    bot.find_persons(user_id, persons[offset])
                    offset += 1
                    break
                else:
                    offset += 1

        elif request == 'очистить список просмотренных':
            drop_table()

        else:
            bot.write_message(event.user_id, 'Твоё сообщение непонятно')
