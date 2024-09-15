from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_inline(*,  btns: dict[str,str], sizes: tuple[int,int]):
    button_inline = InlineKeyboardBuilder()
    for text, date in btns.items():
        button_inline.add(InlineKeyboardButton(text=text, callback_data=date))

    return button_inline.adjust(*sizes).as_markup()

