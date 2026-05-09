from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from typing import List
from models import (
    UsuarioCreate, UsuarioUpdate, UsuarioResponse,
    DisciplinaCreate, DisciplinaUpdate, DisciplinaResponse,
    AtividadeCreate, AtividadeUpdate, AtividadeResponse,
    ProgressoCreate, ProgressoUpdate, ProgressoResponse,
    TipoUsuario
)
from crud import (
    criar_usuario, listar_usuarios, obter_usuario_por_id, atualizar_usuario, deletar_usuario, obter_usuario_por_email,
    criar_disciplina, listar_disciplinas, obter_disciplina_por_id, atualizar_disciplina, deletar_disciplina, matricular_aluno, desmatricular_aluno, listar_disciplinas_professor,
    criar_atividade, listar_atividades, obter_atividade_por_id, atualizar_atividade, deletar_atividade, listar_atividades_disciplina,
    criar_progresso, listar_progresso_aluno, obter_progresso, atualizar_status_progresso, listar_progresso_disciplina
)
from auth import validar_credenciais

# INICIALIZA A APP

app = FastAPI(
    title="Kanban Acadêmico API",
    description="API para gerenciar atividades e progresso acadêmico",
    version="1.0.0"
)

# ROTAS - AUTENTICAÇÃO

@app.post("/login", response_model=UsuarioResponse, tags=["Autenticação"])
def login(email: str, senha: str):
    usuario = obter_usuario_por_email(email)
    
    if not usuario or not validar_credenciais(usuario, senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos"
        )
    
    return UsuarioResponse(
        id=usuario['id'],
        nome=usuario['nome'],
        tipo=usuario['tipo'],
        email=usuario['email']
    )

# ROTAS - USUÁRIOS

@app.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED, tags=["Usuários"])
def registrar_usuario(usuario: UsuarioCreate):
    """
    Registra um novo usuário (professor ou aluno)
    
    **Tipos de usuário:**
    - professor
    - aluno
    """
    novo_usuario = criar_usuario(usuario.nome, usuario.tipo, usuario.email, usuario.senha)
    
    if novo_usuario is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email já cadastrado"
        )
    
    return UsuarioResponse(
        id=novo_usuario['id'],
        nome=novo_usuario['nome'],
        tipo=novo_usuario['tipo'],
        email=novo_usuario['email']
    )

@app.get("/usuarios", response_model=List[UsuarioResponse], tags=["Usuários"])
def listar_todos_usuarios():
    usuarios = listar_usuarios()
    return [
        UsuarioResponse(id=u['id'], nome=u['nome'], tipo=u['tipo'], email=u['email'])
        for u in usuarios
    ]

@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse, tags=["Usuários"])
def obter_usuario(usuario_id: int):
    usuario = obter_usuario_por_id(usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    return UsuarioResponse(
        id=usuario['id'],
        nome=usuario['nome'],
        tipo=usuario['tipo'],
        email=usuario['email']
    )

@app.put("/usuarios/{usuario_id}", response_model=UsuarioResponse, tags=["Usuários"])
def atualizar_dados_usuario(usuario_id: int, dados: UsuarioUpdate):
    atualizado = atualizar_usuario(usuario_id, dados.nome, dados.email)
    if not atualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    usuario = obter_usuario_por_id(usuario_id)
    return UsuarioResponse(
        id=usuario['id'],
        nome=usuario['nome'],
        tipo=usuario['tipo'],
        email=usuario['email']
    )

@app.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Usuários"])
def deletar_usuario_endpoint(usuario_id: int):
    deletado = deletar_usuario(usuario_id)
    if not deletado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )

# ROTAS - DISCIPLINAS

@app.post("/disciplinas", response_model=DisciplinaResponse, status_code=status.HTTP_201_CREATED, tags=["Disciplinas"])
def criar_nova_disciplina(disciplina: DisciplinaCreate):
    nova_disciplina = criar_disciplina(disciplina.nome, disciplina.professor_id, disciplina.descricao)
    
    if nova_disciplina is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Professor inválido"
        )
    
    return DisciplinaResponse(
        id=nova_disciplina['id'],
        nome=nova_disciplina['nome'],
        professor_id=nova_disciplina['professor_id'],
        alunos_matriculados=nova_disciplina.get('alunos_matriculados', [])
    )

@app.get("/disciplinas", response_model=List[DisciplinaResponse], tags=["Disciplinas"])
def listar_todas_disciplinas():
    disciplinas = listar_disciplinas()
    return [
        DisciplinaResponse(
            id=d['id'],
            nome=d['nome'],
            professor_id=d['professor_id'],
            alunos_matriculados=d.get('alunos_matriculados', [])
        )
        for d in disciplinas
    ]

@app.get("/disciplinas/professor/{professor_id}", response_model=List[DisciplinaResponse], tags=["Disciplinas"])
def listar_disciplinas_do_professor(professor_id: int):
    disciplinas = listar_disciplinas_professor(professor_id)
    return [
        DisciplinaResponse(
            id=d['id'],
            nome=d['nome'],
            professor_id=d['professor_id'],
            alunos_matriculados=d.get('alunos_matriculados', [])
        )
        for d in disciplinas
    ]

@app.get("/disciplinas/{disciplina_id}", response_model=DisciplinaResponse, tags=["Disciplinas"])
def obter_disciplina(disciplina_id: int):
    disciplina = obter_disciplina_por_id(disciplina_id)
    if not disciplina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disciplina não encontrada"
        )
    
    return DisciplinaResponse(
        id=disciplina['id'],
        nome=disciplina['nome'],
        professor_id=disciplina['professor_id'],
        alunos_matriculados=disciplina.get('alunos_matriculados', [])
    )

@app.put("/disciplinas/{disciplina_id}", response_model=DisciplinaResponse, tags=["Disciplinas"])
def atualizar_disciplina_endpoint(disciplina_id: int, dados: DisciplinaUpdate):
    disciplina = obter_disciplina_por_id(disciplina_id)
    if not disciplina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disciplina não encontrada"
        )
    
    atualizado = atualizar_disciplina(disciplina_id, dados.nome, dados.descricao)
    if not atualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disciplina não encontrada"
        )
    
    disciplina = obter_disciplina_por_id(disciplina_id)
    return DisciplinaResponse(
        id=disciplina['id'],
        nome=disciplina['nome'],
        professor_id=disciplina['professor_id'],
        alunos_matriculados=disciplina.get('alunos_matriculados', [])
    )

@app.post("/disciplinas/{disciplina_id}/matricular", status_code=status.HTTP_200_OK, tags=["Disciplinas"])
def matricular_aluno_endpoint(disciplina_id: int, aluno_id: int):
    disciplina = obter_disciplina_por_id(disciplina_id)
    if not disciplina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disciplina não encontrada"
        )
    
    matriculado = matricular_aluno(disciplina_id, aluno_id)
    if not matriculado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aluno inválido ou já matriculado"
        )
    
    return {"mensagem": "Aluno matriculado com sucesso"}

@app.delete("/disciplinas/{disciplina_id}/desmatricular/{aluno_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Disciplinas"])
def desmatricular_aluno_endpoint(disciplina_id: int, aluno_id: int):
    disciplina = obter_disciplina_por_id(disciplina_id)
    if not disciplina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disciplina não encontrada"
        )
    
    desmatriculado = desmatricular_aluno(disciplina_id, aluno_id)
    if not desmatriculado:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aluno não encontrado nesta disciplina"
        )

@app.delete("/disciplinas/{disciplina_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Disciplinas"])
def deletar_disciplina_endpoint(disciplina_id: int):
    disciplina = obter_disciplina_por_id(disciplina_id)
    if not disciplina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disciplina não encontrada"
        )
    
    deletado = deletar_disciplina(disciplina_id)
    if not deletado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disciplina não encontrada"
        )

# ROTAS - ATIVIDADES

@app.post("/atividades", response_model=AtividadeResponse, status_code=status.HTTP_201_CREATED, tags=["Atividades"])
def criar_nova_atividade(atividade: AtividadeCreate):
    disciplina = obter_disciplina_por_id(atividade.disciplina_id)
    if not disciplina:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Disciplina inválida"
        )
    
    nova_atividade = criar_atividade(
        atividade.titulo,
        atividade.disciplina_id,
        atividade.data_entrega,
        atividade.descricao,
        atividade.prioridade
    )
    
    if nova_atividade is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Data de entrega inválida ou no passado"
        )
    
    return AtividadeResponse(
        id=nova_atividade['id'],
        titulo=nova_atividade['titulo'],
        descricao=nova_atividade['descricao'],
        data_entrega=nova_atividade['data_entrega'],
        disciplina_id=nova_atividade['disciplina_id'],
        prioridade=nova_atividade['prioridade']
    )

@app.get("/atividades", response_model=List[AtividadeResponse], tags=["Atividades"])
def listar_todas_atividades():
    atividades = listar_atividades()
    return [
        AtividadeResponse(
            id=a['id'],
            titulo=a['titulo'],
            descricao=a['descricao'],
            data_entrega=a['data_entrega'],
            disciplina_id=a['disciplina_id'],
            prioridade=a['prioridade']
        )
        for a in atividades
    ]

@app.get("/atividades/disciplina/{disciplina_id}", response_model=List[AtividadeResponse], tags=["Atividades"])
def listar_atividades_da_disciplina(disciplina_id: int):
    atividades = listar_atividades_disciplina(disciplina_id)
    return [
        AtividadeResponse(
            id=a['id'],
            titulo=a['titulo'],
            descricao=a['descricao'],
            data_entrega=a['data_entrega'],
            disciplina_id=a['disciplina_id'],
            prioridade=a['prioridade']
        )
        for a in atividades
    ]

@app.get("/atividades/{atividade_id}", response_model=AtividadeResponse, tags=["Atividades"])
def obter_atividade(atividade_id: int):
    atividade = obter_atividade_por_id(atividade_id)
    if not atividade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Atividade não encontrada"
        )
    
    return AtividadeResponse(
        id=atividade['id'],
        titulo=atividade['titulo'],
        descricao=atividade['descricao'],
        data_entrega=atividade['data_entrega'],
        disciplina_id=atividade['disciplina_id'],
        prioridade=atividade['prioridade']
    )

@app.put("/atividades/{atividade_id}", response_model=AtividadeResponse, tags=["Atividades"])
def atualizar_atividade_endpoint(atividade_id: int, dados: AtividadeUpdate):
    atividade = obter_atividade_por_id(atividade_id)
    if not atividade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Atividade não encontrada"
        )
    
    atualizado = atualizar_atividade(
        atividade_id,
        dados.titulo,
        dados.descricao,
        dados.data_entrega,
        dados.prioridade
    )
    
    if not atualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Atividade não encontrada"
        )
    
    atividade = obter_atividade_por_id(atividade_id)
    return AtividadeResponse(
        id=atividade['id'],
        titulo=atividade['titulo'],
        descricao=atividade['descricao'],
        data_entrega=atividade['data_entrega'],
        disciplina_id=atividade['disciplina_id'],
        prioridade=atividade['prioridade']
    )

@app.delete("/atividades/{atividade_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Atividades"])
def deletar_atividade_endpoint(atividade_id: int):
    atividade = obter_atividade_por_id(atividade_id)
    if not atividade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Atividade não encontrada"
        )
    
    deletado = deletar_atividade(atividade_id)
    if not deletado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Atividade não encontrada"
        )

# ROTAS - PROGRESSO

@app.post("/progresso", response_model=ProgressoResponse, status_code=status.HTTP_201_CREATED, tags=["Progresso"])
def registrar_progresso(progresso: ProgressoCreate):
    novo_progresso = criar_progresso(progresso.aluno_id, progresso.atividade_id, progresso.status)
    
    if novo_progresso is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Aluno ou atividade inválida"
        )
    
    return ProgressoResponse(
        id=novo_progresso['id'],
        aluno_id=novo_progresso['aluno_id'],
        atividade_id=novo_progresso['atividade_id'],
        status=novo_progresso['status'],
        data_atualizacao=novo_progresso['data_atualizacao']
    )

@app.get("/progresso/aluno/{aluno_id}", response_model=List[ProgressoResponse], tags=["Progresso"])
def obter_progresso_aluno(aluno_id: int):
    progressos = listar_progresso_aluno(aluno_id)
    return [
        ProgressoResponse(
            id=p['id'],
            aluno_id=p['aluno_id'],
            atividade_id=p['atividade_id'],
            status=p['status'],
            data_atualizacao=p['data_atualizacao']
        )
        for p in progressos
    ]

@app.put("/progresso/{aluno_id}/{atividade_id}", response_model=ProgressoResponse, tags=["Progresso"])
def atualizar_progresso(aluno_id: int, atividade_id: int, dados: ProgressoUpdate):
    atividade = obter_atividade_por_id(atividade_id)
    if not atividade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Atividade não encontrada"
        )
    
    atualizado = atualizar_status_progresso(aluno_id, atividade_id, dados.status)
    
    if not atualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Progresso não encontrado"
        )
    
    progresso = obter_progresso(aluno_id, atividade_id)
    return ProgressoResponse(
        id=progresso['id'],
        aluno_id=progresso['aluno_id'],
        atividade_id=progresso['atividade_id'],
        status=progresso['status'],
        data_atualizacao=progresso['data_atualizacao']
    )

@app.get("/progresso/disciplina/{disciplina_id}", response_model=List[ProgressoResponse], tags=["Progresso"])
def obter_progresso_disciplina(disciplina_id: int):
    """Lista progresso de todos os alunos em uma disciplina"""
    disciplina = obter_disciplina_por_id(disciplina_id)
    if not disciplina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Disciplina não encontrada"
        )
    
    progressos = listar_progresso_disciplina(disciplina_id)
    return [
        ProgressoResponse(
            id=p['id'],
            aluno_id=p['aluno_id'],
            atividade_id=p['atividade_id'],
            status=p['status'],
            data_atualizacao=p['data_atualizacao']
        )
        for p in progressos
    ]

# ROTA - HEALTH CHECK

@app.get("/", tags=["Status"])
def root():
    """Redireciona para a documentação Swagger"""
    return RedirectResponse(url="/docs")

# EXECUÇÃO

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
