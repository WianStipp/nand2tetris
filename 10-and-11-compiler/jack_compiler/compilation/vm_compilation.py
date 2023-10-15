"""This module contains the VM Compilation Engine which translated Jack to VM Code."""

from jack_compiler.compilation import base
from jack_compiler.compilation import symbol_table

class VMCompilationEngine(base.CompilationEngine):
  def __init__(self, input_path: str, output_path: str) -> None:
    super().__init__(input_path, output_path)

  def compile_class(self) -> None:
    """Compiles a complete class."""
    self.class_sym_table = symbol_table.SymbolTable()
    self.method_sym_table = symbol_table.SymbolTable()

  def compile_class_var_dec(self) -> None:
    """Compiles a static variable or class variable declaration."""

  def compile_subroutine_dec(self) -> None:
    """Compiles a complete method, function or constructor."""

  def compile_parameter_list(self) -> None:
    """Compiles a (possible empty) parameter list. Does not handle
    the enclosing '()'."""

  def compile_subroutine_body(self) -> None:
    """Complies a subroutine's body."""

  def compile_var_dec(self) -> None:
    """Compiles a var declaration."""

  def compile_statements(self) -> None:
    """Compiles a sequence of statements. Does not handle the
    enclosing '{}'."""

  def compile_let(self) -> None:
    """Compiles a let statement."""

  def compile_if(self) -> None:
    """Compiles an if statement."""

  def compile_while(self) -> None:
    """Compiles a while statement."""

  def compile_do(self) -> None:
    """Compile a do statement"""

  def compile_return(self) -> None:
    """Compile a return statement."""

  def compile_subroutine_call(self) -> None:
    """Compile a subroutine call."""


  def compile_expression(self) -> None:
    """Compiles an expression."""

  def compile_term(self) -> None:
    """Compiles a term. Must do lookahead (LL2)."""

  def compile_expression_list(self) -> None:
    """Compiles a (possibly empty) comma-seperated
    list of expressions."""
