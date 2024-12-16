from lox.error_reporter import ErrorReporter
from lox.scanner import Scanner


class Lox:
    @property
    def had_error(self):
        return ErrorReporter.had_error

    @staticmethod
    def run_file(path):
        with open(path, "r") as file:
            content = file.read()
        Lox.__run(content)

    @staticmethod
    def run_prompt():
        while True:
            try:
                print("> ", end="", flush=True)
                line = input()
                if not line:
                    break
                Lox.__run(line)
            except EOFError:
                break

    @staticmethod
    def __run(source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token)
