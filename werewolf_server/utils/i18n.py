class Language:
    _instance = None
    default_language = 'zh-cn'

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Language, cls).__new__(cls)
            cls._instance.translations = {
                'darkness': {
                    'zh-cn': '天黑请闭眼',
                    'en': 'Darkness falls'
                },
                'port_need': {
                    'zh-cn': '请输入端口：'
                },
                'server_starting': {
                    'zh-cn': '服务器已开启： {host}:{port}'
                },
                'game_mode_select': {
                    'zh-cn': '请选择你要进行的游戏模式\n'
                             '1. 四人局（预女民狼）\n'
                             '输入游戏对应的编号：'
                },
                'game_start': {
                    'zh-cn': '全部玩家已准备，游戏开始'
                },
                'assign_role': {
                    'zh-cn': '你的角色是：{role}'
                },
                'prophet': {
                    'zh-cn': '预言家'
                },
                'witch': {
                    'zh-cn': '女巫',
                },
                'wolf': {
                    'zh-cn': '狼人'
                },
                'civilian': {
                    'zh-cn': '平民'
                },
                'wolf_action': {
                    'zh-cn': '狼人请行动，狼人玩家：{wolfs}'
                },
                'dawn': {
                    'zh-cn': '天亮了'
                },
                'speak': {
                    'zh-cn': '{no}号玩家开始发言，{next}号玩家请准备'
                },
                'speak_last': {
                    'zh-cn': '{no}号玩家开始发言，玩家请准备投票'
                },
                'speak_end': {
                    'zh-cn': '{no}号玩家发言结束'
                },
                'voting': {
                    'zh-cn': '玩家请开始投票'
                }
            }
            cls._instance.current_language = cls.default_language
        return cls._instance

    def set_language(self, language):
        self.current_language = language

    @classmethod
    def get_translation(cls, key, **kwargs):
        translation = cls._instance.translations.get(key, {}).get(cls._instance.current_language, key)
        return translation.format(**kwargs)


language_instance = Language()