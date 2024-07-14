from flask import Flask, jsonify
from flasgger import Swagger, swag_from
import json

app = Flask(__name__)
swagger = Swagger(app)

@app.route('/data', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'A list of Pokemons',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'description': {
                                    'type': 'string',
                                    'example': 'string'
                                },
                                'name': {
                                    'type': 'string',
                                    'example': 'string'
                                },
                                'price': {
                                    'type': 'string',
                                    'example': 'string'
                                },
                                'stock': {
                                    'type': 'string',
                                    'example': 'string'
                                }
                            }
                        }
                    }
                }
            }
        }
    }
})
def GetPokemons():
    with open('data.json', 'r') as file:
        data = [json.loads(line) for line in file]
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
