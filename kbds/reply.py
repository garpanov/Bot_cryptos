from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


start_admin_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Активности"),
            KeyboardButton(text="Обучалка")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Что Вас интересует?'
)

kb_activ_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить активность"),
            KeyboardButton(text="Изменить активность"),
        ],
        {
            KeyboardButton(text="Удалить активность"),
            KeyboardButton(text="Обучалка"),
        }
    ],
    resize_keyboard=True,
    input_field_placeholder='Что Вас интересует?'
)

kb_train_admin = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить обучалку"),
            KeyboardButton(text="Изменить обучалку"),
        ],
        {
            KeyboardButton(text="Удалить обучалку"),
            KeyboardButton(text="Активности"),
        }
    ],
    resize_keyboard=True,
    input_field_placeholder='Что Вас интересует?'
)



activ = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Тапалки'),
        KeyboardButton(text='Тестнеты')
    ]
], resize_keyboard=True, input_field_placeholder='Выберите тип')