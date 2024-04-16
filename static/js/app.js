function corrigirArquivo() {
     // Mostra a mensagem de processamento
    document.getElementById('processing-message').style.display = 'block';

    updateProgress()
}

    function updateProgress() {

    var source = new EventSource("/progress");
    source.onmessage = function(event) {
        document.getElementById("progressBar").style.width = event.data + "%";
        document.getElementById("progressBar").textContent = event.data + "%";
    }
}
