from flask import Flask, request, render_template, redirect
import basedados
from datetime import datetime

def adicionar():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    alunos = basedados.consultar_sql(ligacao_bd,"SELECT nprocesso,nome FROM Alunos ORDER BY nome")
    disciplinas = basedados.consultar_sql(ligacao_bd,"SELECT codigo,nome FROM Disciplinas ORDER BY ano,nome")
    if request.method=="GET":
        return render_template("notas/adicionar.html",alunos=alunos,disciplinas=disciplinas)
    #POST -> guardar na bd
    if request.method=="POST":
        #validar os dados do form
        nprocesso = request.form.get("inprocesso")
        codigo = request.form.get("icodigo_disciplina")
        nota = request.form.get("inota")
        data = request.form.get("idata_nota")
        ano = request.form.get("iano")
        #verificar se os campos estão preenchidos
        if not nprocesso or not codigo or not data or not ano or not nota:
            erro="Os campos são preenchimento obrigatório"
            return render_template("notas/adicionar.html",alunos=alunos,disciplinas=disciplinas,mensagem=erro)
        #validação da nota
        nota = int(nota)
        if nota < 0 or nota > 20:
            erro = "A nota tem de ser um nº entre 0 e 20"
            return render_template("notas/adicionar.html",alunos=alunos,disciplinas=disciplinas,mensagem=erro)
        #validação do ano
        if ano not in ("10","11","12"):
            erro="O ano tem de ser 10, 11 ou 12"
            return render_template("notas/adicionar.html",alunos=alunos,disciplinas=disciplinas,mensagem=erro)
        #validação da data
        data_atual = datetime.now()
        data_nota = datetime.strptime(data,"%Y-%m-%d")
        if data_nota>data_atual:
            erro="A data da nota tem de ser inferior ou igual à data atual"
            return render_template("notas/adicionar.html",alunos=alunos,disciplinas=disciplinas,mensagem=erro)
        #validação da select alunos
        if nprocesso=="-1":
            erro="Tem de selecionar um aluno."
            return render_template("notas/adicionar.html",alunos=alunos,disciplinas=disciplinas,mensagem=erro)
        #validação da select disciplinas
        if codigo=="-1":
            erro="Tem de selecionar uma disciplina."
            return render_template("notas/adicionar.html",alunos=alunos,disciplinas=disciplinas,mensagem=erro)
        #adicionar à tabela notas
        sql="INSERT INTO Notas(codigo_disciplina,nprocesso,nota,data_nota,ano) VALUES (?,?,?,?,?)"
        parametros=(codigo,nprocesso,nota,data,ano)
        basedados.executar_sql(ligacao_bd,sql,parametros)
        return redirect("/nota/listar")

def listar():
    ligacao_bd=basedados.criar_conexao("notas.bd")
    sql="""
        SELECT notas.*,alunos.nome as NomeAluno, disciplinas.nome as NomeDisciplina
        FROM notas
        INNER JOIN alunos ON notas.nprocesso = alunos.nprocesso
        INNER JOIN disciplinas ON notas.codigo_disciplina = disciplinas.codigo
        ORDER BY notas.nprocesso, notas.ano
    """
    dados = basedados.consultar_sql(ligacao_bd,sql)
    return render_template("notas/listar.html",registos=dados)

def mediaporaluno():
    """Função devolve a lista das médias das notas por aluno"""
    sql = """SELECT AVG(nota) as media,alunos.nome as NomeAluno 
            FROM Notas
            INNER JOIN alunos ON notas.nprocesso=alunos.nprocesso
            GROUP BY Notas.nprocesso
            ORDER BY AVG(nota) DESC"""
    ligacao_bd=basedados.criar_conexao("notas.bd")
    medias = basedados.consultar_sql(ligacao_bd,sql)
    return medias