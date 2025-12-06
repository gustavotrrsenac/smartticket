const params = new URLSearchParams(window.location.search);
const nome = params.get("nome");

const especialistas = {
    "João Ribeiro": {
        email: "joao@gmail.com",
        telefone: "(11) 99999-0000",
        especialidade: "Psicólogo",
        data: "12/12/2025",
        doc1: "img/doc1.png",
        doc2: "img/doc2.png"
    },

    "Marina Lopes": {
        email: "marina@yahoo.com",
        telefone: "(21) 98888-2222",
        especialidade: "Terapeuta",
        data: "13/12/2025",
        doc1: "img/doc3.png",
        doc2: "img/doc4.png"
    }
};

if (nome && especialistas[nome]) {
    document.getElementById("nomeEsp").textContent = nome;
    document.getElementById("emailEsp").textContent = especialistas[nome].email;
    document.getElementById("telefoneEsp").textContent = especialistas[nome].telefone;
    document.getElementById("especialidadeEsp").textContent = especialistas[nome].especialidade;
    document.getElementById("dataEsp").textContent = especialistas[nome].data;

    document.getElementById("doc1").src = especialistas[nome].doc1;
    document.getElementById("doc2").src = especialistas[nome].doc2;
} else {
    console.warn("Especialista não encontrado:", nome);
}


function confirmAction(action) {
    const modalMsg = document.getElementById("modalMsg");
    const confirmBtn = document.getElementById("confirmBtn");

    modalMsg.textContent = `Tem certeza que deseja ${action} este especialista?`;

    const modal = new bootstrap.Modal(document.getElementById("confirmModal"));
    modal.show();

    confirmBtn.onclick = function () {
        if (action === "Aprovar") {
            window.location.href = "status.html?status=Validado";
        } 
        else if (action === "Rejeitar") {
            window.location.href = "status.html?status=Rejeitado";
        }
        else if (action === "Complementar") {
            window.location.href = "status.html?status=Complementação";
        }
    };
}
