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
        # Setup Inputs
        input_route = "/parse"
        sentence = "boy meets world"
        parser = "pdx"
        input_json = \
            {
                "sentence": sentence,
                "parser": parser,
                "request_formats": ["tree_ascii", "bracket_diagram", "tree_str"]
            }

        # Set Expectations
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

        # Test actual response meets expected response
        actual_response = self.client.post(input_route, json=input_json)
        self.assertEqual(self.expect_status_code, actual_response.status_code)
        actual_response_data = json.loads(actual_response.data)
        self.assertEqual(expected_response_data, actual_response_data)

    def test_parse_post_f1234_boy(self):

        # Setup Inputs
        input_route = "/parse"
        sentence = "boy meets world"
        parser = "pdx"
        input_json = \
        {
            "sentence": sentence,
            "parser": parser,
            "request_formats": ["tree_image", "tree_ascii", "bracket_diagram", "tree_str"]
        }

        # Set Expectations

        # THIS IS WHERE TREE_IMAGE EXPECTATIONS GO!!!!
        # Need to check size of byte array - json has it's limits.
        # json.loads(actual_response.data)["response_formats"]["tree_image"]
        expected_output_tree_image = inspect.cleandoc("""
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
CbYAAAAASUVORK5CYII=""")

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
            "tree_image": expected_output_tree_image,
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

        # Test actual response meets expected response
        actual_response = self.client.post(input_route, json=input_json)

        #assert_equal.__self__.maxDiff = None
        self.maxDiff = None
        self.assertEqual(self.expect_status_code, actual_response.status_code)
        actual_response_data = json.loads(actual_response.data)
        self.assertEqual(expected_response_data, actual_response_data)


