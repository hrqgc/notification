import sqlite3


conexao = sqlite3.connect('database/base.db', check_same_thread=False)
cursor = conexao.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS requests (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
link TEXT
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS finals (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
link TEXT
)''')

conexao.commit()
#
#
#
# lista_name = [('a fdasfasdfdsa','https://v2.aurorasolar.com/projects/d6b5a45e-4a90-4c1b-8aa5-e325c6d522e8/overview/dashboard'),
#               ('b fdsafsdafsdaf','https://v2.aurorasolar.com/projects/d6b5a45e-4a90-4c1b-8aa5-e325c6d522e8/overview/dashboard'),
#               ('c dasfsaddfgsad','https://v2.aurorasolar.com/projects/d6b5a45e-4a90-4c1b-8aa5-e325c6d522e8/overview/dashboard'),
#               ('d adfsfsdaf','https://v2.aurorasolar.com/projects/d6b5a45e-4a90-4c1b-8aa5-e325c6d522e8/overview/dashboard')]
#
# lista_name2 = [('e fdasfasdfdsa','https://v2.aurorasolar.com/projects/95364a81-6cc0-49d4-8ad1-d65015aa76c5/overview/dashboard'),
#                ('f fdsafsdafsdaf', 'https://v2.aurorasolar.com/projects/95364a81-6cc0-49d4-8ad1-d65015aa76c5/overview/dashboard'),
#                ('g dasfsaddfgsad', 'https://v2.aurorasolar.com/projects/95364a81-6cc0-49d4-8ad1-d65015aa76c5/overview/dashboard')]
# for lista, link in lista_name:
#     cursor.execute('INSERT INTO requests (name,link) VALUES (?,?)', (lista,link))
#     conexao.commit()
#
# for lista,link in lista_name2:
#     cursor.execute('INSERT INTO finals (name,link) VALUES (?,?)', (lista,link))
#     conexao.commit()
