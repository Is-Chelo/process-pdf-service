from weasyprint import HTML

def health():
    print("Hola mundo")



def convert_to_pdf(html: str):
    output_path = "/app/output/salida.pdf"
    HTML(string=html).write_pdf(output_path)
    print(f"PDF generado con éxito en {output_path}")
    return 


if __name__ == "__main__":
    function_name = input("INTRO LA FUNCION: \n")
    if function_name == 'health':
        health()
    else:
        html_input = input('Introduce el HTML:n')
        convert_to_pdf(html_input)
