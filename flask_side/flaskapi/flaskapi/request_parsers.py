from flask_restful import reqparse


def add_arguments_to_parser(parser, arguments):
    for field in arguments:
        parser.add_argument(
            field, help='This field cannot be blank', required=True
        )


login_parser = reqparse.RequestParser()
login_fields = ('email', 'password')
