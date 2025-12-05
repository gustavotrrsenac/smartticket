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
