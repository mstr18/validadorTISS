from flask import Flask, request, render_template, redirect, send_file, jsonify
from ai import corrigir_parte_xml, corrigir_xml_gpt3
from validate import listar_versoes_tiss, validar_xml_contra_xsd
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
SCHEMA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'arquivos_schemas_ans_tiss')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


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
            corrigir_xml_gpt3(filepath)
        else:
            errors.append(validation_errors)
            corrigir_xml_gpt3(filepath)
        
            
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
        
