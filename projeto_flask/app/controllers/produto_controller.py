from flask import Blueprint, flash, redirect, render_template, request, url_for
from app.decorators import login_obrigatorio
from app.services.produto_service import ProdutoService, RegraNegocioError

produto_bp = Blueprint("produtos", __name__, url_prefix="/produtos")


@produto_bp.before_request
@login_obrigatorio
def exigir_login():

    pass


@produto_bp.route("/")
def listar():
    produtos = ProdutoService.listar()
    resumo = ProdutoService.resumo_estoque(produtos)
    return render_template("produtos/lista.html", produtos=produtos, resumo=resumo)


@produto_bp.route("/novo", methods=["GET", "POST"])
def criar():
    if request.method == "POST":
        try:
            ProdutoService.criar(request.form)
            flash("Produto cadastrado com sucesso!", "sucesso")
            return redirect(url_for("produtos.listar"))
        except RegraNegocioError as e:
            flash(str(e), "erro")
    return render_template("produtos/form.html", produto=None, dados=request.form)


@produto_bp.route("/<int:produto_id>/editar", methods=["GET", "POST"])
def editar(produto_id):
    try:
        produto = ProdutoService.obter(produto_id)
    except RegraNegocioError as e:
        flash(str(e), "erro")
        return redirect(url_for("produtos.listar"))

    if request.method == "POST":
        try:
            ProdutoService.atualizar(produto_id, request.form)
            flash("Produto atualizado com sucesso!", "sucesso")
            return redirect(url_for("produtos.listar"))
        except RegraNegocioError as e:
            flash(str(e), "erro")
    return render_template("produtos/form.html", produto=produto, dados=request.form)


@produto_bp.route("/<int:produto_id>/excluir", methods=["POST"])
def excluir(produto_id):
    try:
        ProdutoService.excluir(produto_id)
        flash("Produto excluído.", "sucesso")
    except RegraNegocioError as e:
        flash(str(e), "erro")
    return redirect(url_for("produtos.listar"))
