"""Generates Hack assembly code from the parsed VM command."""

from typing import List, Union, Literal
import os

from vmtranslator import vm, hack


PUSHPOP_CMD = Union[Literal[vm.VMCommandTypes.C_PUSH], Literal[vm.VMCommandTypes.C_POP]]


class ASMCodeWriter:
    """
    Class to translate a parsed VM command into ASM.
    """

    def __init__(self, output_file_path: str) -> None:
        self.output = open(output_file_path, "w", encoding="utf-8")
        self._filename = os.path.basename(output_file_path)

    def write_arithmetic(self, command: str) -> None:
        """
        Writes to the output file the assembly code that implements
        the given arithmetic-logical command.
        """

    def write_push_pop(self, command: PUSHPOP_CMD, segment: str, index: int) -> None:
        """
        Writes to the output file the assembly code that implements
        the given push or pop command.
        """
        segment: hack.MemorySegments = hack.MemorySegments(segment)
        if segment == hack.MemorySegments.CONSTANT:
            assert vm.VMCommandTypes.is_push(command)
            asm = f"""
            //D=index
            @{index}
            D=A
            //Push D to SP
            @SP
            A=M
            M=D
            //SP++
            @SP 
            M=M+1"""
        elif segment in [
            hack.MemorySegments.LOCAL,
            hack.MemorySegments.ARGUMENT,
            hack.MemorySegments.THIS,
            hack.MemorySegments.THAT,
        ]:
            segment_pointer = hack.SEGMENT_POINTER_MAP[segment]
            if vm.VMCommandTypes.is_push(command):
                asm = f"""//push {segment_pointer} {index}
                        // {segment_pointer} i -> D
                        @{segment_pointer}
                        A = M
                        A = A + {index}
                        D = M
                        // Put D onto stack
                        @SP
                        A = M
                        M = D
                        // SP++
                        @SP
                        M = M + 1
                        """
            else:
                asm = f"""// pop {segment_pointer} {index}
                    // SP--
                    @SP
                    M = M-1
                    A = M
                    D = M // D=RAM[SP]
                    // RAM[{segment_pointer}+i] = D
                    @{segment_pointer}
                    A = M
                    A = A+{index}
                    M = D
                    """
        elif segment == hack.MemorySegments.STATIC:
            if vm.VMCommandTypes.is_push(command):
                asm = f"""//push static i
                // D = STATIC[i]
                @{self._filename}.{index}
                A = M
                D = M
                // put D onto stack
                @SP
                A = M
                M = D
                // SP++
                @SP
                M = M+1
                """
            else:
                asm = f"""// pop static i
                // SP--
                @SP
                M = M - 1
                A = M
                D = M
                // STATIC[INDEX] = D
                @{self._filename}.{index}
                M = D
                """
        elif segment == hack.MemorySegments.TEMP:
            if vm.VMCommandTypes.is_push(command):
                asm = f"""//push temp i
                @{hack.RAM_POSITION_MAP[segment]}
                A = A+{index}
                D = M
                // RAM[SP] = D
                @SP
                A = M
                M = D
                // SP++
                @SP
                M = M+1
                """
            else:
                asm = f"""//pop temp i
                // SP--
                @SP
                M = M-1
                // D=RAM[SP]
                A = M
                D = M
                // TEMP[i] = D
                @{hack.RAM_POSITION_MAP[segment]}
                A = A+{index}
                M = D
                """
        elif segment == hack.MemorySegments.POINTER:
            assert index == 0 or index == 1
            accessed_segment = hack.THAT_POINTER if index else hack.THAT_POINTER
            if vm.VMCommandTypes.is_push(command):
                asm = f"""// push pointer index
                @{accessed_segment}
                D = M
                @SP
                A = M
                M = D
                // SP++
                @SP
                M = M+1
                """
            else:
                asm = f"""// pop pointer index
                // SP--
                @SP 
                M = M-1
                // D = RAM[SP]
                A = M
                D = M
                @{accessed_segment}
                M = D
                """
        else:
            raise ValueError()
        lines = code_block_to_lines(asm)
        self._write_lines(lines)

    def _write_lines(self, lines: List[str]) -> None:
        for line in lines:
            self.output.write(line)
            self.output.write("\n")

    def close(self) -> None:
        """
        Closes the output file.
        """
        self.output.close()


def code_block_to_lines(block: str) -> List[str]:
    lines = block.split("\n")
    return [l.strip() for l in lines]
