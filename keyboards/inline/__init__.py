from .start_ikb import start_ikb, main_menu_ikb
from .gift_ikb import gift_ikb, check_subscribe_ikb, pick_gift
from .admin_ikb import *
from .manager_ikb import *
from .calculation_savings_ikb import generate_inline_keyboard, confirm_ikb
from .catalogue_ikb import catalogue_ikb
from .discounts import discounts_ikb
from .dialog_ikb import answer_for_manager_ikb, answer_for_user_dialog_ikb

__all__: list[str] = [
    # start_ikb
    'start_ikb',
    'main_menu_ikb',
    # gift_ikb
    'gift_ikb',
    'check_subscribe_ikb',
    'pick_gift',
    # admin_ikb
    'answer_for_user_ikb',
    'admin_menu_ikb',
    'show_all_managers_ikb',
    'confirm_add_manager_ikb',
    'confirm_del_manager_ikb',
    'back_show_all_managers_ikb',
    # manager_ikb
    'manager_menu_ikb',
    'show_all_my_dialogs_ikb',
    'dialog_with_user_ikb',
    'back_dialog_with_user_ikb',
    'back_all_dialogs_ikb',
    'approve_search_dialog_ikb',
    'notification_new_manager_ikb',
    'back_manager_menu_ikb',
    # calculation_savings_ikb
    'generate_inline_keyboard',
    'confirm_ikb',
    # catalogue_ikb
    'catalogue_ikb',
    # discounts_ikb
    'discounts_ikb',
    # dialog_ikb
    'answer_for_manager_ikb',
    'answer_for_user_dialog_ikb'

]
