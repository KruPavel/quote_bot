from aiogram import Bot, Router, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.filters.text import Text

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from info import TOKEN, text1, text2, text3, text4, text5


bot = Bot(token=TOKEN)
dp = Dispatcher()
main_router = Router()
main_markup = ReplyKeyboardBuilder()
main_markup.button(text='Найти цитату')
main_markup.button(text='Записать цитату')
main_markup.adjust(1, repeat=False)


set_default_commands: list = [
    types.BotCommand(command='start', description='Запустить бота'),
    types.BotCommand(command='write_a_quote', description='Записать цитату'),
    types.BotCommand(command='find_a_quote', description='Найти цитату')
]


class GetQuote(StatesGroup):
    quote: State = State()


class GiveQuote(StatesGroup):
    quote: State = State()


@main_router.message(Command('start'))
async def start(message: types.message):
    await bot.set_my_commands(set_default_commands)
    await message.answer(text=f'Привет, {message.from_user.first_name}! {text1}', reply_markup=main_markup.as_markup())


@main_router.message(Command('write_a_quote'))
@main_router.message(Text('Записать цитату'))
async def write_a_quote(message: types, state: FSMContext):
    await message.answer(text=text2, reply_markup=None)
    await state.set_state(GetQuote.quote)


@main_router.message(GetQuote.quote)
async def get_quote(message: types, state: FSMContext):
    with open ('data.txt', 'a+') as file:
        file.write(message.text)
        file.write(f'\n')
    await message.answer(text=text3)
    await state.clear()


@main_router.message(Text('Найти цитату'))
@main_router.message(Command('find_a_quote'))
async def find_a_quote(message: types.message, state: FSMContext):
    await message.answer(text=text4, reply_markup=None)
    await state.set_state(GiveQuote.quote)


@main_router.message(GiveQuote.quote)
async def give_quote(message: types.message, state: FSMContext):
    quotes = []
    with open ('data.txt', 'r+') as file:
        data = file.readlines()
        for string in data:
            if string.find(message.text) != -1 and len(message.text) > 2:
                array = string.split(' | ')
                quotes.append(array[2])
    if len(quotes) > 0:
        await message.answer(text= f'\n'.join(quotes))
    else:
        await message.answer(text=text5)
    await state.clear()



dp.include_router(main_router)


if __name__ == '__main__':
    dp.run_polling(bot)