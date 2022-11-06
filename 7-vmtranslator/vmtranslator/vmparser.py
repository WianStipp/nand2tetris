"""Defines the Parser class to parse VM code."""

from typing import Union
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

PUSHPOP_CMD = Union[VMCommandTypes.C_PUSH, VMCommandTypes.C_POP]

class VMParser:
  """
  Parses VM code.
  """
  def __init__(self, input_file_path: str) -> None:
    self.input_file_path = input_file_path
    self._current_command = None
  
  def has_more_lines(self) -> bool:
    """Are there more lines in the input?"""
  
  def advance(self) -> None:
    """
    Reads the next command from the current input and
    makes it the current command.
    """
  
  def command_type(self) -> VMCommandTypes:
    """
    Returns a constant representing the type of the
    current command.
    """

  def arg1(self) -> str:
    """
    Returns the first argument of the current command.
    """
  
  def arg2(self) -> str:
    """
    Returns the second argument of the current command.
    """
