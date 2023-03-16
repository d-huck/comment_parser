#!/user/bin/python
"""This module provides methods for parsing comments in erlang code"""

import re
from bisect import bisect_left
from typing import List
from comment_parser.parsers import common

def extract_comments(code: str) -> List[common.Comment]:
  """Extracts a list of comments from the given Erlang code
  
  Comments are represented with the Comment class found in the common module.
  Erlang comments only come in the single-line variety, using a single `%` as 
  the comment token. As in lisp, it is common to use multiple `%` tokens, and 
  this parser respects that removing all comment tokens and returning the text
  including the first whitespace

  Args:
      code (str): String containing code to extract comments from
  Returns:
      List[common.Comment]: List of comments in the order they appear in code
  """
  pattern = r"""
    (?P<literal> (\"([^\"\n])*\")+) |
    (?P<single> %+(?P<single_content>.*)?$)
  """
  
  compiled = re.compile(pattern, re.VERBOSE | re.MULTILINE)

  lines_indexes = []
  for match in re.finditer(r"$", code, re.M):
    lines_indexes.append(match.start())

  comments = []
  for match in compiled.finditer(code):
    kind = match.lastgroup

    start_character = match.start()
    line_no = bisect_left(lines_indexes, start_character)

    if kind == "single":
      comment_content = match.group("single_content")
      comment = common.Comment(comment_content, line_no + 1)
      comments.append(comment)
    elif kind == "multi":
      comment_content = match.group("multi_content")
      comment = common.Comment(comment_content, line_no + 1, multiline=True)
      comments.append(comment)
    elif kind == "error":
      raise common.UnterminatedCommentError()

  return comments