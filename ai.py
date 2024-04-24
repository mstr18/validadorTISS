import google.generativeai as genai
import xml.etree.ElementTree as ET
import math

genai.configure(api_key="AIzaSyACwhkVuzzzK4tXoSarhqaL9Y4CJ-FUc3M")
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}
model = genai.GenerativeModel(model_name="gemini-1.0-pro-001", generation_config=generation_config)

def corrigir_parte_xml(parte_xml):
    prompt = f"Por favor, reescreva o seguinte arquivo XML de modo que não haja nenhuma tag aberta que fique sem fechar. Também caso exista algum valor com 4 casas decimais, arredonde para apenas duas. Me dê como saída apenas o código XML alterado sem comentários ou explicações. Não omita nenhuma parte do código. Não abrevie o código pois vou gravá-lo de volta no xml:\n\n{parte_xml}"
    convo = model.start_chat(history=[])
    
    convo.send_message(prompt)
    response = convo.last.text
    response1 = response.replace("```", " ")
    response2 = response1.replace("xml", " ")
    response_editado = response2.replace("```xml", " ")
    print(response_editado)

    return response_editado

def dividir_xml_em_partes(xml_path, max_part_size=2048):

    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Converter o XML para uma string
    xml_str = ET.tostring(root, encoding='unicode')
    
    # Calcular o número de partes
    num_parts = math.ceil(len(xml_str) / max_part_size)
    
    # Dividir o XML em partes
    parts = []
    for i in range(num_parts):
        start = i * max_part_size
        end = (i + 1) * max_part_size
        parts.append(xml_str[start:end])
    
    return parts

def corrigir_xml_gpt3(xml_path):
    parts = dividir_xml_em_partes(xml_path, max_part_size=1024)

    tasks = []
    for parte in parts:
        tasks.append(corrigir_parte_xml(parte))

    responses = tasks

    file_content = ''.join(responses)

    with open(xml_path, 'w') as file:
        file.write(file_content)
            
    return xml_path