from app.models.usuarios import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.services.produto_service import RegraNegocioError



class AuthService:
    @staticmethod
    def obter_por_id(usuario_id):
        return UsuarioRepository.buscar_por_id(usuario_id)

    @staticmethod
    def autenticar(nome_usuario, senha):
        nome_usuario = (nome_usuario or "").strip()
        usuario = UsuarioRepository.buscar_por_nome_usuario(nome_usuario) if nome_usuario else None

        if usuario is None or not usuario.verificar_senha(senha or ""):
            raise RegraNegocioError("Usuário ou senha inválidos.")
        return usuario

    @staticmethod
    def registrar(dados):
        nome_usuario = (dados.get("nome_usuario") or "").strip()
        senha = dados.get("senha") or ""
        confirmacao = dados.get("confirmar_senha") or ""

        if len(nome_usuario) < 3:
            raise RegraNegocioError("O usuário deve ter pelo menos 3 caracteres.")
        if len(senha) < 6:
            raise RegraNegocioError("A senha deve ter pelo menos 6 caracteres.")
        if senha != confirmacao:
            raise RegraNegocioError("As senhas não conferem.")
        if UsuarioRepository.buscar_por_nome_usuario(nome_usuario):
            raise RegraNegocioError(f"O usuário '{nome_usuario}' já existe.")

        usuario = Usuario(nome_usuario=nome_usuario)
        usuario.definir_senha(senha)
        return UsuarioRepository.salvar(usuario)
