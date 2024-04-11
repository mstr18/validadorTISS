from flask import Flask, request, render_template, redirect
import google.generativeai as genai
from lxml import etree
from urllib.parse import unquote
import os
import re

app = Flask(__name__)
genai.configure(api_key="AIzaSyACwhkVuzzzK4tXoSarhqaL9Y4CJ-FUc3M")
generation_config = {
    "temperature": 0.9,
}
model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config)

UPLOAD_FOLDER = 'uploads'
SCHEMA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'arquivos_schemas_ans_tiss')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

class SchemaResolver(etree.Resolver):
    def __init__(self, schema_path):
        super().__init__()
        self.schema_path = schema_path

    def resolve(self, url, pubid, context):
        if url.startswith('file:/'):
            path = unquote(url.replace('file:/', ''))
        else:
            path = os.path.join(self.schema_path, url)

        if re.match(r'^/[a-zA-Z]:', path):
            path = path[1:]

        return self.resolve_filename(path, context)


def corrigir_xml_gpt3(xml_path):

    with open(xml_path, 'r') as file:
        xml_content = file.read()

    prompt = f"Por favor, corrija os erros neste arquivo XML: {xml_content}. Me dê como saída apenas o código XML alterado sem comentários ou explicações. Não omita nenhuma parte do código. Não abrevie o código pois vou gravá-lo de volta no xml. Não pare de gerar até que o XML esteja completo."
    convo = model.start_chat(history=[
        {
            "role": "user",
            "parts": ["gere o código xml sem parar até terminar"]
        },
        {
            "role": "model",
            "parts": ["```xml\n\n```"]
        },
        ])

    convo.send_message(prompt)
    response = convo.last.text
    response_editado = response.replace("```xml", " ")
    print(convo.last.text)

    with open(xml_path, 'w') as file:
        file.write(response_editado)

    return xml_path


def listar_versoes_tiss(diretorio_schema):
    versoes = set()
    regex = re.compile(r"tissV(\d+_\d+_\d+).xsd")
    for arquivo in os.listdir(diretorio_schema):
        match = regex.search(arquivo)
        if match:
            versoes.add(match.group(1).replace('_', '.'))
    return sorted(versoes)

def validar_xml_contra_xsd(xml_path, xsd_path):
    try:
        with open(xsd_path, 'rb') as xsd_file:
            schema_doc = etree.parse(xsd_file)

        schema = etree.XMLSchema(schema_doc)
        
        codificacoes = ['utf-8', 'iso-8859-1', 'windows-1252']  # Adicione mais codificações se necessário
        for cod in codificacoes:
            try:
                with open(xml_path, 'rb') as xml_file:
                    xml_doc = etree.parse(xml_file)
                    for elem in xml_doc.iter():
                        if elem.text is None:
                            elem.text = ""
                schema.assertValid(xml_doc)
                return "O XML é válido de acordo com o schema XSD fornecido."
            except IOError as e:
                print(f"Falha ao abrir o arquivo {xml_path}: {e}")
                return "Falha ao abrir o arquivo"
            except UnicodeDecodeError as e:
                print(f"Falha ao ler o arquivo XML {xml_path} com a codificação {cod}: {e}")
                return "Falha ao ler o arquivo XML"
            except etree.XMLSyntaxError as e:
                print(f"Erro de análise XML no arquivo {xml_path}: {e}")
                return "Erro de análise XML"


    except IOError as e:
        return f"Erro ao carregar o schema XSD: {e}"
    except etree.XMLSchemaError as e:
        return f"Erro ao validar o XML: {e}"
    except Exception as e:
        return f"Erro desconhecido ao validar o XML: {e}"

@app.route('/', methods=['GET'])
def upload_file_get():
    versoes_tiss = listar_versoes_tiss(SCHEMA_FOLDER)
    return render_template('index.html', versoes_tiss=versoes_tiss)


@app.route('/', methods=['POST'])
def upload_file_post():
    selected_version = request.form.get('version').replace('.', '_')
    file = request.files['file']
    errors = []
    result = []
    if 'file' not in request.files or not file or not file.filename.endswith('.xml'):
        errors.append(f"Erro: O arquivo que você inseriu {file.filename} não é um arquivo com o final .xml. Apenas arquivos .xml são aceitos.")
    else:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        xsd_filename = f"tissV{selected_version}.xsd"
        xsd_path = os.path.join(SCHEMA_FOLDER, xsd_filename)
        validation_errors = validar_xml_contra_xsd(filepath, xsd_path)
        corrigir_xml_gpt3(filepath)
        if validation_errors == "O XML é válido de acordo com o schema XSD fornecido.":
            result.append(validation_errors)
        else:
            errors.append(validation_errors)
            
    errors = ''.join(errors)
    result = ''.join(result)
            
    return render_template('errors.html', errors=errors, result=result, selected_version=selected_version)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
