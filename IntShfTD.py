"""
Текущие цели:
-При запросе пользователя "корзина" выводить не только количество и наименование товара, но и общую стоимость подвидов
товара и стоимость покупки (можно пока только для истребителей)
!Для этого:
переменные со стоимостью товара, подсчет и плейсхолдеры в необходимых местах для вывода соответсвующей информации
-Заказ и оплата?
"""
# импортация модулей

import telebot
from telebot import types
import consts

# создание объекта класса и токен
qb = telebot.TeleBot(consts.token)

# переменные, списки, словари
basket = []
counts = {'TIE-fighter': {'TIE-fighter': 0, 'price': 0}, 'TIE-defender': {'TIE-defender': 0, 'price': 0},
          'TIE-interceptor': {'TIE-interceptor': 0, 'price': 0}, 'all_price': 0}

nwc = {'nwc': None, 'cou': None}

tp_def = 600
tp_fi = 500
tp_int = 750

pic_tie_def = open('imgs/sw_tdef.jpg', 'rb')
pic_tie_fi = open('imgs/sw_tfig.jpg', 'rb')
pic_tie_int = open('imgs/sw_tint.jpg', 'rb')
tie_pics = [pic_tie_fi, pic_tie_def, pic_tie_int]
tt1 = '"TIE-fighter": Самый распрастранённый тип истребителй в рядах Империи.'
tt2 = '"TIE-defender": Новый и усовершенствованный fighter, проект был предложен гранд-адмиралом Трауном.'
tt3 = '"TIE-interceptor": Встречается намного реже и стоит дороже. Отличается более высокой скоростью, ' \
      'чем обычный fighter или defender'
tie_text = [tt1, tt2, tt3]

pic_cruiser_imp = 'http://fractalsponge.net/wp/wp-content/uploads/2017/10/isd72.jpg'
pic_cruiser_hammerhead = 'https://vignette.wikia.nocookie.net/rustarwars/images/3/3a/Hammerhead-class.jpg/revision' \
                         '/latest?cb=20131007130452'
pic_cruiser_venator = 'https://cdnb.artstation.com/p/assets/covers/images/012/253/881/large/' \
                      'anthony-nguyen-screenshot001.jpg?1533833452'
pic_cor = 'https://media.moddb.com/images/groups/1/8/7097/CR95.jpg'

zero = 0

# клавиатуры
markup = types.ReplyKeyboardMarkup(True)  # основная клавиатура, присылается по команде /start
item1 = types.KeyboardButton('Корзина')
item2 = types.KeyboardButton('Каталог')
item3 = types.KeyboardButton('Помощь')
item4 = types.KeyboardButton('Оформление заказа')
markup.add(item1, item2, item3, item4)

markup1 = types.InlineKeyboardMarkup(row_width=3)  # меню TIE типа
but1 = types.InlineKeyboardButton('TIE-fighter', callback_data='tie1')
but2 = types.InlineKeyboardButton('TIE-defender', callback_data='tie2')
but3 = types.InlineKeyboardButton('TIE-interceptor', callback_data='tie3')
but4 = types.InlineKeyboardButton('Мне не подходит ничего из выше предложенного', callback_data='no')
markup1.add(but1, but2, but3, but4)

markup2 = types.InlineKeyboardMarkup(row_width=2)  # ???
bt1 = types.InlineKeyboardButton('Да', callback_data='yes1')
bt2 = types.InlineKeyboardButton('Нет', callback_data='no')
markup2.add(bt1, bt2)

markup3 = types.InlineKeyboardMarkup(row_width=2)  # ???
bt11 = types.InlineKeyboardButton('Да', callback_data='yes2')
bt22 = types.InlineKeyboardButton('Нет', callback_data='no')
markup3.add(bt11, bt22)

markup4 = types.InlineKeyboardMarkup(row_width=2)  # ???
b1t1 = types.InlineKeyboardButton('Да', callback_data='yes3')
b2t2 = types.InlineKeyboardButton('Нет', callback_data='no')
markup4.add(b1t1, b2t2)

markup5 = types.InlineKeyboardMarkup(row_width=2)  # меню типов техники
item001 = types.InlineKeyboardButton('Дроиды', callback_data='droids')
item002 = types.InlineKeyboardButton('Космические корабли', callback_data='space_ships')
item003 = types.InlineKeyboardButton('Оружие', callback_data='weapon')
item004 = types.InlineKeyboardButton('Бытовая техника', callback_data='appliances')
item005 = types.InlineKeyboardButton('"Наземный" транспорт', callback_data='ground_trans')
markup5.add(item001, item002, item003, item004, item005)

star_ships = types.InlineKeyboardMarkup(row_width=1)  # типы космических кораблей
item006 = types.InlineKeyboardButton('TIE-тип', callback_data='tie')
item007 = types.InlineKeyboardButton('Крейсеры, разрушители', callback_data='des')
item008 = types.InlineKeyboardButton('Шатлы', callback_data='stl')
item009 = types.InlineKeyboardButton('Транспортники, грузовые', callback_data='transport cargo')
star_ships.add(item006, item007, item008, item009)

markup6 = types.InlineKeyboardMarkup(row_width=2)  # купи еще что-нибудь)
item010 = types.InlineKeyboardButton('Нет, спасибо', callback_data='no')
item011 = types.InlineKeyboardButton('Да, но из другого раздела', callback_data='other_yes')
item012 = types.InlineKeyboardButton('Да, из другого раздела косм-их кораблей', callback_data='other_yes1')
item013 = types.InlineKeyboardButton('Да, из этого раздела', callback_data='tie')
markup6.add(item010, item011, item012, item013)

count_somth = types.InlineKeyboardMarkup(row_width=3)
item014 = types.InlineKeyboardButton('1', callback_data='+1')
item015 = types.InlineKeyboardButton('3', callback_data='+3')
item016 = types.InlineKeyboardButton('5', callback_data='+5')
item017 = types.InlineKeyboardButton('Другое количество', callback_data='other_count')
count_somth.add(item014, item015, item016)


# функции с декораторами
@qb.message_handler(commands=['start'])
def welcome(message):
    qb.send_message(message.chat.id, 'Добро пожаловать в наш интернет-магазин! '
                                     'Здесь вы можете найти любую технику, от дроида-мыши до космического корабля.',
                    parse_mode='html', reply_markup=markup)


@qb.message_handler(content_types=['text'])
def text_reaction(message):
    if message.text == 'Каталог':
        qb.send_message(message.chat.id, 'Для начала выберите интересующий Вас каталог', reply_markup=markup5)
    elif message.text == 'Корзина':
        if basket == []:
            qb.send_message(message.chat.id, 'Ваша корзина пуста')
        else:
            couel = len(basket)
            for i in range(zero, couel):
                qb.send_message(message.chat.id, '%s. %s * %s \n'
                                                 'Итого за %s: %s' % (i + 1, basket[i], counts[basket[i]][basket[i]],
                                                                      basket[i], counts[basket[i]]['price']))
            qb.send_message(message.chat.id, 'Цена всей покупки: %s' % counts['all_price'])

    elif message.text == 'Помощь':
        qb.send_message(message.chat.id, 'Потыкайте где-нибудь, может из этого выйдет что-то путное')
    elif message.text == 'Оформление заказа':
        qb.send_message(message.chat.id, 'Ваш заказ оформлен, хе-хе.. ')


@qb.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'tie':
                qb.send_message(call.message.chat.id, 'У нас есть несколько кораблей типа TIE на выбор:')
                for i in range(0, 3):
                    qb.send_photo(call.message.chat.id, tie_pics[i], caption='%s' % tie_text[i])
                qb.send_message(call.message.chat.id, 'Выберите подходящий товар:',
                                reply_markup=markup1)

            elif call.data == 'tie1':
                nwc['nwc'] = 'TIE-fighter'
                qb.send_message(call.message.chat.id, 'Выберите необходимое количество товара: ',
                                reply_markup=count_somth)
                # if counts['TIE-fighter']['TIE-fighter'] == 0:
                #     basket.append('TIE-fighter')
                # counts['TIE-fighter']['TIE-fighter'] = counts['TIE-fighter']['TIE-fighter'] + 1
                # counts['TIE-fighter']['price'] = counts['TIE-fighter']['price'] + tp_fi
                # counts['all_price'] = counts['all_price'] + tp_fi
                # qb.send_message(call.message.chat.id, 'Ваш товар добавлен в корзину')

            elif call.data == 'tie2':
                if counts['TIE-defender']['TIE-defender'] == 0:
                    basket.append('TIE-defender')
                counts['TIE-defender']['TIE-defender'] = counts['TIE-defender']['TIE-defender'] + 1
                counts['TIE-defender']['price'] = counts['TIE-defender']['price'] + tp_fi
                counts['all_price'] = counts['all_price'] + tp_def
                qb.send_message(call.message.chat.id, 'Ваш товар добавлен в корзину')

            elif call.data == 'tie3':
                if counts['TIE-interceptor']['TIE-interceptor'] == 0:
                    basket.append('TIE-interceptor')
                counts['TIE-interceptor']['TIE-interceptor'] = counts['TIE-interceptor']['TIE-interceptor'] + 1
                counts['TIE-interceptor']['price'] = counts['TIE-interceptor']['price'] + tp_fi
                counts['all_price'] = counts['all_price'] + tp_int
                qb.send_message(call.message.chat.id, 'Ваш товар добавлен в корзину')

            elif call.data == 'no':
                qb.send_message(call.message.chat.id, 'Надеюсь, Вам еще что-нибудь приглянется')

            elif call.data == 'other_yes':
                qb.send_message(call.message.chat.id, 'Вот разделы техники. Выберите интересующий Вас',
                                reply_markup=markup1)

            elif call.data == 'other_yes1':
                qb.send_message(call.message.chat.id, 'Выберите интересующий Вас тип космического корабля: ',
                                reply_markup=star_ships)

            elif call.data == 'space_ships':
                qb.send_message(call.message.chat.id, 'У нас есть разные типы кораблей на выбор:',
                                reply_markup=star_ships)

            elif call.data == '+1':
                if nwc['nwc'] == 'TIE-fighter':
                    if counts['TIE-fighter']['TIE-fighter'] == 0:
                        basket.append('TIE-fighter')
                    counts['TIE-fighter']['TIE-fighter'] = counts['TIE-fighter']['TIE-fighter'] + 1
                    counts['TIE-fighter']['price'] = counts['TIE-fighter']['price'] + tp_fi
                    counts['all_price'] = counts['all_price'] + tp_fi
                    qb.send_message(call.message.chat.id, 'Ваш товар добавлен в корзину')


            elif call.data == '+3':
                if nwc['nwc'] == 'TIE-fighter':
                    if counts['TIE-fighter']['TIE-fighter'] == 0:
                        basket.append('TIE-fighter')
                    counts['TIE-fighter']['TIE-fighter'] = counts['TIE-fighter']['TIE-fighter'] + 3
                    counts['TIE-fighter']['price'] = counts['TIE-fighter']['price'] + (tp_fi * 3)
                    counts['all_price'] = counts['all_price'] + (tp_fi * 3)
                    qb.send_message(call.message.chat.id, 'Ваш товар добавлен в корзину')


            elif call.data == '+5':
                if nwc['nwc'] == 'TIE-fighter':
                    if counts['TIE-fighter']['TIE-fighter'] == 0:
                        basket.append('TIE-fighter')
                    counts['TIE-fighter']['TIE-fighter'] = counts['TIE-fighter']['TIE-fighter'] + 5
                    counts['TIE-fighter']['price'] = counts['TIE-fighter']['price'] + (tp_fi * 5)
                    counts['all_price'] = counts['all_price'] + (tp_fi * 5)
                    qb.send_message(call.message.chat.id, 'Ваш товар добавлен в корзину')


    except Exception as e:
        print(repr(e))


# пуллинг бота
qb.polling(none_stop=True, interval=0)
