from itertools import product
from nntplib import NNTP_PORT

from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Product
from database.orm_query import orm_add_act, orm_add_train, orm_where_select_act_name, orm_update_product, \
    orm_where_select_train_name, orm_update_train, orm_where_delete_train, orm_where_delete_act
from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds import reply


admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())



@admin_router.message(Command('admin'))
async def start_cmd(message: types.Message):
    await message.answer("Привет, я виртуальный помощник",
                         reply_markup=reply.start_admin_kb)

@admin_router.message(F.text.in_({'Активности', 'Обучалка'}))
async def add_testnet_name(message: types.Message):
    if message.text == 'Активности':
        await message.answer("Выберите, что вас интересует", reply_markup=reply.kb_activ_admin)
    else:
        await message.answer("Выберите, что вас интересует", reply_markup=reply.kb_train_admin)

# ////////////////////////        Product       ////////////////

class AddProduct(StatesGroup):
    #Шаги состояний
    delete = State()

    name_change = State()

    name = State()
    description = State()
    type = State()
    link = State()
    date = State()

    product_change = None


@admin_router.message(StateFilter(None), F.text == 'Удалить активность')
async def delete_testnet_start(message: types.Message, state:FSMContext):
    await message.answer('Введите имя активности, которое хотите удалить', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddProduct.delete)

@admin_router.message(StateFilter(None), F.text == "Изменить активность")
async def change_testnet(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название активности", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name_change)



@admin_router.message(StateFilter(None), F.text == "Добавить активность")
async def add_testnet_name(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название активности", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)





@admin_router.message(StateFilter('*'), Command('отмена'))
@admin_router.message(StateFilter('*'), F.text.casefold() =="отмена")
async def delete_state(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Действия отменены", reply_markup=reply.kb_activ_admin)

@admin_router.message(StateFilter('*'), Command('назад'))
@admin_router.message(StateFilter('*'), F.text.casefold() =="назад")
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer('Предидущего шага нет, или введите название товара или напишите "отмена"')
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            previous = str(previous.state)[11:]
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n Введите {previous}")
            return
        previous = step




@admin_router.message(StateFilter(AddProduct.delete), F.text)
async def delete_testnet(message: types.Message, state: FSMContext, session: AsyncSession):
    try:
        await orm_where_delete_act(session, message.text)
        await message.answer('Активность удалена')
    except:
        await message.answer('Ошибка...\nПрограммист хочет денег..')
    await state.clear()





@admin_router.message(StateFilter(AddProduct.name_change), F.text)
async def change_testnet_name(message: types.Message, state: FSMContext, session: AsyncSession):
    AddProduct.product_change = await orm_where_select_act_name(session=session, names=message.text)
    await message.answer(
        "Введите новое название активности", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)


@admin_router.message(StateFilter(AddProduct.name), F.text)
async def add_testnet_description(message: types.Message, state: FSMContext):
    if message.text == '.' and AddProduct.product_change:
        await state.update_data(name=AddProduct.product_change[0].name)
    else:
        await state.update_data(name=message.text)
    await message.answer("Введите описание активности")
    await state.set_state(AddProduct.description)


@admin_router.message(StateFilter(AddProduct.description), F.text)
async def add_testnet_type(message: types.Message, state: FSMContext):
    if message.text == '.' and AddProduct.product_change:
        await state.update_data(description=AddProduct.product_change[0].description)
    else:
        await state.update_data(description=message.text)
    await message.answer("Выберите вид активности", reply_markup=reply.activ)
    await state.set_state(AddProduct.type)

@admin_router.message(StateFilter(AddProduct.type), F.text)
async def add_testnet_link(message: types.Message, state: FSMContext):
    if message.text == '.' and AddProduct.product_change:
        await state.update_data(type=AddProduct.product_change[0].types)
    else:
        await state.update_data(type=message.text)
    await message.answer("Введите link на пост", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddProduct.link)

@admin_router.message(StateFilter(AddProduct.link), F.text)
async def add_testnet_date(message: types.Message, state: FSMContext):
    if message.text == '.' and AddProduct.product_change:
        await state.update_data(link=AddProduct.product_change[0].link)
    else:
        await state.update_data(link=message.text)
    await message.answer("Введите дату поста")
    await state.set_state(AddProduct.date)

@admin_router.message(StateFilter(AddProduct.date), F.text)
async def add_testnet_prepared(message: types.Message, state: FSMContext, session:AsyncSession):
    if message.text == '.' and AddProduct.product_change:
        await state.update_data(data=AddProduct.product_change[0].date)
    else:
        await state.update_data(date=message.text)
    data = await state.get_data()
    try:
        if AddProduct.product_change:
            await orm_update_product(session,AddProduct.product_change[0].name,data)
        else:
            await orm_add_act(session, data)
        await message.answer("Активность успешно добавлена/изменена", reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
    except:
        await message.answer("Произошла ошибка..", reply_markup=reply.kb_activ_admin)
        await state.clear()


# //////////////////////        Train           ///////////////////////////



class AddTrain(StatesGroup):
    #Шаги состояний
    delete = State()
    name_change = State()

    name = State()
    description = State()

    train_change = None


@admin_router.message(StateFilter(None), F.text == 'Удалить обучалку')
async def delete_train_start(message: types.Message, state: FSMContext):
    await message.answer('Введите имя обучалки, которое хотите удалить', reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(AddTrain.delete)

@admin_router.message(StateFilter(AddTrain.delete), F.text)
async def delete_train(message: types.Message, state: FSMContext, session: AsyncSession):
    try:
        await orm_where_delete_train(session, message.text)
        await message.answer("Обучалка удалена")
    except:
        await message.answer("Ошибка...\nПрограммист хочет денег..")
    await state.clear()


@admin_router.message(StateFilter(None), F.text == 'Изменить обучалку')
async def change_train(message: types.Message, state: FSMContext):
    await message.answer(
        'Введите название обучалки, которое хотите заменить', reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddTrain.name_change)


@admin_router.message(StateFilter(AddTrain.name_change), F.text)
async def change_train_name(message: types.Message, state: FSMContext, session: AsyncSession):
    AddTrain.train_change = await orm_where_select_train_name(session=session, names=message.text)
    await message.answer(
        'Введите новое название обучалки', reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddTrain.name)


@admin_router.message(StateFilter(None), F.text == "Добавить обучалку")
async def add_train_name(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название обучалки", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddTrain.name)


@admin_router.message(StateFilter(AddTrain.name), F.text)
async def add_train_description(message: types.Message, state: FSMContext):
    if message.text == '.' and AddTrain.train_change:
        await state.update_data(name=AddTrain.train_change[0].name)
        print(1)
    else:
        await state.update_data(name=message.text)
    await message.answer("Введите содержимое обучалки")
    await state.set_state(AddTrain.description)

@admin_router.message(StateFilter(AddTrain.description), F.text)
async def add_train_prepared(message: types.Message, state: FSMContext, session:AsyncSession):
    if message.text == '.' and AddTrain.train_change:
        await state.update_data(description=AddTrain.train_change[0].description)
    else:
        await state.update_data(description=message.text)
    data = await state.get_data()
    try:
        if AddTrain.train_change:
            await orm_update_train(session, AddTrain.train_change[0].name, data)
        else:
            await orm_add_train(session, data)
        await message.answer("Обучалка успешно добавлена/изменена")
        await state.clear()
        AddTrain.train_change = None
    except:
        await message.answer("Произошла ошибка..", reply_markup=reply.kb_activ_admin)
        await state.clear()