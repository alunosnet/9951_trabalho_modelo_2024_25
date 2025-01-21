from flask import Flask, render_template, request, redirect
import tabelas
import alunos

app = Flask(__name__)

#criar base de dados
tabelas.CriarBaseDados()

#Rotas
@app.route("/")
def home():
    return render_template("index.html")

############################Rotas para aulnos
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

if __name__=="__main__":
    app.run(debug=True)