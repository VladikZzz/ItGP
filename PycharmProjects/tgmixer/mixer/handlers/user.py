import operator
from datetime import datetime

import aiogram
from aiogram import types
from aiogram.types import \
    ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
import api
import config
from loader import dp, bot
from utils import States
from aiogram.dispatcher import FSMContext

my_info = KeyboardButton('💼 Кошелёк')
ads = KeyboardButton('🔄 Обмен')
save_dep = KeyboardButton('💰 Депозит')
about_us = KeyboardButton('📚 Информация')
web = KeyboardButton('🌐 Веб-версия')
app = KeyboardButton('📱 Приложение')

user_kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(my_info,
                                                                     ads,
                                                                     save_dep,
                                                                     about_us,
                                                                     web,
                                                                     app
                                                                     )

cb2 = CallbackData("post", "id", "action")


@dp.message_handler(state='*',
                    text='💼 Кошелёк')
async def my_account(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)
    await state.set_state(States.USER_STATE[0])
    try:
        u = api.get_user_info(msg.from_user.id)
        if u['state'] != 'banned':
            lim = str(u['limit'])
            c_lim = str(u['current_limit'])
            USDT_balance = str(u['USDT_balance'])
            TRX_balance = str(u['TRX_balance'])
            XLM_balance = str(u['XLM_balance'])
            ADA_balance = str(u['ADA_balance'])
            DOGE_balance = str(u['DOGE_balance'])
            MATIC_balance = str(u['MATIC_balance'])
            LUNA_balance = str(u['LUNA_balance'])
            DOT_balance = str(u['DOT_balance'])
            AVAX_balance = str(u['AVAX_balance'])
            name = u['username']
            button1 = types.InlineKeyboardButton(text='⬆ Ввод', callback_data='in')
            button2 = types.InlineKeyboardButton(text='⬇ Вывод', callback_data='out')
            buttons_ = [button1, button2]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons_)
            code = 'REF'+str(int(u['tg_id']) // 5 + 123)

            m = '<b>💵 Баланс:\n\n</b><b>USDT: </b>' + USDT_balance + '\n' + '<b>TRX: </b>' + TRX_balance  + '\n<b>XLM: </b>' + XLM_balance+ '\n<b>ADA: </b>' + ADA_balance + '\n<b>DOGE: </b>' + DOGE_balance+ '\n<b>MATIC: </b>' + MATIC_balance + '\n<b>LUNA: </b>' + LUNA_balance + '\n<b>DOT: </b>' + DOT_balance + '\n<b>AVAX: </b>' + AVAX_balance + '\n\n' + '<b>📌 Лимиты:\n\n</b><b>Недельный лимит: </b>' + lim + '\n' + '<b>Оставшийся лимит на неделю: </b>' + c_lim + '\n\n '
            if float(lim) < 10001:
                await msg.answer(f"<b>🙎🏼‍♂ {name} Bronze 🥉</b>\n\n" + m, parse_mode=types.ParseMode.HTML,
                                 reply_markup=keyboard)
            elif 10000 < float(lim) < 25001:
                await msg.answer(f"<b>🙎🏼‍♂ {name} Silver 🥈</b>\n\n" + m, parse_mode=types.ParseMode.HTML,
                                 reply_markup=keyboard)
            elif 25000 < float(lim) < 50001:
                await msg.answer(f"<b>🙎🏼‍♂ {name} Gold 🥉</b>\n\n" + m, parse_mode=types.ParseMode.HTML,
                                 reply_markup=keyboard)
            elif float(lim) > 50000:
                await msg.answer(f"<b>🙎🏼‍♂ {name} Diamond 💎</b>\n\n" + m, parse_mode=types.ParseMode.HTML,
                                 reply_markup=keyboard)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await msg.answer(f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                                      parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await msg.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)


@dp.message_handler(state='*',
                    text='🔄 Обмен')
async def ads(msg: types.Message):
    u = api.get_user_info(msg.from_user.id)
    #if u == {'message': 'The user does not exist'}:
    try:
        if u['state'] != 'banned':
            ads = api.get_ads()
            buttons = []
            for ad in ads:
                owner_info = api.get_user_info(ad['owner_id'])
                api.change_ad_amount(ad['id'], owner_info['USDT_balance'])

            ads = api.get_ads()
            for ad in ads:
                if ad['max_amount'] < ad['min_amount']:
                    api.change_ad_state(ad['id'], False)

                if ad['max_amount'] >= ad['min_amount'] and ad['state'] == False:
                    api.change_ad_state(ad['id'], True)

            ads = api.get_ads()
            fake_ads = api.get_fake_ads()
            if (len(ads) + len(fake_ads)) % 10 == 0:
                k = (len(ads) + len(fake_ads)) // 10
            else:
                k = (len(ads) + len(fake_ads)) // 10 + 1

            all_ads = ads + fake_ads
            all_ads.sort(key=operator.itemgetter('max_amount'))
            all_ads.reverse()

            lst = all_ads[slice(0, 10)]

            for ad in lst:
                if ad in ads:
                    owner_info = api.get_user_info(ad['owner_id'])

                    if ad['state'] and owner_info['state'] == 'working':
                        button = types.InlineKeyboardButton(text='🍋' + owner_info['username'] + ' (' + str(ad['min_amount']) + ' - ' + str(ad['max_amount']) + ') USDT',
                                                            callback_data=cb2.new(id=str(ad['id']), action="user_ad"))

                        buttons.append(button)

                elif ad in fake_ads:
                    button = types.InlineKeyboardButton(
                        text='🍋' + ad['owner_name'] + ' (' + str(ad['min_amount']) + ' - ' + str(ad['max_amount']) + ') USDT',
                        callback_data=cb2.new(id=str(ad['id']), action="fake_ad"))
                    buttons.append(button)

            button1 = types.InlineKeyboardButton(text='📋 Моё объявление',
                                                callback_data='my_add')
            button2 = types.InlineKeyboardButton(text='📝 Открытые сделки',
                                                 callback_data='my_trades')

            prev = types.InlineKeyboardButton(text='◀ ' + str(k) + '/' + str(k), callback_data=cb2.new(id=k, action="prev"))
            if k == 0:
                next = types.InlineKeyboardButton(text=str(0) + '/' + str(k) + ' ▶', callback_data=cb2.new(id=0, action="next"))
            elif k < 2:
                next = types.InlineKeyboardButton(text=str(1) + '/' + str(k) + ' ▶', callback_data=cb2.new(id=2, action="next"))
            else:
                next = types.InlineKeyboardButton(text=str(2) + '/' + str(k) + ' ▶', callback_data=cb2.new(id=1, action="next"))
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)

            keyboard.row(prev, next)
            keyboard.row(button1, button2)
            mes = f'<b>🗓 Доска объявлений</b>\n\nЭто список из {len(all_ads)} заявок для обмена <b>TRX</b>, <b>SOL</b>, <b>AVAX</b>, <b>XRP</b>, ' \
                  f'<b>DOGE</b>, <b>DOT</b>, <b>LUNA</b>, <b>MATIC</b> на <b>USDT</b>.\n\n'
            await msg.answer(mes, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
            u_ad = api.get_user_ads(msg.from_user.id)

            if len(u_ad)!= 0 and api.get_user_info(msg.from_user.id)['USDT_balance'] < u_ad[0]['min_amount']:
                await msg.answer('<b>Объявления скрыты ...\n</b>Недостаточный баланс, минимальная сумма Вашего объявления ' + str(u_ad[0]['min_amount']) + ' USDT.', parse_mode=types.ParseMode.HTML)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await msg.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await msg.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)


@dp.message_handler(state='*',
                    text='💰 Депозит')
async def save_dep(msg: types.Message):
    u = api.get_user_info(msg.from_user.id)
    try:
        if u['state'] != 'banned':
            button1 = types.InlineKeyboardButton(text='⬆ Внести депозит', callback_data='dep_in')
            button2 = types.InlineKeyboardButton(text='⬇ Забрать депозит', callback_data='dep_out')
            buttons_ = [button1, button2]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons_)
            await msg.answer('💰 <b>Депозит</b>', reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await msg.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await msg.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)


@dp.message_handler(state='*',
                    text='📚 Информация')
async def about(msg: types.Message):
    u = api.get_user_info(msg.from_user.id)
    try:
        if u['state'] != 'banned':
            button1 = types.InlineKeyboardButton(text='📖 О нас', callback_data='about_us')
            button2 = types.InlineKeyboardButton(text='☎ Поддержка', callback_data='support')
            button3 = types.InlineKeyboardButton(text='📍 Комиссии', callback_data='comission')
            button4 = types.InlineKeyboardButton(text='📄 Условия', callback_data='conditions')
            button5 = types.InlineKeyboardButton(text='💸 Реферальная программа', callback_data='refs')
            button6 = types.InlineKeyboardButton(text='🤝 Партнёры', callback_data='partners')

            buttons_ = [button1, button2, button3, button4, button5, button6]

            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons_)

            await msg.answer('📚 Информация', reply_markup=keyboard)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await msg.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await msg.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)


@dp.message_handler(state='*',
                    text='🌐 Веб-версия')
async def site(msg: types.Message):
    u = api.get_user_info(msg.from_user.id)
    try:
        if u['state'] != 'banned':
            """button1 = types.InlineKeyboardButton(text='Перейти', url='https://google.com')
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)
            await msg.answer('🌐 Веб-версия', reply_markup=keyboard)"""
            await msg.answer('🌐 Веб-версия\n\n<b>Сайт в разработке</b>\n🎉 Скоро запустится Web-версия и работать с нами станет ещё удобнее!', parse_mode=types.ParseMode.HTML)

        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await msg.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await msg.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)


@dp.message_handler(state='*',
                    text='📱 Приложение')
async def about(msg: types.Message):
    u = api.get_user_info(msg.from_user.id)
    try:
        if u['state'] != 'banned':
            await msg.answer('<b>🛠 Приложение в разработке</b>\n\n🎉 Скоро запустится мобильное приложение для IOS/Android и '
                             'работать с нами станет ещё удобнее!', parse_mode=types.ParseMode.HTML)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await msg.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await msg.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(cb2.filter(action=["next"]), state='*')
async def next_page(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            ads = api.get_ads()
            buttons = []
            for ad in ads:
                owner_info = api.get_user_info(ad['owner_id'])
                api.change_ad_amount(ad['id'], owner_info['USDT_balance'])

            ads = api.get_ads()
            for ad in ads:
                if ad['max_amount'] < ad['min_amount']:
                    api.change_ad_state(ad['id'], False)

                if ad['max_amount'] >= ad['min_amount'] and ad['state'] == False:
                    api.change_ad_state(ad['id'], True)

            k = int(callback_data['id'])
            start = 10 * (k - 1)
            stop = 10 * k

            ads = api.get_ads()
            fake_ads = api.get_fake_ads()

            if (len(ads) + len(fake_ads)) % 10 == 0:
                max_k = (len(ads) + len(fake_ads)) // 10
            else:
                max_k = (len(ads) + len(fake_ads)) // 10 + 1

            all_ads = ads + fake_ads
            all_ads.sort(key=operator.itemgetter('max_amount'))
            all_ads.reverse()

            lst = all_ads[slice(start, stop)]

            for ad in lst:
                if ad in ads:
                    owner_info = api.get_user_info(ad['owner_id'])

                    if ad['state'] and owner_info['state'] == 'working':
                        button = types.InlineKeyboardButton(
                            text='🍋' + owner_info['username'] + ' (' + str(ad['min_amount']) + ' - ' + str(ad['max_amount']) + ') USDT',
                            callback_data=cb2.new(id=str(ad['id']), action="user_ad"))

                        buttons.append(button)
                elif ad in fake_ads:
                    button = types.InlineKeyboardButton(
                        text='🍋' + ad['owner_name'] + ' (' + str(ad['min_amount']) + ' - ' + str(ad['max_amount']) + ') USDT',
                        callback_data=cb2.new(id=str(ad['id']), action="fake_ad"))
                    buttons.append(button)

            button1 = types.InlineKeyboardButton(text='📋 Моё объявление',
                                                 callback_data='my_add')
            button2 = types.InlineKeyboardButton(text='📝 Открытые сделки',
                                                 callback_data='my_trades')
            if k == 0:
                prev = types.InlineKeyboardButton(text='◀ ' + str(k) + '/' + str(k),
                                                  callback_data=cb2.new(id=k, action="prev"))
                next = types.InlineKeyboardButton(text=str(0) + '/' + str(k) + ' ▶',
                                                      callback_data=cb2.new(id=0, action="next"))
            elif k + 1 > max_k:
                if k - 1 == 0:
                    prev = types.InlineKeyboardButton(text='◀ ' + str(max_k) + '/' + str(max_k), callback_data=cb2.new(id=max_k, action="prev"))
                else:
                    prev = types.InlineKeyboardButton(text='◀ ' + str(k - 1) + '/' + str(max_k), callback_data=cb2.new(id=max_k, action="prev"))
                next = types.InlineKeyboardButton(text=str(1) + '/' + str(max_k) + ' ▶', callback_data=cb2.new(id=1, action="next"))

            else:
                if k - 1 == 0:
                    prev = types.InlineKeyboardButton(text='◀ ' + str(max_k) + '/' + str(max_k), callback_data=cb2.new(id=k - 1, action="prev"))
                else:
                    prev = types.InlineKeyboardButton(text='◀ ' + str(k - 1) + '/' + str(max_k), callback_data=cb2.new(id=k - 1, action="prev"))

                next = types.InlineKeyboardButton(text=str(k + 1) + '/' + str(max_k) + ' ▶', callback_data=cb2.new(id=k + 1, action="next"))

            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            keyboard.row(prev, next)
            keyboard.row(button1, button2)
            try:
                await call.message.edit_reply_markup(keyboard)
            except aiogram.utils.exceptions.MessageNotModified:
                await call.answer()
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(cb2.filter(action=["prev"]), state='*')
async def prev_page(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            ads = api.get_ads()
            buttons = []
            for ad in ads:
                owner_info = api.get_user_info(ad['owner_id'])
                api.change_ad_amount(ad['id'], owner_info['USDT_balance'])

            ads = api.get_ads()
            for ad in ads:
                if ad['max_amount'] < ad['min_amount']:
                    api.change_ad_state(ad['id'], False)

                if ad['max_amount'] >= ad['min_amount'] and ad['state'] == False:
                    api.change_ad_state(ad['id'], True)

            k = int(callback_data['id'])
            start = 10 * (k - 1)
            stop = 10 * k

            ads = api.get_ads()
            fake_ads = api.get_fake_ads()

            if (len(ads) + len(fake_ads)) % 10 == 0:
                max_k = (len(ads) + len(fake_ads)) // 10
            else:
                max_k = (len(ads) + len(fake_ads)) // 10 + 1

            all_ads = ads + fake_ads
            all_ads.sort(key=operator.itemgetter('max_amount'))
            all_ads.reverse()

            lst = all_ads[slice(start, stop)]

            for ad in lst:
                if ad in ads:
                    owner_info = api.get_user_info(ad['owner_id'])

                    if ad['state'] and owner_info['state'] == 'working':
                        button = types.InlineKeyboardButton(
                            text='🍋' + owner_info['username'] + ' (' + str(ad['min_amount']) + ' - ' + str(ad['max_amount']) + ') USDT',
                            callback_data=cb2.new(id=str(ad['id']), action="user_ad"))

                        buttons.append(button)
                elif ad in fake_ads:
                    button = types.InlineKeyboardButton(
                        text='🍋' + ad['owner_name'] + ' (' + str(ad['min_amount']) + ' - ' + str(ad['max_amount']) + ') USDT',
                        callback_data=cb2.new(id=str(ad['id']), action="fake_ad"))
                    buttons.append(button)

            button1 = types.InlineKeyboardButton(text='📋 Моё объявление',
                                                 callback_data='my_add')
            button2 = types.InlineKeyboardButton(text='📝 Открытые сделки',
                                                 callback_data='my_trades')

            if k == 0:
                prev = types.InlineKeyboardButton(text='◀ ' + str(k) + '/' + str(k),
                                                  callback_data=cb2.new(id=k, action="prev"))
                next = types.InlineKeyboardButton(text=str(0) + '/' + str(k) + ' ▶',
                                                      callback_data=cb2.new(id=0, action="next"))

            elif k + 1 > max_k:
                if k - 1 == 0:
                    prev = types.InlineKeyboardButton(text='◀ ' + str(max_k) + '/' + str(max_k), callback_data=cb2.new(id=max_k, action="prev"))
                else:
                    prev = types.InlineKeyboardButton(text='◀ ' + str(k - 1) + '/' + str(max_k), callback_data=cb2.new(id=k - 1, action="prev"))
                next = types.InlineKeyboardButton(text=str(1) + '/' + str(max_k) + ' ▶', callback_data=cb2.new(id=1, action="next"))

            else:
                if k - 1 == 0:
                    prev = types.InlineKeyboardButton(text='◀ ' + str(max_k) + '/' + str(max_k), callback_data=cb2.new(id=max_k, action="prev"))
                else:
                    prev = types.InlineKeyboardButton(text='◀ ' + str(k - 1) + '/' + str(max_k), callback_data=cb2.new(id=k - 1, action="prev"))

                next = types.InlineKeyboardButton(text=str(k + 1) + '/' + str(max_k) + ' ▶', callback_data=cb2.new(id=k + 1, action="next"))

            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons)
            keyboard.row(prev, next)
            keyboard.row(button1, button2)
            try:
                await call.message.edit_reply_markup(keyboard)

            except aiogram.utils.exceptions.MessageNotModified:
                await call.answer()

        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(state=States.USER_STATE | States.TYPE_AMOUNT | States.CHOOSE_COIN | States.LINK, text='my_add')
async def my_add(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            u_ad = api.get_user_ads(call.from_user.id)
            u_info = api.get_user_info(call.from_user.id)
            name = u_info['username']
            button = types.InlineKeyboardButton(text='🔹 Добавить объявление',
                                                callback_data='create_ad')

            button2 = types.InlineKeyboardButton(text='🔹 Удалить объявление',
                                                 callback_data='delete_ad')

            button3 = types.InlineKeyboardButton(text='🔹 Изменить минимальный лимит',
                                                 callback_data='edit_min')
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.row(button, button2)
            keyboard.add(button3)

            if len(u_ad) != 0:
                min_lim = u_ad[0]['min_amount']
                max_lim = u_ad[0]['max_amount']
                if u_info['state'] == 'no_deposit':
                    mes = f'<b>📋 Моё объявление\n\n</b><b>👨🏼‍💼 Пользователь:</b> {name}\n\n<b>▪ Минимальный лимит: </b>{min_lim} USDT' \
                          f'\n<b>▪ Резерв: </b>{max_lim} USDT\n\n🔴 Отключено\n<i>Отсутствует страховочный депозит на аккаунте</i>'
                else:
                    mes = f'<b>📋 Моё объявление\n\n</b><b>👨🏼‍💼 Пользователь:</b> {name}\n\n<b>▪ Минимальный лимит: </b>{min_lim} USDT' \
                          f'\n<b>▪ Резерв: </b>{max_lim} USDT\n\n🟢 Активно'

                await call.message.answer(mes, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
            else:
                mes = '<b>🙌 У Вас еще нет объявления, самое время его разместить.\n</b>'
                await call.message.answer(mes, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(state=States.USER_STATE | States.TYPE_AMOUNT | States.CHOOSE_COIN | States.LINK, text='my_trades')
async def my_trades(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            trades = api.get_user_trades(call.from_user.id)
            if len(trades) == 0:
                await call.message.answer('⌛ У Вас нет открытых сделок')
            for trade in trades:
                button = types.InlineKeyboardButton(text='Принять',
                                                    callback_data=cb2.new(id=str(trade['id']), action="take_order"))
                button2 = types.InlineKeyboardButton(text='Отклонить',
                                                     callback_data=cb2.new(id=str(trade['id']), action="cancel_order"))

                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.row(button, button2)

                await call.message.answer( f'<b>🔥 Новая сделка! </b>' + '\n\n'
                                          + '<b>С вашего будет списано: </b>' + str(trade['usdt_amount']) +
                                          ' USDT' + '\n' + '<b>На ваш аккаунт будет начислено: </b>' + str(trade['coin_amount']) +
                                          ' ' + str(trade['coin']) + '\n\n⚠️<b>Внимание</b> ⚠️\n\nИгнорирование сделки может привести к применению штрафных санкций!\n<i>Процент прибыльности считается по курсу USDT/' + str(
                    trade['coin']) + ' биржи Bittrex</i>',
                                          parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(state=States.USER_STATE | States.TYPE_AMOUNT | States.CHOOSE_COIN | States.LINK, text='about_us')
async def about_us(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':

            await call.message.answer('👋 <b>О сервисе</b>\n\n🦅 <b>Эскроу агент</b> - связывающий покупателя и продавца различных онлайн сервисов, '
                                      'использующих криптовалютные операции, оставляя их анонимными.\n\n<b>▫ Гарантия '
                                      'проведения сделки\n▫ Анонимность транзакций\n▫ Отсутствие верификации\n▫ '
                                      'Моментальный ввод/вывод</b>', parse_mode=types.ParseMode.HTML)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(state=States.USER_STATE | States.TYPE_AMOUNT | States.CHOOSE_COIN | States.LINK,
                           text='support')
async def support(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':

            button1 = types.InlineKeyboardButton(text='☎ Поддержка', url='https://t.me/'+config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)
            await call.message.answer('📝 Если у Вас возникли какие-либо трудности или вопрос, Вы всегда можете обратиться в '
                                      'нашу службу поддержки!\n\n<b>Просим Вас соблюдать несколько простых условий:</b>\n\n▫ Четко '
                                      'формулируйте вопрос в одном сообщении, при необходимости прикладывайте скриншот\n▫ Не '
                                      'дублируйте свои сообщения, вам обязательно ответят, как только дойдет до Вас очередь',
                                      reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(state=States.USER_STATE | States.TYPE_AMOUNT | States.CHOOSE_COIN | States.LINK,
                           text='comission')
async def comission(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            await call.message.answer('💰 Комиссии за совершение операций вывода:\n\n▫ <b>За вывод</b> '
                                      f'USDT - {config.USDT_COMS}\n▫ <b>За вывод</b> TRX - {config.TRX_COMS}\n'
                                      f'▫ <b>За вывод</b> XLM - {config.XLM_COMS}\n'
                                      f'▫ <b>За вывод</b> DOT - {config.DOT_COMS}\n'
                                      f'▫ <b>За вывод</b> DOGE - {config.DOGE_COMS}\n'
                                      f'▫ <b>За вывод</b> LUNA - {config.LUNA_COMS}\n'
                                      f'▫ <b>За вывод</b> ADA - {config.ADA_COMS}\n'
                                      f'▫ <b>За вывод</b> MATIC - {config.MATIC_COMS}\n'
                                      f'▫ <b>За вывод</b> AVAX - {config.AVAX_COMS}\n\n🎉 <b>За ввод</b> криптовалюты, '
                                      'совершение обмена и вывод депозита комиссия не взимается', parse_mode=types.ParseMode.HTML)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(state=States.USER_STATE | States.TYPE_AMOUNT | States.CHOOSE_COIN | States.LINK,
                           text='conditions')
async def conditions(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            await call.message.answer('📍 <b>Для комфортного использования сервиса просим вас соблюдать ряд простых '
                                      'условий:</b>\n\n▪ Совершать переводы криптовалюты строго по зарегистрированным адресам на '
                                      'платформе\n▪ Быстро реагировать на новые сделки\n▪ Не использовать более одного '
                                      'аккаунта на платформе\n\n❗ Регистрируясь на платформе Вы автоматически соглашаетесь с условиями '
                                      'работы.', parse_mode=types.ParseMode.HTML)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(state=States.USER_STATE | States.TYPE_AMOUNT | States.CHOOSE_COIN | States.LINK,
                           text='refs')
async def refs(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            code = 'REF'+str(int(u['tg_id']) // 5 + 123)
            await call.message.answer(f'💸 <b>Реферальная программа</b>\n\n🎉 Приглашай друзей стать мерчантом по реферальному коду и получай единоразовое вознаграждение 30 USDT после совершения первой сделки!\n\n<b>Реферальный код: </b><b>{code}</b>', parse_mode=types.ParseMode.HTML)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(state=States.USER_STATE | States.TYPE_AMOUNT | States.CHOOSE_COIN | States.LINK,
                           text='partners')
async def partners(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            await call.message.answer('🤝 <b>Нам доверяют 50+ партнёров по всему миру!</b>\n\n<b>Сторонние '
                                      'сервисы:</b>\n\n<i>▫️Bitcasino\n▫️BitStarz\n▫️Cloudbet\n▫️Fairspin '
                                      'Casino\n▫️FontuneJack</i>', parse_mode=types.ParseMode.HTML)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(state=States.USER_STATE | States.TYPE_AMOUNT | States.CHOOSE_COIN | States.LINK, text='in')
async def in_(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            state = dp.current_state(user=call.from_user.id)
            await state.set_state(States.USER_STATE[0])

            button1 = types.InlineKeyboardButton(text='⏳ Открытые заявки', callback_data='open_dep_orders')
            button2 = types.InlineKeyboardButton(text='⚒ Создать заявку', callback_data='make_dep_order')
            buttons_ = [button2, button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                '⬆ <b>Внести USDT</b> \n\nДля пополнения USDT с внешнего кошелька создайте новую заявку.\n\n ⚠ '
                '<b>Внимание</b> ⚠️\n\n▫ Совершайте платежи только по указанным реквизитам.\n'
                '▫ В противном случае вы рискуете потерять свои средства\n\nСредства поступят на ваш баланс после '
                'подтверждения ввода платформой.',
                reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()



@dp.callback_query_handler(state=States.USER_STATE | States.TYPE_AMOUNT | States.CHOOSE_COIN | States.LINK, text='out')
async def out(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            button1 = types.InlineKeyboardButton(text='⏳ Открытые заявки', callback_data='open_out_orders')
            button2 = types.InlineKeyboardButton(text='⚒ Создать заявку', callback_data='make_out_order')
            buttons_ = [button2, button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)
            m = 'Выберите криптовалюту, которую вы хотите вывести с аккаунта.\n\n<b>⚠ Внимание ⚠</b>\n' \
                f'кошельки, указанные при регистрации.\n\nПлатформа взимает комиссию за вывод:\n▫ <b>USDT</b> - {config.USDT_COMS}\n▫ ' \
                f'<b>TRX</b> - {config.TRX_COMS}' \
                f'\n▫ <b>XLM</b> - {config.XLM_COMS}' \
                f'\n▫ <b>DOGE</b> - {config.DOGE_COMS}' \
                f'\n▫ <b>DOT</b> - {config.DOT_COMS}' \
                f'\n▫ <b>ADA</b> - {config.ADA_COMS}' \
                f'\n▫ <b>LUNA</b> - {config.LUNA_COMS}' \
                f'\n▫ <b>MATIC</b> - {config.MATIC_COMS}' \
                f'\n▫ <b>AVAX</b> - {config.AVAX_COMS}\n\n💡Учитывайте эту информацию при совершении операций! '

            await call.message.answer('<b>⬇ Вывести монеты</b>\n\n' + m, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(state=States.USER_STATE | States.TYPE_AMOUNT | States.CHOOSE_COIN, text='dep_in')
async def dep_in(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            u_info = api.get_user_info(call.from_user.id)
            coin_info = api.get_coin_info('USDT')
            network = coin_info['network_type']
            address = coin_info['address']

            if u_info['state'] == 'working':
                await call.message.answer('🤝 Вы уже внесли депозит. Хорошей торговли!')
            elif u_info['state'] == 'no_deposit':
                mes = f'<b>Ввод депозита</b>\n\n<b>Отправьте {config.DEPOSIT} USDT</b>' + '\n<b>Совершайте перевод строго с вашего адреса: </b>' + \
                      u_info['address_USDT'] + \
                      '\n' + '<b>Адрес для перевода: </b>' + address + \
                      '\n\n' + '<b>⚠️Внимание ⚠️</b>\n\n<b>Совершайте перевод строго по сети </b>' + network + '\nУбедитесь, что адреса и сети соответствуют требованиям, чтобы избежать потери средств!\n\nПри совершении платежа учитывайте комиссию сети TRC-20.'


                order_id = len(api.get_user_orders(call.from_user.id)) + call.from_user.id
                api.add_order(order_id, 'created', call.from_user.id, config.DEPOSIT, 'USDT', u_info['address_USDT'], coin_info['address'],
                              'save_deposit')

                buttons = [
                    types.InlineKeyboardButton(text="✅ Оплачено", callback_data=cb2.new(id=str(order_id), action="paid_dep")),
                    types.InlineKeyboardButton(text="❌ Отменить",
                                               callback_data=cb2.new(id=str(order_id), action="cancel_in"))
                ]

                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(*buttons)

                await call.message.answer(mes, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                state = dp.current_state(user=call.from_user.id)
                await state.set_state(States.USER_STATE[0])
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(state=States.USER_STATE | States.TYPE_AMOUNT | States.CHOOSE_COIN, text='dep_out')
async def dep_out(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            u_info = api.get_user_info(call.from_user.id)
            if u_info['state'] == 'no_deposit':
                await call.message.answer('<b>Упсс...</b>\nУ вас отсутствует депозит на аккаунте', parse_mode=types.ParseMode.HTML)
            else:
                button1 = types.InlineKeyboardButton(text='Да', callback_data='dep_out_yes')
                button2 = types.InlineKeyboardButton(text='Нет', callback_data='dep_out_no')
                buttons_ = [button1, button2]
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(*buttons_)
                await call.message.answer('<b>Вывод депозита</b>\n\nВы уверены, что хотите забрать свой депозит?\nБез депозита '
                                          'ваши объявления будут недоступны другим пользователям.\n\n<b>⚠ Внимание '
                                          '⚠</b>\n\nВозврат депозита осуществляется в полном объёме в течение 15 дней, после проверки вашей '
                                          'активности на платформе.', reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(state=States.USER_STATE | States.TYPE_AMOUNT | States.CHOOSE_COIN, text='dep_out_yes')
async def dep_out_yes(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            order_id = len(api.get_user_orders(call.from_user.id)) + call.from_user.id
            u_info = api.get_user_info(call.from_user.id)
            if u_info['state'] == 'working':
                api.add_order(order_id, 'created', call.from_user.id, float(config.DEPOSIT), 'USDT', 'undefined',
                              u_info['address_USDT'], 'save_deposit_out')

                await call.message.answer('✅ Заявка на возврат депозита оформлена.')
                api.change_user_state(u_info['tg_id'], 'no_deposit')
                take = types.InlineKeyboardButton(text="⚒ Взять в обработку",
                                                  callback_data=cb2.new(id=str(order_id), action="take_order_process"))
                buttons = [take,
                    types.InlineKeyboardButton(text="Выплачено",
                                               callback_data=cb2.new(id=str(order_id), action="confirm_withdraw_coins"))
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(*buttons)
                adm = api.get_admins()
                for a in adm:
                    await dp.bot.send_message(str(a), f'<b>Возврат депозита от </b>' + u_info['username'] + \
                                              '\n\n<b>Сумма:</b>' + str(config.DEPOSIT) + 'USDT\n\n' + \
                                              '<b>Адрес для пополнения: </b>' + u_info['address_USDT'],
                                              parse_mode=types.ParseMode.HTML,
                                              reply_markup=keyboard)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(state=States.USER_STATE | States.TYPE_AMOUNT | States.CHOOSE_COIN, text='dep_out_no')
async def dep_out_no(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            u_info = api.get_user_info(call.from_user.id)
            if u_info['state'] == 'no_deposit':
                await call.message.answer('Ошибка')
                await call.answer()
            else:
                await call.message.answer('✅')
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(state=States.USER_STATE | States.TYPE_AMOUNT | States.CHOOSE_COIN, text='make_dep_order')
async def USDT_TRC_20(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            state = dp.current_state(user=call.from_user.id)
            await state.set_state(States.USER_STATE[0])

            u_info = api.get_user_info(call.from_user.id)
            u_orders = api.get_user_orders(call.from_user.id)
            flag = False
            for o in u_orders:
                if o['type'] == 'deposit' and o['status'] == 'created':
                    flag = True
                    break

            if flag:
                await call.answer('У вас есть незакрытые заявки на ввод.')
            else:
                await call.message.answer('<b>Укажите количество USDT для пополнения (только число)</b>\n\n<b>Минимальная '
                                          'сумма: '
                                          '</b>' + str(
                    config.MIN_AMOUNT) + ' USDT' + '\n<b>Максимальная сумма:</b> ' + str(u_info['current_limit']) + ' USDT', parse_mode=types.ParseMode.HTML)

                state = dp.current_state(user=call.from_user.id)
                await state.set_state(States.TYPE_AMOUNT[0])
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.message_handler(state=States.TYPE_AMOUNT)
async def type_amount(msg: types.Message):
    u_info = api.get_user_info(msg.from_user.id)
    try:
        if u_info['state'] != 'banned':
            global amount
            try:
                amount = float(msg.text)
                c_lim = u_info['current_limit']
                if amount > c_lim or amount < config.MIN_AMOUNT:
                    await msg.answer(
                        '<b>Некорректный ввод...</b>\n\n<b>Укажите количество USDT для пополнения (только '
                        'число)</b>\n\n<b>Минимальная сумма: </b>' + str(
                            config.MIN_AMOUNT) + ' USDT' + '\n<b>Максимальная сумма:</b> ' + str(
                            u_info['current_limit']) + ' USDT',
                        parse_mode=types.ParseMode.HTML)

                else:
                    coin_info = api.get_coin_info('USDT')
                    tiker_ = coin_info['tiker']
                    network = coin_info['network_type']
                    address = coin_info['address']
                    mes = '<b>Отправьте </b>' + str(
                        amount) + ' ' + tiker_ + '\n<b>Совершайте перевод строго с вашего адреса: </b>' + u_info[
                              'address_USDT'] + \
                          '\n' + '<b>Адрес для перевода: </b>' + address + \
                          '\n\n' + '<b>⚠Внимание⚠</b>\n\n<b>Совершайте перевод строго по сети </b>' + network + '\nУбедитесь, что адреса и сети соответствуют требованиям, чтобы избежать потери средств!\n\nПри совершении платежа учитывайте комиссию сети TRC-20.'

                    order_id = len(api.get_user_orders(msg.from_user.id)) + msg.from_user.id
                    api.add_order(order_id, 'created', msg.from_user.id, amount, 'USDT', u_info['address_USDT'], address,
                                  'deposit')

                    buttons = [
                        types.InlineKeyboardButton(text="✅ Оплачено",
                                                   callback_data=cb2.new(id=str(order_id), action="paid")),
                        types.InlineKeyboardButton(text="❌ Отменить",
                                                   callback_data=cb2.new(id=str(order_id), action="cancel_in"))

                    ]
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    keyboard.add(*buttons)

                    await msg.answer(mes, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                    state = dp.current_state(user=msg.from_user.id)
                    await state.set_state(States.USER_STATE[0])

            except ValueError:
                await msg.answer(
                    '<b>Некорректный ввод...</b>\n\n<b>Укажите количество USDT для пополнения (только '
                    'число)</b>\n\n<b>Минимальная сумма: </b>' + str(
                        config.MIN_AMOUNT) + ' USDT' + '\n<b>Максимальная сумма:</b> ' + str(
                        u_info['current_limit']) + ' USDT',
                    parse_mode=types.ParseMode.HTML)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await msg.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await msg.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)



@dp.callback_query_handler(cb2.filter(action=["paid"]), state='*')
async def paid(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            order_id = callback_data["id"]
            order = api.get_order_info(order_id)
            try:
                if order['status'] == 'created':
                    await call.message.answer('🔗 Прекрепите ссылку на транзакцию в обозревателе: ')

                    state = dp.current_state(user=call.from_user.id)
                    await state.set_state(States.LINK[0])
                    await call.answer()
                elif order['status'] == 'paid':
                    await call.message.answer('⏳ Ваша заявка уже оплачена, ожидайте поступления!')

                async with state.proxy() as data:
                    data['order_id'] = order_id
            except KeyError:
                await call.message.answer('Ошибка')
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(cb2.filter(action=["cancel_in"]), state='*')
async def cancel_in(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            try:
                order_id = callback_data["id"]
                order = api.get_order_info(order_id)
                if order['status'] != 'created':
                    await call.message.answer('Ошибка!')
                else:
                    api.delete_order(order_id)
                    await call.message.answer('✅ Ввод отменён')
                    await call.answer()
                    state = dp.current_state(user=call.from_user.id)
                    await state.set_state(States.USER_STATE[0])
            except KeyError:
                await call.message.answer('Ошибка!')
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)

    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(cb2.filter(action=["paid_dep"]), state='*')
async def paid_dep(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            order_id = callback_data["id"]
            order = api.get_order_info(order_id)

            if order['status'] == 'created':
                await call.message.answer('🔗 Прекрепите ссылку на транзакцию в обозревателе: ')

                state = dp.current_state(user=call.from_user.id)
                await state.set_state(States.LINK[0])
                await call.answer()
            elif order['status'] == 'paid':
                await call.message.answer('⏳ Ваша заявка уже оплаченна, ожидайте поступления!')

            async with state.proxy() as data:
                data['order_id'] = order_id
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.message_handler(state=States.LINK)
async def send_link(msg: types.Message, state: FSMContext):
    u = api.get_user_info(msg.from_user.id)
    try:
        if u['state'] != 'banned':
            async with state.proxy() as data:
                order_id = data['order_id']

            link = msg.text
            api.change_order_status(order_id, 'paid')
            u_info = api.get_user_info(msg.from_user.id)
            order = api.get_order_info(order_id)

            await msg.answer(
                '✅<b>Заявка в обработке</b>\nСредства поступят на ваш баланс после подтверждения модератором.',
                parse_mode=types.ParseMode.HTML)

            if order['type'] == 'save_deposit':
                take = types.InlineKeyboardButton(text="⚒ Взять в обработку",
                                                  callback_data=cb2.new(id=str(order_id), action="take_order_process"))
                cancel = types.InlineKeyboardButton(text="Отклонить",
                                                  callback_data=cb2.new(id=str(order_id), action="cancel_user_in"))

                buttons = [take,cancel,
                    types.InlineKeyboardButton(text="👍 Подтвердить",
                                               callback_data=cb2.new(id=str(order_id), action="confirm_save_dep"))
                ]
                keyboard = types.InlineKeyboardMarkup(row_width=3)
                keyboard.add(*buttons)
                api.set_order_link(order_id, link)
                adm = api.get_admins()
                for a in adm:
                    await dp.bot.send_message(str(a), f'<b>Внесение страховочного депозита от </b>' + u_info['username'] + \
                                              '\n\n<b>Сумма:</b>' + str(order['amount']) + 'USDT\n\n' + \
                                              '<b>Ссылка на обозреватель: </b>' + link, parse_mode=types.ParseMode.HTML,
                                              reply_markup=keyboard)
            else:
                api.change_current_limit(u_info['tg_id'], order['amount'])
                take = types.InlineKeyboardButton(text="⚒ Взять в обработку",
                                                  callback_data=cb2.new(id=str(order_id), action="take_order_process"))
                cancel = types.InlineKeyboardButton(text="Отклонить",
                                                    callback_data=cb2.new(id=str(order_id), action="cancel_user_in"))

                buttons = [take,cancel,
                    types.InlineKeyboardButton(text="👍 Подтвердить",
                                               callback_data=cb2.new(id=str(order_id), action="confirm_dep"))
                ]

                keyboard = types.InlineKeyboardMarkup(row_width=2)
                keyboard.add(*buttons)
                api.set_order_link(order_id, link)
                adm = api.get_admins()
                for a in adm:
                    await dp.bot.send_message(str(a), f'<b>Депозит монет от от </b>' + u_info['username'] + \
                                              '\n\n<b>Сумма:</b>' + str(order['amount']) + 'USDT\n\n' + \
                                              '<b>Ссылка на обозреватель: </b>' + link, parse_mode=types.ParseMode.HTML,
                                              reply_markup=keyboard)

            state = dp.current_state(user=msg.from_user.id)
            await state.set_state(States.USER_STATE[0])
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await msg.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await msg.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(state='*', text='open_dep_orders')
async def open_orders(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            my_orders = api.get_user_orders(call.from_user.id)
            for order in my_orders:
                if order['type'] == 'deposit':
                    if order['status'] == 'created':
                        coin_info = api.get_coin_info('USDT')
                        tiker_ = coin_info['tiker']
                        network = coin_info['network_type']
                        mes = '<b>Пополнение баланса</b>\n\n<b>Отправьте </b>' + str(order['amount']) + ' ' + tiker_ + '\n<b>Совершайте перевод строго с вашего адреса: </b>' + order['from_adr'] + \
                              '\n' + '<b>Адрес для перевода: </b>' + order['to_adr'] + \
                              '\n\n' + '<b>⚠Внимание⚠</b>\n\n<b>Совершайте перевод строго по сети </b>' + network + f'\nУбедитесь, что адреса и сети соответствуют требованиям, чтобы избежать потери средств!\n\nПри совершении платежа учитывайте комиссию сети {network}.'

                        buttons = [
                            types.InlineKeyboardButton(text="✅ Оплачено",
                                                       callback_data=cb2.new(id=str(order['id']), action="paid")),
                            types.InlineKeyboardButton(text="❌ Отменить",
                                                       callback_data=cb2.new(id=str(order['id']), action="cancel_in"))

                        ]
                        keyboard = types.InlineKeyboardMarkup(row_width=2)
                        keyboard.add(*buttons)

                        await call.message.answer(mes, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)


                    elif order['status'] == 'paid':
                        mes = '<b>Пополнение баланса</b>\n\n' + '<b>Сумма: </b>' + str(order['amount']) + ' ' + ' USDT' + '\n<b>Адрес отправителя: </b>' + order[
                            'from_adr'] + \
                              '\n' + '<b>Адрес получателя: </b>' + order['to_adr'] + '\n\n🕓 Ожидает подтверждения...'

                        await call.message.answer(mes, parse_mode=types.ParseMode.HTML)
                if order['type'] == 'save_deposit':
                    if order['status'] == 'created':
                        coin_info = api.get_coin_info('USDT')
                        tiker_ = coin_info['tiker']
                        network = coin_info['network_type']
                        mes = '<b>Ввод депозита</b>\n\n<b>Отправьте </b>' + str(order['amount']) + ' ' + tiker_ + '\n<b>Совершайте перевод строго с вашего адреса: </b>' + order['from_adr'] + \
                              '\n' + '<b>Адрес для перевода: </b>' + order['to_adr'] + \
                              '\n\n' + '<b>⚠Внимание⚠</b>\n\n<b>Совершайте перевод строго по сети </b>' + network + f'\nУбедитесь, что адреса и сети соответствуют требованиям, чтобы избежать потери средств!\n\nПри совершении платежа учитывайте комиссию сети {network}.'

                        buttons = [
                            types.InlineKeyboardButton(text="✅ Оплачено",
                                                       callback_data=cb2.new(id=str(order['id']), action="paid")),
                            types.InlineKeyboardButton(text="❌ Отменить",
                                                       callback_data=cb2.new(id=str(order['id']), action="cancel_in"))

                        ]
                        keyboard = types.InlineKeyboardMarkup(row_width=2)
                        keyboard.add(*buttons)

                        await call.message.answer(mes, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)


                    elif order['status'] == 'paid':
                        mes = '<b>Ввод депозита</b>\n\n' + '<b>Сумма: </b>' + str(order['amount']) + ' ' + ' USDT' + '\n<b>Адрес отправителя: </b>' + order[
                            'from_adr'] + \
                              '\n' + '<b>Адрес получателя: </b>' + order['to_adr'] + '\n\n🕓 Ожидает подтверждения...'

                        await call.message.answer(mes, parse_mode=types.ParseMode.HTML)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)


    await call.answer()


@dp.callback_query_handler(state='*', text='make_out_order')
async def make_withdraw(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            coins = api.get_coins()
            buttons_ = []
            for coin in coins:
                b = types.InlineKeyboardButton(text=str(coin['tiker']), callback_data=cb2.new(id=str(coin['tiker']), action="coin_out"))
                buttons_.append(b)

            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons_)

            await call.message.answer('Выберите монету на вывод: ', reply_markup=keyboard)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(cb2.filter(action=['coin_out']), state='*')
async def coin_out(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            tiker = callback_data['id']
            async with state.proxy() as data:
                data['tiker_for_out'] = tiker
            if tiker != 'USDT':
                network = api.get_coin_info(tiker)['network_type']
                await call.message.answer(f'<b>Пожалуйста, укажите адрес {tiker} в сети {network}</b>', parse_mode=types.ParseMode.HTML)
                state = dp.current_state(user=call.from_user.id)
                await state.set_state(States.COIN_ADDRESS[0])
            else:
                u_info = api.get_user_info(call.from_user.id)
                async with state.proxy() as data:
                    data['coin_addr'] = u_info['address_USDT']

                coin_balance = u_info[tiker + '_balance']
                min_amount = api.get_min_amount_for_out(tiker)
                coms = api.get_comission(tiker)

                if coin_balance < min_amount:
                    await call.message.answer(
                        f'<b>Недостаточный баланс {tiker}.</b> Минимальная сумма вывода {min_amount} {tiker}.',
                        parse_mode=types.ParseMode.HTML)
                else:
                    await call.message.answer(
                        f'<b>Укажите количество {tiker} для вывода (только число)</b>\n\n<b>Минимальная сумма: </b>{min_amount} {tiker}' + '\n<b>Доступнo:</b> ' + str(
                            coin_balance) + f' {tiker}' + f'\n<b>Комиссия: </b>{coms} {tiker}' + '\n<b>Максимально вы можете отправить: </b>' + str(
                            coin_balance - float(coms)) + f' {tiker}',
                        parse_mode=types.ParseMode.HTML)

                    state = dp.current_state(user=call.from_user.id)
                    await state.set_state(States.COIN_AMOUNT_OUT[0])
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.message_handler(state=States.COIN_ADDRESS)
async def coin_address(msg: types.Message, state: FSMContext):
    coin_addr = msg.text

    async with state.proxy() as data:
        tiker = data['tiker_for_out']

    async with state.proxy() as data:
        data['coin_addr'] = coin_addr

    u_info = api.get_user_info(msg.from_user.id)
    coin_balance = u_info[tiker + '_balance']
    min_amount = api.get_min_amount_for_out(tiker)
    coms =api.get_comission(tiker)

    if coin_balance < min_amount:
        await msg.answer(
            f'<b>Недостаточный баланс {tiker}.</b> Минимальная сумма вывода {min_amount} {tiker}.', parse_mode=types.ParseMode.HTML)
    else:
        await msg.answer(
            f'<b>Укажите количество {tiker} для вывода (только число)</b>\n\n<b>Минимальная сумма: </b>{min_amount} {tiker}' + '\n<b>Доступнo:</b> ' + str(
                coin_balance) + f' {tiker}' + f'\n<b>Комиссия: </b>{coms} {tiker}' + '\n<b>Максимально вы можете отправить: </b>' + str(
                coin_balance - float(coms)) + f' {tiker}',
            parse_mode=types.ParseMode.HTML)

        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(States.COIN_AMOUNT_OUT[0])



@dp.message_handler(state=States.COIN_AMOUNT_OUT)
async def withdraw_coins(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        tiker_for_out = data['tiker_for_out']
        coin_addr = data['coin_addr']

    coin_info = api.get_coin_info(tiker_for_out)
    order_id = len(api.get_user_orders(msg.from_user.id)) + msg.from_user.id
    u_info = api.get_user_info(msg.from_user.id)
    coin_balance = u_info[tiker_for_out + '_balance']
    coin_comission = api.get_comission(tiker_for_out)
    coin_min_amount = api.get_min_amount_for_out(tiker_for_out)

    try:
        coin_amount = float(msg.text)
        if float(coin_amount) > float(coin_balance) - coin_comission or float(coin_amount) < api.get_min_amount_for_out(tiker_for_out):
            await msg.answer(
                f'<b>Некорректный ввод...</b>\n\n<b>Минимальная сумма: </b>{coin_min_amount} {tiker_for_out}' + '\n<b>Доступнo:</b> ' + str(
                    coin_balance) + f' {tiker_for_out}' + f'\n<b>Комиссия: </b>{coin_comission} {tiker_for_out}' + '\n<b>Максимально вы можете отправить: </b>' + str(
                    coin_balance - coin_comission) + f' {tiker_for_out}',
                parse_mode=types.ParseMode.HTML)
            state = dp.current_state(user=msg.from_user.id)
            await state.set_state(States.COIN_AMOUNT_OUT[0])
        else:
            api.add_order(order_id, 'created', msg.from_user.id, float(coin_amount), tiker_for_out,
                          coin_info['address'],
                          coin_addr, 'withdraw')

            await msg.answer(f'✅ Заявка на вывод {tiker_for_out} сформирована. Ожидайте поступления.')
            api.change_coin_balance(msg.from_user.id, float(coin_amount) + coin_comission, 'minus', tiker_for_out)
            take = types.InlineKeyboardButton(text="⚒ Взять в обработку",
                                              callback_data=cb2.new(id=str(order_id), action="take_order_process"))

            buttons = [take,
                       types.InlineKeyboardButton(text="Выплачено",
                                                  callback_data=cb2.new(id=str(order_id),
                                                                        action="confirm_withdraw_coins"))
                       ]
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(*buttons)
            adm = api.get_admins()
            for a in adm:
                await dp.bot.send_message(str(a), f'<b>Вывод монет от от </b>' + u_info['username'] + \
                                          '\n\n<b>Сумма:</b>' + str(coin_amount) + f'{tiker_for_out}\n\n' + \
                                          '<b>Адрес для пополнения: </b>' + coin_addr, parse_mode=types.ParseMode.HTML,
                                          reply_markup=keyboard)

            state = dp.current_state(user=msg.from_user.id)
            await state.set_state(States.USER_STATE[0])

    except ValueError:
        await msg.answer(
            f'<b>Некорректный ввод...</b>\n\n<b>Минимальная сумма: </b>{coin_min_amount} {tiker_for_out}' + '\n<b>Доступнo:</b> ' + str(
                coin_balance) + f' {tiker_for_out}' + f'\n<b>Комиссия: </b>{coin_comission} {tiker_for_out}' + '\n<b>Максимально вы можете отправить: </b>' + str(
                coin_balance - coin_comission) + f' {tiker_for_out}',
            parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(state='*', text='open_out_orders')
async def open_withdraw_orders(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            my_orders = api.get_user_orders(call.from_user.id)
            for order in my_orders:
                if order['type'] == 'withdraw':
                    if order['status'] == 'created':
                        mes = '<b>Вывод с баланса</b>\n\n' + '<b>Сумма: </b>' + str(
                            order['amount']) + ' ' + order['cryptocurrency'] + '\n<b>Адрес получения: </b>' + order['to_adr'] + '\n\n🕓 В обработке...'


                        await call.message.answer(mes, parse_mode=types.ParseMode.HTML)


                    elif order['status'] == 'paid':
                        mes = '<b>Вывод с баланса</b>\n\n' + '<b>Сумма: </b>' + str(
                            order['amount']) + ' ' + order['cryptocurrency'] + '\n<b>Адрес получения: </b>' + order['to_adr'] + '\n\n💯 Оплачена\n\n<b>Подтвердите получение</b>'

                        buttons = [
                            types.InlineKeyboardButton(text="✅ Получено",
                                                       callback_data=cb2.new(id=str(order['id']), action="confirm")),
                            types.InlineKeyboardButton(text="❌ Не получено",
                                                       callback_data=cb2.new(id=str(order['id']), action="not_confirm"))
                        ]
                        keyboard = types.InlineKeyboardMarkup(row_width=2)
                        keyboard.add(*buttons)

                        await call.message.answer(mes, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                    elif order['status'] == 'dispute':
                        mes = '<b>Вывод с баланса</b>\n\n' + '<b>Сумма: </b>' + str(
                            order['amount']) + ' ' + order['cryptocurrency'] + '\n<b>Адрес получения: </b>' + order['to_adr'] + '\n\n💯 Оплачена\n\n<b>🧑🏼‍✈ Диспут</b>'
                        buttons = [
                            types.InlineKeyboardButton(text="✅ Диспут разрешён",
                                                       callback_data=cb2.new(id=str(order['id']), action="confirm")),
                                            ]
                        keyboard = types.InlineKeyboardMarkup(row_width=2)
                        keyboard.add(*buttons)
                        await call.message.answer(mes, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)

                if order['type'] == 'save_deposit_out':
                    if order['status'] == 'created':
                        mes = '<b>Вывод депозита</b>\n\n' + '<b>Сумма: </b>' + str(
                            order['amount']) + ' ' + order['cryptocurrency'] + '\n<b>Адрес получения: </b>' + order['to_adr'] + '\n\n🕓 В обработке...'


                        await call.message.answer(mes, parse_mode=types.ParseMode.HTML)


                    elif order['status'] == 'paid':
                        mes = '<b>Вывод депозита</b>\n\n' + '<b>Сумма: </b>' + str(
                            order['amount']) + ' ' + order['cryptocurrency'] + '\n<b>Адрес получения: </b>' + order['to_adr'] + '\n\n💯 Оплачена\n\n<b>Подтвердите получение</b>'

                        buttons = [
                            types.InlineKeyboardButton(text="✅ Получено",
                                                       callback_data=cb2.new(id=str(order['id']), action="confirm")),
                            types.InlineKeyboardButton(text="❌ Не получено",
                                                       callback_data=cb2.new(id=str(order['id']), action="not_confirm"))
                        ]
                        keyboard = types.InlineKeyboardMarkup(row_width=2)
                        keyboard.add(*buttons)

                        await call.message.answer(mes, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
                    elif order['status'] == 'dispute':
                        mes = '<b>Вывод депозита</b>\n\n' + '<b>Сумма: </b>' + str(
                            order['amount']) + ' ' + order['cryptocurrency'] + '\n<b>Адрес получения: </b>' + order['to_adr'] + '\n\n💯 Оплачена\n\n<b>🧑🏼‍✈ Диспут</b>'

                        buttons = [
                            types.InlineKeyboardButton(text="✅ Диспут разрешён",
                                                       callback_data=cb2.new(id=str(order['id']), action="confirm")),
                                            ]
                        keyboard = types.InlineKeyboardMarkup(row_width=2)
                        keyboard.add(*buttons)
                        await call.message.answer(mes, reply_markup=keyboard, parse_mode=types.ParseMode.HTML)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(cb2.filter(action=["confirm"]), state='*')
async def confirm_payment(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            try:
                order_id = callback_data["id"]
                api.change_order_status(order_id, 'confirmed')
                await call.message.answer('🔒 Заявка закрыта')
                api.delete_order(order_id)
                await call.answer()
            except KeyError:
                await call.message.answer('Ошибка!')
            await call.answer()
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(cb2.filter(action=["not_confirm"]), state='*')
async def not_confirm_payment(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            try:
                order_id = callback_data["id"]
                api.change_order_status(order_id, 'dispute')
                await call.message.answer('<b>🧑🏼‍✈ Открыт диспут</b>\n⏳ Ожидайте, с вами свяжется модератор.', parse_mode=types.ParseMode.HTML)
                await call.answer()
            except KeyError:
                await call.message.answer('Ошибка!')
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(state='*', text='create_ad')
async def create_ad(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            u_ads = api.get_user_ads(call.from_user.id)
            u_info = api.get_user_info(call.from_user.id)
            if u_info['state'] == 'no_deposit':
                button1 = types.InlineKeyboardButton(text='⬆ Внести депозит', callback_data='dep_in')
                buttons_ = [button1]
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                keyboard.add(*buttons_)
                await call.message.answer(f'🔐 Для публикации объявления необходимо внести страховой депозит <b>{config.DEPOSIT} USDT</b>.\n\n'
                                          '❓ <b>Зачем это нужно</b>\n\nСтраховой депозит - это система безопасности '
                                          'защищающая контрагентов от нежелательных потерь и гарантирующая проведение '
                                          'сделок в случае игнорирования мерчантом заявки\n\n<b>⚠️ Важно ⚠️</b>\n\nВы имеете '
                                          'полное право отказаться от сделки, в случае если вас не устраивают ее '
                                          'условия.\n\nВ случае прекращения работы с платформой депозит '
                                          'возвращается в течение 15 рабочих дней на USDT кошелёк',
                                          parse_mode=types.ParseMode.HTML, reply_markup=keyboard)

            elif len(u_ads) > 0:
                await call.answer('Недоступно создание более одного объявления!')

            else:
                u_info = api.get_user_info(call.from_user.id)
                if u_info['USDT_balance'] < 1:
                    await call.message.answer('<b>Недостаточный баланс...</b>\n\nПополните баланс в разделе <b>Кошелек ➡ Ввод ➡ Создать заявку</b>',
                                              parse_mode=types.ParseMode.HTML)
                else:
                    await call.message.answer('📝 Укажите минимальный лимит сделки')

                    state = dp.current_state(user=call.from_user.id)
                    await state.set_state(States.MIN_LIMIT_STATE[0])
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.message_handler(state=States.MIN_LIMIT_STATE)
async def ad_min_limit(msg: types.Message, state: FSMContext):
    try:
        min_limit = float(msg.text)
        async with state.proxy() as data:
            data['min_limit'] = min_limit

        ad_id = len(api.get_user_ads(msg.from_user.id)) + msg.from_user.id
        amount_ = api.get_user_info(msg.from_user.id)['USDT_balance']
        api.add_ad(ad_id, msg.from_user.id, float(min_limit), amount_)

        await msg.answer('✅ Объявление добавлено')

        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(States.USER_STATE[0])

    except ValueError:
        await msg.answer('Некорректный ввод... Укажите только число.')


@dp.callback_query_handler(state='*', text='delete_ad')
async def delete_ad(call: types.CallbackQuery):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            u_ad = api.get_user_ads(call.from_user.id)
            for ad in u_ad:
                api.delete_ad(ad['id'])

            await call.answer('✅ Объявление удалено')
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)


@dp.callback_query_handler(state='*', text='edit_min')
async def edit_min(call: types.CallbackQuery, state: FSMContext):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            u_ad = api.get_user_ads(call.from_user.id)
            if len(u_ad) == 0:
                await call.answer('У вас нет созданного объявления')
            else:
                await call.message.answer('Укажите новый минимальный лимит сделки:')
                ad_id = u_ad[0]['id']
                async with state.proxy() as data:
                    data['ad_id'] = ad_id

                    state = dp.current_state(user=call.from_user.id)
                    await state.set_state(States.CHANGE_MIN_LIMIT[0])
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.message_handler(state=States.CHANGE_MIN_LIMIT)
async def new_min_limit(msg: types.Message, state: FSMContext):
    try:
        new_lim = float(msg.text)
        async with state.proxy() as data:
            ad_id = data['ad_id']

        api.change_ad_min(ad_id, new_lim)
        await msg.answer('✅ Объявление обновлено')
        state = dp.current_state(user=msg.from_user.id)
        await state.set_state(States.USER_STATE[0])
    except ValueError:
        await msg.answer('Некорректный ввод... Укажите только число.')


@dp.callback_query_handler(cb2.filter(action=["user_ad"]), state='*')
async def user_ad(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            ad_id = callback_data['id']
            date = datetime.now()
            ad = api.get_ad_info(ad_id)
            owner_info = api.get_user_info(ad['owner_id'])

            reg_date = datetime.strptime(owner_info['reg_date'], '%Y-%m-%d')
            active_period = (date - reg_date).days
            lim = owner_info['limit']
            if float(lim) < 10001:
                status = 'Bronze 🥉'

            elif 10000 < float(lim) < 25001:
                status = 'Silver 🥈'

            elif 25000 < float(lim) < 50001:
                status = 'Gold 🥉'

            elif float(lim) > 50000:
                status = 'Diamond 💎'

            if 4 >= active_period % 10 <= 2:
                mes_active_per = str(active_period) + ' дня'
            elif active_period % 10 == 1:
                mes_active_per = str(active_period) + ' день'
            elif 19 >= active_period >= 11:
                mes_active_per = str(active_period) + 'дней'
            else:
                mes_active_per = str(active_period) + ' дней'

            min_lim = ad['min_amount']
            max_lim = ad['max_amount']
            mes = '🙍🏼‍♂ <b>Пользователь</b> ' + owner_info['username'] + ': ' + status + '\n\n' + \
                  '<b>Время работы на платформе: </b>' + mes_active_per + \
                  '\n<b>Количество проведенных сделок: </b>' + str(owner_info['trade_count']) + \
                  '\n<b>Общий объём проведенных сделок: </b>' + str(owner_info['trade_amount']) + ' USDT' + f'\n\n<b>Минимальный лимит: </b>{min_lim} USDT' \
                  f'\n<b>Резерв: </b>{max_lim} USDT' + \
                  '\n\n\n\n' + '<i>Вы не можете создать сделку на обмен монет. Подробности у администраторов.</i>'

            await call.message.answer(mes, parse_mode=types.ParseMode.HTML)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()


@dp.callback_query_handler(cb2.filter(action=["fake_ad"]), state='*')
async def user_ad(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    u = api.get_user_info(call.from_user.id)
    try:
        if u['state'] != 'banned':
            ad_id = callback_data['id']
            date = datetime.now()
            ad = api.get_fake_info(ad_id)

            reg_date = datetime.strptime(ad['reg_date'], '%Y-%m-%d')
            active_period = (date - reg_date).days
            lim = ad['max_amount']
            if float(lim) < 10001:
                status = 'Bronze 🥉'

            elif 10000 < float(lim) < 25001:
                status = 'Silver 🥈'

            elif 25000 < float(lim) < 50001:
                status = 'Gold 🥉'

            elif float(lim) > 50000:
                status = 'Diamond 💎'

            if 4 >= active_period % 10 <= 2:
                mes_active_per = str(active_period) + ' дня'
            elif active_period % 10 == 1:
                mes_active_per = str(active_period) + ' день'
            elif 19 >= active_period >= 11:
                mes_active_per = str(active_period) + 'дней'
            else:
                mes_active_per = str(active_period) + ' дней'

            min_lim = ad['min_amount']
            max_lim = ad['max_amount']

            mes = '🙍🏼‍♂ <b>Пользователь</b> ' + ad['owner_name'] + ': ' + status + '\n\n' + \
                  '<b>Время работы на платформе: </b>' + mes_active_per + \
                  '\n<b>Количество проведенных сделок: </b>' + str(ad['trade_number']) + \
                  '\n<b>Общий объём проведенных сделок: </b>' + str(ad['trade_amount']) + ' USDT\n\n' + f'<b>Минимальный лимит: </b>{min_lim} USDT' \
                  f'\n<b>Резерв: </b>{max_lim} USDT' + \
                  '\n\n\n\n' + '<i>Вы не можете создать сделку на обмен монет. Подробности у администраторов.</i>'

            await call.message.answer(mes, parse_mode=types.ParseMode.HTML)
        else:
            button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/' + config.SUPPORT)
            buttons_ = [button1]
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(*buttons_)

            await call.message.answer(
                f'❄ <b>Ваша учётная запись заморожена</b>. Свяжитесь со службой поддержки для разбирательства.',
                parse_mode=types.ParseMode.HTML, reply_markup=keyboard)
    except KeyError:
        await call.message.answer(f'<b>Ваша учётная запись приостоновлена без возможности восстановления.</b>',
                                  parse_mode=types.ParseMode.HTML)

    await call.answer()