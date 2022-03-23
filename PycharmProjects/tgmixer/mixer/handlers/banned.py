from aiogram import Bot, types
from loader import dp, bot
from utils import States


@dp.message_handler(state=States.BANNED)
async def process_start_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)  # take current state of user
    await state.set_state(States.UNAUTHORIZED_STATE[0])
    await message.answer("Ваш аккаунт на время заморожен!")



