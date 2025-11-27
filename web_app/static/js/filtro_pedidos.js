document.addEventListener("DOMContentLoaded", async function () {

    let pedidos = window.APP_DATA.pedidos || []; 
    const idUser = window.APP_DATA.user_id;
    const btnTodos = document.getElementById("btn-todos");
    const btnAprovar = document.getElementById("btn-aprovar");

    let idsAprovar = [];

    // 1️⃣ CARREGA IDS DA API
    async function carregarIdsAprovar() {
        try {
            const response = await fetch(`http://127.0.0.1:8000/api/pedidos/para_aprovar/${idUser}`);
            if (!response.ok) throw new Error("Erro ao consultar API");

            const data = await response.json();

            // extrai somente os ids: [8, 12, 99]
            idsAprovar = data.map(item => item.id_pedido);

            console.log("📌 IDs liberados pela API:", idsAprovar);

        } catch (err) {
            console.error("Erro ao carregar IDs:", err);
        }
    }

    // 2️⃣ APLICA O FILTRO
    function filtrarPedidos(tipo) {
        let filtrados = [];

        if (tipo === "aprovar") {
            filtrados = pedidos.filter(p =>
                idsAprovar.includes(p.id_pedido)
            );
        } else {
            filtrados = pedidos; // sem filtro
        }

        console.log("👌 PEDIDOS FILTRADOS:", filtrados);
        renderizarPedidos(filtrados);
    }

    // 3️⃣ ESTILO DO BOTÃO
    function ativarBotao(btnAtivo) {
        btnTodos.classList.remove("active");
        btnAprovar.classList.remove("active");
        btnAtivo.classList.add("active");
    }

    // 4️⃣ EVENTOS DOS BOTÕES
    btnTodos.addEventListener("click", () => {
        ativarBotao(btnTodos);
        filtrarPedidos("todos");
    });

    btnAprovar.addEventListener("click", () => {
        ativarBotao(btnAprovar);
        filtrarPedidos("aprovar");
    });

    // 5️⃣ PRIMEIRO CARREGA A API, DEPOIS FILTRA
    await carregarIdsAprovar();
    filtrarPedidos("todos");
});


function renderizarPedidos(lista) {
    const container = document.getElementById("pedidos-list");
    const idsLiberados = window.APP_DATA.ids_chefia.map(c => c.id_pedido);
    const pedidoSelecionado = window.APP_DATA.pedido_selecionado;
    const userId = window.APP_DATA.user_id;

    if (!container) {
        console.error("❌ ERRO: #pedidos-list não encontrado.");
        return;
    }

    // Mantém apenas o título
    container.innerHTML = `<h3>Pedidos</h3>`;

    if (lista.length === 0) {
        container.innerHTML += `<p class="nenhum">Nenhum pedido encontrado.</p>`;
        return;
    }

    lista.forEach(p => {
        const ehChefia = idsLiberados.includes(p.id_pedido);
        const ehSelecionado = p.id_pedido === pedidoSelecionado;

        const divClasses = `
            pedido-item
            ${ehChefia ? "chefia" : ""}
            ${ehSelecionado ? "selecionado" : ""}
        `;

        container.innerHTML += `
            <a class="pedido-link"
                href="/dashboard/${userId}/pedido/${p.id_pedido}"
                onclick="carregarChefias(${p.id_pedido})">
                <div class="${divClasses}">
                    <span><b>Pedido #${p.id_pedido}</b> — ${p.nome_projeto} - ${p.nome_lista}</span>
                </div>
            </a>
        `;
    });
}

