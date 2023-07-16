from lxml import etree
from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.entidades.cliente import Cliente
from pynfe.entidades.emitente import Emitente
from pynfe.entidades.notafiscal import NotaFiscal
from pynfe.entidades.fonte_dados import _fonte_dados
from pynfe.processamento.serializacao import SerializacaoXML, SerializacaoQrcode
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.utils.flags import CODIGO_BRASIL
from decimal import Decimal, ROUND_HALF_UP
from sql_varjao import BancoDados
import datetime
import requests
import urllib3
import re

class NFe:
	
	def __init__(self,emitent:list,produtos:list,client:list=None,**kwargs):    
		self.certificado = 'varjaocert.pfx'
		self.senha = 'varjao123'
		self.uf = 'go'
		self.homologacao = True
		self.chave_privada = 'chave_privada.pem'
		self.produtos = kwargs

		#aviso de perigo desativado
		urllib3.disable_warnings()
		
		""" url = "https://httpbin.org/"
		# url = 'https://homolog.sefaz.go.gov.br/'
		# certificado = "path/to/your/certificatovarjaocert.pfx"
		# senha = "senha_do_certificado"
		response = requests.get(url, cert=(chave_privada, None), verify=False)
		print('a resposta é: ', response.text, ' final da resposta!')  """


		# emitente	
		print('emitente: ',emitent)
		emitente = Emitente(
			razao_social=emitent[1],
			nome_fantasia=emitent[2],
			cnpj=emitent[3],  # mexi         # cnpj apenas números
			codigo_de_regime_tributario=emitent[4], # 1 para simples nacional ou 3 para normal
			inscricao_estadual=emitent[5],   # numero de IE da empresa
			inscricao_municipal=emitent[6],
			cnae_fiscal=emitent[7],          # cnae apenas números
			endereco_logradouro=emitent[8],
			endereco_numero=emitent[9],
			endereco_bairro=emitent[10],
			endereco_municipio=emitent[11],  # mexi
			endereco_uf=emitent[12],         # mexi
			endereco_cep=emitent[13],
			endereco_pais=CODIGO_BRASIL
		)
	
		""" emitente = Emitente(
			razao_social='Varjão comercio eletrônicos ltda - SEM VALOR FISCAL',
			nome_fantasia='Varjão Variedades',
			cnpj='27138175000116',  # mexi   # cnpj apenas números
			codigo_de_regime_tributario='1', # 1 para simples nacional ou 3 para normal
			inscricao_estadual='107866048',  # numero de IE da empresa
			inscricao_municipal='5215231',
			cnae_fiscal='4757100',           # cnae apenas números
			endereco_logradouro='Rua da Paz',
			endereco_numero='4',
			endereco_bairro='Pedregal',
			endereco_municipio='Novo Gama',  # mexi
			endereco_uf='GO',  # mexi
			endereco_cep='72860458',
			endereco_pais=CODIGO_BRASIL
		) """
		if client:
			# cliente
			print ('cliente: ',client)
			cliente = Cliente(
				#razao_social='NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
				tipo_documento=cliente[0],  # CPF ou CNPJ
				#email='email@email.com',
				numero_documento=cliente[1],  # mexi, # numero do cpf ou cnpj
				#indicador_ie=9,                 # 9=Não contribuinte
				#endereco_logradouro='Rua dos Bobos',
				#endereco_numero='Zero',
				#endereco_complemento='Ao lado de lugar nenhum',
				#endereco_bairro='Aquele Mesmo',
				#endereco_municipio='Brasilia',
				#endereco_uf='DF',
				#endereco_cep='12345123',
				#endereco_pais=CODIGO_BRASIL,
				#endereco_telefone='11912341234',
			)
		# cliente
		""" cliente = Cliente(
			#razao_social='NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
			tipo_documento='CPF',  # CPF ou CNPJ
			#email='email@email.com',
			numero_documento='01623445540',  # mexi, # numero do cpf ou cnpj
			#indicador_ie=9,                 # 9=Não contribuinte
			#endereco_logradouro='Rua dos Bobos',
			#endereco_numero='Zero',
			#endereco_complemento='Ao lado de lugar nenhum',
			#endereco_bairro='Aquele Mesmo',
			#endereco_municipio='Brasilia',
			#endereco_uf='DF',
			#endereco_cep='12345123',
			#endereco_pais=CODIGO_BRASIL,
			#endereco_telefone='11912341234',
		) """
  
		
		# Nota Fiscal
		nota_fiscal = NotaFiscal(
			emitente=emitente,
			#cliente=cliente,
			uf=kwargs['uf'].upper(),
			natureza_operacao=kwargs['natureza_operacao'],  # venda, compra, transferência, devolução, etc
			# 0=Pagamento à vista; 1=Pagamento a prazo; 2=Outros.
			forma_pagamento=kwargs['forma_pagamento'],
			#novas formas de pagamento: 01 dinheiro, 02 cheque, 03 cartão de crédito, 04 débito, 05 crédito loja, 10 vale alimentação, 11 vale refeição, 12 vale presente, 13 vale combustível, 15 boleto bancário, 90 sem pagamento, 99 outros
			tipo_pagamento=kwargs['tipo_pagamento'],
			modelo=kwargs['modelo'],                 # 55=NF-e; 65=NFC-e
			serie=kwargs['serie'],
			numero_nf=kwargs['numero_nf'],           # Número do Documento Fiscal.
			data_emissao=datetime.datetime.now(),
			data_saida_entrada=datetime.datetime.now(),
			tipo_documento=kwargs['tipo_documento2'],          # 0=entrada; 1=saida
			municipio=kwargs['municipio'],  # mexi  # Código IBGE do Município
			# 0=Sem geração de DANFE;1=DANFE normal, Retrato;2=DANFE normal Paisagem;3=DANFE Simplificado;4=DANFE NFC-e;
			tipo_impressao_danfe=kwargs['tipo_impressao_danfe'],
			forma_emissao=kwargs['forma_emissao'],         # 1=Emissão normal (não em contingência);
			cliente_final=kwargs['cliente_final'],           # 0=Normal;1=Consumidor final;
			indicador_destino=kwargs['indicador_destino'],
			indicador_presencial=kwargs['indicador_presencial'],
			# 1=NF-e normal;2=NF-e complementar;3=NF-e de ajuste;4=Devolução de mercadoria.
			finalidade_emissao=kwargs['finalidade_emisssao'],
			processo_emissao=kwargs['processo_emissao'],  # 0=Emissão de NF-e com aplicativo do contribuinte;
			transporte_modalidade_frete=kwargs['transporte_modalidade'],  # 9=Sem Ocorrência de Transporte.
			informacoes_adicionais_interesse_fisco=kwargs['informacoes_adicionais_interesse_fisco'],
			totais_tributos_aproximado=Decimal(kwargs['totais_tributos_aproximado']).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP),
		)
		print('bem aqui: ',Decimal(kwargs['totais_tributos_aproximado']).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP))
		for chave, valor in kwargs.items():
			print(f'{chave}: {valor}')
		
		""" nota_fiscal = NotaFiscal(
			emitente=emitente,
			#cliente=cliente,
			uf=self.uf.upper(),
			natureza_operacao='VENDA',  # venda, compra, transferência, devolução, etc
			# 0=Pagamento à vista; 1=Pagamento a prazo; 2=Outros.			
			forma_pagamento=0,
			#novas formas de pagamento: 01 dinheiro, 02 cheque, 03 cartão de crédito, 04 débito, 05 crédito loja, 10 vale alimentação, 11 vale refeição, 12 vale presente, 13 vale combustível, 15 boleto bancário, 90 sem pagamento, 99 outros
			tipo_pagamento=1,
			modelo=65,                 # 55=NF-e; 65=NFC-e
			serie='1',
			numero_nf='117',           # Número do Documento Fiscal.
			data_emissao=datetime.datetime.now(),
			data_saida_entrada=datetime.datetime.now(),
			tipo_documento=1,          # 0=entrada; 1=saida
			municipio='5215231',  # mexi  # Código IBGE do Município
			# 0=Sem geração de DANFE;1=DANFE normal, Retrato;2=DANFE normal Paisagem;3=DANFE Simplificado;4=DANFE NFC-e;
			tipo_impressao_danfe=4,
			forma_emissao='1',         # 1=Emissão normal (não em contingência);
			cliente_final=1,           # 0=Normal;1=Consumidor final;
			indicador_destino=1,
			indicador_presencial=1,
			# 1=NF-e normal;2=NF-e complementar;3=NF-e de ajuste;4=Devolução de mercadoria.
			finalidade_emissao='1',
			processo_emissao='0',  # 0=Emissão de NF-e com aplicativo do contribuinte;
			transporte_modalidade_frete=9,  # 9=Sem Ocorrência de Transporte.
			informacoes_adicionais_interesse_fisco='jesse',
			totais_tributos_aproximado=Decimal('21.06'),
		) """

		
		for prod in produtos:
			print('itens: ',prod )
			print('ajeitato: ',prod['pis_modalidade'][:2])
			print('ajeitato: ',prod['confins_modalidade'][:2])
			nota_fiscal.adicionar_produto_servico(
				codigo=prod['codigo'],#                           # id do produto
				#descricao=prod['descricao'],
				descricao='NOTA FISCAL EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
				ncm=prod['ncm'],
				cfop=prod['cfop'],
				unidade_comercial=prod['unidade_comercial'],
				ean=prod['ean'],
				ean_tributavel=prod['ean_tributavel'],
				quantidade_comercial=Decimal(prod['quatidade_comercial']),#        # 12 unidades
				valor_unitario_comercial=Decimal(prod['valor_unitario_comercial']).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP),#  # preço unitário
				valor_total_bruto=Decimal(prod['valor_total_bruto']).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP),#       # preço total
				unidade_tributavel=prod['unidade_tributavel'],
				quantidade_tributavel=Decimal(prod['quantidade_tributavel']),#
				valor_unitario_tributavel=Decimal(prod['valor_unitario_tributavel']).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP),#
				ind_total=prod['ind_total'],#
				icms_modalidade=prod['icms_modalidade'],
				icms_origem=prod['icms_origem'],
				icms_csosn=prod['icms_csosn'],  # mexi
				pis_modalidade=prod['pis_modalidade'][:2],
				cofins_modalidade=prod['confins_modalidade'][:2],
				valor_tributos_aprox=Decimal(prod['valor_tributos_aproximados']).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)
			) 

  
		""" nota_fiscal.adicionar_produto_servico(
			codigo='000328',                           # id do produto
			descricao='NOTA FISCAL EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
			ncm='99999999',
			cfop='5102',
			unidade_comercial='UN',
			ean='SEM GTIN',
			ean_tributavel='SEM GTIN',
			quantidade_comercial=Decimal('12'),        # 12 unidades
			valor_unitario_comercial=Decimal('9.75'),  # preço unitário
			valor_total_bruto=Decimal('117.00'),       # preço total
			unidade_tributavel='UN',
			quantidade_tributavel=Decimal('12'),
			valor_unitario_tributavel=Decimal('9.75'),
			ind_total=1,
			icms_modalidade='102',
			icms_origem=0,
			icms_csosn='102',  # mexi
			pis_modalidade='07',
			cofins_modalidade='07',
			valor_tributos_aprox=Decimal('21.06')
		) """

  

		# responsável técnico
		nota_fiscal.adicionar_responsavel_tecnico(
			cnpj=kwargs['cnpj_responsavel'],
			contato=kwargs['contato_responsavel'],
			email=kwargs['email_responsavel'],
			fone=kwargs['fone_responsavel']
		)
	
		""" nota_fiscal.adicionar_responsavel_tecnico(
			cnpj='27138175000116',
			contato='varjao',
			email='tadasoftware@gmail.com',
			fone='61983453152'
		) """

		
		# serialização
		serializador = SerializacaoXML(_fonte_dados, homologacao=self.homologacao)
		nfce = serializador.exportar()
		# assinatura
		a1 = AssinaturaA1(self.certificado, self.senha)
		xml = a1.assinar(nfce)

		# token de homologacao
		token = '000001'

		csc= kwargs['csc']

		# csc de homologação
		""" csc = '1d386a84c69463e9'  # mexi """
		# gera e adiciona o qrcode no xml NT2015/003
		xml_com_qrcode = SerializacaoQrcode().gerar_qrcode(token, csc, xml)
		# envio
		con = ComunicacaoSefaz(self.uf, self.certificado, self.senha, self.homologacao)
		envio = con.autorizacao(modelo='nfce', nota_fiscal=xml_com_qrcode)

		print(envio)
		print(envio[1])

		# em caso de sucesso o retorno será o xml autorizado
		# Ps: no modo sincrono, o retorno será o xml completo (<nfeProc> = <NFe> + <protNFe>)
		# no modo async é preciso montar o nfeProc, juntando o retorno com a NFe
		if envio[0] == 0:
			print('Sucesso!')
			print(etree.tostring(envio[1], encoding="unicode").replace(
				'\n', '').replace('ns0:', ''))
			print(envio[1])
		# em caso de erro o retorno será o xml de resposta da SEFAZ + NF-e enviada
		else:
			print('Erro:')
			print(envio[1].text)  # resposta da sefaz
			print('Nota:')
			print(etree.tostring(envio[2], encoding="unicode"))  # nfe
   
	

		if envio[0] == 0:
			retorno_sefaz = etree.tostring(envio[1], encoding="unicode")
			# Encontra ID no retorno da SEFAZ, caso a nota tenha sido enviada com sucesso
			id_match = re.search(r'Id=(\S+)', retorno_sefaz)
			if id_match:
				# Seleciona apenas o número da NFe na SEFAZ para servir de nome para o arquivo
				numero_nfe = id_match.group(1)
				
				# Remove caracteres inválidos do número da NFe
				numero_nfe = re.sub(r'[^a-zA-Z0-9]', '', numero_nfe)
				
				arquivo_xml = f'xml_nfe/{numero_nfe}.xml'
				with open(arquivo_xml, 'w') as arquivo:
					arquivo.write(etree.tostring(envio[1], encoding='unicode').replace('\n', '').replace('ns0:', ''))

    

	