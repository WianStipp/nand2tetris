"""This module contains the VM Compilation Engine which translated Jack to VM Code."""

import argparse
import copy

from jack_compiler.compilation import base, symbol_table, vm_writing
from jack_compiler import lexicon

class VMCompilationEngine(base.CompilationEngine):
  def __init__(self, input_path: str, output_path: str) -> None:
    super().__init__(input_path, output_path)
    self.tokenizer.advance()
    self.vm_writer = vm_writing.VMWriter(output_writer=vm_writing.StdOutWriter())
    self.class_symbols = symbol_table.SymbolTable()
    self.subroutine_symbols = symbol_table.SymbolTable()

  def compile_class(self) -> None:
    """Compiles a complete class."""
    self.class_symbols.reset()
    self.tokenizer.advance()
    # class name
    self.tokenizer.advance()
    # open curly
    self.tokenizer.advance()
    while self.tokenizer.token_type() != lexicon.TokenType.SYMBOL:
      keyword = self.tokenizer.keyword()
      if keyword == lexicon.KeywordTypes.STATIC:
        raise NotImplementedError()
        self.class_sym_table.define()
        self.compile_class_var_dec()
      elif keyword == lexicon.KeywordTypes.FIELD:
        raise NotImplementedError()
        self.compile_class_var_dec()
      elif keyword == lexicon.KeywordTypes.CONSTRUCTOR:
        raise NotImplementedError()
      elif keyword == lexicon.KeywordTypes.FUNCTION:
        self.compile_subroutine_dec()
      elif keyword == lexicon.KeywordTypes.METHOD:
        raise NotImplementedError()

  def compile_class_var_dec(self) -> None:
    """Compiles a static variable or class variable declaration."""

  def compile_subroutine_dec(self) -> None:
    """Compiles a complete method, function or constructor."""
    self.subroutine_symbols.reset()
    subroutine_type = self.tokenizer.keyword().value
    self.tokenizer.advance()
    # return type
    if self.tokenizer.token_type() == lexicon.TokenType.KEYWORD:
      ...
    else:
      ...
    self.tokenizer.advance()
    # subroutine name
    self.tokenizer.advance()
    self.tokenizer.advance()
    self.compile_parameter_list()
    self.tokenizer.advance()
    # subroutine body
    self.compile_subroutine_body()
    exit()

  def compile_parameter_list(self) -> None:
    """Compiles a (possible empty) parameter list. Does not handle
    the enclosing '()'."""

  def compile_subroutine_body(self) -> None:
    """Complies a subroutine's body."""
    # open curly
    self.tokenizer.advance()
    # variable declarations
    while self.tokenizer.keyword() == lexicon.KeywordTypes.VAR:
      self.compile_var_dec()
      self.tokenizer.advance()
    
    self.compile_statements()
    # close curly
    self.tokenizer.advance()

  def compile_var_dec(self) -> None:
    """Compiles a var declaration."""

  def compile_statements(self) -> None:
    """Compiles a sequence of statements. Does not handle the
    enclosing '{}'."""
    while True:
      if self.tokenizer.token_type() != lexicon.TokenType.KEYWORD:
        break
      if self.tokenizer.keyword() == lexicon.KeywordTypes.LET:
        self.compile_let()
      elif self.tokenizer.keyword() == lexicon.KeywordTypes.IF:
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

  def compile_if(self) -> None:
    """Compiles an if statement."""

  def compile_while(self) -> None:
    """Compiles a while statement."""

  def compile_do(self) -> None:
    """Compile a do statement"""
    # do
    self.tokenizer.advance()
    self.compile_subroutine_call()
    self.tokenizer.advance()
    # semicolon
    self.tokenizer.advance()

  def compile_return(self) -> None:
    """Compile a return statement."""

  def compile_subroutine_call(self) -> None:
    """Compile a subroutine call."""
    # caller name
    self.tokenizer.advance()
    if self.tokenizer.symbol() == lexicon.Symbols.PERIOD:
      # period
      self.tokenizer.advance()
      # subroutine name
      self.tokenizer.advance()
    # open paran
    self.tokenizer.advance()
    self.compile_expression_list()
    # close paran


  def compile_expression(self) -> None:
    """Compiles an expression."""
    self.compile_term()
    while self.tokenizer.token_type() == lexicon.TokenType.SYMBOL and \
          lexicon.Symbols.is_op(self.tokenizer.symbol()):
      # op
      self.tokenizer.symbol()
      self.tokenizer.advance()
      self.compile_term()
 

  def compile_term(self) -> None:
    """Compiles a term. Must do lookahead (LL2)."""
    if self.tokenizer.token_type() == lexicon.TokenType.IDENTIFIER:
      lookahead_tokenizer = copy.deepcopy(self.tokenizer)
      lookahead_tokenizer.advance()
      raise NotImplementedError()
    elif self.tokenizer.token_type() == lexicon.TokenType.KEYWORD:
      raise NotImplementedError()
    elif self.tokenizer.token_type() == lexicon.TokenType.INT_CONST:
      # int val
      self.vm_writer.write_push(vm_writing.VMSegment.CONSTANT, self.tokenizer.int_val())
      self.tokenizer.advance()
    elif self.tokenizer.token_type() == lexicon.TokenType.STRING_CONST:
      raise NotImplementedError()
    elif self.tokenizer.token_type() == lexicon.TokenType.SYMBOL and \
      self.tokenizer.symbol() == lexicon.Symbols.LEFT_PAREN:
      self.tokenizer.advance()
      self.compile_expression()
      self.tokenizer.advance()
    else:
      raise NotImplementedError()
    

  def compile_expression_list(self) -> None:
    """Compiles a (possibly empty) comma-seperated
    list of expressions."""
    if self.tokenizer.token_type() == lexicon.TokenType.SYMBOL:
      if not self.tokenizer.symbol() == lexicon.Symbols.LEFT_PAREN:
        return
    self.compile_expression()
    while self.tokenizer.token_type() == lexicon.TokenType.SYMBOL and self.tokenizer.symbol() == lexicon.Symbols.COMMA:
      # comma
      self.tokenizer.advance()
      self.compile_expression()


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("source_code_path")
  return parser.parse_args()

if __name__ == "__main__":
  ...
