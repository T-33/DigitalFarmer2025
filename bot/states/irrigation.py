"""
FSM (Finite State Machine) states for irrigation flow.
"""
from aiogram.fsm.state import State, StatesGroup


class IrrigationStates(StatesGroup):
    """
    States for the irrigation recommendation flow.

    Flow:
    1. User sends /start
    2. Bot asks for photo → waiting_for_photo
    3. User sends photo
    4. Bot analyzes crop (API call)
    5. Bot asks for irrigation date → waiting_for_irrigation_date
    6. User provides date
    7. Bot calculates recommendation (API call)
    8. Bot shows result → back to idle
    """

    # Waiting for user to send crop photo
    waiting_for_photo = State()

    # Waiting for user to provide irrigation date
    waiting_for_irrigation_date = State()
