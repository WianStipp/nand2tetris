"""This module contains the SymbolTable class."""

class SymbolTable:
  """
  name | type | kind | #
  """
  def __init__(self) -> None:
    pass
  
  def reset(self) -> None:
    """Empty the SymbolTable and reset the four indicies to 0."""
    ...
  
  def define(self, name: str, type_: str, kind) -> None:
    """Add to the table."""
    ...
  
  def var_count(self, kind) -> int:
    """Return the number of variables of a given kind already defined."""
    ...
  
  def kind_of(self, name: str):
    """Return the kind of named identifier."""
    ...
  
  def type_of(self, name: str) -> str:
    """Return the type of the named identifier."""

  def index_of(self, name: str) -> int:
    """Return the index of the named variable."""