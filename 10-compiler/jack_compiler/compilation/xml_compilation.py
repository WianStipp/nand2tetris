"""This module contains an XML Compilation Engine."""

from lxml import etree as et

from jack_compiler.compilation import base
from jack_compiler import jack_tokenizer, lexicon

class XMLCompilationEngine(base.CompilationEngine):
  def __init__(self, input_path: str, output_path: str) -> None:
    self.input_path = input_path
    self.output_path = output_path
    self.tokenizer = jack_tokenizer.JackTokenizer(self.input_path)
    self._f = open(self.output_path, "wb")
    self._curr_element = None

  def compile_class(self) -> None:
    assert self.tokenizer.keyword() == lexicon.KeywordTypes.CLASS
    self._curr_element = et.Element("class")
    class_element = et.SubElement(self._curr_element, 'keyword')
    class_element.text = 'class'
    self.tokenizer.advance()
    self._curr_element = et.SubElement(self._curr_element, "text")
    self._curr_element.text = self.tokenizer.identifier()
    self._f.write(ET.tostring(self._curr_element))
    self._f.write(b'\n')
      
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

  def compile_expression(self) -> None:
    """Compiles an expression."""

  def compile_term(self) -> None:
    """Compiles a term. Must do lookahead (LL2)."""

  def compile_expression_list(self) -> None:
    """Compiles a (possibly empty) comma-seperated
    list of expressions."""
