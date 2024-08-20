from flask import Flask, request

app = Flask(__name__)

alunos = []

@app.route("/", methods=["GET"])
def joelho():
    return "Hello World", 200
    
@app.route("/teste", methods= ["GET"])
def perna():
    return "Web Service funcionando", 200

@app.route("/cadastrar_aluno", methods=["POST"])
def cadastrar_aluno():
    entrada_dados = {
        "nome": "Tiago",
        "idade": 37,
        "peso": 80.5
    }
    alunos.append(entrada_dados)
    resp = "alunos cadastrado com sucesso!"

    
    return resp, 201
@app.route("/lista_alunos", methods=["GET"])
def lista_aluno():
    return f"A lista de alunos registrados é {alunos}" if len(alunos) >= 1 else "Ainda não temos alunos registrados"
if __name__ == "__main__":
    app.run(debug=True)