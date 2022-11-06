"""Contains the VMTranslator function."""

from vmtranslator import vmparser, codewriter

def translate_to_hack(input_file_path: str, output_file_path: str) -> None:
  """Translate VM code to Hack code."""
  parser = vmparser.VMParser(input_file_path)
  asm_writer = codewriter.ASMCodeWriter(output_file_path)
  # TODO: write code to run
