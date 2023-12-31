import os
from datetime import datetime as dt
from colorama import init, Fore, Back, Style
from os.path import exists

init(True)


class Logger:
    DEBUG = False
    FORMAT = (f"{Fore.LIGHTBLACK_EX}{{date}} {{time}}{Fore.RESET} "
              "[{category}] [{level}"+Fore.RESET+"]: {message}")

    def __init__(self, _log_file_path: str, _debug: bool = False):
        Logger.DEBUG = _debug

        os.makedirs(os.path.dirname(_log_file_path), exist_ok=True)
        opening = 'a+' if exists(_log_file_path) else 'w+'

        self.file = open(_log_file_path, opening, encoding='utf-8')

    @staticmethod
    def removeColors(text: str) -> str:
        output = text

        def scanForColor(text: str) -> tuple[int, str] | None:
            begin = -1

            for i, char in enumerate(text):
                if char == '\033':
                    begin = i

                if char == 'm' and begin != -1:
                    return i, text[:begin]

            return None

        scanResult = scanForColor(output)

        while scanResult is not None:
            end, part = scanResult

            output = part + output[end + 1:]

            scanResult = scanForColor(output)

        return output

    def saveToFile(self, _category: str, _message: str, _level: str) -> None:
        now = dt.now()

        self.file.write(
            Logger.removeColors(
                self.FORMAT.format(
                    date=now.date(),
                    time=now.time(),
                    category=_category,
                    level=_level,
                    message=_message
                )
            ) + '\n'
        )

    def printToShell(self, _category: str, _message: str, _level: str) -> None:
        now = dt.now()

        print(
            self.FORMAT.format(
                date=now.date(),
                time=now.time(),
                category=_category,
                level=_level,
                message=_message
            )
        )

    def log(self, category: str, message: str, shell: bool = True, level: str = Fore.WHITE+'LOG') -> None:
        self.saveToFile(category, message, level)

        if shell:
            self.printToShell(category, message, level)

    def debug(self, category: str, message: str, shell: bool = True):
        if not Logger.DEBUG:
            return

        self.log(category, message, shell, Fore.LIGHTBLUE_EX+'DEBUG')

    def warning(self, category: str, message: str, shell: bool = True):
        self.log(category, message, shell, Fore.LIGHTYELLOW_EX+'WARNING')

    def error(self, category: str, message: str, shell: bool = True):
        self.log(category, message, shell, Fore.LIGHTRED_EX+'ERROR')


if __name__ == '__main__':
    logger = Logger('./test.log')

    logger.log("TEST", "wow this first test.")

    # This message will not be displayed
    logger.debug("TEST", "wow this first test.")

    logger.warning("TEST", "wow this first test.")

    Logger.DEBUG = True

    # This message will be displayed
    logger.debug('DEBUGTEST', 'This message is a debug message.')

    logger.error("FAK", "Shiet, an error occurred !")
