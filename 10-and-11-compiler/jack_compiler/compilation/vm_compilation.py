"""This module contains the VM Compilation Engine which translated Jack to VM Code."""

from typing import Optional, List
import os
import argparse
import copy

from jack_compiler.compilation import base, symbol_table, vm_writing
from jack_compiler import lexicon

class VMCompilationEngine(base.CompilationEngine):
  def __init__(self, input_path: str, output_path: str) -> None:
    super().__init__(input_path, output_path)
    self.tokenizer.advance()
    if os.environ.get("VM_DEBUG"):
      self.vm_writer = vm_writing.VMWriter(output_writer=vm_writing.StdOutWriter())
    else: self.vm_writer = vm_writing.VMWriter(output_writer=vm_writing.FileWriter(self.output_path))
    self.class_symbols = symbol_table.SymbolTable()
    self.subroutine_symbols = symbol_table.SymbolTable()

  def compile_class(self) -> None:
    """Compiles a complete class."""
    self.class_symbols.reset()
    self.tokenizer.advance()
    # class name
    self.class_name = self.tokenizer.identifier()
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
    n_args: int
    if subroutine_type == lexicon.KeywordTypes.FUNCTION:
      n_args = 0
    elif subroutine_type == lexicon.KeywordTypes.METHOD:
      n_args = 1
    else: raise ValueError("")
    self.tokenizer.advance()
    # return type
    if self.tokenizer.token_type() == lexicon.TokenType.KEYWORD:
      ...
    else:
      ...
    self.tokenizer.advance()
    # subroutine name
    self.vm_writer.write_function(f"{self.class_name}.{self.tokenizer.identifier()}", n_args)
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
    if self.tokenizer.token_type() == lexicon.TokenType.SYMBOL:
      # no params
      return
    if self.tokenizer.token_type() == lexicon.TokenType.IDENTIFIER:
      ...
    else:
      ...

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
    self.tokenizer.advance()
    # type
    if self.tokenizer.token_type() == lexicon.TokenType.KEYWORD:
      type_ = self.tokenizer.keyword().value
    else: type_ = self.tokenizer.identifier()
    self.tokenizer.advance()
    names: List[str] = [self.tokenizer.identifier()]
    self.tokenizer.advance()
    while self.tokenizer.symbol() != lexicon.Symbols.SEMICOLON:
      # comma
      self.tokenizer.advance()
      names.append(self.tokenizer.identifier())
      self.tokenizer.advance()
    for name in names:
      self.subroutine_symbols.define(name=name, type_=type_, kind=symbol_table.Kind.VAR)

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
    # let keyword
    self.tokenizer.advance()
    # var name
    varname = self.tokenizer.identifier()
    self.tokenizer.advance()
    if self.tokenizer.token_type() == lexicon.TokenType.SYMBOL and \
      self.tokenizer.symbol() == lexicon.Symbols.LEFT_SQR_PAREN:
      # array
      raise NotImplementedError("")
    # assignment
    self.tokenizer.advance()
    self.compile_expression()
    self.vm_writer.write_pop(vm_writing.VMSegment.LOCAL, self.subroutine_symbols.index_of(varname))
    # semi colon
    self.tokenizer.advance()

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
    self.vm_writer.write_pop(vm_writing.VMSegment.TEMP, 0)
    self.tokenizer.advance()

  def compile_return(self) -> None:
    """Compile a return statement."""
    self.tokenizer.advance()
    if self.tokenizer.token_type() == lexicon.TokenType.SYMBOL:
      # need to push constant 0 for a null return
      self.vm_writer.write_push(vm_writing.VMSegment.CONSTANT, 0)
      self.vm_writer.write_return()
      self.tokenizer.advance()
      return
    self.compile_expression()
    self.vm_writer.write_return()
    self.tokenizer.advance()


  def compile_subroutine_call(self) -> None:
    """Compile a subroutine call."""
    # caller name
    subroutine_name = self.tokenizer.identifier()
    self.tokenizer.advance()
    if self.tokenizer.symbol() == lexicon.Symbols.PERIOD:
      # period
      self.tokenizer.advance()
      # subroutine name
      subroutine_name = f'{subroutine_name}.{self.tokenizer.identifier()}'
      self.tokenizer.advance()
    # open paran
    self.tokenizer.advance()
    self.num_expressions: Optional[int]= None
    self.compile_expression_list()
    assert isinstance(self.num_expressions, int)
    # close paran
    self.vm_writer.write_call(subroutine_name, self.num_expressions)
    self.num_expressions = None


  def compile_expression(self) -> None:
    """Compiles an expression."""
    self.compile_term()
    while self.tokenizer.token_type() == lexicon.TokenType.SYMBOL and \
          lexicon.Symbols.is_op(self.tokenizer.symbol()):
      vm_op = self.tokenizer.symbol()
      if vm_op == lexicon.Symbols.ASTERISK:
        postfix_callable = lambda : self.vm_writer.write_call("Math.multiply", 2)
      else:
        postfix_callable = lambda : self.vm_writer.write_arithmetic(vm_op)
      self.tokenizer.advance()
      self.compile_term()
      postfix_callable()
 

  def compile_term(self) -> None:
    """Compiles a term. Must do lookahead (LL2)."""
    if self.tokenizer.token_type() == lexicon.TokenType.IDENTIFIER:
      lookahead_tokenizer = copy.deepcopy(self.tokenizer)
      lookahead_tokenizer.advance()
      if lookahead_tokenizer.token_type() == lexicon.TokenType.SYMBOL and \
        lookahead_tokenizer.symbol() in {lexicon.Symbols.LEFT_PAREN, lexicon.Symbols.PERIOD}:
        self.compile_subroutine_call()
        self.tokenizer.advance()
      else:
        identifier = self.tokenizer.identifier()
        idx = self.subroutine_symbols.index_of(identifier)
        self.subroutine_symbols.kind_of(identifier)
        self.vm_writer.write_push(vm_writing.VMSegment.LOCAL, idx)
        self.tokenizer.advance()
        if self.tokenizer.token_type() == lexicon.TokenType.SYMBOL and \
            self.tokenizer.symbol() == lexicon.Symbols.LEFT_SQR_PAREN:
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
    elif self.tokenizer.token_type() == lexicon.TokenType.SYMBOL and \
        lexicon.Symbols.is_unary_op(self.tokenizer.symbol()):
      op = self.tokenizer.symbol()
      if op == lexicon.Symbols.MINUS:
        vm_op = vm_writing.VMArithmetic.NEG
      elif op == lexicon.Symbols.TILDA:
        vm_op = vm_writing.VMArithmetic.EQ
      else: raise ValueError(op)
      self.tokenizer.advance()
      self.compile_term()
      self.vm_writer.write_arithmetic(vm_op)
    else:
      raise NotImplementedError()
    

  def compile_expression_list(self) -> None:
    """Compiles a (possibly empty) comma-seperated
    list of expressions."""
    self.num_expressions = 0
    if self.tokenizer.token_type() == lexicon.TokenType.SYMBOL:
      if not self.tokenizer.symbol() == lexicon.Symbols.LEFT_PAREN:
        # no expressions
        return
    self.num_expressions += 1
    self.compile_expression()
    while self.tokenizer.token_type() == lexicon.TokenType.SYMBOL and self.tokenizer.symbol() == lexicon.Symbols.COMMA:
      # comma
      self.tokenizer.advance()
      self.compile_expression()
      self.num_expressions += 1


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("source_code_path")
  return parser.parse_args()

if __name__ == "__main__":
  ...
