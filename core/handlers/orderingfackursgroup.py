from aiogram import Router, F
from core.filters.groupfilter import Groups
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove
from core.utils.dbconnect import cursorexecute, insertdata, finduser
from core.keyboards.keyb_generator import make_keyb, makegroups

router = Router()

name_facul = ['АТиЭ', 'БиВМ', 'АБиЭ', 'ЭК', 'АСП']
num_kurs = ['1 курс', '2 курс', '3 курс', '4 курс', '5 курс', '6 курс']
groupslist = []


class OrderGroup(StatesGroup):
    choosing_facul = State()
    choosing_kurs = State()
    choosing_group = State()
    updating_prof = State()


@router.message(Command(commands=['reg']))
async def cmd_reg(message: Message, state: FSMContext):
    user = await finduser(message.from_user.id)
    if user is False:
        await message.answer(text="Выбери свой факультет:", reply_markup=make_keyb(name_facul))
        await state.set_state(OrderGroup.choosing_facul)
        await state.update_data(updating_prof=False)
    else:
        await message.answer(text="Вы уже зарегистрированы", reply_markup=ReplyKeyboardRemove)


@router.message(Command(commands=['updprof']))
async def cmd_updprof(message: Message, state: FSMContext):
    user = await finduser(message.from_user.id)
    if user is True:
        await message.answer(text="Выбери свой факультет:", reply_markup=make_keyb(name_facul))
        await state.set_state(OrderGroup.choosing_facul)
        await state.update_data(updating_prof=True)
    else:
        await message.answer(text="Твой аккаунт не найден, пройди регистрацию нажав комманду /reg",
                             reply_markup=ReplyKeyboardRemove)


@router.message(OrderGroup.choosing_facul, F.text.in_(name_facul))
async def fac_choosing(message: Message, state: FSMContext):
    await state.update_data(choosen_fac=message.text)
    await message.answer(text="Спасибо. Теперь, пожалуйста, выберите курс:",
                         reply_markup=make_keyb(num_kurs))
    await state.set_state(OrderGroup.choosing_kurs)


@router.message(OrderGroup.choosing_kurs, F.text.in_(num_kurs))
async def kurs_choosing(message: Message, state: FSMContext):
    await state.update_data(choosen_kurs=message.text)
    data = await state.get_data()
    kurs, slovo = data['choosen_kurs'].split(" ", 1)
    fac = data['choosen_fac']
    params = ()
    sql = f"""SELECT name FROM Groups WHERE facul = '{fac}' AND kurs = {kurs}"""
    data = await cursorexecute(sql, params)
    grouplist = map(lambda x: list(x), data)
    for i in grouplist:
        groupslist.append(i[0])
    await message.answer(text=f"""А теперь выбери свою группу:""", reply_markup=makegroups(data))


@router.message(Groups(groupslist))
async def group_choosing(message: Message, state: FSMContext):
    data = await state.get_data()
    kurs, slovo = data['choosen_kurs'].split(" ", 1)
    if data['updating_prof'] is True:
        sql = f"""UPDATE User_tg SET 
        group_id = (SELECT group_id FROM Groups WHERE name = '{message.text}')
         WHERE user_id = '{message.from_user.id}' """
        await insertdata(sql)
        await message.answer(text=
f"""<b>Аккаунт обновлен!</b>
Ваши данные:
Факультет: <b>{data['choosen_fac']}</b>
Курс: <b>{kurs}</b>
Группа: <b>{message.text}</b>
""", reply_markup=ReplyKeyboardRemove)
    else:
        sql = f"""INSERT INTO User_tg(user_id, group_id) VALUES ({message.from_user.id},
            (SELECT group_id FROM Groups WHERE name = '{message.text}'))"""
        sig = await insertdata(sql)
        if sig is True:
            await message.answer(text=f"""
                <b>Cпасибо за регистрацию {message.from_user.first_name}!</b>
                Ваши данные:
                Факультет: <b>{data['choosen_fac']}</b>
                Курс: <b>{kurs}</b>
                Группа: <b>{message.text}</b>
                """, reply_markup=ReplyKeyboardRemove)
        else:
            await message.answer(text=f"""Вы уже зарегистрированы
                """, reply_markup=ReplyKeyboardRemove)

