# Validador XML para TISS

Este projeto contém um validador XML robusto, projetado especificamente para lidar com as diferentes versões do padrão TISS, além de garantir a correta codificação e tratamento de erros durante a leitura dos arquivos.

## Funcionalidades

- **Suporte a Múltiplas Versões do TISS**: Compatível com todas as versões do padrão TISS.
- **Detecção de Codificação**: Identifica automaticamente a codificação do arquivo XML, suportando UTF-8, ISO-8859-1, entre outras.
- **Tratamento de Erros de Leitura**: Capaz de identificar e informar erros durante a leitura do arquivo, como tags malformadas ou problemas de estrutura.

## Exceções Tratadas

Aqui estão algumas das exceções XML que já foram tratadas pelo validador:

- `TISSVersionError`: Erro lançado quando uma versão não suportada do TISS é detectada.
- `EncodingError`: Erro lançado quando há problemas relacionados à codificação do arquivo XML.
- `FileReadError`: Erro lançado quando o arquivo XML não pode ser lido corretamente.
- `IOError`: Esse erro é lançado quando há algum problema ao abrir o arquivo XML.
- `Falta de Tags`: Caso faltar alguma tag no arquivo XML, o validador irá inserir uma string vazia para que não estoure um erro.
- `Arquivo não é um XML`: Caso o arquivo enviado não for um XML o sistema trata e exibe uma mensagem de erro. Além disso, ao inserir o arquivo apenas o XML é permitido.

## Como Usar

Para utilizar o validador, siga os passos abaixo:

1. Clone o repositório para sua máquina local.
2. Instale as dependências necessárias utilizando `pip install -r requirements.txt`.
3. Execute o validador com o comando `python main.py`.

Ou utilize a imagem docker disponível no Docker Hub:

```
docker pull chiapettaiago/validadorxml:latest
```

Para executar use o seguinte comando:

```
docker run -p 5000:5000 chiapettaiago/validadorxml:latest
```

Após isso basta digitar http://localhost:5000 no seu navegador e o validador xml vai abrir.
