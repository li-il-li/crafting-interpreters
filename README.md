# Crafting Interpreters

## Mountain Map

Front-end:
1. Character Stream -> Scanning / Lexing -> Tokens
2. Tokens -> Parsing -> Abstract Syntax Tree
3. Static Analysis
  - Binding
  - Type checking
---- Peek of the mountain ----
"Middle-end":
4. Intermediate Representations(IR)
5. IR -> Optimizations -> Optimized IR
Back-end:
6. Optimized IR -> Code generation -> Bytecode for VMs (Assembly for native)
7. Bytecode -> Interpreter / Virtual Machine ->  Assembly (Machine Code)
8. Runtime (eg. GC)

Shortcuts:
- Single-pass compilers
- Tree-walk interpreters
- Transpiler -> source-to-source compiler (Typescript -> Javascript)
- Just-in-time compilation

Compiler vs Interpreter
- Compiling is an *implementation technique* that involves translating source language to some other - usually lower-level - form.
- When we say a language implementation is a **compiler**, we mean it translates source code, but doesn't execute it.
- When we say a language implementation is an **interpreter**, we mean it takes the source code and executes it.
-> CPython is an interpreter, and it has a compiler.

## Lox

- Dynamically typed
- Garbage collected
- Data types:
  - Booleans
  - Numbers
  - Strings
  - Nil
- Arithmetic
  - +
  - - (infix and prefix)
  - *
  - /
- Compariosn
  - <
  - >
  - <=
  - >=
  - ==
- Logical operators
  - !
  - and
  - or
  - No bitwise, shift, modulo, or conditional operators
- Statements
  - Expression produces a *value*
  - Statement produces a *effect*
- Control Flow
  - if ... else ...
  - while() {}
  - for() {}
- Functions
  - fun ...
- Closures
- Classes
  - When it comes to objects, there are actually two approaches to them, classes and prototypes (Javascript).


## Chapter 4
- The rules that determine how a particular language groups characters into lexemes are called its **lexical grammar**.
-
