// Token de autenticación para las llamadas fetch
window.apiToken = "sym-6565900705"; // asegúrate de que coincida con el de settings.json

function guardarToken(token) {
  localStorage.setItem("symctx_token", token);
}

function getAuthHeaders() {
  const token = localStorage.getItem("symctx_token");
  return {
    "Authorization": `Bearer ${token}`,
    "Content-Type": "application/json"
  };
}

function registrarEntrada() {
  const texto = document.getElementById("registroTexto").value;
  const token = localStorage.getItem("symctx_token");

  fetch("/symctx/register", {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${token}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ texto: texto })
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("resultadoRegistro").textContent = JSON.stringify(data, null, 2);
  })
  .catch(err => {
    document.getElementById("resultadoRegistro").textContent = "Error: " + err.message;
  });
}
