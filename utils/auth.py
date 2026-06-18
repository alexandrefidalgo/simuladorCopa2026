import hashlib


def hash_senha(senha: str) -> str:
    """Retorna hash SHA-256 da senha (projeto educacional)."""
    return hashlib.sha256(senha.encode()).hexdigest()


def verificar_senha(senha: str, senha_hash: str) -> bool:
    """Verifica se a senha confere com o hash armazenado."""
    return hash_senha(senha) == senha_hash
