"""This module contains the Jack Tokenizer."""

from typing import Any
import re

from jack_compiler import lexicon

class JackTokenizer:
  def __init__(self, file_path: str) -> None:
    self.file_path = file_path
    with open(self.file_path, 'r', encoding='utf-8') as f:
      self.input_stream = " ".join([l.replace("\n", "").strip() for l in f.readlines()])
      print(self.input_stream)
    self._re_keyword_pattern = "|".join([v.value for v in lexicon.KeywordTypes])
    self._re_symbol_pattern = "|".join([re.escape(v.value) for v in lexicon.Symbols])
    self.advance()
  
  def has_more_tokens(self) -> bool:
    """Are there any more tokens in the input?"""
    return bool(len(self.input_stream.strip()))

  def advance(self) -> Any:
    """
    Gets the next token from the input and makes it the
    current token.
    """
    keyword_match = re.search(self._re_keyword_pattern, self.input_stream)
    symbol_match = re.search(self._re_symbol_pattern, self.input_stream)
    int_match = re.search(r'-?\d+', self.input_stream)
    string_cont_match = re.search(r'"[^"]*"', self.input_stream)
    if keyword_match and keyword_match.span()[0] == 0:
      self.current_token = lexicon.KeywordTypes(keyword_match.group())
      self._token_type = lexicon.TokenType.KEYWORD
    elif symbol_match and symbol_match.span()[0] == 0:
      self.current_token = lexicon.Symbols(symbol_match.group())
      self._token_type = lexicon.TokenType.SYMBOL
    elif int_match and int_match.span()[0] == 0:
      self.current_token = int(int_match.group())
      self._token_type = lexicon.TokenType.INT_CONST
    elif string_cont_match and string_cont_match.span()[0] == 0:
      self.current_token = string_cont_match.group()
      self._token_type = lexicon.TokenType.STRING_CONST
    else:
      # identifier
      self.current_token = None # current token is up until the min of the next match
      self._token_type = lexicon.TokenType.IDENTIFIER
    print(self.current_token)

  def token_type(self) -> lexicon.TokenType:
    """Return the type of the current token."""
    return self._token_type
    if isinstance(self.current_token, lexicon.KeywordTypes):
      return lexicon.TokenType.KEYWORD
    elif isinstance(self.current_token, lexicon.Symbols):
      return lexicon.TokenType.SYMBOL
    elif isinstance(self.current_token, int):
      return lexicon.TokenType.INT_CONST
    elif isinstance(self.current_token):
      return lexicon.TokenType.STRING_CONST

  def keyword(self) -> lexicon.KeywordTypes:
    """Returns the keyword which is the current token."""

  def symbol(self) -> lexicon.Symbols:
    """Returns the character which is the current token."""

  def identifier(self) -> str:
    """Returns the identifier which is the current token."""

  def int_val(self) -> int:
    """Returns the integer value of the current token."""
    assert self.token_type() == lexicon.TokenType.INT_CONST
    return self.current_token

  def string_val(self) -> str:
    """Returns the string value of the current token."""
    assert self.token_type() == lexicon.TokenType.STRING_CONST
    return self.current_token
