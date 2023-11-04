import argparse

from jack_compiler import jack_analyzer
from jack_compiler.compilation import vm_compilation, xml_compilation


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("source_code_path")
  parser.add_argument("compiler")
  return parser.parse_args()


def main():
  args = parse_args()
  if args.compiler == 'xml':
    compiler_class = xml_compilation.XMLCompilationEngine
  elif args.compiler == 'vm':
    compiler_class = vm_compilation.VMCompilationEngine
  else: raise ValueError(f"did not recognize {args.compiler=}")
  analyzer = jack_analyzer.JackAnalyzer(args.source_code_path, compiler_class)
  analyzer.analyze()


if __name__ == "__main__":
  main()
