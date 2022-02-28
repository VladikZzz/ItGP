from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, CallbackQuery
from aiogram.utils import executor
from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters import Text

bot = Bot('5247379382:AAFgWDJRuRAoH81PxZg9gZ8rT2qKfTwiYVI')  # Не забудьте подставить свой токен!
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    make_offer_button = KeyboardButton('💸 Пожертвовать')
    about = KeyboardButton('📚 О нас')
    greet_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    greet_kb.row(make_offer_button, about)

    await message.answer("❗<b>Сайты для помощи жителям Украины блокируют, банки замораживают счета, поэтому мы вынуждены "
                         "собирать средства в Телеграмм c помощью криптовалюты.</b>❗\n\n<b>🙌 Почему ЮНИСЕФ? </b> "
                         "\nВаше пожертвование позволит вам оказаться в хорошей компании: \n\n🔺 <b>ЮНИСЕФ</b> помог "
                         "спасти больше детских жизней - 90 миллионов человек за период с 1990 года, - чем любая "
                         "другая гуманитарная организация. \n\n🔺 <b>ЮНИСЕФ</b> является крупнейшим в мире поставщиком готового к "
                         "употреблению терапевтического питания — пасты с высоким содержанием белка, которая может в "
                         "течение нескольких недель вернуть здоровье ребенку, страдающему от недостаточного питания.\n\n🔺 "
                         "<b>ЮНИСЕФ</b> проводит вакцинацию около 40 процентов детей во всем мире.",
                         reply_markup=greet_kb, parse_mode=types.ParseMode.HTML)



@dp.message_handler(Text(equals='💸 Пожертвовать'))
async def donate(message: types.Message):
    button1 = types.InlineKeyboardButton(text='BTC', callback_data='BTC')
    button2 = types.InlineKeyboardButton(text='ETH-ERC20', callback_data='ETH-ERC20')
    button3 = types.InlineKeyboardButton(text='USDT-TRC20', callback_data='USDT-TRC20')
    button4 = types.InlineKeyboardButton(text='USDT-ERC20', callback_data='USDT-ERC20')

    buttons = [button1, button2, button3, button4]
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)

    await message.answer('<b>Выберите способ пожертвования:</b>', reply_markup=keyboard, parse_mode=types.ParseMode.HTML)


@dp.message_handler(Text(equals='📚 О нас'))
async def donate(message: types.Message):
    await message.answer(
                         "🇺🇦 Сейчас, как никогда, мы объединили свои усилия и средства для помощи Украинскому народу.  "
                         "Делая пожертвования в это непростое время, Вы оказываете благотворительную помощь не только "
                         "армии и раненным, но и медикам, беженцам, детям и пенсионерам.\n\n<b>Гуманитарный штаб "
                         "помогает людям по 4-м основным направлениям:</b>\n\n❗ Организация <b>эвакуации людей</b> из зоны "
                         "военных действий. \n\n❗ Доставка <b>гуманитарной помощи</b> (продукты, вода, лекарства, "
                         "средства гигиены и т.д.) в зону военных действий. \n\n❗ <b>Размещение переселенцев</b> на базах, "
                         "в санаториях и лагерях вне зоны военных действий. \n\n❗ <b>Оказание адресной помощи</b> детям, "
                         "потерявших родителей в зоне военных действий.Каждое из направлений Гуманитарного штаба "
                         "имеет своих представителей на местах (в зоне военных действий, в местах компактного "
                         "проживания переселенцев) и тесно взаимодействует с общественными и волонтерскими "
                         "организациями, международными организациями и областными державными администрациями.", parse_mode=types.ParseMode.HTML)



@dp.callback_query_handler(state='*', text='BTC')
async def BTC(call: types.CallbackQuery):
    await call.message.answer("<b>BTC кошёлек: \n</b>bc1qgj97tka0p3nw67tgrfgtlujdqtrw5wpshf5324", parse_mode=types.ParseMode.HTML)
    await call.answer()


@dp.callback_query_handler(state='*', text='ETH-ERC20')
async def ETH(call: types.CallbackQuery):
    await call.message.answer("<b>ETH-ERC20 кошелёк: \n</b>0x4FB29e919310522a7d9a3EB2570DfAf6dF205fBF", parse_mode=types.ParseMode.HTML)
    await call.answer()


@dp.callback_query_handler(state='*', text='USDT-ERC20')
async def USDT_E(call: types.CallbackQuery):
    await call.message.answer("<b>USDT-ERC20 кошелёк: \n</b>0x4FB29e919310522a7d9a3EB2570DfAf6dF205fBF", parse_mode=types.ParseMode.HTML)
    await call.answer()


@dp.callback_query_handler(state='*', text='USDT-TRC20')
async def USDT_T(call: types.CallbackQuery):
    await call.message.answer("<b>USDT-TRC20 кошелёк: \n</b>TNzpxpaEQbHRBfsC6jJGAH4FWu2pYkiu7N", parse_mode=types.ParseMode.HTML)
    await call.answer()


if __name__ == '__main__':
    executor.start_polling(dp)