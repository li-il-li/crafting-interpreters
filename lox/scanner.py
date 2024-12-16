from typing import Dict, Final, List

from lox.error_reporter import ErrorReporter
from lox.token import Token
from lox.token_type import TokenType


class Scanner:
    __source: str
    __tokens: List[Token]
    __start: int
    __current: int
    __line: int

    keywords: Final[Dict[str, TokenType]] = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source: str) -> None:
        self.__source = source
        self.__tokens = []
        self.__start = 0
        self.__current = 0
        self.__line = 1

    def scan_tokens(self) -> List[Token]:
        while not self.__is_at_end():
            # We are at the beginning of the next lexeme.
            self.__start = self.__current
            self.__scan_token()

        self.__tokens.append(Token(TokenType.EOF, "", None, self.__line))
        return self.__tokens

    def __is_at_end(self) -> bool:
        return self.__current >= len(self.__source)

    def __scan_token(self) -> None:
        char = self.__advance()

        match char:
            case "(":
                self.__add_token(TokenType.LEFT_PAREN)
            case ")":
                self.__add_token(TokenType.RIGHT_PAREN)
            case "{":
                self.__add_token(TokenType.LEFT_BRACE)
            case "}":
                self.__add_token(TokenType.RIGHT_BRACE)
            case ",":
                self.__add_token(TokenType.COMMA)
            case ".":
                self.__add_token(TokenType.DOT)
            case "-":
                self.__add_token(TokenType.MINUS)
            case "+":
                self.__add_token(TokenType.PLUS)
            case ";":
                self.__add_token(TokenType.SEMICOLON)
            case "*":
                self.__add_token(TokenType.STAR)
            case "!":
                self.__add_token(
                    TokenType.BANG_EQUAL
                    if self.__match("=")
                    else TokenType.BANG
                )
            case "=":
                self.__add_token(
                    TokenType.EQUAL_EQUAL
                    if self.__match("=")
                    else TokenType.EQUAL
                )
            case "<":
                self.__add_token(
                    TokenType.LESS_EQUAL
                    if self.__match("=")
                    else TokenType.LESS
                )
            case ">":
                self.__add_token(
                    TokenType.GREATER_EQUAL
                    if self.__match("=")
                    else TokenType.GREATER
                )
            case "/":
                if self.__match("/"):
                    # A comment goes until the end of the line.
                    # and is - obviously - ignored
                    while self.__peek() != "\n" and not self.__is_at_end():
                        self.__advance()
                else:
                    self.__add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                # Ignore whitespace
                pass
            case "\n":
                self.__line += 1
            case '"':
                self.__string()
            case _:
                if self.__is_digit(char):
                    self.__number()
                elif self.__is_alpha(char):
                    self.__identifier()
                else:
                    ErrorReporter.error(self.__line, "Unexptected character.")

    def __advance(self) -> str:
        char = self.__source[self.__current]
        self.__current += 1
        return char

    def __add_token(self, type: TokenType, literal: object = None) -> None:
        text = self.__source[self.__start : self.__current]
        self.__tokens.append(Token(type, text, literal, self.__line))

    def __match(self, expected: str) -> bool:
        if not self.__is_at_end():
            return False
        if self.__source[self.__current] != expected:
            return False

        self.__current += 1
        return True

    def __peek(self) -> str:
        if self.__is_at_end():
            return "\0"
        else:
            return self.__source[self.__current]

    def __string(self) -> None:
        while self.__peek() != '"' and not self.__is_at_end():
            if self.__peek() == "\n":
                self.__line += 1
                self.__advance()

        if self.__is_at_end():
            ErrorReporter.error(self.__line, "Unterminated string.")
            return

        # The closing ".
        self.__advance()

        # Trim the surrounding quotes.
        value = self.__source[self.__start + 1 : self.__current + 1]
        self.__add_token(TokenType.STRING, value)

    def __is_digit(self, char: str) -> bool:
        return char >= "0" and char <= "9"

    def __number(self) -> None:
        # Look at integer part
        while self.__is_digit(self.__peek()):
            self.__advance()

        # Look for a fractional part.
        if self.__peek() == "." and self.__is_digit(self.__peek_next()):
            # Consume the "."
            self.__advance()

            while self.__is_digit(self.__peek()):
                self.__advance()

        self.__add_token(
            TokenType.NUMBER,
            float(self.__source[self.__start : self.__current]),
        )

    def __peek_next(self) -> str:
        """
        Looks ahead 2 characters.
        """
        if self.__current + 1 >= len(self.__source):
            return "\0"
        return self.__source[self.__current + 1]

    def __identifier(self) -> None:
        """
        maximal munch
        """
        while self.__is_alphanumeric(self.__peek()):
            self.__advance()

        text = self.__source[self.__start : self.__current]
        token_type: TokenType = self.keywords.get(text, TokenType.IDENTIFIER)
        self.__add_token(token_type)

    def __is_alpha(self, char: str):
        return (
            (char >= "a" and char <= "z")
            or (char >= "A" and char <= "Z")
            or (char == "_")
        )

    def __is_alphanumeric(self, char: str) -> bool:
        return self.__is_alpha(char) or self.__is_digit(char)
