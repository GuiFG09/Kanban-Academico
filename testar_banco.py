from database import atividades_tbl

def testar_escrita():
    atividade_teste = {
        'titulo': 'Atividade de Teste',
        'descricao': 'Validando o TinyDB',
        'data_entrega': '2026-05-10',
        'status': 'ativa'
    }
    
    atividades_tbl.insert(atividade_teste)
    print("Sucesso! A atividade foi salva no db.json.")

if __name__ == "__main__":
    testar_escrita()