
document.addEventListener("DOMContentLoaded", function () {

    const pedidos = window.APP_DATA.pedidos || [];
    const ids_chefia = window.APP_DATA.ids_chefia || [];

    const btnTodos = document.getElementById("btn-todos");
    const btnAprovar = document.getElementById("btn-aprovar");

    // ======== FUNÇÃO DE FILTRAGEM ========
    function filtrarPedidos(tipo) {

        let filtrados = [];

        if (tipo === "aprovar") {
            // Só pedidos onde id_chefia presente na lista que o Renato pode aprovar
            filtrados = pedidos.filter(p => ids_chefia.includes(p.id_chefia) && p.aprovado === 0);
        } else {
            filtrados = pedidos;
        }

        console.log("PEDIDOS FILTRADOS:", filtrados);

        // 👉 Aqui você exibe seus pedidos na tela:
        renderizarPedidos(filtrados);
    }

    // ======== ATIVAR/DESATIVAR BOTÕES ========
    function ativarBotao(btnAtivo) {
        btnTodos.classList.remove("active");
        btnAprovar.classList.remove("active");

        btnAtivo.classList.add("active");
    }

    // ======== EVENTOS DOS BOTÕES ========
    btnTodos.addEventListener("click", function () {
        ativarBotao(btnTodos);
        filtrarPedidos("todos");
    });

    btnAprovar.addEventListener("click", function () {
        ativarBotao(btnAprovar);
        filtrarPedidos("aprovar");
    });

    // Carrega inicialmente “todos”
    filtrarPedidos("todos");
});

// ====== SUA FUNÇÃO DE RENDERIZAÇÃO DA TELA ======
function renderizarPedidos(lista) {
    // Aqui você já deve ter um método para preencher os pedidos.
    console.log("Renderizando:", lista);

    // Exemplo simples para debugging:
    // document.getElementById("lista-pedidos").innerText = JSON.stringify(lista, null, 2);
}
