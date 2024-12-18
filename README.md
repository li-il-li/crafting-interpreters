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
- The formalism we used for defining the lexical grammar—the rules for how characters get grouped into tokens—was called a **regular language**.

## Chapter 5

- Regular languages aren’t powerful enough to handle expressions which can nest arbitrarily deeply
- We need a bigger hammer, and that hammer is a **context-free grammar (CFG)**.

| Terminology |  | Lexical grammar | Syntactic grammar |
| :--- | :--- | :--- | :--- |
| The "alphabet" is ... | $\rightarrow$ | Characters | Tokens |
| A "string" is ... | $\rightarrow$ | Lexeme or token | Expression |
| It's implemented by the $\ldots$ | $\rightarrow$ | Scanner | Parser |

- A formal grammar’s job is to specify which strings are valid and which aren’t.
If we were defining a grammar for English sentences, “eggs are tasty for breakfast” would be in the grammar, but “tasty breakfast for are eggs” would probably not.
- Strings created this way are called **derivations** because each is derived from the rules of the grammar.
- Rules are called **productions** because they produce strings in the grammar.
- Each production in a context-free grammar has a **head**—its name—and a **body**, which describes what it generates.
- A **terminal** (expression) is a letter from the grammar’s alphabet. These are called “terminals”, in the sense of an “end point” because they don’t lead to any further “moves” in the game.
- A **nonterminal** (expression) is a named reference to another rule in the grammar.It means “play that rule and insert whatever it produces here”. In this way, the grammar composes.
- Encoded in: Backus-Naur form (BNF)
- The fact that a rule can refer to itself—directly or indirectly—kicks it up even more, letting us pack an infinite number of strings into a finite grammar.

```
breakfast → protein ( "with" breakfast "on the side" )?
          | bread ;

protein   → "really"+ "crispy" "bacon"
          | "sausage"
          | ( "scrambled" | "poached" | "fried" ) "eggs" ;

bread     → "toast" | "biscuits" | "English muffin" ;
```

- Instead of repeating the rule name each time we want to add another production for it, we'll allow a series of productions separated by a pipe (`|`).
- Further, we'll allow parentheses for grouping and then allow | within that to select one from a series of options within the middle of a production.
- We also use a postfix `*` to allow the previous symbol or group to be repeated zero or more times -> recursion.
- A postfix `+` is similar, but requires the preceding production to appear at least once.
- A postfix `?` is for an optional production. The thing before it can appear zero or one time, but not more.

Mini language goal:
```
1 - (2 * 3) < 4 == false
```

Grammar:
```
expression     → literal
               | unary
               | binary
               | grouping ;

literal        → NUMBER | STRING | "true" | "false" | "nil" ;
grouping       → "(" expression ")" ;
unary          → ( "-" | "!" ) expression ;
binary         → expression operator expression ;
operator       → "==" | "!=" | "<" | "<=" | ">" | ">="
               | "+"  | "-"  | "*" | "/" ;
```

-> we CAPITALIZE terminals that are a single lexeme whose text representation may vary. NUMBER is any number literal, and STRING is any string literal. Later, we’ll do the same for IDENTIFIER.

- Literals. Numbers, strings, Booleans, and nil.
- Unary **expressions**. A prefix！to perform a logical not, and - to negate a number.
- Binary **expressions**. The infix arithmetic (+, -, *, /) and logic operators (==, !=, <, <=, >, >=) we know and love.
- Parentheses (grouping **expression**). A pair of ( and ) wrapped around an expression.

Expressions
	•	An expression is a combination of values, variables, operators, and function calls that evaluates to a single value
	•	Expressions always produce or return a value
	•	Examples:
  	▪	5 + 3 (evaluates to 8)
  	▪	x * y
  	▪	isValid()
  	▪	"Hello" + " World"
  	▪	counter++
Statements
	•	A statement is a complete unit of execution that performs some action
	•	Statements don't necessarily produce a value
	•	They typically control program flow or change state
	•	Examples:
  	▪	Assignment statements: x = 5;
  	▪	Control flow statements: if, while, for, switch
  	▪	Declaration statements: let x;
  	▪	Function declarations: function doSomething() { }
  	▪	Return statements: return value;

Each style has a certain “grain” to it.
That’s what the paradigm name literally says—an object-oriented language wants you to *orient* your code along the rows of types.
A functional language instead encourages you to lump each column’s worth of code together into a *function*.

The Visitor pattern is really about approximating the functional style within an OOP language.
-> We can define all of the behavior for a new operation on a set of types in one place, without having to touch the types themselves.
