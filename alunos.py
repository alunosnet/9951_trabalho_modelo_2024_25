from flask import Flask, request, render_template, redirect
import basedados

def adicionar():
    #se é um método GET enviar o form para preencher
    if request.method=="GET":
        return render_template("alunos/adicionar.html")
    #se é um método POST adicionar à bd
    if request.method=="POST":
        #criar uma ligação à bd
        ligacao_bd=basedados.criar_conexao("notas.bd")
        #validar os dados
        nome      = request.form.get("inome")
        morada    = request.form.get("imorada")
        cp        = request.form.get("icp")
        data_nasc = request.form.get("idata_nasc")
        email     = request.form.get("iemail")
        if not nome or len(nome)<3 or len(nome)>100:
            return render_template("alunos/adicionar.html",mensagem="Nome não é válido. Deve ser preenchido com 3 letras no minimo e 100 no máximo.")
        if not morada:
            return render_template("alunos/adicionar.html",mensagem="A morada deve estar preenchida.")
        #adicionar os dados à bd
        sql = "INSERT INTO Alunos(nome,morada,cp,data_nasc,email) VALUES (?,?,?,?,?)"
        parametros = (nome,morada,cp,data_nasc,email)
        basedados.executar_sql(ligacao_bd,sql,parametros)
        #redicionar para a rota /aluno/listar
        return redirect("/aluno/listar")
    
def listar():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    sql = "SELECT * FROM Alunos ORDER BY Nome"
    dados = basedados.consultar_sql(ligacao_bd,sql)
    return render_template("alunos/listar.html",registos = dados)

def apagar():
    nprocesso = request.form.get("nprocesso")
    #consulta à bd para recolher os dados do aluno
    sql = "SELECT * FROM Alunos WHERE nprocesso=?"
    parametros =(nprocesso)
    ligacao_bd=basedados.criar_conexao("notas.bd")
    dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
    return render_template("alunos/apagar.html",registo = dados[0])

def apagar_confirmado():
    nprocesso = request.form.get("nprocesso")
    ligacao_bd=basedados.criar_conexao("notas.bd")
    sql="DELETE FROM Alunos WHERE nprocesso=?"
    parametros=(nprocesso)
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/aluno/listar")

def editar():
    nprocesso = request.form.get("nprocesso")
    #consulta à bd para recolher os dados do aluno
    sql = "SELECT * FROM Alunos WHERE nprocesso=?"
    parametros =(nprocesso)
    ligacao_bd=basedados.criar_conexao("notas.bd")
    dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
    return render_template("alunos/editar.html",registo = dados[0])

def editar_confirmado():
    nprocesso = request.form.get("nprocesso")
    #criar uma ligação à bd
    ligacao_bd=basedados.criar_conexao("notas.bd")
    sql = "SELECT * FROM Alunos WHERE nprocesso=?"
    parametros =(nprocesso)
    dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
    #validar os dados
    nome      = request.form.get("inome")
    morada    = request.form.get("imorada")
    cp        = request.form.get("icp")
    data_nasc = request.form.get("idata_nasc")
    email     = request.form.get("iemail")
    if not nome or len(nome)<3 or len(nome)>100:
        return render_template("alunos/editar.html",registo=dados[0],mensagem="Nome não é válido. Deve ser preenchido com 3 letras no minimo e 100 no máximo.")
    if not morada:
        return render_template("alunos/editar.html",registo=dados[0],mensagem="A morada deve estar preenchida.")
    #atualizar os dados na bd
    sql = "UPDATE Alunos SET nome = ?, morada = ?, cp = ?, data_nasc=?, email=? WHERE nprocesso=?"
    parametros=(nome,morada,cp,data_nasc,email,nprocesso)
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/aluno/listar")

def pesquisar():
    if request.method=="GET":
        return render_template("alunos/pesquisar.html")
    if request.method=="POST":
        nome = request.form.get("inome")
        ligacao_bd = basedados.criar_conexao("notas.bd")
        #TODO: erro ao pesquisar
        sql = "SELECT * FROM Alunos WHERE nome like ?"
        nome = "%" + nome + "%"
        parametros=(nome,)
        dados = basedados.consultar_sql(ligacao_bd,sql,parametros)
        return render_template("alunos/pesquisar.html",registos=dados)