"""The JackAnalyzer is the top-most module used to run compilation."""

from typing import List
import os

from jack_compiler.compilation import xml_compilation


class JackAnalyzer:
  def __init__(self, input_path: str) -> None:
    self.input_path = input_path

  def analyze(self) -> None:
    """Analyze the Jack code"""
    source_files = get_jack_source_files(self.input_path)
    for source_file in source_files:
      output_path = get_output_path(source_file)
      print(f"compiling {source_file} into {output_path}")
      compiler = xml_compilation.XMLCompilationEngine(source_file, output_path)
      compiler.compile_class()


def get_jack_source_files(path: str) -> List[str]:
  """Get the list of Jack files in the input path as a list."""
  is_dir = os.path.isdir(path)
  if is_dir:
    return [p for p in os.listdir(path) if p.endswith(".jack")]
  assert path.endswith(".jack")
  return [path]


def get_output_path(input_path: str) -> os.PathLike:
  return input_path.replace(".jack", ".xml")
