from flask.ext.restful import Resource


class Messages(Resource):
    def get(self):
        return "hello friend"