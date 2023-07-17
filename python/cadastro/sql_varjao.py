import sqlite3 as sql


class BancoDados:
	"""Abertura e fechamento do banco de dados e soluções 
	de inserção,remoção e alteração de registros"""
	def __init__(self, nome_bd) -> None:
		self.nome_bd = nome_bd
		self.conexao = None
		self.cursor = None


	def conectar_bd(self):
		self.conexao = sql.connect(self.nome_bd)
		self.cursor = self.conexao.cursor()


	def desconectar_bd(self):
		if self.cursor:
			self.conexao.commit()
			self.cursor.close()
		if self.conexao:
			self.conexao.close()


	def inserir_dados_bd(self, nome_tb, lista_dados):
		"""Inserir registro em tabelas onde nao foi atribuídas key autoincrement"""
		try:
			self.conectar_bd()
			placeholders = ', '.join(['?' for _ in range(len(lista_dados))])
			self.cursor.execute(
				f'INSERT INTO {nome_tb} VALUES ({placeholders})', lista_dados)
			print('Dados inseridos com sucesso!')
			return True
		except sql.Error as e:
			print('Erro SQLite: 1',e)
			return False
		finally:
			self.desconectar_bd()
		


	def inserir_dados_key_bd(self, nome_tb, colunas, lista_dados):
		"""Inserir registro onde haja key auto incremente. Nessa função você 
  		precisa informar as colunas com exceção da coluna key"""
		try:
			self.conectar_bd()
			placeholders = ', '.join(['?' for _ in range(len(lista_dados))])
			colunas_ = ', '.join(colunas)
			self.cursor.execute(
				f'INSERT INTO {nome_tb} ({colunas_}) VALUES ({placeholders})', lista_dados)
			print('Dados com key inseridos com sucesso!')
			return True
		except sql.Error as e:
			print('Erro SQLite: 2',e)
			return False
		finally:
			self.desconectar_bd()
	


	def excluir_registro_bd(self, nome_tb, coluna_id, id):
		"""Remove registro do banco de dados"""
		try:
			self.conectar_bd()
			# por questão de segurança foi adicionado um marcador em vez do dado diretamente
			query = f'DELETE FROM {nome_tb} WHERE {coluna_id} = ?'
			self.cursor.execute(query, (id,))
			print('Registro excluído com sucesso!')
			return True
		except sql.Error as e:
			print('Erro SQLite: 3',e)
			return False
		finally:
			self.desconectar_bd()
			


	def alterar_dados_id_bd(self, nome_tb, dados):
		"""Recebe o nome da tabela e um dicionário com a seguinte estrutura:
		{coluna_id: id, coluna_dado: novo_dado}"""
		try:
			self.conectar_bd()
			print('recebeu isso: ',dados)

			for coluna_dado, novo_dado in dados.items():
				if 'id_' in coluna_dado:
					id_ = novo_dado
					coluna_id=coluna_dado
			for coluna_dado, novo_dado in dados.items():
				query = f"UPDATE {nome_tb} SET {coluna_dado} = ? WHERE {coluna_id} = ?"											
				self.cursor.execute(query, (novo_dado, id_))
    
			print('Dados alterados com sucesso!')
			return True
    
		except sql.Error as e:
			print('Erro SQLite: 4',e)
			return False
		finally:
			self.desconectar_bd()
			


	def consultar_tabela_bd(self, nome_tabela):
		"""Retorna todos os dados da tabela"""
		try:
			self.conectar_bd()
			self.cursor.execute(f'SELECT * FROM {nome_tabela}')
			dados_tab = self.cursor.fetchall()
		except sql.Error as e:
			print('Erro SQLite: 5',e)
		finally:
			self.desconectar_bd()
			return dados_tab
	

	def verifica_login(self, usuario, senha):
		"""Verifica o Login do usuário se encontrado retorna o nome do usuário """
		try:
			self.conectar_bd()
			self.cursor.execute(f"""SELECT * FROM 'usuarios'
						WHERE nome='{usuario}' 
						OR email='{usuario}' 
						OR cpf='{usuario}' 
						AND senha='{senha}'""")
			resultado = self.cursor.fetchone()
			if resultado != None and usuario in resultado and senha in resultado:
				return resultado
			else:
				return False
		except sql.Error as e:
			print('Erro SQLite: 6',e)
			return False
		finally:
			self.desconectar_bd()


	def criar_tabela_bd(self, nome_tb, coluna_tb):
		"""Cria tabelas no banco de dados"""
		try:
			self.conectar_bd()
			fields_str = ', '.join(coluna_tb)
			self.cursor.execute(
				f'CREATE TABLE IF NOT EXISTS {nome_tb} ({fields_str})')
		except sql.Error as e:
			print('Erro SQLite: 7',e)
			print(f'Erro na criação da tabela: ',nome_tb)
		finally:
			self.desconectar_bd()


	def gerar_novo_numero_nfe(self):
		self.conectar_bd()
		self.cursor.execute(f'SELECT numero_nfe FROM conf_nfe')
		numero_atualizado = self.cursor.fetchone()[0]
		self.cursor.execute(f'UPDATE conf_nfe SET numero_nfe = ?', (numero_atualizado,))
		self.desconectar_bd()

	
	def consulta_dados_bd(self, consulta, coluna, tabela):
		"""Retorna todos os dados relacionados a Consulta. Util para consultas onde se espera mais de um resultado"""

		dados='NAO PASSOU NAS CONDIÇÕES'
		try:
			self.conectar_bd()
			if 'id_' in coluna:
				self.cursor.execute(
					f'SELECT * FROM {tabela} WHERE {coluna} = ?', (consulta,))				
			else:
				self.cursor.execute(
					f'SELECT * FROM {tabela} WHERE {coluna} LIKE "%'f'{consulta}'f'%" order by {coluna}')
			dados = self.cursor.fetchall()
			return dados
		except sql.Error as e:
			print('Erro SQLite: 8',e)
			return False
		finally:			
			self.desconectar_bd()



	def consulta_dado_bd(self, consulta, coluna, tabela):
		"""Consulta Registros no banco de dados retorna o resultado mais aproximado"""
		try:
			self.conectar_bd()
			if 'id_' in coluna:
				self.cursor.execute(
					f'SELECT * FROM {tabela} WHERE {coluna} = ?', (consulta,))
			else:
				self.cursor.execute(
					f'SELECT * FROM {tabela} WHERE {coluna} LIKE "%'f'{consulta}'f'%" order by {coluna}')
			resultado_unico = self.cursor.fetchone()
			return [resultado_unico]#precisa alterar
		except sql.Error as e:
			print('Erro SQLite: 9',e)
			return False
		finally:
			self.desconectar_bd()
			
   
	def consulta_dado_especifico_bd(self, consulta, coluna, tabela):
		"""Consulta Registro específico no banco de dados retorna apenas um resultado"""
		try:
			self.conectar_bd()
			self.cursor.execute(
				f'SELECT * FROM {tabela} WHERE {coluna} = {consulta}')
			resultado = self.cursor.fetchone()
			return resultado
		except sql.Error as e:
			print('Erro SQLite: 10',e)
			return False
		finally:
			self.desconectar_bd()


	def consulta_conlunas_bd(self, colunas, tabela):#terminar
		self.conectar_bd()
		self.cursor.execute(f'SELECT {colunas} FROM {tabela} ')
  
		self.desconectar_bd()


if __name__ == '__main__':

	tab = BancoDados('varjao.db')

	tab.criar_tabela_bd('produtos', ['''
		id_produto INTEGER PRIMARY KEY,
		prod_descricao TEXT,
		prod_preco DECIMAL(10, 2),     
		prod_grupo TEXT
		'''])

	tab.criar_tabela_bd('usuarios', ['''
		id_usuario INTEGER PRIMARY KEY,
		nome TEXT,
		cpf TEXT UNIQUE,
		email TEXT UNIQUE,
		telefone TEXT,
		apelido TEXT,
		senha TEXT 
		'''])

	tab.criar_tabela_bd('inf_vendas', ['''
		id_inf_venda INTEGER PRIMARY KEY AUTOINCREMENT,
		atendente_id INTEGER,
		data DATE, 
		quant_vendas INTEGER,     
		FOREIGN KEY (atendente_id) REFERENCES atendentes(usuario_id)
		'''])

	tab.criar_tabela_bd('empresas', ['''
		id_empresa INTEGER PRIMARY KEY AUTOINCREMENT,
		razao_social TEXT,
		nome_fantasia TEXT,
		cnpj INTEGER UNIQUE,		
		cod_regime_tribut TEXT,
		insc_estadual INTEGER,
		insc_municipal INTEGER,
		cnae_fiscal INTEGER,
		end_logradouro TEXT,
		end_numero INTEGER,
		end_bairro TEXT,
		end_municipio TEXT,
		end_uf TEXT,
		end_cep INTEGER,
		funcao TEXT
		'''])

	tab.criar_tabela_bd('fiscal_produto', ['''
		id_fiscal_produto INTEGER PRIMARY KEY AUTOINCREMENT,
		nome_grupo TEXT UNIQUE,
		ncm	INTEGER,
		cfop INTEGER,
		unidade_comercial TEXT,
		ean	INTEGER,
		ean_tributavel	INTEGER,
		unidade_tributavel	TEXT,
		icms_modalidade INTEGER,
		icms_origem INTEGER,
		icms_cson INTEGER,
		pis_modalidade INTEGER,
		confins_modalidade INTEGER                                    
		'''])

	
	tab.criar_tabela_bd('conf_nfe',['''
		id_conf_nfe INTEGER PRIMARY KEY AUTOINCREMENT,
		nome_config_nfe TEXT UNIQUE,
		uf TEXT,
		nat_operacao TEXT,
		forma_pag TEXT,
		tipo_pag TEXT,
		modelo TEXT,
		serie INTEGER,
		numero_nfe INTEGER,
		tipo_documento TEXT,
		cod_municipio INTEGER,
		tipo_impressao TEXT,
		forma_emissao TEXT,
		cliente_final TEXT,
		indicador_destino TEXT,
		indicador_presencial TEXT,
		finalidade_emissao TEXT,
		processo_emissao TEXT,
		transp_mod_frente TEXT,
		inf_adic_interesse_fisco TEXT,
		csc_prod TEXT,
		empresa_emitente TEXT
		'''])
 

	tab.criar_tabela_bd('vendas', ['''
		id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
		cpf_cliente INTEGER,
		data_venda DATE,
		valor_total DECIMAL(10, 2),
		FOREIGN KEY (cpf_cliente) REFERENCES clientes(cpf)
	'''])

	tab.criar_tabela_bd('itens_venda', ['''
		venda_id INTEGER,
		produto_id INTEGER,
		quantidade INTEGER,
		valor_unitario DECIMAL(10, 2),
		grupo_produto TEXT,
		FOREIGN KEY (venda_id) REFERENCES vendas(id_venda),
		FOREIGN KEY (produto_id) REFERENCES produtos(id_produto)
	'''])

	tab.criar_tabela_bd('clientes', ['''
		id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
		nome TEXT,
		cpf TEXT UNIQUE,
		email TEXT UNIQUE,
		telefone TEXT                                                   
		'''])

	tab.criar_tabela_bd('atendentes', ['''
		usuario_id INTEGER UNIQUE,
		apelido TEXT,
		perfil TEXT,
		FOREIGN KEY (usuario_id) REFERENCES usuarios(id_usuario)
		'''])

if __name__ == '__main__':
	db=BancoDados('varjao.db')
	db.gerar_novo_numero_nfe()