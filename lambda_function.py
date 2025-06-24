from weasyprint import HTML
import json
import boto3
import os
import uuid
s3 = boto3.client("s3")

BUCKET_NAME = os.environ.get("BUCKET_NAME", "solunes-lambda-storage") # Usa variable de entorno o pon directo

def health():
    return {
        "statusCode": 200,
        "body": json.dumps("Hola mundo desde health")
    }


# TODO: Funcion para subir al s3 
def upload_pdf_to_s3(pdf_bytes, filename):
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=filename,
        Body=pdf_bytes,
        ContentType='application/pdf'
    )

    # URL pública directa (sin firma)
    url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"
    return url

# TODO: Funcion para convertir el hmlt a pdf
def convert_to_pdf(html: str, path:str):
    pdf_bytes = HTML(string=html).write_pdf()
    unique_filename = f"{path}/{uuid.uuid4()}.pdf"
    url = upload_pdf_to_s3(pdf_bytes, unique_filename)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "PDF generado y subido a S3",
            "url": url
        })
    }




def lambda_handler(event, context):
    try:
        # 1. Inicializa vacío
        data = {}

        # 2. Si viene desde API Gateway con queryStringParameters
        if 'queryStringParameters' in event and event['queryStringParameters']:
            data = event['queryStringParameters']

        # 3. Si viene desde API Gateway con body JSON (POST)
        elif 'body' in event and event['body']:
            try:
                data = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
            except json.JSONDecodeError:
                return {"statusCode": 400, "body": json.dumps("Body inválido")}

        # 4. Si es invocación directa (como desde consola Lambda)
        elif isinstance(event, dict):
            data = event

        # 5. Obtener función
        func = data.get('function', '').strip()


        if func == 'health':
            return health()
        elif func == 'convert_to_pdf':
            html = data.get('html', '')
            path = data.get('path', 'credentials')
            if not html:
                return {"statusCode": 400, "body": json.dumps("Falta parámetro html")}
            return convert_to_pdf(html, path)
        else:
            return {"statusCode": 400, "body": json.dumps("Función no reconocida")}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(str(e))}
