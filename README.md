# 📚 Kanban Acadêmico - API Backend

Sistema simples para gerenciar atividades e progresso acadêmico de forma colaborativa.

## 🚀 Início Rápido

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Executar a API
```bash
python main.py
```

A API estará disponível em: **http://localhost:8000**

## 📖 Acessar a Documentação

Após iniciar a API, abra no navegador:
- **Swagger UI**: http://localhost:8000/docs ← Use aqui para testar!
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Autenticação Simples

A API usa **email e senha** (sem tokens JWT).

### Login
```bash
POST /login
email: daniel@example.com
senha: Messi123

Resposta:
{
  "id": 2,
  "nome": "Daniel",
  "tipo": "professor",
  "email": "daniel@example.com"
}
```

**Sem token necessário!** Todas as rotas funcionam direto.

## 👥 Tipos de Usuário

- **Professor** (tipo: "professor")
  - Criar disciplinas
  - Criar atividades
  - Matricular alunos
  - Ver progresso dos alunos

- **Aluno** (tipo: "aluno")
  - Ver suas atividades
  - Atualizar seu próprio progresso
  - Ver seu próprio histórico

## 📋 Exemplos de Uso (pelo Swagger)

### 1. Registrar Novo Usuário
```
POST /usuarios

{
  "nome": "João Silva",
  "tipo": "aluno",
  "email": "joao@estudante.com",
  "senha": "senha123"
}
```

### 2. Fazer Login
```
POST /login
email: joao@estudante.com
senha: senha123
```

### 3. Criar Disciplina
```
POST /disciplinas

{
  "nome": "Programação em Python",
  "professor_id": 1,
  "descricao": "Disciplina de Python avançado"
}
```

### 4. Criar Atividade
```
POST /atividades

{
  "titulo": "Criar função recursiva",
  "descricao": "Implementar função de Fibonacci",
  "data_entrega": "2026-05-20",
  "disciplina_id": 1,
  "prioridade": "alta"
}
```

**Nota:** A data de entrega **não pode ser no passado!**

### 5. Matricular Aluno
```
POST /disciplinas/{disciplina_id}/matricular?aluno_id={aluno_id}
```

### 6. Atualizar Status de Progresso
```
PUT /progresso/{aluno_id}/{atividade_id}

{
  "status": "FAZENDO"
}
```

### 7. Ver Progresso do Aluno
```
GET /progresso/aluno/{aluno_id}
```

## 🔄 Fluxo Típico

1. Professor cria conta (POST /usuarios)
2. Professor cria disciplina (POST /disciplinas)
3. Professor matricula alunos (POST /disciplinas/{id}/matricular)
4. Professor cria atividade (POST /atividades) → Progresso criado automaticamente
5. Aluno atualiza seu progresso (PUT /progresso/{aluno_id}/{atividade_id})
6. Professor vê progresso da turma (GET /progresso/disciplina/{disciplina_id})

## 📊 Status do Kanban

- **A_FAZER**: Atividade não iniciada
- **FAZENDO**: Atividade em andamento
- **PRONTO**: Atividade concluída

## 📝 Prioridades de Atividade

- **baixa**
- **media**
- **alta**

## 🛠️ Estrutura do Projeto

```
├── main.py           # API FastAPI (principal)
├── models.py         # Modelos Pydantic
├── crud.py           # Operações CRUD
├── database.py       # Inicialização TinyDB
├── auth.py           # Validação simples
├── requirements.txt  # Dependências
└── db.json          # Banco de dados (criado automaticamente)
```

## 💾 Banco de Dados

- **Tipo**: TinyDB (JSON local)
- **Arquivo**: `db.json` (criado automaticamente ao rodar)
- **Sem necessidade de servidor**

## ✅ Regras de Negócio

✅ Todos podem criar usuários, disciplinas e atividades  
✅ Data de entrega deve ser a partir de hoje (não pode ser passada)  
✅ Ao criar atividade, progresso é criado automaticamente para cada aluno  
✅ Nenhuma autenticação por token - tudo é simples!

## 🚀 Dicas para Colegas

1. **Comece pelo Swagger** (`http://localhost:8000/docs`)
2. **Crie um usuário** com POST /usuarios
3. **Teste as rotas** direto no Swagger (botão "Try it out")
4. **Use dados realistas** (datas futuras, emails válidos)
5. **O banco salva automaticamente** em `db.json`

## 📁 Exemplo de Requisição cURL

```bash
# Criar usuário
curl -X POST "http://localhost:8000/usuarios" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Maria Silva",
    "tipo": "aluno",
    "email": "maria@example.com",
    "senha": "senha123"
  }'

# Listar usuários
curl -X GET "http://localhost:8000/usuarios"

# Criar disciplina
curl -X POST "http://localhost:8000/disciplinas" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Python Avançado",
    "professor_id": 1
  }'
```

---

**Desenvolvido com FastAPI + TinyDB + Pydantic** 🚀  
**Simples, rápido e sem complexidade desnecessária!**