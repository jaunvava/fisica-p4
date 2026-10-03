document.addEventListener("DOMContentLoaded", () => {
  // Alertas: fechar no clique e sumir sozinhos após 4s
  document.querySelectorAll(".alerta").forEach((alerta) => {
    const fechar = () => {
      alerta.style.opacity = "0";
      setTimeout(() => alerta.remove(), 400);
    };
    alerta.querySelector(".alerta-fechar").addEventListener("click", fechar);
    setTimeout(fechar, 4000);
  });

  // Confirmação antes de excluir
  document.querySelectorAll(".form-excluir").forEach((form) => {
    form.addEventListener("submit", (e) => {
      if (!confirm(`Excluir o produto "${form.dataset.nome}"?`)) {
        e.preventDefault();
      }
    });
  });

  // Busca em tempo real na tabela
  const busca = document.getElementById("busca");
  if (busca) {
    const linhas = document.querySelectorAll("#tabela-produtos tbody tr");
    const semResultados = document.getElementById("sem-resultados");

    busca.addEventListener("input", () => {
      const termo = busca.value.trim().toLowerCase();
      let visiveis = 0;
      linhas.forEach((tr) => {
        const mostra = tr.textContent.toLowerCase().includes(termo);
        tr.hidden = !mostra;
        if (mostra) visiveis++;
      });
      semResultados.hidden = visiveis > 0;
    });
  }

  // Validação no cliente (o service valida de novo no servidor)
  const form = document.getElementById("form-produto");
  if (form) {
    const erro = document.getElementById("erro-form");

    form.addEventListener("submit", (e) => {
      const nome = form.nome.value.trim();
      const preco = parseFloat(form.preco.value);
      const quantidade = parseInt(form.quantidade.value, 10);
      const mensagens = [];

      form.querySelectorAll(".input").forEach((i) => i.classList.remove("invalido"));

      if (nome.length < 2) {
        mensagens.push("Nome deve ter ao menos 2 caracteres.");
        form.nome.classList.add("invalido");
      }
      if (isNaN(preco) || preco <= 0) {
        mensagens.push("Preço deve ser maior que zero.");
        form.preco.classList.add("invalido");
      }
      if (isNaN(quantidade) || quantidade < 0) {
        mensagens.push("Quantidade não pode ser negativa.");
        form.quantidade.classList.add("invalido");
      }

      if (mensagens.length) {
        e.preventDefault();
        erro.textContent = mensagens.join(" ");
        erro.hidden = false;
      }
    });
  }
});
