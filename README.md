# SNOL Interpreter

A modular interpreter for the **Simple Number-Only Language (SNOL)** — a case-sensitive, minimalistic language that supports only integer and real number operations. Designed as a structured programming project to demonstrate key compiler/interpreter components.

---

## 📌 Objective

To implement a functioning interpreter for SNOL by breaking down the system into independent, structured components (lexer, parser, evaluator, etc.) and coordinating them in a clean control loop.

---

## 🧠 Language Overview (SNOL)

SNOL supports:

- Integer and floating-point literals
- Arithmetic operations (`+`, `-`, `*`, `/`, `%`)
- Variable assignment and type inference
- Input (`BEG var`) and output (`PRINT var`)
- Exit command (`EXIT!`) to terminate the interpreter

## 🔤 Sample Commands

```bash
num = 0
PRINT num         # Output: [num] = 0
BEG value         # Prompts user for input
value + 5         # Arithmetic expression
EXIT!             # Terminates interpreter
```

## ✅ Features

- Validates variable definitions and usage
- Supports basic error handling:
  - Undefined variables
  - Type mismatches
  - Invalid command syntax
  - Unknown or invalid tokens
- Input validation (ensures correct numeric format)
- Mimics command-line REPL interface

## 🧱 Modular Structure
- **main.py:**
  - Interpreter Control Loop: Entry point. Reads user input, coordinates all modules, and manages the REPL and EXIT! command.
- **tokenizer.py:**
  - Tokenizer: Converts raw input into a list of tokens (keywords, literals, operators). Enforces syntax and token rules.
  - Syntax Validator: Parses token lists to recognize SNOL grammar. Returns structured data or errors.
- **symbol_table.py:**
  - Variable Manager: Stores variables with types (int/float). Handles assignments, lookups, and reassignments.
- **evaluator.py:**
  - Arithmetic Evaluator: Computes results from parsed expressions using correct precedence and type checks.
- **io_handler.py:**
  - I/O Manager: Handles BEG var for input and PRINT commands for output formatting and variable lookups.


## 🧑‍🤝‍🧑 Member	Feature Area	Responsibility
- **Lexical Analyzer**
  - Built the tokenizer (lexer.py) to clean and break input into valid tokens.
- **Syntax Validator**
  - Designed the parser to understand and structure SNOL commands (parser.py).
- **Symbol Table Manager**
  - Developed the variable tracking system (symbol_table.py) with type inference.
- **Expression Evaluator**
  - Handled arithmetic computations with error handling (evaluator.py).
- **I/O + REPL Loop**
  - Created the main control loop and I/O management (main.py, io_handler.py).

## 🚀 How to Run
(To be followed)

## 📂 Project Structure

```bash
Project_SNOL/
├── main.py              # REPL loop and coordinator
├── lexer.py             # Tokenizer
├── parser.py            # Syntax analyzer
├── symbol_table.py      # Variable manager
├── evaluator.py         # Arithmetic processor
├── io_handler.py        # Input/output handlers
├── README.md            # Project documentation
```

## Git Workflow
1. Checkout a Branch
To checkout a branch, follow these steps:

List branches: To see all available branches, run:

```bash
Checkout a branch: To switch to an existing branch, run:
git checkout <branch-name>
```

2. Committing Changes
```bash
git add <specific file>
or
git add .
```
Commit Message Format
Please use:

 ```bash
git commit -m "<feature>(<assignedFeature>): <short-description>"
or
git commit -m "<fix>(<assignedFeature>): <short-description>"
```

Push your changes to your feature branch
```bash
git push origin feature/branchname
```













