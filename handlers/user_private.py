from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.enums.parse_mode import ParseMode
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query import orm_select_act, orm_where_select_act, orm_select_train
from kbds.inline import get_inline

router_for_user_private = Router()


@router_for_user_private.message(CommandStart())
async def start(message: types.Message):
    await message.answer("Приветствую! Пожалуйста, выберите, что вас интересует",
                         reply_markup=get_inline(btns={'Активности': 'Activities',
                                                       'Обучалка': 'train'}, sizes=(2, 0)))



# ///////////////  inline  ///////////////

@router_for_user_private.callback_query(F.data.startswith("train"))
async def train_starts(callback: types.CallbackQuery, session: AsyncSession):
    result = ''
    for termin in await orm_select_train(session= session):
        result += f'📚<b>{termin.name}</b> - <i>{termin.description}</i>\n\n'

    await callback.answer()
    await callback.message.answer(result, parse_mode=ParseMode.HTML,
                                  reply_markup=get_inline(btns={"Астивности": 'Activities'}, sizes=(1,0)))

@router_for_user_private.callback_query(F.data.startswith("Activities"))
async def Activities_starts(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer('Выберите активности, которые вам нужны.',
                                  reply_markup=get_inline(btns={"Тапалки": 'act_tap',
                                                                'Тестнеты': 'act_test'}, sizes=(2,0)))


@router_for_user_private.callback_query(F.data.startswith("act"))
async def Activities_testn_tapal(callback: types.CallbackQuery, session: AsyncSession):
    product_id = callback.data.split("_")[-1]
    if product_id == "tap":
        type = 'Тапалки'
        inline_key = 'Тестнеты'
        inline_meaning = 'act_test'
    else:
        type = 'Тестнеты'
        inline_key = 'Тапалки'
        inline_meaning = 'act_tap'
    projects = f'<b>{type}</b>\n'
    for project in await orm_where_select_act(session=session, types=type):
        projects += (f'<b>Name — </b><i>{project.name}</i>\n  '
                     f'<b>Инвестиции — </b><i>{project.description}</i>\n  '
                     f'<b>Пост — </b><a href="{project.link}">*ТИЦЬ*</a>\n  '
                     f'<b>Пост был создан </b><i>{project.date}</i>\n\n')
    await callback.answer()
    await callback.message.answer(projects, parse_mode=ParseMode.HTML, reply_markup=get_inline(
                                                                        btns={inline_key: inline_meaning,
                                                                              'Обучалка': 'train'}, sizes=(2,0)))
