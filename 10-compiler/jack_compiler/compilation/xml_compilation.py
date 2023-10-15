"""This module contains an XML Compilation Engine."""

from lxml import etree as et
import xml.etree.ElementTree as ET

from jack_compiler.compilation import base
from jack_compiler import jack_tokenizer, lexicon

parser = et.XMLParser(remove_blank_text=True)

class XMLCompilationEngine(base.CompilationEngine):
  def __init__(self, input_path: str, output_path: str) -> None:
    self.input_path = input_path
    self.output_path = output_path
    self.tokenizer = jack_tokenizer.JackTokenizer(self.input_path)
    self.tokenizer.advance()
    self._f = open(self.output_path, "wb")
    self._parent_element = None

  def compile_class(self) -> None:
    assert self.tokenizer.keyword() == lexicon.KeywordTypes.CLASS
    self.root = et.Element("class")
    class_element = et.SubElement(self.root, 'keyword')
    class_element.text = ' class '
    self.tokenizer.advance()
    classname_id = et.SubElement(self.root, 'identifier')
    classname_id.text = f" {self.tokenizer.identifier()} "
    self.tokenizer.advance()
    assert (v := self.tokenizer.symbol().value) == '{'
    open_body = et.SubElement(self.root, 'symbol'); open_body.text = f" {v} "
    self._parent_element = open_body
    self.tokenizer.advance()

    while self.tokenizer.token_type() != lexicon.TokenType.SYMBOL:
      keyword = self.tokenizer.keyword()
      # is a class var dec
      if keyword in {lexicon.KeywordTypes.STATIC, lexicon.KeywordTypes.FIELD}:
        self.compile_class_var_dec()
      # is subroutine dec
      elif keyword in {lexicon.KeywordTypes.CONSTRUCTOR, lexicon.KeywordTypes.FUNCTION, lexicon.KeywordTypes.METHOD}:
        self.compile_subroutine_dec()
      else: raise ValueError(f"Should have been a classvardec or a subroutinedec, got {keyword}")

    assert (v := self.tokenizer.symbol().value) == '}'
    close_body = et.SubElement(self.root, 'symbol'); close_body.text = f" {v} "
    print_tree(self.root)
      
  def compile_class_var_dec(self) -> None:
    """Compiles a static variable or class variable declaration."""
    classvardec = et.SubElement(self._parent_element, "classVarDec")
    keyword = et.SubElement(classvardec, 'keyword')
    keyword.text = f" {self.tokenizer.keyword().value} "
    self.tokenizer.advance()
    if self.tokenizer.token_type() == lexicon.TokenType.KEYWORD:
      type_identifier = et.SubElement(classvardec, 'keyword')
      type_identifier.text = f" {self.tokenizer.keyword().value} "
    elif self.tokenizer.token_type() == lexicon.TokenType.IDENTIFIER:
      classname = et.SubElement(classvardec, 'identifier')
      classname.text = f" {self.tokenizer.identifier()} "
    else: raise ValueError(f"Expected type declaration or classname, but got {self.tokenizer.token_type()}")
    self.tokenizer.advance()
    varname = et.SubElement(classvardec, 'identifier')
    varname.text = f" {self.tokenizer.identifier()} "
    self.tokenizer.advance()
    while self.tokenizer.symbol() != lexicon.Symbols.SEMICOLON:
      comma = et.SubElement(classvardec, 'symbol')
      comma.text = f" {self.tokenizer.symbol().value} "
      self.tokenizer.advance()
      varname = et.SubElement(classvardec, 'identifier')
      varname.text = f" {self.tokenizer.identifier().value} "
      self.tokenizer.advance()
    endline = et.SubElement(classvardec, 'symbol')
    endline.text = f" {self.tokenizer.symbol().value} "
    # either more var names or end line
    print_tree(self._parent_element)


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

def get_element_tree_string(element: et.Element) -> str:
    ET.indent(element)
    return ET.tostring(element, encoding='unicode')

def print_tree(element: et.Element) -> None:
    print(get_element_tree_string(element))

if __name__ == "__main__":
  compiler = XMLCompilationEngine('/Users/wianstipp/Desktop/projects/official_nand2tetris/nand2tetris/projects/10/ExpressionLessSquare/Main.jack', "ts")
  compiler.compile_class()
