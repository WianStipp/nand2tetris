"""This module contains the VMWriter class."""

import enum

class Segment(str, enum.Enum):
  CONSTANT = 'constant'
  ARGUMENT = 'argument'
  LOCAL = 'local'
  STATIC = 'static'
  THIS = 'this'
  THAT = 'that'
  POINTER = 'pointer'
  TEMP = 'temp'

class Arithmetic(str, enum.Enum):
  ADD = 'add'
  SUB = 'sub'
  NEG = 'neg'
  EQ = 'eq'
  GT = 'gt'
  LT = 'lt'
  AND = 'and'
  OR = 'or'
  NOT = 'not'

class VMWriter:
  def __init__(self, output_path: str) -> None:
    self.output_path = output_path
  
  def write_push(self, segment: Segment, index: int) -> None:
    """Write a VM push command"""
  
  def write_pop(self, segment: Segment, index: int) -> None:
    """Write a VM push command"""

  def write_arithmetic(self, command: Arithmetic) -> None:
    """Write a VM arithmetic-logical command."""
  
  def write_label(self, label: str) -> None:
    """Write a VM label comamnd."""
  
  def write_goto(self, label: str) -> None:
    """Write a VM goto comamnd."""

  def write_if(self, label: str) -> None:
    """Write a VM if comamnd."""

  def write_call(self, name: str, num_args: int) -> None:
    """Write a VM call comamnd."""

  def write_function(self, name: str, num_vars: int) -> None:
    """Write a VM function comamnd."""
  
  def write_return(self) -> None:
    """Write a VM return command."""
  
  def close(self) -> None:
    """Close the output file / stream"""
