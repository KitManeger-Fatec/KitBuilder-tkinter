// static/js/logger.js

function enviarLog(msg, nivel="info") {
    fetch("http://127.0.0.1:8000/log", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mensagem: msg, nivel })
    }).catch(err => console.error("Erro ao enviar log:", err));
}

/* 
// OPCIONAL: para interceptar todos console.log:
const oldLog = console.log;
console.log = function (...args) {
    oldLog(...args);
    logPython(args.join(" "), "info");
};

// OPCIONAL: interceptar todos console.error:
const oldError = console.error;
console.error = function (...args) {
    oldError(...args);
    logPython(args.join(" "), "error");
};
*/
