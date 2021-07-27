import abc
from typing import Dict

from framework.custom_logging import logger

menu_h = [
    {'title': 'Объекты', 'url_name': 'main'},
    {'title': 'Помощь', 'url_name': 'help'},
    {'title': 'Отзывы и предложения', 'url_name': 'reviews'},
    {'title': 'Выйти', 'url_name': 'logout'},
    {'title': 'Регистрация', 'url_name': 'register'},
    {'title': 'Вход', 'url_name': 'login'},
]

menu_v = [
    {'title': 'Создать объект', 'url_name': 'add_object'},
    {'title': 'Добавить материалы в объект', 'url_name': 'upload'},
    {'title': 'Очистить объект', 'url_name': 'clear_object'},
    {'title': 'Удалить объект', 'url_name': 'del_object'},
    {'title': 'Скачать данные объекта (xml)', 'url_name': 'select_dl_obj'},
]


class ExtendedDataContextMixin(abc.ABC):
    def get_context_data(self, *args, **kwargs) -> Dict:
        context = super().get_context_data()
        # user_menu_h = []
        if self.request.user.is_authenticated:
            user_menu_h = menu_h[0:-2]
            context['leftmenu'] = menu_v
        else:
            user_menu_h = menu_h[0:3] + menu_h[-2:]
        context['mainmenu'] = user_menu_h
        logger.debug(context)
        extended_context = self.get_extended_context()
        context = {**context, **extended_context}
        return context

    @abc.abstractmethod
    def get_extended_context(self) -> Dict:
        raise NotImplementedError
