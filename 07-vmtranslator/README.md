# VMTranslator

Translates from VM code to low-level Jack ASM code.

### How to Use

```bash
$ poetry install
```

```bash
$ poetry run python inputFileName.vm outputFileName.asm
```


### Course Tests

Arithmetic Tests:
- [x] SimpleAdd
- [x] StackTest

Memory Access Tests:
- [x] BasicTest
- [x] PointerTest
- [x] StaticTest
