## 开发环境要求

- Python 3.11 及以上版本
- 终端或命令行界面

## 安装

1. 克隆项目到本地：
   ```bash
   git clone https://github.com/waterisblue/WerewolfCommand.git
   ```

2. 进入项目目录：
   ```bash
   cd WerewolfCommand
   ```

3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
   
## 程序结构

### werewolf_server

程序的服务端，进行所有的程序逻辑计算。

- game 存放游戏模式，其中base_game是游戏模式可以选择继承的基类（推荐）。
- model 存放需要的数据模型，例如参与成员。
- role 存放游戏角色，例如：女巫、预言家等，base_role是可以选择继承的基类（推荐）。
- static 存放静态文件，目前主要存放i18n信息。
- util 工具包

### werewolf_client

存放客户端文件，主要用于和服务端通信和约定消息类型。

### werewolf_common

存放客户端与服务端的通用文件，例如通信消息格式。

### werewolf_test

用于程序测试。

## 快速开始

- 参考`werewolf_common/model/message.py`参考消息传输格式。
- 参考`werewolf_server/game/base_game.py`和某一对应实现基类(`werewolf_server/game/game_default_4_member.py`)以了解游戏角色开发过程。
- 参考`werewolf_server/role/base_role.py`和某一对应实现基类以了解游戏角色开发过程。


