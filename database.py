from tinydb import TinyDB

db = TinyDB('db.json')

atividades_tbl = db.table('atividades')
progresso_tbl = db.table('progresso')
usuarios_tbl = db.table('usuarios')
disciplinas_tbl = db.table('disciplinas')

print("Banco e tabelas inicializados!")