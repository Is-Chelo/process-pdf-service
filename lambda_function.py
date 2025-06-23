from weasyprint import HTML
import json


def health():
    return {
        "statusCode": 200,
        "body": json.dumps("Hola mundo desde health")
    }

def convert_to_pdf(html: str):
    pdf_bytes = HTML(string=html).write_pdf()
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "PDF generado", "size_bytes": len(pdf_bytes)})
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
            if not html:
                return {"statusCode": 400, "body": json.dumps("Falta parámetro html")}
            return convert_to_pdf(html)
        else:
            return {"statusCode": 400, "body": json.dumps("Función no reconocida")}
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps(str(e))}
