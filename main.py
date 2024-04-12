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
                "parts": ["**XML Correction Assistant**\n\n**Purpose:** To correct errors in XML files provided by the user.\n\n**Capabilities:**\n\n* Validation: Checks XML files against standards (e.g., XML Schema, DTD) and identifies errors.\n* Error identification: Detects common XML errors, such as:\n    * Invalid syntax\n    * Missing or duplicate elements/attributes\n    * Invalid character entities\n    * Well-formedness issues\n* Error correction: Automatically corrects identified errors using predefined rules and heuristics.\n* Comprehensive reporting: Provides detailed reports summarizing the identified and corrected errors.\n\n**Usage:**\n\n1. **Input XML File:** Provide the XML file that needs to be corrected as input.\n2. **Validation:** The assistant will validate the XML file against relevant XML Schemas or DTDs.\n3. **Error Identification:** The assistant will identify and display a list of detected errors.\n4. **Error Correction:** The assistant will automatically correct identified errors, providing a corrected XML file.\n5. **Reporting:** A comprehensive report will be generated, outlining the errors found and the corrections made.\n\n**Benefits:**\n\n* **Accuracy:** Ensures the corrected XML files conform to XML standards, improving their reliability.\n* **Time-saving:** Automates error identification and correction processes, saving users time and effort.\n* **Improved data quality:** Corrected XML files enhance the quality of data used in applications or systems.\n* **Compliance:** Helps organizations meet XML data exchange requirements by providing error-free files.\n\n**Note:** The correction capabilities of this assistant are limited to predefined error types. For complex or custom XML errors, manual review and correction may still be necessary."]
            },
            {
                "role": "user",
                "parts": ["You must generate the complete xml"]
            },
            {
                "role": "model",
                "parts": ["**Complete XML Generation**\n\n**Purpose:** To generate a complete XML file based on user-provided input data.\n\n**Capabilities:**\n\n* Data parsing: Converts user-provided data into a structured XML format.\n* Element and attribute creation: Generates XML elements and attributes based on the input data.\n* XML Schema validation: Ensures the generated XML file conforms to a specified XML Schema.\n* Well-formedness: Produces XML files that adhere to XML well-formedness rules.\n\n**Usage:**\n\n1. **Input Data:** Provide the data that needs to be converted into XML format. This data can be in various formats, such as CSV, JSON, or even plain text.\n2. **Data Parsing:** The assistant will parse the input data and identify the relevant elements and attributes.\n3. **XML Schema:** Specify the XML Schema that the generated XML file should conform to. This ensures that the XML structure and data types are valid.\n4. **Element and Attribute Creation:** The assistant will generate the corresponding XML elements and attributes based on the parsed data and the specified XML Schema.\n5. **XML File Generation:** The assistant will assemble the generated elements and attributes into a complete XML file.\n\n**Benefits:**\n\n* **Accuracy:** Ensures that the generated XML files are structurally and semantically correct.\n* **Efficiency:** Automates the process of XML file generation, saving users time and effort.\n* **Flexibility:** Supports various input data formats, making it adaptable to different data sources.\n* **Compliance:** Helps organizations meet XML data exchange requirements by providing well-formed and schema-compliant XML files.\n\n**Note:** The complexity of the generated XML files is dependent on the input data and the specified XML Schema. For highly complex XML structures, manual review and editing may still be necessary."]
            },
            {
                "role": "user",
                "parts": ["don't forget to always close the open tags"]
            },
            {
                "role": "model",
                "parts": ["**Automatic Tag Closure**\n\n**Purpose:** To ensure that all open tags in an XML file are properly closed.\n\n**Capabilities:**\n\n* Tag identification: Identifies all open and closed tags in the XML file.\n* Automatic closure: Automatically inserts missing closing tags for any unclosed open tags.\n* Well-formedness: Ensures that the resulting XML file is well-formed and conforms to XML standards.\n\n**Usage:**\n\n1. **Input XML File:** Provide the XML file that needs to be checked for open tags.\n2. **Tag Identification:** The assistant will scan the XML file and identify all open and closed tags.\n3. **Automatic Closure:** For any unclosed open tags, the assistant will automatically insert the corresponding closing tags.\n4. **Well-formedness Validation:** The assistant will validate the modified XML file to ensure that it is well-formed.\n\n**Benefits:**\n\n* **Accuracy:** Ensures that all XML tags are properly closed, improving the reliability of the XML file.\n* **Time-saving:** Automates the process of identifying and closing open tags, saving users time and effort.\n* **Improved data quality:** Properly closed XML tags enhance the quality of data used in applications or systems.\n* **Compliance:** Helps organizations meet XML data exchange requirements by providing well-formed XML files.\n\n**Note:** This capability assumes that the XML file is otherwise well-formed and contains no other errors. For complex or malformed XML files, manual review and correction may still be necessary."]
            },
            ])

        convo.send_message(prompt)
        response = convo.last.text
        response_editado = response.replace("```xml", " ")
        print(convo.last.text)

        contador += 1
    return response_editado


def corrigir_xml_gpt3(xml_path, erro):

    with open(xml_path, 'r') as file:
        xml_content = file.read()

    parte1 = xml_content[:len(xml_content)//4]
    parte2 = xml_content[len(xml_content)//4:2*len(xml_content)//4]
    parte3 = xml_content[2*len(xml_content)//4:3*len(xml_content)//4]
    parte4 = xml_content[3*len(xml_content)//4:]

    response_editado1 = corrigir_parte_xml(parte1, erro)
    response_editado2 = corrigir_parte_xml(parte2, erro)
    response_editado3 = corrigir_parte_xml(parte3, erro)
    response_editado3 = corrigir_parte_xml(parte4, erro)

    with open(xml_path, 'w') as file:
        file.write(response_editado1 + response_editado2 + response_editado3)
            
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

