from database import usuarios_tbl, disciplinas_tbl, atividades_tbl, progresso_tbl
from models import TipoUsuario, StatusAtividade
from typing import Optional, List, Dict
from datetime import datetime

# FUNÇÕES AUXILIARES

def gerar_proximo_id(tabela) -> int:
    """Gera o próximo ID único para uma tabela"""
    registros = tabela.all()
    if not registros:
        return 1
    return max([r.get('id', 0) for r in registros]) + 1

# CRUD - USUÁRIOS

def criar_usuario(nome: str, tipo: str, email: str, senha: str) -> Dict:
    # Valida se email já existe
    usuario_existente = usuarios_tbl.search(lambda x: x['email'] == email)
    if usuario_existente:
        return None
    
    usuario_id = gerar_proximo_id(usuarios_tbl)
    novo_usuario = {
        'id': usuario_id,
        'nome': nome,
        'tipo': tipo,
        'email': email,
        'senha': senha,  
        'criado_em': datetime.now().isoformat()
    }
    usuarios_tbl.insert(novo_usuario)
    return novo_usuario

def listar_usuarios() -> List[Dict]:
    return usuarios_tbl.all()

def obter_usuario_por_id(usuario_id: int) -> Optional[Dict]:
    resultado = usuarios_tbl.search(lambda x: x['id'] == usuario_id)
    return resultado[0] if resultado else None

def obter_usuario_por_email(email: str) -> Optional[Dict]:
    resultado = usuarios_tbl.search(lambda x: x['email'] == email)
    return resultado[0] if resultado else None

def atualizar_usuario(usuario_id: int, nome: Optional[str] = None, email: Optional[str] = None) -> bool:
    """Atualiza dados do usuário"""
    usuario = obter_usuario_por_id(usuario_id)
    if not usuario:
        return False
    
    atualizacoes = {}
    if nome:
        atualizacoes['nome'] = nome
    if email:
        outro_usuario = usuarios_tbl.search(lambda x: x['email'] == email and x['id'] != usuario_id)
        if outro_usuario:
            return False
        atualizacoes['email'] = email
    
    usuarios_tbl.update(atualizacoes, lambda x: x['id'] == usuario_id)
    return True

def deletar_usuario(usuario_id: int) -> bool:
    resultado = usuarios_tbl.remove(lambda x: x['id'] == usuario_id)
    return len(resultado) > 0

# CRUD - DISCIPLINAS

def criar_disciplina(nome: str, professor_id: int, descricao: Optional[str] = None) -> Optional[Dict]:
    # Valida se professor existe
    professor = obter_usuario_por_id(professor_id)
    if not professor or professor['tipo'] != TipoUsuario.PROFESSOR:
        return None
    
    disciplina_id = gerar_proximo_id(disciplinas_tbl)
    nova_disciplina = {
        'id': disciplina_id,
        'nome': nome,
        'professor_id': professor_id,
        'descricao': descricao,
        'alunos_matriculados': [],
        'criado_em': datetime.now().isoformat()
    }
    disciplinas_tbl.insert(nova_disciplina)
    return nova_disciplina

def listar_disciplinas() -> List[Dict]:
    return disciplinas_tbl.all()

def obter_disciplina_por_id(disciplina_id: int) -> Optional[Dict]:
    resultado = disciplinas_tbl.search(lambda x: x['id'] == disciplina_id)
    return resultado[0] if resultado else None

def listar_disciplinas_professor(professor_id: int) -> List[Dict]:
    return disciplinas_tbl.search(lambda x: x['professor_id'] == professor_id)

def atualizar_disciplina(disciplina_id: int, nome: Optional[str] = None, descricao: Optional[str] = None) -> bool:
    disciplina = obter_disciplina_por_id(disciplina_id)
    if not disciplina:
        return False
    
    atualizacoes = {}
    if nome:
        atualizacoes['nome'] = nome
    if descricao is not None:
        atualizacoes['descricao'] = descricao
    
    disciplinas_tbl.update(atualizacoes, lambda x: x['id'] == disciplina_id)
    return True

def matricular_aluno(disciplina_id: int, aluno_id: int) -> bool:
    disciplina = obter_disciplina_por_id(disciplina_id)
    aluno = obter_usuario_por_id(aluno_id)
    
    if not disciplina or not aluno or aluno['tipo'] != TipoUsuario.ALUNO:
        return False
    
    if aluno_id not in disciplina.get('alunos_matriculados', []):
        alunos = disciplina.get('alunos_matriculados', [])
        alunos.append(aluno_id)
        disciplinas_tbl.update({'alunos_matriculados': alunos}, lambda x: x['id'] == disciplina_id)
    
    return True

def desmatricular_aluno(disciplina_id: int, aluno_id: int) -> bool:
    disciplina = obter_disciplina_por_id(disciplina_id)
    if not disciplina or aluno_id not in disciplina.get('alunos_matriculados', []):
        return False
    
    alunos = disciplina.get('alunos_matriculados', [])
    alunos.remove(aluno_id)
    disciplinas_tbl.update({'alunos_matriculados': alunos}, lambda x: x['id'] == disciplina_id)
    return True

def deletar_disciplina(disciplina_id: int) -> bool:
    resultado = disciplinas_tbl.remove(lambda x: x['id'] == disciplina_id)
    return len(resultado) > 0

# CRUD - ATIVIDADES

def criar_atividade(titulo: str, disciplina_id: int, data_entrega: str, descricao: Optional[str] = None, prioridade: str = "media") -> Optional[Dict]:
    # Valida se a disciplina existe
    disciplina = obter_disciplina_por_id(disciplina_id)
    if not disciplina:
        return None
    
    # Valida se a data de entrega não é no passado
    try:
        data_entrega_obj = datetime.strptime(data_entrega, "%Y-%m-%d").date()
        data_hoje = datetime.now().date()
        if data_entrega_obj < data_hoje:
            return None 
    except ValueError:
        return None  
    
    atividade_id = gerar_proximo_id(atividades_tbl)
    nova_atividade = {
        'id': atividade_id,
        'titulo': titulo,
        'descricao': descricao,
        'data_entrega': data_entrega,
        'disciplina_id': disciplina_id,
        'prioridade': prioridade,
        'criado_em': datetime.now().isoformat()
    }
    atividades_tbl.insert(nova_atividade)
    
    # Cria progresso para cada aluno matriculado
    for aluno_id in disciplina.get('alunos_matriculados', []):
        criar_progresso(aluno_id, atividade_id)
    
    return nova_atividade

def listar_atividades() -> List[Dict]:
    return atividades_tbl.all()

def obter_atividade_por_id(atividade_id: int) -> Optional[Dict]:
    resultado = atividades_tbl.search(lambda x: x['id'] == atividade_id)
    return resultado[0] if resultado else None

def listar_atividades_disciplina(disciplina_id: int) -> List[Dict]:
    return atividades_tbl.search(lambda x: x['disciplina_id'] == disciplina_id)

def atualizar_atividade(atividade_id: int, titulo: Optional[str] = None, descricao: Optional[str] = None, data_entrega: Optional[str] = None, prioridade: Optional[str] = None) -> bool:
    atividade = obter_atividade_por_id(atividade_id)
    if not atividade:
        return False
    
    atualizacoes = {}
    if titulo:
        atualizacoes['titulo'] = titulo
    if descricao is not None:
        atualizacoes['descricao'] = descricao
    if data_entrega:
        atualizacoes['data_entrega'] = data_entrega
    if prioridade:
        atualizacoes['prioridade'] = prioridade
    
    atividades_tbl.update(atualizacoes, lambda x: x['id'] == atividade_id)
    return True

def deletar_atividade(atividade_id: int) -> bool:
    progresso_tbl.remove(lambda x: x['atividade_id'] == atividade_id)
    resultado = atividades_tbl.remove(lambda x: x['id'] == atividade_id)
    return len(resultado) > 0

# CRUD - PROGRESSO

def criar_progresso(aluno_id: int, atividade_id: int, status: str = "A_FAZER") -> Optional[Dict]:
    """Cria um registro de progresso"""
    aluno = obter_usuario_por_id(aluno_id)
    atividade = obter_atividade_por_id(atividade_id)
    
    if not aluno or not atividade:
        return None
    
    progresso_id = gerar_proximo_id(progresso_tbl)
    novo_progresso = {
        'id': progresso_id,
        'aluno_id': aluno_id,
        'atividade_id': atividade_id,
        'status': status,
        'data_criacao': datetime.now().isoformat(),
        'data_atualizacao': datetime.now().isoformat()
    }
    progresso_tbl.insert(novo_progresso)
    return novo_progresso

def listar_progresso_aluno(aluno_id: int) -> List[Dict]:
    return progresso_tbl.search(lambda x: x['aluno_id'] == aluno_id)

def obter_progresso(aluno_id: int, atividade_id: int) -> Optional[Dict]:
    resultado = progresso_tbl.search(lambda x: x['aluno_id'] == aluno_id and x['atividade_id'] == atividade_id)
    return resultado[0] if resultado else None

def atualizar_status_progresso(aluno_id: int, atividade_id: int, novo_status: str) -> bool:
    progresso = obter_progresso(aluno_id, atividade_id)
    if not progresso:
        return False
    
    progresso_tbl.update(
        {
            'status': novo_status,
            'data_atualizacao': datetime.now().isoformat()
        },
        lambda x: x['aluno_id'] == aluno_id and x['atividade_id'] == atividade_id
    )
    return True

def listar_progresso_disciplina(disciplina_id: int) -> List[Dict]:
    atividades = listar_atividades_disciplina(disciplina_id)
    atividade_ids = [a['id'] for a in atividades]
    return progresso_tbl.search(lambda x: x['atividade_id'] in atividade_ids)
