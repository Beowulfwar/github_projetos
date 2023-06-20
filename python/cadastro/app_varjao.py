from PIL import Image
import customtkinter as ctk
import matplotlib.pyplot as plt
import class_varjao as cv
import sql_varjao as s
import importlib
import numpy as np


importlib.reload(cv)
importlib.reload(s)

# chama as classes utilizadas
p = cv.Produtos()
b = s.BancoDados('varjao.db')
c = cv.Consultas()
v = cv.Vendas()
u = cv.Validacoes()
cp = cv.Cadastros()
f = cv.Fiscal()

# guarda a situação de uma janela
janela_aberta = False




def grafico_circulo():
    fig, ax = plt.subplots()

    # espessura do gráfico
    size = 0.6

    # valores atribuídos ao gráfico
    vals = np.array([[60], [37], [29], [50], [70]])

    # cores atribuídas ao gráfico e os labels
    bar_color = ['tab:cyan', 'tab:red', 'tab:blue', 'tab:orange', 'tab:green']
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
    grafico_piec = ctk.CTkImage(Image.open('grafico_pie.png'), size=(200, 150))

    return grafico_piec

class Principal:
    tamanho_minimo = 1
    tamanho_maximo = 200
    acrescenta = tamanho_minimo
    expancao = False
    bt_menu = ctk.CTkButton

    def __init__(self) -> None:
        self.ver1, self.ver2, self.ver3, self.ver4 = True, True, True, True
       

    def janela_dashboard(self,colaborador):
        
        """ if Principal.janela_log:
            print('aqui veio tambem')
            Principal.janela_log.destroy() """
            
        

        def limpar_frame(event):
            widget = event.widget
            if isinstance(widget, ctk.CTk):
                for widget in frame_expansivo.winfo_children():
                    widget.pack_forget()
                contrair_frame()

        # função para expandir o frame
        def expansao_frame():

            Principal.acrescenta += 10
            expansao_frame
            frame_expansivo.configure(width=Principal.acrescenta)
            if Principal.acrescenta >= Principal.tamanho_maximo:
                # janela_dash.after_cancel(rep)
                frame_expansivo.configure(width=Principal.tamanho_maximo)

        # função para contrair o frame
        def contrair_frame():
            
            Principal.acrescenta -= 10
            rep = self.janela_dash.after(5, contrair_frame)
            frame_expansivo.configure(width=Principal.acrescenta)
            if Principal.acrescenta <= 1:
                self.janela_dash.after_cancel(rep)
                frame_expansivo.configure(width=Principal.tamanho_minimo)
                self.ver1, self.ver2, self.ver3, self.ver4 = True, True, True, True

        def exp_frame_cadastros():
            global ver1, ver2, ver3, ver4
            for widget in frame_expansivo.winfo_children():
                widget.pack_forget()

            if self.ver1:
                self.ver1, self.ver2, self.ver3, self.ver4 = False, True, True, True
                expansao_frame()
                bt_janela_cad_produto.pack(side='top', padx=10, pady=5)
                bt_janela_cad_usuario.pack(side='top', padx=10, pady=5)
                bt_janela_cad_empresas.pack(side='top', padx=10, pady=5)

            elif frame_expansivo.winfo_width() >= 200:
                contrair_frame()

        def exp_frame_venda():
          
            for widget in frame_expansivo.winfo_children():
                widget.pack_forget()

            if self.ver2:
                self.ver2, self.ver1, self.ver3, self.ver4 = False, True, True, True
                expansao_frame()
                bt_janela_venda.pack(side='top', padx=10, pady=5)
                bt_janela_inf_vendas.pack(side='top', padx=10, pady=5)

            elif frame_expansivo.winfo_width() >= 200:
                contrair_frame()

        def exp_frame_consulta_venda():

            for widget in frame_expansivo.winfo_children():
                widget.pack_forget()

            if self.ver3:
                self.ver3, self.ver1, self.ver2, self.ver4 = False, True, True, True
                expansao_frame()
                bt_janela_consulta_venda.pack(side='top', padx=10, pady=5)
                bt_janela_consulta_usuario.pack(side='top', padx=10, pady=5)
                bt_janela_consulta_produto.pack(side='top', padx=10, pady=5)

            elif frame_expansivo.winfo_width() >= 200:
                contrair_frame()

        def exp_frame_fiscal():

            for widget in frame_expansivo.winfo_children():
                widget.pack_forget()

            if self.ver4:
                self.ver4, self.ver1, self.ver2, self.ver3 = False, True, True, True
                expansao_frame()
                bt_janela_fiscal.pack(side='top', padx=10, pady=5)
                bt_janela_confg_nf.pack(side='top', padx=10, pady=5)

            elif frame_expansivo.winfo_width() >= 200:
                contrair_frame()

        def exp_frame_perfil():

            for widget in frame_expansivo.winfo_children():
                widget.pack_forget()

            if self.ver2:
                self.ver2, self.ver1, self.ver3, self.ver4 = False, True, True, True
                expansao_frame()
                bt_janela_perfil.pack(side='top', padx=10, pady=5)

            elif frame_expansivo.winfo_width() >= 200:
                contrair_frame()

        def exp_frame_config():
       
            for widget in frame_expansivo.winfo_children():
                widget.pack_forget()

            if self.ver2:
                self.ver2, self.ver1, self.ver3, self.ver4 = False, True, True, True
                expansao_frame()
                bt_janela_config.pack(side='top', padx=10, pady=5)
            elif frame_expansivo.winfo_width() >= 200:
                contrair_frame()
                
        self.janela_dash = cv.Janela('1100x750', titulo=colaborador)        

        # imagens dos botões
        img_cadastro = ctk.CTkImage(Image.open('img\\adicionar_preto (2).png'),
                                    Image.open('img\\adicionar_branco (2).png'),
                                    size=(25, 25))
        img_config = ctk.CTkImage(Image.open('img\\config_preto (2).png'),
                                Image.open('img\\config_branco (2).png'),
                                size=(25, 25))
        img_menu_user = ctk.CTkImage(Image.open('img\\menu_user_preto (2).png'),
                                    Image.open('img\\menu_user_branco (2).png'),
                                    size=(25, 25))
        img_vendas = ctk.CTkImage(Image.open('img\\vendas_preto (2).png'),
                                Image.open('img\\vendas_branco (2).png'),
                                size=(25, 25))
        img_consulta = ctk.CTkImage(Image.open('img\\consulta_preto (2).png'),
                                    Image.open('img\\consulta_branco (2).png'),
                                    size=(25, 25))
        img_fiscal = ctk.CTkImage(Image.open('img\\fiscal_preto (2).png'),
                                Image.open('img\\fiscal_branco (2).png'),
                                size=(25, 25))

        
        # atualiza a janela com as informações atuais
        self.janela_dash.bind('<Button-1>', limpar_frame)
        # janela_dash.update()

        # frame que é alterado constatemente
        frame_fixo = ctk.CTkFrame(self.janela_dash, width=50)
        frame_fixo.grid(row=0, column=0, sticky='ns')

        # janela_dash.columnconfigure(0, weight=1)
        self.janela_dash.rowconfigure(0, weight=1)

        frame_expansivo = ctk.CTkFrame(
            self.janela_dash, width=0, height=self.janela_dash.winfo_height())
        frame_expansivo.grid(row=0, column=1, sticky='ns')

        # botão menu do frame
        bt_cadastro = ctk.CTkButton(frame_fixo, image=img_cadastro, text='', width=40,
                                    height=40, command=exp_frame_cadastros)
        bt_vendas = ctk.CTkButton(frame_fixo, image=img_vendas, text='', width=40,
                                height=40, command=exp_frame_venda)
        bt_consulta = ctk.CTkButton(frame_fixo, image=img_consulta, text='', width=40,
                                    height=40, command=exp_frame_consulta_venda)
        bt_fiscal = ctk.CTkButton(frame_fixo, image=img_fiscal, text='', width=40,
                                height=40, command=exp_frame_fiscal)
        bt_config = ctk.CTkButton(frame_fixo, image=img_config, text='', width=40,
                                height=40, command=exp_frame_config)
        bt_perfil = ctk.CTkButton(frame_fixo, image=img_menu_user, text='', width=40,
                                height=40, command=exp_frame_perfil)

        bt_cadastro.pack(side='top', padx=5, pady=(10, 5))
        bt_vendas.pack(side='top', padx=5, pady=5)
        bt_consulta.pack(side='top', padx=5, pady=5)
        bt_fiscal.pack(side='top', padx=5, pady=5)
        bt_config.pack(side='bottom', padx=5, pady=5)
        bt_perfil.pack(side='bottom', padx=5, pady=5)

        # remove o argumento width=50 do frame para que ele possa ser modificado
        frame_fixo.grid_propagate(False)

        # botoes de cadastros
        bt_janela_cad_produto = ctk.CTkButton(
            master=frame_expansivo,
            image=img_cadastro,
            text='Cadastro de produtos',
            width=180,
            height=60,
            anchor='w',
            font=('tuple', 10),
            command=cp.janel_cad_produto
        )

        bt_janela_cad_usuario = ctk.CTkButton(
            master=frame_expansivo,
            image=img_cadastro,
            text='Cadastro de usuários',
            width=180,
            height=60,
            anchor='w',
            font=('tuple', 10),
            command=cp.janel_cad_usuario
        )

        bt_janela_cad_empresas = ctk.CTkButton(
            master=frame_expansivo,
            image=img_cadastro,
            text='Cadastro de Empresas',
            width=180,
            height=60,
            anchor='w',
            font=('tuple', 10),
            command=cp.janel_cad_empresa

        )

        # botoes vendas

        bt_janela_venda = ctk.CTkButton(
            master=frame_expansivo,
            image=img_vendas,
            text='Realizar venda',
            width=180,
            height=60,
            anchor='w',
            font=('tuple', 10),
            command=v.janel_vendas
        )

        bt_janela_inf_vendas = ctk.CTkButton(
            master=frame_expansivo,
            image=img_vendas,
            text='Informe de vendas',
            width=180,
            height=60,
            anchor='w',
            font=('tuple', 10),
            command=v.inf_vendas
        )

        # botões de consultas
        bt_janela_consulta_venda = ctk.CTkButton(
            master=frame_expansivo,
            image=img_consulta,
            text='Consultar Vendas',
            width=180,
            height=60,
            anchor='w',
            font=('tuple', 10),
            command=c.janel_consulta_vendas
        )

        bt_janela_consulta_usuario = ctk.CTkButton(
            master=frame_expansivo,
            image=img_consulta,
            text='Consultar usuário',
            width=180,
            height=60,
            anchor='w',
            font=('tuple', 10),
            command=c.janel_consulta_usuario
        )

        bt_janela_consulta_produto = ctk.CTkButton(
            master=frame_expansivo,
            image=img_consulta,
            text='Consultar produto',
            width=180,
            height=60,
            anchor='w',
            font=('tuple', 10),
            command=c.janel_consulta_produtos
        )
        # botões fiscais
        bt_janela_fiscal = ctk.CTkButton(
            master=frame_expansivo,
            image=img_consulta,
            text='grupos fiscais dos produtos',
            width=180,
            height=60,
            anchor='w',
            font=('tuple', 10),
            command=cp.janel_grupo_fiscal
        )
        bt_janela_confg_nf = ctk.CTkButton(
            master=frame_expansivo,
            image=img_consulta,
            text='Configuração NF',
            width=180,
            height=60,
            anchor='w',
            font=('tuple', 10),
            command=f.janel_config_nf
        )
        # botões de configurações
        bt_janela_config = ctk.CTkButton(
            master=frame_expansivo,
            image=img_consulta,
            text='Consultar produto',
            width=180,
            height=60,
            anchor='w',
            font=('tuple', 10)
        )
        # botões perfil
        bt_janela_perfil = ctk.CTkButton(
            master=frame_expansivo,
            image=img_consulta,
            text='Consultar produto',
            width=180,
            height=60,
            anchor='w',
            font=('tuple', 10)
        )

        self.janela_dash.mainloop()


    ########################################################################################
    ################################### JANELA DE LOGIN ####################################
    ########################################################################################


    def janela_login(self):

        # função para mostrar e esconder senha
        def mostrar_senha():
            if checkbox_mostrar.get():
                senha.configure(show='')
            else:
                senha.configure(show='*')

        # verifica o login do usuario no banco de dados
        def login_usuario():
            lembrar = lembrar_usuario.get()
            u.salvar_dados(usuario, senha, lembrar)
            resultado = b.verifica_login(usuario.get(), senha.get())

            if resultado:
                janela_log.destroy()
                self.janela_dashboard(resultado[1])
            else:
                erro_senha.place(x=65, y=220)

        
        

        img_login = ctk.CTkImage(Image.open('img\\login_preto (3).png'), Image.open('img\\login_branco (3).png'),
                                size=(64, 64))

        janela_log = cv.Janela('300x400', False, False, 'Login')



        frame_login1 = ctk.CTkFrame(master=janela_log, width=280, height=380)
        frame_login1.place(relx=0.5, rely=0.5, anchor='center')

        titulo_janela = ctk.CTkLabel(master=frame_login1, image=img_login, compound='top', text='Login',
                                    font=('', 20))
        usuario = ctk.CTkEntry(
            master=frame_login1, placeholder_text='Usuário', width=230, font=('', 14))
        senha = ctk.CTkEntry(
            master=frame_login1, placeholder_text='Senha', width=230, show='*', font=('', 14))
        lembrar_usuario = ctk.BooleanVar()
        checkbox_lembrar = ctk.CTkCheckBox(
            master=frame_login1, text='Lembrar de mim', variable=lembrar_usuario)
        checkbox_mostrar = ctk.CTkCheckBox(
            master=frame_login1, text='Mostrar', command=mostrar_senha)
        lb_cadastro = ctk.CTkLabel(
            master=frame_login1, text='Cadastro', cursor='hand2', text_color='#0080FF')
        botao = ctk.CTkButton(
            master=frame_login1, text='LOGIN', command=login_usuario)
        erro_senha = ctk.CTkLabel(
            janela_log, text='Senha ou usuário inválido!', text_color='red')

        lb_cadastro.bind('<Button-1>', lambda event: cp.janel_cad_usuario())

        titulo_janela.place(x=115, y=10)
        usuario.place(x=25, y=110)
        senha.place(x=25, y=170)
        checkbox_lembrar.place(x=25, y=250)
        checkbox_mostrar.place(x=150, y=250)
        botao.place(x=75, y=300)
        lb_cadastro.place(x=120, y=330)

        usuario.insert(0, u.ler_config()[0])
        senha.insert(0, u.ler_config()[1])

        janela_log.mainloop()


if __name__ == '__main__':
    app=Principal()
    app.janela_login()
