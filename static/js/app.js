document.getElementById('fileInput').addEventListener('change', function(event) {
    var file = event.target.files[0];
    var reader = new FileReader();
    reader.onload = function(event) {
        var xmlString = event.target.result;
        var parser = new DOMParser();
        var xmlDoc = parser.parseFromString(xmlString, 'text/xml');
        var ansPadrao = xmlDoc.querySelector('//ans:Padrao'); // Altere para o seletor correto se necessário
        if (ansPadrao) {
            var tissVersion = ansPadrao.textContent.replace('.', '_');
            document.getElementById('versionSelect').value = tissVersion;
        } else {
            alert('Número de versão do TISS não encontrado no arquivo XML.');
        }
    };
    reader.readAsText(file);
});

