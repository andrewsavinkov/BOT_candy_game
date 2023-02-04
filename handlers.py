from aiogram import types
from loader import dp
from random import randint

user_name=''
new_game=False
total = 150
first = 0
bot_moves=False
user_moves=False
duel=[]
current=0

@dp.message_handler(commands=['start', 'старт'])
async def mes_start(message: types.Message):
    await message.answer('Добрый день! Добро пожаловать в игру: забери все конфеты.'
                         'За один ход игрок может взять от 1 до 28 конфет. Забравший последние конфеты побеждает'
                         f'и получает все ({total}) конфеты, лежащие на столе.'
                         'Изменить количество конфет можно в соответствующем пункте меню. Удачи!')
    print(message.from_user.id)

@dp.message_handler(commands=['help'])
async def mes_help(message: types.Message):
    await message.answer('не помогу!')

@dp.message_handler(commands=['show_total'])
async def mes_help(message: types.Message):
    await message.answer(f'на столе сейчас {total} конфет')

@dp.message_handler(commands=['who'])
async def mes_help(message: types.Message):
    if bot_moves:
        await message.answer('Ходит бот')
    elif user_moves:
        await message.answer(f'Ходит {message.from_user.first_name}')
    else:
        await message.answer('Игра не началась')

@dp.message_handler(commands=['new_game'])
async def mes_new_game(message: types.Message):
    global new_game
    global user_name
    global user_moves
    global first
    new_game = True
    user_moves=True
    user_name=message.from_user.first_name
    await message.answer(f'Игра началась,'
                         f'ходит {user_name}')

@dp.message_handler(commands=['duel'])
async def mes_duel(message: types.Message):
    global new_game
    global user_name
    global user_moves
    global duel
    global first
    global current

    duel.append(int(message.from_user.id))
    duel.append(int(message.text.split()[1]))
    first = randint(0,1)
    if first:
        await dp.bot.send_message(duel[0], 'Первый ход за тобой, бери конфеты')
        await dp.bot.send_message(duel[1], 'Первый ход за твоим противником, жди своего хода')

    else:
        await dp.bot.send_message(duel[1], 'Первый ход за тобой, бери конфеты')
        await dp.bot.send_message(duel[0], 'Первый ход за твоим противником, жди своего хода')

    current = duel[0] if first else duel[1]
    new_game=True



@dp.message_handler(commands=['set'])
async def mes_set(message: types.Message):
    global total
    global new_game

    count = message.text.split()[1]
    if not new_game:
        if count.isdigit():
            total=int(count)
            await message.answer(f'Конфет теперь будет {count}')
        else:
            await message.answer(f'{message.from_user.first_name}, напишите цифрами')
    else:
        await message.answer(f'{message.from_user.first_name}, нельзя менять правила во время игры!')

def bot_makes_a_move():
    global total
    if (total / 28) < 2 and (total / 28) > 1:
        if total==29:
            candies_to_take=1
        else:
            candies_to_take=total-29
    elif total<=28:
        candies_to_take=total
    else:
        candies_to_take=randint(1, 28)
    return candies_to_take

@dp.message_handler()
async def mes_uncaught(message: types.Message):
    global current
    global total
    global duel
    global new_game
    global user_moves
    global bot_moves
    if new_game:
        if len(duel)==0:
            if message.text.isdigit():
                if int(message.text)>=1 and int(message.text)<=28:
                    total-=int(message.text)
                    if total <= 0:
                        await message.answer(f'Ура, {message.from_user.first_name}, ты победил')
                        new_game = False
                        user_moves=False
                        bot_moves=False
                        total=150
                    else:
                        await message.answer(f'{message.from_user.first_name} взял {message.text} конфет. '
                                         f' на столе осталось {total}')
                        user_moves = False
                        bot_moves = True
                        bot_takes=bot_makes_a_move()
                        total-=bot_takes
                        if total <= 0:
                            await message.answer(f'Увы, {message.from_user.first_name}, ты победил')
                            new_game = False
                            total = 150
                        else:
                            await message.answer(f'БОТ взял {bot_takes} конфет. '
                                             f' на столе осталось {total}')
                            bot_moves=False
                            user_moves=True
                else:
                    await message.answer(f'{message.from_user.first_name}, вы можете взять от 1 до 28 конфет за один раз')
            else:
                await message.answer(f'{message.from_user.first_name}, напишите цифрами')
        elif len(duel) > 0:
            if current == message.from_user.id:
                name = message.from_user.first_name
                count = message.text
                if new_game:
                    if message.text.isdigit() and 0 < int(message.text) < 29:
                        total -= int(message.text)
                        if total <= 0:
                            await message.answer(f'Ура, {name}, ты победил!')
                            await dp.bot.send_message(enemy_id(), 'К сожалению, ты проиграл, твой оппонент оказался смышленнее!')
                            new_game = False
                        else:
                            await message.answer(f'{name} взял {message.text} конфет.'
                                                     f'На столе осталось {total}')
                            await dp.bot.send_message(enemy_id(), f'Теперь твой ход, бери конфеты. На столе {total} конфет.')
                            switch_players()
                    else:
                        await message.answer(f'{name}, Надо указать число от 1 до 28!')
def switch_players():
    global duel
    global current
    if current == duel[0]:
        current=duel[1]
    else:
        current=duel[0]

def enemy_id():
    global duel
    global current
    if current == duel[0]:
        return duel[1]
    else:
        return duel[0]
