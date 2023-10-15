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
    self._parent_element = None

  def compile_class(self) -> None:
    assert self.tokenizer.keyword() == lexicon.KeywordTypes.CLASS
    self.root = et.Element("class")
    self._parent_element = self.root
    class_element = et.SubElement(self.root, 'keyword')
    class_element.text = ' class '
    self.tokenizer.advance()
    classname_id = et.SubElement(self.root, 'identifier')
    classname_id.text = f" {self.tokenizer.identifier()} "
    self.tokenizer.advance()
    assert (v := self.tokenizer.symbol().value) == '{'
    open_body = et.SubElement(self.root, 'symbol')
    open_body.text = f" {v} "
    temp = self._parent_element
    self.tokenizer.advance()
    self._parent_element = temp

    while self.tokenizer.token_type() != lexicon.TokenType.SYMBOL:
      print(self.tokenizer.input_stream)
      print(self.tokenizer._current_token)
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
    with open(self.output_path, 'w') as f:
      f.write(get_element_tree_string(self.root))
      
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
      varname.text = f" {self.tokenizer.identifier()} "
      self.tokenizer.advance()
    endline = et.SubElement(classvardec, 'symbol')
    endline.text = f" {self.tokenizer.symbol().value} "
    self.tokenizer.advance()


  def compile_subroutine_dec(self) -> None:
    """Compiles a complete method, function or constructor."""
    subroutine_dec = et.SubElement(self._parent_element, 'subroutineDec')
    subroutine_type = et.SubElement(subroutine_dec, 'keyword')
    subroutine_type.text = f" {self.tokenizer.keyword().value} "
    self.tokenizer.advance()
    if self.tokenizer.token_type() == lexicon.TokenType.KEYWORD:
      type_ = et.SubElement(subroutine_dec, 'keyword')
      type_.text = f" {self.tokenizer.keyword().value} "
    else:
      id_ = et.SubElement(subroutine_dec, 'identifier')
      id_.text = f" {self.tokenizer.identifier()} "
    self.tokenizer.advance()
    # now subroutine name
    e = et.SubElement(subroutine_dec, 'identifier')
    e.text = f" {self.tokenizer.identifier()} "
    self.tokenizer.advance()
    # open paran
    e = et.SubElement(subroutine_dec, 'symbol')
    e.text = f" {self.tokenizer.symbol()} "
    self.tokenizer.advance()
    temp = self._parent_element
    self._parent_element = subroutine_dec
    # now paramater list
    self.compile_parameter_list()
    self._parent_element = temp
    # close paran
    e = et.SubElement(subroutine_dec, 'symbol')
    e.text = f" {self.tokenizer.symbol()} "
    self.tokenizer.advance()
    # now subroutine body
    temp = self._parent_element
    self._parent_element = subroutine_dec
    self.compile_subroutine_body()
    self._parent_element = temp


  def compile_parameter_list(self) -> None:
    """Compiles a (possible empty) parameter list. Does not handle
    the enclosing '()'."""
    paramlist = et.SubElement(self._parent_element, 'parameterList')
    # no params
    if self.tokenizer.token_type() == lexicon.TokenType.SYMBOL:
      return
    if self.tokenizer.token_type() == lexicon.TokenType.IDENTIFIER:
      type_ = et.SubElement(paramlist, 'identifier')
      type_.text = f" {self.tokenizer.identifier()} "
    else:
      type_ = et.SubElement(paramlist, 'keyword')
      type_.text = f" {self.tokenizer.keyword()} "
    self.tokenizer.advance()
    varname = et.SubElement(paramlist, 'identifier')
    varname.text = f" {self.tokenizer.identifier()} "
    self.tokenizer.advance()
    while self.tokenizer.token_type() == lexicon.TokenType.SYMBOL and \
        self.tokenizer.symbol() == lexicon.Symbols.COMMA:
      comma = et.SubElement(paramlist, 'symbol')
      comma.text = f" {self.tokenizer.symbol()} "
      self.tokenizer.advance()
      if self.tokenizer.token_type() == lexicon.TokenType.IDENTIFIER:
        type_ = et.SubElement(paramlist, 'identifier')
        type_.text = f" {self.tokenizer.identifier()} "
      else:
        type_ = et.SubElement(paramlist, 'keyword')
        type_.text = f" {self.tokenizer.keyword()} "
      self.tokenizer.advance()
      varname = et.SubElement(paramlist, 'identifier')
      varname.text = f" {self.tokenizer.identifier()} "
      self.tokenizer.advance()

  def compile_subroutine_body(self) -> None:
    """Complies a subroutine's body."""
    subroutine_body = et.SubElement(self._parent_element, 'subroutineBody')
    # open curly
    e = et.SubElement(subroutine_body, 'symbol')
    e.text = f" {self.tokenizer.symbol()} "
    self.tokenizer.advance()

    temp = self._parent_element
    self._parent_element = subroutine_body
    while self.tokenizer.keyword() == lexicon.KeywordTypes.VAR:
      self.compile_var_dec()
      self.tokenizer.advance()
    self._parent_element = temp

    temp = self._parent_element
    self._parent_element = subroutine_body
    self.compile_statements()
    self._parent_element = temp
    # close curly
    e = et.SubElement(subroutine_body, 'symbol')
    e.text = f" {self.tokenizer.symbol()} "
    self.tokenizer.advance()

  def compile_var_dec(self) -> None:
    """Compiles a var declaration."""
    vardec = et.SubElement(self._parent_element, 'varDec')   
    var = et.SubElement(vardec, 'keyword')
    var.text = f" {self.tokenizer.keyword().value} " # should be 'var'
    self.tokenizer.advance()
    if self.tokenizer.token_type() == lexicon.TokenType.KEYWORD:
      type_ = et.SubElement(vardec, 'keyword')
      type_.text = f" {self.tokenizer.keyword().value} "
    else:
      id_ = et.SubElement(vardec, 'identifier')
      id_.text = f" {self.tokenizer.identifier()} "
    self.tokenizer.advance()
    varname = et.SubElement(vardec, 'identifier')
    varname.text = f" {self.tokenizer.identifier()} "
    self.tokenizer.advance()

    while self.tokenizer.symbol() != lexicon.Symbols.SEMICOLON:
      comma = et.SubElement(vardec, 'symbol')
      comma.text = f" {self.tokenizer.symbol()} "
      self.tokenizer.advance()
      extended_varname = et.SubElement(vardec, 'identifier')
      extended_varname.text = f" {self.tokenizer.identifier()} "
      self.tokenizer.advance()

    end = et.SubElement(vardec, 'symbol')
    end.text = f" {self.tokenizer.symbol()} "

  def compile_statements(self) -> None:
    """Compiles a sequence of statements. Does not handle the
    enclosing '{}'."""
    subroutine_body = et.SubElement(self._parent_element, 'statements')   
    self._parent_element = subroutine_body
    while True:
      print()
      print("stream:", self.tokenizer.input_stream)
      print('current', self.tokenizer._current_token)
      if self.tokenizer.token_type() != lexicon.TokenType.KEYWORD:
        print('breaking - next item is not a statement')
        break
      if self.tokenizer.keyword() == lexicon.KeywordTypes.LET:
        self.compile_let()
      elif self.tokenizer.keyword() == lexicon.KeywordTypes.IF:
        print("compiling if")
        self.compile_if()
      elif self.tokenizer.keyword() == lexicon.KeywordTypes.WHILE:
        self.compile_while()
      elif self.tokenizer.keyword() == lexicon.KeywordTypes.DO:
        self.compile_do()
      elif self.tokenizer.keyword() == lexicon.KeywordTypes.RETURN:
        self.compile_return()
      else:
        self.tokenizer.advance()
        break
    

  def compile_let(self) -> None:
    """Compiles a let statement."""
    let_statement = et.SubElement(self._parent_element, 'letStatement')   
    let = et.SubElement(let_statement, 'keyword')
    let.text = f" {self.tokenizer.keyword()} "
    self.tokenizer.advance()
    varname = et.SubElement(let_statement, 'identifier')
    varname.text = f" {self.tokenizer.identifier()} "
    self.tokenizer.advance()
    # now, 0 or 1 expressions
    if self.tokenizer.token_type() == lexicon.TokenType.SYMBOL and \
        self.tokenizer.symbol() == lexicon.Symbols.LEFT_SQR_PAREN:
        left_paran = et.SubElement(let_statement, 'symbol')
        left_paran.text = f" {self.tokenizer.symbol()} "
        self.compile_expression()
        self.tokenizer.advance()
        assert self.tokenizer.symbol() == lexicon.Symbols.RIGHT_SQR_PAREN
        right_paran = et.SubElement(let_statement, 'symbol')
        right_paran.text = f" {self.tokenizer.symbol()} "
    eq = et.SubElement(let_statement, 'symbol')
    eq.text = f" {self.tokenizer.symbol()} "
    self.tokenizer.advance()
    temp = self._parent_element
    self._parent_element = let_statement
    self.compile_expression()
    self._parent_element = temp
    # now, semicolon
    assert self.tokenizer.symbol() == lexicon.Symbols.SEMICOLON
    end = et.SubElement(let_statement, 'symbol')
    end.text = f" {self.tokenizer.symbol()} "
    self.tokenizer.advance()

  def compile_if(self) -> None:
    """Compiles an if statement."""
    if_statement = et.SubElement(self._parent_element, 'ifStatement')   
    if_kw = et.SubElement(if_statement, 'keyword')
    if_kw.text = f" {self.tokenizer.keyword()} "
    self.tokenizer.advance()
    open_paran = et.SubElement(if_statement, 'symbol')
    open_paran.text = f" {self.tokenizer.symbol()} "
    self.tokenizer.advance()
    temp = self._parent_element
    self._parent_element = if_statement
    self.compile_expression()
    self._parent_element = temp
    close_paran = et.SubElement(if_statement, 'symbol')
    close_paran.text = f" {self.tokenizer.symbol()} "
    self.tokenizer.advance()

    open_paran = et.SubElement(if_statement, 'symbol')
    open_paran.text = f" {self.tokenizer.symbol()} "
    self.tokenizer.advance()
    temp = self._parent_element
    self._parent_element = if_statement
    self.compile_statements()
    assert self.tokenizer.symbol() == lexicon.Symbols.RIGHT_CURLY
    self._parent_element = temp
    close_paran = et.SubElement(if_statement, 'symbol')
    close_paran.text = f" {self.tokenizer.symbol()} "
    self.tokenizer.advance()

    if self.tokenizer.token_type() == lexicon.TokenType.KEYWORD and \
        self.tokenizer.keyword() == lexicon.KeywordTypes.ELSE:
      else_kw = et.SubElement(if_statement, 'keyword')
      else_kw.text = f" {self.tokenizer.keyword()} "
      self.tokenizer.advance()
      open_paran = et.SubElement(if_statement, 'symbol')
      open_paran.text = f" {self.tokenizer.symbol()} "
      self.tokenizer.advance()
      temp = self._parent_element
      self._parent_element = if_statement
      self.compile_statements()
      self._parent_element = temp
      close_paran = et.SubElement(if_statement, 'symbol')
      close_paran.text = f" {self.tokenizer.symbol()} "

  def compile_while(self) -> None:
    """Compiles a while statement."""
    while_statement = et.SubElement(self._parent_element, 'whileStatement')   
    while_kw = et.SubElement(while_statement, 'keyword')
    while_kw.text = f" {self.tokenizer.keyword()} "
    self.tokenizer.advance()
    open_paran = et.SubElement(while_statement, 'symbol')
    open_paran.text = f" {self.tokenizer.symbol()} "
    self.tokenizer.advance()
    temp = self._parent_element
    self._parent_element = while_statement
    self.compile_expression()
    close_paran = et.SubElement(while_statement, 'symbol')
    close_paran.text = f" {self.tokenizer.symbol()} "
    self.tokenizer.advance()
    # now, statements
    open_paran = et.SubElement(while_statement, 'symbol')
    open_paran.text = f" {self.tokenizer.symbol()} "
    self.tokenizer.advance()
    self.compile_statements()
    close_paran = et.SubElement(while_statement, 'symbol')
    close_paran.text = f" {self.tokenizer.symbol()} "
    self.tokenizer.advance()
    self._parent_element = temp

  def compile_do(self) -> None:
    """Compile a do statement"""
    do_statement = et.SubElement(self._parent_element, 'doStatement')   
    do = et.SubElement(do_statement, 'keyword')
    do.text = f" {self.tokenizer.keyword()} "
    self.tokenizer.advance()
    temp = self._parent_element
    self._parent_element = do_statement
    self.compile_subroutine_call()
    self._parent_element = temp
    self.tokenizer.advance()
    close = et.SubElement(do_statement, 'symbol')
    close.text = f" {self.tokenizer.symbol()} "
    self.tokenizer.advance()

  def compile_return(self) -> None:
    """Compile a return statement."""
    return_statement = et.SubElement(self._parent_element, 'returnStatement')
    close = et.SubElement(return_statement, 'keyword')
    close.text = f" {self.tokenizer.keyword()} "
    self.tokenizer.advance()
    if self.tokenizer.token_type() == lexicon.TokenType.SYMBOL:
      close = et.SubElement(return_statement, 'symbol')
      close.text = f" {self.tokenizer.symbol()} "
      self.tokenizer.advance()
      return
    temp = self._parent_element
    self._parent_element = return_statement
    self.compile_expression()
    self._parent_element = temp
    close = et.SubElement(return_statement, 'symbol')
    close.text = f" {self.tokenizer.symbol()} "
    self.tokenizer.advance()


  def compile_subroutine_call(self) -> None:
    # subroutine_call = et.SubElement(self._parent_element, 'subroutineCall')
    subroutine_call = self._parent_element
    caller_name = et.SubElement(subroutine_call, 'identifier')   
    caller_name.text = f" {self.tokenizer.identifier()} "
    self.tokenizer.advance()
    if self.tokenizer.symbol() == lexicon.Symbols.PERIOD:
      period = et.SubElement(subroutine_call, 'symbol')   
      period.text = f" {self.tokenizer.symbol()} "
      self.tokenizer.advance()
      subroutine_name = et.SubElement(subroutine_call, 'identifier')   
      subroutine_name.text = f" {self.tokenizer.identifier()} "
      self.tokenizer.advance()
    open_paran = et.SubElement(subroutine_call, 'symbol')   
    open_paran.text = f" {self.tokenizer.symbol()} "
    self.tokenizer.advance()
    temp = self._parent_element
    self._parent_element = subroutine_call
    self.compile_expression_list() 
    self._parent_element = temp
    close_paran = et.SubElement(subroutine_call, 'symbol')   
    close_paran.text = f" {self.tokenizer.symbol()} "

  def compile_expression(self) -> None:
    """Compiles an expression."""
    expression = et.SubElement(self._parent_element, 'expression')   
    temp = self._parent_element
    self._parent_element = expression
    self.compile_term()
    self._parent_element = temp

  def compile_term(self) -> None:
    """Compiles a term. Must do lookahead (LL2)."""
    term = et.SubElement(self._parent_element, 'term')   
    if self.tokenizer.token_type() == lexicon.TokenType.IDENTIFIER:
      term_name = et.SubElement(term, 'identifier')
      term_name.text = f" {self.tokenizer.identifier()} "
    elif self.tokenizer.token_type() == lexicon.TokenType.KEYWORD:
      term_name = et.SubElement(term, 'keyword')
      term_name.text = f" {self.tokenizer.keyword()} "
    else:
      raise NotImplementedError()
    self.tokenizer.advance()


  def compile_expression_list(self) -> None:
    """Compiles a (possibly empty) comma-seperated
    list of expressions."""
    expression_list = et.SubElement(self._parent_element, 'expressionList')   
    temp = self._parent_element
    self._parent_element = expression_list
    if self.tokenizer.token_type() == lexicon.TokenType.SYMBOL:
      return
    self.compile_expression()
    while self.tokenizer.token_type() == lexicon.TokenType.SYMBOL and self.tokenizer.symbol() == lexicon.Symbols.COMMA:
      comma = et.SubElement(expression_list, 'symbol')
      comma.text = f" {self.tokenizer.symbol()} "
      self.tokenizer.advance()
      self.compile_expression()
    self._parent_element = temp

def get_element_tree_string(element: et.Element) -> str:
    ET.indent(element)
    return ET.tostring(element, encoding='unicode', short_empty_elements=False)

def print_tree(element: et.Element) -> None:
    print(get_element_tree_string(element))

def simple_xml_eq_check(file1, file2):
  tree1 = ET.parse(file1)
  tree2 = ET.parse(file2)
  elements1 = [(el.tag, el.text.strip()) for el in tree1.iter()]
  elements2 = [(el.tag, el.text.strip()) for el in tree2.iter()]
  return elements1 == elements2

if __name__ == "__main__":
  compiler = XMLCompilationEngine('/Users/wianstipp/Desktop/projects/official_nand2tetris/nand2tetris/projects/10/ExpressionLessSquare/Main.jack', "ts")
  compiler.compile_class()

