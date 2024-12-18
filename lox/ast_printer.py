from lox.expr import Binary, Expr, ExprVisitor, Grouping, Literal, Unary


class AstPrinter(ExprVisitor[str]):
    def print(self, expr: Expr) -> str:
        return expr.accept(self)

    # Concrete implementations of all abstract methods
    def visit_binary_expr(self, expr: Binary) -> str:
        return self.__parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_grouping_expr(self, expr: Grouping) -> str:
        return self.__parenthesize("group", expr.expression)

    def visit_literal_expr(self, expr: Literal) -> str:
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: Unary) -> str:
        return self.__parenthesize(expr.operator.lexeme, expr.right)

    def __parenthesize(self, name: str, *exprs: Expr) -> str:
        expr_strings = [expr.accept(self) for expr in exprs]
        return f"({name} {' '.join(expr_strings)})"
