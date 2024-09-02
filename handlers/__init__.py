from aiogram import Router

from .start import start_router
from .admin import admin_router
from .manager import manager_router
from .gift import gift_router
from .question import question_router
from .mini_course import mini_course_router
from .calculation_savings import calculation_router
from .webinar import webinar_router
from .order import order_router
from .catalogue import catalogue_router
from .discounts import discounts_router
from .dialog import dialog_router
from .user import user_router


router = Router(name='root')

router.include_router(router=start_router)
router.include_router(router=admin_router)
router.include_router(router=manager_router)
router.include_router(router=gift_router)
router.include_router(router=question_router)
router.include_router(router=mini_course_router)
router.include_router(router=calculation_router)
router.include_router(router=webinar_router)
router.include_router(router=order_router)
router.include_router(router=catalogue_router)
router.include_router(router=discounts_router)
router.include_router(router=dialog_router)
router.include_router(router=user_router)
