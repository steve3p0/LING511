# Rock Paper Scissors Lizard Spock
# By Steve Braich
#
# Inspiration:
#   https://stackoverflow.com/questions/7428124/how-can-i-fake-request-post-and-get-params-for-unit-testing-in-flask
#   https://flask.palletsprojects.com/en/1.0.x/testing/

from unittest import TestCase
from app import app
import json
import inspect

# Integration Tests
class TestApp(TestCase):

    def setUp(self):
        self.expect_status_code = 200
        # self.expect_choices = lizardspock.choices
        # self.expect_results = lizardspock.results

        self.input_content_type = 'application/json'
        self.client = app.test_client()

    def test_parse_post(self):

        sentence = "The student loves his syntax homework"
        expected_result = inspect.cleandoc("""
        [TP [NP [D The] [N student]] [VP [V loves] [NP [D his] [N syntax] [N homework]]]]""")

        input_route = '/parse'
        input_json = {'sentence': sentence}

        actual_response = self.client.post(input_route, json=input_json)
        self.assertEqual(actual_response.status_code, self.expect_status_code)

        actual_parse_str = json.loads(actual_response.data)
        self.assertTrue(isinstance(actual_parse_str, str))

        self.assertEqual(expected_result, actual_parse_str)

    def test_parse_post_stanford(self):

        sentence = "The student loves his syntax homework"
        expected_result = inspect.cleandoc("""
        [ROOT [S [NP [DT The] [NN student]] [VP [VBZ loves] [NP [PRP$ his] [NN syntax] [NN homework]]]]]""")

        input_route = '/parse'
        input_json = \
        {
            'sentence': sentence,
            'parser': "stanford"
        }

        actual_response = self.client.post(input_route, json=input_json)
        self.assertEqual(actual_response.status_code, self.expect_status_code)

        actual_parse_str = json.loads(actual_response.data)
        self.assertTrue(isinstance(actual_parse_str, str))

        self.assertEqual(expected_result, actual_parse_str)

    def test_parse_post_image(self):

        sentence = "The student loves his syntax homework"
        expected_result = inspect.cleandoc("""
        [TP [NP [D The] [N student]] [VP [V loves] [NP [D his] [N syntax] [N homework]]]]""")

        input_route = '/parse'
        input_json = {'sentence': sentence}

        #actual_response = self.client.post(input_route, json=input_json)
        actual_response = self.client.post(input_route, )

        self.assertEqual(actual_response.status_code, self.expect_status_code)

        actual_parse_str = json.loads(actual_response.data)
        self.assertTrue(isinstance(actual_parse_str, str))

        self.assertEqual(expected_result, actual_parse_str)

    def test_parse_post_f234_student(self):

        sentence = "The student loves his syntax homework"
        parser = "pdx"

        input_route = "/parse"
        input_json = \
        {
            "sentence": sentence,
            "parser": parser,
            "request_formats": ["tree_ascii", "bracket_diagram", "tree_str"]
        }

        actual_response = self.client.post(input_route, json=input_json)
        self.assertEqual(self.expect_status_code, actual_response.status_code)

        actual_response_data = json.loads(actual_response.data)
        self.assertTrue(isinstance(actual_response_data, dict))

        actual_sentence = actual_response_data["sentence"]
        actual_parser = actual_response_data["parser"]
        actual_formats = actual_response_data["response_formats"]

        self.assertTrue(isinstance(actual_sentence, str))
        self.assertTrue(isinstance(actual_parser, str))
        self.assertTrue(isinstance(actual_formats, dict))

        actual_tree_ascii = actual_formats["tree_ascii"]
        self.assertTrue(isinstance(actual_tree_ascii, str))
        actual_bracket_diagram = actual_formats["bracket_diagram"]
        self.assertTrue(isinstance(actual_bracket_diagram, str))
        actual_tree_str = actual_formats["tree_str"]
        self.assertTrue(isinstance(actual_tree_str, str))

        expected_output_tree_ascii = inspect.cleandoc("""
                  TP                         
      ____________|________                   
     |                     VP                
     |             ________|____              
     NP           |             NP           
  ___|_____       |     ________|_______      
 D         N      V    D        N       N    
 |         |      |    |        |       |     
The     student loves his     syntax homework""")

        expected_output_bracket_diagram = inspect.cleandoc("""
            [TP [NP [D The] [N student]] [VP [V loves] [NP [D his] [N syntax] [N homework]]]]""")
        expected_output_tree_str = inspect.cleandoc("""
            (TP (NP (D The) (N student)) (VP (V loves) (NP (D his) (N syntax) (N homework))))""")

        expected_sentence = sentence
        expected_parser = parser
        expected_output = \
        {
            "tree_ascii": expected_output_tree_ascii,
            "bracket_diagram": expected_output_bracket_diagram,
            "tree_str": expected_output_tree_str
        }
        expected_response_data = \
        {
            "sentence": expected_sentence,
            "parser": expected_parser,
            "response_formats": expected_output
        }

        self.assertEqual(expected_sentence, actual_sentence)
        self.assertEqual(expected_parser, actual_parser)

        self.assertEqual(expected_output_tree_ascii, actual_tree_ascii)
        self.assertEqual(expected_output_bracket_diagram, actual_bracket_diagram)
        self.assertEqual(expected_output_tree_str, actual_tree_str)
        self.assertEqual(expected_output_bracket_diagram, actual_bracket_diagram)

        self.assertEqual(expected_response_data, actual_response_data)

    def test_parse_post_f234_boy(self):

        sentence = "boy meets world"
        parser = "pdx"

        input_route = "/parse"
        input_json = \
        {
            "sentence": sentence,
            "parser": parser,
            "request_formats": ["tree_ascii", "bracket_diagram", "tree_str"]
        }

        actual_response = self.client.post(input_route, json=input_json)
        self.assertEqual(self.expect_status_code, actual_response.status_code)

        actual_response_data = json.loads(actual_response.data)
        expected_output_tree_ascii = inspect.cleandoc("""
      TP           
  ____|____         
 |         VP      
 |     ____|____    
 NP   |         NP 
 |    |         |   
 N    V         N  
 |    |         |   
boy meets     world""")

        expected_output_bracket_diagram = inspect.cleandoc("""
            [TP [NP [N boy]] [VP [V meets] [NP [N world]]]]""")
        expected_output_tree_str = inspect.cleandoc("""
            (TP (NP (N boy)) (VP (V meets) (NP (N world))))""")

        expected_sentence = sentence
        expected_parser = parser
        expected_output = \
        {
            "tree_ascii": expected_output_tree_ascii,
            "bracket_diagram": expected_output_bracket_diagram,
            "tree_str": expected_output_tree_str
        }
        expected_response_data = \
        {
            "sentence": expected_sentence,
            "parser": expected_parser,
            "response_formats": expected_output
        }
        self.assertEqual(expected_response_data, actual_response_data)