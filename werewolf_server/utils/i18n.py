class Language:
    _instance = None
    default_language = 'zh-cn'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Language, cls).__new__(cls)
            cls._instance.translations = {
                'darkness': {
                    'zh-cn': '天黑请闭眼，{user} 请准备好。',
                    'en': 'Darkness falls, {user} get ready.'
                },
                'port_need': {
                    'zh-cn': '请输入端口：'
                },
                'server_starting': {
                    'zh-cn': '服务器已开启： {host}:{port}'
                },
                'game_mode_select': {
                    'zh-cn': f'请选择你要进行的游戏模式\n'
                             f'1. 四人局（预女民狼）\n'
                             f'输入游戏对应的编号：'
                }
            }
            cls._instance.current_language = cls.default_language
        return cls._instance

    def set_language(self, language):
        self.current_language = language

    def get_translation(self, key, **kwargs):
        translation = self.translations.get(key, {}).get(self.current_language, key)
        return translation.format(**kwargs)


language_instance = Language()