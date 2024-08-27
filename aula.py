from flask import Flask, request

 

app = Flask(__name__)
local_id = 1
local_id_disciplina = 1
alunos = []
disciplinas = []
matriculas = []
@app.route("/", methods=["GET"])
def joelho():
    return "Hello World", 200

@app.route("/teste", methods= ["GET"])
def perna():
    return "Web Service funcionando", 200

@app.route("/aluno", methods=["POST"])
def cadastrar_aluno():
    global local_id 
    

    entrada_dados = request.json
   
    if not bool(entrada_dados['nome']) or not bool(entrada_dados['idade']) or not bool(entrada_dados['cpf']):
        return 'Erro ao cadastrar aluno, faltaram informações', 404
    print(local_id, flush=True)
    entrada_dados['id'] = local_id
    alunos.append(entrada_dados)
    resp = "aluno cadastrado com sucesso!"
    local_id += 1
    return resp, 201
@app.route("/aluno/<int:id>/", methods=["GET"])
def buscar_aluno(id):
    
    for aluno in alunos:
        if aluno['id'] == id:
            return aluno, 200
    return "Não encontrei um aluno com esse ID", 404

@app.route("/aluno/<int:id>/", methods=["PUT"])
def editar_aluno(id):
    
    encontrado = False
    

    for aluno in alunos:
        if id == aluno['id']:
            encontrado = True
            if 'nome' in request.json:
                aluno['nome'] = request.json['nome']
            if 'idade' in request.json:
                aluno['idade'] = request.json['idade']
            if 'cpf' in request.json:
                aluno['cpf'] = request.json['cpf']
    if not encontrado:
        return "Não encontrei um aluno com esse ID", 404
    return "Aluno editado com sucesso", 200
@app.route("/aluno/<int:id>/", methods=["DELETE"])
def deletar_aluno(id):
    encontrado = False
    global alunos
    
    len_inicial = len(alunos)
    alunos = [aluno for aluno in alunos if aluno['id'] != id]
    len_final = len(alunos)
    
    if len_final < len_inicial:
        encontrado = True
    if not encontrado:
         return "Aluno nao encontrado", 404
    return "Aluno(s) deletado(s) com sucesso", 200
        
@app.route("/aluno", methods=["GET"])
def lista_aluno():
    resp = {"alunos": alunos}
    if len(alunos)>=1:
        return resp,200
    else:
        return "Ainda não temos alunos registrados",200

#disciplina
@app.route("/disciplina", methods=["POST"])
def cadastrar_disciplina():
    global local_id_disciplina
    entrada_dados = request.json
    if not bool(entrada_dados['nome']) or not bool(entrada_dados['aulas_semanais']):
        return 'Erro ao cadastrar disciplina, faltaram informações', 404
    entrada_dados['id'] = local_id_disciplina
    disciplinas.append(entrada_dados)
    resp = "disciplina cadastrada com sucesso!"
    local_id_disciplina += 1
    return resp, 201
@app.route("/disciplina/<int:id>/", methods=["GET"])
def buscar_disciplina(id):
    for disciplina in disciplinas:
        if disciplina['id'] == id:
            return disciplina, 200
    return "Não encontrei uma disciplina com esse ID", 404

@app.route("/disciplina/<int:id>/", methods=["PUT"])
def editar_disciplina(id):
    encontrado = False
    for disciplina in disciplinas:
        if disciplina['id'] == id:
            encontrado = True
            if 'nome' in request.json:
                disciplina['nome'] = request.json['nome']
            if 'aulas_semanais' in request.json:
                disciplina['aulas_semanais'] = request.json['aulas_semanais']
    if not encontrado:
        return "Não encontrei um disciplina com esse ID", 404
    return "disciplina editado com sucesso", 200
@app.route("/disciplina/<int:id>/", methods=["DELETE"])
def deletar_disciplina(id):
    global disciplinas
    encontrado = False
    
    len_inicial = len(disciplinas)
    disciplinas = [disciplina for disciplina in disciplinas if disciplina['id'] != id]
    len_final = len(disciplinas)
    
    if len_final < len_inicial:
        encontrada= True
    if not encontrada:
         return "Disciplina nao encontrada", 404
    return "Disciplna(s) deletada(s) com sucesso", 200
@app.route("/disciplina", methods=["GET"])
def lista_disciplina():
    
    resp = {"disciplinas": disciplinas}
    if len(disciplinas)>=1:
        return resp,200
    return "Ainda não temos disciplinas registradas",200
   

@app.route("/matricula", methods=["POST"])
def matricular_aluno():
    aluno_encontrado = False
    disciplina_encontrada = False
    if not request.json['id_aluno'] or not request.json['id_disciplina']:
        return "Faltam informações para matricular o aluno a uma disciplina", 404
    id_aluno = request.json['id_aluno']
    id_disciplina = request.json['id_disciplina']
    for aluno in alunos:
        if aluno['id'] == id_aluno:
            aluno_encontrado = True
            aluno_nome = aluno['nome']
    for disciplina in disciplinas:
        if disciplina['id'] == id_disciplina:
            disciplina_encontrada = True
            disciplina_nome = disciplina['nome']
    if not aluno_encontrado or not disciplina_encontrada:
        return "ID fornecido não possui materia ou aluno associado", 404
    matricula = {"ID aluno": id_aluno,
                 "nome aluno": aluno_nome,
                 "ID disciplina": id_disciplina,
                 "nome disciplina": disciplina_nome}
    matriculas.append(matricula)
    return f"{matricula} aluno matriculado com sucesso", 201
@app.route("/matricula", methods=["GET"])
def lista_matriculas():
    resp = {"alunos": matriculas}
    if len(matriculas)>=1:
        return resp,200
    return "Ainda não temos alunos registrados",200
@app.route("/matricula/<int:id>", methods=["DELETE"])
def deletar_matriculas(id):
    global matriculas
    matricula_encontrada = False
    
    len_inicial = len(matriculas)
    matriculas = [matricula for matricula in matriculas if matricula['ID aluno'] != id]
    len_final = len(matriculas)
    
    if len_final < len_inicial:
        matricula_encontrada= True
    if not matricula_encontrada:
         return "Matricula nao encontrada", 404
    return "Matricula(s) deletada(s) com sucesso", 200
    
@app.route("/matricula/<int:id>", methods=["GET"])
def buscar_matriculas(id):
    resp = []
    encontrado = False
    for matricula in matriculas:
        if matricula['ID aluno'] == id:
            resp.append(matricula)
            encontrado = True
    if encontrado:
        return resp, 200
    return "Nenhuma matricula encontrada com esse ID, cheque se você envio o ID certo", 404 
if __name__ == "__main__":
    app.run(debug=True)

 
