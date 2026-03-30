import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

BOT_TOKEN = "8338523828:AAFLCVgERXdIHEhHmiP7dQz7lmRHBn7wzGE"
CHANNEL_ID = -1003730509838
BOT_USERNAME = "yukoqimi_bot_robot"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ================= STATES =================
class Form(StatesGroup):
    tarif = State()
    yuk = State()
    vazn = State()
    qayerdan = State()
    qayerga = State()
    mashina = State()
    tel = State()

# ================= TARJIMALAR =================
T = {
"uz":{
"lang":"Tilni tanlang",
"reklama":"📢 Reklama berish",
"tarif":"Tarifni tanlang",
"oddiy":"📦 Oddiy",
"tezkor":"⚡️ Tezkor",
"vip":"💎 VIP",
"yuk":"📦 Yuk turini yozing",
"vazn":"⚖️ Yuk vazni",
"qayerdan":"📍 Qayerdan olinadi",
"qayerga":"📍 Qayerga yetkaziladi",
"mashina":"🚚 Qanday mashina kerak",
"tel":"📞 Telefon raqam",
"sent":"✅ Yuk kanalga yuborildi",
"band_btn":"✅ Yuk band qilindi",
"band":"❌ Yuk band qilindi",
"yangi":"➕ Yangi yuk"
},

"ru":{
"lang":"Выберите язык",
"reklama":"📢 Подать объявление",
"tarif":"Выберите тариф",
"oddiy":"📦 Обычный",
"tezkor":"⚡️ Срочный",
"vip":"💎 VIP",
"yuk":"📦 Тип груза",
"vazn":"⚖️ Вес",
"qayerdan":"📍 Откуда",
"qayerga":"📍 Куда",
"mashina":"🚚 Тип машины",
"tel":"📞 Телефон",
"sent":"✅ Отправлено",
"band_btn":"✅ Груз занят",
"band":"❌ Груз занят",
"yangi":"➕ Новый груз"
},

"en":{
"lang":"Choose language",
"reklama":"📢 Post advertisement",
"tarif":"Choose tariff",
"oddiy":"📦 Standard",
"tezkor":"⚡️ Express",
"vip":"💎 VIP",
"yuk":"📦 Cargo type",
"vazn":"⚖️ Weight",
"qayerdan":"📍 From",
"qayerga":"📍 To",
"mashina":"🚚 Truck type",
"tel":"📞 Phone",
"sent":"✅ Sent",
"band_btn":"✅ Cargo taken",
"band":"❌ Cargo taken",
"yangi":"➕ New cargo"
},

"tr":{
"lang":"Dil seçin",
"reklama":"📢 Reklam ver",
"tarif":"Tarif seçin",
"oddiy":"📦 Standart",
"tezkor":"⚡️ Hızlı",
"vip":"💎 VIP",
"yuk":"📦 Yük türü",
"vazn":"⚖️ Ağırlık",
"qayerdan":"📍 Nereden",
"qayerga":"📍 Nereye",
"mashina":"🚚 Araç türü",
"tel":"📞 Telefon",
"sent":"✅ Gönderildi",
"band_btn":"✅ Yük alındı",
"band":"❌ Yük alındı",
"yangi":"➕ Yeni yük"
}
}

user_lang = {}

# ================= TIL TUGMALARI =================
lang_kb = InlineKeyboardMarkup(
inline_keyboard=[
[
InlineKeyboardButton(text="🇺🇿 O'zbek",callback_data="lang_uz"),
InlineKeyboardButton(text="🇷🇺 Русский",callback_data="lang_ru")
],
[
InlineKeyboardButton(text="🇬🇧 English",callback_data="lang_en"),
InlineKeyboardButton(text="🇹🇷 Türkçe",callback_data="lang_tr")
]
]
)

# ================= START =================
@dp.message(CommandStart())
async def start(message:Message):
    await message.answer("Tilni tanlang",reply_markup=lang_kb)

# ================= TIL TANLASH =================
@dp.callback_query(F.data.startswith("lang_"))
async def set_lang(call:CallbackQuery):

    lang=call.data.split("_")[1]
    user_lang[call.from_user.id]=lang

    tarif_kb=InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text=T[lang]["oddiy"],callback_data="tarif_oddiy")],
    [InlineKeyboardButton(text=T[lang]["tezkor"],callback_data="tarif_tezkor")],
    [InlineKeyboardButton(text=T[lang]["vip"],callback_data="tarif_vip")]
    ]
    )

    await call.message.answer(T[lang]["tarif"],reply_markup=tarif_kb)

# ================= YANGI_YUK =================
@dp.callback_query(F.data=="yangi_yuk")
async def yangi_yuk(call:CallbackQuery,state:FSMContext):

    lang=user_lang.get(call.from_user.id,"uz")

    tarif_kb=InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text=T[lang]["oddiy"],callback_data="tarif_oddiy")],
    [InlineKeyboardButton(text=T[lang]["tezkor"],callback_data="tarif_tezkor")],
    [InlineKeyboardButton(text=T[lang]["vip"],callback_data="tarif_vip")]
    ]
    )

await call.message.answer(T[lang]["tarif"],reply_markup=tarif_kb)

# ================= TARIF =================
@dp.callback_query(F.data.startswith("tarif_"))
async def tarif(call:CallbackQuery,state:FSMContext):

    tarif=call.data.split("_")[1]
    await state.update_data(tarif=tarif)

    lang=user_lang.get(call.from_user.id,"uz")

    await call.message.answer(T[lang]["yuk"])
    await state.set_state(Form.yuk)

# ================= FORM =================
@dp.message(Form.yuk)
async def yuk(message:Message,state:FSMContext):

    lang=user_lang.get(message.from_user.id,"uz")

    await state.update_data(yuk=message.text)
    await message.answer(T[lang]["vazn"])
    await state.set_state(Form.vazn)

@dp.message(Form.vazn)
async def vazn(message:Message,state:FSMContext):

    lang=user_lang.get(message.from_user.id,"uz")

    await state.update_data(vazn=message.text)
    await message.answer(T[lang]["qayerdan"])
    await state.set_state(Form.qayerdan)

@dp.message(Form.qayerdan)
async def qayerdan(message:Message,state:FSMContext):

    lang=user_lang.get(message.from_user.id,"uz")

    await state.update_data(qayerdan=message.text)
    await message.answer(T[lang]["qayerga"])
    await state.set_state(Form.qayerga)

@dp.message(Form.qayerga)
async def qayerga(message:Message,state:FSMContext):

    lang=user_lang.get(message.from_user.id,"uz")

    await state.update_data(qayerga=message.text)
    await message.answer(T[lang]["mashina"])
    await state.set_state(Form.mashina)

@dp.message(Form.mashina)
async def mashina(message:Message,state:FSMContext):

    lang=user_lang.get(message.from_user.id,"uz")

    await state.update_data(mashina=message.text)
    await message.answer(T[lang]["tel"])
    await state.set_state(Form.tel)

@dp.message(Form.tel)
async def tel(message:Message,state:FSMContext):

    lang=user_lang.get(message.from_user.id,"uz")

    await state.update_data(tel=message.text)
    data=await state.get_data()

    post=f"""
🚛 <b>YANGI YUK</b>

📦 <b>Yuk:</b> {data['yuk']}
⚖️ <b>Vazn:</b> {data['vazn']}

📍 <b>Yo‘nalish:</b>
{data['qayerdan']} ➜ {data['qayerga']}

🚚 <b>Mashina:</b> {data['mashina']}

📞 <b>Telefon:</b>
{data['tel']}

💰 <b>Tarif:</b> {data['tarif']}
"""

    kb=InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton(text=T[lang]["reklama"],url=f"https://t.me/{BOT_USERNAME}")]
    ]
    )

    await bot.send_message(CHANNEL_ID,post,reply_markup=kb,parse_mode="HTML")

    menu_kb=InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=T[lang]["yangi"],callback_data="yangi_yuk")]
        ]
    )

    await message.answer(T[lang]["sent"],reply_markup=menu_kb)

    await state.clear()


# ================= RUN =================
async def main():
    print("Bot ishga tushdi")
    await dp.start_polling(bot)

if __name__=="__main__":
    asyncio.run(main())
