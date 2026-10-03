from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app.services.auth_service import AuthService
from app.services.produto_service import RegraNegocioError

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@auth_bp.before_app_request
def carregar_usuario_logado():

    usuario_id = session.get("usuario_id")
    g.usuario = AuthService.obter_por_id(usuario_id) if usuario_id else None


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if g.usuario:
        return redirect(url_for("produtos.listar"))

    if request.method == "POST":
        try:
            usuario = AuthService.autenticar(
                request.form.get("nome_usuario"), request.form.get("senha")
            )
            session.clear()
            session["usuario_id"] = usuario.id
            flash(f"Bem-vindo, {usuario.nome_usuario}!", "sucesso")

            # volta pra tela de login 
            destino = request.args.get("next", "")
            if not destino.startswith("/") or destino.startswith("//"):
                destino = url_for("produtos.listar")
            return redirect(destino)
        except RegraNegocioError as e:
            flash(str(e), "erro")
    return render_template("login/login.html", dados=request.form)


@auth_bp.route("/registrar", methods=["GET", "POST"])
def registrar():
    if g.usuario:
        return redirect(url_for("produtos.listar"))

    if request.method == "POST":
        try:
            AuthService.registrar(request.form)
            flash("Conta criada! Faça login.", "sucesso")
            return redirect(url_for("auth.login"))
        except RegraNegocioError as e:
            flash(str(e), "erro")
    return render_template("login/registrar.html", dados=request.form)


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Você saiu do sistema.", "sucesso")
    return redirect(url_for("auth.login"))
