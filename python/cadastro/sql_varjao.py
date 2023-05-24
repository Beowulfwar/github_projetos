import sqlite3 as sql

class Db:
	def __init__(self) -> None:
		# Atribuição do banco de dados e suas tabelas
		self.banco_dados = 'varjao.db'
		self.tb_produto = 'produtos'
		self.tb_usuarios = 'usuarios'


	def cad_produto(self, descricao, preco):

		conexao = sql.connect(f'{self.banco_dados}')
		c = conexao.cursor()
		c.execute(f'''CREATE TABLE IF NOT EXISTS {self.tb_produto} (
			cod_produto INTEGER PRIMARY KEY,
			prod_descricao TEXT,
			prod_preco FLOAT
			)''')
		c.execute(f'INSERT INTO {self.tb_produto} (prod_descricao, prod_preco) VALUES(?,?)', (
			f'{descricao.get()}',
			f'{float(preco.get())}'
		))
		conexao.commit()
		conexao.close()
		print('Produto cadastrado com sucesso!')
 
 
	def consulta_usuarios(self, campo, dado):

		conexao = sql.connect(f'{self.banco_dados}')
		c = conexao.cursor()
		c.execute(f'SELECT * FROM {self.tb_usuarios} WHERE {campo} = ?', (dado,))
		resultado = c.fetchone()
		conexao.close()
		if resultado:
			print("verificar consulta_usuarios passou..")
		else:
			print('verificar consulta_usuario nao passou...')
			
			
	def cadastrar_usuarios(self, nome, cpf, email, celular, senha, apelido=None):

		conexao = sql.connect(f'{self.banco_dados}')

		c = conexao.cursor()
		c.execute(f'''CREATE TABLE IF NOT EXISTS {self.tb_usuarios} (
			nome text,
			cpf text,
			email text,
			celular text,
			apelido text,
			senha text
		)''')
		if apelido is None:
			c.execute(f'''INSERT INTO {self.tb_usuarios} VALUES(?,?,?,?,?,?)''', (
				f'{nome.get()}',
				f'{cpf.get()}',
				f'{email.get()}',
				f'{celular.get()}',
				f'{senha.get()}'
			))
		else:
			c.execute(f'''INSERT INTO {self.tb_usuarios} VALUES(?,?,?,?,?,?)''', (
				f'{nome.get()}',
				f'{cpf.get()}',
				f'{email.get()}',
				f'{celular.get()}',
				f'{apelido.get()}',
				f'{senha.get()}'
			))
		conexao.commit()
		conexao.close()
		print('Usuario cadastrado com sucesso!')
  
  
	def verifica_login(self, usuario, senha):

		conexao = sql.connect(f'{self.banco_dados}')
		c = conexao.cursor()
		c.execute(f"""SELECT * FROM {self.tb_usuarios}
					WHERE nome='{usuario}' 
					OR email='{usuario}' 
					OR cpf='{usuario}' 
					OR apelido='{usuario}' 
					AND senha='{senha}'""")
		resultado = c.fetchone()
		conexao.close()

		if resultado != None and usuario in resultado and senha in resultado:
			return resultado
		else:
			return False
