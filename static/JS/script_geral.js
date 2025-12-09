// --- 1. DADOS (AGORA COM REQUERENTE) ---
const dbChamadosGerais = [
    { id: 601001, titulo: "Lentidão no Sistema Fiscal", status: "Novo", requerente: "Ana Pereira", local: "SP", cat: "TI > Sistemas", abertura: "2025-12-08T08:00", prazo: "2025-12-08T16:00" },
    { id: 601002, titulo: "Plotagem Planta Hospitalar", status: "Novo", requerente: "Carlos Eng.", local: "RJ", cat: "Arq > Plotagem", abertura: "2025-12-08T09:30", prazo: "2025-12-08T14:30" },
    { id: 601003, titulo: "Revisão Contrato Franquia", status: "Novo", requerente: "Dra. Julia", local: "MG", cat: "Jur > Contratos", abertura: "2025-12-07T10:00", prazo: "2025-12-09T10:00" },
    { id: 601004, titulo: "Acesso Bloqueado VPN", status: "Pendente", requerente: "Roberto TI", local: "SP", cat: "TI > Acessos", abertura: "2025-12-08T10:00", prazo: "2025-12-08T12:00" },
    { id: 601005, titulo: "Projeto Elétrico Galpão", status: "Novo", requerente: "Construtora Z", local: "BA", cat: "Arq > Projetos", abertura: "2025-12-05T14:00", prazo: "2025-12-10T18:00" },
    { id: 601006, titulo: "Erro Instalação AutoCAD", status: "Novo", requerente: "Estagiário Lucas", local: "RS", cat: "TI > Software", abertura: "2025-12-08T08:00", prazo: "2025-12-08T12:00" },
    { id: 601007, titulo: "Parecer Trabalhista", status: "Pendente", requerente: "RH Central", local: "DF", cat: "Jur > Consultoria", abertura: "2025-12-06T09:00", prazo: "2025-12-08T09:00" },
    { id: 601008, titulo: "Servidor local offline", status: "Novo", requerente: "Gerente TI", local: "MG", cat: "TI > Infra", abertura: "2025-12-08T07:00", prazo: "2025-12-08T11:00" }
];

let currentPageGen = 1;
const rowsPerPageGen = 8; 
let filteredDataGen = [...dbChamadosGerais]; 

// Verifica se já pescou algo antes (para não duplicar se recarregar)
const chamadosPescados = JSON.parse(localStorage.getItem('smartTicket_pescados')) || [];
// Filtra os que JÁ foram pescados para não aparecerem aqui
filteredDataGen = filteredDataGen.filter(t => !chamadosPescados.some(p => p.id === t.id));


function formatarData(isoString) {
    const data = new Date(isoString);
    return `${String(data.getDate()).padStart(2,'0')}/${String(data.getMonth()+1).padStart(2,'0')}/${data.getFullYear()} ${String(data.getHours()).padStart(2,'0')}:${String(data.getMinutes()).padStart(2,'0')}`;
}

function getSLAProgressBar(aberturaIso, prazoIso) {
    const inicio = new Date(aberturaIso).getTime();
    const fim = new Date(prazoIso).getTime();
    const agora = new Date().getTime(); 
    
    const totalTempo = fim - inicio;
    const tempoCorrido = agora - inicio;
    let porcentagem = (tempoCorrido / totalTempo) * 100;

    if (porcentagem < 0) porcentagem = 0;
    
    let corClass = "sla-fill-green";
    if (porcentagem > 70) corClass = "sla-fill-yellow";
    if (porcentagem >= 100) { porcentagem = 100; corClass = "sla-fill-red"; }

    const dataPrazoFormatada = formatarData(prazoIso);

    return `
        <div class="sla-container">
            <span class="sla-date-text">${dataPrazoFormatada}</span>
            <div class="sla-bar-bg">
                <div class="sla-bar-fill ${corClass}" style="width: ${porcentagem}%"></div>
            </div>
        </div>
    `;
}

function updateGeneralTable() {
    const textFilter = document.getElementById("generalSearch").value.toLowerCase();
    const locFilter = document.getElementById("locFilter").value;

    // Filtra base + remove os que já foram pescados
    const disponiveis = dbChamadosGerais.filter(t => !chamadosPescados.some(p => p.id === t.id));

    filteredDataGen = disponiveis.filter(item => {
        const matchesText = 
            item.id.toString().includes(textFilter) || 
            item.titulo.toLowerCase().includes(textFilter) ||
            item.requerente.toLowerCase().includes(textFilter); // Busca por requerente tbm
        const matchesLoc = locFilter === "" || item.local === locFilter;
        return matchesText && matchesLoc;
    });

    renderGeneralRows();
}

function renderGeneralRows() {
    const tableBody = document.getElementById("generalTableBody");
    tableBody.innerHTML = "";

    const start = (currentPageGen - 1) * rowsPerPageGen;
    const end = start + rowsPerPageGen;
    const pageItems = filteredDataGen.slice(start, end);

    pageItems.forEach(ticket => {
        let statusClass = "st-novo";
        if(ticket.status === "Pendente") statusClass = "st-pendente";

        const slaHTML = getSLAProgressBar(ticket.abertura, ticket.prazo);
        const dataAberturaFmt = formatarData(ticket.abertura);

        const row = `
            <tr>
                <td><input type="checkbox" class="custom-check"></td>
                <td>${ticket.id}</td>
                <td><a href="#" class="ticket-link">${ticket.titulo}</a></td>
                <td><div class="d-flex align-items-center"><span class="status-dot ${statusClass}"></span>${ticket.status}</div></td>
                
                <td style="font-weight: 500; color:white;">${ticket.requerente}</td>

                <td><span class="loc-badge">${ticket.local}</span></td>
                <td><span class="cat-badge">${ticket.cat}</span></td>
                <td style="font-size: 0.85rem; color: rgba(255,255,255,0.7);">${dataAberturaFmt}</td>
                <td>${slaHTML}</td>
                <td class="text-center">
                    <button class="assign-btn" onclick="atribuirChamado(${ticket.id})">
                        Pescar
                    </button>
                </td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });

    updatePaginationUIGen(filteredDataGen.length);
}

function updatePaginationUIGen(totalItems) {
    const totalPages = Math.ceil(totalItems / rowsPerPageGen) || 1;
    document.getElementById("infoTextGeneral").innerText = `Total: ${totalItems} chamados`;
    document.getElementById("pageIndicatorGen").innerText = `${currentPageGen} / ${totalPages}`;
}
function changePageGeneral(d) { currentPageGen += d; renderGeneralRows(); }

// --- MÁGICA DE TRANSIÇÃO ---
function atribuirChamado(id) {
    if(confirm(`Deseja pescar o chamado #${id}? Ele irá para sua lista.`)) {
        
        // 1. Acha o chamado
        const ticket = dbChamadosGerais.find(c => c.id === id);
        
        if (ticket) {
            // 2. Cria o objeto formato "Meus Chamados"
            const novoMeuChamado = {
                id: ticket.id,
                titulo: ticket.titulo,
                status: "Em Atendimento", // Muda status automático
                data: formatarData(ticket.abertura),
                cat: ticket.cat,
                cliente: ticket.requerente
            };

            // 3. Salva na memória do navegador
            const meusAtuais = JSON.parse(localStorage.getItem('smartTicket_meus')) || [];
            meusAtuais.unshift(novoMeuChamado); // Adiciona no topo
            localStorage.setItem('smartTicket_meus', JSON.stringify(meusAtuais));

            // 4. Salva lista de "pescados" para não mostrar mais aqui
            chamadosPescados.push(ticket);
            localStorage.setItem('smartTicket_pescados', JSON.stringify(chamadosPescados));

            // 5. Atualiza a tela
            updateGeneralTable();
            alert("Chamado pescado com sucesso! Verifique 'Meus Chamados'.");
        }
    }
}

function sortGeneralTable(n) { console.log("Ordenar", n); }

window.onload = () => { updateGeneralTable(); };