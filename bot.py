import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import time

# ================= НАСТРОЙКИ =================
TOKEN = 'vk1.a.X89WgPJdARa-HNpcwbakSRbUWpxFHA0QMsxKF6jnOqo6PnJq-uD8fNF8JOLqVzsB89XXJxA3H071TtY4tah9r_Isj2tEeSrBVYm9gIgAgooov4wy84BIyUF80tOYvGipCX-jzIMazdk_4SI6fr33sFtFIevq85RgBcEopAmjVLSzeSAzUAjUNnATF65z-dN2nb3sbNcHwctfCQv6-TsUqQ'
GROUP_ID = 214117275
# =============================================

vk_session = vk_api.VkApi(token=TOKEN)
longpoll = VkBotLongPoll(vk_session, group_id=GROUP_ID)
vk = vk_session.get_api()

# ================= КЛАВИАТУРА =================
def get_main_keyboard():
    """Создаём главную клавиатуру с кнопками (2 ряда)"""
    keyboard = VkKeyboard(one_time=False)
    
    # Первый ряд - 3 кнопки
    keyboard.add_button('Консультация', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button('Написать сайт', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button('Приложение', color=VkKeyboardColor.SECONDARY)
    
    # Переход на второй ряд
    keyboard.row()
    
    # Второй ряд - 2 кнопки
    keyboard.add_button('Предложить своё', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_button('Контакты', color=VkKeyboardColor.PRIMARY)
    
    return keyboard.get_keyboard()

# ================= ОТВЕТЫ БОТА =================
def get_response(command):
    """Возвращает ответ в зависимости от команды"""
    responses = {
        'консультация': """📚 **Консультация по предмету**

Я помогаю разобраться в сложных темах:
• Теоретическая информатика
• Программирование  

Напишите, какой предмет вас интересует, и я помогу!""",
        
        'сайт': """💻 **Написание личного сайта**

Создам для вас современный сайт:
• Визитка / Портфолио
• Лендинг

⏱ Срок: 3-7 дней

Расскажите, какой сайт вам нужен?""",
        
        'приложение': """📱 **Написание приложения**

Разработаю приложение под вашу задачу:
• VK-боты
• Мобильные приложения
• Десктопные программы

⏱ Срок: обсуждается индивидуально

Опишите, что должно уметь ваше приложение?""",
        
        'предложить': """✍️ **Предложить свою идею**

Отлично! Расскажите подробнее о вашем проекте:
• Что нужно сделать?
• Какие есть пожелания?
• Желаемые сроки?

Я изучу вашу задачу и предложу решение!""",
        
        'контакты': """📞 **Контакты для связи:**

📧 Email: sciensfeja@gmail.com
📱 Telegram: @VetaSvetlaja
📞 Телефон: +7 (981) 843-31-71 (Максим)

Напишите, и я отвечу в ближайшее время!""",
    }
    return responses.get(command, "Я вас не понял. Выберите пункт из меню 👇")

# ================= ОСНОВНОЙ ЦИКЛ =================
print("✅ Бот успешно запущен и ожидает сообщений...")

for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:
        message_text = event.obj.message['text'].lower().strip()
        user_id = event.obj.message['from_id']
        message_time = event.obj.message['date']
        current_time = int(time.time())
        
        # Пропускаем старые сообщения (старше 10 секунд)
        if current_time - message_time > 10:
            print(f"⏰ Пропущено старое сообщение от {user_id}")
            continue
        
        # Игнорируем сообщения от самого бота
        if user_id == GROUP_ID:
            continue
        
        print(f"📨 Новое сообщение от {user_id}: '{message_text}'")
        
        # Приветствие (с клавиатурой)
        if message_text in ['привет', 'здравствуй', 'хай', 'hi', 'ку', 'начать', 'старт']:
            vk.messages.send(
                user_id=user_id,
                message="👋 Здравствуйте! Я бот-помощник.\n\nВыберите услугу, которая вас интересует:",
                keyboard=get_main_keyboard(),
                random_id=random.randint(1, 10**9)
            )
            print(f"✅ Отправлено приветствие")
        
        # Консультация
        elif 'консультаци' in message_text or message_text == 'консультация':
            vk.messages.send(
                user_id=user_id,
                message=get_response('консультация'),
                random_id=random.randint(1, 10**9)
            )
            print(f"✅ Отправлена информация о консультации")
        
        # Написание сайта
        elif 'сайт' in message_text or 'написать сайт' in message_text:
            vk.messages.send(
                user_id=user_id,
                message=get_response('сайт'),
                random_id=random.randint(1, 10**9)
            )
            print(f"✅ Отправлена информация о сайте")
        
        # Приложение
        elif 'приложен' in message_text or message_text == 'приложение':
            vk.messages.send(
                user_id=user_id,
                message=get_response('приложение'),
                random_id=random.randint(1, 10**9)
            )
            print(f"✅ Отправлена информация о приложении")
        
        # Предложить своё
        elif 'предложит' in message_text or 'предложить' in message_text:
            vk.messages.send(
                user_id=user_id,
                message=get_response('предложить'),
                random_id=random.randint(1, 10**9)
            )
            print(f"✅ Отправлена информация о предложении")
        
        # Контакты
        elif 'контакт' in message_text or message_text == 'контакты':
            vk.messages.send(
                user_id=user_id,
                message=get_response('контакты'),
                random_id=random.randint(1, 10**9)
            )
            print(f"✅ Отправлены контакты")
        
        # Если не распознали - показываем меню с клавиатурой
        else:
            vk.messages.send(
                user_id=user_id,
                message="🤔 Не совсем понял вас. Выберите услугу из меню:",
                keyboard=get_main_keyboard(),
                random_id=random.randint(1, 10**9)
            )
            print(f"❌ Не распознано, отправлено меню")