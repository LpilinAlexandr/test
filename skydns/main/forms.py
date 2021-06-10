import logging
import json
from django import forms
from django.utils import timezone
from django.utils.formats import date_format, time_format


email_logger = logging.getLogger('email')
api_logger = logging.getLogger('api')


class LogForm(forms.Form):
    """
    Базовая форма для логирования.
    """
    def __init__(self, request=None, url=None, *args, **kwargs):
        """
        Для инициализации перед валидацией требуется передать request и url
            request: HttpRequest
            url: str
        """
        super().__init__(*args, **kwargs)
        if request:
            self.request = request
            self.method = request.method
            self.url = url
            self.time = timezone.now()

    def save(self):
        """
        Возвращает словарь с урлом, методом запроса и временем запроса
        """
        return {
            'time': f'{date_format(self.time)} {time_format(self.time)}',
            'url': self.url,
            'method': self.method,
        }

    @staticmethod
    def format_message(message_dict: dict):
        """
        Преобразует словарь для логирования в строку
        :param message_dict: Словарь с параметрами для логирования
        """
        text = ''
        for key, value in message_dict.items():
            text += f" {key}: {value};"

        return text


class EmailForm(LogForm):
    """
    Форма для емеила
    """
    email = forms.EmailField(label='Ваш email')

    def save(self):
        data = super().save()
        data.update({
            'params': self.cleaned_data.get('email')
        })
        email_logger.info(self.format_message(data))
        return 'Спасибо. Email сохранён.'


class ApiForm(LogForm):

    method = forms.CharField()

    def __init__(self, params, *args, **kwargs):
        super().__init__(data=params, *args, **kwargs)
        self.params = params

    def clean_method(self):
        """
        Если метод не равен "ping" то по заданию возвращаем ошибку
        """
        if self.cleaned_data.get('method') == 'ping':
            return 'ping'
        return self.add_error('method', 'Ожидается метод "ping"')

    def save(self):
        data = super().save()
        data.update({
            'params': json.dumps(self.params) if self.params else ''
        })
        api_logger.info(self.format_message(data))
        return 'Спасибо'
