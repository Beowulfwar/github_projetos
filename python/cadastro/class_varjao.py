import customtkinter as ctk
from tkinter import ttk
import re
import os
from sql_varjao import BancoDados
from PIL import Image
from tkcalendar import DateEntry
from fpdf import FPDF
from fpdf.enums import XPos, YPos


db = BancoDados('varjao.db')


class Janela(ctk.CTk):
	def __init__(self, geometria='400x400', a=True, l=True, titulo='janela') -> None:
		super().__init__()
		self.title(titulo)		
		self._set_appearance_mode('dark')
		self.geometry(geometria)
		self.resizable(a, l)
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
	def __init__(self, geometry='400x400', resizable=True, title='Top Level Window'):
		super().__init__()
		self.title(title)

		self.geometry(geometry)
		self.resizable(*resizable)
		self.centralizar_janela()
		self.bring_to_front()

  
	def bring_to_front(window):
		window.lift()
		window.attributes('-topmost', True)
		#window.attributes('-topmost', False)

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

	# nome=None, cpf=None, email=None, celular=None, senha=None, apelido=None) -> None:
	def __init__(self):

		# arquivo que guarda configuração do usuário
		self.ARQUIVO_CONFIG = 'config.txt'

		# características do objeto usuário
		""" self.nome = nome
		self.cpf = cpf
		self.email = email
		self.celular = celular
		self.apelido = apelido
		self.tipo = ['usuario', 'master', 'cliente', 'vendedor']
		self.senha = senha """

		# erros personalizados
		self.email_erro = None
		self.nome_erro = None
		self.cpf_erro = None
		self.tel_erro = None
		self.apelido_erro = None
		self.senha_erro = None

	def validar_email(self, var, frame):

		# Expressão regular para verificar o formato do e-mail
		regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

		# Verifica se o e-mail corresponde à expressão regular utiliza a biblioteca re
		if not re.match(regex, var.get()):

			var.configure(border_color='red')

			if self.email_erro is None:
				self.email_erro = ctk.CTkLabel(master=frame,
											   text='Verifique email.',
											   text_color='red',
											   height=1,
											   font=('Roboto', 10))
				self.email_erro.place(x=65, y=200)
			return False
		else:
			var.configure(border_color='gray')

			if self.email_erro is not None:
				self.email_erro.place_forget()
				self.email_erro = None
			return True

	def validar_apelido(self, var, frame):

		if not var.get():

			var.configure(border_color='red')

			if self.apelido_erro is None:
				self.apelido_erro = ctk.CTkLabel(frame, text='Verifique seu Apelido.', text_color='red', height=1,
												 font=('Roboto', 10))
				self.apelido_erro.place(x=65, y=320)
			return False
		else:
			var.configure(border_color='gray')

			if self.apelido_erro is not None:
				self.apelido_erro.place_forget()
				self.apelido_erro = None
			return True

	def validar_nome(self, var, frame):

		if var.get() == '' and len(list(var.get())) < 15:

			var.configure(border_color='red')

			if self.nome_erro is None:
				self.nome_erro = ctk.CTkLabel(frame, text='Verifique seu nome.', text_color='red', height=1,
											  font=('Roboto', 10))
				self.nome_erro.place(x=65, y=80)
			return False
		else:
			var.configure(border_color='gray')

			if self.nome_erro is not None:
				self.nome_erro.place_forget()
				self.nome_erro = None
			return True

	def validar_cpf(self, var, frame):

		# remove tudo que nao for número
		cpf = re.sub(r'\D', '', var.get())

		if len(list(cpf)) != 11:

			var.configure(border_color='red')

			if self.cpf_erro is None:
				self.cpf_erro = ctk.CTkLabel(frame, text='Verifique seu CPF.', text_color='red', height=1,
											 font=('Roboto', 10))
				self.cpf_erro.place(x=65, y=140)
			return False

		else:
			var.configure(border_color='gray')

			if self.cpf_erro is not None:
				self.cpf_erro.place_forget()
				self.cpf_erro = None
			return True

	def validar_telefone(self, var, frame):

		# remove tudo que nao for número
		celular = re.sub(r'\D', '', var.get())

		if len(list(celular)) != 11:
			var.configure(border_color='red')

			if self.tel_erro is None:
				self.tel_erro = ctk.CTkLabel(frame, text='Verifique seu nº de celular.', text_color='red', height=1,
											 font=('Roboto', 10))
				self.tel_erro.place(x=65, y=260)
			return False
		else:
			var.configure(border_color='gray')

			if self.tel_erro is not None:
				self.tel_erro.place_forget()
				self.tel_erro = None
			return True

	def validar_senha(self, senha1, senha2, frame):
		if senha1.get() != senha2.get() or len(list(senha1.get())) < 6:
			senha1.configure(border_color='red')
			senha2.configure(border_color='red')
			if self.senha_erro is None:
				self.senha_erro = ctk.CTkLabel(frame, text='Verifique sua senha.', text_color='red', height=1,
											   font=('Roboto', 10))
				self.senha_erro.place(x=65, y=380)
			return False
		else:
			senha1.configure(border_color='gray')
			senha2.configure(border_color='gray')
			if self.senha_erro is not None:
				self.senha_erro.place_forget()
				self.senha_erro = None
			return True


	def validar_cnpj(self, widget ):
	 
		cnpj = re.sub(r'\D','',widget.get())
		if len(cnpj) != 14:
			widget.configure(border_color='red')
			return False
		else:
			widget.configure(border_color='gray')
			return True


	def validar_alpha(self,widget):

		if not widget.get().replace(' ', '').isalpha():
			widget.configure(border_color='red')
			return False
		else:
			widget.configure(border_color='gray')
			return True


	def validar_insc_estadual(self,widget):

		insc_estadual = re.sub(r'\D','',widget.get())
		if not insc_estadual.isdigit() and len(insc_estadual) != 9:
			widget.configure(border_color='red')
			return False
		else:
			widget.configure(border_color='gray')
			return True
	
 
	def validar_insc_municipal(self,widget):
		insc_municipal = re.sub(r'\D','',widget.get())
		if not insc_municipal.isdigit() and len(insc_municipal) != 11:
			widget.configure(border_color='red')
			return False
		else:
			widget.configure(border_color='gray')
			return True


	def validar_cnae(self,widget):
		cnae = re.sub(r'\D','',widget.get())
		if not cnae.isdigit() and len(cnae) != 7:
			widget.configure(border_color='red')
			return False
		else:
			widget.configure(border_color='gray')
			return True

	def validar_digitos(self,widget):
		var = re.sub(r'\D','',widget.get())
		if not var.isdigit():
			widget.configure(border_color='red')
			return False
		else: 
			widget.configure(border_color='gray')
			return True

	def validar_campo_vasio(self,widget):
		if not widget.get():
			widget.configure(border_color='red')
			return False
		else:
			widget.configure(border_color='gray')
			return True


	# salvar os dados do usuario caso a caixa lembrar esteja marcada.
	def salvar_dados(self, usuario, senha, lembrar):
		if lembrar:
			with open(self.ARQUIVO_CONFIG, 'w') as arquivo:
				arquivo.write(f'{usuario.get()}\n')
				arquivo.write(f'{senha.get()}\n')
			with open(self.ARQUIVO_CONFIG, 'r') as arquivo:
				print(
					f'usuario: {arquivo.readline()}senha: {arquivo.readline()}')

	# preenche automaticamente os campos usuários e senha com as informações do arquivo config
	def ler_config(self):

		if os.path.isfile(self.ARQUIVO_CONFIG):
			with open(self.ARQUIVO_CONFIG, 'r') as arquivo:
				usuario = arquivo.readline().strip()
				senha = arquivo.readline().strip()
				return usuario, senha
		return None
	


class Produtos():
	def __init__(self) -> None:
		self.cod_produto = None
		self.descricao_produto = None
		self.preco_produto = None
		self.nome_erro = None
		self.preco_erro = None

	def validar_nome_produto(self, var, frame):

		if var.get() == '':

			var.configure(border_color='red')

			if self.nome_erro is None:
				self.nome_erro = ctk.CTkLabel(frame, text='Verifique a descrição do produto', text_color='red',
											  height=1, font=('Roboto', 10))
				self.nome_erro.grid(row=1, column=1, padx=(
					0, 10), pady=(5, 0), sticky='w')

			return False
		else:
			var.configure(border_color='gray')

			if self.nome_erro is not None:
				self.nome_erro.grid_remove()
				self.nome_erro = None
			return True

	def validar_preco_produto(self, var, frame):

		if float(var.get()) <= 0 or var.get() == '':

			var.configure(border_color='red')

			if self.preco_erro is None:
				self.preco_erro = ctk.CTkLabel(frame, text='Verifique o preco do produto', text_color='red', height=1,
											   font=('Roboto', 10))
				self.preco_erro.grid(row=3, column=1, padx=(
					0, 10), pady=(5, 0), sticky='w')
			return False
		else:
			var.configure(border_color='gray')

			if self.preco_erro is not None:
				self.preco_erro.grid_remove()
				self.preco_erro = None
			return True


class Consultas():
	janela_consulta_usuario_aberta = False
	janela_consulta_vendas_aberta = False
	janela_consulta_produtos_aberta = False

	def __init__(self) -> None:
		self.azul = '#0080FF'
		self.azul_metal_claro = '#B0C4DE'
		self.azul_claro = '#ADD8E6'
  

	def janel_consulta_usuario(self):

		def preenche_treeview():
			cx.delete(*cx.get_children())
			usuario = db.consultar_tabela_bd('usuarios')
			for v, item in enumerate(usuario):
				if v % 2 == 0:
					cx.insert('', 'end', values=item, tags=('linha_impar',))
				else:
					cx.insert('', 'end', values=item)

		def consulta_treeview():
			cx.delete(*cx.get_children())
			usuario = db.consulta_dado_bd(
				et_consulta.get(), op_menu.get().lower(), 'usuarios')[1]

			for v, item in enumerate(usuario):
				if v % 2 == 0:
					cx.insert('', 'end', values=item, tags=('linha_impar',))
				else:
					cx.insert('', 'end', values=item)

		if not Consultas.janela_consulta_usuario_aberta:
			Consultas.janela_consulta_usuario_aberta = True

			janela_consulta_usuario = Janela(
				'600x350', False, False, 'Consulta usuário')

			lb_consulta = ctk.CTkLabel(
				janela_consulta_usuario, text='Consulta usuário', font=('Roboto', 20))
			lb_consulta.grid(row=0, column=0, columnspan=3, pady=(10, 20))

			op_menu = ctk.CTkOptionMenu(janela_consulta_usuario, values=[
				'Nome', 'CPF', 'Email', 'Celular', 'Apelido'])
			op_menu.grid(row=1, column=0, padx=10)

			et_consulta = ctk.CTkEntry(
				janela_consulta_usuario, placeholder_text='<<< Informe o campo')
			et_consulta.grid(row=1, column=1, padx=10)

			bt_consulta = ctk.CTkButton(
				janela_consulta_usuario, text='Consulta', command=consulta_treeview)
			bt_consulta.grid(row=1, column=2, padx=10)

			cx = ttk.Treeview(janela_consulta_usuario, columns=(
				'Id', 'Nome', 'CPF', 'E-mail', 'Telefone', 'Apelido'), show='headings')

			cx.tag_configure('linha_impar', background=self.azul_claro)

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

			cx.grid(row=2, column=0, columnspan=4, pady=10, padx=20)

			def fecha_janela():
				Consultas.janela_consulta_usuario_aberta = False
				janela_consulta_usuario.destroy()

			janela_consulta_usuario.protocol('WM_DELETE_WINDOW', fecha_janela)
			janela_consulta_usuario.mainloop()
   

	def janel_consulta_vendas(self):

		if not Consultas.janela_consulta_vendas_aberta:
			Consultas.janela_consulta_vendas_aberta = True

			janela_consulta_vendas = JanelaTop('600x350',(False,False),'Consulta vendas')
			""" janela_consulta_vendas.title('Consulta vendas')
			janela_consulta_vendas.geometry('600x350')
			janela_consulta_vendas.resizable(False, False) """

			def preenche_treeview():
				cx.delete(*cx.get_children())
				usuario = self.conteudo_tabela_bd('vendas', 'data')
				for v in usuario:
					cx.insert('', 'end', values=v)

			def consulta_treeview():

				cx.delete(*cx.get_children())
				usuario = self.consulta_ordenada(
					et_consulta.get(), op_menu.get().lower(), 'vendas')
				for v in usuario:
					cx.insert('', 'end', values=v)

			lb_consulta = ctk.CTkLabel(
				janela_consulta_vendas, text='Consulta vendas', font=('Roboto', 20))
			lb_consulta.grid(row=0, column=0, columnspan=3, pady=20)

			op_menu = ctk.CTkOptionMenu(janela_consulta_vendas, values=[
				'Nome', 'CPF', 'Email', 'Celular', 'Apelido'])
			op_menu.grid(row=1, column=0, padx=10)

			et_consulta = ctk.CTkEntry(
				janela_consulta_vendas, placeholder_text='<<< Informe o campo')
			et_consulta.grid(row=1, column=1, padx=10)

			bt_consulta = ctk.CTkButton(
				janela_consulta_vendas, text='Consulta', command=consulta_treeview)
			bt_consulta.grid(row=1, column=2, padx=10)

			cx = ttk.Treeview(janela_consulta_vendas, columns=(
				'Id', 'Nome', 'CPF', 'E-mail', 'Telefone', 'Apelido'), show='headings')

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

					if v % 2 == 0:
						cx.insert('', 'end', values=item,
								  tags=('linha_impar',))
					else:
						cx.insert('', 'end', values=item)

			def consulta_treeview():
				produto = ''
				if op_menu.get() == 'Id' and et_consulta.get().isdigit():
					opcao = 'id_produto'
					produto = db.consulta_dado_bd(
						et_consulta.get(), opcao, 'produtos')[1]
				elif op_menu.get() == 'Descrição':
					opcao = 'prod_descricao'
					produto = db.consulta_dado_bd(
						et_consulta.get(), opcao, 'produtos')[1]

				cx.delete(*cx.get_children())

				for v, item in enumerate(produto):

					if v % 2 == 0:
						cx.insert('', 'end', values=item,
								  tags=('linha_impar',))
					else:
						cx.insert('', 'end', values=item)

			lb_consulta = ctk.CTkLabel(
				janela_consulta_produtos, text='Consulta produtos', font=('Roboto', 20))
			lb_consulta.grid(row=0, column=0, columnspan=3, pady=(10, 20))

			op_menu = ctk.CTkOptionMenu(janela_consulta_produtos, width=110, values=[
				'Id', 'Descrição'])
			op_menu.grid(row=1, column=0, padx=10)

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

			cx.tag_configure('linha_impar', background=self.azul_claro)

			cx.column('Id', minwidth=0, width=30)
			cx.column('Descrição', minwidth=0, width=150)
			cx.column('Preço', minwidth=0, width=100)
			cx.column('Grupo', minwidth=0, width=100)

			cx.heading('Id', text='Id')
			cx.heading('Descrição', text='Descrição')
			cx.heading('Preço', text='Preço')
			cx.heading('Grupo', text='Grupo')

			preenche_treeview()

			cx.grid(row=2, column=0, columnspan=3, pady=10, padx=20)

			et_consulta = ctk.CTkEntry(
				janela_consulta_produtos, placeholder_text='<<< Informe o campo')
			et_consulta.grid(row=1, column=1, padx=10)
			et_consulta.bind('<Return>', lambda e: consulta_treeview())

			bt_consulta = ctk.CTkButton(
				janela_consulta_produtos, text='Consulta', width=110, command=consulta_treeview)
			bt_consulta.grid(row=1, column=2, padx=10)

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

	def __init__(self) -> None:
		super().__init__()
		self.lb_troco_valor = None
		self.cont = 0

	# busca o produto no banco de dados para incluir na venda

	def adicionar_linha_produto(self):

		img_excluir = ctk.CTkImage(Image.open('img\\excluir_vermelho (2).png'))
		linha_produtos = []

		if self.et_cod_produto.get().isdigit():
			Vendas.produto = db.consulta_dado_bd(
				self.et_cod_produto.get(), 'id_produto', 'produtos')

		elif self.et_cod_produto.get().replace(' ', '').isalpha():
			Vendas.produto = db.consulta_dado_bd(
				self.et_cod_produto.get(), 'prod_descricao', 'produtos')[1]
		else:
			print('Produto nao cadastrado!')
		print(Vendas.produto)
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
			for lb in linha_produtos:
				lb.destroy()
				cont += 1
			# quando exclui atualiza a lista de widgets e e refaz a soma
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
				valor_m = Vendas.widgets[v-1].cget('text')*int(wid.get())
				Vendas.widgets[v+1].configure(text=valor_m)

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
		lista_venda = []
		self.var, self.var2, self.var3 = 0, 0, 0
		self.valor = 0

		def lista_de_compras():
			for wid in Vendas.widgets:
				if isinstance(wid, ctk.CTkLabel) and wid.cget('text'):
					lista_venda.append(wid.cget('text'))
				if isinstance(wid, ctk.CTkEntry):
					if wid.get():
						lista_venda.append(wid.get())
					else:
						lista_venda.append(1)
				lista_venda.append(Vendas.produto)

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
				self.janela_vendas, text='Registrar venda', font=('', 15))
			bt_emitir_nf = ctk.CTkButton(
				self.janela_vendas, text='Emitir NF', font=('', 15))
			bt_inf_cpf = ctk.CTkButton(
				self.janela_vendas, text='Informe CPF', font=('', 15))

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
			bt_inf_cpf.grid(row=8, column=2, padx=10, pady=5, sticky='w')
   
		def fecha_janela():
			Vendas.janela_vendas_aberta =False
			self.janela_vendas.destroy()
   
		self.janela_vendas.protocol('WM_DELETE_WINDOW',fecha_janela)






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
			Vendas.janela_inf_vendas_aberta =True

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

	def __init__(self) -> None:
		self.azul = '#0080FF'
		self.azul_metal_claro = '#B0C4DE'
		self.azul_claro = '#ADD8E6'
		

	def janel_cad_produto(self):

		def salvar_prod():
			if p.validar_nome_produto(descricao_produto, frame) and p.validar_preco_produto(preco_produto, frame):
				db.inserir_dados_key_bd('produtos', ('prod_descricao', 'prod_preco', 'prod_grupo'), (
					descricao_produto.get(), float(preco_produto.get()), grupo_produto.get()))
				lb_erro = ctk.CTkLabel(frame, text='Produto cadastrado com sucesso!', text_color='#0080FF',
									   font=('Roboto', 10))
				lb_erro.grid(row=5, column=0, columnspan=2,
							 padx=10, pady=(5, 0))
				descricao_produto.delete(0, ctk.END)
				preco_produto.delete(0, ctk.END)
				descricao_produto.focus_set()

		def converte_preco(prod_preco):
			try:
				preco = float(prod_preco.get().replace(',', '.'))
				if isinstance(preco, float):
					prod_preco.configure(border_color='gray')
					prod_preco.delete(0, 'end')
					preco = f'{preco:.2f}'
					prod_preco.insert(0, preco)
				else:
					prod_preco.configure(border_color='red')
			except ValueError:
				prod_preco.configure(border_color='red')

		def lista_grupo_produto():
			lista_grupo = []
			lista = db.consultar_tabela_bd('fiscal_produto')
			for g in lista:
				print(g[0])
				lista_grupo.append(g[0])
			return lista_grupo

		p = Produtos()
		if not Cadastros.janela_cad_produto_aberta:
			Cadastros.janela_cad_produto_aberta = True

			janela_cad_produto = JanelaTop(
				'300x300', (False, False), 'Cadastro de produtos')

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
			grupo_produto = ctk.CTkComboBox(
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
				row=5, column=0, padx=10, pady=(5, 0), sticky='w')
			grupo_produto.grid(
				row=6, column=0, columnspan=2, padx=10, pady=(0, 5))
			bt_salvar.grid(
				row=7, column=0, columnspan=2, padx=10, pady=15, sticky='ns')

			def fechar_janela():
				janela_cad_produto.destroy()
				Cadastros.janela_cad_produto_aberta = False

			janela_cad_produto.protocol('WM_DELETE_WINDOW', fechar_janela)
			janela_cad_produto.mainloop()

	def janel_cad_usuario(self):

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
									   command=lambda: salvar_usuario())


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

			usuario = Validacoes()

			# verifica os dados do usuario no cadastro e salva no banco de dados
			def salvar_usuario():
				def valida():
					if not usuario.validar_nome(nome, frame):
						return False
					elif  not usuario.validar_cpf(cpf, frame):
						return False
					elif not usuario.validar_email(email, frame):
						return False
					elif not usuario.validar_telefone(celular, frame):
						return False
					elif  not usuario.validar_senha(senha1, senha2, frame):
						return False
					else:
						return True

				if valida():
				
					db.inserir_dados_key_bd('usuarios', ('nome', 'cpf', 'email', 'celular', 'apelido', 'senha'),
											[nome.get(), cpf.get(), email.get(), celular.get(), apelido.get(), senha1.get()])
					cad_janela.after(400, cad_janela.destroy)
					Cadastros.janela_cad_usuario_aberta = False

			

			def fecha_janela_cadastro():
				cad_janela.destroy()
				Cadastros.janela_cad_usuario_aberta = False

			cad_janela.protocol('WM_DELETE_WINDOW', fecha_janela_cadastro)

	def janel_cad_empresa(self):

		dados_empresa = []
		valida = Validacoes()
		def botao_salvar():
			def validar():
				
				if not valida.validar_alpha(razao_social):				
					return False
				elif not valida.validar_alpha(nome_fantasia):			
					return False
				elif not valida.validar_cnpj(cnpj):			
					return False
				elif not valida.validar_insc_estadual(insc_estadual):		
					return False
				elif not valida.validar_insc_municipal(insc_munipal):			
					return False
				elif not valida.validar_cnae(cod_cnae):			
					return False
				elif not valida.validar_campo_vasio(end_logradouro):			
					return False
				elif not valida.validar_campo_vasio(end_municipio):				
					return False
				elif not valida.validar_digitos(end_numero):		
					return False
				elif not valida.validar_campo_vasio(end_bairro):				
					return False
				elif not valida.validar_digitos(end_cep):				
					return False
				elif not valida.validar_alpha(end_uf):				
					return False
				elif not valida.validar_campo_vasio(end_pais):				
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
	   						
					if isinstance(wid, ctk.CTkEntry):						
							if wid.get().isdigit():
								try:
									var = int(wid.get())
								except ValueError:
									print('Não conseguiu converter para inteiro para inserção no banco de dados.')
								dados_empresa.append(var)
							else:
								dados_empresa.append(wid.get())

				db.inserir_dados_bd('empresas', dados_empresa)
				

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
			""" op_menu = ctk.CTkOptionMenu(janela_consulta_usuario, values=[
				'Nome', 'CPF', 'Email', 'Celular', 'Apelido']) """
			cod_regime_trib = ctk.CTkOptionMenu(
				frame, values=['Simples nacional', 'Lucro presumido', 'Lucro real'])
			insc_estadual = ctk.CTkEntry(
				frame, placeholder_text='Inscrição estadual')
			insc_munipal = ctk.CTkEntry(
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
			end_pais = ctk.CTkEntry(frame, placeholder_text='Pais')
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
			insc_munipal.grid(row=6, column=0, pady=5, padx=10, sticky='w')
			cod_cnae.grid(row=7, column=0, pady=5, padx=10, sticky='w')
			end_logradouro.grid(row=8, column=0, columnspan=2,
								pady=5, padx=10, sticky='w')
			end_numero.grid(row=9, column=1, pady=5, padx=10, sticky='w')
			end_bairro.grid(row=10, column=0, pady=5, padx=10, sticky='w')
			end_municipio.grid(row=9, column=0, pady=5, padx=10, sticky='w')
			end_uf.grid(row=12, column=1, pady=5, padx=10, sticky='w')
			end_cep.grid(row=12, column=0, pady=5, padx=10, sticky='w')
			end_pais.grid(row=14, column=0, pady=5, padx=10, sticky='w')
			bt_salvar.grid(row=15, column=0, columnspan=2, pady=20, padx=10)

			def fechar_janela():
				janela_cad_empresa.destroy()
				Cadastros.janela_cad_empresa_aberta = False

			janela_cad_empresa.protocol('WM_DELETE_WINDOW', fechar_janela)
			janela_cad_empresa.mainloop()

	def janel_grupo_fiscal(self):

		def salvar_grupo_fiscal():
			dados_grupo_fiscal = []
			for wid in frame.winfo_children():
				if isinstance(wid, ctk.CTkEntry):
					if wid.get().isdigit():
						integer = int(wid.get())
						dados_grupo_fiscal.append(integer)
					else:
						dados_grupo_fiscal.append(wid.get())

			db.inserir_dados_bd('fiscal_produto', dados_grupo_fiscal)

		if not Cadastros.janela_grupo_fiscal_aberta:
			Cadastros.janela_grupo_fiscal_aberta = True

			janela_grupo_fiscal = JanelaTop(
				'270x550', (False, False), 'Cadastro de grupos fiscais')
			""" janela_grupo_fiscal.geometry('270x550')
			janela_grupo_fiscal.resizable(False, False) """

			frame = ctk.CTkFrame(janela_grupo_fiscal, width=250, height=530)

			lb_titulo = ctk.CTkLabel(
				frame, text='Cadastro de grupos fiscais', font=('', 20))
			et_nome_grupo = ctk.CTkEntry(
				frame, placeholder_text='Nome do grupo', width=200)
			et_ncm = ctk.CTkEntry(frame, placeholder_text='NCM')
			et_cfop = ctk.CTkEntry(frame, placeholder_text='CFOP')
			et_unid_comercial = ctk.CTkEntry(
				frame, placeholder_text='Unidade comercial')
			et_ean = ctk.CTkEntry(frame, placeholder_text='EAN')
			et_ean_tributavel = ctk.CTkEntry(
				frame, placeholder_text='EAN tributavel')
			et_unidade_tributavel = ctk.CTkEntry(
				frame, placeholder_text='Unidade tributavel')
			et_icms_modalidade = ctk.CTkEntry(
				frame, placeholder_text='ICMS modalidade')
			et_icms_origem = ctk.CTkEntry(
				frame, placeholder_text='ICMS origem')
			et_icms_csosn = ctk.CTkEntry(frame, placeholder_text='ICMS CSOSN')
			et_pis_modalidade = ctk.CTkEntry(
				frame, placeholder_text='PIS modalidade')
			et_confins_modalidade = ctk.CTkEntry(
				frame, placeholder_text='Confins modalidade')
			bt_salvar = ctk.CTkButton(
				frame, text='Salvar', command=salvar_grupo_fiscal)

			frame.place(relx=0.5, rely=0.5, anchor='center')

			lb_titulo.grid(row=0, padx=10, pady=5)
			et_nome_grupo.grid(row=1, sticky='w', padx=10, pady=5)
			et_ncm.grid(row=2, sticky='w', padx=10, pady=5)
			et_cfop.grid(row=3, sticky='w', padx=10, pady=5)
			et_unid_comercial.grid(row=4, sticky='w', padx=10, pady=5)
			et_ean.grid(row=5, sticky='w', padx=10, pady=5)
			et_ean_tributavel.grid(row=6, sticky='w', padx=10, pady=5)
			et_unidade_tributavel.grid(row=8, sticky='w', padx=10, pady=5)
			et_icms_modalidade.grid(row=9, sticky='w', padx=10, pady=5)
			et_icms_origem.grid(row=10, sticky='w', padx=10, pady=5)
			et_icms_csosn.grid(row=11, sticky='w', padx=10, pady=5)
			et_pis_modalidade.grid(row=12, sticky='w', padx=10, pady=5)
			et_confins_modalidade.grid(row=13, sticky='w', padx=10, pady=5)
			bt_salvar.grid(row=14, pady=10)

			def fecha_janela():
				janela_grupo_fiscal.destroy()
				Cadastros.janela_grupo_fiscal_aberta = False

			janela_grupo_fiscal.protocol('WM_DELETE_WINDOW', fecha_janela)
			janela_grupo_fiscal.mainloop()


class Fiscal:
    
    
	def janel_config_nf(self):
     
		janela = JanelaTop('300x900',(False,False),'Configuração de NF')
  
		lb_config_nf = ctk.CTkLabel(janela,text='Configuração de NF', font=('', 15))
		uf = ctk.CTkOptionMenu(janela, values=['GO','DF','Ba','SP','MG'])
		nat_operacao = ctk.CTkOptionMenu(janela, values=['Venda','Compra','Transferência','Devolução',])
		forma_pg = ctk.CTkOptionMenu(janela,values=['Cartão à vista', 'Cartão parcelado', 'Cartão débito' ,'Pix','Dinheiro'])
		tipo_pg = ctk.CTkOptionMenu(janela, values=['Á vista', 'Á prazo', 'Parcelado'])
		modelo_nf = ctk.CTkOptionMenu(janela, values=['NFC-e', 'NF-e'])
		serie_nf = ctk.CTkOptionMenu(janela, values=['1'])
		numero_NF = ctk.CTkEntry(janela, placeholder_text='Ultimo numero de NF emitida')
		tipo_doc = ctk.CTkOptionMenu(janela, values=['Entrada', 'Saida'])
		cod_municipio = ctk.CTkEntry(janela, placeholder_text='Código do município')
		tipo_impressao_danfe = ctk.CTkOptionMenu(janela, values=['NFC-e','Sem geração de DANFE', 'DANFE', 'DANFE Paisagem','DANFE simplificado'])
		form_emissao = ctk.CTkOptionMenu(janela, values=['Normal'])
		cliente_final = ctk.CTkOptionMenu(janela, values=['Consumidor final', 'Normal'])
		indicador_destino = ctk.CTkEntry(janela, placeholder_text='indicador de destino')
		indicador_presencial = ctk.CTkEntry(janela, placeholder_text='Indicador presencial')
		finalidade_emissao = ctk.CTkOptionMenu(janela, values=['NF-e normal', 'NF-e complementar', 'NF-e de ajuste', 'NF-e devolução'])
		processo_emissao = ctk.CTkOptionMenu(janela, values=['Emissão com aplicativo do contribuinte'])
		transporte_modalidade = ctk.CTkOptionMenu(janela, values=['Sem ocorrencia de transporte'])
		inf_adicionais = ctk.CTkOptionMenu(janela, values=['Varjão Variedades'])
		tributos_aproximado = ctk.CTkEntry(janela, placeholder_text='Tributos aproximados')
		confirm_config = ctk.CTkButton(janela, text='OK')
  
		lb_config_nf.grid(row=0, padx=10, pady=(5,10))
		uf.grid(row=1, padx=10, pady=5, sticky='w')
		nat_operacao.grid(row=2, padx=10, pady=5, sticky='w')
		forma_pg.grid(row=3, padx=10, pady=5, sticky='w')
		tipo_pg.grid(row=4, padx=10, pady=5, sticky='w')
		modelo_nf.grid(row=5, padx=10, pady=5, sticky='w')
		serie_nf.grid(row=6, padx=10, pady=5, sticky='w')
		numero_NF.grid(row=7, padx=10, pady=5, sticky='w')
		tipo_doc.grid(row=8, padx=10, pady=5, sticky='w')
		cod_municipio.grid(row=9, padx=10, pady=5, sticky='w')
		tipo_impressao_danfe.grid(row=10, padx=10, pady=5, sticky='w')
		form_emissao.grid(row=11, padx=10, pady=5, sticky='w')
		cliente_final.grid(row=12, padx=10, pady=5, sticky='w')
		indicador_destino.grid(row=13, padx=10, pady=5, sticky='w')
		indicador_presencial.grid(row=14, padx=10, pady=5, sticky='w')
		finalidade_emissao.grid(row=15, padx=10, pady=5, sticky='w')
		processo_emissao.grid(row=16, padx=10, pady=5, sticky='w')
		transporte_modalidade.grid(row=17, padx=10, pady=5, sticky='w')
		inf_adicionais.grid(row=18, padx=10, pady=5, sticky='w')
		tributos_aproximado.grid(row=19, padx=10, pady=5, sticky='w')
		confirm_config.grid(row=20, padx=10, pady=10)
  
  

  
class graficos:
	def grafico_bar_vertival():
		fig, ax = plt.subplots()

		# dados do grafico
		nomes = ['Alessandro', 'Ana', 'danny', 'manoela', 'yara']
		counts = [40, 40, 30, 55, 70]

		# cores das barras do grafico
		bar_labels = ['red', 'blue', '_red', 'orange', 'cyan']
		bar_colors = ['tab:cyan', 'tab:red',
					  'tab:blue', 'tab:orange', 'tab:green']

		# montagem do grafico com labels e cores
		ax.bar(nomes, counts, label=bar_labels, color=bar_colors)

		ax.set_title('vendas')

		# salva uma figura
		plt.savefig('grafico_barv.png')

		# abrindo a imagem com ctkimage para os widgets
		grafico_barv = ctk.CTkImage(Image.open(
			'grafico_barv.png'), size=(200, 150))

		return grafico_barv

	def grafico_bar_horizontal():
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
			'grafico_barh.png'), size=(200, 150))

		return grafico_barh


