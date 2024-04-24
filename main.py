from flask import Flask, request, render_template, redirect, send_file, jsonify
from ai import corrigir_parte_xml, corrigir_xml_gpt3
from validate import listar_versoes_tiss, validar_xml_contra_xsd, find_padrao_tag
import os
import time

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
    file = request.files['file']
    errors = []
    result = []
    if 'file' not in request.files or not file or not file.filename.endswith('.xml'):
        errors.append(f"Erro: O arquivo que você inseriu {file.filename} não é um arquivo com o final .xml. Apenas arquivos .xml são aceitos.")
    else:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        
        # Encontrar a versão TISS do arquivo XML
        selected_version = None
        for version in listar_versoes_tiss(SCHEMA_FOLDER):
            version_short = version.replace('.', '_')
            xsd_filename = f"tissV{version_short}.xsd"
            xsd_path = os.path.join(SCHEMA_FOLDER, xsd_filename)
            if validar_xml_contra_xsd(filepath, xsd_path) == "O XML é válido de acordo com o schema XSD fornecido.":
                selected_version = version
                break
        
        if selected_version is None:
            errors.append(f"Erro: Não foi possível determinar a versão TISS do arquivo {file.filename}.")
        else:
            # Validar e corrigir o arquivo XML
            validation_errors = validar_xml_contra_xsd(filepath, os.path.join(SCHEMA_FOLDER, f"tissV{selected_version.replace('.', '_')}.xsd"))
            if validation_errors == "O XML é válido de acordo com o schema XSD fornecido.":
                result.append(validation_errors)
                corrigir_xml_gpt3(filepath)
                tiss = find_padrao_tag(filepath)
            else:
                errors.append(validation_errors)
                corrigir_xml_gpt3(filepath)
                tiss = find_padrao_tag(filepath)
            
    errors = ''.join(errors)
    result = ''.join(result)
            
    return render_template('errors.html', errors=errors, result=result, selected_version=selected_version, tiss=tiss, filename=file.filename)

@app.route('/download')
def download_file():
    filename = request.args.get('filename')
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    return send_file(filepath, as_attachment=True)

@app.route('/progress')
def progress():
    def generate():
        x = 1
        while x <= 100:
            time.sleep(30)  # Simula um trabalho sendo feito
            yield f"data:{x}\n\n"
            x += 4
    return app.response_class(generate(), mimetype='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
        
