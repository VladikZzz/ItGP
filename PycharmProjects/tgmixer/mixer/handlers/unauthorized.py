from aiogram import Bot, types
import api
import config
from handlers.admin import admin_kb
from handlers.user import user_kb
from loader import dp, bot
from utils import States


@dp.message_handler(commands=['start'], state='*')
async def process_start_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)  # take current state of user
    await state.set_state(States.UNAUTHORIZED_STATE[0])
    button1 = types.InlineKeyboardButton(text='📲 Связаться', url='https://t.me/'+config.SUPPORT)
    buttons_ = [button1]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons_)

    await message.answer("<b>B2B service</b> для безопасных сделок с криптовалютами.\n\n"
                         "Для того чтобы стать нашим мерчантом и предоставлять свои услуги обмена криптовалют, свяжитесь с менеджером для уточнения деталей.\n\n"
                         "<b>Для авторизации введите токен</b>", reply_markup=keyboard, parse_mode=types.ParseMode.HTML)


# Authorization works only in UNAUTHORIZED state
@dp.message_handler(state=States.UNAUTHORIZED_STATE)
async def authorization(msg: types.Message):
    global u_token
    u_token = msg.text
    tg_id = msg.from_user.id

    state = dp.current_state(user=msg.from_user.id)  # take current state

    if api.check_token(u_token, str(tg_id)) == 'user':
        await state.set_state(States.USER_STATE[0])
        await msg.answer("Вы успешно авторизовались!", reply_markup=user_kb)
    elif api.check_token(u_token, str(tg_id)) == 'admin':
        await state.set_state(States.ADMIN_STATE)
        await msg.answer("Вы успешно авторизовались!", reply_markup=admin_kb)
    else:
        await msg.answer("Неверный токен!")
        await state.set_state(States.UNAUTHORIZED_STATE[0])

