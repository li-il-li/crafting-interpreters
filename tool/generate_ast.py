import sys
from typing import Sequence


def define_visitor(file, base_name: str, types: Sequence[str]) -> None:
    """Define the visitor interface"""
    file.write(f"class {base_name}Visitor(Generic[R], ABC):\n")

    # Extract class names for visitor methods
    for type_def in types:
        class_name = type_def.split(":", 1)[0].strip()
        file.write("    @abstractmethod\n")
        file.write(
            f"    def visit_{class_name.lower()}_expr(self, expr: '{class_name}') -> R:\n"
        )
        file.write("        pass\n\n")


def define_ast(output_dir: str, base_name: str, types: tuple[str, ...]) -> None:
    with open(
        f"{output_dir}/{base_name.lower()}.py", "w", encoding="utf-8"
    ) as file:
        # Write imports
        file.write(
            "from dataclasses import dataclass\n"
            "from typing import Any, TypeVar, Generic\n"
            "from abc import ABC, abstractmethod\n\n"
            "from lox.token import Token\n\n\n"
        )

        # Define type variable for visitor
        file.write("R = TypeVar('R')\n\n")

        # Define visitor interface
        define_visitor(file, base_name, types)

        # Define base expression class
        file.write(f"class {base_name}(ABC):\n")
        file.write("    @abstractmethod\n")
        file.write(
            f"    def accept(self, visitor: '{base_name}Visitor[R]') -> R:\n"
        )
        file.write("        pass\n\n")

        # Generate subclasses
        for type_def in types:
            class_name, fields = type_def.split(":", 1)
            class_name = class_name.strip()

            # Class definition
            file.write(f"@dataclass\nclass {class_name}({base_name}):\n")

            # Write fields
            if fields.strip():
                for field in fields.strip().split(","):
                    type_name, var_name = field.strip().split()
                    file.write(f"    {var_name}: {type_name}\n")
            else:
                file.write("    pass\n")

            # Write accept method
            file.write(
                f"\n    def accept(self, visitor: '{base_name}Visitor[R]') -> R:\n"
            )
            file.write(
                f"        return visitor.visit_{class_name.lower()}_expr(self)\n"
            )
            file.write("\n")


if __name__ == "__main__":
    define_ast(
        sys.argv[1],
        "Expr",
        (
            "Binary   : Expr left, Token operator, Expr right",
            "Grouping : Expr expression",
            "Literal  : Any value",
            "Unary    : Token operator, Expr right",
        ),
    )
