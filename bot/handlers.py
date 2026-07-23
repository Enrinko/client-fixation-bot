from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from bot.phone import normalize_phone
from bot.storage import DuplicateClientError, LeadStorage

FIX_CLIENT_BUTTON = "Зафиксировать клиента"
PHONE_HINT = "Не похоже на телефон. Пример: +79161234567 или 89161234567. Попробуйте ещё раз:"
DUPLICATE_MESSAGE = "Клиент уже в работе."

router = Router()


class FixClient(StatesGroup):
    client_phone = State()
    realtor_phone = State()
    client_name = State()


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=FIX_CLIENT_BUTTON)]],
        resize_keyboard=True,
    )


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Привет! Я бот фиксации клиентов.\nНажмите кнопку, чтобы зафиксировать клиента.",
        reply_markup=main_menu(),
    )


@router.message(F.text == FIX_CLIENT_BUTTON)
async def start_fixation(message: Message, state: FSMContext) -> None:
    await state.set_state(FixClient.client_phone)
    await message.answer("Введите телефон клиента:", reply_markup=ReplyKeyboardRemove())


@router.message(FixClient.client_phone)
async def client_phone_entered(
    message: Message, state: FSMContext, lead_storage: LeadStorage
) -> None:
    phone = normalize_phone(message.text or "")
    if phone is None:
        await message.answer(PHONE_HINT)
        return
    if lead_storage.has_client(phone):
        await state.clear()
        await message.answer(DUPLICATE_MESSAGE, reply_markup=main_menu())
        return
    await state.update_data(client_phone=phone)
    await state.set_state(FixClient.realtor_phone)
    await message.answer("Введите телефон риелтора:")


@router.message(FixClient.realtor_phone)
async def realtor_phone_entered(message: Message, state: FSMContext) -> None:
    phone = normalize_phone(message.text or "")
    if phone is None:
        await message.answer(PHONE_HINT)
        return
    await state.update_data(realtor_phone=phone)
    await state.set_state(FixClient.client_name)
    await message.answer("Введите ФИО клиента:")


@router.message(FixClient.client_name)
async def client_name_entered(
    message: Message, state: FSMContext, lead_storage: LeadStorage
) -> None:
    name = " ".join((message.text or "").split())
    if len(name.split()) < 2:
        await message.answer("Введите ФИО полностью, например: Иванов Иван Иванович")
        return
    data = await state.get_data()
    await state.clear()
    try:
        lead_storage.add_lead(data["client_phone"], data["realtor_phone"], name)
    except DuplicateClientError:
        await message.answer(DUPLICATE_MESSAGE, reply_markup=main_menu())
        return
    await message.answer("Клиент зафиксирован ✅", reply_markup=main_menu())
