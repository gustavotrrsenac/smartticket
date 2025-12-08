// --- 1. SIMULANDO O BANCO DE DADOS (24 Itens) ---
const dbChamados = [
    { id: 405100, titulo: "Revisão de Contrato Social", status: "Em Atendimento", data: "08-12-2025 09:15", cat: "Jurídico > Contratos", cliente: "Empresa Alpha LTDA" },
    { id: 301825, titulo: "Servidor de Arquivos Offline", status: "Pendente", data: "08-12-2025 10:30", cat: "TI > Infraestrutura", cliente: "Hospital Central" },
    { id: 502330, titulo: "Renderização Projeto Alpha", status: "Pendente", data: "07-12-2025 14:20", cat: "Arquitetura > 3D", cliente: "Construtora Viver Bem" },
    { id: 301811, titulo: "Bug no Login do Portal", status: "Solucionado", data: "06-12-2025 18:45", cat: "TI > Desenvolvimento", cliente: "Clinica Sorriso" },
    { id: 405102, titulo: "Parecer Lei Trabalhista", status: "Em Atendimento", data: "08-12-2025 11:00", cat: "Jurídico > Consultoria", cliente: "Restaurante Sabor" },
    { id: 502335, titulo: "Plotagem Planta Baixa Térreo", status: "Em Atendimento", data: "08-12-2025 08:00", cat: "Arquitetura > Plotagem", cliente: "Shopping Norte" },
    { id: 302001, titulo: "Erro na Impressora Fiscal", status: "Pendente", data: "05-12-2025 09:00", cat: "TI > Suporte", cliente: "Mercado do Bairro" },
    { id: 405110, titulo: "Processo Civil 4022", status: "Solucionado", data: "01-12-2025 10:00", cat: "Jurídico > Processos", cliente: "Tech Solutions" },
    { id: 502400, titulo: "Modelagem 3D Fachada", status: "Em Atendimento", data: "08-12-2025 13:00", cat: "Arquitetura > 3D", cliente: "Residencial Flores" },
    { id: 301900, titulo: "VPN Caindo Constantemente", status: "Em Atendimento", data: "08-12-2025 07:45", cat: "TI > Redes", cliente: "Advocacia Silva" },
    { id: 405115, titulo: "Abertura de Filial RJ", status: "Pendente", data: "09-12-2025 08:00", cat: "Jurídico > Societário", cliente: "Grupo Varejo" },
    { id: 502410, titulo: "Projeto Interiores Sala", status: "Solucionado", data: "02-12-2025 16:30", cat: "Arquitetura > Interiores", cliente: "Cliente Final (João)" },
    { id: 302010, titulo: "Backup Falhou no Domingo", status: "Pendente", data: "08-12-2025 06:00", cat: "TI > Infraestrutura", cliente: "Logística Express" },
    { id: 405120, titulo: "Dúvida Tributária ICMS", status: "Solucionado", data: "04-12-2025 11:15", cat: "Jurídico > Tributário", cliente: "Indústria Metal" },
    { id: 502420, titulo: "Estudo de Viabilidade", status: "Em Atendimento", data: "08-12-2025 15:00", cat: "Arquitetura > Projetos", cliente: "Construtora Ideal" },
    { id: 302020, titulo: "Instalação Office 365", status: "Solucionado", data: "05-12-2025 14:00", cat: "TI > Suporte", cliente: "Escola Aprender" },
    { id: 405130, titulo: "Análise de Risco Contratual", status: "Pendente", data: "07-12-2025 09:30", cat: "Jurídico > Contratos", cliente: "Startup Inova" },
    { id: 502430, titulo: "Detalhamento Marcenaria", status: "Em Atendimento", data: "08-12-2025 10:45", cat: "Arquitetura > Interiores", cliente: "Ap. Decorado 502" },
    { id: 302030, titulo: "Monitor Piscando", status: "Solucionado", data: "03-12-2025 10:00", cat: "TI > Hardware", cliente: "Recepção Central" },
    { id: 405140, titulo: "Audiência Trabalhista", status: "Pendente", data: "15-12-2025 14:00", cat: "Jurídico > Trabalhista", cliente: "Transportadora Veloz" },
    { id: 502440, titulo: "Levantamento Topográfico", status: "Solucionado", data: "01-12-2025 08:00", cat: "Arquitetura > Terreno", cliente: "Condomínio Lago" },
    { id: 302040, titulo: "Firewall Bloqueando Site", status: "Em Atendimento", data: "08-12-2025 11:30", cat: "TI > Segurança", cliente: "Financeira Cred" },
    { id: 405150, titulo: "Registro de Marca INPI", status: "Pendente", data: "10-12-2025 09:00", cat: "Jurídico > Intelectual", cliente: "Marca Nova" },
    { id: 502450, titulo: "Visita Técnica Obra", status: "Em Atendimento", data: "08-12-2025 08:30", cat: "Arquitetura > Obra", cliente: "Residência Santos" }
];

// --- 2. CONFIGURAÇÕES DE PAGINAÇÃO ---
let currentPage = 1;
const rowsPerPage = 7; // Quantos chamados por tela
let filteredData = [...dbChamados]; // Começa com todos

// --- 3. FUNÇÃO PRINCIPAL: FILTRA E RENDERIZA ---
function updateTable() {
    // 1. Captura filtros
    const textFilter = document.getElementById("globalSearch").value.toLowerCase();
    const statusFilter = document.getElementById("statusFilter").value;

    // 2. Filtra o Array "Banco de Dados"
    filteredData = dbChamados.filter(item => {
        const matchesText = 
            item.id.toString().includes(textFilter) || 
            item.titulo.toLowerCase().includes(textFilter) ||
            item.cliente.toLowerCase().includes(textFilter) ||
            item.cat.toLowerCase().includes(textFilter);
        
        const matchesStatus = statusFilter === "" || item.status === statusFilter;

        return matchesText && matchesStatus;
    });

    // 3. Se a página atual for maior que o total de páginas nova, volta para a 1
    const totalPages = Math.ceil(filteredData.length / rowsPerPage) || 1;
    if (currentPage > totalPages) currentPage = 1;

    renderRows();
}

// --- 4. RENDERIZA APENAS A PÁGINA ATUAL ---
function renderRows() {
    const tableBody = document.getElementById("tableBody");
    tableBody.innerHTML = ""; // Limpa tabela

    // Define inicio e fim do slice (fatia do array)
    const start = (currentPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const pageItems = filteredData.slice(start, end);

    // Gera o HTML
    pageItems.forEach(ticket => {
        let statusClass = "";
        if(ticket.status === "Em Atendimento") statusClass = "st-atendimento";
        else if(ticket.status === "Pendente") statusClass = "st-pendente";
        else if(ticket.status === "Solucionado") statusClass = "st-solucionado";

        const row = `
            <tr>
                <td><input type="checkbox" class="custom-check"></td>
                <td>${ticket.id}</td>
                <td><a href="#" class="ticket-link">${ticket.titulo}</a></td>
                <td><div class="d-flex align-items-center"><span class="status-dot ${statusClass}"></span>${ticket.status}</div></td>
                <td>${ticket.data}</td>
                <td><span class="cat-badge">${ticket.cat}</span></td>
                <td>${ticket.cliente}</td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });

    updatePaginationUI(filteredData.length);
}

// --- 5. CONTROLES DE PAGINAÇÃO ---
function updatePaginationUI(totalItems) {
    const totalPages = Math.ceil(totalItems / rowsPerPage) || 1;
    const start = (currentPage - 1) * rowsPerPage + 1;
    let end = currentPage * rowsPerPage;
    if (end > totalItems) end = totalItems;

    // Texto "Mostrando X de Y"
    const infoText = document.getElementById("infoText");
    if (totalItems === 0) {
        infoText.innerText = "Nenhum chamado encontrado.";
    } else {
        infoText.innerText = `Mostrando ${start}-${end} de ${totalItems} chamados`;
    }

    // Indicador "1 / 4"
    document.getElementById("pageIndicator").innerText = `${currentPage} / ${totalPages}`;

    // Habilitar/Desabilitar botões
    document.getElementById("btnPrev").disabled = (currentPage === 1);
    document.getElementById("btnNext").disabled = (currentPage === totalPages || totalItems === 0);
}

function changePage(direction) {
    currentPage += direction;
    renderRows();
}

// --- INICIALIZAÇÃO ---
window.onload = () => {
    updateTable(); // Carrega tabela ao abrir
};

// --- EXPORTAR ---
document.getElementById('btnExport').addEventListener('click', function() {
    let csv = [];
    csv.push('\uFEFFID;Título;Status;Data;Categoria;Cliente'); // Cabeçalho
    
    filteredData.forEach(row => {
        csv.push(`${row.id};"${row.titulo}";${row.status};${row.data};"${row.cat}";"${row.cliente}"`);
    });

    let csvFile = new Blob([csv.join("\n")], {type: "text/csv;charset=utf-8;"});
    let downloadLink = document.createElement("a");
    downloadLink.download = "meus_chamados.csv";
    downloadLink.href = window.URL.createObjectURL(csvFile);
    downloadLink.style.display = "none";
    document.body.appendChild(downloadLink);
    downloadLink.click();
});