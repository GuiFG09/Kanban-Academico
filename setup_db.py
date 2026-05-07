from database import usuarios_tbl, disciplinas_tbl, progresso_tbl, atividades_tbl

def inicializar_dados():
    # Limpa o banco para evitar duplicados em cada execução de teste
    usuarios_tbl.truncate()
    disciplinas_tbl.truncate()
    atividades_tbl.truncate()
    progresso_tbl.truncate()

    # 1. Mock de Usuários (Diferenciados pelo campo 'tipo' conforme o diagrama)
    usuarios = [
        {'id': 1, 'nome': 'Prof. Mohsen', 'tipo': 'professor', 'email': 'mohsen@ifpb.edu.br'},
        {'id': 101, 'nome': 'Guilherme', 'tipo': 'aluno', 'email': 'gui@estudante.ifpb.edu.br'},
        {'id': 102, 'nome': 'Ana', 'tipo': 'aluno', 'email': 'ana@estudante.ifpb.edu.br'},
        {'id': 103, 'nome': 'Pedro', 'tipo': 'aluno', 'email': 'pedro@estudante.ifpb.edu.br'}
    ]
    usuarios_tbl.insert_multiple(usuarios)

    # 2. Mock de Disciplina (Ligada ao Professor pelo id)
    disciplina = {
        'id': 10,
        'nome': 'Engenharia de Software',
        'professor_id': 1
    }
    disciplinas_tbl.insert(disciplina)

    # 3. Mock de Matrícula (Simulando quem está na disciplina)
    # No TinyDB, podemos guardar os IDs dos alunos dentro da disciplina
    disciplinas_tbl.update({'alunos_matriculados': [101, 102, 103]}, doc_ids=[1])

    print("✅ Mock de dados concluído: Professor, Alunos e Disciplina criados.")

if __name__ == "__main__":
    inicializar_dados()