"""The JackAnalyzer is the top-most module used to run compilation."""

from typing import List, Type
import os

from jack_compiler.compilation import base

class JackAnalyzer:
  def __init__(self, input_path: str, compilation_engine: Type[base.CompilationEngine]) -> None:
    self.input_path = input_path
    self.compilation_engine = compilation_engine

  def analyze(self) -> None:
    """Analyze the Jack code"""
    source_files = get_jack_source_files(self.input_path)
    for source_file in source_files:
      print(source_file)
      output_path = get_output_path(source_file)
      print(f"compiling {source_file} into {output_path}")
      self.compilation_engine(source_file, output_path).compile_class()

def get_jack_source_files(path: str) -> List[str]:
  """Get the list of Jack files in the input path as a list."""
  is_dir = os.path.isdir(path)
  if is_dir:
    return [os.path.join(path, p) for p in os.listdir(path) if p.endswith(".jack")]
  assert path.endswith(".jack")
  return [path]


def get_output_path(input_path: str) -> os.PathLike:
  return input_path.replace(".jack", ".xml")
