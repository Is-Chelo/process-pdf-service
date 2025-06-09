import json
import base64
import tempfile
from weasyprint import HTML


def sumar(event):
    x = int(event["queryStringParameters"].get("x", 0))
    y = int(event["queryStringParameters"].get("y", 0))
    return {
        "statusCode": 200,
        "body": json.dumps({"resultado": x + y})
    }


def lambda_handler(event, context):
    path = event.get("path", "/")

    if "/sumar" in path:
        return sumar(event)
    elif "/pdf" in path:
        return pdf_generate()
    else:
        return {
            "statusCode": 404,
            "body": json.dumps("Ruta no encontrada")
        }
