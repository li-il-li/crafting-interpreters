from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from lox.token import Token

R = TypeVar('R')

class ExprVisitor(Generic[R], ABC):
    @abstractmethod
    def visit_binary_expr(self, expr: 'Binary') -> R:
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr: 'Grouping') -> R:
        pass

    @abstractmethod
    def visit_literal_expr(self, expr: 'Literal') -> R:
        pass

    @abstractmethod
    def visit_unary_expr(self, expr: 'Unary') -> R:
        pass

class Expr(ABC):
    @abstractmethod
    def accept(self, visitor: 'ExprVisitor[R]') -> R:
        pass

@dataclass
class Binary(Expr):
    left: Expr
    operator: Token
    right: Expr

    def accept(self, visitor: 'ExprVisitor[R]') -> R:
        return visitor.visit_binary_expr(self)

@dataclass
class Grouping(Expr):
    expression: Expr

    def accept(self, visitor: 'ExprVisitor[R]') -> R:
        return visitor.visit_grouping_expr(self)

@dataclass
class Literal(Expr):
    value: Any

    def accept(self, visitor: 'ExprVisitor[R]') -> R:
        return visitor.visit_literal_expr(self)

@dataclass
class Unary(Expr):
    operator: Token
    right: Expr

    def accept(self, visitor: 'ExprVisitor[R]') -> R:
        return visitor.visit_unary_expr(self)
