from database import usuarios_tbl

def popular_banco():
    # Limpa a tabela para evitar duplicatas ao rodar várias vezes
    usuarios_tbl.truncate() 
    
    usuarios = [
        {'id': 1, 'nome': 'Professor Mohsen', 'tipo': 'professor'},
        {'id': 101, 'nome': 'Guilherme', 'tipo': 'aluno'},
        {'id': 102, 'nome': 'Ana', 'tipo': 'aluno'},
        {'id': 103, 'nome': 'Pedro', 'tipo': 'aluno'}
    ]
    
    usuarios_tbl.insert_multiple(usuarios)
    print(f"{len(usuarios)} usuários inseridos com sucesso!")

if __name__ == "__main__":
    popular_banco()