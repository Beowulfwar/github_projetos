import customtkinter as ctk
import sqlite3 as sql
import re
import os
import matplotlib.pyplot as plt
import numpy as np


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
                self.nome_erro.grid(row=1, column=1, padx=(0, 10), pady=(5, 0), sticky='w')

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
                self.preco_erro.grid(row=3, column=1, padx=(0, 10), pady=(5, 0), sticky='w')
            return False
        else:
            var.configure(border_color='gray')

            if self.preco_erro is not None:
                self.preco_erro.grid_remove()
                self.preco_erro = None
            return True



            
    



    







