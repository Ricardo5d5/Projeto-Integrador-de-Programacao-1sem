#Versao Final

import requests
from lxml import html

import csv

pagina = requests.get ('https://www.cepea.esalq.usp.br/br/indicador/soja.aspx')
dados = html.fromstring(pagina.content)

print()

#Retorna numero de linha do Banco de Dados
def Num_Linhas_BD(Local_arquivo):
    Num_Linha = 0
    with open(Local_arquivo, 'r+', newline='') as csv_file:
        Num_Linha = sum(1 for line in csv_file)     # conta a legenda
    return (Num_Linha)

#Função para verificar se o novo dado está no Banco de Dados
def Verifica_NewData_BD(Local_arquivo, Dado_Ver):
    with open(Local_arquivo, 'r') as csv_file:   
        arquivo = csv.reader(csv_file, delimiter=';')
        Num_Linha_QueNaoTem = 0
        for i in arquivo:
            if (i[0] == Dado_Ver):
                break  
            else:
                Num_Linha_QueNaoTem += 1
    return (Num_Linha_QueNaoTem)

#Função para Criar um Banco de Dados .csv
def Cria_BD(Local_arquivo, indicador):     #indicador = 1 (PARANAGUA) e 2 (PARANA)
    with open(Local_arquivo, 'w', newline='') as arquivo:
        final = csv.writer(arquivo, delimiter=';')
        final.writerow(["Data", "VALOR R$*", "VAR./DIA", "VAR./MÊS", "VALOR US$*"])
        
        
        for cont in range(15, 0, -1):   #OBS:15 é o número de dados que ficam disponivel no site
            dados_linha = dados.xpath('//*[@id="imagenet-indicador{}"]/tbody/tr[{}]/td/text()'.format(indicador, cont))   
            final.writerow(dados_linha)
            #print(dados_linha)
    print('Arquivos criados com sucesso!')

#Função para adicionar os novos dados no Banco de Dados .csv
def Adcionar_BD(Local_arquivo, indicador):     #indicador = 1 (PARANAGUA) e 2 (PARANA)
    Num_Linhas_Arq = Num_Linhas_BD(Local_arquivo)
    print('numero linhas antes de atualizar:', Num_Linhas_Arq)

    with open(Local_arquivo, 'a', newline='') as arquivo:
        final = csv.writer(arquivo, delimiter=';')
       
        for cont in range(15, 0, -1):   #OBS:15 é o número de dados que ficam disponivel no site
            dados_linha = dados.xpath('//*[@id="imagenet-indicador{}"]/tbody/tr[{}]/td/text()'.format(indicador, cont))
            Num_Linha_QueNaoTem = Verifica_NewData_BD(Local_arquivo, dados_linha[0])

            if (Num_Linhas_Arq == Num_Linha_QueNaoTem):
                final.writerow(dados_linha)
    print('Arquivos atualizados com sucesso!')
    Num_Linhas_Arq = Num_Linhas_BD(Local_arquivo)
    print('numero linhas depois de atualizar:', Num_Linhas_Arq)

#Imprime Banco de Dados
def Print_BD(Local_arquivo):
    with open(Local_arquivo, 'r') as csv_file:  
        arquivo = csv.reader(csv_file, delimiter=';')
        for i in arquivo:
            print(str(i[0]).rjust(11, ' '), str(i[1]).rjust(11, ' '), str(i[2]).rjust(10, ' '), str(i[3]).rjust(10, ' '), str(i[4]).rjust(12, ' '))

#Para Criar
#Cria_BD('esalq_PARANAGUA_soja.csv')
#Cria_BD('esalq_PARANA_soja.csv')

#Para Adcionar
BD_Paranagua = '/content/drive/My Drive/SojaWin_BDAg_(WebBot)/esalq_PARANAGUA_soja.csv'
BD_Parana = '/content/drive/My Drive/SojaWin_BDAg_(WebBot)/esalq_PARANA_soja.csv'

Adcionar_BD(BD_Paranagua, 1)    
Adcionar_BD(BD_Parana, 2)

print()
print('INDICADOR DA SOJA ESALQ/BM&FBOVESPA - PARANAGUÁ')  
Print_BD(BD_Paranagua)
print()
print('INDICADOR DA SOJA ESALQ/BM&FBOVESPA - PARANA')  
Print_BD(BD_Parana)
