import sqlite3 as sql


class BancoDados:
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
		self.conectar_bd()
		print(lista_dados)
		placeholders = ', '.join(['?' for _ in range(len(lista_dados))])
		self.cursor.execute(
			f'INSERT INTO {nome_tb} VALUES ({placeholders})', lista_dados)
		print('Dados inseridos com sucesso!')
		self.desconectar_bd()

	def inserir_dados_key_bd(self, nome_tb, colunas, lista_dados):
		self.conectar_bd()

		placeholders = ', '.join(['?' for _ in range(len(lista_dados))])
		colunas_ = ', '.join(colunas)

		self.cursor.execute(
			f'INSERT INTO {nome_tb} ({colunas_}) VALUES ({placeholders})', lista_dados)
		print('Dados com key inseridos com sucesso!')
		self.desconectar_bd()

	def consultar_tabela_bd(self, nome_tabela):
		self.conectar_bd()

		self.cursor.execute(f'SELECT * FROM {nome_tabela}')
		dados_tab = self.cursor.fetchall()

		self.desconectar_bd()
		return dados_tab

	def consultar_dado_bd(self, consulta, tabela):
		self.conectar_bd()

		self.cursor.execute(f'SELECT {consulta} FROM {tabela}')
		dados = self.cursor.fetchall()

		self.desconectar_bd()
		return dados


	def verifica_login(self, usuario, senha):
		self.conectar_bd()
		self.cursor.execute(f"""SELECT * FROM 'usuarios'
					WHERE nome='{usuario}' 
					OR email='{usuario}' 
					OR cpf='{usuario}' 
					AND senha='{senha}'""")
		resultado = self.cursor.fetchone()
		self.desconectar_bd()
		if resultado != None and usuario in resultado and senha in resultado:
			return resultado
		else:
			return False

	def criar_tabela_bd(self, nome_tb, index_tb):
		self.conectar_bd()
		fields_str = ', '.join(index_tb)
		self.cursor.execute(
			f'CREATE TABLE IF NOT EXISTS {nome_tb} ({fields_str})')
		self.desconectar_bd()
  
	def consulta_dado_bd(self, consulta, index, tabela):
		self.conectar_bd()
		if 'id' in index:
			self.cursor.execute(
				f'SELECT * FROM {tabela} WHERE {index} = ?', (consulta,))
		else:
			self.cursor.execute(
				f'SELECT * FROM {tabela} WHERE {index} LIKE "%'f'{consulta}'f'%" order by {index}')
		#resultado_consulta = self.cursor.fetchall()
		resultado_unico = self.cursor.fetchone()
		self.desconectar_bd()
		return resultado_unico


class Consulta(BancoDados):
	def __init__(self, nome_bd) -> None:
		super().__init__(nome_bd)
	

class Tabelas(BancoDados):
	def __init__(self, nome_bd) -> None:
		super().__init__(nome_bd)
	
if __name__ ==  '__main__':  
    
	tab=Tabelas('varjao.db')

	tab.criar_tabela_bd('produtos', ['''
		id_produto INTEGER PRIMARY KEY,
		prod_descricao TEXT,
		prod_preco FLOAT,     
		prod_grupo TEXT
		'''])

	tab.criar_tabela_bd('usuarios', ['''
		id_usuario INTEGER PRIMARY KEY,
		nome TEXT,
		cpf TEXT,
		email TEXT,
		celular TEXT,
		apelido TEXT,
		senha TEXT                                                      
		'''])

	tab.criar_tabela_bd('inf_vendas', ['''
		data DATE, 
		quant_vendas INTEGER                             
		'''])

	tab.criar_tabela_bd('empresas', ['''
		razao_social TEXT,
		nome_fantasia TEXT,
		cnpj INTEGER,		
		cod_regime_tribut INTEGER,
		insc_estadual INTEGER,
		insc_municipal INTEGER,
		cnae_fiscal INTEGER,
		end_logradouro TEXT,
		end_numero INTEGER,
		end_bairro TEXT,
		end_municipio TEXT,
		end_uf TEXT,
		end_cep INTEGER,
		end_pais TEXT
		'''])

	tab.criar_tabela_bd('fiscal_Produto',['''
		nome_grupo TEXT,
		ncm	INTEGER,
		cfop INTEGER,
		unidade_comercial TEXT,
		ean	INTEGER,
		ean_tributavel	INTEGER,
		unidade_tributavel	TEXT,
		icms_modalidade INTEGER,
		icms_sorigem INTEGER,
		icms_cson INTEGER,
		pis_modalidade INTEGER,
		confins_modalidade INTEGER                                    
		'''])
 
	#exemplo de tabelas para vendas

	tab.criar_tabela_bd('vendas', ['''
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		cliente_id INTEGER,
		data_venda DATE,
		valor_total DECIMAL(10, 2),
		FOREIGN KEY (cliente_id) REFERENCES clientes(id)
	'''])

	tab.criar_tabela_bd('itens_venda', ['''
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		venda_id INTEGER,
		produto_id INTEGER,
		quantidade INTEGER,
		valor_unitario DECIMAL(10, 2),
		grupo_produto TEXT,
		FOREIGN KEY (venda_id) REFERENCES vendas(id),
		FOREIGN KEY (produto_id) REFERENCES produtos(id)
	'''])