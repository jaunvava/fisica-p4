from app.extensions import db
from app.models.produto import Produto


class ProdutoRepository:
    @staticmethod
    def listar_todos():
        return db.session.execute(
            db.select(Produto).order_by(Produto.nome)
        ).scalars().all()

    @staticmethod
    def buscar_por_id(produto_id):
        return db.session.get(Produto, produto_id)

    @staticmethod
    def buscar_por_nome(nome):
        return db.session.execute(
            db.select(Produto).filter(db.func.lower(Produto.nome) == nome.lower())
        ).scalar_one_or_none()

    @staticmethod
    def salvar(produto):
        db.session.add(produto)
        db.session.commit()
        return produto

    @staticmethod
    def atualizar():
        db.session.commit()

    @staticmethod
    def excluir(produto):
        db.session.delete(produto)
        db.session.commit()
