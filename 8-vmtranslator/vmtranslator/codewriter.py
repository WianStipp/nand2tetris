"""Generates Hack assembly code from the parsed VM command."""

from typing import List, Union, Literal, Optional
import os

from vmtranslator import vm, hack


PUSHPOP_CMD = Union[Literal[vm.VMCommandTypes.C_PUSH], Literal[vm.VMCommandTypes.C_POP]]


class ASMCodeWriter:
    """
    Class to translate a parsed VM command into ASM.
    """

    def __init__(self, output_file_path: str) -> None:
        self.written_lines: List[str] = []
        self.output = open(output_file_path, "w", encoding="utf-8")
        self._out_filename = os.path.basename(output_file_path).split(".")[0]
        self.i = 0  # hacky solution to make sure goto labels are unique :/
        self._current_func: Optional[str] = None
        # self.init_memory()
        self.write_init()

    def set_file_name(self, filename: str) -> None:
        """Informs that a translation of a new VM file has started."""
        self._input_filename = os.path.basename(filename).split(".")[0]

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
                @{self._out_filename}.{index}
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
                @{self._out_filename}.{index}
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
        fname = f"{self._current_func}${label}" if self._current_func else label
        self._write_lines([f"({fname})"])

    def write_goto(self, label: str) -> None:
        """Writes assembly code that effects the goto command."""
        fname = f"{self._current_func}${label}" if self._current_func else label
        asm = f"""
                @{fname}
                0;JMP
                """
        self._write_lines(code_block_to_lines(asm))

    def write_if(self, label: str) -> None:
        """Writes assembly code that effects the if-goto command."""
        fname = f"{self._current_func}${label}" if self._current_func else label
        asm = f"""
            // D = pop stack
            @SP
            M=M-1
            A=M
            D=M
            // if D>0, jump to label
            @{fname}
            D;JNE
            """
        self._write_lines(code_block_to_lines(asm))

    def write_function(self, function_name: str, num_vars: int) -> None:
        """Writes assembly code that effects the function command."""
        self.write_label(function_name)
        for _ in range(num_vars):
            self.write_push_pop(
                vm.VMCommandTypes.C_PUSH, hack.MemorySegments.CONSTANT, 0
            )
        # self._current_func = function_name

    def write_call(self, function_name: str, num_args: int) -> None:
        """Writes assembly code that effects the call command.
        Args:
            function_name: Name of the function being called.
            num_args: Number of arguments to call the function with.
        Returns:
            None
        """
        self.i += 1
        asm = f"""
                // push returnAddress
                @{function_name}$ret.{self.i}
                D=A 
                @SP
                A=M
                M=D
                @SP
                M=M+1
                // push LCL
                @LCL
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                // push ARG
                @ARG
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                // push THIS
                @THIS
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                // push THAT
                @THAT
                D=M
                @SP
                A=M
                M=D
                @SP
                M=M+1
                // ARG = SP - 5 - nArgs
                @SP
                D=M
                @5
                D=D-A
                @{num_args}
                D=D-A
                @ARG
                M=D
                // LCL = SP
                @SP
                D=M
                @LCL
                M=D
                // goto functionName
                @{function_name}
                0;JMP
                // insert (returnAddress)
                ({function_name}$ret.{self.i})
                """
        self._write_lines(code_block_to_lines(asm))

    def write_return(self) -> None:
        """Writes assembly code that effects the return command."""
        self.i += 1
        asm = f"""
                // endFrame = LCL
                @LCL
                D=M
                @endFrame{self.i}
                M=D
                // retAttr=*(endFrame - 5)
                @5
                D=A
                @endFrame{self.i}
                A=M
                A=A-D
                D=M
                @retAttr{self.i}
                M=D
                // *ARG=pop()
                @SP
                M=M-1
                A=M
                D=M
                @ARG
                A=M
                M=D
                // SP = ARG + 1
                @ARG
                D=M+1
                @SP
                M=D
                // THAT = *(endFrame-1)
                @endFrame{self.i}
                A=M
                A=A-1
                D=M
                @THAT
                M=D
                // THIS = *(endFrame-2)
                @endFrame{self.i}
                A=M
                A=A-1
                A=A-1
                D=M
                @THIS
                M=D
                // ARG = *(endFrame-3)
                @endFrame{self.i}
                A=M
                A=A-1
                A=A-1
                A=A-1
                D=M
                @ARG
                M=D
                // LCL = *(endFrame-4)
                @endFrame{self.i}
                A=M
                A=A-1
                A=A-1
                A=A-1
                A=A-1
                D=M
                @LCL
                M=D
                // goto retAttr
                @retAttr{self.i}
                A=M
                0;JMP
                """
        self._write_lines(code_block_to_lines(asm))
        # self._current_func = None

    def write_init(self) -> None:
        """Write the startup bootstrap code."""
        asm = """
                @256
                D=A
                @SP
                M=D
                """
        self._write_lines(code_block_to_lines(asm))
        self.write_call("Sys.init", 0)

    def _write_lines(self, lines: List[str]) -> None:
        for line in lines:
            if not line or line.startswith("//"):
                continue
            self.output.write(line)
            self.output.write("\n")
            self.written_lines.append(line)

    def close(self) -> None:
        """
        Closes the output file.
        """
        self.output.close()

    def init_memory(self) -> None:
        asm = """
                @SP
                """


def code_block_to_lines(block: str) -> List[str]:
    lines = block.split("\n")
    return [l.strip() for l in lines]
