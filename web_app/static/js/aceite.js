async function alterarAceite(linhaPedido, novoValor) {

    const resp = await fetch(`${window.APP_DATA.API_URL}/pedido_item/aceite/${linhaPedido}`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ aceito: novoValor })
    });

    if (resp.ok) {

        // Atualiza o item no front
        const item = window.APP_DATA.itens.find(i => i.linha_pedido === linhaPedido);

        if (item) {
            item.aceito = novoValor;
            enviarLog(`Item ATUALIZADO no front: linha_pedido=${linhaPedido}, aceito=${novoValor}`, "info");
        } else {
            enviarLog(`❌ Item NÃO encontrado no front: linha_pedido=${linhaPedido}`, "error");
        }

    } else {
        alert("Erro ao atualizar aceite.");
    }
}

async function finalizarAprovacao() {
    const itens = window.APP_DATA.itens;
    const user = window.APP_DATA.funcionario.nome;
    const userId = window.APP_DATA.user_id;
    const pedido_id = window.APP_DATA.pedido_selecionado;

    const aprovados = itens.filter(i => i.aceito === 1);
    const removidos = itens.filter(i => i.aceito === 0);
    enviarLog("ITENS: " + JSON.stringify(itens), "info");

    itens.forEach(i => {
        enviarLog(`Tipo: ${typeof i.aceito} | Valor: ${i.aceito}`, "info");
    });

    enviarLog(`user: ${user} | pedido_id: ${pedido_id} | userId: ${userId}`, "info");


    // Caso 1: nenhum removido → todos aprovados
    if (removidos.length === 0) {
        try {
            const r = await fetch(`${window.APP_DATA.API_URL}/AprovaPedido`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    "id_pedido": pedido_id, 
                    "id_chefia": userId,
                    "aprovado": 1 })
            });

            if (!r.ok) throw new Error("Erro ao aprovar");

            alert("Pedido aprovado com sucesso!");
            location.reload();

        } catch (err) {
            console.error(err);
            alert("Erro ao aprovar.");
        }
        return;
    }

    // Caso 2: todos removidos → reprovado
    if (aprovados.length === 0 && removidos.length > 0) {
        // Aqui você define: pedido_reprovado = 3
        await fetch(`${window.APP_DATA.API_URL}/AprovaPedido`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                "id_pedido": pedido_id, 
                "id_chefia": userId,
                "aprovado": 3 })
        });

        enviarLog(`Pedido ${pedido_id} reprovado — todos itens removidos`);
        alert("Pedido reprovado — todos os itens foram removidos.");

        location.reload();
        return;
    }

    // Caso 3: mistura (tem removido e tem aprovado) → ressalva
    if (aprovados.length > 0 && removidos.length > 0) {

        const payload = { pedido_id, removidos, user };

        try {
            const r = await fetch(`${window.APP_DATA.API_URL}/AprovaPedido`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ 
                    "id_pedido": pedido_id, 
                    "id_chefia": userId,
                    "aprovado": 2 })
            });

            if (!r.ok) throw new Error("Erro ao gerar ressalva");

            enviarLog(`Pedido ${pedido_id} em ressalva — itens removidos: ${JSON.stringify(removidos)}`);

            alert("Pedido em ressalva — alguns itens foram removidos.");
            location.reload();

        } catch (err) {
            console.error(err);
            alert("Erro ao gerar ressalva.");
        }
        return;
    }
}
