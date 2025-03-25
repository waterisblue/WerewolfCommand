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
                'game_nos': {
                    'zh-cn': '参与玩家编号有: {nos}'
                },
                'game_no': {
                    'zh-cn': '你的玩家编号是: {no}'
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
                    'zh-cn': '狼人请行动，狼人玩家：{wolfs}\n'
                             '在此期间, 你有{time}秒的时间可以和队友交谈,\n'
                             '你可以通过 c+no 选择你要杀死的玩家:'
                },
                'dawn': {
                    'zh-cn': '天亮了\n'
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
                    'zh-cn': '玩家开始投票'
                },
                'check_check_no': {
                    'zh-cn': '请输入你要查验的玩家编号(c+no)：'
                },
                'member_no_not_found': {
                    'zh-cn': '该玩家不存在或未存活'
                },
                'check_member_role': {
                    'zh-cn': '{no}号玩家的身份是：{role_name}'
                },
                'exile_member': {
                    'zh-cn': '{no}号玩家被放逐'
                },
                'exile_member_equal': {
                    'zh-cn': '投票结果为平票，没有玩家被放逐'
                },
                'exile_member_result': {
                    'zh-cn': '结果：{res}\n'
                },
                'exile_member_stat': {
                    'zh-cn': '{no}号玩家：{v}票\n'
                },
                'exile_input_no': {
                    'zh-cn': '请选择你要投票放逐的玩家编号(c+玩家编号)：'
                },
                'exile_select_no': {
                    'zh-cn': '你投票给了{no}号'
                },
                'good_man': {
                    'zh-cn': '好人'
                },
                'kill_member': {
                    'zh-cn': '你选择了{no}号'
                },
                'night_dead': {
                    'zh-cn': '今晚死亡的是{no}号'
                },
                'night_no_dead': {
                    'zh-cn': '没有人死亡'
                },
                'save_or_poison': {
                    'zh-cn': '你选择（c+s：使用解药，c+p+玩家编号：使用毒药，c+k：跳过）'
                },
                'save_member': {
                    'zh-cn': '你救了{no}号'
                },
                'poison_member': {
                    'zh-cn': '你毒了{no}号'
                },
                'not_enough': {
                    'zh-cn': '你没有{str}'
                },
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