// Dados Mockados (Apenas chamados DESSA pessoa)
const meusChamados = [
    { id: 1024, assunto: "Erro ao acessar VPN", status: "Aberto", data: "Hoje, 10:30" },
    { id: 1020, assunto: "Solicitação de Mouse Novo", status: "Resolvido", data: "Ontem" },
    { id: 1015, assunto: "Dúvida sobre Holerite", status: "Aguardando", data: "05/12/2025" },
    { id: 998,  assunto: "Instalação do Photoshop", status: "Resolvido", data: "01/12/2025" }
];

function renderClientTable(lista) {
    const tbody = document.getElementById('clientTableBody');
    const empty = document.getElementById('emptyState');
    
    tbody.innerHTML = '';

    if (lista.length === 0) {
        empty.style.display = 'block';
        return;
    } else {
        empty.style.display = 'none';
    }

    lista.forEach(ticket => {
        let statusClass = 'st-aberto';
        if(ticket.status === 'Resolvido') statusClass = 'st-resolvido';
        if(ticket.status === 'Aguardando') statusClass = 'st-aguardando';

        const row = `
            <tr>
                <td style="opacity:0.6;">#${ticket.id}</td>
                <td style="font-weight:500; color:white;">${ticket.assunto}</td>
                <td><span class="status-tag ${statusClass}">${ticket.status}</span></td>
                <td style="font-size:0.9rem; opacity:0.8;">${ticket.data}</td>
                <td class="text-end">
                    <button class="btn-icon" onclick="alert('Ver detalhes do #${ticket.id}')">➜</button>
                </td>
            </tr>
        `;
        tbody.innerHTML += row;
    });
}

function filtrarChamados() {
    const termo = document.getElementById('clientSearch').value.toLowerCase();
    const filtrados = meusChamados.filter(t => 
        t.assunto.toLowerCase().includes(termo) || 
        t.id.toString().includes(termo)
    );
    renderClientTable(filtrados);
}

// Inicializa
window.onload = () => {
    renderClientTable(meusChamados);
};