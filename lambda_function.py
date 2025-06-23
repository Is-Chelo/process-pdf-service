from weasyprint import HTML
import json


def health():
    return {
        "statusCode": 200,
        "body": json.dumps("Hola mundo desde health")
    }

def convert_to_pdf(html: str):
    pdf_bytes = HTML(string=html).write_pdf()
    # Si quieres subir a S3, hazlo aquí
    # Pero para ejemplo solo devolvemos tamaño PDF
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "PDF generado", "size_bytes": len(pdf_bytes)})
    }



def lambda_handler(event, context):
    # Se espera que event tenga {"function": "health"} o {"function": "convert_to_pdf", "html": "..."}
    try:
        data = event.get('queryStringParameters') or {}
        func = data.get('function', '')
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
