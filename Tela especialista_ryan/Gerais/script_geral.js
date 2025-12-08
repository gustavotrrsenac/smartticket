// --- 1. SIMULANDO BANCO DE DADOS (CHAMADOS GERAIS / SEM TÉCNICO) ---
const dbChamadosGerais = [
    { id: 601001, titulo: "Internet Lenta no 3º Andar", status: "Novo", local: "Escritório Central", cat: "TI > Redes", data: "08-12-2025 14:00" },
    { id: 601002, titulo: "Impressão de Plantas A0", status: "Novo", local: "Obra Alpha", cat: "Arquitetura > Plotagem", data: "08-12-2025 13:45" },
    { id: 601003, titulo: "Dúvida Cláusula 4ª", status: "Novo", local: "Filial Norte", cat: "Jurídico > Contratos", data: "08-12-2025 13:30" },
    { id: 601004, titulo: "Criar usuário no sistema BI", status: "Pendente", local: "Escritório Central", cat: "TI > Acessos", data: "08-12-2025 12:15" },
    { id: 601005, titulo: "Aprovação de Layout", status: "Novo", local: "Obra Beta", cat: "Arquitetura > Projetos", data: "08-12-2025 11:50" },
    { id: 601006, titulo: "Atualizar Licença Office", status: "Novo", local: "Filial Sul", cat: "TI > Software", data: "08-12-2025 11:00" },
    { id: 601007, titulo: "Parecer sobre Aditivo", status: "Pendente", local: "Escritório Central", cat: "Jurídico > Consultoria", data: "08-12-2025 10:20" },
    { id: 601008, titulo: "Computador não liga", status: "Novo", local: "Recepção", cat: "TI > Hardware", data: "08-12-2025 09:00" },
    { id: 601009, titulo: "Cotação Material Escritório", status: "Novo", local: "Almoxarifado", cat: "Adm > Compras", data: "08-12-2025 08:30" },
    { id: 601010, titulo: "Erro ao gerar boleto", status: "Pendente", local: "Financeiro", cat: "TI > Sistemas", data: "07-12-2025 18:00" },
    { id: 601011, titulo: "Revisão Memorial Descritivo", status: "Novo", local: "Obra Alpha", cat: "Arquitetura > Doc", data: "07-12-2025 16:45" },
    { id: 601012, titulo: "Configurar Email no Celular", status: "Novo", local: "Diretoria", cat: "TI > Suporte", data: "07-12-2025 15:00" }
];

// --- 2. CONFIGURAÇÕES DE PAGINAÇÃO ---
let currentPageGen = 1;
const rowsPerPageGen = 8; 
let filteredDataGen = [...dbChamadosGerais]; 

// --- 3. ATUALIZAR TABELA ---
function updateGeneralTable() {
    const textFilter = document.getElementById("generalSearch").value.toLowerCase();
    const locFilter = document.getElementById("locFilter").value;

    filteredDataGen = dbChamadosGerais.filter(item => {
        const matchesText = 
            item.id.toString().includes(textFilter) || 
            item.titulo.toLowerCase().includes(textFilter);
        
        const matchesLoc = locFilter === "" || item.local === locFilter;

        return matchesText && matchesLoc;
    });

    const totalPages = Math.ceil(filteredDataGen.length / rowsPerPageGen) || 1;
    if (currentPageGen > totalPages) currentPageGen = 1;

    renderGeneralRows();
}

// --- 4. RENDERIZAR LINHAS ---
function renderGeneralRows() {
    const tableBody = document.getElementById("generalTableBody");
    tableBody.innerHTML = "";

    const start = (currentPageGen - 1) * rowsPerPageGen;
    const end = start + rowsPerPageGen;
    const pageItems = filteredDataGen.slice(start, end);

    pageItems.forEach(ticket => {
        // Status com cores
        let statusClass = "st-novo"; // Padrão azul
        if(ticket.status === "Pendente") statusClass = "st-pendente"; // Amarelo

        const row = `
            <tr>
                <td><input type="checkbox" class="custom-check"></td>
                <td>${ticket.id}</td>
                <td><a href="#" class="ticket-link">${ticket.titulo}</a></td>
                <td><div class="d-flex align-items-center"><span class="status-dot ${statusClass}"></span>${ticket.status}</div></td>
                <td>${ticket.local}</td>
                <td><span class="cat-badge">${ticket.cat}</span></td>
                <td>${ticket.data}</td>
                <td class="text-center">
                    <button class="assign-btn" onclick="atribuirChamado(${ticket.id})">
                        Atribuir a mim
                    </button>
                </td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });

    updatePaginationUIGen(filteredDataGen.length);
}

// --- 5. PAGINAÇÃO UI ---
function updatePaginationUIGen(totalItems) {
    const totalPages = Math.ceil(totalItems / rowsPerPageGen) || 1;
    const start = (currentPageGen - 1) * rowsPerPageGen + 1;
    let end = currentPageGen * rowsPerPageGen;
    if (end > totalItems) end = totalItems;

    const infoText = document.getElementById("infoTextGeneral");
    if (totalItems === 0) {
        infoText.innerText = "Nenhum chamado disponível.";
    } else {
        infoText.innerText = `Mostrando ${start}-${end} de ${totalItems} chamados`;
    }

    document.getElementById("pageIndicatorGen").innerText = `${currentPageGen} / ${totalPages}`;
    document.getElementById("btnPrevGen").disabled = (currentPageGen === 1);
    document.getElementById("btnNextGen").disabled = (currentPageGen === totalPages || totalItems === 0);
}

function changePageGeneral(direction) {
    currentPageGen += direction;
    renderGeneralRows();
}

// --- 6. SIMULAÇÃO DE ATRIBUIÇÃO ---
function atribuirChamado(id) {
    // Apenas visual para o protótipo
    alert(`Chamado #${id} atribuído ao seu perfil com sucesso!`);
    // Na vida real, aqui faríamos um POST para o backend
    // Removemos da lista visualmente para simular que saiu do "Pool Geral"
    const index = dbChamadosGerais.findIndex(c => c.id === id);
    if (index > -1) {
        dbChamadosGerais.splice(index, 1);
        updateGeneralTable();
    }
}

// --- ORDENAÇÃO ---
function sortGeneralTable(n) {
    // (Lógica de ordenação idêntica à anterior, pode copiar se quiser a funcionalidade completa de sort)
    console.log("Ordenar coluna " + n); 
}

// Inicializa
window.onload = () => {
    updateGeneralTable();
};