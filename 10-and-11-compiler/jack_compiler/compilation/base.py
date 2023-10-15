"""This module contains the ABC for the compilation engine."""

import abc

from jack_compiler import jack_tokenizer


class CompilationEngine(abc.ABC):
  """
  Abstract interface for a CompilationEngine that reads from the input path
  and writes to the output path.
  """
  def __init__(self, input_path: str, output_path: str) -> None:
    self.input_path = input_path
    self.output_path = output_path
    self.tokenizer = jack_tokenizer.JackTokenizer(self.input_path)

  @abc.abstractmethod
  def compile_class(self) -> None:
    """Compiles a complete class."""

  @abc.abstractmethod
  def compile_class_var_dec(self) -> None:
    """Compiles a static variable or class variable declaration."""

  @abc.abstractmethod
  def compile_subroutine_dec(self) -> None:
    """Compiles a complete method, function or constructor."""

  @abc.abstractmethod
  def compile_parameter_list(self) -> None:
    """Compiles a (possible empty) parameter list. Does not handle
    the enclosing '()'."""

  @abc.abstractmethod
  def compile_subroutine_body(self) -> None:
    """Complies a subroutine's body."""

  @abc.abstractmethod
  def compile_var_dec(self) -> None:
    """Compiles a var declaration."""

  @abc.abstractmethod
  def compile_statements(self) -> None:
    """Compiles a sequence of statements. Does not handle the
    enclosing '{}'."""

  @abc.abstractmethod
  def compile_let(self) -> None:
    """Compiles a let statement."""

  @abc.abstractmethod
  def compile_if(self) -> None:
    """Compiles an if statement."""

  @abc.abstractmethod
  def compile_while(self) -> None:
    """Compiles a while statement."""

  @abc.abstractmethod
  def compile_do(self) -> None:
    """Compile a do statement"""

  @abc.abstractmethod
  def compile_return(self) -> None:
    """Compile a return statement."""

  @abc.abstractmethod
  def compile_subroutine_call(self) -> None:
    """Compile a subroutine call."""


  @abc.abstractmethod
  def compile_expression(self) -> None:
    """Compiles an expression."""

  @abc.abstractmethod
  def compile_term(self) -> None:
    """Compiles a term. Must do lookahead (LL2)."""

  @abc.abstractmethod
  def compile_expression_list(self) -> None:
    """Compiles a (possibly empty) comma-seperated
    list of expressions."""
