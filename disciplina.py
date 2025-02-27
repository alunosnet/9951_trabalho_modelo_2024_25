from flask import Flask, render_template, request, make_response, redirect
import basedados

def disciplina_adicionar():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    #verificar se o método é GET
    if request.method=="GET":   
        return render_template('disciplina/adicionar.html')
    if request.method=="POST":
        #validar os dados
        nome = request.form.get("input_nome")
        if not nome:
            return render_template('disciplina/adicionar.html',mensagem="Tem de preencher o campo do nome")
        ano = request.form.get("input_ano")
        nr_modulos = request.form.get("input_nr_modulos")
        nr_horas = request.form.get("input_nr_horas")
        max_faltas = request.form.get("input_max_faltas")
        #adicionar à bd
        sql = "INSERT INTO Disciplinas(nome,ano,nr_modulos,nr_horas,max_faltas) VALUES (?,?,?,?,?)"
        parametros = (nome,ano,nr_modulos,nr_horas,max_faltas)
        basedados.executar_sql(ligacao_bd,sql,parametros)
        return redirect("/disciplina/listar")

def disciplina_listar():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    sql = "SELECT * FROM Disciplinas"
    dados = basedados.consultar_sql(ligacao_bd,sql)
    return render_template('disciplina/listar.html',registos = dados)

def disciplina_apagar():
    #codigo
    codigo = request.form.get("codigo")
    #consulta à bd para recolher os dados da disciplina selecionado
    sql = "SELECT * FROM Disciplinas WHERE codigo=?"
    parametros=(codigo,)
    #executar a consulta
    ligacao_bd = basedados.criar_conexao("notas.bd")
    dados =  basedados.consultar_sql(ligacao_bd,sql,parametros)
    return render_template("disciplina/apagar.html",registo = dados[0])

def disciplina_apagar_confirmado():
    #codigo
    codigo = request.form.get("codigo")
    sql = "DELETE FROM Disciplinas WHERE codigo=?"
    parametros=(codigo,)
    ligacao_bd = basedados.criar_conexao("notas.bd")
    basedados.executar_sql(ligacao_bd,sql,parametros)
    #redirecionar para a pagina de listar 
    return redirect("/disciplina/listar")

def disciplina_editar():
    #codigo
    codigo = request.form.get("codigo")
    #consulta à bd para recolher os dados 
    sql = "SELECT * FROM Disciplinas WHERE codigo=?"
    parametros=(codigo,)
    #executar a consulta
    ligacao_bd = basedados.criar_conexao("notas.bd")
    dados =  basedados.consultar_sql(ligacao_bd,sql,parametros)
    return render_template("disciplina/editar.html",registo = dados[0])

def disciplina_editar_confirmado():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    codigo = request.form.get("codigo")
    #consulta à bd para recolher os dados 
    sql = "SELECT * FROM Disciplinas WHERE codigo=?"
    parametros=(codigo,)
    #executar a consulta
    dados =  basedados.consultar_sql(ligacao_bd,sql,parametros)
    if request.method=="POST":
        #validar os dados
        nome = request.form.get("input_nome")
        if not nome:
            return render_template('aluno/editar.html',registo=dados[0],mensagem="Tem de preencher o campo do nome")
        ano = request.form.get("input_ano")
        nr_modulos = request.form.get("input_nr_modulos")
        nr_horas = request.form.get("input_nr_horas")
        max_faltas = request.form.get("input_max_faltas")
        codigo = request.form.get("codigo")
        #editar a disciplina na bd
        sql = "UPDATE Disciplinas SET nome=?, ano=?, nr_modulos=?, nr_horas=?, max_faltas=? WHERE codigo=?"
        parametros = (nome,ano,nr_modulos,nr_horas,max_faltas,codigo)
        basedados.executar_sql(ligacao_bd,sql,parametros)
        return redirect("/disciplina/listar")