"""
Responsável por criar a base de dados e as tabelas
"""
import basedados

def CriarBaseDados():
    #criar a ligação à base de dados
    ligacao_bd = basedados.criar_conexao("notas.bd")
    #ativar a integridade referêncial
    ativa_integridade_referencial = "PRAGMA foreign_keys=ON"
    basedados.executar_sql(ligacao_bd,ativa_integridade_referencial)
    #criar tabela alunos
    #alunos(nprocesso<PK>,nome,morada,cp,data_nasc,email)
    sql="""
    CREATE TABLE IF NOT EXISTS Alunos(
        nprocesso INTEGER PRIMARY KEY,
        nome TEXT NOT NULL CHECK(length(nome)>=3),
        morada TEXT,
        cp TEXT,
        data_nasc NUMERIC,
        email TEXT NOT NULL CHECK(email like '%@%.%')
    )
    """
    basedados.executar_sql(ligacao_bd,sql)
    #criar tabela disciplinas  
    # disciplinas(codigo<PK>,nome,ano,nr_modulos,nr_horas,max_faltas)
    sql="""
    CREATE TABLE IF NOT EXISTS Disciplinas(
        codigo INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        ano INTEGER CHECK (ano>=10),
        nr_modulos INTEGER CHECK (nr_modulos>=1),
        nr_horas INTEGER CHECK (nr_horas>=1),
        max_faltas INTEGER CHECK (max_faltas>=1)
    )
    """
    basedados.executar_sql(ligacao_bd,sql)
    #criar tabela notas 
    # notas(codigo<PK>,codigo_disciplina<FK>,nprocesso<FK>,nota,data_nota,ano)
    sql = """
    CREATE TABLE IF NOT EXISTS Notas(
        codigo INTEGER PRIMARY KEY,
        codigo_disciplina INTEGER REFERENCES Disciplinas(codigo),
        nprocesso INTEGER REFERENCES Alunos(nprocesso),
        nota INTEGER CHECK (nota>=10 and nota<=20),
        data_nota NUMERIC,
        ano INTEGER
    )
    """
    basedados.executar_sql(ligacao_bd,sql)