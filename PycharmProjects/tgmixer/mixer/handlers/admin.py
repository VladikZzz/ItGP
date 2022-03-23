import json
from datetime import datetime

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

import api
import config
from handlers.user import cb2
from loader import dp
from utils import States

coin = KeyboardButton('📥 Монеты')
user = KeyboardButton('⚒ Пользователь')
ads = KeyboardButton('✅ Объявления')
orders = KeyboardButton('📬 Заявки')
trades = KeyboardButton('🔁 Сделки')
fake = KeyboardButton('🤡 Фейк объявление')
admin_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(user, ads, orders, trades, fake, coin)

cb = CallbackData("post", "id", "action")


########USER##############

@dp.message_handler(state='*', text='⚒ Пользователь')
async def user_interaction(msg: types.Message):
    add_user = InlineKeyboardButton('🔹 Добавить', callback_data='add_user')
    del_user_ = InlineKeyboardButton('🔹 Удалить', callback_data='del_user')
    ban_user = InlineKeyboardButton('🔹 Заморозить', callback_data='ban_user')
    unban_user = InlineKeyboardButton('🔹 Разморозить', callback_data='unban_user')
    change_limit = InlineKeyboardButton('🔹 Изменить лимит', callback_data='change_limit')
    list_users = InlineKeyboardButton('🔹 Список пользователей', callback_data='list_users')
    change_date = InlineKeyboardButton('🔹 Изменить дату регистрации', callback_data='change_date')
    send_to_users = InlineKeyboardButton('🔹 Отправить всем', callback_data='send_to_users')
    pay_for_ref = InlineKeyboardButton('🔹 Заплатить за реферала', callback_data='pay_for_ref')

    buttons = InlineKeyboardMarkup(row_width=1).add(add_user, del_user_, ban_user, unban_user, change_limit, change_date, list_users, send_to_users, pay_for_ref)
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])
    await msg.answer("<b>Выберите действия:</b>", reply_markup=buttons, parse_mode=types.ParseMode.HTML)


@dp.message_handler(state='*', text='🔁 Сделки')
async def trades(msg: types.Message):
    trades = api.get_trades()
    k = 0
    for trade in trades:
        if trade['state'] != 'cancel':
            k += 1
            cancel = types.InlineKeyboardButton(text="❌ Отменить",
                                              callback_data=cb2.new(id=str(trade['id']), action="cancel_order_from_adm"))
            buttons = [cancel]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            usr = api.get_user_info(trade['to_id'])['username']
            usdt_amount = trade['usdt_amount']
            await msg.answer(f'Сделка c {usr}\n\nСумма: {usdt_amount} USDT', reply_markup=keyboard)
    if k == 0:
        await msg.answer('Нет открытых сделок.')


@dp.message_handler(state='*', text='📬 Заявки')
async def orders(msg: types.Message):
    orders_ = api.get_orders()
    if len(orders_) == 0:
        await msg.answer('👌 Все заявки обработаны')

    for order in orders_:
        u_info = api.get_user_info(order['owner_id'])
        take = types.InlineKeyboardButton(text="⚒ Взять в обработку",
                                          callback_data=cb2.new(id=str(order['id']), action="take_order_process"))
        taken = types.InlineKeyboardButton(text="❌ Уже в обработке, НЕ ТРОГАТЬ",
                                           callback_data=cb2.new(id=str(order['id']), action="taken_order_process"))
        cancel = types.InlineKeyboardButton(text="Отклонить",
                                            callback_data=cb2.new(id=str(order['id']), action="cancel_user_in"))

        if order['type'] == 'deposit' and order['status'] == 'paid':
            if order['flag'] != 'taken':
                buttons = [take, cancel, types.InlineKeyboardButton(text="✅ Подтвердить",
                                                            callback_data=cb2.new(id=str(order['id']),
                                                                                  action="confirm_dep"))]
            else:
                buttons = [taken, cancel, types.InlineKeyboardButton(text="✅ Подтвердить",
                                                             callback_data=cb2.new(id=str(order['id']),
                                                                                   action="confirm_dep"))]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            await msg.answer(f'<b>Депозит монет от </b>' + u_info['username'] + \
                             '\n\n<b>Сумма:</b> ' + str(order['amount']) + ' USDT\n\n' + \
                             '<b>Ссылка на обозреватель: </b>' + order['link'], parse_mode=types.ParseMode.HTML,
                             reply_markup=keyboard)
        elif order['type'] == 'save_deposit' and order['status'] == 'paid':
            if order['flag'] != 'taken':
                buttons = [take, cancel,
                           types.InlineKeyboardButton(text="✅ Подтвердить",
                                                      callback_data=cb2.new(id=str(order['id']),
                                                                            action="confirm_save_dep"))]
            else:
                buttons = [taken, cancel,
                           types.InlineKeyboardButton(text="✅ Подтвердить",
                                                      callback_data=cb2.new(id=str(order['id']),
                                                                            action="confirm_save_dep"))]

            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            await msg.answer(f'<b>Внесение страховочного депозита от </b>' + u_info['username'] + \
                             '\n\n<b>Сумма:</b> ' + str(order['amount']) + ' USDT\n\n' + \
                             '<b>Ссылка на обозреватель: </b>' + order['link'], parse_mode=types.ParseMode.HTML,
                             reply_markup=keyboard)

        elif order['type'] == 'withdraw' and order['status'] == 'created':
            if order['flag'] != 'taken':
                buttons = [take,
                           types.InlineKeyboardButton(text="✅ Выплачено",
                                                      callback_data=cb2.new(id=str(order['id']),
                                                                            action="confirm_withdraw_coins"))
                           ]
            else:
                buttons = [taken,
                           types.InlineKeyboardButton(text="✅ Выплачено",
                                                      callback_data=cb2.new(id=str(order['id']),
                                                                            action="confirm_withdraw_coins"))
                           ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)



            await msg.answer('<b>Вывод монет от </b>' + u_info['username'] + \
                             '\n\n<b>Сумма:</b> ' + str(order['amount']) + ' ' + order['cryptocurrency'] + '\n\n' + \
                             '<b>Адрес для пополнения: </b>' + order['to_adr'],
                             parse_mode=types.ParseMode.HTML,
                             reply_markup=keyboard)

        elif order['type'] == 'save_deposit_out' and order['status'] == 'created':
            if order['flag'] != taken:
                buttons = [take,
                           types.InlineKeyboardButton(text="✅ Выплачено",
                                                      callback_data=cb2.new(id=str(order['id']),
                                                                            action="confirm_withdraw_coins"))
                           ]
            else:
                buttons = [taken,
                           types.InlineKeyboardButton(text="✅ Выплачено",
                                                      callback_data=cb2.new(id=str(order['id']),
                                                                            action="confirm_withdraw_coins"))
                           ]

            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)

            await msg.answer('<b>Возврат депозита от </b>' + u_info['username'] + \
                             '\n\n<b>Сумма:</b> ' + str(order['amount']) + ' USDT\n\n' + \
                             '<b>Адрес для пополнения: </b>' + u_info['address_USDT'],
                             parse_mode=types.ParseMode.HTML,
                             reply_markup=keyboard)

        elif order['type'] == 'save_deposit_out' and order['status'] == 'dispute':
            button1 = types.InlineKeyboardButton(text='Связаться', url='tg://user?id='+str(order['owner_id']))
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            addr = order['to_adr']
            await msg.answer('🆘 <b>ДИСПУТ</b>\n\n' + '<b>Вывод монет от </b>' + u_info['username'] + \
                             '\n\n<b>Сумма:</b> ' + str(order['amount']) + ' ' + order['cryptocurrency'] + '\n\n' + \
                             '<b>Адрес для пополнения: </b>' + addr,
                             parse_mode=types.ParseMode.HTML,
                             reply_markup=keyboard)

        elif order['type'] == 'withdraw' and order['status'] == 'dispute':
            button1 = types.InlineKeyboardButton(text='Связаться', url='tg://user?id=' + str(order['owner_id']))
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            addr = order['to_adr']
            await msg.answer('🆘 <b>ДИСПУТ</b>\n\n' + '<b>Возврат депозита от </b>' + u_info['username'] + \
                             '\n\n<b>Сумма:</b> ' + str(order['amount']) + ' USDT\n\n' + \
                             '<b>Адрес для пополнения: </b>' + addr,
                             parse_mode=types.ParseMode.HTML,
                             reply_markup=keyboard)



@dp.message_handler(state='*', text='✅ Объявления')
async def ads(msg: types.Message):
    ads = api.get_ads()
    buttons = []
    for ad in ads:
        owner_info = api.get_user_info(ad['owner_id'])
        api.change_ad_amount(ad['id'], owner_info['USDT_balance'])

    ads = api.get_ads()
    for ad in ads:
        if ad['max_amount'] < ad['min_amount']:
            api.change_ad_state(ad['id'], False)

        if ad['max_amount'] >= ad['max_amount'] and ad['state'] == False:
            api.change_ad_state(ad['id'], True)

    ads = api.get_ads()
    for ad in ads:
        owner_info = api.get_user_info(ad['owner_id'])

        if ad['state'] and owner_info['state'] == 'working':
            button = types.InlineKeyboardButton(
                text=owner_info['username'] + ' ' + str(ad['min_amount']) + ' - ' + str(ad['max_amount']),
                callback_data=cb2.new(id=str(ad['id']), action="user_ad_admin"))

            buttons.append(button)

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    await msg.answer('Доска объявлений:', reply_markup=keyboard)


@dp.message_handler(state='*', text='🤡 Фейк объявление')
async def fake_ad(msg: types.Message):
    create = InlineKeyboardButton('🔸 Создать', callback_data='create_fake')
    edit = InlineKeyboardButton('🔹 Редактивровать', callback_data='edit_fake')

    buttons = InlineKeyboardMarkup(row_width=2).add(create, edit)

    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])

    await msg.answer('Выберите', reply_markup=buttons, parse_mode=types.ParseMode.HTML)


@dp.message_handler(state='*', text='📥 Монеты')
async def coin_interaction(msg: types.Message):
    add_coin = InlineKeyboardButton('Добавить адрес', callback_data='add_coin')
    del_coin = InlineKeyboardButton('Удалить адрес', callback_data='del_coin')
    edit_coin = InlineKeyboardButton('Изменить адрес', callback_data='edit_coin')

    buttons = InlineKeyboardMarkup(row_width=1).add(add_coin, del_coin, edit_coin)
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])
    await msg.answer("<b>Выберите действия:</b>", reply_markup=buttons, parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(cb2.filter(action=["take_order_process"]), state='*')
async def take_order_next_call(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    order_id = callback_data['id']
    try:
        api.change_order_flag(order_id, 'taken')

        order = api.get_order_info(order_id)

        await call.message.edit_reply_markup()
        taken = types.InlineKeyboardButton(text="❌Уже в обработке, НЕ ТРОГАТЬ",
                                           callback_data=cb2.new(id=str(order['id']), action="taken_order"))
        cancel = types.InlineKeyboardButton(text="Отклонить",
                                            callback_data=cb2.new(id=str(order['id']), action="cancel_user_in"))

        if order['type'] == 'deposit' and order['status'] == 'paid':
            buttons = [taken, cancel, types.InlineKeyboardButton(text="✅ Подтвердить",
                                                         callback_data=cb2.new(id=str(order['id']),
                                                                               action="confirm_dep"))]
        elif order['type'] == 'save_deposit' and order['status'] == 'paid':
            buttons = [taken, cancel,
                       types.InlineKeyboardButton(text="✅ Подтвердить",
                                                  callback_data=cb2.new(id=str(order['id']),
                                                                        action="confirm_save_dep"))]

        elif order['type'] == 'withdraw' and order['status'] == 'created':
            buttons = [taken,
                       types.InlineKeyboardButton(text="Выплачено",
                                                  callback_data=cb2.new(id=str(order['id']),
                                                                        action="confirm_withdraw_coins"))
                       ]


        elif order['type'] == 'save_deposit_out' and order['status'] == 'created':
            buttons = [taken,
                       types.InlineKeyboardButton(text="Выплачено",
                                                  callback_data=cb2.new(id=str(order['id']),
                                                                        action="confirm_withdraw_coins"))
                       ]

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)
        await call.message.edit_reply_markup(keyboard)
    except KeyError:
        await call.answer('Заявка уже обработана')


@dp.callback_query_handler(state=States.ADMIN_STATE, text="edit_fake")
async def edit_fake(call: types.CallbackQuery):
    fake_ads = api.get_fake_ads()
    buttons = []
    for ad in fake_ads:
        button = types.InlineKeyboardButton(
            text=ad['owner_name'] + ' ' + str(ad['min_amount']) + ' - ' + str(ad['max_amount']),
            callback_data=cb2.new(id=str(ad['id']), action="fake_ad_edit"))
        buttons.append(button)

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    await call.message.answer('Выберите', reply_markup=keyboard, parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(cb2.filter(action=["fake_ad_edit"]), state='*')
async def choosen_fake(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    ad_id = callback_data['id']

    delete = InlineKeyboardButton('🔹 Удалить', callback_data=cb2.new(id=str(ad_id), action="fake_ad_delete"))
    min_limit = InlineKeyboardButton('🔹 Минимальный лимит', callback_data=cb2.new(id=str(ad_id), action="fake_ad_min"))
    max_limit = InlineKeyboardButton('🔹 Минимальный лимит', callback_data=cb2.new(id=str(ad_id), action="fake_ad_max"))
    fake_count = InlineKeyboardButton('🔹 Количество сделок',
                                      callback_data=cb2.new(id=str(ad_id), action="fake_ad_count"))
    fake_amount = InlineKeyboardButton('🔹 Объем сделок', callback_data=cb2.new(id=str(ad_id), action="fake_ad_amount"))
    buttons = InlineKeyboardMarkup(row_width=2).add(delete, min_limit, max_limit, fake_count, fake_amount)
    await call.message.answer('Выберите действие', reply_markup=buttons)


@dp.callback_query_handler(cb2.filter(action=["fake_ad_delete"]), state='*')
async def delete_fake(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    ad_id = callback_data['id']
    api.delete_fake(ad_id)
    await call.answer('Объявление удалено')


@dp.callback_query_handler(cb2.filter(action=["fake_ad_min"]), state='*')
async def min_fake(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    ad_id = callback_data['id']
    async with state.proxy() as data:
        data['ad_id'] = ad_id
    await call.message.answer('Укажите новый минимальный лимит')
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.NEW_FAKE_MIN[0])


@dp.message_handler(state=States.NEW_FAKE_MIN)
async def new_min_fake(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ad_id = data['ad_id']

    new_min = msg.text
    api.change_fake_min(ad_id, new_min)


@dp.callback_query_handler(cb2.filter(action=["fake_ad_count"]), state='*')
async def fake_count(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    ad_id = callback_data['id']
    async with state.proxy() as data:
        data['ad_id'] = ad_id
    await call.message.answer('Укажите новое количество сделок')
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.NEW_FAKE_COUNT[0])


@dp.message_handler(state=States.NEW_FAKE_COUNT)
async def new_fake_count(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ad_id = data['ad_id']

    new_c = msg.text
    api.change_fake_count(ad_id, new_c)


@dp.callback_query_handler(cb2.filter(action=["fake_ad_amount"]), state='*')
async def fake_amount(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    ad_id = callback_data['id']
    async with state.proxy() as data:
        data['ad_id'] = ad_id
    await call.message.answer('Укажите новый объем сделок сделок')
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.NEW_FAKE_AMOUNT[0])


@dp.message_handler(state=States.NEW_FAKE_AMOUNT)
async def new_fake_amount(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ad_id = data['ad_id']

    new_amount = msg.text
    api.change_fake_amount(ad_id, new_amount)


@dp.callback_query_handler(cb2.filter(action=["fake_ad_max"]), state='*')
async def max_fake(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    ad_id = callback_data['id']
    async with state.proxy() as data:
        data['ad_id'] = ad_id
    await call.message.answer('Укажите новый максимальный лимит')
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.NEW_FAKE_MAX[0])


@dp.message_handler(state=States.NEW_FAKE_MAX)
async def new_max_fake(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        ad_id = data['ad_id']

    new_max = msg.text
    api.change_fake_max(ad_id, new_max)


@dp.callback_query_handler(state=States.ADMIN_STATE, text="create_fake")
async def create_fake(call: types.CallbackQuery):
    await call.message.answer('Введите имя пользователя')
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.FAKE_NAME[0])


@dp.message_handler(state=States.FAKE_NAME)
async def fake_name(msg: types.Message, state: FSMContext):
    fake_name = msg.text
    async with state.proxy() as data:
        data['fake_name'] = fake_name

    await msg.answer('Введите количество сделок')
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.FAKE_TRADE_NUMBER[0])


@dp.message_handler(state=States.FAKE_TRADE_NUMBER)
async def fake_trade_number(msg: types.Message, state: FSMContext):
    fake_trade_number = msg.text
    async with state.proxy() as data:
        data['fake_trade_number'] = fake_trade_number

    await msg.answer('Введите объем торгов')
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.FAKE_TRADE_AMOUNT[0])


@dp.message_handler(state=States.FAKE_TRADE_AMOUNT)
async def fake_trade_amount(msg: types.Message, state: FSMContext):
    fake_trade_amount = msg.text
    async with state.proxy() as data:
        data['fake_trade_amount'] = fake_trade_amount

    await msg.answer('Введите дату регистрации в формате год-месяц-день')
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.FAKE_DATE[0])


@dp.message_handler(state=States.FAKE_DATE)
async def fake_date(msg: types.Message, state: FSMContext):
    fake_date = msg.text
    async with state.proxy() as data:
        data['fake_date'] = fake_date

    await msg.answer('Введите минимальный лимит')
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.FAKE_MIN_LIMIT[0])


@dp.message_handler(state=States.FAKE_MIN_LIMIT)
async def fake_min_limit(msg: types.Message, state: FSMContext):
    fake_min_limit = msg.text
    async with state.proxy() as data:
        data['fake_min_limit'] = fake_min_limit

    await msg.answer('Введите максимальный лимит')
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.FAKE_MAX_LIMIT[0])


@dp.message_handler(state=States.FAKE_MAX_LIMIT)
async def fake_des(msg: types.Message, state: FSMContext):
    fake_max_limit = msg.text
    async with state.proxy() as data:
        fake_min_limit = data['fake_min_limit']
        fake_date = data['fake_date']
        fake_trade_amount = data['fake_trade_amount']
        fake_trade_number = data['fake_trade_number']
        fake_name = data['fake_name']

    date = datetime.strptime(fake_date, '%Y-%m-%d').date()
    id_ = len(api.get_fake_ads()) + 1
    api.create_fake_ad(id_, fake_name, int(fake_trade_number), float(fake_trade_amount), date, float(fake_min_limit),
                       float(fake_max_limit), fake_des)
    await msg.answer('Фейк объявление успешно добавлено!')
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])


@dp.callback_query_handler(state=States.ADMIN_STATE, text="add_user")
async def add_user(call: types.CallbackQuery):
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])

    await call.message.answer("<b>Дайте юзернейм пользователю:</b>\n", parse_mode=types.ParseMode.HTML)
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.ADD_ID[0])
    await call.answer()


@dp.message_handler(state=States.ADD_ID)
async def generate(msg: types.Message, state: FSMContext):
    username = msg.text

    async with state.proxy() as data:
        data['username'] = username

    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])

    await msg.answer("<b>Введите telegram-ID нового пользователя:</b>\n", parse_mode=types.ParseMode.HTML)
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADD_TOKEN[0])


@dp.message_handler(state=States.ADD_TOKEN)
async def add_token(msg: types.Message, state: FSMContext):
    tg_id = msg.text

    async with state.proxy() as data:
        data['tg_id'] = tg_id

    adm = InlineKeyboardButton('😎 Админ', callback_data=cb.new(id=msg.text, action='adm'))
    usr = InlineKeyboardButton('💩 Пользователь', callback_data=cb.new(id=msg.text, action='usr'))
    buttons = InlineKeyboardMarkup(row_width=2).add(adm, usr)

    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])

    await msg.answer("<b>Выберите тип нового токена:</b>\n", reply_markup=buttons, parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(cb.filter(action=['adm']), state=States.ADMIN_STATE)
async def add_admin(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    uid = int(callback_data["id"])
    token = 'A-' + str((uid // 3))

    async with state.proxy() as data:
        username = data['username']
        tg_id = data['tg_id']

    await call.message.answer('💡 <b>Пользователь добавлен!\n </b>' + 'Токен:' + token,
                              parse_mode=types.ParseMode.HTML)
    api.add_user(username, token, tg_id, 0, 0, 'admin', 'address_USDT')
    api.change_user_state(tg_id, 'no_deposit')

    await call.answer()


@dp.callback_query_handler(cb.filter(action=['usr']), state=States.ADMIN_STATE)
async def set_limit(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    uid = int(callback_data["id"])
    token = 'USRMCNT' + str((uid // 3))

    async with state.proxy() as data:
        data['token'] = token

    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])

    await call.message.answer('💡 <b>Установите еженедельный лимит:</b> ', parse_mode=types.ParseMode.HTML)
    await call.answer()

    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.LIMIT[0])
    await call.answer()


@dp.message_handler(state=States.LIMIT)
async def add_USDT_address(msg: types.Message, state: FSMContext):
    limit = msg.text

    async with state.proxy() as data:
        data['limit'] = limit

    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])

    await msg.answer("<b>Установите USDT TRC-20 адрес пользователя:</b>\n", parse_mode=types.ParseMode.HTML)
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADD_TRX_ADDRESS[0])


@dp.message_handler(state=States.ADD_TRX_ADDRESS)
async def USDT_address(msg: types.Message, state: FSMContext):
    USDT_address = msg.text

    async with state.proxy() as data:
        username = data['username']
        tg_id = data['tg_id']
        token = data['token']
        limit = data['limit']

    api.add_user(username, token, tg_id, limit, limit, 'user', USDT_address)
    await msg.answer('💡 <b>Пользователь добавлен!\n </b>' + 'Токен: ' + token, parse_mode=types.ParseMode.HTML)
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])


@dp.callback_query_handler(state=States.ADMIN_STATE, text="del_user")
async def del_user(call: types.CallbackQuery):
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])

    await call.message.answer(f'<b>Введите TG-ID пользователя:</b>', parse_mode=types.ParseMode.HTML)
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.DEL_USR[0])
    await call.answer()


@dp.message_handler(state=States.DEL_USR)
async def del_user_next(msg: types.Message):
    tg_id_ = msg.text
    api.delete_user(tg_id_)

    ads = api.get_user_ads(tg_id_)
    for ad in ads:
        api.delete_ad(ad['id'])

    await msg.answer("❗ Пользователь удалён")

    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])

    state = dp.current_state(chat=tg_id_, user=tg_id_)
    await state.set_state(States.UNAUTHORIZED_STATE[0])

    await dp.bot.send_message(str(tg_id_), f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>', parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(state=States.ADMIN_STATE, text="ban_user")
async def ban_user(call: types.CallbackQuery):
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])

    await call.message.answer(f'<b>Введите TG-ID пользователя:</b>', parse_mode=types.ParseMode.HTML)
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.BAN_USR[0])
    await call.answer()


@dp.message_handler(state=States.BAN_USR)
async def ban_user_next(msg: types.Message):
    tg_id_ = msg.text
    await msg.answer("❗ Пользователь заморожен")
    api.change_user_state(tg_id_, 'banned')

    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])

    state = dp.current_state(chat=tg_id_, user=tg_id_)
    await state.set_state(States.BANNED[0])
    button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
    buttons_ = [button1]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons_)

    await dp.bot.send_message(str(tg_id_), f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.', parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


@dp.callback_query_handler(state=States.ADMIN_STATE, text="unban_user")
async def unban_user(call: types.CallbackQuery):
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])

    await call.message.answer(f'<b>Введите TG-ID пользователя:</b>', parse_mode=types.ParseMode.HTML)
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.UNBAN_USR[0])
    await call.answer()


@dp.message_handler(state=States.UNBAN_USR)
async def unban_user_next(msg: types.Message):
    tg_id_ = msg.text
    await msg.answer("❗ Пользователь разморожен")

    api.change_user_state(tg_id_, 'working')

    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])

    state = dp.current_state(chat=tg_id_, user=tg_id_)
    await state.set_state(States.USER_STATE[0])

    await dp.bot.send_message(str(tg_id_), f'<b>🎉 Ваша учётная запись разморожена.</b> Можете продолжать пользоваться платформой.', parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(state=States.ADMIN_STATE, text="change_limit")
async def change_limit(call: types.CallbackQuery):
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])

    await call.message.answer(f'<b>Введите TG-ID пользователя:</b>', parse_mode=types.ParseMode.HTML)
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.CHANGE_LIMIT[0])
    await call.answer()


@dp.message_handler(state=States.CHANGE_LIMIT)
async def get_id_for_limit(msg: types.Message):
    global tg_id_for_limit
    tg_id_for_limit = msg.text
    await msg.answer("Установите новый лимит:")

    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])

    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.TYPE_LIMIT[0])


@dp.message_handler(state=States.TYPE_LIMIT)
async def change_limit_next(msg: types.Message):
    new_limit = msg.text
    await msg.answer("Лимит успешно изменён!")

    info = api.get_user_info(tg_id_for_limit)
    range = int(new_limit) - info['limit']
    api.change_limit(info['username'], info['token'], info['tg_id'], int(new_limit), info['current_limit'] + range,
                     info['role'])

    await dp.bot.send_message(str(tg_id_for_limit), f'<b>У вас изменён ежедневный лимит!</b>',
                              parse_mode=types.ParseMode.HTML)

    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])


@dp.callback_query_handler(state=States.ADMIN_STATE, text="change_date")
async def change_date(call: types.CallbackQuery):
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])

    await call.message.answer(f'<b>Введите TG-ID пользователя:</b>', parse_mode=types.ParseMode.HTML)
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.CHANGE_DATE[0])
    await call.answer()


@dp.message_handler(state=States.CHANGE_DATE)
async def get_id_for_date(msg: types.Message, state: FSMContext):
    tg_id_date = msg.text
    async with state.proxy() as data:
        data['tg_id_date'] = tg_id_date

    await msg.answer("Установите новую дату в формате год-месяц-день:")

    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])

    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.TYPE_DATE[0])


@dp.message_handler(state=States.TYPE_DATE)
async def change_date_next(msg: types.Message, state: FSMContext):
    new_date = msg.text
    async with state.proxy() as data:
        tg_id_date = data['tg_id_date']

    api.change_reg_date(tg_id_date, new_date)
    await msg.answer("Дата регистрации успешно изменена!")

    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])


@dp.callback_query_handler(state=States.ADMIN_STATE, text="pay_for_ref")
async def pay_for_ref(call: types.CallbackQuery):
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])

    await call.message.answer(f'<b>Введите промо-код пользователя которому начислить награду:</b>', parse_mode=types.ParseMode.HTML)
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.PROMO_CODE[0])
    await call.answer()


@dp.message_handler(state=States.PROMO_CODE)
async def promo_code(msg: types.Message, state: FSMContext):
    code = msg.text
    users = api.get_all_users()
    for u in users:
        c = 'REF'+str(int(u['tg_id']) // 5 + 123)
        if c == code:
            api.change_coin_balance(u['tg_id'], 30, 'plus', 'USDT')
            await dp.bot.send_message(str(u['tg_id']), f'<b>🎉 Вам начислена награда 30 USDT за реферала</b>', parse_mode=types.ParseMode.HTML)
            break

    await msg.answer("Награда начислена")

    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])



@dp.callback_query_handler(state=States.ADMIN_STATE, text="send_to_users")
async def send_to_users(call: types.CallbackQuery):
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])

    await call.message.answer(f'<b>Введите текст который хотите отправить всем пользователям</b>', parse_mode=types.ParseMode.HTML)
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.SEND_TO_ALL[0])
    await call.answer()


@dp.message_handler(state=States.SEND_TO_ALL)
async def send_to_all(msg: types.Message, state: FSMContext):
    mes = msg.text
    users = api.get_all_users()
    for u in users:
        if u['role'] == 'user':
            await dp.bot.send_message(str(u['tg_id']), mes)

    await msg.answer("Сообщение отправлено всем пользователям")

    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])


@dp.callback_query_handler(state=States.ADMIN_STATE, text="list_users")
async def list_users(call: types.CallbackQuery):
    users = api.get_all_users()
    mess = "<b>Активные польватели:\n\n</b> "
    for u in users:
        if u['role'] == 'user':
            un = u['username']
            t = u['token']
            id_ = str(u['tg_id'])
            lim = str(u['limit'])
            c_lim = str(u['current_limit'])
            m = '<b>Юзернейм: </b>' + un + '\n' + '<b>Токен: </b>' + t + '\n' + '<b>TG ID: </b>' + id_ + '\n' + '<b>Ежедневный лимит: </b>' + lim + '\n' + '<b>Лимит на сегодня: </b>' + c_lim + '\n\n '
            mess += m

    await call.message.answer(mess, parse_mode=types.ParseMode.HTML)


################COIN################

@dp.callback_query_handler(state=States.ADMIN_STATE, text="add_coin")
async def add_coin(call: types.CallbackQuery):
    button1 = types.InlineKeyboardButton(text='USDT', callback_data=cb2.new(id=str('USDT'), action="add_addr"))
    button2 = types.InlineKeyboardButton(text='TRX', callback_data=cb2.new(id=str('TRX'), action="add_addr"))
    button3 = types.InlineKeyboardButton(text='XLM', callback_data=cb2.new(id=str('XLM'), action="add_addr"))
    button4 = types.InlineKeyboardButton(text='ADA', callback_data=cb2.new(id=str('ADA'), action="add_addr"))
    button5 = types.InlineKeyboardButton(text='DOGE', callback_data=cb2.new(id=str('DOGE'), action="add_addr"))
    button6 = types.InlineKeyboardButton(text='MATIC', callback_data=cb2.new(id=str('MATIC'), action="add_addr"))
    button7 = types.InlineKeyboardButton(text='LUNA', callback_data=cb2.new(id=str('LUNA'), action="add_addr"))
    button8 = types.InlineKeyboardButton(text='DOT', callback_data=cb2.new(id=str('DOT'), action="add_addr"))
    button9 = types.InlineKeyboardButton(text='AVAX', callback_data=cb2.new(id=str('AVAX'), action="add_addr"))


    buttons_ = [button1, button2, button3, button4, button5, button6, button7, button8, button9]
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons_)

    await call.message.answer("<b>Выберите монету:</b>\n", parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(cb2.filter(action=["add_addr"]), state='*')
async def add_addr(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    coin = callback_data["id"]
    async with state.proxy() as data:
        data['new_coin'] = coin

    await call.message.answer('<b>Укажите сеть:</b>', parse_mode=types.ParseMode.HTML)
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.NETWORK[0])


@dp.message_handler(state=States.NETWORK)
async def add_network(msg: types.Message, state: FSMContext):
    network = msg.text
    async with state.proxy() as data:
        data['network'] = network

    await msg.answer("<b>Введите адрес кошелька:</b>\n", parse_mode=types.ParseMode.HTML)

    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADDRESS[0])


@dp.message_handler(state=States.ADDRESS)
async def add_address(msg: types.Message, state: FSMContext):
    address = msg.text
    async with state.proxy() as data:
        network = data['network']
        tiker = data['new_coin']

    response = api.add_coin(tiker, network, address)

    if response.status_code == 400:
        await msg.answer("<b>Данная монета уже добавлена!</b>\n", parse_mode=types.ParseMode.HTML)
    else:
        await msg.answer("<b>Новая монета успешно добавлена!</b>\n", parse_mode=types.ParseMode.HTML)

    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])


@dp.callback_query_handler(state=States.ADMIN_STATE, text="del_coin")
async def del_coin(call: types.CallbackQuery):
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])
    coins = api.get_coins()
    buttons_ = []
    for coin in coins:
        button1 = types.InlineKeyboardButton(text=coin['tiker'], callback_data=cb2.new(id=str(coin['tiker']), action="del_addr"))
        buttons_.append(button1)
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(*buttons_)

    if len(buttons_) != 0:
        await call.message.answer("<b>Выберите монету:</b>\n", parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    else:
        await call.answer('Нечего удалять')

    await call.answer()


@dp.callback_query_handler(cb2.filter(action=["del_addr"]), state='*')
async def del_addr(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    coin = callback_data["id"]
    api.delete_coin(coin)

    await call.answer('Монета удалена')
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])


@dp.callback_query_handler(state=States.ADMIN_STATE, text="edit_coin")
async def edit_coin(call: types.CallbackQuery):
    coins = api.get_coins()
    buttons_ = []
    for coin in coins:
        button1 = types.InlineKeyboardButton(text=coin['tiker'],
                                             callback_data=cb2.new(id=str(coin['tiker']), action="edit_addr"))
        buttons_.append(button1)
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        keyboard.add(*buttons_)

    if len(buttons_) != 0:
        await call.message.answer("<b>Выберите монету:</b>\n", parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    else:
        await call.answer('Нечего изменять')

    await call.answer()


@dp.callback_query_handler(cb2.filter(action=["edit_addr"]), state='*')
async def del_addr(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    coin = callback_data["id"]

    async with state.proxy() as data:
        data['coin_'] = coin

    await call.message.answer('Введите новый адрес')
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.NEW_COIN_ADDR[0])


@dp.message_handler(state=States.NEW_COIN_ADDR)
async def new_coin_addr(msg: types.Message, state: FSMContext):
    new_addr = msg.text
    async with state.proxy() as data:
        tiker = data['coin_']
    api.change_coin_addr(tiker, new_addr)
    await msg.answer('Адрес изменён')
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.ADMIN_STATE[0])


@dp.callback_query_handler(cb2.filter(action=['confirm_dep']), state='*')
async def confirm_dep(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    order_id = int(callback_data["id"])
    try:
        o_info = api.get_order_info(order_id)
        api.change_USDT_balance(o_info['owner_id'], o_info['amount'], 'plus')
        api.change_order_status(order_id, 'confirmed')
        await dp.bot.send_message(str(o_info['owner_id']), f'<b>Ваш депозит </b>' + str(o_info['amount']) + '<b>USDT '
                                                                                                            'зачислен на '
                                                                                                            'Ваш '
                                                                                                            'баланс!</b>',
                                  parse_mode=types.ParseMode.HTML)
        api.delete_order(order_id)
        await call.answer('Депозит подтверждён')
    except KeyError:
        await call.answer('Данный депозит уже обработан.')


@dp.callback_query_handler(cb2.filter(action=["cancel_user_in"]), state='*')
async def cancel_user_in(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    order = api.get_order_info(callback_data['id'])
    u = api.get_user_info(order['owner_id'])
    try:
        if order['status'] != 'paid':
            await call.message.answer('Ошибка!')
        else:
            api.delete_order(order['id'])
            await call.message.answer('✅ Ввод отменён')
            amount = order['amount']
            tiker = order['cryptocurrency']
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await dp.bot.send_message(str(order['owner_id']),
                                      f'<b>❌ Ваш депозит на сумму {amount} {tiker} отклонён.</b>\n\nДля уточнения деталей свяжитесь со службой поддержки.',
                                      parse_mode=types.ParseMode.HTML, reply_markup=keyboard)

            await call.answer()
            state = dp.current_state(user=call.from_user.id)
            await state.set_state(States.ADMIN_STATE[0])
    except KeyError:
        await call.message.answer('Ошибка!')

    await call.answer()


@dp.callback_query_handler(cb2.filter(action=['confirm_save_dep']), state='*')
async def confirm_save_dep(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    try:
        order_id = int(callback_data["id"])
        o_info = api.get_order_info(order_id)
        api.change_order_status(order_id, 'confirmed')
        api.change_user_state(o_info['owner_id'], 'working')

        await dp.bot.send_message(str(o_info['owner_id']),
                                  f'<b>Ваш страховочный депозит зачислен, приятной торговли!</b>',
                                  parse_mode=types.ParseMode.HTML)
        api.delete_order(order_id)
        await call.answer('Депозит подтверждён')
    except KeyError:
        await call.answer('Данный депозит уже обработан.')


@dp.callback_query_handler(cb2.filter(action=['confirm_withdraw_coins']), state='*')
async def confirm_USDT_withdraw(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    try:
        order_id = int(callback_data["id"])
        o_info = api.get_order_info(order_id)
        api.change_order_status(order_id, 'paid')

        buttons = [
            types.InlineKeyboardButton(text="Получено",
                                       callback_data=cb2.new(id=str(order_id), action="confirm")),
            types.InlineKeyboardButton(text="Не получено",
                                       callback_data=cb2.new(id=str(order_id), action="not_confirm"))
        ]
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)

        await dp.bot.send_message(str(o_info['owner_id']),
                                  f'<b>💸 Проверьте постуление</b>\n\n<b>Сумма:</b> ' + str(o_info['amount']) + ' ' + o_info[
                                      'cryptocurrency'] + '\n<b>Адрес получения:</b> ' + o_info['to_adr'],
                                  parse_mode=types.ParseMode.HTML, reply_markup=keyboard)

        await call.answer('Вывод подтверждён')
    except KeyError:
        await call.answer('Заявка уже обработана')



@dp.callback_query_handler(cb2.filter(action=["user_ad_admin"]), state='*')
async def user_ad(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    ad_id = callback_data['id']
    date = datetime.now()
    ad = api.get_ad_info(ad_id)
    owner_info = api.get_user_info(ad['owner_id'])

    reg_date = datetime.strptime(owner_info['reg_date'], '%Y-%m-%d')
    active_period = (date - reg_date).days
    mes = 'Пользователь ' + owner_info['username'] + '\n\n' + \
          'Время работы на платформе: ' + str(active_period) + ' дней' + \
          '\nКоличество проведенных сделок: ' + str(owner_info['trade_count']) + \
          '\nОбщий объём проведенных сделок: ' + str(owner_info['trade_amount']) + ' TRX' + \
          '\n\n' + str(ad['description'])

    button = types.InlineKeyboardButton(text='Создать сделку',
                                        callback_data=cb2.new(id=str(ad['id']), action="create_order"))

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.row(button)
    await call.message.answer(mes, reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(cb2.filter(action=["create_order"]), state='*')
async def create_order(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    ad_id = callback_data['id']

    async with state.proxy() as data:
        data['ad_id'] = ad_id

    ad_info = api.get_ad_info(ad_id)
    ad_amount = ad_info['max_amount']
    await call.message.answer(
        'Укажите сумму сделки от ' + str(ad_info['min_amount']) + ' - ' + str(ad_amount) + 'USDT: ')
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.TYPE_TRADE_AMOUNT[0])


@dp.message_handler(state=States.TYPE_TRADE_AMOUNT)
async def type_amount_usdt(msg: types.Message, state: FSMContext):
    trade_amount = msg.text
    async with state.proxy() as data:
        ad_id = data['ad_id']

    await state.set_state(States.CHOOSE_COIN_FOR_TRADE[0])
    if float(trade_amount) > api.get_ad_info(ad_id)['max_amount'] or float(trade_amount) < api.get_ad_info(ad_id)[
        'min_amount']:
        state = dp.current_state(user=msg.from_user.id)
        await msg.answer('Некорректный ввод, попробуйте еще раз!')
        await state.set_state(States.TYPE_TRADE_AMOUNT[0])

    else:
        async with state.proxy() as data:
            data['trade_amount'] = trade_amount
        coins = api.get_coins()
        buttons = []
        for coin in coins:
            if str(coin['tiker']) != 'USDT':
                b = types.InlineKeyboardButton(text=str(coin['tiker']),
                                               callback_data=cb2.new(id=str(coin['tiker']), action="choose_coin"))
                buttons.append(b)

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(*buttons)

        await msg.answer('Выберите монету для трейда:', reply_markup=keyboard)


@dp.callback_query_handler(cb2.filter(action=['choose_coin']), state='*')
async def choose_coin(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    tiker = callback_data['id']

    async with state.proxy() as data:
        data['tiker'] = tiker

    await call.message.answer('Укажите процент сделки:')
    state = dp.current_state(user=call.from_user.id)
    await state.set_state(States.TYPE_PERCENT[0])


@dp.message_handler(state=States.TYPE_PERCENT)
async def type_percent(msg: types.Message, state: FSMContext):
    percent = msg.text
    async with state.proxy() as data:
        ad_id = data['ad_id']
        trade_amount = data['trade_amount']
        tiker = data['tiker']

    ad_info = api.get_ad_info(ad_id)
    owner_info = api.get_user_info(ad_info['owner_id'])

    trade_id = len(api.get_trades()) + 1

    url = "https://api.bittrex.com/api/v1.1/public/getticker?market=USD-" + str(tiker)

    j = requests.get(url)
    data = json.loads(j.text)
    price = data['result']['Ask']

    coin_amount = float(trade_amount) / price + (float(trade_amount) * float(percent) / 100 / price)

    api.add_trade(trade_id, int(owner_info['tg_id']), 'created', float(trade_amount), float(coin_amount), str(tiker))
    await msg.answer('Сделка отправлена пользователю!')

    button = types.InlineKeyboardButton(text='Принять',
                                        callback_data=cb2.new(id=str(trade_id), action="take_order"))
    button2 = types.InlineKeyboardButton(text='Отклонить',
                                         callback_data=cb2.new(id=str(trade_id), action="cancel_order"))

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.row(button, button2)

    await dp.bot.send_message(str(owner_info['tg_id']), f'<b>🔥 Новая сделка! </b>' + '\n\n'
                              + '<b>С вашего баланса будет списано: </b>' + str(trade_amount) +
                              ' USDT' + '\n' + '<b>На ваш аккаунт будет начислено: </b>' + str(coin_amount) +
                              ' ' + str(tiker) + '\n' + '<b>Чистая прибыльность: </b>' + str(
        percent) + '%\n\n⚠️<b>Внимание</b> ⚠️\n\nИгнорирование сделки может привести к применению штрафных санкций!\n\n<i>Процент прибыльности считается по курсу USDT/' + str(
        tiker) + ' биржи Bittrex</i>',
                              parse_mode=types.ParseMode.HTML, reply_markup=keyboard)


@dp.callback_query_handler(cb2.filter(action=['take_order']), state='*')
async def take_order(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    trade_id = callback_data['id']
    trade_info = api.get_trade_info(trade_id)
    if trade_info['state'] == 'created':
        api.change_USDT_balance(trade_info['to_id'], trade_info['usdt_amount'], 'minus')
        api.change_coin_balance(trade_info['to_id'], trade_info['coin_amount'], 'plus', trade_info['coin'])
        api.change_trade_state(trade_id, 'success')

        api.change_trade_amount(trade_info['to_id'], trade_info['usdt_amount'])
        api.change_trade_count(trade_info['to_id'])

        await call.message.answer('Сделка совершена!')
    else:
        await call.message.answer('Ошибка!')

    await call.answer()


@dp.callback_query_handler(cb2.filter(action=['cancel_order']), state='*')
async def cancel_order(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    trade_id = callback_data['id']
    trade_info = api.get_trade_info(trade_id)

    if trade_info['state'] == 'created':
        trade_id = callback_data['id']
        api.change_trade_state(trade_id, 'cancel')
        await call.message.answer('Сделка отменена!')

    elif trade_info['state'] == 'success':
        await call.message.answer('Сделка уже совершена!')

    else:
        await call.message.answer('Сделка уже отменена!')

    await call.answer()


@dp.callback_query_handler(cb2.filter(action=['cancel_order_from_adm']), state='*')
async def cancel_order(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    trade_id = callback_data['id']
    trade_info = api.get_trade_info(trade_id)

    if trade_info['state'] == 'created':
        trade_id = callback_data['id']
        api.change_trade_state(trade_id, 'cancel')
        await call.message.answer('Сделка отменена!')
        await dp.bot.send_message(str(trade_info['to_id']), f'<b>❗ Клиент отменил сделку </b>' + '\n\n'
                                  + '<b>Сумма: </b>' + str(trade_info['usdt_amount']) +
                                  ' USDT', parse_mode=types.ParseMode.HTML)
    elif trade_info['state'] == 'success':
        await call.message.answer('Сделка уже совершена!')

    else:
        await call.message.answer('Сделка уже отменена!')

    await call.answer()