import json

from flask import Response


def success_response_handler(response, mimetype="application/json", status=200):
    return Response(
        mimetype=mimetype,
        response=response,
        status=status
    )


def client_error_response_handler(message="Unmapped error", status=400):
    response_message = {
        "message": message
    }

    return Response(
        mimetype="application/json",
        response=json.dumps(response_message),
        status=status
    )


def server_error_response_handler(message="Unmapped error", status=500):
    response_message = {
        "message": message
    }

    return Response(
        mimetype="application/json",
        response=json.dumps(response_message),
        status=status
    )
