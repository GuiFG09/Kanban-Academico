from typing import Optional

def validar_credenciais(usuario: dict, senha: str) -> bool:
    """Valida se a senha está correta (texto plano para MVP)"""
    if usuario is None:
        return False
    return usuario.get("senha") == senha
