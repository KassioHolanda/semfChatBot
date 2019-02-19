import postgresql as psql
from Conexao import *

con = Conexao('pq://readonly:123@100.100.100.203/poda_teste')
cpf = '01211973360'
rs = con.consultar("select nome from pessoa where cpf = '{0}'".format(cpf))
for linha in rs:
    print(linha[0])

con.fechar()
