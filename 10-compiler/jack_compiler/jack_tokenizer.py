"""This module contains the Jack Tokenizer."""


class JackTokenizer:
  def __init__(self, file_path: str) -> None:
    self.file_path = file_path
    with open(self.file_path, 'r', encoding='utf-8') as f:
      self.lines = [l.replace("\n", "") for l in f.readlines()]
    self.current_idx: int = 0

  def has_more_tokens(self) -> bool:
    """Are there any more tokens in the input?"""

  def advance(self) -> None:
    """
    Gets the next token from the input and makes it the
    current token.
    """

  def token_type(self):
    """Return the type of the current token."""

  def keyword(self):
    """Returns the keyword which is the current token."""

  def symbol(self):
    """Returns the character which is the current token."""

  def identifier(self):
    """Returns the identifier which is the current token."""

  def int_val(self) -> int:
    """Returns the integer value of the current token."""

  def string_val(self) -> str:
    """Returns the string value of the current token."""
