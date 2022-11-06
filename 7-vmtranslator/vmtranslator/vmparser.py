"""Defines the Parser class to parse VM code."""

from typing import Union, List, Optional, Literal
import enum


class VMCommandTypes(enum.Enum):
    """
    Defines the VM command types.
    """

    C_ARITHMETIC = "C_ARITHMETIC"
    C_PUSH = "C_PUSH"
    C_POP = "C_POP"
    C_LABEL = "C_LABEL"
    C_GOTO = "C_GOTO"
    C_IF = "C_IF"
    C_FUNCTION = "C_FUNCTION"
    C_RETURN = "C_RETURN"
    C_CALL = "C_CALL"


CMD_TO_TYPE_MAP = {
    "push": VMCommandTypes.C_PUSH,
    "pop": VMCommandTypes.C_POP,
    "add": VMCommandTypes.C_ARITHMETIC,
    "sub": VMCommandTypes.C_ARITHMETIC,
    "neg": VMCommandTypes.C_ARITHMETIC,
    "eq": VMCommandTypes.C_ARITHMETIC,
    "gt": VMCommandTypes.C_ARITHMETIC,
    "lt": VMCommandTypes.C_ARITHMETIC,
    "and": VMCommandTypes.C_ARITHMETIC,
    "or": VMCommandTypes.C_ARITHMETIC,
    "not": VMCommandTypes.C_ARITHMETIC,
}

PUSHPOP_CMD = Union[Literal[VMCommandTypes.C_PUSH], Literal[VMCommandTypes.C_POP]]


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

    def command_type(self) -> VMCommandTypes:
        """
        Returns a constant representing the type of the
        current command.
        """
        for cmd, type_ in CMD_TO_TYPE_MAP.items():
            line_cmd, *_ = self._current_line.split()
            if cmd in line_cmd:
                return type_
        raise ValueError(f"Unspecified command in line {self._current_line}")

    def arg1(self) -> str:
        """
        Returns the first argument of the current command.
        """
        _, arg1, _ = self._current_line.split()
        return arg1

    def arg2(self) -> str:
        """
        Returns the second argument of the current command.
        """
        _, _, arg2 = self._current_line.split()
        return arg2

    def _read_file_lines(self) -> List[str]:
        with open(self.input_file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        return [l.strip("\n") for l in lines]
