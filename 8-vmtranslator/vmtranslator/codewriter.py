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
        self._filename = os.path.basename(output_file_path).split(".")[0]
        self.i = 0

    def set_file_name(self, filename: str) -> None:
        """Informs that a translation of a new VM file has started."""

    def write_arithmetic(self, command: str) -> None:
        """
        Writes to the output file the assembly code that implements
        the given arithmetic-logical command.
        """
        self.i += 1
        command = vm.ArithmeticCommands(command)
        if command == vm.ArithmeticCommands.ADD:
            asm = """//add
                    // SP--
                    @SP
                    M=M-1
                    // D = RAM[SP]
                    A=M
                    D=M
                    // M = D + RAM[SP-1]
                    A=A-1
                    M=D+M
                    """
        elif command == vm.ArithmeticCommands.SUB:
            asm = """//sub
                    // SP--
                    @SP
                    M=M-1
                    // D = RAM[SP]
                    A=M
                    D=M
                    // M = RAM[SP-1] - D
                    A=A-1
                    M=M-D
                    """
        elif command == vm.ArithmeticCommands.NEG:
            asm = """//neg
                    @SP
                    A=M
                    A=A-1
                    M=-M
                    """
        elif command == vm.ArithmeticCommands.EQ:
            asm = f"""//eq
                    @SP
                    M=M-1
                    A=M
                    D=M
                    A=A-1
                    // D==0 if EQ, else not
                    D=M-D
                    // RAM[SP] = 0 (false)
                    M=0
                    // if D==0, JUMP to ZERO
                    @ZERO{self.i}
                    D;JEQ

                    // jump to END
                    @END{self.i}
                    0;JMP

                    (ZERO{self.i})
                    // RAM[SP-1] = 1
                    @SP
                    A=M
                    A=A-1
                    M=-1

                    (END{self.i})
                    """

        elif command == vm.ArithmeticCommands.GT:
            asm = f"""//eq
                    @SP
                    M=M-1
                    A=M
                    D=M
                    A=A-1
                    // D>0 if GT, else not
                    D=M-D
                    // RAM[SP] = 0 (false)
                    M=0
                    // if D>0, JUMP to POSITIVE
                    @POSITIVE{self.i}
                    D;JGT

                    // jump to END
                    @END{self.i}
                    0;JMP

                    (POSITIVE{self.i})
                    // RAM[SP-1] = 1
                    @SP
                    A=M
                    A=A-1
                    M=-1

                    (END{self.i})
                    """
        elif command == vm.ArithmeticCommands.LT:
            asm = f"""//eq
                    @SP
                    M=M-1
                    A=M
                    D=M
                    A=A-1
                    // D<0 if LT, else not
                    D=M-D
                    // RAM[SP] = 0 (false)
                    M=0
                    // if D>0, JUMP to NEGATIVE
                    @NEGATIVE{self.i}
                    D;JLT

                    // jump to END
                    @END{self.i}
                    0;JMP

                    (NEGATIVE{self.i})
                    // RAM[SP-1] = 1
                    @SP
                    A=M
                    A=A-1
                    M=-1

                    (END{self.i})
                    """
        elif command == vm.ArithmeticCommands.AND:
            asm = """//and
                    // SP--
                    @SP
                    M=M-1
                    // D = RAM[SP]
                    A=M
                    D=M
                    // M = RAM[SP-1] - D
                    A=A-1
                    M=M&D
                    """

        elif command == vm.ArithmeticCommands.OR:
            asm = """//or
                    // SP--
                    @SP
                    M=M-1
                    // D = RAM[SP]
                    A=M
                    D=M
                    // M = RAM[SP-1] - D
                    A=A-1
                    M=M|D
                    """
        elif command == vm.ArithmeticCommands.NOT:
            asm = """//not
                    @SP
                    A=M
                    A=A-1
                    M=!M
                    """
        else:
            raise ValueError()
        lines = code_block_to_lines(asm)
        self._write_lines(lines)

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
                        @{index}
                        D=A
                        @{segment_pointer}
                        D=M+D
                        A=D
                        D=M
                        @SP
                        A=M
                        M=D
                        @SP
                        M=M+1
                        """
            else:
                asm = f"""//pop {segment_pointer} {index}
                        @{index}
                        D=A
                        @{segment_pointer}
                        D=M+D
                        @R13
                        M=D
                        @SP
                        M=M-1
                        A=M
                        D=M
                        @R13
                        A=M
                        M=D
                        """
        elif segment == hack.MemorySegments.STATIC:
            if vm.VMCommandTypes.is_push(command):
                asm = f"""//push static i
                // D = STATIC[i]
                @{self._filename}.{index}
                D=M
                // put D onto stack
                @SP
                A=M
                M=D
                // SP++
                @SP
                M=M+1
                """
            else:
                asm = f"""// pop static i
                // SP--
                @SP
                M=M-1
                A=M
                D=M
                // STATIC[INDEX] = D
                @{self._filename}.{index}
                M=D
                """
        elif segment == hack.MemorySegments.TEMP:
            if vm.VMCommandTypes.is_push(command):
                asm = f"""//push temp i
                @{index}
                D=A
                @{hack.RAM_POSITION_MAP[segment]}
                A=A+D
                D=M
                // RAM[SP] = D
                @SP
                A=M
                M=D
                // SP++
                @SP
                M=M+1
                """
            else:
                asm = f"""//pop temp i
                // SP--
                @{index}
                D=A
                @{hack.RAM_POSITION_MAP[segment]}
                D=A+D
                // store addr in RAM13
                @R13
                M=D
                @SP
                M=M-1
                A=M
                D=M
                @R13
                A=M
                M=D
                """
        elif segment == hack.MemorySegments.POINTER:
            assert index == 0 or index == 1
            accessed_segment = hack.THAT_POINTER if index else hack.THIS_POINTER
            if vm.VMCommandTypes.is_push(command):
                asm = f"""// push pointer index
                @{accessed_segment}
                D=M
                @SP
                A=M
                M=D
                // SP++
                @SP
                M=M+1
                """
            else:
                asm = f"""// pop pointer index
                // SP--
                @SP 
                M=M-1
                // D = RAM[SP]
                A=M
                D=M
                @{accessed_segment}
                M=D
                """
        else:
            raise ValueError()
        lines = code_block_to_lines(asm)
        self._write_lines(lines)

    def write_label(self, label: str) -> None:
        """Writes assembly code that effects the label command."""

    def write_goto(self, label: str) -> None:
        """Writes assembly code that effects the goto command."""

    def write_if(self, label: str) -> None:
        """Writes assembly code that effects the if-goto command."""

    def write_function(self, function_name: str, num_vars: int) -> None:
        """Writes assembly code that effects the function command."""

    def write_call(self, function_name: str, num_args: int) -> None:
        """Writes assembly code that effects the call coammnd."""

    def write_return(self) -> None:
        """Writes assembly code that effects the return command."""

    def _write_lines(self, lines: List[str]) -> None:
        for line in lines:
            if not line or line.startswith("//"):
                continue
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
