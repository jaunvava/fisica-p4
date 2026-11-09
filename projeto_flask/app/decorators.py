from functools import wraps

from flask import flash, g, redirect, request, url_for


def login_obrigatorio(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if g.get("usuario") is None:
            flash("Faça login para continuar.", "erro")
            return redirect(url_for("auth.login", next=request.path))
        return view(*args, **kwargs)

    return wrapper
