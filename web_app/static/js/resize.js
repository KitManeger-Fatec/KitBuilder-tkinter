// resizable.js
document.addEventListener("DOMContentLoaded", () => {
  const accentColor = "rgba(0,204,255,1)"; // usado apenas para cursor dinamicamente se quiser

  document.querySelectorAll(".resizable th").forEach((th, index) => {
    // cria o pegador visível
    const resizer = document.createElement("div");
    resizer.classList.add("resizer");
    th.appendChild(resizer);

    let startX = 0;
    let startWidth = 0;
    const minWidth = 60; // largura minima da coluna em px

    const onMouseMove = (e) => {
      // calcula nova largura
      const diff = e.pageX - startX;
      let newWidth = startWidth + diff;
      if (newWidth < minWidth) newWidth = minWidth;

      th.style.width = newWidth + "px";
    };

    const onMouseUp = () => {
      document.body.classList.remove("resizing");
      document.removeEventListener("mousemove", onMouseMove);
      document.removeEventListener("mouseup", onMouseUp);
      // restaura cursor
      document.body.style.cursor = "";
    };

    resizer.addEventListener("mousedown", (e) => {
      e.stopPropagation();
      startX = e.pageX;
      startWidth = th.offsetWidth;

      // adicionar classe que previne seleção de texto
      document.body.classList.add("resizing");
      // muda cursor globalmente pra ficar claro que está arrastando
      document.body.style.cursor = "col-resize";

      document.addEventListener("mousemove", onMouseMove);
      document.addEventListener("mouseup", onMouseUp);
    });

    // suporte básico a touch (opcional)
    resizer.addEventListener("touchstart", (e) => {
      if (e.touches.length !== 1) return;
      startX = e.touches[0].pageX;
      startWidth = th.offsetWidth;
      document.body.classList.add("resizing");
      document.addEventListener("touchmove", touchMove);
      document.addEventListener("touchend", touchEnd);
    });

    const touchMove = (e) => {
      const diff = e.touches[0].pageX - startX;
      let newWidth = startWidth + diff;
      if (newWidth < minWidth) newWidth = minWidth;
      th.style.width = newWidth + "px";
    };

    const touchEnd = () => {
      document.body.classList.remove("resizing");
      document.removeEventListener("touchmove", touchMove);
      document.removeEventListener("touchend", touchEnd);
    };
  });
});
