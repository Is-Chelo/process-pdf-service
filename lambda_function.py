import json
import base64
import tempfile
from weasyprint import HTML

def pdf_generate(event):
    
    data = json.loads(event.get("body", "{}"))
    html_content = int(data.get("html_content", 0))
    # html_content = """
    # <html>
    # <head>
    #     <style>
    #         body { font-family: sans-serif; }
    #         h1 { color: navy; }
    #     </style>
    # </head>
    # <body>
    #     <h1>¡Hola desde AWS Lambda!</h1>
    #     <p>Este PDF fue generado dinámicamente.</p>
    # </body>
    # </html>
    # """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
        HTML(string=html_content).write_pdf(tmp_pdf.name)

        with open(tmp_pdf.name, "rb") as f:
            pdf_data = f.read()
            encoded_pdf = base64.b64encode(pdf_data).decode("utf-8")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/pdf",
            "Content-Disposition": "inline; filename=\"documento.pdf\""
        },
        "isBase64Encoded": True,
        "body": encoded_pdf
    }

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
