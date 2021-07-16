import abc
from typing import Dict

from framework.custom_logging import logger

menu_v = [
    {'title': 'Главная', 'url_name': 'main'},
    {'title': 'Помощь', 'url_name': 'main'},
    {'title': 'Отзывы и предложения', 'url_name': 'main'},
    {'title': 'Регистрация/Войти', 'url_name': 'register'},
]

menu_h = [
    {'title': 'Добавить объект', 'url_name': 'add_object'},
    {'title': 'Добавить материалы в объект', 'url_name': 'upload'},
    {'title': 'Очистить объект', 'url_name': 'add_object'},
    {'title': 'Удалить объект', 'url_name': 'add_object'},
    {'title': 'Скачать данные объекта (xml)', 'url_name': 'add_object'},
]


class ExtendedDataContextMixin(abc.ABC):
    def get_context_data(self, *args, **kwargs) -> Dict:
        context = super().get_context_data()
        user_menu_v = menu_v.copy()
        if self.request.user.is_authenticated:
            user_menu_v.pop(-1)
            context['leftmenu'] = menu_h
        context['mainmenu'] = user_menu_v
        logger.debug(context)
        extended_context = self.get_extended_context()
        context = {**context, **extended_context}
        return context

    @abc.abstractmethod
    def get_extended_context(self) -> Dict:
        raise NotImplementedError


#         if 'cat_selected' not in context:
#             context['cat_selected'] = ''
#         return context
