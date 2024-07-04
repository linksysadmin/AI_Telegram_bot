from aiogram.fsm.state import State, StatesGroup


class Generation(StatesGroup):
    prompt = State()
    image = State()
    # waiting = State()

