import json


class Language:
    _instance = None
    default_language = 'zh-cn'

    def __init__(self):
        self.set_language(self.default_language)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Language, cls).__new__(cls)
            cls._instance.current_language = cls.default_language
        return cls._instance

    def set_language(self, language):
        with open(f'static/i18n/{language}.json', 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
            self.translations = data

    @classmethod
    def get_translation(cls, key, **kwargs):
        translation = cls._instance.translations.get(key, key)
        return translation.format(**kwargs)


language_instance = Language()