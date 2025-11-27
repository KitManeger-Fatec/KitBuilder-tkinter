// static/js/chefias.js

function carregarChefias() {

    const idPedido = APP_DATA.pedido_selecionado;
    const chefias = APP_DATA.ids_chefia;   // 🟢 Já vindo do backend Flask

    enviarLog(`Carregando chefias do pedido ${idPedido} direto do backend (sem API)`);
    
    const container = document.getElementById("chefias-container");
    container.innerHTML = "";

    if (!chefias || chefias.length === 0) {
        enviarLog("Nenhuma chefia encontrada.");
        container.innerHTML = "<p style='color:#bbb;'>Nenhum dado.</p>";
        return;
    }

    enviarLog(`Chefias recebidas: ${JSON.stringify(chefias)}`);

    chefias.forEach(c => {
        const div = document.createElement("div");
        div.classList.add("chefe-item");

        const statusMap = {
            0: "Pendente",
            1: "Aprovado",
            2: "Ressalvas",
            3: "Reprovado"
        };

        const status = statusMap[c.aprovado] ?? "Status desconhecido";

        div.innerHTML = `
            <div class="chefe-nome">${c.nome_chefia}</div>
            <div class="chefe-nivel">Nível: ${c.nivel_chefia}</div>
            <div class="chefe-status ${status.toLowerCase()}">${status}</div>
        `;

        container.appendChild(div);
    });

    enviarLog("Chefias renderizadas com sucesso.");
}


// 🟢 Executa automaticamente ao carregar a página
document.addEventListener("DOMContentLoaded", () => {
    enviarLog("chefias.js carregado — chamando carregarChefias()");
    carregarChefias();
});
