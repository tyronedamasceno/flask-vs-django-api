from flask_restful import reqparse


def add_arguments_to_parser(parser, arguments):
    for field in arguments:
        parser.add_argument(
            field, help='This field cannot be blank', required=True
        )


login_parser = reqparse.RequestParser()
user_parser = reqparse.RequestParser()
self_transaction_parser = reqparse.RequestParser()

login_fields = ('email', 'password')
user_fields = ('email', 'password', 'doc_number')
self_transaction_fields = ('value', )

add_arguments_to_parser(login_parser, login_fields)
add_arguments_to_parser(user_parser, user_fields)
add_arguments_to_parser(self_transaction_parser, self_transaction_fields)
