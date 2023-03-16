#!/usr/bin/python
"""Tests for comment_parser.parsers.ocaml_parser.py"""

import unittest 
from comment_parser.parsers import common
from comment_parser.parsers import ocaml_parser

class OCAMLParserTest(unittest.TestCase):

  def testSimpleMain(self):
    code = "(* this is a comment *)\nint main() {\nreturn 0;\n}\n"
    comments = ocaml_parser.extract_comments(code)
    expected = [common.Comment(code[2:21], 1, multiline=False)]
    self.assertEqual(comments, expected)

  def testSingleLineComment(self):
    code = '(* single line comment *)'
    comments = ocaml_parser.extract_comments(code)
    expected = [common.Comment(' single line comment ', 1, multiline=False)]
    self.assertEqual(comments, expected)

  def testSingleLineCommentInStringLiteral(self):
    code = 'char* msg = "(* this is not a comment*)"'
    comments = ocaml_parser.extract_comments(code)
    self.assertEqual(comments, [])

  def testMultiLineComment(self):
    code = '(* multiline\ncomment *)'
    comments = ocaml_parser.extract_comments(code)
    expected = [common.Comment(code[2:-2], 1, multiline=True)]
    self.assertEqual(comments, expected)

  def testSingleLineCommentWithStars(self):
    code = "(***************)"
    comments = ocaml_parser.extract_comments(code)
    expected = [common.Comment(code[2:-2], 1, multiline=False)]
    self.assertEqual(comments, expected)
  
  def testMultiLineCommentWithStars(self):
    code = "(******\n*********)"
    comments = ocaml_parser.extract_comments(code)
    expected = [
      common.Comment(code[2:-2], 1, multiline=True)
      ]
    self.assertEqual(comments, expected)

  def testMultiLineCommentInStringLiteral(self):
    code = 'char* msg = "(* This is not a\\nmultiline comment *)"'
    comments = ocaml_parser.extract_comments(code)
    self.assertEqual(comments, [])

  def testMultiLineCommentUnterminated(self):
    code = 'int a = 1; (* Unterminated\\n comment'
    self.assertRaises(common.UnterminatedCommentError,
                      ocaml_parser.extract_comments, code)

  def testMultipleSinglelineComments(self):
    code = '(* abc *) (* 123 *)'
    comments = ocaml_parser.extract_comments(code)
    expected = [
        common.Comment(' abc ', 1, multiline=False),
        common.Comment(' 123 ', 1, multiline=False),
    ]
    self.assertEqual(comments, expected)

  def testStringThenComment(self):
    code = r'"" (* "abc *)'
    comments = ocaml_parser.extract_comments(code)
    expected = [
        common.Comment(' "abc ', 1, multiline=False),
    ]
    self.assertEqual(comments, expected)

  def testCommentStartInsideEscapedQuotesInStringLiteral(self):
    # TODO(#27): Re-enable test.
    # code = r'" \" /* \" "'
    # comments = ocaml_parser.extract_comments(code)
    # self.assertEqual(comments, [])
    pass

  def testStringEscapedBackslashCharacter(self):
    code = r'"(**)"'
    comments = ocaml_parser.extract_comments(code)
    self.assertEqual(comments, [])

  def testTwoStringsFollowedByComment(self):
    code = r'"""" (* foo *)'
    comments = ocaml_parser.extract_comments(code)
    self.assertEqual(comments, [common.Comment(' foo ', 1)])
    
  def testCommentedMultilineComment(self):
    # TODO: Not even sure if this is good ocaml code 
    code = '''(* What if i start a (* here *)
    int main(){return 0;}
    (* and ended it here *)*)'''
    comments = ocaml_parser.extract_comments(code)
    expected = [
        common.Comment(" What if i start a (* here ", 1, False),
        common.Comment(" and ended it here *)", 3, False)
    ]
    self.assertEqual(comments, expected)

  def testMultilineCommentedComment(self):
    code = '''(*(* here
    int main(){return 0;}
    *)(* and ended it here *)'''
    comments = ocaml_parser.extract_comments(code)
    expected = [
        common.Comment('(* here\n    int main(){return 0;}\n    ', 1, True),
        common.Comment(' and ended it here ', 3, False)
    ]
    self.assertEqual(comments, expected)
