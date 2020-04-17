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

    def test_parse_post_complex(self):

        sentence = "The student loves his syntax homework"
        parser = "pdx"
        formats = []
        # formats.append("tree_str")
        formats.append("tree_ascii")
        formats.append("bracketed_diagram")
        formats.append("tree_str")

        parse_dict = {}
        parse_dict["sentence"] = sentence
        parse_dict["parser"] = parser
        parse_dict["formats"] = formats

        expected_result = inspect.cleandoc("""
        [TP [NP [D The] [N student]] [VP [V loves] [NP [D his] [N syntax] [N homework]]]]""")

        input_route = '/parse'
        #input_json = {'sentence': sentence, 'parser': parser}
        input_json = json.dumps(parse_dict)

        actual_response = self.client.post(input_route, json=input_json)
        self.assertEqual(actual_response.status_code, self.expect_status_code)

        actual_parse_str = json.loads(actual_response.data)
        self.assertTrue(isinstance(actual_parse_str, str))

        self.assertEqual(expected_result, actual_parse_str)