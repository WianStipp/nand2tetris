# VMTranslator

Translates from VM code to low-level Jack ASM code.

### How to Use

```bash
$ poetry install
```

On a .vm file, to produce `inputFileName.asm`

```bash
$ poetry run python inputFileName.vm
```

On a directory of .vm files, to produce `pathToDir.asm`

```bash
$ poetry run python pathToDir
```

### Course Tests

Arithmetic Tests:
- [x] SimpleAdd
- [x] StackTest

Memory Access Tests:
- [x] BasicTest
- [x] PointerTest
- [x] StaticTest

Program Flow:
- [X] BasicLoop
- [X] FibonacciSeries

Function Calls:
- [X] SimpleFunction
- [X] NestedCall
- [X] FibonacciElement
- [X] StaticsTest
