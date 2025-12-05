const params = new URLSearchParams(window.location.search);
const especialistaStatus = params.get("status");

const statusIcon = document.getElementById("statusIcon");
const statusTitle = document.getElementById("statusTitle");
const statusMessage = document.getElementById("statusMessage");

function renderStatus(status) {

    if(status === "Validado") {
        statusIcon.className = "fas fa-check-circle validado";
        statusTitle.textContent = "Especialista Validado!";
        statusMessage.textContent = "O especialista foi aprovado e está apto para atuar na plataforma.";
    } 
    else if(status === "Rejeitado") {
        statusIcon.className = "fas fa-times-circle rejeitado";
        statusTitle.textContent = "Especialista Rejeitado!";
        statusMessage.textContent = "A validação do especialista foi rejeitada. Consulte os motivos e solicite nova documentação.";
    } 
    else if(status === "Complementação") {
        statusIcon.className = "fas fa-exclamation-triangle complemento";
        statusTitle.textContent = "Solicitação de Complementação!";
        statusMessage.textContent = "Foi solicitada complementação dos documentos. O especialista precisa reenviar as informações.";
    } 
    else {
        statusIcon.className = "fas fa-info-circle";
        statusTitle.textContent = "Status Desconhecido";
        statusMessage.textContent = "Por favor, consulte o administrador.";
    }
}

function voltarPainel() {
    window.location.href = "painel_adm.html";
}

renderStatus(especialistaStatus);
