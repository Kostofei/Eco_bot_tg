from aiogram.filters.callback_data import CallbackData
from typing import Optional


class UserCallbackData(CallbackData, prefix='user'):
    target: Optional[str] = None
    action: Optional[str] = None
    details: Optional[str] = None
    user_id: Optional[int] = None
    chat_id: Optional[int] = None
    gift: Optional[str] = None
    dialog_id: Optional[int] = None


class AdminCallbackData(CallbackData, prefix='admin'):
    target: Optional[str] = None
    action: Optional[str] = None
    details: Optional[str] = None
    manager_id: Optional[int] = None


class ManagerCallbackData(CallbackData, prefix='admin'):
    target: Optional[str] = None
    action: Optional[str] = None
    details: Optional[str] = None
    manager_id: Optional[int] = None
    user_id: Optional[int] = None
    dialog_id: Optional[int] = None


class DialogCallbackData(CallbackData, prefix='admin'):
    target: Optional[str] = None
    action: Optional[str] = None
    details: Optional[str] = None
    dialog_id: Optional[int] = None
