class ErrorReporter:
    had_error = False

    @staticmethod
    def error(line: int, message: str):
        ErrorReporter.__report(line, "", message)

    @staticmethod
    def __report(line: int, where: str, message: str):
        print(f'[line {line}] Error "{where}": {message}')
        ErrorReporter.had_error = True
