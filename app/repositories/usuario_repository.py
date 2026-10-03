"""Repository: única camada que conversa com o banco via Flask-SQLAlchemy."""

from app.extensions import db
from app.models.usuarios import Usuario


class UsuarioRepository:
    @staticmethod
    def buscar_por_id(usuario_id):
        return db.session.get(Usuario, usuario_id)

    @staticmethod
    def buscar_por_nome_usuario(nome_usuario):
        return db.session.execute(
            db.select(Usuario).filter(
                db.func.lower(Usuario.nome_usuario) == nome_usuario.lower()
            )
        ).scalar_one_or_none()

    @staticmethod
    def salvar(usuario):
        db.session.add(usuario)
        db.session.commit()
        return usuario
