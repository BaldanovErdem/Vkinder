from keyboard import sender
from main import *


for event in bot.longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        request = event.text.lower()
        user_id = str(event.user_id)
        msg = event.text.lower()
        sender(user_id, msg.lower())
        create_tables_orm(engine)

        if bot.get_user_info(user_id) and bot.number_of_persons(user_id, persons, offset):   # Исключения должны влиять на логику исполнения программы (замечание проверяющего №1)
            first_name, sex, bdate, city = bot.get_user_info(user_id)
            if persons == [] or persons[offset] == persons[-1]:               # применить обычное условие здесь (замечание проверяющего №3)
                persons = bot.find_insert_users(user_id, offset_1)
                offset_1 = offset_1 + count

            if request == 'новый кандидат':
                for i in range(0, 1000):
                    if search_id_orm(persons[offset][2]) == 0:
                        bot.find_persons(user_id, persons[offset])
                        offset += 1
                        break
                    else:
                        offset += 1

            elif request == 'очистить список просмотренных':
                drop_tables_orm(engine)

            else:
                bot.write_message(event.user_id, 'Твоё сообщение непонятно')
