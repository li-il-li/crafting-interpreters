# Create lexemes
from dataclasses import dataclass

from lox.token_type import TokenType


@dataclass(frozen=True)
class Token:
    """
    token = Token(type=some_token_type, lexeme="example", literal=None, line=1)
    """

    type: TokenType
    lexeme: str
    literal: object
    line: int

    def __str__(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal}"
