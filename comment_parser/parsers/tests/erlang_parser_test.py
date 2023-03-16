#!/usr/bin/python
"""Tests for comment_parser.parsers.erlang_parser.py"""

import unittest
from comment_parser.parsers import common 
from comment_parser.parsers import erlang_parser

class ErlangParserTest(unittest.TestCase):
  def testSimpleMain(self):
    code = "% this is a comment\nhello_world() -> io:fwrite(\"hello, world\n\")."
    comments = erlang_parser.extract_comments(code)
    expected = [common.Comment(code[1:19], 1, False)]
    self.assertEqual(comments, expected)
    
  def testSingleLineComment(self):
    code = "% single line comment"
    comments = erlang_parser.extract_comments(code)
    expected = [common.Comment(code[1:], 1, False)]
    self.assertEqual(comments, expected)
    
  def testSingleLineCommentInStringLiteral(self):
    code = 'io:fwrite("% this is not a comment").'
    comments = erlang_parser.extract_comments(code)
    self.assertEqual(comments, [])
    
  def testMultipleCommentCharacters(self):
    code = '%% this is a comment'
    comments = erlang_parser.extract_comments(code)
    expected = [common.Comment(code[2:], 1, False)]
    self.assertEqual(comments, expected)
  
  def testCommentsAfterLine(self):
    code = 'io:fwrite(\"hello, world\"). % this is a comment'
    comments = erlang_parser.extract_comments(code)
    expected = [common.Comment(' this is a comment', 1, False)]
    self.assertEqual(comments, expected)