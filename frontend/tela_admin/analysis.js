function confirmAction(action) {
    const modalMsg = document.getElementById("modalMsg");
    const confirmBtn = document.getElementById("confirmBtn");

    if (action === "Aprovar") {
        modalMsg.innerHTML = "Deseja realmente <strong>aprovar</strong> este especialista?";
    }

    if (action === "Rejeitar") {
        modalMsg.innerHTML = "Deseja realmente <strong>rejeitar</strong> este especialista?";
    }

    if (action === "Complementar") {
        modalMsg.innerHTML = "Deseja solicitar <strong>complementação de documentos</strong>?";
    }

    confirmBtn.onclick = function() {
        alert("Ação realizada: " + action);
        let modal = bootstrap.Modal.getInstance(document.getElementById('confirmModal'));
        modal.hide();
    };

    let modal = new bootstrap.Modal(document.getElementById('confirmModal'));
    modal.show();
}
