from PIL import Image, ImageTk
import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
import class_varjao as cv
import sql_varjao as s
import importlib
import numpy as np
import os
import re
from customtkinter import CTkImage
importlib.reload(cv)
importlib.reload(s)

# chama as classes utilizadas
p = cv.Produtos()
b = s.Db()


class Usuario():

    def __init__(self, nome=None, cpf=None, email=None, celular=None, senha=None, apelido=None) -> None:
        super().__init__()
        self.img = None

        # arquivo que guarda configuração do usuário
        self.ARQUIVO_CONFIG = 'config.txt'

        # características do objeto usuário
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.celular = celular
        self.apelido = apelido
        self.tipo = ['usuario', 'master']
        self.senha = senha

        # erros personalizados
        self.email_erro = None
        self.nome_erro = None
        self.cpf_erro = None
        self.cel_erro = None
        self.apelido_erro = None
        self.senha_erro = None


    def validar_email(self, var, frame):

        # Expressão regular para verificar o formato do e-mail
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        # Verifica se o e-mail corresponde à expressão regular utiliza a biblioteca re
        if not re.match(regex, var.get()):

            var.configure(border_color='red')

            if self.email_erro is None:
                self.email_erro = ctk.CTkLabel(master=frame, text='Verifique email.', text_color='red', height=1,
                                               font=('Roboto', 10))
                self.email_erro.place(x=65, y=200)

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


    def validar_celular(self, var, frame):

        # remove tudo que nao for número
        celular = re.sub(r'\D', '', var.get())

        if len(list(celular)) != 11:
            var.configure(border_color='red')

            if self.cel_erro is None:
                self.cel_erro = ctk.CTkLabel(frame, text='Verifique seu nº de celular.', text_color='red', height=1,
                                             font=('Roboto', 10))
                self.cel_erro.place(x=65, y=260)
            return False
        else:
            var.configure(border_color='gray')

            if self.cel_erro is not None:
                self.cel_erro.place_forget()
                self.cel_erro = None
            return True


    def validar_senha(self, senha1, senha2, frame):

        if senha1.get() != senha2.get() or len(list(senha1.get())) < 6:

            senha1.configure(border_color='red')
            senha2.configure(border_color='red')

            if self.senha_erro is None:
                self.senha_erro = ctk.CTkLabel(frame, text='Verifique sua senha.', text_color='red', height=1,
                                               font=('Roboto', 10))
                self.senha_erro.place(x=65, y=380)
        else:
            senha1.configure(border_color='gray')
            senha2.configure(border_color='gray')

            if self.senha_erro is not None:
                self.senha_erro.place_forget()
                self.senha_erro = None
            return True


    #salvar os dados do usuario caso a caixa lembrar esteja marcada.
    def salvar_dados(self, usuario, senha, lembrar):
        if lembrar:
            with open(self.ARQUIVO_CONFIG, 'w') as arquivo:
                arquivo.write(f'{usuario.get()}\n')
                arquivo.write(f'{senha.get()}\n')
            with open(self.ARQUIVO_CONFIG, 'r') as arquivo:
                print(f'usuario: {arquivo.readline()}senha: {arquivo.readline()}')

    #preenche automaticamente os campos usuários e senha com as informações do arquivo config
    def ler_config(self):

        if os.path.isfile(self.ARQUIVO_CONFIG):
            with open(self.ARQUIVO_CONFIG, 'r') as arquivo:
                usuario = arquivo.readline().strip()
                senha = arquivo.readline().strip()
                return usuario, senha
        return None


u = Usuario()

#guarda o status de uma janela
janela_aberta = False

#aparência das janelas
ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')


def centralizar_janela(janela):
    largura_janela = janela.winfo_width()
    altura_janela = janela.winfo_height()

    largura_tela = janela.winfo_screenwidth()
    altura_tela = janela.winfo_screenheight()

    posicao_x = (largura_tela - largura_janela) // 2
    posicao_y = (altura_tela - altura_janela) // 2

    janela.geometry(f"{largura_janela}x{altura_janela}+{posicao_x}+{posicao_y}")


def grafico_bar_vertival():

	fig, ax = plt.subplots()

	#dados do grafico
	nomes = ['Alessandro', 'Ana', 'danny', 'manoela', 'yara']
	counts = [40, 40, 30, 55,70]

	#cores das barras do grafico
	bar_labels = ['red', 'blue', '_red', 'orange', 'cyan']
	bar_colors = ['tab:cyan', 'tab:red', 'tab:blue', 'tab:orange', 'tab:green']

	#montagem do grafico com labels e cores
	ax.bar(nomes, counts, label=bar_labels, color=bar_colors)

	ax.set_title('vendas')

	#salva uma figura
	plt.savefig('grafico_barv.png')

	#abrindo a imagem com ctkimage para os widgets
	grafico_barv =ctk.CTkImage(Image.open('grafico_barv.png'), size=(200, 150))

	return grafico_barv


def grafico_bar_horizontal():
	
	np.random.seed(19680801)
	bar_labels= ['Alessandro', 'Ana', 'danny', 'manoela', 'yara']
	bar_color= ['tab:cyan', 'tab:red', 'tab:blue', 'tab:orange', 'tab:green']

	plt.rcdefaults()
	fig, ax = plt.subplots()
 
	#dados do grafico
	pessoas = ('Alessandro', 'Ana', 'Danny', 'Manoela', 'Yara')
	y_pos = np.arange(len(pessoas))
	performance = 3+10 * np.random.rand(len(pessoas))
	
	ax.barh(y_pos, performance, align='center', label=bar_labels, color=bar_color)
	ax.set_yticks(y_pos, labels=pessoas)
	ax.invert_yaxis()
	ax.set_xlabel('Performance')
	ax.set_title('Total geral de vendas')
 
	#salva a imagem do grafico
	plt.savefig('grafico_barh.png')
	
	grafico_barh = ctk.CTkImage(Image.open('grafico_barh.png'), size=(200, 150))
 
	return grafico_barh


def grafico_circulo():
    
	fig, ax = plt.subplots()
 
	#espessura do gráfico
	size = 0.6
 
	#valores atribuídos ao gráfico
	vals = np.array([[60], [37], [29], [50], [70]])
 
	#cores atribuidas ao grafico e os labels
	bar_color= ['tab:cyan', 'tab:red', 'tab:blue', 'tab:orange', 'tab:green']
	bar_labels= ['Alessandro', 'Ana', 'danny', 'manoela', 'yara']
 
	#montagem do grafico
	ax.pie(vals.sum(axis=1), radius=1, wedgeprops=dict(width=size, edgecolor='w'), colors= bar_color)

	#aspecto e titulo do grafico
	ax.set(aspect="equal", title='Titulo')
	ax.legend(bar_labels, loc='upper left',bbox_to_anchor=(0.78, 1), bbox_transform=plt.gcf().transFigure)
	#salva figura do grafico
	plt.savefig('grafico_pie.png')
 
	#converte a imagem em uma imagem ctk
	grafico_piec = ctk.CTkImage(Image.open('grafico_pie.png'), size=(200, 150))

	return grafico_piec



def deletar_img_grafico():
    arquivo1 = 'grafico_barh.png'
    arquivo2 = 'grafico_barv.png'
    arquivo3 = 'grafico_pie.png'
    os.remove(arquivo1,arquivo2,arquivo3)


########################################################################################
#############################JANELA DE CADASTRO DE USUÁRIOS#############################
########################################################################################

def cadastro():
    
	global janela_aberta
 
	if not janela_aberta:
     
		janela_aberta = True

		ctk.set_appearance_mode('dark')
		ctk.set_default_color_theme('dark-blue')

		cad_janela = ctk.CTk()
		cad_janela.geometry('330x620')
		cad_janela.title('Cadastro')
		cad_janela.resizable(False, False)

		frame = ctk.CTkFrame(master=cad_janela, width=310, height=600)
		frame.place(relx=0.5, rely=0.5, anchor='center')

		titulo_cad = ctk.CTkLabel(master=frame, text='Cadastro', font=('Roboto', 25))
		titulo_cad.place(x=110, y=25)

		lb_nome = ctk.CTkLabel(frame, text_color='#0080FF', text='Nome', font=('Roboto', 12))
		lb_nome.place(x=15, y=70)

		nome = ctk.CTkEntry(master=frame, placeholder_text='Nome completo', width=280, font=('Roboto', 15))
		nome.place(x=15, y=95)

		lb_cpf = ctk.CTkLabel(frame, text_color='#0080FF', text='CPF', font=('Roboto', 12))
		lb_cpf.place(x=15, y=130)

		cpf = ctk.CTkEntry(master=frame, placeholder_text='CPF', width=280, font=('Roboto', 15))
		cpf.place(x=15, y=155)

		lb_email = ctk.CTkLabel(frame, text_color='#0080FF', text='E-mail', font=('Roboto', 12))
		lb_email.place(x=15, y=190)

		email = ctk.CTkEntry(master=frame, placeholder_text='E-mail', width=280, font=('Roboto', 15))
		email.place(x=15, y=215)

		lb_celular = ctk.CTkLabel(frame, text_color='#0080FF', text='celular', font=('Roboto', 12))
		lb_celular.place(x=15, y=250)

		celular = ctk.CTkEntry(master=frame, placeholder_text='Celular', width=280, font=('Roboto', 15))
		celular.place(x=15, y=275)

		lb_apelido = ctk.CTkLabel(frame, text_color='#0080FF', text='apelido', font=('Roboto', 12))
		lb_apelido.place(x=15, y=310)

		apelido = ctk.CTkEntry(master=frame, placeholder_text='Apelido *opcional', width=280,
									font=('Roboto', 15))
		apelido.place(x=15, y=335)

		lb_senha = ctk.CTkLabel(frame, text_color='#0080FF', text='senha', font=('Roboto', 12))
		lb_senha.place(x=15, y=370)

		senha1 = ctk.CTkEntry(master=frame, placeholder_text='Senha', width=280, show='*', font=('Roboto', 15))
		senha1.place(x=15, y=395)

		lb_senha2 = ctk.CTkLabel(frame, text_color='#0080FF', text='senha', font=('Roboto', 12))
		lb_senha2.place(x=15, y=430)

		senha2 = ctk.CTkEntry(master=frame, placeholder_text='Confirma senha', show='*', width=280,
								font=('Roboto', 15))
		senha2.place(x=15, y=455)

		# Verifica os dados assim que o usuário retira o foco do mouse
		""" email.bind('<FocusOut>', lambda event: usuario.validar_email(email, frame))
		nome.bind('<FocusOut>', lambda event: usuario.confere(nome, frame))
		cpf.bind('<FocusOut>', lambda event: usuario.validar_cpf(cpf, frame))
		celular.bind('<FocusOut>', lambda event: usuario.validar_celular(celular, frame))
		apelido.bind('<FocusOut>', lambda event: usuario.confere(apelido, frame))
		senha.bind('<FocusOut>', lambda event: usuario.validar_senha(senha, senha2, frame))
		senha2.bind('<FocusOut>', lambda event: usuario.validar_senha(senha, senha2, frame)) """

		usuario = Usuario(nome.get(), cpf.get(), email.get(), celular.get(), senha1.get(), apelido.get())
		#verifica os dados do usuario no cadastro e salva no banco de dados
		def salvar_usuario():
			a = 0
			# as condições a seguir verificam erros nos campos obrigatórios. Caso haja nao executam a função cadastrar_usuarios()
			if usuario.validar_nome(nome, frame):
				a += 1
			if usuario.validar_cpf(cpf, frame):
				a += 1
			if usuario.validar_email(email, frame):
				a += 1
			if usuario.validar_celular(celular, frame):
				a += 1
			if usuario.validar_senha(senha1, senha2, frame):
				a += 1

			if a == 5:
				b.cadastrar_usuarios(nome, cpf, email, celular, senha1, apelido)
				# Linha para fechar a janela depois de 500ms .after agenda a função destroy() para ser executada depois desse tempo.
				cad_janela.after(500, cad_janela.destroy)
				janela_aberta = False

		salvar_cad = ctk.CTkButton(master=frame, text='Salvar', font=('Roboto', 20),
									command=lambda: salvar_usuario())
		salvar_cad.place(x=90, y=520)

		def fechando_janela():
			global janela_aberta
			cad_janela.destroy()
			janela_aberta =False
   
		cad_janela.protocol('WM_DELETE_WINDOW', fechando_janela)
		
		centralizar_janela(cad_janela)
		cad_janela.mainloop()
  
	else:
		print('A janela já está aberta.')



########################################################################################
#############################JANELA DE CADASTRO DE PRODUTOS#############################
########################################################################################

def cad_produto_janela():

	janela_cad_produto = ctk.CTk()
	janela_cad_produto.geometry('300x300')
	janela_cad_produto.resizable(False, False)
	janela_cad_produto.title('Cadastro de produtos')
	# redimensiona janela atribuindo pesos iguais para linha e coluna
	janela_cad_produto.rowconfigure(0, weight=1)
	janela_cad_produto.columnconfigure(0, weight=1)

	frame = ctk.CTkFrame(master=janela_cad_produto, width=600, height=600)
	frame.grid(row=0, column=0, sticky='nsew', padx=15, pady=15)
	frame.grid_columnconfigure(0, weight=1)
	frame.grid_columnconfigure(1, weight=1)

	lb_titulo = ctk.CTkLabel(frame, text='Cadastro de produtos', font=('Roboto', 20))
	lb_titulo.grid(row=0, column=0, columnspan=2)

	lb_descricao = ctk.CTkLabel(frame, text='Descrição', font=('Roboto', 10))
	lb_descricao.grid(row=1, column=0, padx=10, pady=(5, 0), sticky='sw')

	descricao_produto = ctk.CTkEntry(frame, placeholder_text='Descrição do produto', width=250,
											font=('Roboto', 15))
	descricao_produto.grid(row=2, column=0, columnspan=2, padx=10, pady=(0, 5))

	lb_preco = ctk.CTkLabel(frame, text='Preço', font=('Roboto', 10))
	lb_preco.grid(row=3, column=0, padx=10, pady=(5, 0), sticky='w')

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

	preco_produto = ctk.CTkEntry(frame, placeholder_text='Valor do produto', width=250, font=('Roboto', 15))
	preco_produto.grid(row=4, column=0, columnspan=2, padx=10, pady=(0, 5))
	preco_produto.bind('<FocusOut>', lambda event: converte_preco(preco_produto))

	def salvar_prod():
		if p.validar_nome_produto(descricao_produto, frame) and p.validar_preco_produto(preco_produto,frame):
			b.cad_produto(descricao_produto, preco_produto)
			lb_erro = ctk.CTkLabel(frame, text='Produto cadastrado com sucesso!', text_color='#0080FF',
									font=('Roboto', 10))
			lb_erro.grid(row=5, column=0, columnspan=2, padx=10, pady=(5, 0))
			descricao_produto.delete(0, ctk.END)
			preco_produto.delete(0, ctk.END)
			descricao_produto.focus_set()
			return True

	botao_salvar = ctk.CTkButton(frame, text='Salvar', command= lambda: salvar_prod())
	botao_salvar.grid(row=6, column=0, columnspan=2, padx=10, pady=15, sticky='ns')

	centralizar_janela(janela_cad_produto)
	janela_cad_produto.mainloop()



########################################################################################
################################## JANELA dASHBOARD ####################################
########################################################################################

tamanho_minimo = 1
tamanho_maximo = 200
acrescenta = tamanho_minimo
expansao = False
bt_menu = ctk.CTkButton

def janela_dashboard(colaborador):
    
	janela_dash = ctk.CTk()
	janela_dash.title(colaborador)
	janela_dash.resizable(True, True)
	janela_dash.geometry('1100x750')
	
	#função para expandir o frame
	def expansao_frame():
		global acrescenta, expansao
		acrescenta += 10
		rep = janela_dash.after(5,expansao_frame)
		frame_expansivo.configure(width=acrescenta)
		if acrescenta >= tamanho_maximo:
			janela_dash.after_cancel(rep)
			frame_expansivo.configure(width=tamanho_maximo)


	#função para contrair o frame
	def contrair_frame():    
		global acrescenta, expansao, bt_menu
		acrescenta -= 10
		rep = janela_dash.after(5,contrair_frame)
		frame_expansivo.configure(width= acrescenta)
		if acrescenta <= 1:
			janela_dash.after_cancel(rep)
			frame_expansivo.configure(width=tamanho_minimo)
	
	
	def exp_frame_cadastros():
		for widget in frame_expansivo.winfo_children():
			widget.pack_forget()
		contrair_frame()		
		if frame_expansivo.winfo_width() <= 1:			
			expansao_frame()
			#posiciona botoes de cadastro
			bt_janela_cad_produto.pack(side='top', padx=10, pady=5)
			bt_janela_cad_vendedor.pack(side='top', padx=10, pady=5)
			bt_janela_cad_usuario.pack(side='top', padx=10, pady=5)
		else:
			for widget in frame_expansivo.winfo_children():
				widget.pack_forget()
			contrair_frame()
   
   
	def exp_frame_venda():
		for widget in frame_expansivo.winfo_children():
			widget.pack_forget()
		if frame_expansivo.winfo_width() <= 1:			
			expansao_frame()
			bt_janela_venda.pack(side='top', padx=10, pady=5)
		else:
			bt_janela_venda.pack_forget()
			contrair_frame()
   
	
	def exp_frame_consulta_venda():
		for widget in frame_expansivo.winfo_children():
			widget.pack_forget()
		if frame_expansivo.winfo_width() <= 1:			
			expansao_frame()
			bt_janela_consulta_venda.pack(side='top', padx=10, pady=5)
		else:
			bt_janela_consulta_venda.pack_forget()
			contrair_frame()
   

	#imagens dos botões
	img_cadastro = CTkImage(Image.open('img\\adicionar_preto (2).png'), Image.open('img\\adicionar_branco (2).png'))
	img_config = ctk.CTkImage(Image.open('img\\config_preto (2).png'), Image.open('img\\config_branco (2).png'))
	img_menu = ctk.CTkImage(Image.open('img\\menu_preto (2).png'), Image.open('img\\menu_branco (2).png'))
	img_menu_user = ctk.CTkImage(Image.open('img\\menu_user_preto (2).png'), Image.open('img\\menu_user_branco (2).png'))
	img_vendas = ctk.CTkImage(Image.open('img\\vendas_preto (2).png'), Image.open('img\\vendas_branco (2).png'))
	img_consulta = ctk.CTkImage(Image.open('img\\consulta_preto (2).png'), Image.open('img\\consulta_branco (2).png'))
	
 
	#atualiza a janela com as informações atuais
	janela_dash.update()
	
	#frame que é alterado constatemente
	frame_fixo = ctk.CTkFrame(janela_dash, width=50)
	frame_fixo.grid(row=0, column=0, sticky='ns')
	
	#janela_dash.columnconfigure(0, weight=1)
	janela_dash.rowconfigure(0, weight=1)	
	
	frame_expansivo = ctk.CTkFrame (janela_dash, width=0, height=janela_dash.winfo_height())
	frame_expansivo.grid(row=0, column=1, sticky='ns')
 
	#botão menu do frame
	bt_cadastro = ctk.CTkButton(frame_fixo, image=img_cadastro, text='', width=tamanho_minimo -10, height= tamanho_minimo -10, command= exp_frame_cadastros)
	bt_cadastro.pack(side='top', padx=5, pady=(10,5))
 
	bt_vendas = ctk.CTkButton(frame_fixo, image=img_vendas, text='', width=tamanho_minimo -10, height=tamanho_minimo -10, command=exp_frame_venda)
	bt_vendas.pack(side='top', padx=5, pady=5)
 
	bt_consulta = ctk.CTkButton(frame_fixo, image=img_consulta, text='', width=tamanho_minimo -10, height= tamanho_minimo -10, command=exp_frame_consulta_venda)
	bt_consulta.pack(side='top', padx=5, pady=5)
 
	bt_config = ctk.CTkButton(frame_fixo, image=img_config, text='', width=tamanho_minimo - 10,height=tamanho_minimo -10)
	bt_config.pack(side='bottom', padx=5, pady=5)

	bt_perfil = ctk.CTkButton(frame_fixo, image=img_menu_user , text='', width=tamanho_minimo -10, height= tamanho_minimo -10)
	bt_perfil.pack(side='bottom', padx=5, pady=5)

	#remove o argumento width=50 do frame para que ele possa ser modificado
	frame_fixo.grid_propagate(False)
	
	#botoes de cadastros
	bt_janela_cad_produto = ctk.CTkButton(
     									master=frame_expansivo, 
                                       	image=img_cadastro, 
                                      	text='Cadastro de produtos', 
                                        width=180,                             
                                       	height=60,
                                        anchor='w', 
                                       	font=('tuple', 10), 
                                       	command=cad_produto_janela
                                        )

 
	bt_janela_cad_vendedor =ctk.CTkButton(
										master=frame_expansivo, 
										image=img_cadastro, 
										text='Cadastro de vendedores', 
										width=180, 
										height=60,
										anchor='w',
										font=('tuple', 10)
										)
 
 	
	bt_janela_cad_usuario = ctk.CTkButton(
										master=frame_expansivo, 
										image=img_cadastro, 
										text='Cadastro de usuarios', 
										width=180, 
										height=60,
										anchor='w',
										font=('tuple', 10)
										)


	#botoes vendas
	bt_janela_venda = ctk.CTkButton(
									master=frame_expansivo, 
									image=img_vendas, 
									text='Realizar venda', 
									width=180, 
									height=60,
									anchor='w',
									font=('tuple', 10)
									)

	centralizar_janela(janela_dash)
 
	#botões de consultas
	bt_janela_consulta_venda =ctk.CTkButton(
										master=frame_expansivo, 
										image=img_consulta, 
										text='Consultar Vendas', 
										width=180, 
										height=60, 
										anchor='w', 
										font=('tuple', 10)
										)

	janela_dash.mainloop()


########################################################################################
################################### JANELA DE LOGIN ####################################
########################################################################################

def janela_login():
    
	janela_log = ctk.CTk()
	janela_log.geometry('300x400')
	janela_log.title('Login')
	janela_log.resizable(False, False)

	#imagens janela login
	img_login = ctk.CTkImage(Image.open('img\login_preto (3).png'),Image.open('img\login_branco (3).png'), size=(64,64) )

	# cria um frame
	frame_login1 = ctk.CTkFrame(master=janela_log, width=280, height=380)
	frame_login1.place(relx=0.5, rely=0.5, anchor='center')

	# todos os widgets contidos no Frame em ordem de cima para baixo
	titulo_janela = ctk.CTkLabel(master=frame_login1, image=img_login, compound='top', text='Login', font=('Roboto', 20))
	titulo_janela.place(x=115, y=10)

	usuario = ctk.CTkEntry(master=frame_login1, placeholder_text='Usuário', width=230, font=('Roboto', 14))
	usuario.place(x=25, y=110)

	# inf_obg = ctk.CTkLabel(master=frame, text='*Campo obrigatório', text_color='red', font=('Roboto', 8)).place(x=25,y=140)

	senha = ctk.CTkEntry(master=frame_login1, placeholder_text='Senha', width=230, show='*', font=('Roboto', 14))
	senha.place(x=25, y=170)
	# inf_obg2 = ctk.CTkLabel(master=frame, text='*Campo obrigatório', text_color='red', font=('Roboto', 8)).place(x=25,y=200)

	# checkbox lembrar senha
	lembrar_usuario = ctk.BooleanVar()
	checkbox_lembrar = ctk.CTkCheckBox(master=frame_login1, text='Lembrar de mim', variable=lembrar_usuario)
	checkbox_lembrar.place(x=25, y=250)

	usuario.insert(0, u.ler_config()[0])
	senha.insert(0, u.ler_config()[1])


	# função para mostrar e esconder senha
	def mostrar_senha():
		if checkbox_mostrar.get():
			senha.configure(show='')
		else:
			senha.configure(show='*')


	checkbox_mostrar = ctk.CTkCheckBox(master=frame_login1, text='Mostrar', command=mostrar_senha)
	checkbox_mostrar.place(x=150, y=250)


	def login_usuario(usuario_, senha_):
		lembrar = lembrar_usuario.get()
		u.salvar_dados(usuario_, senha_, lembrar)
		resultado = b.verifica_login(usuario_.get(), senha_.get())
		janela_log.protocol('WM_DELETE_WINDOW',janela_log.quit)
		janela_log.destroy()
		if resultado:
			janela_dashboard(resultado[0])
		else:
			erro_senha = ctk.CTkLabel(janela_log, text='Senha ou usuario invalido!')
			erro_senha.place(x=65, y=250)


	botao = ctk.CTkButton(master=frame_login1, text='LOGIN', command=lambda: login_usuario(usuario, senha))
	botao.place(x=75, y=300)

	# Label que chama a janela cadastro
	lb_cadastro = ctk.CTkLabel(master=frame_login1, text='Cadastro', cursor='hand2', text_color='#427DDD')
	lb_cadastro.place(x=120, y=330)
	lb_cadastro.bind('<Button-1>', lambda event: cadastro())
 
	centralizar_janela(janela_log)
	janela_log.mainloop()

janela_login()