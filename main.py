from flask import Flask, request, render_template, redirect, send_file
import asyncio
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
model = genai.GenerativeModel(model_name="gemini-1.0-pro-001", generation_config=generation_config)

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
    
def corrigir_parte_xml(metade, erro):
    contador = 0
    while contador == 0:
        prompt = f"Por favor, corrija o erro {erro} nesta parte do arquivo XML: {metade}. Me dê como saída apenas o código XML alterado sem comentários ou explicações. Não omita nenhuma parte do código. Não abrevie o código pois vou gravá-lo de volta no xml. Não pare de gerar até que o XML esteja completo."
        convo = model.start_chat(history=[
        {
            "role": "user",
            "parts": ["You are an artificial intelligence made to correct xml files that will be input by the user"]
        },
        {
            "role": "model",
            "parts": ["```xml\n\n```"]
        },
        {
            "role": "user",
            "parts": ["You must generate the complete xml"]
        },
        {
            "role": "model",
            "parts": ["```xml\n\n```"]
        },
        {
            "role": "user",
            "parts": ["don't forget to always close the open tags"]
        },
        {
            "role": "model",
            "parts": ["```xml\n"]
        },
        {
            "role": "user",
            "parts": ["If there is a value with 4 decimal places, round up"]
        },
        {
            "role": "model",
            "parts": ["```xml\n\n\n```\n\nOutput:\n\n```xml\n\n\n```"]
        },
        
          {
            "role": "user",
            "parts": ["quantidadeExecutada e ReducaoAcrescimo devem ter o mesmo valor sempre. Altere para que fique assim."]
        },
        {
            "role": "model",
            "parts": ["Input:\n\n```xml\n\n```\n\nOutput:\n\n```xml\n\n```"]
        },
        ])
        convo.send_message(prompt)
        response = convo.last.text
        response1 = response.replace("```", " ")
        response2 = response1.replace("xml", " ")
        response_editado = response2.replace("```xml", " ")
        print(response_editado)

        contador += 1
    return response_editado


def corrigir_xml_gpt3(xml_path, erro):

    with open(xml_path, 'r') as file:
        xml_content = file.read()

    parte1 = xml_content[:len(xml_content)//30]
    parte2 = xml_content[len(xml_content)//30:2*len(xml_content)//30]
    parte3 = xml_content[2*len(xml_content)//30:3*len(xml_content)//30]
    parte4 = xml_content[3*len(xml_content)//30:4*len(xml_content)//30]
    parte5 = xml_content[4*len(xml_content)//30:5*len(xml_content)//30]
    parte6 = xml_content[5*len(xml_content)//30:6*len(xml_content)//30]
    parte7 = xml_content[6*len(xml_content)//30:7*len(xml_content)//30]
    parte8 = xml_content[7*len(xml_content)//30:8*len(xml_content)//30]
    parte9 = xml_content[8*len(xml_content)//30:9*len(xml_content)//30]
    parte10 = xml_content[9*len(xml_content)//30:10*len(xml_content)//30]
    parte11 = xml_content[10*len(xml_content)//30:11*len(xml_content)//30]
    parte12 = xml_content[11*len(xml_content)//30:12*len(xml_content)//30]
    parte13 = xml_content[12*len(xml_content)//30:13*len(xml_content)//30]
    parte14 = xml_content[13*len(xml_content)//30:14*len(xml_content)//30]
    parte15 = xml_content[14*len(xml_content)//30:15*len(xml_content)//30]
    parte16 = xml_content[15*len(xml_content)//30:16*len(xml_content)//30]
    parte17 = xml_content[16*len(xml_content)//30:17*len(xml_content)//30]
    parte18 = xml_content[17*len(xml_content)//30:18*len(xml_content)//30]
    parte19 = xml_content[18*len(xml_content)//30:19*len(xml_content)//30]
    parte20 = xml_content[19*len(xml_content)//30:20*len(xml_content)//30]
    parte21 = xml_content[20*len(xml_content)//30:21*len(xml_content)//30]
    parte22 = xml_content[21*len(xml_content)//30:22*len(xml_content)//30]
    parte23 = xml_content[22*len(xml_content)//30:23*len(xml_content)//30]
    parte24 = xml_content[23*len(xml_content)//30:24*len(xml_content)//30]
    parte25 = xml_content[24*len(xml_content)//30:25*len(xml_content)//30]
    parte26 = xml_content[25*len(xml_content)//30:26*len(xml_content)//30]
    parte27 = xml_content[26*len(xml_content)//30:27*len(xml_content)//30]
    parte28 = xml_content[27*len(xml_content)//30:28*len(xml_content)//30]
    parte29 = xml_content[28*len(xml_content)//30:29*len(xml_content)//30]
    parte30 = xml_content[29*len(xml_content)//30:]


    response_editado1 = corrigir_parte_xml(parte1, erro)
    response_editado2 = corrigir_parte_xml(parte2, erro)
    response_editado3 = corrigir_parte_xml(parte3, erro)
    response_editado4 = corrigir_parte_xml(parte4, erro)
    response_editado5 = corrigir_parte_xml(parte5, erro)
    response_editado6 = corrigir_parte_xml(parte6, erro)
    response_editado7 = corrigir_parte_xml(parte7, erro)
    response_editado8 = corrigir_parte_xml(parte8, erro)
    response_editado9 = corrigir_parte_xml(parte9, erro)
    response_editado10 = corrigir_parte_xml(parte10, erro)
    response_editado11 = corrigir_parte_xml(parte11, erro)
    response_editado12 = corrigir_parte_xml(parte12, erro)
    response_editado13 = corrigir_parte_xml(parte13, erro)
    response_editado14 = corrigir_parte_xml(parte14, erro)
    response_editado15 = corrigir_parte_xml(parte15, erro)
    response_editado16 = corrigir_parte_xml(parte16, erro)
    response_editado17 = corrigir_parte_xml(parte17, erro)
    response_editado18 = corrigir_parte_xml(parte18, erro)
    response_editado19 = corrigir_parte_xml(parte19, erro)
    response_editado20 = corrigir_parte_xml(parte20, erro)
    response_editado21 = corrigir_parte_xml(parte21, erro)
    response_editado22 = corrigir_parte_xml(parte22, erro)
    response_editado23 = corrigir_parte_xml(parte23, erro)
    response_editado24 = corrigir_parte_xml(parte24, erro)
    response_editado25 = corrigir_parte_xml(parte25, erro)
    response_editado26 = corrigir_parte_xml(parte26, erro)
    response_editado27 = corrigir_parte_xml(parte27, erro)
    response_editado28 = corrigir_parte_xml(parte28, erro)
    response_editado29 = corrigir_parte_xml(parte29, erro)
    response_editado30 = corrigir_parte_xml(parte30, erro)


    with open(xml_path, 'w') as file:
        file.write(response_editado1 + response_editado2 + response_editado3 + response_editado4 + response_editado5 +
           response_editado6 + response_editado7 + response_editado8 + response_editado9 + response_editado10 +
           response_editado11 + response_editado12 + response_editado13 + response_editado14 + response_editado15 +
           response_editado16 + response_editado17 + response_editado18 + response_editado19 + response_editado20 +
           response_editado21 + response_editado22 + response_editado23 + response_editado24 + response_editado25 +
           response_editado26 + response_editado27 + response_editado28 + response_editado29 + response_editado30)


            
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
                return f"Falha ao abrir o arquivo: {e}"
            except UnicodeDecodeError as e:
                print(f"Falha ao ler o arquivo XML {xml_path} com a codificação {cod}: {e}")
                return f"Falha ao ler o arquivo XML com a codificação {cod}: {e}"
            except etree.XMLSyntaxError as e:
                print(f"Erro de análise XML no arquivo {xml_path}: {e}")
                return f"Erro de análise XML: {e}"


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
        if validation_errors == "O XML é válido de acordo com o schema XSD fornecido.":
            result.append(validation_errors)
            corrigir_xml_gpt3(filepath, validation_errors)
        else:
            errors.append(validation_errors)
            corrigir_xml_gpt3(filepath, validation_errors)
            
    errors = ''.join(errors)
    result = ''.join(result)
            
    return render_template('errors.html', errors=errors, result=result, selected_version=selected_version, filename=file.filename)

@app.route('/download')
def download_file():
    filename = request.args.get('filename')
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

