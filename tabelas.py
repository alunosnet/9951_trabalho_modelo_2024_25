import basedados

#Criar a base de dados e as tabelas
ligacao_bd=basedados.criar_conexao("notas.bd")

ativa_referencia_integridade="PRAGMA foreign_keys=ON"
basedados.executar_sql(ligacao_bd,ativa_referencia_integridade)

#alunos(nprocesso<pk>,nome,morada,cp,data_nasc,email)
comando_cria_tabela_alunos="""
CREATE TABLE IF NOT EXISTS Alunos(
    nprocesso INTEGER PRIMARY KEY,
    nome TEXT NOT NULL CHECK(length(nome)>=3),
    morada TEXT,
    cp TEXT,
    data_nasc NUMERIC,
    email TEXT NOT NULL CHECK(email LIKE '%@%.%')
)
"""
basedados.executar_sql(ligacao_bd,comando_cria_tabela_alunos)
#disciplinas(codigo<pk>,nome,ano,nr_modulos,nr_horas,max_faltas)

comando_cria_tabela_disciplinas="""
CREATE TABLE IF NOT EXISTS Disciplinas(
    codigo INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    ano INTEGER CHECK (ano>0),
    nr_modulos INTEGER CHECK (nr_modulos>0),
    nr_horas INTEGER CHECK (nr_horas>0),
    max_faltas INTEGER CHECK (max_faltas)
)
"""
basedados.executar_sql(ligacao_bd,comando_cria_tabela_disciplinas)

#notas(codigo<pk>,codigo_disciplina<fk>,nprocesso<fk>,nota,data_nota,modulo,ano)
comando_cria_tabela_notas="""
CREATE TABLE IF NOT EXISTS Notas(
    codigo INTEGER PRIMARY KEY,
    codigo_disciplina INTEGER REFERENCES Disciplinas(codigo)
    on delete cascade,
    nprocesso INTEGER REFERENCES Alunos(nprocesso)
    on delete cascade,
    nota INTEGER NOT NULL CHECK (nota>=0 AND nota<=20),
    data_nota NUMERIC NOT NULL,
    modulo INTEGER NOT NULL CHECK (modulo>0),
    ano INTEGER NOT NULL CHECK (ano>0)
)
"""
basedados.executar_sql(ligacao_bd,comando_cria_tabela_notas)