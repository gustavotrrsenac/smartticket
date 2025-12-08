document.addEventListener("DOMContentLoaded", () => {
  const senhaInput = document.getElementById("senha");
  const confirmarInput = document.getElementById("confirmar");
  const form = document.getElementById("form-cadastro");
  const botao = document.getElementById("btn-cadastrar");

  const reqMinuscula = document.getElementById("req-minuscula");
  const reqMaiuscula = document.getElementById("req-maiuscula");
  const reqEspecial = document.getElementById("req-especial");
  const reqNumero = document.getElementById("req-numero");
  const reqConfirmar = document.getElementById("req-confirmar");

  // Função que atualiza um item usando o texto armazenado em data-base
  function atualizar(elemento, condicao) {
    const base = elemento.dataset.base || elemento.textContent;
    if (condicao) {
      elemento.textContent = "✔ " + base;
      elemento.classList.add("ok");
      elemento.classList.remove("erro");
    } else {
      elemento.textContent = "✖ " + base;
      elemento.classList.add("erro");
      elemento.classList.remove("ok");
    }
  }

  function todosRequisitosOk() {
    const lista = [reqMinuscula, reqMaiuscula, reqEspecial, reqNumero, reqConfirmar];
    return lista.every(li => li.classList.contains("ok"));
  }

  function validarSenha() {
    const senha = senhaInput.value;
    const confirmar = confirmarInput.value;

    const temMinuscula = /[a-z]/.test(senha);
    const temMaiuscula = /[A-Z]/.test(senha);
    const temEspecial = /[^a-zA-Z0-9]/.test(senha);
    const temNumero = /\d/.test(senha);
    const iguais = senha !== "" && senha === confirmar;

    atualizar(reqMinuscula, temMinuscula);
    atualizar(reqMaiuscula, temMaiuscula);
    atualizar(reqEspecial, temEspecial);
    atualizar(reqNumero, temNumero);
    atualizar(reqConfirmar, iguais);

    // Habilita/desabilita botão visualmente (opcional)
    botao.disabled = !todosRequisitosOk();
    botao.style.opacity = botao.disabled ? "0.6" : "1";
  }

  // listeners
  senhaInput.addEventListener("input", validarSenha);
  confirmarInput.addEventListener("input", validarSenha);

  // Prevenir submit se requisitos não ok
  form.addEventListener("submit", (e) => {
    validarSenha(); // garantir última validação
    if (!todosRequisitosOk()) {
      e.preventDefault();
      alert("Por favor, verifique os requisitos da senha antes de cadastrar.");
    } else {
      // aqui você pode permitir envio ou integrar com backend
      // e.preventDefault(); // descomente se quiser evitar envio real
      console.log("Formulário válido — pode enviar para o servidor");
    }
  });

  // inicializa estado
  validarSenha();
});