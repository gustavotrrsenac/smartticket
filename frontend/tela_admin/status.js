// Simula dados vindos do backend ou parâmetro da URL
const especialistaStatus = "Validado"; // troque para "Rejeitado" ou "Complementação" para testar

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
        statusMessage.textContent = "Foi solicitada complementação dos documentos. O especialista precisa reenviar as informações pendentes.";
    } 
    else {
        statusIcon.className = "fas fa-info-circle";
        statusTitle.textContent = "Status Desconhecido";
        statusMessage.textContent = "Por favor, consulte o administrador para mais informações.";
    }
}

function voltarPainel() {
    window.location.href = "index.html";
}

// Renderiza ao carregar
renderStatus(especialistaStatus);
