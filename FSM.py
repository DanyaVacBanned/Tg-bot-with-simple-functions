from aiogram.dispatcher.filters.state import State, StatesGroup

class Request(StatesGroup):
    user_request = State()

class Sub(StatesGroup):
    subApprove = State()

class Unsub(StatesGroup):
    unsubApprove = State()

class Sendall(StatesGroup):
    mailing = State()