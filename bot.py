import telebot
import os

TOKEN = ''

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_handler(message):
    if not os.path.exists(str(message.from_user.id)):
        os.mkdir(str(message.from_user.id))                                                     #создание папки пользователя
        f = open(os.getcwd() +"\\"+ str(message.from_user.id) + '\\tasks.txt', 'w')             #создание файла для задач
        f.close()
    answer="Привет!) \nЯ бот todo. \nНапиши мне /help, чтобы получить справку о том, что я могу делать"
    bot.send_message(message.from_user.id, answer)
    
        
@bot.message_handler(commands=['help'])                                                         #вывод справки о том, как 
def help_handler(message):                                                                      #пользоваться ботом
    answer="Привет!) \nЯ бот todo. \nНапиши мне /start, чтобы начать. \n"+\
    "/new_item <название задачи> - добавление новой задачи.\n "+\
    "/all - список всех задач.\n "+\
    "/delete <номер задачи> - удаление задачи, после команды введите только номер задачи "
    bot.send_message(message.from_user.id, answer)                          
        
        
@bot.message_handler(commands=['new_item'])                                                     #добавление новой задачи 
def new_item_handler(message):                                                                  #в конец списка задач
    f = open(os.getcwd() +"\\"+ str(message.from_user.id) + '\\tasks.txt', 'a')
    if len(message.text.split())>1:
        f.write(' '.join(message.text.split()[1:]) +'\n')
    else: 
        bot.send_message(message.from_user.id, "Вы не написали задачу")
    f.close()
        

@bot.message_handler(commands=['all'])                                                          #вывод всех задач
def all_handler(message):
    filename = os.getcwd() +"\\"+ str(message.from_user.id) + '\\tasks.txt'
    answer=''
    i=1
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        with open(filename, 'r') as f:
            for line in f:
                answer += str(i)+'. ' + line 
                i+=1
        bot.send_message(message.from_user.id, answer)
    else:
        bot.send_message(message.from_user.id, "Список задач пуст")
    

@bot.message_handler(commands=['delete'])                                                       #удаление задачи
def delete_handler(message):
    if '<' not in message.text and '>' not in message.text and len(message.text.split())>1:
        i = int(message.text.split()[-1])
    
        filename = os.getcwd() +"\\"+ str(message.from_user.id) + '\\tasks.txt'
        with open(filename, 'r') as f:
            lines = f.readlines()
        del lines[i-1]
        
        with open(filename, 'w') as f:
            f.write(''.join(lines))
        
    else:
        bot.send_message(message.from_user.id, "После комманды /delete введите только число")
        

bot.polling()