from database import atividades_tbl, progresso_tbl, disciplinas_tbl

def criar_atividade_teste():
    # Dados da nova atividade
    nova_ativ = {
        'id': 500,
        'titulo': 'Diagrama de Classes',
        'descricao': 'Finalizar o diagrama do projeto Kanban',
        'data_entrega': '2026-05-15',
        'disciplina_id': 10
    }
    atividades_tbl.insert(nova_ativ)

    # Simulação da Automação: Criar progresso para cada aluno matriculado
    # (Isso executa o que está no seu Diagrama de Atividades)
    alunos = [101, 102, 103]
    for aluno_id in alunos:
        progresso_tbl.insert({
            'aluno_id': aluno_id,
            'atividade_id': 500,
            'status': 'A_FAZER', # Status inicial do Kanban
            'cor_prioridade': 'verde'
        })
    
    print("✅ Teste de Escrita: Atividade e Progressos criados no db.json!")

if __name__ == "__main__":
    criar_atividade_teste()