import json

def lambda_handler(event, context):
    html_content = """
    <html>
    <head>
        <style>
            body { font-family: sans-serif; }
            h1 { color: navy; }
        </style>
    </head>
    <body>
        <h1>¡Hola desde AWS Lambda!</h1>
        <p>Este PDF fue generado dinámicamente.</p>
    </body>
    </html>
    """

    try:
        # Crear archivo temporal para el PDF
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            HTML(string=html_content).write_pdf(tmp_pdf.name)

            # Leer el contenido PDF y convertir a base64
            with open(tmp_pdf.name, "rb") as f:
                pdf_data = f.read()
                encoded_pdf = base64.b64encode(pdf_data).decode('utf-8')

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/pdf',
                'Content-Disposition': 'inline; filename="documento.pdf"'
            },
            'isBase64Encoded': True,
            'body': encoded_pdf
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error al generar PDF: {str(e)}')
        }
    
    # TODO implement
    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Carlos Lambda!')
    # }
