import asyncio
import logging


async def main():
    logging.basicConfig(
        level=logging.DEBUG,  # 设置根记录器的阈值为 DEBUG
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 日志输出格式
        handlers=[
            logging.StreamHandler(),  # 输出到控制台
            logging.FileHandler('app.log')  # 记录到文件
        ]
    )


if __name__ == '__main__':
    asyncio.run(main())