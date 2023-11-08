import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler
import os


class Logger:
    """Log level
    Level     value  content
    DEBUG     10     細節信息, 僅當診斷問題時適用
    INFO      20     確認程序按預期進行
    WARNING   30     表明有已經或即將發生的意外, 但程序仍按預計進行
    ERROR     40     由於嚴重問題, 程序的某些功能已經不能正常運行
    CRITICAL  50     嚴重的錯誤, 表明程序已不能繼執行
    """

    def __init__(
        self,
        loggerName="main",
        level=logging.DEBUG,
    ):
        self.logger = logging.getLogger(loggerName)
        self.logger.setLevel(level)
        self.handlerList = list()

    def create_file_handler(
        self,
        logFolderPath,
        logfileName,
        maxMB,
        backupCount,
        level=logging.INFO,
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ):
        """建立fileLogger

        Args:
            filePath (_type_): _description_
            maxMB (_type_): _description_
            backupCount (_type_): _description_
            level (_type_, optional): _description_. Defaults to logging.warning.
            fmt (str, optional): _description_. Defaults to "%(asctime)s - %(name)s - %(levelname)s - %(message)s".
            datefmt (str, optional): _description_. Defaults to "%Y-%m-%d %H:%M:%S".
        """
        ### 建立檔案路徑
        os.makedirs(logFolderPath, exist_ok=True)

        ### 建立 fileHandler
        fileHandler = RotatingFileHandler(
            filename=os.path.join(logFolderPath, logfileName),
            maxBytes=maxMB * 1024 * 1024,
            backupCount=backupCount,
            encoding="utf-8",  # utf-8 才能寫中文
        )
        fileHandler.setLevel(level)

        ### 定義輸出格式
        formatter = logging.Formatter(fmt, datefmt)
        fileHandler.setFormatter(formatter)

        self.logger.addHandler(fileHandler)

        self.logger.info(" ")
        self.logger.info("=" * 100)

    def create_stream_handler(
        self,
        level=logging.DEBUG,
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ):
        """建立streamHandler

        Args:
            level (_type_, optional): _description_. Defaults to logging.info.
            fmt (str, optional): _description_. Defaults to "%(asctime)s - %(name)s - %(levelname)s - %(message)s".
            datefmt (str, optional): _description_. Defaults to "%Y-%m-%d %H:%M:%S".
        """
        ### 建立 fileHandler
        streamHandler = StreamHandler()
        streamHandler.setLevel(level)

        ### 定義輸出格式
        formatter = logging.Formatter(fmt, datefmt)
        streamHandler.setFormatter(formatter)

        self.logger.addHandler(streamHandler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def reover_all_handler(self):
        """刪除所有 handler"""
        for handler in self.handlerList:
            self.logger.removeHandler(handler)


if __name__ == "__main__":
    logger = Logger()
    logger.create_file_handler(
        logFolderPath="./data/logs",
        logfileName="system_log.log",
        maxMB=10,
        backupCount=1,
    )
    logger.create_stream_handler()
    logger.warning("test123")
