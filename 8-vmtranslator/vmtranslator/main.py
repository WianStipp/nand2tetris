"""Main entry point for running the VMTranslator from the command line."""

from typing import Optional
import argparse

from vmtranslator import codewriter, vmparser, vm


def translate_to_hack(
    input_file_path: str, output_file_path: Optional[str] = None
) -> None:
    """Translate VM code to Hack code, writing to the output path."""
    parser = vmparser.VMParser(input_file_path)
    asm_writer = codewriter.ASMCodeWriter(output_file_path)

    while parser.has_more_lines():
        parser.advance()
        cmd_type = parser.command_type()
        if cmd_is_pushpop_type(cmd_type):
            asm_writer.write_push_pop(cmd_type, parser.arg1(), parser.arg2())
        elif cmd_is_arithmetic_type(cmd_type):
            asm_writer.write_arithmetic(parser.arg1())
        else:
            raise ValueError(f"command type: {cmd_type} not recognized.")
    asm_writer.close()


def cmd_is_pushpop_type(cmd_type: vm.VMCommandTypes) -> bool:
    """Return True if the cmd_type is a pushpop type, else False"""
    is_pushpop_type = (
        cmd_type == vm.VMCommandTypes.C_PUSH or cmd_type == vm.VMCommandTypes.C_POP
    )
    return is_pushpop_type


def cmd_is_arithmetic_type(cmd_type: vm.VMCommandTypes) -> bool:
    """Return True if the cmd_type is a pushpop type, else False"""
    return cmd_type == vm.VMCommandTypes.C_ARITHMETIC


def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("output_file")
    args = parser.parse_args()
    translate_to_hack(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
