"""This module contains the SymbolTable class."""

from typing import NamedTuple
from collections import OrderedDict
import enum

class Kind(str, enum.Enum):
  STATIC = "static"
  FIELD = "field"
  ARG = "arg"
  VAR = "var"

class TableEntry(NamedTuple):
  type_: str
  kind: Kind
  count: int

class SymbolTable:
  """
  name | type | kind | #
  """
  def __init__(self) -> None:
    self.reset()
  
  def reset(self) -> None:
    """Empty the SymbolTable and reset the four indicies to 0."""
    self.data: OrderedDict[str, TableEntry] = OrderedDict()
  
  def define(self, name: str, type_: str, kind: Kind) -> None:
    """Add to the table."""
    if name in self.data:
      raise ValueError(f"{name=} is already defined in the table.")
    self.data[name] = TableEntry(type_, kind, 0)
  
  def var_count(self, kind: Kind) -> int:
    """Return the number of variables of a given kind already defined."""
    counter: int = 0
    for _, row in self.data.items():
      if row.kind == kind:
        counter += row.count
    return counter
  
  def kind_of(self, name: str) -> Kind:
    """Return the kind of named identifier."""
    return self.data[name].kind
  
  def type_of(self, name: str) -> str:
    """Return the type of the named identifier."""
    return self.data[name].type_

  def index_of(self, name: str) -> int:
    """Return the index of the named variable."""
    return self.data[name].count
    # return list(self.data.keys()).index(name)
