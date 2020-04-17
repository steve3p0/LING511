# PSU Syntax Library API
# By Steve Braich
#
# Sources:
#   https://flask-restful.readthedocs.io/en/0.3.5/quickstart.html

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from typing import List, Dict
from flask_cors import CORS
from json import JSONDecodeError
#import json

import tree
import tree_exceptions

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
api = Api(app)


class Parse(Resource):
    """ Encapsulates an abstract RESTful resource for POSTing a parse request """

    def __init__(self) -> None:
        """ Constructor for Parse that sets up an HTTP POST """
        try:
            json_data = request.get_json(force=True)
            self.sentence = json_data['sentence']

            if "parser" in json_data:
                self.parser = json_data['parser']
            else:
                self.parser = None

            if "outputs" in json_data:
                self.output = json_data['formats']
            else:
                self.output = None

        except TypeError as err:
            raise tree_exceptions.InvalidUsage(err.message, 400, request.get_data())
        except JSONDecodeError as err:
            raise tree_exceptions.InvalidUsage(err.message, 400, request.get_data())
        except Exception as err:
            raise tree_exceptions.InvalidUsage(err.message, 400, request.get_data())

    def post(self) -> Dict:
        """ HTTP POST call parses a string
        :return: Dict[result] (example { 'results': 'win', 'player': 1, computer: 5 }
        :rtype: Union[Dict[str, str], None]
        """

        try:
            result = tree.parse(self.sentence, parser=self.parser, request_outputs=self.output)
            #JSON.stringify(result)
            #result = j

            return result
        except IndexError as err:
            raise tree_exceptions.InvalidUsage(err.message, 400, request.get_data())


api.add_resource(Parse, '/parse')

if __name__ == '__main__':
    # app.run()
    # app.run(ssl_context='adhoc')
    app.run(debug=True)
    # app.run(debug=False)
    # app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)
