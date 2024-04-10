from flask import Flask, request, render_template, redirect
from lxml import etree
from urllib.parse import unquote
import os
import re

app = Flask(__name__)

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
        
        with open(xml_path, 'rb') as xml_file:
            xml_doc = etree.parse(xml_file)

        schema.assertValid(xml_doc)
        return "O XML é válido de acordo com o schema XSD fornecido."
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
    if 'file' not in request.files or not file or not file.filename.endswith('.xml'):
        return redirect(request.url)
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    xsd_filename = f"tissV{selected_version}.xsd"
    xsd_path = os.path.join(SCHEMA_FOLDER, xsd_filename)
    errors = validar_xml_contra_xsd(filepath, xsd_path)

    return render_template('errors.html', errors=errors, selected_version=selected_version)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
