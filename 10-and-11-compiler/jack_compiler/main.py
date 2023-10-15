import argparse

from jack_compiler import jack_analyzer


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("source_code_path")
  return parser.parse_args()


def main():
  args = parse_args()
  analyzer = jack_analyzer.JackAnalyzer(args.source_code_path)
  analyzer.analyze()


if __name__ == "__main__":
  main()
