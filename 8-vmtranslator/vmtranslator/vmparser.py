"""Defines the Parser class to parse VM code."""

from typing import List, Optional

from vmtranslator import vm

CMD_TO_TYPE_MAP = {
    "push": vm.VMCommandTypes.C_PUSH,
    "pop": vm.VMCommandTypes.C_POP,
    "label": vm.VMCommandTypes.C_LABEL,
    "goto": vm.VMCommandTypes.C_GOTO,
    "if-goto": vm.VMCommandTypes.C_IF,
    **{m.value: vm.VMCommandTypes.C_ARITHMETIC for m in vm.ArithmeticCommands},
}


class VMParser:
    """
    Parses VM code.
    """

    def __init__(self, input_file_path: str) -> None:
        self.input_file_path = input_file_path
        self.file_lines = self._read_file_lines()
        self._line_pointer: Optional[int] = None
        self._current_line: Optional[str] = None

    def has_more_lines(self) -> bool:
        """Are there more lines in the input?"""
        if self._line_pointer is None:
            lp = -1
        else:
            lp = self._line_pointer
        return bool(self.file_lines[lp + 1 :])

    def advance(self) -> None:
        """
        Reads the next command from the current input and
        makes it the current command.
        """
        if self._line_pointer is None:
            self._line_pointer = -1
        self._line_pointer += 1
        self._current_line = self.file_lines[self._line_pointer]

    def command_type(self) -> vm.VMCommandTypes:
        """
        Returns a constant representing the type of the
        current command.
        """
        line_cmd, *_ = self._current_line.split()
        return CMD_TO_TYPE_MAP[line_cmd]

    def arg1(self) -> str:
        """
        Returns the first argument of the current command.

        In the case of C_ARITHMETIC, return the command itself.
        """
        if self.command_type() == vm.VMCommandTypes.C_ARITHMETIC:
            return self._current_line
        _, arg1, *_ = self._current_line.split()
        return arg1

    def arg2(self) -> int:
        """
        Returns the second argument of the current command.
        """
        _, _, arg2 = self._current_line.split()
        return int(arg2)

    def _read_file_lines(self) -> List[str]:
        with open(self.input_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        lines = [l.strip("\n") for l in lines if not l.startswith("//")]
        lines = [l.split("//")[0].strip() for l in lines]
        return [l for l in lines if l]
