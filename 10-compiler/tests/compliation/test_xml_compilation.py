from typing import List, Tuple
import pytest
import xml.etree.ElementTree as ET
import glob
from lxml import etree as et

from jack_compiler.compilation.xml_compilation import XMLCompilationEngine
from jack_compiler.jack_tokenizer import JackTokenizer

EXPRESSIONLESS_SQUARE_PATH = '../../official_nand2tetris/nand2tetris/projects/10/ExpressionLessSquare'

def get_inputs_and_expected_paths(dir_path: str) -> List[Tuple[str, str]]:
    jack_files = glob.glob(f"{dir_path}/*.jack")
    token_xml_files = [path.replace('.jack', '.xml') for path in jack_files]
    return list(zip(jack_files, token_xml_files))

@pytest.mark.parametrize("jack, expected_xml", get_inputs_and_expected_paths(EXPRESSIONLESS_SQUARE_PATH))
def test_expressionless_compilation(jack, expected_xml):
  assert simple_xml_eq_check(jack, expected_xml)


def simple_xml_eq_check(file1, file2):
  compiler = XMLCompilationEngine(file1, "tmp1")
  tree1 = ET.parse(file2)
  compiler.compile_class()
  tree2 = ET.parse("tmp1")
  elements1 = [(el.tag, el.text.strip()) for el in tree1.iter()]
  elements2 = [(el.tag, el.text.strip() if el.text else "") for el in tree2.iter()]
  if elements1 == elements2:
    return True
  for e1, e2 in zip(elements1, elements2):
     if e1 != e2:
        print("answer:", e1)
        print("got:", e2)
        break
  return False


if __name__ == "__main__":
  paths = get_inputs_and_expected_paths(EXPRESSIONLESS_SQUARE_PATH)[::-1]
  for input_, expected in paths:
     print(input_)
     test_expressionless_compilation(input_, expected)
