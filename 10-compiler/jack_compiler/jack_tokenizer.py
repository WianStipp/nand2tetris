"""This module contains the Jack Tokenizer."""

from typing import Any, Optional, List
import re

from jack_compiler import lexicon

class JackTokenizer:
  def __init__(self, file_path: str) -> None:
    self.file_path = file_path
    with open(self.file_path, 'r', encoding='utf-8') as f:
      self.input_stream = " ".join([l.replace("\n", " ").strip() for l in f.readlines()])
    keywords = [v.value for v in lexicon.KeywordTypes]
    self._re_keyword_pattern = r"\b(" + "|".join(keywords) + r")\b"
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
    span_end = None
    if keyword_match and keyword_match.span()[0] == 0:
      self._current_token = lexicon.KeywordTypes(keyword_match.group())
      self._token_type = lexicon.TokenType.KEYWORD
      span_end = keyword_match.span()[1]
    elif symbol_match and symbol_match.span()[0] == 0:
      self._current_token = lexicon.Symbols(symbol_match.group())
      self._token_type = lexicon.TokenType.SYMBOL
      span_end = symbol_match.span()[1]
    elif int_match and int_match.span()[0] == 0:
      self._current_token = int(int_match.group())
      self._token_type = lexicon.TokenType.INT_CONST
      span_end = int_match.span()[1]
    elif string_cont_match and string_cont_match.span()[0] == 0:
      self._current_token = string_cont_match.group()
      self._token_type = lexicon.TokenType.STRING_CONST
      span_end = string_cont_match.span()[1]
    else:
      # identifier
      next_match_start = get_min_span_start([keyword_match, symbol_match, int_match, string_cont_match])
      if next_match_start is not None:
        self._current_token = self.input_stream[:next_match_start].strip()
      else:
        self._current_token = self.input_stream.strip()
      span_end = len(self._current_token)
      self._token_type = lexicon.TokenType.IDENTIFIER
    # reset input_stream
    assert span_end
    self.input_stream = self.input_stream[span_end:].strip()

  def token_type(self) -> lexicon.TokenType:
    """Return the type of the current token."""
    return self._token_type

  def keyword(self) -> lexicon.KeywordTypes:
    """Returns the keyword which is the current token."""
    assert self.token_type() == lexicon.TokenType.KEYWORD
    return self._current_token

  def symbol(self) -> lexicon.Symbols:
    """Returns the character which is the current token."""
    assert self.token_type() == lexicon.TokenType.SYMBOL
    return self._current_token

  def identifier(self) -> str:
    """Returns the identifier which is the current token."""
    assert self.token_type() == lexicon.TokenType.IDENTIFIER
    return self._current_token

  def int_val(self) -> int:
    """Returns the integer value of the current token."""
    assert self.token_type() == lexicon.TokenType.INT_CONST
    return self._current_token

  def string_val(self) -> str:
    """Returns the string value of the current token."""
    assert self.token_type() == lexicon.TokenType.STRING_CONST
    return self._current_token

def get_min_span_start(matches: List[Optional[re.Match]]) -> int:
  min_start: Optional[int] = None
  for match in matches:
    if not match:
      continue
    match_start = match.span()[0]
    if min_start is None:
      min_start = match_start
    else:
      min_start = min(min_start, match_start)
  return min_start
