document.addEventListener("DOMContentLoaded", () => {
    const img = document.getElementById("produto-imagem");
    const logoPath = "/assets/images/Logo.jpg"; // imagem padrão

    img.src = logoPath;
    img.style.display = "block";

    // Adiciona evento de clique em cada linha da tabela
    document.querySelectorAll(".tabela-itens tbody tr").forEach(row => {
        row.addEventListener("click", async () => {
            const codigo = row.children[2]?.textContent?.trim(); // 3ª coluna (código)
            if (!codigo) {
                img.src = logoPath;
                return;
            }

            try {
                const response = await fetch(`http://127.0.0.1:8000/produto/${codigo}/imagem`);
                if (!response.ok) throw new Error("Erro ao buscar imagem");
                const data = await response.json();

                console.log("🔍 Imagem recebida:", data.imagem);
                img.src = data.imagem; // aplica a imagem retornada pela API
            } catch (error) {
                console.error("Erro ao carregar imagem:", error);
                img.src = logoPath;
            }
        });
    });
});
