"""The JackAnalyzer is the top-most module used to run compilation."""


class JackAnalyzer:
  def __init__(self, input_path: str) -> None:
    self.input_path = input_path

  def analyze(self) -> None:
    """Analyze the Jack code"""
