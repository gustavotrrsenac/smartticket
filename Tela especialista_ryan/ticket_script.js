// Dados fixos iniciais (Histórico)
const dbChamadosIniciais = [
    { id: 405100, titulo: "Revisão de Contrato Social", status: "Em Atendimento", data: "08/12/2025 09:15", cat: "Jurídico > Contratos", cliente: "Empresa Alpha LTDA" },
    { id: 301825, titulo: "Servidor de Arquivos Offline", status: "Pendente", data: "08/12/2025 10:30", cat: "TI > Infraestrutura", cliente: "Hospital Central" },
    { id: 502330, titulo: "Renderização Projeto Alpha", status: "Pendente", data: "07/12/2025 14:20", cat: "Arquitetura > 3D", cliente: "Construtora Viver Bem" },
    { id: 301811, titulo: "Bug no Login do Portal", status: "Solucionado", data: "06/12/2025 18:45", cat: "TI > Desenvolvimento", cliente: "Clinica Sorriso" }
];

// --- CARREGAR DADOS + PESCADOS ---
let dbChamados = [...dbChamadosIniciais];

// Verifica memória do navegador
const chamadosPescados = JSON.parse(localStorage.getItem('smartTicket_meus')) || [];
if (chamadosPescados.length > 0) {
    // Adiciona os pescados no topo da lista
    dbChamados = [...chamadosPescados, ...dbChamados];
}

// Configurações
let currentPage = 1;
const rowsPerPage = 7; 
let filteredData = [...dbChamados]; 

function updateTable() {
    const textFilter = document.getElementById("globalSearch").value.toLowerCase();
    const statusFilter = document.getElementById("statusFilter").value;

    filteredData = dbChamados.filter(item => {
        const matchesText = 
            item.id.toString().includes(textFilter) || 
            item.titulo.toLowerCase().includes(textFilter) ||
            item.cliente.toLowerCase().includes(textFilter) ||
            item.cat.toLowerCase().includes(textFilter);
        
        const matchesStatus = statusFilter === "" || item.status === statusFilter;
        return matchesText && matchesStatus;
    });

    const totalPages = Math.ceil(filteredData.length / rowsPerPage) || 1;
    if (currentPage > totalPages) currentPage = 1;

    renderRows();
}

function renderRows() {
    const tableBody = document.getElementById("tableBody");
    tableBody.innerHTML = ""; 

    const start = (currentPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const pageItems = filteredData.slice(start, end);

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

function updatePaginationUI(totalItems) {
    const totalPages = Math.ceil(totalItems / rowsPerPage) || 1;
    const start = (currentPage - 1) * rowsPerPage + 1;
    let end = currentPage * rowsPerPage;
    if (end > totalItems) end = totalItems;

    const infoText = document.getElementById("infoText");
    if (totalItems === 0) {
        infoText.innerText = "Nenhum chamado encontrado.";
    } else {
        infoText.innerText = `Mostrando ${start}-${end} de ${totalItems} chamados`;
    }

    document.getElementById("pageIndicator").innerText = `${currentPage} / ${totalPages}`;
    document.getElementById("btnPrev").disabled = (currentPage === 1);
    document.getElementById("btnNext").disabled = (currentPage === totalPages || totalItems === 0);
}

function changePage(direction) {
    currentPage += direction;
    renderRows();
}

window.onload = () => { updateTable(); };

// Exportar (Igual)
document.getElementById('btnExport').addEventListener('click', function() {
    let csv = [];
    csv.push('\uFEFFID;Título;Status;Data;Categoria;Cliente');
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