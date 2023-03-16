#!/usr/bin/python
"""Tests for comment_parser.parsers.lisp_parser.py"""

import unittest
from comment_parser.parsers import common
from comment_parser.parsers import lisp_parser

class LispParerTest(unittest.TestCase):
    
  def testSimpleMain(self):
    code = "; this is a comment\n(format t \"Hello, World!\")"
    comments = lisp_parser.extract_comments(code)
    expected = [common.Comment(code[1:19], 1, False)]
    self.assertEqual(comments, expected)
    
  def testSingleLineComment(self):
    code = "; single line comment"
    comments = lisp_parser.extract_comments(code)
    expected = [common.Comment(code[1:], 1, False)]
    self.assertEqual(comments, expected)
    
  def testSingleLineCommentInStringLiteral(self):
    code = '(format t "; this is not a comment")'
    comments = lisp_parser.extract_comments(code)
    self.assertEqual(comments, [])
    
  def testMultipleCommentCharacters(self):
    code = ';; this is a comment'
    comments = lisp_parser.extract_comments(code)
    expected = [common.Comment(code[2:], 1, False)]
    self.assertEqual(comments, expected)
  
  def testCommentsAfterLine(self):
    code = '(t format "Hello World") ; this is a comment'
    comments = lisp_parser.extract_comments(code)
    expected = [common.Comment(' this is a comment', 1, False)]
    self.assertEqual(comments, expected)
    
  def testMultiLineComment(self):
    code = '#| multiline\ncomment |#'
    comments = lisp_parser.extract_comments(code)
    expected = [common.Comment(code[2:-2], 1, multiline=True)]
    self.assertEqual(comments, expected)

  def testMultiLineCommentWithStars(self):
    code = "#|*************|#"
    comments = lisp_parser.extract_comments(code)
    expected = [common.Comment(code[2:-2], 1, multiline=True)]
    self.assertEqual(comments, expected)

  def testMultiLineCommentInStringLiteral(self):
    code = 'char* msg = "#| This is not a\\nmultiline comment |#"'
    comments = lisp_parser.extract_comments(code)
    self.assertEqual(comments, [])
    
  def testMultiLineCommentUnterminated(self):
    code = '(format t \"Hello, World!\") #| Unterminated\\n comment'
    self.assertRaises(common.UnterminatedCommentError,
                      lisp_parser.extract_comments, code)

  def testMultipleMultilineComments(self):
    code = '#| abc |# #| 123 |#'
    comments = lisp_parser.extract_comments(code)
    expected = [
        common.Comment(' abc ', 1, multiline=True),
        common.Comment(' 123 ', 1, multiline=True),
    ]
    self.assertEqual(comments, expected)

  def testStringThenComment(self):
    code = r'"" #| "abc |#'
    comments = lisp_parser.extract_comments(code)
    expected = [
        common.Comment(' "abc ', 1, multiline=True),
    ]
    self.assertEqual(comments, expected)

  def testCommentStartInsideEscapedQuotesInStringLiteral(self):
    # TODO(#27): Re-enable test.
    # code = r'" \" /* \" "'
    # comments = lisp_parser.extract_comments(code)
    # self.assertEqual(comments, [])
    pass

  def testStringEscapedBackslashCharacter(self):
    code = r'"\\"'
    comments = lisp_parser.extract_comments(code)
    self.assertEqual(comments, [])

  def testTwoStringsFollowedByComment(self):
    code = r'"""" ; foo'
    comments = lisp_parser.extract_comments(code)
    self.assertEqual(comments, [common.Comment(' foo', 1)])

  def testCommentedMultilineComment(self):
    code = '''; What if i start a #| here
    (format t \"Hello, World!\")
    ; and ended it here |#'''
    comments = lisp_parser.extract_comments(code)
    expected = [
        common.Comment(" What if i start a #| here", 1, False),
        common.Comment(" and ended it here |#", 3, False)
    ]
    self.assertEqual(comments, expected)

  def testMultilineCommentedComment(self):
    code = '''#|; here
    int main(){return 0;}
    |#; and ended it here |#'''
    comments = lisp_parser.extract_comments(code)
    expected = [
        common.Comment('; here\n    int main(){return 0;}\n    ', 1, True),
        common.Comment(' and ended it here |#', 3, False)
    ]
    self.assertEqual(comments, expected)