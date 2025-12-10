// --- DADOS ---
let listaEspecialistas = [
    { 
        id: 101, nome: "João Ribeiro", email: "joao@eng.com", area: "Engenharia", registro: "CREA-SP 12345", 
        cpf: "123.456.789-00", rg: "12.345.678-X", celular: "(11) 99999-8888", telefone: "(11) 3333-4444", status: "pendente" 
    },
    { 
        id: 102, nome: "Marina Lopes", email: "mari@adv.com", area: "Advocacia", registro: "OAB-RJ 99887", 
        cpf: "222.333.444-55", rg: "22.333.444-5", celular: "(21) 98888-7777", telefone: "(21) 3322-1100", status: "pendente" 
    },
    { 
        id: 103, nome: "Dr. Pedro Silva", email: "pedro@med.com", area: "Saúde", registro: "CRM-MG 55443", 
        cpf: "555.666.777-88", rg: "33.444.555-6", celular: "(31) 97777-6666", telefone: "(31) 3200-1000", status: "pendente" 
    },
    { 
        id: 104, nome: "Carla Dias", email: "carla@nutri.com", area: "Nutrição", registro: "CRN-3 11223", 
        cpf: "888.222.111-00", rg: "44.222.111-X", celular: "(11) 91234-5678", telefone: "", status: "aprovado" 
    },
    { 
        id: 105, nome: "Roberto Matos", email: "beto@ti.com", area: "TI", registro: "N/A", 
        cpf: "999.888.777-66", rg: "44.555.666-7", celular: "(41) 99999-1111", telefone: "", status: "rejeitado" 
    }
];

// Usuários agora só tem Nome e Email (+ ID e Status)
let listaUsuarios = [
    { id: 501, nome: "Empresa Alpha", email: "alpha@corp.com", status: "Ativo" },
    { id: 502, nome: "Carlos Eduardo", email: "carlos@gmail.com", status: "Ativo" },
    { id: 503, nome: "Fernanda Lima", email: "nanda@hotmail.com", status: "Inativo" }
];

let idSelecionado = null;
window.abaAtual = 'pendente';

// --- INICIALIZAÇÃO ---
document.addEventListener('DOMContentLoaded', () => {
    filtrarTabela('pendente');
    renderUsuarios();
    atualizarKPIs();
    renderChart(); 
});

// --- RENDERIZAR TABELA ESPECIALISTAS ---
function filtrarTabela(filtro, btnElement) {
    if(btnElement) {
        document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
        btnElement.classList.add('active');
    }
    window.abaAtual = filtro;

    const filtrados = listaEspecialistas.filter(esp => esp.status === filtro);
    const tbody = document.getElementById('lista-especialistas');
    tbody.innerHTML = "";

    if (filtrados.length === 0) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center; opacity:0.5; padding:20px;">Vazio.</td></tr>`;
        return;
    }

    filtrados.forEach(esp => {
        let acaoHTML = '';
        let statusBadge = '';

        if (esp.status === 'pendente') {
            statusBadge = '<span class="status st-pendente">Pendente</span>';
            acaoHTML = `<button class="btn-action" onclick="abrirModalAnalise(${esp.id})">Analisar</button>`;
        } else if (esp.status === 'aprovado') {
            statusBadge = '<span class="status st-aprovado">Aprovado</span>';
            acaoHTML = `<button class="btn-undo" onclick="desfazerAcao(${esp.id})"><i class="fa-solid fa-rotate-left"></i> Desfazer</button>`;
        } else {
            statusBadge = '<span class="status st-rejeitado">Rejeitado</span>';
            acaoHTML = `<button class="btn-undo" onclick="desfazerAcao(${esp.id})"><i class="fa-solid fa-rotate-left"></i> Desfazer</button>`;
        }

        const row = `
            <tr>
                <td><a href="#" class="link-nome" onclick="verDetalhes('especialista', ${esp.id})">${esp.nome}</a></td>
                <td>${esp.area}</td>
                <td>${esp.registro}</td>
                <td>${statusBadge}</td>
                <td>${acaoHTML}</td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

// --- RENDERIZAR TABELA USUÁRIOS ---
function renderUsuarios() {
    const tbody = document.getElementById('lista-usuarios');
    tbody.innerHTML = "";
    listaUsuarios.forEach(u => {
        const statusClass = u.status === 'Ativo' ? 'st-aprovado' : 'st-rejeitado';
        tbody.innerHTML += `
            <tr>
                <td>#${u.id}</td>
                <td><a href="#" class="link-nome" onclick="verDetalhes('usuario', ${u.id})">${u.nome}</a></td>
                <td>${u.email}</td>
                <td><span class="status ${statusClass}">${u.status}</span></td>
            </tr>
        `;
    });
}

// --- MODAL DE ANÁLISE (Especialistas Pendentes) ---
function abrirModalAnalise(id) {
    idSelecionado = id;
    const esp = listaEspecialistas.find(e => e.id === id);
    if(esp) {
        document.getElementById('analiseNome').innerText = esp.nome;
        document.getElementById('analiseArea').innerText = esp.area;
        document.getElementById('analiseEmail').innerText = esp.email;
        document.getElementById('analiseCPF').innerText = esp.cpf;
        document.getElementById('analiseRG').innerText = esp.rg;
        document.getElementById('analiseCelular').innerText = esp.celular;
        document.getElementById('analiseTelefone').innerText = esp.telefone || "N/A";
        document.getElementById('modalAnalise').style.display = 'flex';
    }
}

// --- MODAL DE DETALHES (Perfil: Especialista OU Usuário) ---
function verDetalhes(tipo, id) {
    let dados;
    // Seleciona todos os campos exclusivos de especialista
    const camposExtras = document.querySelectorAll('.campos-especialista');

    if (tipo === 'especialista') {
        dados = listaEspecialistas.find(e => e.id === id);
        
        // 1. Configura visual
        document.getElementById('perfilTipo').innerText = "Especialista";
        document.getElementById('perfilTipo').className = "status st-pendente"; // Cor laranja
        
        // 2. MOSTRA campos extras
        camposExtras.forEach(el => el.style.display = 'block');

        // 3. Preenche dados extras
        document.getElementById('perfilCPF').innerText = dados.cpf;
        document.getElementById('perfilRG').innerText = dados.rg;
        document.getElementById('perfilCelular').innerText = dados.celular;
        document.getElementById('perfilTelefone').innerText = dados.telefone || "N/A";
        document.getElementById('perfilRegistro').innerText = dados.registro;
        document.getElementById('perfilStatusText').innerText = dados.status.toUpperCase();

    } else {
        // É USUÁRIO
        dados = listaUsuarios.find(u => u.id === id);
        
        // 1. Configura visual
        document.getElementById('perfilTipo').innerText = "Cliente";
        document.getElementById('perfilTipo').className = "status st-aprovado"; // Cor verde
        
        // 2. ESCONDE campos extras (CPF, RG, etc)
        camposExtras.forEach(el => el.style.display = 'none');

        // 3. Status simples
        document.getElementById('perfilStatusText').innerText = dados.status;
    }

    if(dados) {
        // Dados comuns a ambos
        document.getElementById('perfilNome').innerText = dados.nome;
        document.getElementById('perfilEmail').innerText = dados.email;
        document.getElementById('modalPerfil').style.display = 'flex';
    }
}

function fecharModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// --- AÇÕES ---
function processarDecisao(decisao) {
    const index = listaEspecialistas.findIndex(e => e.id === idSelecionado);
    if(index !== -1) {
        listaEspecialistas[index].status = decisao;
        alert(decisao === 'aprovado' ? "Aprovado!" : "Rejeitado!");
        fecharModal('modalAnalise');
        filtrarTabela('pendente');
        atualizarKPIs();
    }
}

function desfazerAcao(id) {
    if(confirm("Voltar para PENDENTE?")) {
        const index = listaEspecialistas.findIndex(e => e.id === id);
        listaEspecialistas[index].status = 'pendente';
        filtrarTabela(window.abaAtual);
        atualizarKPIs();
    }
}

function showSection(id) {
    document.querySelectorAll('.view-section').forEach(el => el.style.display = 'none');
    document.getElementById(id).style.display = 'block';
    document.querySelectorAll('.menu-btn').forEach(btn => btn.classList.remove('active'));
    event.currentTarget.classList.add('active');
}

function atualizarKPIs() {
    const pend = listaEspecialistas.filter(e => e.status === 'pendente').length;
    const ativ = listaEspecialistas.filter(e => e.status === 'aprovado').length;
    document.getElementById('count-pendentes').innerText = pend;
    document.getElementById('kpi-pendentes').innerText = pend;
    document.getElementById('kpi-ativos').innerText = ativ;
}

// --- GRÁFICO ---
function renderChart() {
    const ctx = document.getElementById('adminChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun'],
            datasets: [{
                label: 'Novos Usuários',
                data: [12, 19, 30, 50, 80, 120],
                borderColor: '#a855f7',
                backgroundColor: 'rgba(168, 85, 247, 0.2)',
                tension: 0.4,
                fill: true
            },
            {
                label: 'Especialistas',
                data: [2, 5, 8, 15, 20, 35],
                borderColor: '#22c55e',
                tension: 0.4,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: 'white' } } },
            scales: {
                y: { grid: { color: 'rgba(255,255,255,0.1)' }, ticks: { color: 'white' } },
                x: { grid: { display: false }, ticks: { color: 'white' } }
            }
        }
    });
}