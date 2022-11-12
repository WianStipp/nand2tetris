"""Main entry point for running the VMTranslator from the command line."""

from typing import Optional, List
import os
import argparse

from vmtranslator import codewriter, vmparser, vm


def translate_to_hack(input_path: str, output_file_path: Optional[str] = None) -> None:
    """Translate VM code to Hack code, writing to the output path."""
    input_is_file = os.path.isfile(input_path)
    output_file_path = output_file_path or (
        make_output_path_for_input_file(input_path)
        if input_is_file
        else make_output_path_for_input_dir(input_path)
    )
    vm_file_paths: List[os.PathLike] = (
        [input_path] if input_is_file else list_all_vm_files(input_path)
    )
    print("input file paths:", *vm_file_paths)
    print("output file path:", output_file_path)
    asm_writer = codewriter.ASMCodeWriter(output_file_path)
    for vm_path in vm_file_paths:
        parser = vmparser.VMParser(vm_path)
        asm_writer.set_file_name(vm_path)
        while parser.has_more_lines():
            parser.advance()
            cmd_type = parser.command_type()
            if cmd_is_pushpop_type(cmd_type):
                asm_writer.write_push_pop(cmd_type, parser.arg1(), parser.arg2())
            elif cmd_is_arithmetic_type(cmd_type):
                asm_writer.write_arithmetic(parser.arg1())
            elif cmd_is_label_type(cmd_type):
                asm_writer.write_label(parser.arg1())
            # elif cmd_is_goto_type(cmd_type):
            # asm_writer.write_goto(parser.arg1())
            elif cmd_is_if_type(cmd_type):
                asm_writer.write_if(parser.arg1())
            else:
                raise ValueError(f"command type: {cmd_type} not recognized.")
    asm_writer.close()


def list_all_vm_files(dir_path: str) -> List[str]:
    """Given a directory path, list all the VM files in it."""
    abs_dir_path = os.path.abspath(os.path.dirname(dir_path))
    vm_files = [
        os.path.basename(name) for name in os.listdir(dir_path) if name.endswith("vm")
    ]
    return [os.path.join(abs_dir_path, vmfile) for vmfile in vm_files]


def make_output_path_for_input_dir(input_path: str) -> str:
    filename = f"{os.path.basename(os.path.abspath(input_path))}.asm"
    return os.path.join(os.path.abspath(input_path), filename)


def make_output_path_for_input_file(input_path: str) -> str:
    filename = f"{os.path.basename(input_path).strip('.vm')}.asm"
    return os.path.join(os.path.dirname(os.path.abspath(input_path)), filename)


def cmd_is_pushpop_type(cmd_type: vm.VMCommandTypes) -> bool:
    """Return True if the cmd_type is a pushpop type, else False"""
    is_pushpop_type = (
        cmd_type == vm.VMCommandTypes.C_PUSH or cmd_type == vm.VMCommandTypes.C_POP
    )
    return is_pushpop_type


def cmd_is_arithmetic_type(cmd_type: vm.VMCommandTypes) -> bool:
    """Return True if the cmd_type is a pushpop type, else False"""
    return cmd_type == vm.VMCommandTypes.C_ARITHMETIC


def cmd_is_label_type(cmd_type: vm.VMCommandTypes) -> bool:
    """Return True if the cmd_type is label type, else False"""
    return cmd_type == vm.VMCommandTypes.C_LABEL


def cmd_is_goto_type(cmd_type: vm.VMCommandTypes) -> bool:
    """Return True if the cmd_type is goto type, else False"""
    return cmd_type == vm.VMCommandTypes.C_GOTO


def cmd_is_if_type(cmd_type: vm.VMCommandTypes) -> bool:
    """Return True if the cmd_type is label type, else False"""
    return cmd_type == vm.VMCommandTypes.C_IF


def get_cmdline_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "input_path", help="Either a VM file or a directory of VM files"
    )
    parser.add_argument(
        "--output_file", required=False, help="Where to save the output assembly file"
    )
    return parser.parse_args()


def main() -> None:
    """Run the VM Translator"""
    args = get_cmdline_args()
    translate_to_hack(args.input_path, args.output_file)


if __name__ == "__main__":
    main()
