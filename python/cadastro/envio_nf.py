from lxml import etree
from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.entidades.cliente import Cliente
from pynfe.entidades.emitente import Emitente
from pynfe.entidades.notafiscal import NotaFiscal
from pynfe.entidades.fonte_dados import _fonte_dados
from pynfe.processamento.serializacao import SerializacaoXML, SerializacaoQrcode
from pynfe.processamento.assinatura import AssinaturaA1
from pynfe.utils.flags import CODIGO_BRASIL
from decimal import Decimal
from class_varjao import Vendas
from sql_varjao import BancoDados
import datetime
import requests
import urllib3
import os


certificado = 'varjaocert.pfx'
senha = 'varjao123'
uf = 'go'
homologacao = True
chave_privada = 'chave_privada.pem'

urllib3.disable_warnings()
""" url = "https://httpbin.org/"
# url = 'https://homolog.sefaz.go.gov.br/'
# certificado = "path/to/your/certificatovarjaocert.pfx"
# senha = "senha_do_certificado"

response = requests.get(url, cert=(chave_privada, None), verify=False)

print('a resposta é: ', response.text, ' final da resposta!')  """


# emitente
emitente = Emitente(
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
)

# cliente
cliente = Cliente(
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
)

# Nota Fiscal
nota_fiscal = NotaFiscal(
    emitente=emitente,
    #cliente=cliente,
    uf=uf.upper(),
    natureza_operacao='VENDA',  # venda, compra, transferência, devolução, etc
    # 0=Pagamento à vista; 1=Pagamento a prazo; 2=Outros.
    forma_pagamento=0,
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
)

# Produto
nota_fiscal.adicionar_produto_servico(
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
)

# responsável técnico
nota_fiscal.adicionar_responsavel_tecnico(
    cnpj='27138175000116',
    contato='varjao',
    email='tadasoftware@gmail.com',
    fone='61983453152'
)

# serialização
serializador = SerializacaoXML(_fonte_dados, homologacao=homologacao)
nfce = serializador.exportar()

# assinatura
a1 = AssinaturaA1(certificado, senha)
xml = a1.assinar(nfce)

# token de homologacao
token = '000001'

# csc de homologação
csc = '1d386a84c69463e9'  # mexi

# gera e adiciona o qrcode no xml NT2015/003
xml_com_qrcode = SerializacaoQrcode().gerar_qrcode(token, csc, xml)
qrcode = SerializacaoQrcode()
# envio
con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
envio = con.autorizacao(modelo='nfce', nota_fiscal=xml_com_qrcode)
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
arquivo_xml = 'NFCe.xml'
with open(arquivo_xml, 'w') as arquivo:
    arquivo.write(etree.tostring(envio[1], encoding='unicode').replace('\n', '').replace('ns0:', ''))