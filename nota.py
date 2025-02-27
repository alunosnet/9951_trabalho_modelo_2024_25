from flask import Flask, render_template, request, make_response, redirect
import basedados

def nota_adicionar():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    #verificar se o método é GET
    if request.method=="GET":
        alunos = basedados.consultar_sql(ligacao_bd,"SELECT * FROM Alunos ORDER BY nome")
        disciplinas = basedados.consultar_sql(ligacao_bd,"SELECT * FROM Disciplinas ORDER BY ano,nome")
        return render_template('nota/adicionar.html',alunos = alunos, disciplinas = disciplinas)
    if request.method=="POST":
        alunos = basedados.consultar_sql(ligacao_bd,"SELECT * FROM Alunos ORDER BY nome")
        disciplinas = basedados.consultar_sql(ligacao_bd,"SELECT * FROM Disciplinas ORDER BY ano,nome")
        #validar os dados
        nprocesso=request.form.get("nprocesso")
        codigo_disciplina=request.form.get("codigo_disciplina")
        nota=int(request.form.get("input_nota"))
        data=request.form.get("input_data")
        modulo=request.form.get("input_modulo")
        ano=request.form.get("input_ano")
        if nota<0 or nota>20:
            return render_template("nota/adicionar.html",alunos=alunos,disciplinas=disciplinas,mensagem="Nota não é válida")
        #adicionar à bd
        sql = "INSERT INTO Notas(nprocesso,codigo_disciplina,nota,data_nota,modulo,ano) VALUES (?,?,?,?,?,?)"
        parametros = (nprocesso,codigo_disciplina,nota,data,modulo,ano)
        basedados.executar_sql(ligacao_bd,sql,parametros)
        return redirect("/nota/listar")
    
def nota_listar():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    sql = """ SELECT notas.*,alunos.nome as NomeAluno,disciplinas.nome as  NomeDisciplina FROM Notas
    INNER JOIN Alunos ON Notas.nprocesso=Alunos.nprocesso
    INNER JOIN Disciplinas ON Notas.Codigo_Disciplina=Disciplinas.codigo
    ORDER BY Notas.nprocesso,Notas.ano
    """
    dados = basedados.consultar_sql(ligacao_bd,sql)
    #######################################Consulta com group by e avg
    sql = """SELECT Alunos.nome as NomeAluno,avg(nota) as media 
            FROM Notas INNER JOIN Alunos 
            ON Notas.nprocesso=Alunos.nprocesso
            GROUP BY Notas.nprocesso,Alunos.nome"""
    medias = basedados.consultar_sql(ligacao_bd,sql)
    return render_template('nota/listar.html',registos = dados,medias=medias)

def nota_apagar():
    #codigo
    codigo = request.form.get("codigo")
    #consulta à bd para recolher os dados 
    sql = """SELECT Notas.*,Alunos.nome as NomeAluno FROM Notas
        INNER JOIN Alunos ON Alunos.nprocesso=Notas.nprocesso 
        WHERE codigo=?"""
    parametros=(codigo,)
    #executar a consulta
    ligacao_bd = basedados.criar_conexao("notas.bd")
    dados =  basedados.consultar_sql(ligacao_bd,sql,parametros)
    return render_template("nota/apagar.html",registo = dados[0])

def nota_apagar_confirmado():
    #codigo
    codigo = request.form.get("codigo")
    sql = "DELETE FROM Notas WHERE codigo=?"
    parametros=(codigo,)
    ligacao_bd = basedados.criar_conexao("notas.bd")
    basedados.executar_sql(ligacao_bd,sql,parametros)
    #redirecionar para a pagina de listar alunos
    return redirect("/nota/listar")

def nota_editar():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    alunos = basedados.consultar_sql(ligacao_bd,"SELECT * FROM Alunos ORDER BY nome")
    disciplinas = basedados.consultar_sql(ligacao_bd,"SELECT * FROM Disciplinas ORDER BY ano,nome")
    codigo=request.form.get("codigo")
    sql="SELECT * FROM Notas WHERE codigo=?"
    parametros=(codigo,)
    dados=basedados.consultar_sql(ligacao_bd,sql,parametros)
    return render_template('nota/editar.html',alunos = alunos, disciplinas = disciplinas,registo=dados[0])

def nota_editar_confirmado():
    ligacao_bd = basedados.criar_conexao("notas.bd")
    codigo=request.form.get("codigo")
    print(codigo)
    sql="SELECT * FROM Notas WHERE codigo=?"
    parametros=(codigo,)
    dados=basedados.consultar_sql(ligacao_bd,sql,parametros)
    alunos = basedados.consultar_sql(ligacao_bd,"SELECT * FROM Alunos ORDER BY nome")
    disciplinas = basedados.consultar_sql(ligacao_bd,"SELECT * FROM Disciplinas ORDER BY ano,nome")
    #validar os dados
    nprocesso=request.form.get("nprocesso")
    codigo_disciplina=request.form.get("codigo_disciplina")
    nota=int(request.form.get("input_nota"))
    data=request.form.get("input_data")
    modulo=request.form.get("input_modulo")
    ano=request.form.get("input_ano")
    if nota<0 or nota>20:
        return render_template("nota/adicionar.html",alunos=alunos,disciplinas=disciplinas,mensagem="Nota não é válida",registo=dados[0])
    #adicionar à bd
    sql = "UPDATE Notas SET nprocesso=?,codigo_disciplina=?,nota=?,data_nota=?,modulo=?,ano=? WHERE codigo=?"
    parametros = (nprocesso,codigo_disciplina,nota,data,modulo,ano,codigo)
    basedados.executar_sql(ligacao_bd,sql,parametros)
    return redirect("/nota/listar")