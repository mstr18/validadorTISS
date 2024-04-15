function corrigirArquivo() {
     // Mostra a mensagem de processamento
    document.getElementById('processing-message').style.display = 'block';
    // Envia o evento 'corrigir arquivo' para o servidor
    var filepath = document.getElementById('fileInput').files[0].name;
    socket.emit('corrigir arquivo', {data: filepath});

}
