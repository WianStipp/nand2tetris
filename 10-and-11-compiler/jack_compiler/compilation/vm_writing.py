"""This module contains the VMWriter class."""

import abc
import enum

from jack_compiler import lexicon

class VMSegment(str, enum.Enum):
  CONSTANT = 'constant'
  ARGUMENT = 'argument'
  LOCAL = 'local'
  STATIC = 'static'
  THIS = 'this'
  THAT = 'that'
  POINTER = 'pointer'
  TEMP = 'temp'

class VMArithmetic(str, enum.Enum):
  ADD = 'add'
  SUB = 'sub'
  NEG = 'neg'
  EQ = 'eq'
  GT = 'gt'
  LT = 'lt'
  AND = 'and'
  OR = 'or'
  NOT = 'not'

class OutputWriter(abc.ABC):
  @abc.abstractmethod
  def write(self, cmd: str) -> None:
    ...

  @abc.abstractmethod
  def close(self) -> None:
    ...

class FileWriter(OutputWriter):
  def __init__(self, output_path: str) -> None:
    self.output_path = output_path

  def write(self, cmd: str) -> None:
    with open(self.output_path, 'a') as f:
      f.write(cmd)
    
  def close(self) -> None:
    ...

class StdOutWriter(OutputWriter):
  """Useful for debugging"""
  def write(self, cmd: str) -> None:
    print(cmd)

  def close(self) -> None:
    ...

class VMWriter:
  def __init__(self, output_writer: OutputWriter) -> None:
    self.output_writer = output_writer
  
  def write_push(self, segment: VMSegment, index: int) -> None:
    """Write a VM push command"""
    cmd = f"push {segment.value} {index}"
    self.output_writer.write(cmd)
  
  def write_pop(self, segment: VMSegment, index: int) -> None:
    """Write a VM push command"""
    cmd = f"pop {segment.value} {index}"
    self.output_writer.write(cmd)

  def write_arithmetic(self, command: lexicon.Symbols) -> None:
    """Write a VM arithmetic-logical command."""
    if command == lexicon.Symbols.PLUS:
      cmd = VMArithmetic.ADD
    elif command == lexicon.Symbols.MINUS:
      cmd = VMArithmetic.SUB
    elif command == lexicon.Symbols.LT:
      cmd = VMArithmetic.LT
    elif command == lexicon.Symbols.GT:
      cmd = VMArithmetic.GT
    elif command == lexicon.Symbols.ASTERISK:
      cmd = VMArithmetic.NOT
    else: raise ValueError(command)
    self.output_writer.write(cmd.value)
  
  def write_label(self, label: str) -> None:
    """Write a VM label comamnd."""
    cmd = f"label {label}"
    self.output_writer.write(cmd)
  
  def write_goto(self, label: str) -> None:
    """Write a VM goto comamnd."""
    cmd = f"goto {label}"
    self.output_writer.write(cmd)

  def write_if(self, label: str) -> None:
    """Write a VM if comamnd."""
    cmd = f"if-goto {label}"
    self.output_writer.write(cmd)

  def write_call(self, name: str, num_args: int) -> None:
    """Write a VM call comamnd."""
    cmd = f"call {name} {num_args}"
    self.output_writer.write(cmd)

  def write_function(self, name: str, num_vars: int) -> None:
    """Write a VM function comamnd."""
    cmd = f"function {name} {num_vars}"
    self.output_writer.write(cmd)
  
  def write_return(self) -> None:
    """Write a VM return command."""
    self.output_writer.write("return")
  
  def close(self) -> None:
    """Close the output file / stream"""
    self.output_writer.close()
