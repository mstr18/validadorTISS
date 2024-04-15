import google.generativeai as genai

genai.configure(api_key="AIzaSyACwhkVuzzzK4tXoSarhqaL9Y4CJ-FUc3M")
generation_config = {
    "temperature": 0.9,
}
model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config)

def corrigir_parte_xml(metade):

    prompt = f"Por favor, reescreva o arquivo XML {metade} para que possa atendar aos parâmetros que foram passados. Me dê como saída apenas o código XML alterado sem comentários ou explicações. Não omita nenhuma parte do código. Não abrevie o código pois vou gravá-lo de volta no xml. Não pare de gerar até que o XML esteja completo."
    convo = model.start_chat(history=[
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
        "parts": ["```xml"]
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
        "parts": ["quantidadeExecutada and ReducaoAcrescimo must always have the same value. Change it so it looks like this."]
    },
    {
        "role": "model",
        "parts": ["```xml\n\n\n```\n\nOutput:\n\n```xml\n\n\n```"]
    },
    ])
    convo.send_message(prompt)
    response = convo.last.text
    response1 = response.replace("```", " ")
    response2 = response1.replace("xml", " ")
    response_editado = response2.replace("```xml", " ")
    print(response_editado)

    return response_editado

def corrigir_xml_gpt3(xml_path):

    with open(xml_path, 'r') as file:
        xml_content = file.read()
        
    response_editado_list = []
    partes = []

    for i in range(1, 26):
        parte = xml_content[(i-1)*len(xml_content)//25:i*len(xml_content)//25]
        partes.append(parte)
        response_editado = corrigir_parte_xml(parte)
        response_editado_list.append(response_editado)
        print(f"Loop {i} de 25.")
        
    file_content = ''.join(response_editado_list)

    with open(xml_path, 'w') as file:
        file.write(file_content)
            
    return xml_path

