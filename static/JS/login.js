// -----------------------------
// CADASTRO
// -----------------------------
const modalCadastro = document.getElementById("modalCadastro");
const linkCadastro = document.getElementById("abrirCadastro");
const fecharCadastro = document.getElementById("fecharCadastro");

linkCadastro.addEventListener("click", function (e) {
    e.preventDefault();
    modalCadastro.style.display = "flex";
});

function fecharModalCadastro() {
    modalCadastro.style.display = "none";
}

fecharCadastro.addEventListener("click", fecharModalCadastro);


// -----------------------------
// ESQUECI MINHA SENHA
// -----------------------------
const modalSenha = document.getElementById("modalSenha");
const btnEsqueci = document.querySelector(".esqueci");
const fecharSenha = document.getElementById("fecharSenha");

btnEsqueci.addEventListener("click", function (e) {
    e.preventDefault();
    modalSenha.style.display = "flex";
});

function fecharModalSenha() {
    modalSenha.style.display = "none";
}

fecharSenha.addEventListener("click", fecharModalSenha);


// -----------------------------
// FECHAR AO CLICAR FORA
// -----------------------------
window.onclick = function (event) {
    if (event.target === modalCadastro) {
        fecharModalCadastro();
    }
    if (event.target === modalSenha) {
        fecharModalSenha();
    }
};


// -----------------------------
// BOTÃO DE ENVIAR RECUPERAÇÃO
// -----------------------------
document.getElementById("btnEnviarRecuperacao").addEventListener("click", function () {
    const email = document.getElementById("emailRecuperar").value;

    if (email.trim() === "") {
        alert("Por favor, digite seu e-mail.");
        return;
    }

    alert("Se o e-mail existir no sistema, enviaremos um link de recuperação.");
    fecharModalSenha();
});
