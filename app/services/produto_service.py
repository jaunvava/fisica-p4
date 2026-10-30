from decimal import Decimal, InvalidOperation

from app.models.produto import Produto
from app.repositories.produto_repository import ProdutoRepository


class RegraNegocioError(Exception):
    pass


class ProdutoService:
    @staticmethod
    def listar():
        return ProdutoRepository.listar_todos()

    @staticmethod
    def obter(produto_id):
        produto = ProdutoRepository.buscar_por_id(produto_id)
        if produto is None:
            raise RegraNegocioError("Produto não encontrado.")
        return produto

    @staticmethod
    def criar(dados):
        nome, descricao, preco, quantidade = ProdutoService._validar(dados)

        if ProdutoRepository.buscar_por_nome(nome):
            raise RegraNegocioError(f"Já existe um produto chamado '{nome}'.")

        produto = Produto(
            nome=nome, descricao=descricao, preco=preco, quantidade=quantidade
        )
        return ProdutoRepository.salvar(produto)

    @staticmethod
    def atualizar(produto_id, dados):
        produto = ProdutoService.obter(produto_id)
        nome, descricao, preco, quantidade = ProdutoService._validar(dados)

        existente = ProdutoRepository.buscar_por_nome(nome)
        if existente and existente.id != produto.id:
            raise RegraNegocioError(f"Já existe um produto chamado '{nome}'.")

        produto.nome = nome
        produto.descricao = descricao
        produto.preco = preco
        produto.quantidade = quantidade
        ProdutoRepository.atualizar()
        return produto

    @staticmethod
    def excluir(produto_id):
        produto = ProdutoService.obter(produto_id)
        ProdutoRepository.excluir(produto)

    @staticmethod
    def resumo_estoque(produtos):
        total_itens = sum(p.quantidade for p in produtos)
        valor_total = sum((p.preco * p.quantidade for p in produtos), Decimal("0"))
        return {"total_itens": total_itens, "valor_total": valor_total}

    @staticmethod
    def _validar(dados):
        nome = (dados.get("nome") or "").strip()
        descricao = (dados.get("descricao") or "").strip()

        if len(nome) < 2:
            raise RegraNegocioError("O nome deve ter pelo menos 2 caracteres.")

        try:
            preco = Decimal(str(dados.get("preco", "")).replace(",", "."))
        except InvalidOperation:
            raise RegraNegocioError("Preço inválido.")
        if preco <= 0:
            raise RegraNegocioError("O preço deve ser maior que zero.")

        try:
            quantidade = int(dados.get("quantidade", 0))
        except (TypeError, ValueError):
            raise RegraNegocioError("Quantidade inválida.")
        if quantidade < 0:
            raise RegraNegocioError("A quantidade não pode ser negativa.")

        return nome, descricao, preco, quantidade
