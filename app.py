from flask import Flask, render_template, request, redirect
import tabelas
import alunos, disciplinas, notas

app = Flask(__name__)

#criar base de dados
tabelas.CriarBaseDados()

#Rotas
@app.route("/")
def home():
    return render_template("index.html")

############################Rotas para alunos
@app.route('/aluno/adicionar',methods=["GET","POST"])
def aluno_adicionar():
    return alunos.adicionar()

@app.route("/aluno/listar")
def aluno_listar():
    return alunos.listar()

@app.route("/aluno/apagar",methods=["POST"])
def aluno_apagar():
    return alunos.apagar()

@app.route("/aluno/apagar_confirmado",methods=["POST"])
def aluno_apagar_confirmado():
    return alunos.apagar_confirmado()

@app.route("/aluno/editar",methods=["POST"])
def aluno_editar():
    return alunos.editar()

@app.route("/aluno/editar_confirmado",methods=["POST"])
def aluno_editar_confirmado():
    return alunos.editar_confirmado()

@app.route("/aluno/pesquisar",methods=["GET","POST"])
def aluno_pesquisar():
    return alunos.pesquisar()

########################################Rotas das disciplinas
@app.route("/disciplina/adicionar",methods=["GET","POST"])
def disciplina_adicionar():
    return disciplinas.adicionar()

#############################################Rotas das notas
@app.route("/nota/adicionar",methods=["GET","POST"])
def nota_adicionar():
    return notas.adicionar()

@app.route("/nota/listar")
def nota_listar():
    return notas.listar()

#####################################################
@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/aceitar_cookies",methods="POST")
def aceitar_cookies():
    resposta = make_response(redirect("/"))
    resposta.set_cookie("aviso","aceitou",max_age=30*24*60*60)
    return resposta #TODO: continuar aqui (falta o importa e falta o código layout)

if __name__=="__main__":
    app.run(debug=True)