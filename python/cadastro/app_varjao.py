from PIL import Image
import customtkinter as ctk
import class_varjao as cv
import sql_varjao as s
import importlib

importlib.reload(cv)
importlib.reload(s)

# chama as classes utilizadas
b = s.BancoDados('varjao.db')
c = cv.Consultas()
v = cv.Vendas()
u = cv.Validacoes()
cp = cv.Cadastros()
f = cv.Fiscal()

# guarda a situação de uma janela
janela_aberta = False

class Principal:
    tamanho_minimo = 1
    tamanho_maximo = 200
    acrescenta = tamanho_minimo
    expancao = False
    bt_menu = ctk.CTkButton

    def __init__(self) -> None:
        self.ver1, self.ver2, self.ver3, self.ver4 = True, True, True, True
        
    def janela_dashboard(self, colaborador):

        def fechar_frame(event):
            widget = event.widget
            if isinstance(widget, ctk.CTk):
                for widget in frame_expansivo.winfo_children():
                    widget.pack_forget()
                contrair_frame()

        # função para expandir o frame
        def expansao_frame():

            Principal.acrescenta += 10
            # expansao_frame()
            frame_expansivo.configure(width=Principal.acrescenta)
            self.janela_dash.geometry(
                f'{self.largura_dash + Principal.tamanho_maximo}x{self.altura_dash}')
            if Principal.acrescenta >= Principal.tamanho_maximo:
                # janela_dash.after_cancel(rep)
                frame_expansivo.configure(width=Principal.tamanho_maximo)
                self.janela_dash.geometry(
                    f'{self.janela_dash.winfo_width() + Principal.tamanho_maximo}x{self.altura_dash}')

        # função para contrair o frame

        def contrair_frame():

            Principal.acrescenta -= 10
            rep = self.janela_dash.after(5, contrair_frame)
            frame_expansivo.configure(width=Principal.acrescenta)
            if Principal.acrescenta <= 1:
                self.janela_dash.after_cancel(rep)
                frame_expansivo.configure(width=Principal.tamanho_minimo)
                self.ver1, self.ver2, self.ver3, self.ver4 = True, True, True, True
                self.janela_dash.geometry(
                    f'{self.janela_dash.winfo_width() - Principal.tamanho_maximo}x{self.altura_dash}')

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
                bt_janela_cad_perfil.pack(side='top', padx=10, pady=5)

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

        def exp_frame_consulta():

            for widget in frame_expansivo.winfo_children():
                widget.pack_forget()

            if self.ver3:
                self.ver3, self.ver1, self.ver2, self.ver4 = False, True, True, True
                expansao_frame()
                bt_janela_consulta_venda.pack(side='top', padx=10, pady=5)
                bt_janela_consulta_usuario.pack(side='top', padx=10, pady=5)
                bt_janela_consulta_produto.pack(side='top', padx=10, pady=5)
                bt_janela_consulta_empresa.pack(side='top', padx=10, pady=5)

            elif frame_expansivo.winfo_width() >= 200:
                contrair_frame()

        def exp_frame_fiscal():

            for widget in frame_expansivo.winfo_children():
                widget.pack_forget()

            if self.ver4:
                self.ver4, self.ver1, self.ver2, self.ver3 = False, True, True, True
                expansao_frame()
                bt_janela_grup_fiscal.pack(side='top', padx=10, pady=5)
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

        graficos = cv.Graficos()

        self.largura_dash = 1100
        self.altura_dash = 800

        self.janela_dash = cv.Janela(f'{self.largura_dash}x{self.altura_dash}', resizable=(
            True, True), titulo=colaborador)

        # imagens dos botões
        img_cadastro = ctk.CTkImage(Image.open('img\\adicionar_preto (2).png'),
                                    Image.open(
            'img\\adicionar_branco (2).png'),
            size=(25, 25))
        img_config = ctk.CTkImage(Image.open('img\\config_preto (2).png'),
                                  Image.open('img\\config_branco (2).png'),
                                  size=(25, 25))
        img_menu_user = ctk.CTkImage(Image.open('img\\menu_user_preto (2).png'),
                                     Image.open(
            'img\\menu_user_branco (2).png'),
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
        self.janela_dash.bind('<Button-1>', fechar_frame)
        # janela_dash.update()

        # frame que é alterado constatemente
        frame_fixo = ctk.CTkFrame(
            self.janela_dash, width=50, height=self.janela_dash.winfo_height())
        frame_fixo.grid(row=0, column=0, sticky='ns')

        # janela_dash.columnconfigure(0, weight=1)
        self.janela_dash.rowconfigure(0, weight=1)

        frame_expansivo = ctk.CTkFrame(
            self.janela_dash, width=0, height=self.janela_dash.winfo_height())
        frame_expansivo.grid(row=0, column=1, sticky='ns')

        frame_graficos = ctk.CTkFrame(self.janela_dash, width=self.janela_dash.winfo_width(
        ) - 50, height=self.janela_dash.winfo_height())
        frame_graficos.grid(row=0, column=2, sticky='nswe')

        # graficos dashboard
        lb_grafico_vertical = ctk.CTkLabel(
            frame_graficos, text='', image=graficos.grafico_bar_vertival())
        lb_grafico_horizontal = ctk.CTkLabel(
            frame_graficos, text='', image=graficos.grafico_bar_horizontal())
        lb_grafico_circulo = ctk.CTkLabel(
            frame_graficos, text='', image=graficos.grafico_circulo())

        lb_grafico_vertical.grid(
            row=0, column=1, columnspan=2, padx=10, pady=(10))
        lb_grafico_horizontal.grid(row=1, column=1, padx=10, pady=(10))
        lb_grafico_circulo.grid(row=1, column=2, padx=10, pady=(10))

        # botão menu do frame
        bt_cadastro = ctk.CTkButton(frame_fixo, image=img_cadastro, text='', width=40,
                                    height=40, command=exp_frame_cadastros)
        bt_vendas = ctk.CTkButton(frame_fixo, image=img_vendas, text='', width=40,
                                  height=40, command=exp_frame_venda)
        bt_consulta = ctk.CTkButton(frame_fixo, image=img_consulta, text='', width=40,
                                    height=40, command=exp_frame_consulta)
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
        # frame_fixo.grid_propagate(False)

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

        bt_janela_cad_perfil = ctk.CTkButton(
            master=frame_expansivo,
            image=img_cadastro,
            text='Cadastro de perfil',
            width=180,
            height=60,
            anchor='w',
            font=('tuple', 10),
            command=cp.janel_cad_perfil
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

        bt_janela_consulta_empresa = ctk.CTkButton(
            master=frame_expansivo,
            image=img_consulta,
            text='Consultar empresa',
            width=180,
            height=60,
            anchor='w',
            font=('tuple', 10),
            command=c.janel_consulta_empresa
        )
        # botões fiscais
        bt_janela_grup_fiscal = ctk.CTkButton(
            master=frame_expansivo,
            image=img_consulta,
            text='grupos fiscais dos produtos',
            width=180,
            height=60,
            anchor='w',
            font=('tuple', 10),
            command=f.janel_grupo_fiscal
        )
        bt_janela_confg_nf = ctk.CTkButton(
            master=frame_expansivo,
            image=img_consulta,
            text='Configuração NF',
            width=180,
            height=60,
            anchor='w',
            font=('tuple', 10),
            command=f.janel_config_nfe
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

    def janela_login(self):

        log = cv.Log()

        def completar_usuario():
            if usuario.get() in log.ler_login_usuario():
                senha.insert('0', log.ler_login_usuario()[usuario.get()])

        # função para mostrar e esconder senha
        def mostrar_senha():
            if checkbox_mostrar.get():
                senha.configure(show='')
            else:
                senha.configure(show='*')

        # verifica o login do usuario no banco de dados
        def login_usuario():
            resultado = b.verifica_login(usuario.get(), senha.get())
            if resultado:
                if lembrar_usuario.get():
                    log.salvar_login(usuario.get(), senha.get())
                janela_log.destroy()
                self.janela_dashboard(resultado[1])
            else:
                erro_senha.place(x=65, y=220)

        img_login = ctk.CTkImage(Image.open('img\\login_preto (3).png'), Image.open('img\\login_branco (3).png'),
                                 size=(64, 64))

        janela_log = cv.Janela('300x400', (False, False), 'Login')

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
        usuario.bind('<FocusOut>', lambda e: completar_usuario())

        titulo_janela.place(x=115, y=10)
        usuario.place(x=25, y=110)
        senha.place(x=25, y=170)
        checkbox_lembrar.place(x=25, y=250)
        checkbox_mostrar.place(x=150, y=250)
        botao.place(x=75, y=300)
        lb_cadastro.place(x=120, y=330)

        dado = list(log.ler_login_usuario().items())

        usuario.insert(0, dado[-1][-2])
        senha.insert(0, dado[-1][-1])

        janela_log.mainloop()


if __name__ == '__main__':
    app = Principal()
    app.janela_login()
