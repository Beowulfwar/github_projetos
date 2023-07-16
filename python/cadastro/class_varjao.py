import customtkinter as ctk
from tkinter import ttk
import re
import os
from sql_varjao import BancoDados
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import random
import json
import envio_nf

db = BancoDados('varjao.db')


class Janela(ctk.CTk):
	def __init__(self, geometria='400x400', resizable=(True, True), titulo='janela') -> None:
		super().__init__()
		self.title(titulo)
		self._set_appearance_mode('dark')
		self.geometry(geometria)
		self.resizable(*resizable)
		self.centralizar_janela(self)

	@staticmethod
	def centralizar_janela(janela):
		largura_janela = janela.winfo_width()
		altura_janela = janela.winfo_height()

		largura_tela = janela.winfo_screenwidth()
		altura_tela = janela.winfo_screenheight()

		posicao_x = (largura_tela - largura_janela) // 2
		posicao_y = (altura_tela - altura_janela) // 2

		janela.geometry(
			f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")


class JanelaTop(ctk.CTkToplevel):
	def __init__(self, geometry='400x400', resizable=(True, True), title='Janela'):
		super().__init__()
		self.title(title)
		self.geometry(geometry)
		self.resizable(*resizable)
		self.centralizar_janela()
		self.bring_to_front()

	def bring_to_front(window):
		window.lift()
		window.attributes('-topmost', True)

	def centralizar_janela(self):
		self.update_idletasks()
		width = self.winfo_width()
		height = self.winfo_height()
		x = (self.winfo_screenwidth() // 2) - (width // 2)
		y = (self.winfo_screenheight() // 2) - (height // 2)
		self.geometry(f"+{x}+{y}")


class NFCe(FPDF):
	def header(self):
		empresa = db.consulta_dado_bd('123456789', 'cnpj', 'empresas')
		# Logo
		imagem = r'img\logo.png'

		self.image(imagem, x=4, y=4, w=10, dims=(50, 40))
		self.set_xy(13, 4)
		self.set_font('helvetica', 'B', 10)
		self.cell(0, 10, empresa[0], align='L',
				  new_x=XPos.LMARGIN, new_y=YPos.NEXT)

	def footer(self):
		self.set_y(-15)
		self.set_font('helvetica', 'I', 8)
		self.cell(0, 10, 'www.exemplo.com', new_x=XPos.CENTER, new_y=YPos.TOP)


class Validacoes:

	texto_erro = ''

	def __init__(self):
		self.janela_erro_altura = 140
		self.azul = '#0080FF'
		self.azul_metal_claro = '#B0C4DE'
		self.azul_claro = '#ADD8E6'

	def validar_email(self, widget, alteracao: bool = None):
		"""Verifica se o e-mail está segue o padrão impedindo que seja atribuídos dados aleatórios """
		# Expressão regular para verificar o formato do e-mail
		regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

		# Verifica se o e-mail corresponde à expressão regular utiliza a biblioteca re
		if not re.match(regex, widget.get()):
			if db.consulta_dado_especifico_bd(widget.get(), 'email', 'usuarios'):
				self.janel_erro('Esse email ja foi cadastrado', widget)
			widget.configure(border_color='red')
			self.janel_erro('Verifique o campo E-mail', widget)
			print('passou!')
			return False
		else:
			widget.configure(border_color='gray')
			return True

	def validar_apelido(self, widget, alteracao: bool = None):
		if len(widget.get()) < 6:
			if alteracao and db.consulta_dado_especifico_bd(widget.get(), 'apelido', 'usuarios'):
				self.janel_erro(
					'Esse apelido já esta sendo usado por outro usuário', widget)
				return False
			widget.configure(border_color='red')
			self.janel_erro('Verifique o campo apelido', widget)
			return False
		else:
			widget.configure(border_color='gray')
			return True

	def validar_nome(self, widget):

		if widget.get() == '' and len(list(widget.get())) < 15:
			widget.configure(border_color='red')
			self.janel_erro('Verifique o campo nome', widget)
			return False
		else:
			widget.configure(border_color='gray')
			return True

	def validar_cpf(self, widget, alteracao: bool = None):

		# remove tudo que nao for número
		cpf = re.sub(r'\D', '', widget.get())

		if len(list(cpf)) != 11:
			if alteracao and db.consulta_dado_especifico_bd(widget.get(), 'cpf', 'usuarios'):
				self.janel_erro(
					'Já existe usuário cadastrado com esse CPF', widget)
				return False
			if db.consulta_dado_especifico_bd(widget.get(), 'cpf', 'clientes'):
				self.janel_erro(
					'Já existe cliente cadastrado com esse CPF', widget)
				return False
			widget.configure(border_color='red')
			self.janel_erro('Verifique o campo CPF', widget)
			return False
		else:
			widget.configure(widget, border_color='gray')
			return True

	def validar_telefone(self, widget):
		# remove tudo que nao for número
		celular = re.sub(r'\D', '', widget.get())

		if len(list(celular)) != 11:
			widget.configure(border_color='red')
			self.janel_erro('Verifique o campo telefone', widget)
			return False
		else:
			widget.configure(border_color='gray')
			return True

	def validar_senha(self, senha1, senha2):
		if senha1.get() != senha2.get() or len(list(senha1.get())) < 6:
			senha1.configure(border_color='red')
			senha2.configure(border_color='red')
			self.janel_erro('Verifique os campos de senhas', senha1)
			return False
		else:
			senha1.configure(border_color='gray')
			senha2.configure(border_color='gray')
			return True

	def validar_cnpj(self, widget, alteracao=None):

		cnpj = re.sub(r'\D', '', widget.get())
		if len(cnpj) != 14:
			if alteracao and db.consulta_dado_especifico_bd(widget.get(), 'cnpj', 'empresas'):
				self.janel_erro('Esse CNPJ ja foi cadastrado', widget)
				return False
			widget.configure(border_color='red')
			self.janel_erro('Verifique o campo CNPJ', widget)
			return False
		else:
			widget.configure(border_color='gray')
			return True

	def validar_alpha(self, widget):

		if not widget.get().replace(' ', '').isalpha():
			widget.configure(border_color='red')
			self.janel_erro('Nesse campo são permitidas apenas letras', widget)
			return False
		else:
			widget.configure(border_color='gray')
			return True

	def validar_insc_estadual(self, widget):

		insc_estadual = re.sub(r'\D', '', widget.get())
		if not insc_estadual.isdigit() or len(insc_estadual) != 9:
			widget.configure(border_color='red')
			self.janel_erro('Verifique o campo IE', widget)
			return False
		else:
			widget.configure(border_color='gray')
			return True

	def validar_insc_municipal(self, widget):
		insc_municip = re.sub(r'\D', '', widget.get())
		if not insc_municip or len(insc_municip) != 11:
			widget.configure(border_color='red')
			self.janel_erro('Verifique o campo IM', widget)
			return False
		else:
			widget.configure(border_color='gray')
			return True

	def validar_cnae(self, widget):
		cnae = re.sub(r'\D', '', widget.get())
		if not cnae.isdigit() or len(cnae) != 7:
			widget.configure(border_color='red')
			self.janel_erro('Verifique o campo CNAE', widget)
			return False
		else:
			widget.configure(border_color='gray')
			return True

	def validar_cep(self, widget):
		cep = re.sub(r'\D', '', widget.get())
		if not cep or len(cep) != 8:
			widget.configure(border_color='red')
			self.janel_erro('Verifique o campo CEP', widget)
			return False
		else:
			widget.configure(border_color='gray')
			return True

	def validar_digitos(self, widget):
		var = re.sub(r'\D', '', widget.get())
		if not var.isdigit():
			widget.configure(border_color='red')
			self.janel_erro(
				'Nesse campo são permitidos apenas dígitos', widget)
			return False
		else:
			widget.configure(border_color='gray')
			return True

	def validar_campo_vazio(self, widget):
		if not widget.get():
			widget.configure(border_color='red')
			self.janel_erro('Verifique o campo vazio', widget)
			return False
		else:
			widget.configure(border_color='gray')
			return True

	def validar_ncm(self, widget):
		ncm = widget.get()
		ncm = re.sub(r'\D', '', ncm)

		if len(ncm) == 8:
			widget.configure(border_color='gray')
			return True
		else:
			widget.configure(border_color='red')
			self.janel_erro('Verifique o campo NCM', widget)
			return False

	def validar_cfop(self, widget):
		cfop = widget.get()
		cfop = re.sub(r'\D', '', cfop)

		if len(cfop) == 4:
			widget.configure(border_color='gray')
			return True
		else:
			widget.configure(border_color='red')
			self.janel_erro('Verifique o campo CFOP', widget)
			return False

	def validar_ean(self, widget):

		ean = widget.get()
		ean = re.sub(r'\D', '', ean)
		if widget.get() == 'SEM GTIN':
			return True
		elif len(ean) == 13:
			widget.configure(border_color='gray')
			return True
		else:
			widget.configure(border_color='red')
			self.janel_erro('Verifique o campo EAN', widget)
			return False

	def validar_csosn(self, widget):
		csosn = widget.get()
		csosn_validos = ['101', '102', '201', '202',
						 '203', '300', '400', '500', '900']

		if csosn in csosn_validos:
			widget.configure(border_color='gray')
			return True
		else:
			widget.configure(border_color='red')
			self.janel_erro('Verifique o campo CSOSN', widget)
			return False

	def validar_nome_produto(self, widget):

		if widget.get() == '':
			widget.configure(border_color='red')
			self.janel_erro('Verifique o campo nome', widget)

			return False
		else:
			widget.configure(border_color='gray')
			return True

	def validar_preco_produto(self, widget):
		if widget.get():
			print(widget.get())
			if float(widget.get()) <= 0 or not widget.get():
				widget.configure(border_color='red')
				self.janel_erro('Verifique o campo preço', widget)
				return False
			else:
				widget.configure(border_color='gray')
				return True
		else:
			widget.configure(border_color='red')
			self.janel_erro('Verifique o campo preço', widget)	
		

	def janel_erro(self, texto_erro, wid=None):

		def fecha_janela():
			Validacoes.texto_erro = ''
			self.janela.destroy()
		if len(texto_erro) > 35:
			self.frame.configure(width=len(texto_erro)*10)
			self.janela.configure(width=len(texto_erro)*10)



		if not Validacoes.texto_erro:
			self.janela = JanelaTop(
				f'400x200', (False, False), 'Erro!')
			self.frame = ctk.CTkFrame(self.janela)
			lb_titulo = ctk.CTkLabel(
				self.frame, text='Erros encontrados!', text_color=self.azul, font=('', 20))
			self.lb_inf_erro = ctk.CTkLabel(
				self.frame, text=texto_erro, text_color='red', font=('', 20))
			bt_ok = ctk.CTkButton(self.frame, text='OK',
								  width=50, command=fecha_janela)
   
			if wid:
				self.lb_inf_erro.bind('<Button-1>', lambda e: wid.focus_set())

			self.frame.pack(padx=10, pady=10, fill='both')
			lb_titulo.pack(pady=10)
			self.lb_inf_erro.pack(pady=10)
			bt_ok.pack(pady=10)

			Validacoes.texto_erro = texto_erro
			self.janela.protocol('WM_DELETE_WINDOW', fecha_janela)
		else:
			if texto_erro not in Validacoes.texto_erro:
				self.janela.geometry(f'400x{self.janela_erro_altura}')
				self.janela_erro_altura = (len(self.frame.winfo_children()))*75
				self.frame.pack(fill='both', expand=True)
				self.lb_inf_erro.configure(
					text=Validacoes.texto_erro+'\n'+texto_erro)
				Validacoes.texto_erro += '\n'+texto_erro


class Log:
	def salva_log_usuario(self, user_id, config):
		arquivo_log = 'config.log'
		try:
			with open(arquivo_log, 'r', ) as arquivo:
				try:
					configs = json.load(arquivo)
				except json.JSONDecodeError:
					configs = {}
		except FileNotFoundError:
			configs = {}

		configs[user_id] = config
		with open(arquivo_log, 'w', encoding='utf-8') as arquivo:
			json.dump(configs, arquivo, indent=4, ensure_ascii=False)

	def ler_log_usuario(self):
		log_file = 'config.log'
		try:
			with open(log_file, 'r') as file:
				contents = file.read()
				if contents.strip():  # Verifica se o arquivo não está vazio ou contém apenas espaços em branco
					config = json.loads(contents)

					return config

		except FileNotFoundError:
			pass
		return None

	def salvar_login(self, usuario, senha=''):
		arquivo_log = 'usuario.log'
		try:
			with open(arquivo_log, 'r', ) as arquivo:
				try:
					configs = json.load(arquivo)
				except json.JSONDecodeError:
					configs = {}
		except FileNotFoundError:
			configs = {}

		configs[usuario] = senha
		with open(arquivo_log, 'w', encoding='utf-8') as arquivo:
			json.dump(configs, arquivo, indent=4, ensure_ascii=False)

	def ler_login_usuario(self):
		arquivo = 'usuario.log'
		try:
			with open(arquivo, 'r') as file:
				contents = file.read()
				if contents.strip():  # Verifica se o arquivo não está vazio ou contém apenas espaços em branco
					config = json.loads(contents)
					return config

		except FileNotFoundError:
			pass
		return None


class Produtos():
	def __init__(self) -> None:
		self.cod_produto = None
		self.descricao_produto = None
		self.preco_produto = None
		self.nome_erro = None
		self.preco_erro = None


class Formatacoes:
	def formata_cpf(self, cpf):
		"""recebe o o numero CPF sem formação e devolve ele com o padrão CPF 123.456.798-00"""
		cpf = str(cpf)
		# Verifica se o número possui 11 dígitos
		if len(cpf) != 11:
			raise ValueError('O número deve ter 11 dígitos')
		# Formatação do CPF
		cpf_formatado = '{}.{}.{}-{}'.format(cpf[:3],
											 cpf[3:6], cpf[6:9], cpf[9:])
		return cpf_formatado

	def formata_moeda(self, valor):
		val = f'R$: {valor:.2f}'
		return val

	def formata_cnpj(self, cnpj):
		"""Recebe um cnpj apenas dígitos e devolve o padrão 123.456.789/0001-00"""
		cnpj = str(cnpj)
		# Verifica se o número possui 14 dígitos
		if len(cnpj) != 14:
			raise ValueError('O número deve ter 14 dígitos')
		try:
			cnpj = str(cnpj)
		except TypeError:
			print('O tipo de dados nao pode ser convertido em str')

			# Formatação do CNPJ
		cnpj_formatado = '{}.{}.{}/{}-{}'.format(
			cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:])
		return cnpj_formatado

	def formata_data_bd(self, data):

		data_partes = str(data).split(' ')
		data_ = data_partes[0]
		hora = data_partes[1]
		ano, mes, dia = data_.split('-')
		data_formatada = f'{dia}/{mes}/{ano} {hora}'
		return data_formatada


class Consultas():
	janela_consulta_usuario_aberta = False
	janela_consulta_vendas_aberta = False
	janela_consulta_produtos_aberta = False
	janela_consulta_empresa_aberta = False

	def __init__(self) -> None:
		self.azul = '#0080FF'
		self.azul_metal_claro = '#B0C4DE'
		self.azul_claro = '#ADD8E6'
		self.formata = Formatacoes()

	def janel_consulta_empresa(self):

		def preenche_treeview():

			cx.delete(*cx.get_children())
			empresa = db.consultar_tabela_bd('empresas')
			for v, item in enumerate(empresa):
				list_item = [
					list_item for list_item in item if list_item != item[6]]
				list_item[3] = self.formata.formata_cnpj(list_item[3])
				if v % 2 == 0:

					cx.insert(
						'', 'end', values=list_item[:-1], tags=('linha_par',))
				else:
					cx.insert('', 'end', values=list_item[:-1])

		def consulta_treeview():
			usuario = []
			opcao = op_menu.get().lower()
			if opcao == 'id':
				opcao = 'id_empresas'
			elif opcao == 'razão social':
				opcao = 'razao_social'
			elif opcao == 'nome fantasia':
				opcao = 'nome_fantasia'

			lb_erro.grid_forget()
			cx.delete(*cx.get_children())
			usuario = db.consulta_dados_bd(
				et_consulta.get(), opcao, 'empresas')

			try:
				if et_consulta.get() and usuario[0]:
					for v, item in enumerate(usuario):
						list_item = [
							list_item for list_item in item if list_item != item[6]]
						list_item[0:-
								  1][3] = self.formata.formata_cnpj(list_item[3])
						if v % 2 == 0:
							cx.insert('', 'end', values=list_item,
									  tags=('linha_par',))
						else:
							cx.insert('', 'end', values=list_item)
				else:
					preenche_treeview()
			except IndexError:
				lb_erro.configure(
					text='Empresa nao encontrada!', text_color='red')
				lb_erro.grid(row=1, column=0, columnspan=3)

		def dado_treeview():
			valor_selecionado = cx.selection()
			if valor_selecionado:
				dados = cx.item(valor_selecionado)['values']

		if not Consultas.janela_consulta_empresa_aberta:
			Consultas.janela_consulta_empresa_aberta = True

			janela_consulta_empresa = JanelaTop(
				'600x380', (False, False), 'Consulta empresa')

			lb_consulta = ctk.CTkLabel(
				janela_consulta_empresa, text='Consulta empresa', text_color=self.azul, font=('Roboto', 20))
			lb_erro = ctk.CTkLabel(janela_consulta_empresa, text='')
			op_menu = ctk.CTkOptionMenu(janela_consulta_empresa, values=[
				'Razão social', 'CNPJ', 'Nome fantasia', 'Id'])
			et_consulta = ctk.CTkEntry(
				janela_consulta_empresa, placeholder_text='<<< Informe o campo')
			bt_consulta = ctk.CTkButton(
				janela_consulta_empresa, text='Consulta', command=consulta_treeview)
			bt_alterar = ctk.CTkButton(janela_consulta_empresa, text='Alterar')
			bt_excluir = ctk.CTkButton(janela_consulta_empresa, text='Excluir')
			bt_atualizar = ctk.CTkButton(
				janela_consulta_empresa, text='Atualizar')

			# estilo do treeview
			estilo = ttk.Style()
			estilo.theme_use('default')
			estilo.configure('Treeview',
							 foreground='black',
							 rowheight=20
							 )
			estilo.map('Treeview',
					   background=[('selected', self.azul)])

			cx = ttk.Treeview(janela_consulta_empresa, columns=(
				'Id', 'Razão social', 'Nome fantasia', 'CNPJ', 'RT', 'Insc estadual'), show='headings')

			with Image.open('img\\excluir_vermelho (1).png') as img:
				img_excluir = ImageTk.PhotoImage(img, master=cx)

			cx.tag_configure('linha_par', background=self.azul_claro)

			cx.column('Id', minwidth=0, width=30)
			cx.column('Razão social', minwidth=0, width=150)
			cx.column('Nome fantasia', minwidth=0, width=120)
			cx.column('CNPJ', minwidth=0, width=120)
			cx.column('RT', minwidth=0, width=30)
			cx.column('Insc estadual', minwidth=0, width=80)

			cx.heading('Id', text='ID')
			cx.heading('Razão social', text='Razão social')
			cx.heading('Nome fantasia', text='Nome fantasia')
			cx.heading('CNPJ', text='CNPJ')
			cx.heading('RT', text='RT')
			cx.heading('Insc estadual', text='Insc estadual')

			preenche_treeview()

			et_consulta.bind('<Return>', lambda e: consulta_treeview())
			cx.bind('<Return>', lambda e: dado_treeview())

			lb_consulta.grid(row=0, column=0, columnspan=3, pady=(10, 10))
			op_menu.grid(row=2, column=0, padx=10)
			et_consulta.grid(row=2, column=1, padx=10)
			bt_consulta.grid(row=2, column=2, padx=10)
			cx.grid(row=3, column=0, columnspan=3, pady=10, padx=20)
			bt_alterar.grid(row=4, column=0, pady=5)
			bt_excluir.grid(row=4, column=1, pady=5)
			bt_atualizar.grid(row=4, column=2, pady=5)

			def fecha_janela():
				Consultas.janela_consulta_empresa_aberta = False
				janela_consulta_empresa.destroy()

			janela_consulta_empresa.protocol('WM_DELETE_WINDOW', fecha_janela)

	def janel_consulta_usuario(self):
		val = Validacoes()
		janela_altera_usuario_aberta=False
		def preenche_treeview():

			cx.delete(*cx.get_children())
			usuario = db.consultar_tabela_bd('usuarios')

			for v, item in enumerate(usuario):
				if v % 2 == 0:

					cx.insert(
						'', 'end', values=item[:-1], tags=('linha_par',), image=img_excluir)
				else:
					cx.insert('', 'end', values=item[:-1], image=img_excluir)

		def consulta_treeview():
			usuario = []
			opcao = op_menu.get().lower()
			if opcao == 'id':
				opcao = 'id_usuario'

			lb_erro.grid_forget()
			cx.delete(*cx.get_children())
			usuario = db.consulta_dados_bd(
				et_consulta.get(), opcao, 'usuarios')
			try:
				if et_consulta.get() and usuario[0]:
					for v, item in enumerate(usuario):
						list_item = [
							list_item for list_item in item if list_item != item[6]]

						if v % 2 == 0:
							cx.insert('', 'end', values=list_item,
									  tags=('linha_par',))
						else:
							cx.insert('', 'end', values=list_item)
				else:
					preenche_treeview()
			except IndexError:
				lb_erro.configure(
					text='Usuário nao encontrado!', text_color='red')
				lb_erro.grid(row=1, column=0, columnspan=3)

		def dado_treeview():

			valor_selecionado = cx.selection()
			if valor_selecionado:
				dados = cx.item(valor_selecionado)['values']
			print(dados)
		self.cont = 0

		def altera_usuario():
			nonlocal janela_altera_usuario_aberta

			usuario = None
			linha = cx.selection()
			if linha:
				usuario = cx.item(linha)['values']

			def salvar_alteracao():
				def validacao():
					if not val.validar_nome(et_nome) or\
							not val.validar_cpf(et_cpf, True) or\
							not val.validar_email(et_email, True) or\
							not val.validar_telefone(et_fone) or\
							not val.validar_apelido(et_apelido, True):
						val.validar_nome(et_nome)
						val.validar_cpf(et_cpf)
						val.validar_email(et_email)
						val.validar_telefone(et_fone)
						val.validar_apelido(et_apelido)
						return False
					else:
						return True

				if validacao():

					db.alterar_dados_id_bd('usuarios', {
						'id_usuario': int(usuario[0]),
						'nome': et_nome.get(),
						'cpf': et_cpf.get(),
						'email': et_email.get(),
						'telefone': et_fone.get(),
						'apelido': et_apelido.get()
					})
     
			if usuario:
				if not janela_altera_usuario_aberta and usuario:
					janela_altera_usuario_aberta=True
	
					img_caneta = ctk.CTkImage(Image.open(
						'img\\caneta_preta (2).png'), Image.open('img\\caneta_branca (2).png'))

					janela_altera_usuario = JanelaTop(
						'240x420', (False, False), 'Atualização cadastral')
					frame = ctk.CTkFrame(janela_altera_usuario,
										width=380, height=380)
					lb_titulo = ctk.CTkLabel(
						frame, text='Atualização cadastral', text_color=self.azul, font=('', 20))
					lb_nome = ctk.CTkLabel(
						frame, text='Nome', text_color=self.azul)
					bt_nome_alt = ctk.CTkButton(
						frame, image=img_caneta, text='', width=40, command=lambda: et_nome.configure(state='normal'))
					et_nome = ctk.CTkEntry(frame)
					lb_cpf = ctk.CTkLabel(frame, text='CPF', text_color=self.azul)
					bt_cpf_alt = ctk.CTkButton(
						frame, image=img_caneta, text='', width=40, command=lambda: et_cpf.configure(state='normal'))
					et_cpf = ctk.CTkEntry(frame)
					lb_email = ctk.CTkLabel(
						frame, text='E-mail', text_color=self.azul)
					bt_email_alt = ctk.CTkButton(
						frame, image=img_caneta, text='', width=40, command=lambda: et_email.configure(state='normal'))
					et_email = ctk.CTkEntry(frame)
					lb_fone = ctk.CTkLabel(
						frame, text='Telefone', text_color=self.azul)
					bt_fone_alt = ctk.CTkButton(
						frame, image=img_caneta, text='', width=40, command=lambda: et_fone.configure(state='normal'))
					et_fone = ctk.CTkEntry(frame)
					lb_apelido = ctk.CTkLabel(
						frame, text='Apelido', text_color=self.azul)
					et_apelido = ctk.CTkEntry(frame)
					bt_apelido_alt = ctk.CTkButton(
						frame, image=img_caneta, text='', width=40, command=lambda: et_apelido.configure(state='normal'))
					bt_salvar = ctk.CTkButton(
						frame, text='Salvar', command=salvar_alteracao)
		
					if usuario:
						et_nome.insert(0, usuario[1])
						et_cpf.insert(0, usuario[2])
						et_email.insert(0, usuario[3])
						et_fone.insert(0, usuario[4])
						et_apelido.insert(0, usuario[5])

					et_nome.configure(state='disabled')
					et_cpf.configure(state='disabled')
					et_email.configure(state='disabled')
					et_fone.configure(state='disabled')
					et_apelido.configure(state='disabled')

					frame.pack(padx=10, pady=10, fill='both', expand=True)
					lb_titulo.grid(row=0, columnspan=2, pady=15, padx=10)
					lb_nome.grid(row=1, padx=10)
					bt_nome_alt.grid(row=2, column=1, padx=(0, 10), sticky='w')
					et_nome.grid(row=2, padx=(10, 0))
					lb_cpf.grid(row=3, padx=10)
					bt_cpf_alt.grid(row=4, column=1, padx=(0, 10), sticky='w')
					et_cpf.grid(row=4, padx=(10, 0))
					lb_email.grid(row=5, padx=10)
					bt_email_alt.grid(row=6, column=1, padx=(0, 10), sticky='w')
					et_email.grid(row=6, padx=(10, 0))
					lb_fone.grid(row=7, padx=10)
					bt_fone_alt.grid(row=8, column=1, padx=(0, 10), sticky='w')
					et_fone.grid(row=8, padx=(10, 0))
					lb_apelido.grid(row=9, padx=10)
					bt_apelido_alt.grid(row=10, column=1, padx=(0, 10), sticky='w')
					et_apelido.grid(row=10, padx=(10, 0))
					bt_salvar.grid(row=11, column=0,
								columnspan=2, pady=15, padx=10)
	
					def fecha_janela():
						nonlocal janela_altera_usuario_aberta
						janela_altera_usuario_aberta = False
						janela_altera_usuario.destroy()
	
					janela_altera_usuario.protocol('WM_DELETE_WINDOW',fecha_janela)
			
	


		def excluir_usuario():
			linha=cx.selection()
			if linha:
				usuario=cx.item(linha)['values']
			def excluir():
				if usuario:
					if db.excluir_registro_bd('usuarios', 'id_usuario',usuario[0]):
						janela.destroy()
				else:
					val.janel_erro('É necessario selecionar um usuário')
  
  
			janela = JanelaTop('400x170',(False,False),'Confirmação')
			frame =ctk.CTkFrame(janela)
			lb_conf= ctk.CTkLabel(frame,text='Confirme a exclução do usuario:',text_color=self.azul, font=('', 20))
			lb_usuario =ctk.CTkLabel(frame, text=usuario[1], text_color='red', font=('', 20))
			bt_conf= ctk.CTkButton(frame,text='OK', command=excluir)
			
			frame.pack(padx=10, pady=10, fill='both', expand=True)		
			lb_conf.pack(pady=(10,5))
			lb_usuario.pack(pady=(5,10))
			bt_conf.pack(pady=10)

   
			
				

		if not Consultas.janela_consulta_usuario_aberta:
			Consultas.janela_consulta_usuario_aberta = True

			janela_consulta_usuario = JanelaTop(
				'600x380', (False, False), 'Consulta usuário')

			lb_consulta = ctk.CTkLabel(
				janela_consulta_usuario, text='Consulta usuário', text_color=self.azul, font=('Roboto', 20))
			lb_erro = ctk.CTkLabel(janela_consulta_usuario, text='')
			op_menu = ctk.CTkOptionMenu(janela_consulta_usuario, values=[
				'Nome', 'CPF', 'Email', 'Telefone', 'Apelido', 'Id'])
			et_consulta = ctk.CTkEntry(
				janela_consulta_usuario, placeholder_text='<<< Informe o campo')
			bt_consulta = ctk.CTkButton(
				janela_consulta_usuario, text='Consulta', command=consulta_treeview)
			bt_alterar = ctk.CTkButton(janela_consulta_usuario, text='Alterar', command=altera_usuario)
			bt_excluir = ctk.CTkButton(janela_consulta_usuario, text='Excluir', command=excluir_usuario)
			bt_atualizar = ctk.CTkButton(
				janela_consulta_usuario, text='Atualizar', command=preenche_treeview)

			# estilo do treeview
			estilo = ttk.Style()
			estilo.theme_use('default')
			estilo.configure('Treeview',
							 foreground='black',
							 rowheight=20
							 )
			estilo.map('Treeview',
					   background=[('selected', self.azul)])

			cx = ttk.Treeview(janela_consulta_usuario, columns=(
				'Id', 'Nome', 'CPF', 'E-mail', 'Telefone', 'Apelido'), show='headings')

			with Image.open('img\\excluir_vermelho (1).png') as img:
				img_excluir = ImageTk.PhotoImage(img, master=cx)

			cx.tag_configure('linha_par', background=self.azul_claro)

			cx.column('Id', minwidth=0, width=30)
			cx.column('Nome', minwidth=0, width=110)
			cx.column('CPF', minwidth=0, width=100)
			cx.column('E-mail', minwidth=0, width=120)
			cx.column('Telefone', minwidth=0, width=100)
			cx.column('Apelido', minwidth=0, width=100)

			cx.heading('Id', text='ID')
			cx.heading('Nome', text='Nome')
			cx.heading('CPF', text='CPF')
			cx.heading('E-mail', text='E-mail')
			cx.heading('Telefone', text='Telefone')
			cx.heading('Apelido', text='Apelido')

			preenche_treeview()

			et_consulta.bind('<Return>', lambda e: consulta_treeview())
			cx.bind('<Return>', lambda e: dado_treeview())
			cx.bind('<Button-1>', lambda e: altera_usuario())

			lb_consulta.grid(row=0, column=0, columnspan=3, pady=(10, 20))
			op_menu.grid(row=2, column=0, padx=10)
			et_consulta.grid(row=2, column=1, padx=10)
			bt_consulta.grid(row=2, column=2, padx=10)
			cx.grid(row=3, column=0, columnspan=3, pady=10, padx=20)
			bt_alterar.grid(row=4, column=0, pady=5)
			bt_excluir.grid(row=4, column=1, pady=5)
			bt_atualizar.grid(row=4, column=2, pady=5)

			def fecha_janela_usuario():
				Consultas.janela_consulta_usuario_aberta = False
				janela_consulta_usuario.destroy()

			janela_consulta_usuario.protocol(
				'WM_DELETE_WINDOW', fecha_janela_usuario)
			# janela_consulta_usuario.mainloop()

	def janel_consulta_vendas(self):

		def preenche_treeview():
			cx.delete(*cx.get_children())
			usuario = db.consultar_tabela_bd('vendas')
			for v, item in enumerate(usuario):
				list_item = [n_item for n_item in item]
				if list_item[1] == None:
					list_item[1] = 'Sem CPF'
				if list_item[3]:
					list_item[3] = f'R$: {list_item[3]:.2f}'
				if list_item[1] != 'Sem CPF':
					list_item[1] = db.consulta_dado_bd(
						list_item[0], 'cpf', 'clientes')[0][2]
				if list_item[2]:
					list_item[2] = self.formata.formata_data_bd(list_item[2])

				if v % 2 == 0:
					cx.insert('', 'end', values=list_item, tags=('linha_par',))
				else:
					cx.insert('', 'end', values=list_item)

		def consulta_treeview():
			opcao = None
			if op_menu.get() == 'Id venda':
				opcao = 'id_venda'
			elif op_menu.get() == 'CPF':
				opcao = 'cliente_id'
			elif op_menu.get() == 'Data':
				opcao = 'data_venda'

			cx.delete(*cx.get_children())

			venda = db.consulta_dado_bd(
				et_consulta.get(), opcao, 'vendas')
			try:
				if et_consulta.get() and venda[0]:
					for v, item in enumerate(venda):
						list_item = [n_item for n_item in item]
						if list_item[1] == None:
							list_item[1] = 'Sem CPF'
						else:
							list_item[1] = self.formata.formata_cpf(
								list_item[1])
						if list_item[3]:
							list_item[3] = f'R$: {list_item[3]:.2f}'
						if list_item[1] != 'Sem CPF':
							list_item[1] = db.consulta_dado_bd(
								list_item[0], 'cpf', 'clientes')[0][2]
						if list_item[2]:
							list_item[2] = self.formata.formata_data_bd(
								list_item[2])

						if v % 2 == 0:
							cx.insert('', 'end', values=list_item,
									  tags=('linha_par',))
						else:
							cx.insert('', 'end', values=list_item)
				else:
					preenche_treeview()
			except IndexError:
				lb_erro.configure(
					text='Produto nao encontrado!', text_color='red')
				lb_erro.grid(row=1, column=0, columnspan=3)

		if not Consultas.janela_consulta_vendas_aberta:
			Consultas.janela_consulta_vendas_aberta = True

			janela_consulta_vendas = JanelaTop(
				'480x380', (False, False), 'Consulta vendas')

			lb_consulta = ctk.CTkLabel(
				janela_consulta_vendas, text='Consulta vendas', font=('Roboto', 20))
			lb_erro = ctk.CTkLabel(janela_consulta_vendas, text='')
			op_menu = ctk.CTkOptionMenu(janela_consulta_vendas, values=[
				'Id venda', 'CPF', 'Data',])
			et_consulta = ctk.CTkEntry(
				janela_consulta_vendas, placeholder_text='<<< Informe o campo')
			bt_consulta = ctk.CTkButton(
				janela_consulta_vendas, text='Consulta', command=consulta_treeview)
			et_consulta.bind('<Return>', lambda e: consulta_treeview())

			# estilo do treeview
			estilo = ttk.Style()
			estilo.theme_use('default')
			estilo.configure('Treeview',
							 foreground='black',
							 rowheight=20
							 )
			estilo.map('Treeview',
					   background=[('selected', self.azul)])

			cx = ttk.Treeview(janela_consulta_vendas, columns=(
				'Id vendas', 'CPF cliente', 'Data', 'Valor total'), show='headings')

			cx.tag_configure('linha_par', background=self.azul_claro)

			cx.column('Id vendas', minwidth=0, width=30)
			cx.column('CPF cliente', minwidth=0, width=110)
			cx.column('Data', minwidth=0, width=120)
			cx.column('Valor total', minwidth=0, width=80)

			cx.heading('Id vendas', text='ID')
			cx.heading('CPF cliente', text='CPF cliente')
			cx.heading('Data', text='Data/Hora')
			cx.heading('Valor total', text='Total venda')

			preenche_treeview()

			lb_consulta.grid(row=0, column=0, columnspan=3, pady=20)
			op_menu.grid(row=1, column=0, padx=10)
			et_consulta.grid(row=1, column=1, padx=10)
			bt_consulta.grid(row=1, column=2, padx=10)
			cx.grid(row=2, column=0, columnspan=4, pady=10, padx=20)

			def fecha_janela():
				Consultas.janela_consulta_vendas_aberta = False
				janela_consulta_vendas.destroy()

			janela_consulta_vendas.protocol('WM_DELETE_WINDOW', fecha_janela)

	def janel_consulta_produtos(self):

		if not Consultas.janela_consulta_produtos_aberta:
			Consultas.janela_consulta_produtos_aberta = True
			janela_consulta_produtos = JanelaTop(
				'420x350', (False, False), 'Consulta produtos')

			def preenche_treeview():
				cx.delete(*cx.get_children())
				produto = db.consultar_tabela_bd(
					'produtos')

				for v, item in enumerate(produto):
					list_item = [lista for lista in item]
					if list_item[2]:
						list_item[2] = f'R$: {item[2]:.2f}'

					if v % 2 == 0:
						cx.insert('', 'end', values=list_item,
								  tags='linha_par')
					else:
						cx.insert('', 'end', values=list_item)

			def consulta_treeview():
				produto = ''
				opcao = 'id_produto'
				lb_erro.grid_forget()
				if op_menu.get() == 'Id' and et_consulta.get().isdigit():
					opcao = 'id_produto'
				elif op_menu.get() == 'Descrição' and et_consulta.get():
					opcao = 'prod_descricao'

				produto = db.consulta_dados_bd(
					et_consulta.get(), opcao, 'produtos')

				cx.delete(*cx.get_children())
				try:
					if et_consulta.get() and produto[0]:
						for v, item in enumerate(produto):
							list_item = [lista for lista in item]
							if list_item[2]:
								list_item[2] = f'R$: {item[2]:.2f}'

							if v % 2 == 0:
								cx.insert('', 'end', values=list_item,
										  tags=('linha_par',))
							else:
								cx.insert('', 'end', values=list_item)
					else:
						preenche_treeview()
				except IndexError:
					lb_erro.configure(
						text='Produto nao encontrado!', text_color='red')
					lb_erro.grid(row=1, column=0, columnspan=3)

			lb_titulo = ctk.CTkLabel(
				janela_consulta_produtos, text='Consulta produtos', font=('Roboto', 20))
			lb_erro = ctk.CTkLabel(janela_consulta_produtos, text='')
			op_menu = ctk.CTkOptionMenu(janela_consulta_produtos, width=110, values=[
				'Id', 'Descrição'])
			et_consulta = ctk.CTkEntry(
				janela_consulta_produtos, placeholder_text='<<< Informe o campo')
			bt_consulta = ctk.CTkButton(
				janela_consulta_produtos, text='Consulta', width=110, command=consulta_treeview)

			et_consulta.bind('<Return>', lambda e: consulta_treeview())

			# estilo do treeview
			estilo = ttk.Style()
			estilo.theme_use('default')
			estilo.configure('Treeview',
							 # background='lightgray',
							 foreground='black',
							 rowheight=20,
							 # fieldbackground='lightgray'#B0C4DE'
							 )
			estilo.map('Treeview',
					   background=[('selected', self.azul)])

			cx = ttk.Treeview(janela_consulta_produtos, columns=(
				'Id', 'Descrição', 'Preço', 'Grupo'), show='headings')

			cx.tag_configure('linha_par', background=self.azul_claro)

			cx.column('Id', minwidth=0, width=30)
			cx.column('Descrição', minwidth=0, width=150)
			cx.column('Preço', minwidth=0, width=100)
			cx.column('Grupo', minwidth=0, width=100)

			cx.heading('Id', text='Id')
			cx.heading('Descrição', text='Descrição')
			cx.heading('Preço', text='Preço')
			cx.heading('Grupo', text='Grupo')

			preenche_treeview()

			lb_titulo.grid(row=0, column=0, columnspan=3, pady=10)
			op_menu.grid(row=2, column=0, padx=10)
			et_consulta.grid(row=2, column=1, padx=10)
			bt_consulta.grid(row=2, column=2, padx=10)
			cx.grid(row=3, column=0, columnspan=3, pady=10, padx=20)

			def fecha_janela():
				janela_consulta_produtos.destroy()
				Consultas.janela_consulta_produtos_aberta = False

			janela_consulta_produtos.protocol('WM_DELETE_WINDOW', fecha_janela)


class Vendas():
	janela_vendas_aberta = False
	janela_inf_vendas_aberta = False
	produto = None
	vl_total = 0.0
	lista_venda = []
	widgets = None
	cpf_cliente = None
	venda_id = None

	def __init__(self) -> None:

		self.lb_troco_valor = None
		self.cont = 0
		self.azul = '#0080FF'
		self.azul_metal_claro = '#B0C4DE'
		self.azul_claro = '#ADD8E6'
	# busca o produto no banco de dados para incluir na venda

	def adicionar_linha_produto(self):

		img_excluir = ctk.CTkImage(Image.open('img\\excluir_vermelho (2).png'))
		linha_produtos = []

		if self.et_cod_produto.get().isdigit():
			Vendas.produto = db.consulta_dado_especifico_bd(
				self.et_cod_produto.get(), 'id_produto', 'produtos')

		elif self.et_cod_produto.get().replace(' ', '').isalpha():
			Vendas.produto = db.consulta_dado_bd(
				self.et_cod_produto.get(), 'prod_descricao', 'produtos')[0]
		else:
			print('Produto nao cadastrado!')

		# labels para adicionar informações dos produtos
		self.lb_add_cod_produto = ctk.CTkLabel(
			self.frame_lista, text=Vendas.produto[0])
		self.lb_add_descricao_produto = ctk.CTkLabel(
			self.frame_lista, text=Vendas.produto[1], width=200)
		self.lb_add_valorunit_produto = ctk.CTkLabel(
			self.frame_lista, text=Vendas.produto[2], width=80)

		# entrada de quantidade de produto
		self.et_add_quant_produto = ctk.CTkEntry(
			self.frame_lista, placeholder_text=1, width=35)
		self.et_add_quant_produto.bind(
			'<FocusOut>', lambda e: self.soma_total())
		self.et_add_quant_produto.bind(
			'<FocusOut>', lambda e: self.conf_debit())
		self.et_add_quant_produto.bind('<Return>', lambda e: self.soma_total())
		self.et_add_quant_produto.bind('<Return>', lambda e: self.conf_debit())

		self.lb_add_valor_produto = ctk.CTkLabel(
			self.frame_lista, text=Vendas.produto[2], width=80)

		self.lb_add_valor_produto.grid(
			row=self.cont, column=4, padx=10, pady=5)

		# exclui a linhas do produto caso o label seja clicado
		def excluir_linha():
			cont = 0
			for wid in linha_produtos:
				wid.destroy()
				cont += 1
			# quando exclui atualiza a lista de widgets e refaz a soma
			Vendas.widgets = self.frame_lista.winfo_children()
			self.soma_total()
			self.conf_debit()

		# posicionar os labels na lista de compras
		self.lb_add_cod_produto.grid(
			row=self.cont, column=0, padx=10, pady=5)
		self.lb_add_descricao_produto.grid(
			row=self.cont, column=1, padx=10, pady=5)
		self.lb_add_valorunit_produto.grid(
			row=self.cont, column=2, padx=10, pady=5)
		self.et_add_quant_produto.grid(
			row=self.cont, column=3, padx=10, pady=5)

		# label para excluir produtos da lista
		lb_excluir_produto = ctk.CTkLabel(
			self.frame_lista, image=img_excluir, text='', width=80)
		lb_excluir_produto.grid(row=self.cont, column=5, padx=10, pady=5)
		lb_excluir_produto.bind('<Button-1>', lambda e:  excluir_linha())

		# atualizar a lista de widgets e chama a função soma_total
		Vendas.widgets = self.frame_lista.winfo_children()
		self.soma_total()
		self.conf_debit()

		# adiciona os produtos na lista
		linha_produtos.append(self.lb_add_cod_produto)
		linha_produtos.append(self.lb_add_descricao_produto)
		linha_produtos.append(self.lb_add_valorunit_produto)
		linha_produtos.append(self.et_add_quant_produto)
		linha_produtos.append(self.lb_add_valor_produto)
		linha_produtos.append(lb_excluir_produto)

		# limpa o campo para nova inserção
		self.et_cod_produto.delete(0, 'end')

		# contador
		self.cont += 1

	# atualiza o label com o total da lista

	def soma_total(self):
		total = 0
		for v, wid in enumerate(Vendas.widgets):

			if isinstance(wid, ctk.CTkEntry) and wid.get() != '':
				valor_un = Vendas.widgets[v-1].cget('text')*int(wid.get())
				Vendas.widgets[v+1].configure(text=valor_un)

			if isinstance(wid, ctk.CTkEntry):
				total += Vendas.widgets[v+1].cget('text')

		Vendas.vl_total = total
		self.lb_sub_total_valor.configure(text=f'{Vendas.vl_total:.2f}')
		self.diminuir_lb(self.lb_sub_total_valor)

	def diminuir_lb(self, lb):
		tamanho = 30
		text_lb = lb.cget('text')
		for _ in range(4, len(text_lb)):
			tamanho -= 3
			lb.configure(font=('', tamanho))

	def janela_erro(self, texto):
		janela_erro = JanelaTop('350x100', (False, False), 'Erro!')
		lb_erro = ctk.CTkLabel(janela_erro, text=texto, font=('', 15))
		lb_erro.pack()

	def registrar_venda(self):
		lista_itens = []
		cod_produto = None
		quantidade = None
		valor_unit = None
		grupo_produto = None
		data = dt.datetime.now()
		data_formatada = data.strftime('%Y-%m-%d %H:%M:%S')

		if Vendas.widgets:
			for v, wid in enumerate(Vendas.widgets):
				if isinstance(wid, ctk.CTkEntry):
					quantidade = wid.get()
					valor_unit = Vendas.widgets[v-1].cget('text')
					cod_produto = Vendas.widgets[v-3].cget('text')

					try:
						quantidade = int(quantidade)
					except ValueError:
						quantidade = 1

					produto = db.consulta_dado_especifico_bd(
						cod_produto, 'id_produto', 'produtos')[0]

					if produto:
						grupo_produto = produto[3]

					if quantidade and valor_unit and grupo_produto and cod_produto:
						item = cod_produto, quantidade, valor_unit, grupo_produto
						lista_itens.append(item)

			if len(lista_itens) > 0:
				for prod in lista_itens:
					db.inserir_dados_key_bd('itens_venda', [
											'produto_id', 'quantidade', 'valor_unitario', 'grupo_produto'], prod)
		else:
			self.janela_erro('Você precisa ter itens para registrar.')

		if Vendas.cpf_cliente:
			cliente = db.consulta_dado_bd(
				Vendas.cpf_cliente, 'cpf', 'clientes')
			db.inserir_dados_key_bd('vendas', ['cliente_id', 'data_venda', 'valor_total'], [
									cliente[0], data_formatada, Vendas.vl_total])
		else:
			db.inserir_dados_key_bd('vendas', ['data_venda', 'valor_total'], [
									data_formatada, Vendas.vl_total])

	def emitir_nf(self):

		val = Validacoes()
		fiscal_prod = []
		lista_produtos = []
		valor_trib_aprox = 0.0
		conf_fiscal = db.consultar_tabela_bd('conf_nfe')

		for emp in conf_fiscal:
			fiscal_prod.append(emp[1])

		janela = JanelaTop('310x210', (True, True), 'Emitir NFe')
		frame = ctk.CTkFrame(janela)
		lb_titulo = ctk.CTkLabel(
			frame, text='Emissão NFe', text_color=self.azul, font=('', 25))
		lb_empresa_emit = ctk.CTkLabel(
			frame, text='Configura NFe', text_color=self.azul)
		op_empresa = ctk.CTkOptionMenu(frame, values=fiscal_prod)
		lb_cpf_cliente = ctk.CTkLabel(
			frame, text='CPF   *Opcional', text_color=self.azul)
		et_inf_cpf = ctk.CTkEntry(frame, placeholder_text='Informe o CPF')
		bt_emitir = ctk.CTkButton(frame, text='Emitir', command=lambda: envia_nfe(
			et_inf_cpf.get(), op_empresa.get()))

		frame.pack(fill='both', anchor='center', expand=True)
		lb_titulo.grid(row=0, column=0, columnspan=2)
		lb_empresa_emit.grid(row=1, column=0, padx=10)
		op_empresa.grid(row=2, column=0, pady=5, padx=10)
		lb_cpf_cliente.grid(row=1, column=1, padx=10)
		et_inf_cpf.grid(row=2, column=1)
		bt_emitir.grid(row=3, column=0, columnspan=2)

		# coleta todos os produtos e valores da venda
		if Vendas.widgets:
			for v, wid in enumerate(Vendas.widgets):
				if isinstance(wid, ctk.CTkEntry):
					cod = str(Vendas.widgets[v-3].cget("text"))
					grup_prod = db.consulta_dado_especifico_bd(
						cod, 'id_produto', 'produtos')
					if wid.get():
						quant = wid.get()
					else:
						quant = 1
					produto = {'codigo': Vendas.widgets[v-3].cget('text'),
							   'descricao': Vendas.widgets[v-2].cget('text'),
							   'val_unitario': Vendas.widgets[v-1].cget('text'),
							   'quantidade': quant,
							   'grupo': grup_prod[0][3]}
					Vendas.lista_venda.append(produto)

		# cria o diretorio caso nao exista
		diretorio = 'xml_nfe'
		if not os.path.exists(diretorio):
			os.makedirs(diretorio)

		for prod in Vendas.lista_venda:
			valor_total_bruto = float(
				prod['quantidade']) * (prod['val_unitario'])
			valor_trib_aprox += valor_total_bruto*0.18  # verificar como calcula

			if prod:
				grupo_prod = db.consulta_dado_bd(
					prod['grupo'], 'nome_grupo', 'fiscal_produto')[0]
				# print(grupo_prod,'dado: ',grupo_prod[9][1])
				dados_prod = {
					'codigo': str(prod['codigo']),
					'descricao': str(prod['descricao']),
					'ncm': str(grupo_prod[2]),
					'cfop': str(grupo_prod[3]),
					'unidade_comercial': str(grupo_prod[4]),
					'ean': str(grupo_prod[5]),
					'ean_tributavel': str(grupo_prod[6]),
					'quatidade_comercial': str(prod['quantidade']),
					'valor_unitario_comercial': str(prod['val_unitario']),
					'valor_total_bruto': str(valor_total_bruto),
					'unidade_tributavel': str(grupo_prod[7]),
					'quantidade_tributavel': str(prod['quantidade']),
					'valor_unitario_tributavel': str(prod['val_unitario']),
					'ind_total': 1,
					'icms_modalidade': str(grupo_prod[8]),
					'icms_origem': int(grupo_prod[9][0]),
					'icms_csosn': str(grupo_prod[10]),
					'pis_modalidade': str(grupo_prod[11]),
					'confins_modalidade': str(grupo_prod[12]),
					'valor_tributos_aproximados': str(valor_trib_aprox)
				}
				lista_produtos.append(dados_prod)

		responsavel_tecnico = dict(
			cnpj_responsavel='27138175000116',
			contato_responsavel='Jessé Varjao',
			email_responsavel='jesseaff@gmail.com',
			fone_responsavel='61983453152')

		def envia_nfe(cpf, op):
			emitente = db.consulta_dado_bd(db.consulta_dado_bd(
				op, 'nome_config_nfe', 'conf_nfe')[0][21], 'cnpj', 'empresas')[0]
			tip_doc = 'cpf'
			tab_conf = [
				nova_list for fisc in conf_fiscal for nova_list in fisc]
			if len(cpf) == 11:
				tip_doc = 'cpf'
			if len(cpf) == 14:
				tip_doc = 'cnpj'

			tab_conf[4] = int(tab_conf[4][:1])
			tab_conf[5] = int(tab_conf[5][:1])
			tab_conf[6] = int(tab_conf[6][:2])
			tab_conf[7] = str(tab_conf[7])
			tab_conf[8] = str(tab_conf[8])
			tab_conf[9] = int(tab_conf[9][:1])
			tab_conf[10] = str(tab_conf[10])
			tab_conf[11] = int(tab_conf[11][:1])
			tab_conf[12] = str(tab_conf[12][:1])
			tab_conf[13] = int(tab_conf[13][:1])
			tab_conf[14] = int(tab_conf[14][:1])
			tab_conf[15] = int(tab_conf[15][:1])
			tab_conf[16] = str(tab_conf[16][:1])
			tab_conf[17] = str(tab_conf[17][:1])
			tab_conf[18] = int(tab_conf[18][:1])
			tab_conf[19] = str(tab_conf[19])
			tab_conf[20] = str(tab_conf[20])

			emitente = [str(var) for var in emitente]

			cliente = None
			if cpf:
				if val.validar_cpf(et_inf_cpf):
					cliente = [tip_doc, cpf]
				else:
					et_inf_cpf.configure(border_color='red')
					return False

			nfe = envio_nf.NFe(
				**{'uf': tab_conf[2],
				   'natureza_operacao': tab_conf[3],
				   'forma_pagamento': tab_conf[4],
				   'tipo_pagamento': tab_conf[5],
				   'modelo': tab_conf[6],
				   'serie': tab_conf[7],
				   'numero_nf': tab_conf[8],
				   'tipo_documento2': tab_conf[9],
				   'municipio': tab_conf[10],
				   'tipo_impressao_danfe': tab_conf[11],
				   'forma_emissao': tab_conf[12],
				   'cliente_final': tab_conf[13],
				   'indicador_destino': tab_conf[14],
				   'indicador_presencial': tab_conf[15],
				   'finalidade_emisssao': tab_conf[16],
				   'processo_emissao': tab_conf[17],
				   'transporte_modalidade': tab_conf[18],
				   'informacoes_adicionais_interesse_fisco': tab_conf[19],
				   'csc': tab_conf[20],
				   'totais_tributos_aproximado': valor_trib_aprox
				   },
				**responsavel_tecnico,
				emitent=emitente,
				cliente=cliente,
				produtos=lista_produtos
			)

			db.gerar_novo_numero_nfe()

			if et_inf_cpf.get():
				ver_cliente = db.consulta_dado_bd(
					int(et_inf_cpf.get()), 'cpf', 'clientes')
				if ver_cliente[0] is None:
					cpf_cliente = db.inserir_dados_key_bd(
						'clientes', ['cpf',], [et_inf_cpf.get()])
					print('cliente salvo: ', cpf_cliente)

	""" def inf_cpf(self):
		def salva_cliente():
			Vendas.cpf_cliente=et_cpf.get()
			db.inserir_dados_key_bd('clientes',['cpf'],[Vendas.cpf_cliente])
			janela_cpf_cliente.destroy()


		janela_cpf_cliente=JanelaTop('230x80',resizable=(False,False),title='Informe o CPF do cliente')
		lb_titulo =ctk.CTkLabel(janela_cpf_cliente, text='CPF', font=('',15))
		et_cpf =ctk.CTkEntry(janela_cpf_cliente,placeholder_text='CPF')
		bt_ok = ctk.CTkButton(janela_cpf_cliente,width=50, text='ok', command=salva_cliente)
		
		lb_titulo.grid(row=0,column=0, columnspan=2, padx=10, pady=5)
		et_cpf.grid(row=1, padx=(10,5), pady=5)
		bt_ok.grid(row=1,column=1, padx=(5,10), pady=5) """

	def conf_debit(self):

		total_apg = 0
		self.var2 = self.et_cart_debit.get()

		try:
			self.var2 = float(self.var2)
		except ValueError:
			self.var2 = 0
		if self.et_cart_debit.get():
			self.et_cart_debit.delete(0, 'end')

		if self.var2 != 0:
			self.et_cart_debit.insert(0, f'{self.var2:.2f}')

		total_pg = self.var + self.var2 + self.var3
		self.lb_total_pg_valor.configure(text=f'{total_pg:.2f}')
		self.diminuir_lb(self.lb_total_pg_valor)
		total_apg = Vendas.vl_total - self.var - self.var2 - self.var3
		troco = total_pg - Vendas.vl_total

		if troco > 0:
			self.lb_troco_valor.configure(text=f'{troco:.2f}')
			self.diminuir_lb(self.lb_troco_valor)
		else:
			self.lb_troco_valor.configure(text=f'{0.00:.2f}')

		if total_apg > 0:
			self.lb_total_apg_valor.configure(text=f'{total_apg:.2f}')
			self.diminuir_lb(self.lb_total_apg_valor)
		else:
			self.lb_total_apg_valor.configure(text=f'{0.00:.2f}')

	def janel_vendas(self):
		Vendas.cpf_cliente = None
		Vendas.lista_venda = []
		self.var, self.var2, self.var3 = 0, 0, 0
		self.valor = 0
		val = Validacoes()
		""" def lista_de_compras():
			for wid in Vendas.widgets:
				if isinstance(wid, ctk.CTkLabel) and wid.cget('text'):
					Vendas.lista_venda.append(wid.cget('text'))
				if isinstance(wid, ctk.CTkEntry):
					if wid.get():
						Vendas.lista_venda.append(wid.get())
					else:
						Vendas.lista_venda.append(1)
				Vendas.lista_venda.append(Vendas.produto) """

		def conf_credit():

			total_apg = 0
			self.var = self.et_cart_credit.get()

			try:
				self.var = float(self.var)
			except ValueError:
				self.var = 0

			if self.et_cart_credit.get():
				self.et_cart_credit.delete(0, 'end')

			if self.var != 0:
				self.et_cart_credit.insert(0, f'{self.var:.2f}')

			total_pg = self.var + self.var2 + self.var3
			self.lb_total_pg_valor.configure(text=f'{total_pg:.2f}')
			self.diminuir_lb(self.lb_total_pg_valor)
			troco = total_pg - Vendas.vl_total

			if troco > 0:
				self.lb_troco_valor.configure(text=f'{troco:.2f}')
				self.diminuir_lb(self.lb_troco_valor)
			else:
				self.lb_troco_valor.configure(text=f'{0.00:.2f}')

			total_apg = Vendas.vl_total - self.var - self.var2 - self.var3

			if total_apg > 0:
				self.lb_total_apg_valor.configure(text=f'{total_apg:.2f}')
				self.diminuir_lb(self.lb_total_apg_valor)
			else:
				self.lb_total_apg_valor.configure(text=f'{0.00:.2f}')

		def conf_dinheiro():

			self.var3 = self.et_dinheiro.get()

			try:
				self.var3 = float(self.var3)
			except ValueError:
				self.var3 = 0

			if self.et_dinheiro.get():
				self.et_dinheiro.delete(0, 'end')

			if self.var3 != 0:
				self.et_dinheiro.insert(0, f'{self.var3:.2f}')

			total_pg = self.var + self.var2 + self.var3
			self.lb_total_pg_valor.configure(text=f'{total_pg:.2f}')
			self.diminuir_lb(self.lb_total_pg_valor)
			total_apg = Vendas.vl_total - self.var - self.var2 - self.var3
			troco = total_pg - Vendas.vl_total

			if troco > 0:

				self.lb_troco_valor.configure(text=f'{troco:.2f}')
				self.diminuir_lb(self.lb_troco_valor)
			else:
				self.lb_troco_valor.configure(text=f'{0.00:.2f}')

			if total_apg > 0:
				self.lb_total_apg_valor.configure(text=f'{total_apg:.2f}')
				self.diminuir_lb(self.lb_total_apg_valor)
			else:
				self.lb_total_apg_valor.configure(text=f'{0.00:.2f}')

		img_venda = ctk.CTkImage(Image.open(
			'img\\vendas_preto (2).png'), Image.open('img\\vendas_branco (2).png'))
		img_cartao = ctk.CTkImage(Image.open(
			'img\\cartao_preto (2).png'), Image.open('img\\cartao_branco (2).png'))
		img_dinheiro = ctk.CTkImage(Image.open(
			'img\\dinheiro_preto (2).png'), Image.open('img\\dinheiro_branco (2).png'))

		if not Vendas.janela_vendas_aberta:
			Vendas.janela_vendas_aberta = True
			self.janela_vendas = JanelaTop('700x690', (True, True), 'Vendas')

			self.lb_produto = ctk.CTkLabel(
				self.janela_vendas, text='Lista de compras', font=('', 20))
			self.lb_index = ctk.CTkLabel(self.janela_vendas,
										 text=f'Codigo                           Descrição                                     Valor Unit      Quantidade       Valor                    Excluir '
										 )

			self.frame_lista = ctk.CTkScrollableFrame(
				self.janela_vendas, width=650, height=300)
			self.et_cod_produto = ctk.CTkEntry(
				self.janela_vendas, placeholder_text='Código ou descrição')
			self.frame_total = ctk.CTkFrame(
				self.janela_vendas)
			self.lb_sub_total_text = ctk.CTkLabel(
				self.frame_total, text=f'Subtotal R$:', text_color='#0080FF', font=('', 30))
			self.lb_sub_total_valor = ctk.CTkLabel(
				self.frame_total, text=f'{0.00:.2f}', text_color='#0080FF', font=('', 30), anchor='e')
			self.lb_total_pg_text = ctk.CTkLabel(
				self.frame_total, text=f'Total pago R$:', text_color='#0080FF', font=('', 30))
			self.lb_total_pg_valor = ctk.CTkLabel(
				self.frame_total, text=f'{0.00:.2f}', text_color='#0080FF', font=('', 30), anchor='e')
			self.lb_total_apg_text = ctk.CTkLabel(
				self.frame_total, text=f'Total a pagar R$:', text_color='#0080FF', font=('', 30))
			self.lb_total_apg_valor = ctk.CTkLabel(
				self.frame_total, text=f'{0.00:.2f}', text_color='#0080FF', font=('', 30), anchor='e')
			self.lb_troco_text = ctk.CTkLabel(
				self.frame_total, text=f'Troco R$:', text_color='#0080FF', font=('', 30))
			self.lb_troco_valor = ctk.CTkLabel(
				self.frame_total, text=f'{0.00:.2f}', text_color='#0080FF', font=('', 30), anchor='e')
			self.bt_adicionar = ctk.CTkButton(
				self.janela_vendas, text='Adicionar', command=self.adicionar_linha_produto)
			frame_form_pag = ctk.CTkFrame(self.janela_vendas)
			lb_form_pag = ctk.CTkLabel(
				frame_form_pag, text='Formas de pagamentos', font=('', 15))
			bt_cart_credit = ctk.CTkButton(
				frame_form_pag, text='Cartão de crédito', image=img_cartao, anchor='w')
			bt_cart_debit = ctk.CTkButton(
				frame_form_pag, text='Cartão de débito', image=img_cartao, anchor='w')
			bt_dinheiro = ctk.CTkButton(
				frame_form_pag, text='Dinheiro ou PIX', image=img_dinheiro, anchor='w')
			self.et_cart_credit = ctk.CTkEntry(
				frame_form_pag, placeholder_text='Cartão de crédito')
			self.et_cart_debit = ctk.CTkEntry(
				frame_form_pag, placeholder_text='Cartão de débito')
			self.et_dinheiro = ctk.CTkEntry(
				frame_form_pag, placeholder_text='Dinheiro ou PIX',)

			bt_registrar = ctk.CTkButton(
				self.janela_vendas, text='Registrar venda', command=self.registrar_venda, font=('', 15))
			bt_emitir_nf = ctk.CTkButton(
				self.janela_vendas, text='Emitir NF', command=self.emitir_nf, font=('', 15))

			self.et_cod_produto.bind(
				'<Return>', lambda e: self.adicionar_linha_produto())
			self.et_cod_produto.bind(
				'<Return>', lambda e: self.conf_debit())
			self.et_cod_produto.bind('<FocusOut>', lambda e: self.conf_debit())

			self.et_cart_credit.bind('<FocusOut>', lambda e: conf_credit())
			self.et_cart_credit.bind('<Return>', lambda e: conf_credit())
			self.et_cart_debit.bind('<FocusOut>', lambda e: self.conf_debit())
			self.et_cart_debit.bind('<Return>', lambda e: self.conf_debit())
			self.et_dinheiro.bind('<FocusOut>', lambda e: conf_dinheiro())
			self.et_dinheiro.bind('<Return>', lambda e: conf_dinheiro())

			self.lb_produto.grid(
				row=0, column=1, columnspan=3, pady=(10, 5))
			self.lb_index.grid(
				row=1, column=0, columnspan=4, padx=10, sticky='w')
			self.frame_lista.grid(
				row=2, column=0, columnspan=4, pady=(5, 10), padx=10, sticky='w')
			self.frame_total.grid(
				row=3, rowspan=5, column=2, columnspan=2, pady=10, padx=(0, 10), sticky='nw')
			self.lb_sub_total_text.grid(
				row=0, column=0, pady=10, padx=10, sticky='w')
			self.lb_total_pg_text.grid(
				row=1, column=0, pady=10, padx=10, sticky='w')
			self.lb_total_apg_text.grid(
				row=2, column=0, pady=10, padx=10, sticky='w')
			self.lb_troco_text.grid(
				row=3, column=0, pady=10, padx=10, sticky='w')
			self.lb_sub_total_valor.grid(
				row=0, column=1, pady=10, padx=10, sticky='e')
			self.lb_total_pg_valor.grid(
				row=1, column=1, pady=10, padx=10, sticky='e')
			self.lb_total_apg_valor.grid(
				row=2, column=1, pady=10, padx=10, sticky='e')
			self.lb_troco_valor.grid(
				row=3, column=1, pady=10, padx=10, sticky='e')
			self.et_cod_produto.grid(
				row=3, column=0, padx=10, sticky='w')
			self.bt_adicionar.grid(
				row=3, column=1, padx=10, sticky='w')
			frame_form_pag.grid(
				row=4, rowspan=4, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')
			lb_form_pag.grid(
				row=0, column=0, pady=5, columnspan=2)
			bt_cart_credit.grid(
				row=1, column=0, pady=3, padx=(10, 3), sticky='w')
			bt_cart_debit.grid(
				row=2, column=0, pady=3, padx=(10, 3), sticky='w')
			bt_dinheiro.grid(
				row=3, column=0, pady=(3, 10), padx=(10, 3), sticky='w')
			self.et_cart_credit.grid(
				row=1, column=1, pady=3, padx=(3, 10), sticky='w')
			self.et_cart_debit.grid(
				row=2, column=1, pady=3, padx=(3, 10), sticky='w')
			self.et_dinheiro.grid(
				row=3, column=1, pady=(3, 10), padx=(3, 10), sticky='w')
			bt_registrar.grid(row=8, column=0, padx=10, pady=5, sticky='w')
			bt_emitir_nf.grid(row=8, column=1, padx=10, pady=5, sticky='w')
			""" bt_inf_cpf.grid(row=8, column=2, padx=10, pady=5, sticky='w') """

		def fecha_janela():
			Vendas.janela_vendas_aberta = False
			self.janela_vendas.destroy()

		self.janela_vendas.protocol('WM_DELETE_WINDOW', fecha_janela)

	def criar_pdf_cupom_fiscal(self):
		# Define o tamanho personalizado da página (em pontos)

		empresa = db.consulta_dado_bd('27138175000116', 'cnpj', 'empresas')

		largura = 80
		altura = 300
		cnpj = empresa[1]
		endereco = f"{empresa[7]}, {empresa[8]}, {empresa[9]}, {empresa[10]}, {empresa[11]}"
		insc_estadual = empresa[4]
		itens_cupom = [
			{"produto": "Produto 1", "quantidade": 2, "preco": 10.00},
			{"produto": "Produto 2", "quantidade": 1, "preco": 15.00},
			{"produto": "Produto 3", "quantidade": 3, "preco": 5.00}
		]
		total_cupom = sum(item["quantidade"] * item["preco"]
						  for item in itens_cupom)
		total_pg = 40
		numeronf = 120
		serienf = 1
		cpf_cliente = 12345678998
		chave_acesso = '1234 5678 1234 4567 1236 7896 7894 1236 7894 7896 3215'
		protocolo_aut = 123456789123456
		qrcode = "QRCode"

		# Cria um novo objeto CupomFiscal com tamanho personalizado
		pdf = NFCe(format=(largura, altura))

		# Adiciona uma nova página
		pdf.add_page()

		# Define o tamanho da fonte
		pdf.set_line_width(5)
		pdf.set_font('helvetica', '', 10)
		pdf.set_left_margin(4)
		pdf.set_top_margin(4)
		pdf.set_right_margin(4)

		# Escreve as informações no arquivo PDF
		pdf.cell(0, 4, f"{cnpj}  IE:{insc_estadual}",
				 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.cell(0, 4, f"{endereco}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.cell(0, 1, '-'*60, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

		pdf.cell(0, 4, 'DANFE NFCe- Documento auxiliar da nota',
				 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.cell(0, 4, 'fiscal eletrônica para consumidor final',
				 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.cell(0, 4, 'Não permite aproveitamento de crédito IMCS',
				 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.cell(0, 1, '-'*60, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

		pdf.cell(0, 4, f"Nº|Descrição     | Qtd | Un | Vl Unit | Vl Total",
				 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.cell(0, 1, '-'*60, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

		for v, item in enumerate(itens_cupom):
			pdf.cell(5, 4, f"{v}", new_x=XPos.RIGHT, new_y=YPos.TOP)
			pdf.cell(25, 4, f"{item['produto']}",
					 new_x=XPos.RIGHT, new_y=YPos.TOP)
			pdf.cell(5, 4, f"{item['quantidade']}",
					 new_x=XPos.RIGHT, new_y=YPos.TOP)
			pdf.cell(8, 4, f"{'UN'}", new_x=XPos.RIGHT, new_y=YPos.TOP)
			pdf.cell(13, 4, f"{item['preco']:.2f}",
					 new_x=XPos.RIGHT, new_y=YPos.TOP)
			pdf.cell(10, 4, f"{item['preco']*item['quantidade']:.2f}",
					 new_x=XPos.LMARGIN, new_y=YPos.NEXT)

		pdf.cell(0, 1, '-'*60, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.cell(55, 4, f'Quantidade total de itens: ',
				 new_x=XPos.RIGHT, new_y=YPos.TOP)
		pdf.cell(5, 4, f'{len(itens_cupom):.2f}',
				 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.cell(55, 4, f'Valor total da Nota: ',
				 new_x=XPos.RIGHT, new_y=YPos.TOP)
		pdf.cell(5, 4, f'{total_cupom:.2f} ',
				 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.cell(55, 4, f'Desconto: ', new_x=XPos.RIGHT, new_y=YPos.TOP)
		pdf.cell(5, 4, f'{total_cupom-total_pg:.2f}',
				 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.set_font(style='B', size=10)
		pdf.cell(55, 4, f"Total pago: R$", new_x=XPos.RIGHT, new_y=YPos.TOP)
		pdf.cell(5, 4, f'{total_cupom:.2f}',
				 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.set_font(size=10)
		pdf.cell(0, 1, '-'*60, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.cell(55, 4, f'Tributos totais incidentes:',
				 new_x=XPos.RIGHT, new_y=YPos.TOP)
		pdf.cell(5, 4, f'{total_cupom*0.2314}',
				 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.cell(0, 1, '-'*60, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.cell(55, 4, f'Nº NF: {numeronf}',
				 new_x=XPos.RIGHT, new_y=YPos.TOP)
		pdf.cell(5, 4, f'Serie: {serienf}',
				 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.cell(50, 4, 'Consulte em http://www.nfe.am.gov.br',
				 new_x=XPos.LEFT, new_y=YPos.NEXT)
		pdf.cell(68, 4, 'CHAVE DE ACESSO', align='C',
				 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.set_font(size=7)
		pdf.cell(0, 4, f'{chave_acesso}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.set_font(size=10)
		pdf.cell(0, 1, '-'*60, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.cell(0, 4, 'CONSUMIDOR', align='C',
				 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.cell(0, 4, f'CPF: {cpf_cliente}',
				 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.cell(0, 1, '-'*60, new_x=XPos.LEFT, new_y=YPos.NEXT)
		pdf.cell(0, 4, 'Consulta de leitor via QR Code',
				 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.cell(60, 4, f'{qrcode}', align='C',
				 new_x=XPos.LMARGIN, new_y=YPos.NEXT)
		pdf.cell(
			0, 4, f'Protocolo de autorização: {protocolo_aut}', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

		# Salva o arquivo PDF
		pdf.output("cupom_fiscal.pdf")

	# @staticmethod

	def janela_calendario(self):
		janela = ctk.CTk()
		janela.title('Calendário')

		calendario = Calendar(janela, selectmod='day',
							  year=2023, month=6, day=2)
		calendario.pack()

		janela.mainloop

	def inf_vendas(self):

		def bt_salvar():
			data = et_data.get_date()
			vendas = int(quant_vendas.get())
			db.inserir_dados_bd('inf_vendas', [data, vendas])

		if not Vendas.janela_inf_vendas_aberta:
			Vendas.janela_inf_vendas_aberta = True

			janela_inf_vendas = JanelaTop(
				'200x150', (False, False), 'Informe de vendas Diárias')

			lb_data = ctk.CTkLabel(
				janela_inf_vendas, text='Informe de vendas', font=('', 20))
			lb_data.grid(row=0, column=0, pady=5, padx=10)

			et_data = DateEntry(janela_inf_vendas, date_pattern='dd/mm/yyyy')
			et_data.grid(row=2, column=0, pady=5, padx=(10, 1))

			quant_vendas = ctk.CTkEntry(
				janela_inf_vendas, placeholder_text='Vendas diárias', width=90)
			quant_vendas.grid(row=3, column=0, pady=5, padx=10)

			bt_ok = ctk.CTkButton(janela_inf_vendas, text='OK',
								  width=90, command=bt_salvar)
			bt_ok.grid(row=4, column=0, pady=5, padx=10)

			def fecha_janela():
				Vendas.janela_inf_vendas_aberta = False
				janela_inf_vendas.destroy()

			janela_inf_vendas.protocol('WM_DELETE_WINDOW', fecha_janela)


class Cadastros():
	janela_cad_usuario_aberta = False
	janela_cad_empresa_aberta = False
	janela_cad_produto_aberta = False
	janela_grupo_fiscal_aberta = False
	janela_cad_perfil_aberta = False

	def __init__(self) -> None:
		self.azul = '#0080FF'
		self.azul_metal_claro = '#B0C4DE'
		self.azul_claro = '#ADD8E6'

	def janel_cad_perfil(self):
		val = Validacoes()

		def cad_perfil():
			val.validar_cpf(et_cpf)
			if et_cpf.get():
				usuario = db.consulta_dado_especifico_bd(
					et_cpf.get(), 'cpf', 'usuarios')
				if usuario and et_cpf.get() in usuario:
					lb_usuario_encontrado.configure(
						text=f'Seu apelido: {usuario[5]}\nEle será usado em\nseu historico de vendas')

					if usuario[5]:
						db.inserir_dados_bd(
							'atendentes', [usuario[0], usuario[5], op_perfil.get().lower()])
					else:
						lb_usuario_encontrado.configure(
							text='Você nao cadastrou apelido\nAltere seu cadastro.')
				else:
					lb_usuario_encontrado.configure(text='CPF nao encontrado!')

		if not Cadastros.janela_cad_perfil_aberta:
			Cadastros.janela_cad_perfil_aberta = True

			janela_cad_perfil = JanelaTop(geometry='180x220', resizable=(
				False, False), title='Cadastro de perfil')

			frame_inf = ctk.CTkFrame(janela_cad_perfil, width=140, height=70)

			lb_titulo = ctk.CTkLabel(
				janela_cad_perfil, text='Cadastro de Perfil')
			et_cpf = ctk.CTkEntry(
				janela_cad_perfil, placeholder_text='Digite seu CPF')
			op_perfil = ctk.CTkOptionMenu(
				janela_cad_perfil, values=['Atendente'])
			lb_usuario_encontrado = ctk.CTkLabel(frame_inf, text='')

			bt_salvar = ctk.CTkButton(
				janela_cad_perfil, text='Salvar', width=70, command=cad_perfil)

			lb_titulo.grid(row=0, padx=20, pady=5)
			et_cpf.grid(row=2, padx=20, pady=5)
			op_perfil.grid(row=3, padx=20, pady=5)
			frame_inf.grid(row=4, padx=20, pady=5)
			lb_usuario_encontrado.pack()
			bt_salvar.grid(row=6, padx=20, pady=(10, 5))

			def fecha_janela_perfil():
				Cadastros.janela_cad_perfil_aberta = False
				janela_cad_perfil.destroy()

			janela_cad_perfil.protocol('WM_DELETE_WINDOW',	fecha_janela_perfil)

	def janel_cad_produto(self):
		val = Validacoes()

		def salvar_prod():
			def validar():
				if not val.validar_nome_produto(descricao_produto) or \
						not val.validar_preco_produto(preco_produto):
					val.validar_nome_produto(descricao_produto)
					val.validar_preco_produto(preco_produto)
					return False
				else:
					return True

			if validar():
				db.inserir_dados_key_bd('produtos', ('prod_descricao', 'prod_preco', 'prod_grupo'), (
					descricao_produto.get(), float(preco_produto.get()), grupo_produto.get()))
				lb_erro = ctk.CTkLabel(frame, text='Produto cadastrado com sucesso!', text_color=self.azul,
									   font=('Roboto', 10))
				lb_erro.grid(row=5, column=0, columnspan=2,
							 padx=10, pady=(5, 0))
				descricao_produto.delete(0, ctk.END)
				preco_produto.delete(0, ctk.END)
				descricao_produto.focus_set()

		def converte_preco(widget):
			if widget.get():
				try:
					preco = float(widget.get().replace(',', '.'))
					if isinstance(preco, float):
						widget.configure(border_color='gray')
						widget.delete(0, 'end')
						preco = f'{preco:.2f}'
						widget.insert(0, preco)
					else:
						widget.configure(border_color='red')
				except ValueError:
					widget.configure(border_color='red')
			else:
				widget.configure(border_color='gray')

		def lista_grupo_produto():
			lista_grupo = []
			lista = db.consultar_tabela_bd('fiscal_produto')
			for g in lista:
				lista_grupo.append(g[1])
			return lista_grupo

		if not Cadastros.janela_cad_produto_aberta:
			Cadastros.janela_cad_produto_aberta = True

			janela_cad_produto = JanelaTop(
				'300x350', (False, False), 'Cadastro de produtos')

			janela_cad_produto.rowconfigure(0, weight=1)
			janela_cad_produto.columnconfigure(0, weight=1)

			frame = ctk.CTkFrame(master=janela_cad_produto,
								 width=600, height=600)
			frame.grid(row=0, column=0, sticky='nsew', padx=15, pady=15)
			frame.grid_columnconfigure(0, weight=1)
			frame.grid_columnconfigure(1, weight=1)

			lb_titulo = ctk.CTkLabel(
				frame, text='Cadastro de produtos', font=('', 20))
			lb_descricao = ctk.CTkLabel(
				frame, text='Descrição', font=('', 10))
			descricao_produto = ctk.CTkEntry(
				frame, placeholder_text='Descrição do produto', width=250, font=('', 15))
			lb_preco = ctk.CTkLabel(
				frame, text='Preço', font=('', 10))
			preco_produto = ctk.CTkEntry(
				frame, placeholder_text='Valor do produto', width=250, font=('', 15))
			lb_grupo_produto = ctk.CTkLabel(
				frame, text='Grupo do produto', font=('', 15))
			grupo_produto = ctk.CTkOptionMenu(
				frame, values=lista_grupo_produto())
			bt_salvar = ctk.CTkButton(
				frame, text='Salvar', command=salvar_prod)

			preco_produto.bind(
				'<FocusOut>', lambda event: converte_preco(preco_produto))

			lb_titulo.grid(
				row=0, column=0, columnspan=2)
			lb_descricao.grid(
				row=1, column=0, padx=10, pady=(5, 0), sticky='sw')
			descricao_produto.grid(
				row=2, column=0, columnspan=2, padx=10, pady=(0, 5))
			lb_preco.grid(
				row=3, column=0, padx=10, pady=(5, 0), sticky='w')
			preco_produto.grid(
				row=4, column=0, columnspan=2, padx=10, pady=(0, 5))
			lb_grupo_produto.grid(
				row=6, column=0, columnspan=2, padx=10, pady=(5, 0), sticky='w')
			grupo_produto.grid(
				row=7, column=0, columnspan=2, padx=10, pady=(0, 5))
			bt_salvar.grid(
				row=8, column=0, columnspan=2, padx=10, pady=15, sticky='ns')

			def fechar_janela():
				janela_cad_produto.destroy()
				Cadastros.janela_cad_produto_aberta = False

			janela_cad_produto.protocol('WM_DELETE_WINDOW', fechar_janela)
			janela_cad_produto.mainloop()

	def janel_cad_usuario(self):
		val = Validacoes()
		# verifica os dados do usuario no cadastro e salva no banco de dados

		def salvar_usuario():
			def valida():
				if not val.validar_nome(nome) or \
						not val.validar_cpf(cpf) or \
						not val.validar_email(email) or \
						not val.validar_telefone(celular) or \
						not val.validar_senha(senha1, senha2):
					val.validar_nome(nome)
					val.validar_cpf(cpf)
					val.validar_email(email)
					val.validar_telefone(celular)
					val.validar_senha(senha1, senha2)
					if apelido.get():
						val.validar_apelido(apelido)
					return False
				else:
					return True


			if valida():
				db.inserir_dados_key_bd('usuarios', ('nome', 'cpf', 'email', 'telefone', 'apelido', 'senha'),
										[nome.get(), cpf.get(), email.get(), celular.get(), apelido.get(), senha1.get()])
				cad_janela.after(400, cad_janela.destroy)
				Cadastros.janela_cad_usuario_aberta = False

		if not Cadastros.janela_cad_usuario_aberta:
			Cadastros.janela_cad_usuario_aberta = True

			ctk.set_appearance_mode('dark')
			ctk.set_default_color_theme('dark-blue')

			cad_janela = JanelaTop('330x620', (False, False), 'Cadastro')

			frame = ctk.CTkFrame(master=cad_janela, width=310, height=600)
			frame.place(relx=0.5, rely=0.5, anchor='center')

			titulo_cad = ctk.CTkLabel(
				master=frame, text='Cadastro', font=('', 25))
			lb_nome = ctk.CTkLabel(
				frame, text_color=self.azul, text='Nome', font=('', 12))
			nome = ctk.CTkEntry(
				master=frame, placeholder_text='Nome completo', width=280, font=('', 15))
			lb_cpf = ctk.CTkLabel(
				frame, text_color=self.azul, text='CPF', font=('', 12))

			cpf = ctk.CTkEntry(
				master=frame, placeholder_text='CPF', width=280, font=('', 15))
			lb_email = ctk.CTkLabel(
				frame, text_color=self.azul, text='E-mail', font=('', 12))
			email = ctk.CTkEntry(
				master=frame, placeholder_text='E-mail', width=280, font=('', 15))
			lb_celular = ctk.CTkLabel(
				frame, text_color=self.azul, text='celular', font=('', 12))
			celular = ctk.CTkEntry(
				master=frame, placeholder_text='Celular', width=280, font=('', 15))
			lb_apelido = ctk.CTkLabel(
				frame, text_color=self.azul, text='apelido', font=('', 12))
			apelido = ctk.CTkEntry(
				master=frame, placeholder_text='Apelido *opcional', width=280, font=('', 15))
			lb_senha = ctk.CTkLabel(
				frame, text_color=self.azul, text='senha', font=('', 12))
			senha1 = ctk.CTkEntry(
				master=frame, placeholder_text='Senha', width=280, show='*', font=('', 15))
			lb_senha2 = ctk.CTkLabel(
				frame, text_color=self.azul, text='senha', font=('', 12))
			senha2 = ctk.CTkEntry(
				master=frame, placeholder_text='Confirma senha', show='*', width=280, font=('', 15))
			salvar_cad = ctk.CTkButton(master=frame, text='Salvar', font=('', 20),
									   command=salvar_usuario)

			titulo_cad.place(x=110, y=25)
			lb_nome.place(x=15, y=70)
			nome.place(x=15, y=95)
			lb_cpf.place(x=15, y=130)
			cpf.place(x=15, y=155)
			lb_email.place(x=15, y=190)
			email.place(x=15, y=215)
			lb_celular.place(x=15, y=250)
			celular.place(x=15, y=275)
			lb_apelido.place(x=15, y=310)
			apelido.place(x=15, y=335)
			lb_senha.place(x=15, y=370)
			senha1.place(x=15, y=395)
			lb_senha2.place(x=15, y=430)
			senha2.place(x=15, y=455)
			salvar_cad.place(x=90, y=520)

			def fecha_janela_cadastro():
				cad_janela.destroy()
				Cadastros.janela_cad_usuario_aberta = False

			cad_janela.protocol('WM_DELETE_WINDOW', fecha_janela_cadastro)

	def janel_cad_empresa(self):

		dados_empresa = []
		valida = Validacoes()

		def botao_salvar():
			def validar():

				if not valida.validar_alpha(razao_social) or \
						not valida.validar_alpha(nome_fantasia) or \
						not valida.validar_cnpj(cnpj) or \
						not valida.validar_insc_estadual(insc_estadual) or \
						not valida.validar_insc_municipal(insc_municipal) or \
						not valida.validar_cnae(cod_cnae) or \
						not valida.validar_campo_vazio(end_logradouro) or \
						not valida.validar_campo_vazio(end_municipio) or \
						not valida.validar_digitos(end_numero) or \
						not valida.validar_campo_vazio(end_bairro) or \
						not valida.validar_cep(end_cep) or \
						not valida.validar_alpha(end_uf):
					valida.validar_alpha(razao_social)
					valida.validar_alpha(nome_fantasia)
					valida.validar_cnpj(cnpj)
					valida.validar_insc_estadual(insc_estadual)
					valida.validar_insc_municipal(insc_municipal)
					valida.validar_cnae(cod_cnae)
					valida.validar_campo_vazio(end_logradouro)
					valida.validar_campo_vazio(end_municipio)
					valida.validar_digitos(end_numero)
					valida.validar_campo_vazio(end_bairro)
					valida.validar_cep(end_cep)
					valida.validar_alpha(end_uf)
					return False
				else:
					return True

			if validar():

				widgets = frame.winfo_children()
				for wid in widgets:
					if isinstance(wid, ctk.CTkOptionMenu):
						if wid.get() == 'Simples nacional':
							dados_empresa.append(1)
						elif wid.get() == 'Lucro presumido':
							dados_empresa.append(3)
						elif wid.get() == 'Lucro real':
							dados_empresa.append(3)
						else:
							dados_empresa.append(wid.get())
					if isinstance(wid, ctk.CTkEntry):
						if wid.get().isdigit():
							try:
								var = int(wid.get())
							except ValueError:
								print(
									'Não conseguiu converter para inteiro para inserção no banco de dados.')
							dados_empresa.append(var)
						else:
							dados_empresa.append(wid.get())

				db.inserir_dados_key_bd('empresas', [
					'razao_social',
					'nome_fantasia',
					'cnpj',
					'cod_regime_tribut',
					'insc_estadual',
					'insc_municipal',
					'cnae_fiscal',
					'end_logradouro',
					'end_numero',
					'end_bairro',
					'end_municipio',
					'end_uf',
					'end_cep',
					'funcao'
				], dados_empresa)

		if not Cadastros.janela_cad_empresa_aberta:
			Cadastros.janela_cad_empresa_aberta = True

			janela_cad_empresa = JanelaTop(
				'340x580', (False, False), 'cadastro de empresas')

			frame = ctk.CTkFrame(janela_cad_empresa)

			lb_titulo = ctk.CTkLabel(
				frame, text='Cadastro empresas', font=('', 20))
			razao_social = ctk.CTkEntry(
				frame, placeholder_text='Razão social', width=300)
			nome_fantasia = ctk.CTkEntry(
				frame, placeholder_text='Nome Fantasia')
			cnpj = ctk.CTkEntry(frame, placeholder_text='CNPJ')
			cod_regime_trib = ctk.CTkOptionMenu(
				frame, values=['Simples nacional', 'Lucro presumido', 'Lucro real'])
			insc_estadual = ctk.CTkEntry(
				frame, placeholder_text='Inscrição estadual')
			insc_municipal = ctk.CTkEntry(
				frame, placeholder_text='Inscrição municipal')
			cod_cnae = ctk.CTkEntry(frame, placeholder_text='Código CNAE')
			end_logradouro = ctk.CTkEntry(
				frame, placeholder_text='Logradouro', width=300)
			end_numero = ctk.CTkEntry(
				frame, placeholder_text='Nº', width=50)
			end_bairro = ctk.CTkEntry(
				frame, placeholder_text='Bairro', width=200)
			end_municipio = ctk.CTkEntry(
				frame, placeholder_text='Município')
			end_uf = ctk.CTkEntry(frame,
								  placeholder_text='UF', width=50)
			end_cep = ctk.CTkEntry(frame, placeholder_text='CEP')
			funcao = ctk.CTkOptionMenu(frame, values=['Padrão', 'Emitente'])
			bt_salvar = ctk.CTkButton(
				frame, text='Salvar', command=botao_salvar)

			frame.place(relx=0.5, rely=0.5, anchor='center')

			lb_titulo.grid(row=0, column=0, columnspan=2, pady=5, padx=10)
			razao_social.grid(row=1, column=0, columnspan=2,
							  pady=5, padx=10, sticky='w')
			nome_fantasia.grid(row=2, column=0, pady=5, padx=10, sticky='w')
			cnpj.grid(row=3, column=0, pady=5, padx=10, sticky='w')
			cod_regime_trib.grid(row=4, column=0, pady=5, padx=10, sticky='w')
			insc_estadual.grid(row=5, column=0, pady=5, padx=10, sticky='w')
			insc_municipal.grid(row=6, column=0, pady=5, padx=10, sticky='w')
			cod_cnae.grid(row=7, column=0, pady=5, padx=10, sticky='w')
			end_logradouro.grid(row=8, column=0, columnspan=2,
								pady=5, padx=10, sticky='w')
			end_numero.grid(row=9, column=1, pady=5, padx=10, sticky='w')
			end_bairro.grid(row=10, column=0, pady=5, padx=10, sticky='w')
			end_municipio.grid(row=9, column=0, pady=5, padx=10, sticky='w')
			end_uf.grid(row=12, column=1, pady=5, padx=10, sticky='w')
			end_cep.grid(row=12, column=0, pady=5, padx=10, sticky='w')
			funcao.grid(row=14, column=0, pady=5, padx=10, sticky='w')
			bt_salvar.grid(row=15, column=0, columnspan=2, pady=20, padx=10)

			def fechar_janela():
				janela_cad_empresa.destroy()
				Cadastros.janela_cad_empresa_aberta = False

			janela_cad_empresa.protocol('WM_DELETE_WINDOW', fechar_janela)
			janela_cad_empresa.mainloop()


class Fiscal:
	def __init__(self) -> None:
		self.azul = '#0080FF'
		self.azul_metal_claro = '#B0C4DE'
		self.azul_claro = '#ADD8E6'

	def janel_grupo_fiscal(self):
		val = Validacoes()
		lista_icms = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
		lista_cst = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '49', '50', '51', '52', '53', '54', '55',
					 '56', '60', '61', '62', '63', '64', '65', '66', '67', '70', '71', '72', '73', '74', '75', '98', '99']

		def salvar_grupo_fiscal():
			dados_grupo_fiscal = []

			def valida():
				if not val.validar_campo_vazio(et_nome_grupo) or \
						not val.validar_ncm(et_ncm) or \
						not val.validar_cfop(et_cfop) or \
						not val.validar_ean(et_ean) or \
						not val.validar_ean(et_ean_tributavel) or \
						not cb_icms_origem.get()[:1] in lista_icms or \
						not cb_pis_modalidade.get()[:2] in lista_cst or \
						not cb_confins_modalidade.get()[:2] in lista_cst:
					val.validar_campo_vazio(et_nome_grupo)
					val.validar_ncm(et_ncm)
					val.validar_cfop(et_cfop)
					val.validar_ean(et_ean)
					val.validar_ean(et_ean_tributavel)
					return False
				else:
					return True

			if valida():
				for wid in frame.winfo_children():
					if isinstance(wid, ctk.CTkEntry):
						if wid.get().isdigit():
							integer = int(wid.get())
							dados_grupo_fiscal.append(integer)
						else:
							dados_grupo_fiscal.append(wid.get())
						wid.delete(0, 'end')
					if isinstance(wid, ctk.CTkOptionMenu):
						dados_grupo_fiscal.append(wid.get())
					if isinstance(wid, ctk.CTkComboBox):
						dados_grupo_fiscal.append(wid.get())
				db.inserir_dados_key_bd('fiscal_produto', [
					'nome_grupo',
					'ncm',
					'cfop',
					'unidade_comercial',
					'ean',
					'ean_tributavel',
					'unidade_tributavel',
					'icms_modalidade',
					'icms_origem',
					'icms_cson',
					'pis_modalidade',
					'confins_modalidade'], dados_grupo_fiscal)
				lb_inf.grid(row=14)
				lb_inf.configure(
					text='Grupo cadastrado com sucesso!', text_color=self.azul)
			else:
				lb_inf.grid(row=14)
				lb_inf.configure(text='Verifique os dados!', text_color='red')

		def check_box():
			if ck_ean.get():
				et_ean.insert(0, 'SEM GTIN')
				et_ean_tributavel.insert(0, 'SEM GTIN')
				et_ean.configure(state='disabled')
				et_ean_tributavel.configure(state='disabled')
			else:
				et_ean.configure(state='normal')
				et_ean_tributavel.configure(state='normal')
				et_ean.delete(0, 'end')
				et_ean_tributavel.delete(0, 'end')
				et_ean.configure(placeholder_text='EAN')
				et_ean_tributavel.configure(placeholder_text='EAN Tributavel')

		if not Cadastros.janela_grupo_fiscal_aberta:
			Cadastros.janela_grupo_fiscal_aberta = True

			janela_grupo_fiscal = JanelaTop(
				'270x620', (False, False), 'Cadastro de grupos fiscais')

			icms_origem = [
				'0 - Nacional, exceto as indicadas nos códigos 3, 4, 5 e 8',
				'1 - Estrangeira - Importação direta, exceto a indicada no código 6',
				'2 - Estrangeira - Adquirida no mercado interno, exceto a indicada no código 7',
				'3 - Nacional, mercadoria ou bem com Conteúdo de Importação superior a 40% (quarenta por cento) e inferior ou igual a 70% ',
				'4 - Nacional, cuja produção tenha sido feita em conformidade com os processos produtivos básicos',
				'5 - Nacional, mercadoria ou bem com Conteúdo de Importação inferior ou igual a 40%',
				'6 - Estrangeira - Importação direta, sem similar nacional, constante em lista de Resolução CAMEX e gás natural',
				'7 - Estrangeira - Adquirida no mercado interno, sem similar nacional, constante em lista de Resolução CAMEX e gás natural',
				'8 - Nacional, mercadoria ou bem com Conteúdo de Importação superior a 70%']

			cst_pis_cofins = [
				'01 - Operação Tributável com Alíquota Básica',
				'02 - Operação Tributável com Alíquota Diferenciada',
				'03 - Operação Tributável com Alíquota por Unidade de Medida de Produto',
				'04 - Operação Tributável Monofásica - Revenda a Alíquota Zero',
				'05 - Operação Tributável por Substituição Tributária',
				'06 - Operação Tributável a Alíquota Zero',
				'07 - Operação Isenta da Contribuição',
				'08 - Operação sem Incidência da Contribuição',
				'09 - Operação com Suspensão da Contribuição',
				'49 - Outras Operações de Saída',
				'50 - Operação com Direito a Crédito - Vinculada Exclusivamente a Receita Tributada no Mercado Interno',
				'51 - Operação com Direito a Crédito – Vinculada Exclusivamente a Receita Não Tributada no Mercado Interno',
				'52 - Operação com Direito a Crédito - Vinculada Exclusivamente a Receita de Exportação',
				'53 - Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno',
				'54 - Operação com Direito a Crédito - Vinculada a Receitas Tributadas no Mercado Interno e de Exportação',
				'55 - Operação com Direito a Crédito - Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação',
				'56 - Operação com Direito a Crédito - Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de Exportação',
				'60 - Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Tributada no Mercado Interno',
				'61 - Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita Não-Tributada no Mercado Interno',
				'62 - Crédito Presumido - Operação de Aquisição Vinculada Exclusivamente a Receita de Exportação',
				'63 - Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno',
				'64 - Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas no Mercado Interno e de Exportação',
				'65 - Crédito Presumido - Operação de Aquisição Vinculada a Receitas Não-Tributadas no Mercado Interno e de Exportação',
				'66 - Crédito Presumido - Operação de Aquisição Vinculada a Receitas Tributadas e Não-Tributadas no Mercado Interno, e de Exportação',
				'67 - Crédito Presumido - Outras Operações',
				'70 - Operação de Aquisição sem Direito a Crédito',
				'71 - Operação de Aquisição com Isenção',
				'72 - Operação de Aquisição com Suspensão',
				'73 - Operação de Aquisição a Alíquota Zero',
				'74 - Operação de Aquisição sem Incidência da Contribuição',
				'75 - Operação de Aquisição por Substituição Tributária',
				'98 - Outras Operações de Entrada',
				'99 - Outras Operações'
			]

			frame = ctk.CTkFrame(janela_grupo_fiscal, width=250, height=530)

			lb_titulo = ctk.CTkLabel(
				frame, text='Cadastro de grupos fiscais', font=('', 20))
			et_nome_grupo = ctk.CTkEntry(
				frame, placeholder_text='Nome do grupo', width=200)
			et_ncm = ctk.CTkEntry(frame, placeholder_text='NCM')
			et_cfop = ctk.CTkEntry(frame, placeholder_text='CFOP')
			op_unid_comercial = ctk.CTkOptionMenu(
				frame, values=['UN', 'KG', 'LT'])
			ck_ean = ctk.CTkCheckBox(
				frame, text='Sem GTIN', text_color=self.azul, command=check_box)
			et_ean = ctk.CTkEntry(frame, placeholder_text='EAN')
			et_ean_tributavel = ctk.CTkEntry(
				frame, placeholder_text='EAN Tributavel')
			op_unidade_tributavel = ctk.CTkOptionMenu(
				frame, values=['UN', 'KG', 'LT'])
			op_icms_modalidade = ctk.CTkOptionMenu(
				frame, values=['102', '101', '201', '202', '203', '300', '400', '500', '900'])
			cb_icms_origem = ctk.CTkComboBox(
				frame, values=icms_origem)
			op_icms_csosn = ctk.CTkOptionMenu(
				frame, values=['102', '101', '201', '202', '203', '300', '400', '500', '900'])
			cb_pis_modalidade = ctk.CTkComboBox(
				frame, values=cst_pis_cofins)
			cb_confins_modalidade = ctk.CTkComboBox(
				frame, values=cst_pis_cofins)
			lb_inf = ctk.CTkLabel(frame, text=' ', text_color=self.azul)
			bt_salvar = ctk.CTkButton(
				frame, text='Salvar', command=salvar_grupo_fiscal)

			frame.place(relx=0.5, rely=0.5, anchor='center')

			lb_titulo.grid(row=0, padx=10, pady=5)
			et_nome_grupo.grid(row=1, sticky='w', padx=10, pady=5)
			et_ncm.grid(row=2, sticky='w', padx=10, pady=5)
			et_cfop.grid(row=3, sticky='w', padx=10, pady=5)
			op_unid_comercial.grid(row=4, sticky='w', padx=10, pady=5)
			ck_ean.grid(row=5, sticky='w', padx=10, pady=5)
			et_ean.grid(row=6, sticky='w', padx=10, pady=5)
			et_ean_tributavel.grid(row=7, sticky='w', padx=10, pady=5)
			op_unidade_tributavel.grid(row=8, sticky='w', padx=10, pady=5)
			op_icms_modalidade.grid(row=9, sticky='w', padx=10, pady=5)
			cb_icms_origem.grid(row=10, sticky='w', padx=10, pady=5)
			op_icms_csosn.grid(row=11, sticky='w', padx=10, pady=5)
			cb_pis_modalidade.grid(row=12, sticky='w', padx=10, pady=5)
			cb_confins_modalidade.grid(row=13, sticky='w', padx=10, pady=5)
			lb_inf.grid(row=14)
			bt_salvar.grid(row=15, pady=10)

			def fecha_janela():
				janela_grupo_fiscal.destroy()
				Cadastros.janela_grupo_fiscal_aberta = False

			janela_grupo_fiscal.protocol('WM_DELETE_WINDOW', fecha_janela)
			janela_grupo_fiscal.mainloop()

	def janel_config_nfe(self):

		def salvar_config_fisc():
			""" config_nfe=[]
			for wid in janela.winfo_children():
					if isinstance(wid, ctk.CTkEntry) or isinstance(wid, ctk.CTkOptionMenu):
							config_nfe.append(wid.get()) """

			db.inserir_dados_key_bd('conf_nfe', [
				'nome_config_nfe',
				'uf',
				'nat_operacao',
				'forma_pag',
				'tipo_pag',
				'modelo',
				'serie',
				'numero_nfe',
				'tipo_documento',
				'cod_municipio',
				'tipo_impressao',
				'forma_emissao',
				'cliente_final',
				'indicador_destino',
				'indicador_presencial',
				'finalidade_emissao',
				'processo_emissao',
				'transp_mod_frente',
				'inf_adic_interesse_fisco',
				'csc_prod',
				'empresa_emitente'
			], [
				nome_conf_fisc.get(),
				uf.get(),
				nat_operacao.get(),
				forma_pg.get(),
				tipo_pg.get(),
				modelo_nfe.get(),
				serie_nfe.get(),
				numero_nfe.get(),
				tipo_doc.get(),
				cod_municipio.get(),
				tipo_impressao_danfe.get(),
				form_emissao.get(),
				cliente_final.get(),
				indicador_destino.get(),
				indicador_presencial.get(),
				finalidade_emissao.get(),
				processo_emissao.get(),
				transporte_modalidade.get(),
				inf_adicionais.get(),
				csc.get(),
				empresa_emit.get()
			])

		janela = JanelaTop('470x800', (False, False), 'Configuração de NF')
		frame = ctk.CTkFrame(janela)

		lb_config_nfe = ctk.CTkLabel(
			frame, text='Configuração de NF', text_color=self.azul, font=('', 20))
		lb_nome_conf = ctk.CTkLabel(
			frame, text='Nome da configuração', text_color=self.azul)
		nome_conf_fisc = ctk.CTkEntry(
			frame, placeholder_text='Nome da configuração')
		lb_uf = ctk.CTkLabel(frame, text='UF', text_color=self.azul)
		uf = ctk.CTkOptionMenu(frame, values=['GO', 'DF', 'Ba', 'SP', 'MG'])
		lb_nat_op = ctk.CTkLabel(
			frame, text='Natureza da operação', text_color=self.azul)
		nat_operacao = ctk.CTkOptionMenu(
			frame, values=['Venda', 'Compra', 'Transferência', 'Devolução',])
		lb_form_pag = ctk.CTkLabel(
			frame, text='Forma de pagamento', text_color=self.azul)
		forma_pg = ctk.CTkOptionMenu(
			frame, values=['0-Pagamento avísta', '1-Pagamento a prazo', '2-Outros'])
		lb_tipo_pag = ctk.CTkLabel(
			frame, text='Tipo de pagamento', text_color=self.azul)
		tipo_pg = ctk.CTkOptionMenu(frame, values=['1 dinheiro', '2 cheque', '3 cartão de crédito', '4 débito', '5 crédito loja', '10 vale alimentação',
									'11 vale refeição', '12 vale presente', '13 vale combustível', '15 boleto bancário', '90 sem pagamento', '99 outros'])
		lb_mod_nfe = ctk.CTkLabel(
			frame, text='Modelo de NF', text_color=self.azul)
		modelo_nfe = ctk.CTkOptionMenu(frame, values=['65-NFC-e', '55-NF-e'])
		lb_serie_nfe = ctk.CTkLabel(
			frame, text='Serie da NF', text_color=self.azul)
		serie_nfe = ctk.CTkOptionMenu(frame, values=['1'])
		lb_num_nfe = ctk.CTkLabel(
			frame, text='Número da ultima NF emitida', text_color=self.azul)
		numero_nfe = ctk.CTkEntry(
			frame, placeholder_text='Número da ultima NF')
		lb_tipo_doc = ctk.CTkLabel(
			frame, text='Tipo de documento', text_color=self.azul)
		tipo_doc = ctk.CTkOptionMenu(frame, values=['1-Saida', '0-Entrada'])
		lb_cod_municip = ctk.CTkLabel(
			frame, text='Código IBGE do município', text_color=self.azul)
		cod_municipio = ctk.CTkEntry(
			frame, placeholder_text='Código IBGE município')
		lb_empresa_emit = ctk.CTkLabel(
			frame, text='Empresa emitente', text_color=self.azul)
		empresa_emit = ctk.CTkEntry(
			frame, placeholder_text='CNPJ empresa emitente')
		lb_tip_imp_danfe = ctk.CTkLabel(
			frame, text='Tipo de impressão DANFE', text_color=self.azul)
		tipo_impressao_danfe = ctk.CTkOptionMenu(frame, values=[
												 '4-NFC-e', '0-Sem geração de DANFE', '1-DANFE retrato', '2-DANFE Paisagem', '3-DANFE simplificado'])
		lb_form_emissao = ctk.CTkLabel(
			frame, text='Forma de emissão', text_color=self.azul)
		form_emissao = ctk.CTkOptionMenu(frame, values=['1-Emissão Normal'])
		lb_cliente_final = ctk.CTkLabel(
			frame, text='Cliente final', text_color=self.azul)
		cliente_final = ctk.CTkOptionMenu(
			frame, values=['1-Consumidor final', '0-Normal'])
		lb_ind_destino = ctk.CTkLabel(
			frame, text='Indicador de destinatário', text_color=self.azul)
		indicador_destino = ctk.CTkOptionMenu(
			frame, values=['1-Não contribuinte', '0-contribuinte', '2-insento'])
		lb_ind_presencial = ctk.CTkLabel(
			frame, text='Indicador presencial', text_color=self.azul)
		indicador_presencial = ctk.CTkEntry(
			frame, placeholder_text='1-Indicador presencial')
		lb_finalid_emissao = ctk.CTkLabel(
			frame, text='Finalidade de emissão', text_color=self.azul)
		finalidade_emissao = ctk.CTkOptionMenu(frame, values=[
											   '1-NF-e normal', '2-NF-e complementar', '3-NF-e de ajuste', '4-NF-e devolução'])
		lb_processo_emissao = ctk.CTkLabel(
			frame, text='Processo de emissão', text_color=self.azul)
		processo_emissao = ctk.CTkOptionMenu(
			frame, values=['0-Emissão com aplicativo do contribuinte'], width=100)
		processo_emissao.configure(width=100)
		lb_transp_modalid = ctk.CTkLabel(
			frame, text='Transporte modalidade frete', text_color=self.azul)
		transporte_modalidade = ctk.CTkOptionMenu(
			frame, values=['9-Sem ocorrencia de transporte'])
		lb_inf_adicionais = ctk.CTkLabel(
			frame, text='Informações adicionais', text_color=self.azul)
		inf_adicionais = ctk.CTkEntry(
			frame, placeholder_text='Informações adicionais')
		lb_csc = ctk.CTkLabel(frame, text='CSC Produção', text_color=self.azul)
		csc = ctk.CTkEntry(frame, placeholder_text='CSC')
		lb_erro = ctk.CTkLabel(frame, text='', text_color='red')
		confirm_config = ctk.CTkButton(
			frame, text='Salvar', command=salvar_config_fisc)

		frame.pack(padx=10, pady=10, fill='both', expand=True)
		lb_config_nfe.grid(row=0, column=0, columnspan=2,
						   padx=(10, 5), pady=(5, 10))
		lb_nome_conf.grid(row=1, column=0, columnspan=2,
						  padx=(10, 5), sticky='w')
		nome_conf_fisc.grid(row=2, column=0, columnspan=2,
							padx=(10, 5), pady=(0, 1), sticky='w')
		lb_uf.grid(row=3, padx=(10, 5), sticky='w')
		uf.grid(row=4, padx=(10, 5), pady=(0, 1), sticky='w')
		lb_nat_op.grid(row=5, padx=(10, 5), sticky='w')
		nat_operacao.grid(row=6, padx=(10, 5), pady=(0, 1), sticky='w')
		lb_form_pag.grid(row=7, padx=(10, 5), sticky='w')
		forma_pg.grid(row=8, padx=(10, 5), pady=(0, 1), sticky='w')
		lb_tipo_pag.grid(row=9, padx=(10, 5), sticky='w')
		tipo_pg.grid(row=10, padx=(10, 5), pady=(0, 1), sticky='w')
		lb_mod_nfe.grid(row=11, padx=(10, 5), sticky='w')
		modelo_nfe.grid(row=12, padx=(10, 5), pady=(0, 1), sticky='w')
		lb_serie_nfe.grid(row=13, padx=(10, 5), sticky='w')
		serie_nfe.grid(row=14, padx=(10, 5), pady=(0, 1), sticky='w')
		lb_num_nfe.grid(row=15, padx=(10, 5), sticky='w')
		numero_nfe.grid(row=16, padx=(10, 5), pady=(0, 1), sticky='w')
		lb_tipo_doc.grid(row=17, padx=(10, 5), sticky='w')
		tipo_doc.grid(row=18, padx=(10, 5), pady=(0, 1), sticky='w')
		lb_cod_municip.grid(row=19, padx=(10, 5), sticky='w')
		cod_municipio.grid(row=20, padx=(10, 5), pady=(0, 1), sticky='w')
		lb_empresa_emit.grid(row=21, padx=(10, 5), sticky='w')
		empresa_emit.grid(row=22, padx=(10, 5), pady=(0, 1), sticky='w')
		lb_tip_imp_danfe.grid(row=1, column=1, padx=(5, 10), sticky='w')
		tipo_impressao_danfe.grid(
			row=2, column=1, padx=(5, 10), pady=(0, 1), sticky='w')
		lb_form_emissao.grid(row=3, column=1, padx=(5, 10), sticky='w')
		form_emissao.grid(row=4, column=1, padx=(
			5, 10), pady=(0, 1), sticky='w')
		lb_cliente_final.grid(row=5, column=1, padx=(5, 10), sticky='w')
		cliente_final.grid(row=6, column=1, padx=(
			5, 10), pady=(0, 1), sticky='w')
		lb_ind_destino.grid(row=7, column=1, padx=(5, 10), sticky='w')
		indicador_destino.grid(row=8, column=1, padx=(
			5, 10), pady=(0, 1), sticky='w')
		lb_ind_presencial.grid(row=9, column=1, padx=(5, 10), sticky='w')
		indicador_presencial.grid(
			row=10, column=1, padx=(5, 10), pady=(0, 1), sticky='w')
		lb_finalid_emissao.grid(row=11, column=1, padx=(5, 10), sticky='w')
		finalidade_emissao.grid(row=12, column=1, padx=(
			5, 10), pady=(0, 1), sticky='w')
		lb_processo_emissao.grid(row=13, column=1, padx=(5, 10), sticky='w')
		processo_emissao.grid(row=14, column=1, padx=(
			5, 10), pady=(0, 1), sticky='w')
		lb_transp_modalid.grid(row=15, column=1, padx=(5, 10), sticky='w')
		transporte_modalidade.grid(
			row=16, column=1, padx=(5, 10), pady=(0, 1), sticky='w')
		lb_inf_adicionais.grid(row=17, column=1, padx=(5, 10), sticky='w')
		inf_adicionais.grid(row=18, column=1, padx=(5, 10),
							pady=(0, 1), sticky='w')
		lb_csc.grid(row=19, column=1, padx=(5, 10), pady=(0, 1), sticky='w')
		csc.grid(row=20, column=1, padx=(5, 10), pady=(0, 1), sticky='w')
		lb_erro.grid(row=23, column=1, padx=(5, 10), pady=5, sticky='w')
		confirm_config.grid(row=24, column=0, columnspan=2, padx=10, pady=10)


class Graficos:

	def gerador_cor(self):
		cor = random.randint(0, 16777215)
		return f'#{cor:06x}'

	def grafico_bar_vertival(self):
		fig, ax = plt.subplots(figsize=(20, 12))

		# dados do grafico
		# meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro']
		nomes = ['Alessandro', 'Ana', 'Danny', 'Manoela', 'Vinicios']
		counts = [40, 40, 30, 55, 70]

		bar_colors = []

		for _ in range(len(nomes)):
			bar_colors.append(self.gerador_cor())

		# montagem do grafico com labels e cores
		ax.bar(nomes, counts, color=bar_colors)

		ax.set_title('vendas')
		# salva uma figura
		plt.savefig('grafico_barv.png')

		# abrindo a imagem com ctkimage para os widgets
		grafico_barv = ctk.CTkImage(Image.open(
			'grafico_barv.png'), size=(1020, 350))

		return grafico_barv

	def grafico_bar_horizontal(self):
		np.random.seed(19680801)
		bar_labels = ['Alessandro', 'Ana', 'danny', 'manoela', 'yara']
		bar_color = ['tab:cyan', 'tab:red',
								 'tab:blue', 'tab:orange', 'tab:green']

		plt.rcdefaults()
		fig, ax = plt.subplots()

		# dados do grafico
		pessoas = ('Alessandro', 'Ana', 'Danny', 'Manoela', 'Yara')
		y_pos = np.arange(len(pessoas))
		performance = 3 + 10 * np.random.rand(len(pessoas))

		ax.barh(y_pos, performance, align='center',
				label=bar_labels, color=bar_color)
		ax.set_yticks(y_pos, labels=pessoas)
		ax.invert_yaxis()
		ax.set_xlabel('Performance')
		ax.set_title('Total geral de vendas')

		# salva a imagem do grafico
		plt.savefig('grafico_barh.png')

		grafico_barh = ctk.CTkImage(Image.open(
			'grafico_barh.png'), size=(500, 425))

		return grafico_barh

	def grafico_circulo(self):
		fig, ax = plt.subplots()

		# espessura do gráfico
		size = 0.6

		# valores atribuídos ao gráfico
		vals = np.array([[60], [37], [29], [50], [70]])

		# cores atribuídas ao gráfico e os labels
		bar_color = ['tab:cyan', 'tab:red',
					 'tab:blue', 'tab:orange', 'tab:green']
		bar_labels = ['Alessandro', 'Ana', 'danny', 'manoela', 'yara']

		# montagem do gráfico
		ax.pie(vals.sum(axis=1), radius=1, wedgeprops=dict(
			width=size, edgecolor='w'), colors=bar_color)

		# aspecto e titulo do gráfico
		ax.set(aspect="equal", title='Titulo')
		ax.legend(bar_labels, loc='upper left', bbox_to_anchor=(
			0.78, 1), bbox_transform=plt.gcf().transFigure)
		# salva figura do gráfico
		plt.savefig('grafico_pie.png')

		# converte a imagem em uma imagem ctk
		grafico_piec = ctk.CTkImage(Image.open(
			'grafico_pie.png'), size=(500, 425))

		return grafico_piec
