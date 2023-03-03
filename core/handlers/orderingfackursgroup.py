import asyncio
from datetime import datetime

from aiogram import Router, F

from core.filters.prepodfilter import Prepods
from core.filters.groupfilter import Groups
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from core.keyboards.meny import menu
from core.utils.dbconnect import cursorexecute, insertdata, finduser, log_event
from core.keyboards.keyb_generator import make_keyb, makegroups
from core.utils.messages import start_msg, reg_msg, help_msg, updated_msg, registered_msg, registered1_msg, \
    stud_or_prepod_msg, wait_preplist_msg, sendid_prep_msg, idbigger_one_msg, addprepods_msg, sps_reg

router = Router()
yesno = ['ДА', 'НЕТ']
roles = ['Студент', 'Преподаватель']
name_facul = ['АТиЭ', 'БиВМ', 'АБиЭ', 'ЭК', 'АСП']
num_kurs = ['1 курс', '2 курс', '3 курс', '4 курс', '5 курс', '6 курс']
groupslist = []
prepodlist = []


class OrderGroup(StatesGroup):
    choosing_answer = State()
    choosing_prepod = State()
    choosing_prepods = State()
    choosing_role = State()
    choosing_facul = State()
    choosing_kurs = State()
    choosing_group = State()
    updating_prof = State()
    comp_state = State()


@router.message(Command(commands=['reg']))
async def cmd_reg(message: Message, state: FSMContext):
    user = await finduser(message.from_user.id)
    if user is False:
        await message.answer(text=stud_or_prepod_msg,
                             reply_markup=make_keyb(roles))
        await state.set_state(OrderGroup.choosing_role)
        await state.update_data(updating_prof=False)
    else:
        await message.answer(text=f"{registered1_msg} {help_msg}", reply_markup= await menu())


@router.message(Command(commands=['updprof']))
async def cmd_updprof(message: Message, state: FSMContext):
    user = await finduser(message.from_user.id)
    if user is True:
        await message.answer(text=stud_or_prepod_msg,
                             reply_markup=make_keyb(roles))
        await state.update_data(updating_prof=True)
        await state.set_state(OrderGroup.choosing_role)
        event = 'Запрос на обновление аккаунта'
        user_id = message.from_user.id
        username = message.from_user.username
        name = f"{message.from_user.first_name} {message.from_user.last_name}"
        mess = message.text
        date = datetime.now()
        await log_event(user_id, username, name, event, mess, date)
    else:
        await message.answer(text=reg_msg.format(message.from_user.first_name),
                             reply_markup= make_keyb(['Зарегистрироваться']))


@router.message(OrderGroup.choosing_role, F.text.in_(roles))
async def role_chosing(message: Message, state: FSMContext):
    if message.text == 'Студент':
        await message.answer(text="Выбери свой факультет:", reply_markup=make_keyb(name_facul))
        await state.set_state(OrderGroup.choosing_facul)
    elif message.text == 'Преподаватель':
        sql = f"""SELECT name, prepod_id FROM Prepods """
        data = await cursorexecute(sql, None)
        prepods = list(map(lambda x: list(x), data))
        msg = []
        for i in range(0, len(prepods), 100):
            msg.append(prepods[i:i + 100])
        await message.answer(
            text=sendid_prep_msg,
            reply_markup = ReplyKeyboardRemove)
        await message.answer(
            text=wait_preplist_msg)
        await asyncio.sleep(5)
        for i in msg:
            msg1 = []
            for k in i:
                msg = f"id: {k[1]} - {k[0]}\n"
                msg1.append(msg)
                prepodlist.append(k[1])
            await message.answer(text=' '.join(msg1))
        await state.set_state(OrderGroup.choosing_prepod)
        # print(prepodlist)
@router.message(OrderGroup.choosing_prepod, Prepods(prepodlist))
async def prepods_chosing(message: Message, state: FSMContext):
    data = await state.get_data()
    msg = message.text.split(' ')
    if len(msg) > 1:
        await message.answer(text=idbigger_one_msg)
    else:
        if data['updating_prof'] is True:
            lasdate = datetime.now()
            sql = f"""UPDATE User_tg SET status = 'prepod',  group_id = '0', prepod_id0 ={msg[0]}, last_date = '{lasdate}' WHERE user_id = '{message.from_user.id}' """
            await insertdata(sql)
            await message.answer(text="<b>Если хотите обновить или добавить других преподавателей нажмите ДА / НЕТ</b>",
                                 reply_markup=make_keyb(yesno))
            await state.set_state(OrderGroup.choosing_answer)
        else:
            regdate = datetime.now()
            sql = f"""INSERT INTO User_tg(user_id, status, group_id, prepod_id0, reg_date) 
            VALUES ({message.from_user.id},'prepod', 0000, {msg[0]},'{regdate}')"""
            await insertdata(sql)
            await message.answer(text="<b>Если хотите подписаться на расписание других преподавателей нажмите ДА / НЕТ</b>",
                                 reply_markup=make_keyb(yesno))
            await state.set_state(OrderGroup.choosing_answer)
@router.message(OrderGroup.choosing_answer, F.text.in_(yesno))
async def answer_choosing(message: Message, state: FSMContext):
    data = await state.get_data()
    if message.text == "ДА":
        await message.answer(text=addprepods_msg, reply_markup=ReplyKeyboardRemove)
        if data['updating_prof'] is True:
            await state.set_state(OrderGroup.choosing_prepods)
        else:
            await state.set_state(OrderGroup.choosing_prepods)
    else:
        await message.answer(text=f"{sps_reg.format(message.from_user.first_name)}{help_msg}",
                             reply_markup=await menu())
    event = 'Регистрация или обновление'
    user_id = message.from_user.id
    username = message.from_user.username
    name = f"{message.from_user.first_name} {message.from_user.last_name}"
    mess = message.text
    date = datetime.now()
    await log_event(user_id, username, name, event, mess, date)


@router.message(OrderGroup.choosing_prepods, Prepods(prepodlist))
async def prepods_chosing(message: Message, state: FSMContext):
    data = await state.get_data()
    msg = message.text.split(' ')
    sql = None
    lasdate = datetime.now()

    if len(msg) == 3:
        sql = f"""UPDATE User_tg SET status = 'prepod',  group_id = '', prepod_id1 ={msg[0]}, prepod_id2 ={msg[1]},
                prepod_id3 ={msg[2]}, last_date = '{lasdate}'
                WHERE user_id = '{message.from_user.id}' """
    elif len(msg) == 2:
        sql = f"""UPDATE User_tg SET status = 'prepod',  group_id = '', prepod_id1 ={msg[0]}, prepod_id2 ={msg[1]},
               prepod_id3 = '', last_date = '{lasdate}'
               WHERE user_id = '{message.from_user.id}' """
    elif len(msg) == 1:
        sql = f"""UPDATE User_tg SET status = 'prepod', group_id = '', prepod_id1 ={msg[0]}, prepod_id2 ='',
                prepod_id3 = '', last_date = '{lasdate}'
                WHERE user_id = '{message.from_user.id}' """

    if data['updating_prof'] is True:
        await insertdata(sql)
        await message.answer(text=f"""<b>Аккаунт обновлен!</b>""", reply_markup=await menu())
        event = 'Обновление аккаунта'
        user_id = message.from_user.id
        username = message.from_user.username
        name = f"{message.from_user.first_name} {message.from_user.last_name}"
        mess = message.text
        date = datetime.now()
        await log_event(user_id, username, name, event, mess, date)
    else:
        sig = await insertdata(sql)
        if sig is True:
            await message.answer(text=f"""<b>Cпасибо за регистрацию {message.from_user.first_name}!{help_msg}</b>""",
                                 reply_markup=await menu())
        else:
            await message.answer(text=f"{registered1_msg} {help_msg}",
                                 reply_markup=await menu())
    await state.set_state(OrderGroup.comp_state)
@router.message(OrderGroup.comp_state, Groups(groupslist))
async def fac_choosing(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    name = f"{message.from_user.first_name} {message.from_user.last_name}"
    event = ''
    mess = message.text
    date = datetime.datetime.now()
    await log_event(user_id, username, name, event, mess, date)


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
    await state.set_state(OrderGroup.choosing_group)


@router.message(OrderGroup.choosing_group, Groups(groupslist))
async def group_choosing(message: Message, state: FSMContext):
    data = await state.get_data()
    kurs, slovo = data['choosen_kurs'].split(" ", 1)
    lasdate = datetime.now()
    if data['updating_prof'] is True:
        sql = f"""UPDATE User_tg SET status = 'student',
        group_id = (SELECT group_id FROM Groups WHERE name = '{message.text}'),
        prepod_id0 = '', prepod_id1 = '', prepod_id2 = '', prepod_id3 = '', last_date = '{lasdate}'
        WHERE user_id = '{message.from_user.id}' """
        await insertdata(sql)
        await message.answer(text=updated_msg.format(data['choosen_fac'], kurs, message.text),
                             reply_markup=await menu())
        user_id = message.from_user.id
        username = message.from_user.username
        name = f"{message.from_user.first_name} {message.from_user.last_name}"
        event = 'Обновление аккаунта'
        mess = message.text
        date = datetime.now()
        await log_event(user_id, username, name, event, mess, date)
    else:
        regdate = datetime.now()
        sql = f"""INSERT INTO User_tg(user_id, status, group_id, reg_date) VALUES ({message.from_user.id}, 'student',
            (SELECT group_id FROM Groups WHERE name = '{message.text}'), '{regdate}')"""
        sig = await insertdata(sql)
        if sig is True:
            await message.answer(text=registered_msg.format(message.from_user.first_name, data['choosen_fac'],
                                                            kurs, message.text ), reply_markup=await menu())
            user_id = message.from_user.id
            username = message.from_user.username
            name = f"{message.from_user.first_name} {message.from_user.last_name}"
            event = 'Регистрация'
            mess = message.text
            date = datetime.now()
            await log_event(user_id, username, name, event, mess, date)
        else:
            await message.answer(text=f"{registered1_msg} {help_msg}", reply_markup=await menu())
