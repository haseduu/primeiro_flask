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

@app.route("/cadastrar_aluno", methods=["POST"])
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
@app.route("/buscar_aluno", methods=["POST"])
def buscar_aluno():
    if not request.json['id']:
        return 'Erro ao procurar aluno, preciso do ID do aluno para alterar informações', 404
    for aluno in alunos:
        if aluno['id'] == request.json['id']:
            return aluno, 201
    return "Não encontrei um aluno com esse ID", 404

@app.route("/editar_aluno", methods=["POST"])
def editar_aluno():
    
    encontrado = False
    if not request.json['id']:
        return 'Erro ao editar aluno, preciso do ID do aluno para alterar informações', 404

    for aluno in alunos:
        if aluno['id'] == request.json['id']:
            encontrado = True
            if 'nome' in request.json:
                aluno['nome'] = request.json['nome']
            if 'idade' in request.json:
                aluno['idade'] = request.json['idade']
            if 'cpf' in request.json:
                aluno['cpf'] = request.json['cpf']
    if not encontrado:
        return "Não encontrei um aluno com esse ID", 404
    return "Aluno editado com sucesso", 201
@app.route("/deletar_aluno", methods=["POST"])
def deletar_aluno():
    encontrado = False
    if not request.json['id']:
        return 'Erro ao deletar aluno, preciso do ID do aluno para alterar informações', 404
    for aluno in alunos:
        if aluno['id'] == request.json['id']:
            encontrado = True
            i = alunos.index(aluno)
            alunos.pop(i)
            nome = aluno['nome']
            resp = f"Aluno de nome: {nome} deletado com sucesso"
    if not encontrado:
        return "Não encontrei um aluno com esse ID", 404
    return resp, 201 
        
@app.route("/lista_alunos", methods=["GET"])
def lista_aluno():
    resp = {"alunos": alunos}
    return resp if len(alunos) >= 1 else "Ainda não temos alunos registrados"

#disciplina
@app.route("/cadastrar_disciplina", methods=["POST"])
def cadastrar_disciplina():
    global local_id_disciplina
    

    entrada_dados = request.json
   
    if not bool(entrada_dados['nome']) or not bool(entrada_dados['aulas_semanais']):
        return 'Erro ao cadastrar disciplina, faltaram informações', 404
    
    print(local_id, flush=True)
    entrada_dados['id'] = local_id_disciplina
    disciplinas.append(entrada_dados)
    resp = "disciplina cadastrada com sucesso!"
    local_id_disciplina += 1
    return resp, 201
@app.route("/buscar_disciplina", methods=["POST"])
def buscar_disciplina():
    if not request.json['id']:
        return 'Erro ao procurar discplina, preciso do ID da disciplina', 404
    for disciplina in disciplinas:
        if disciplina['id'] == request.json['id']:
            return disciplina, 201
    return "Não encontrei uma disciplina com esse ID", 404

@app.route("/editar_disciplina", methods=["POST"])
def editar_disciplina():
    
    encontrado = False
    if not request.json['id']:
        return 'Erro ao editar disciplina, preciso do ID da disciplina para alterar informações', 404

    for disciplina in disciplinas:
        if disciplina['id'] == request.json['id']:
            encontrado = True
            if 'nome' in request.json:
                disciplina['nome'] = request.json['nome']
            if 'aulas_semanais' in request.json:
                disciplina['aulas_semanais'] = request.json['aulas_semanais']
            
    if not encontrado:
        return "Não encontrei um disciplina com esse ID", 404
    return "disciplina editado com sucesso", 201
@app.route("/deletar_disciplina", methods=["POST"])
def deletar_disciplina():
    encontrado = False
    if not request.json['id']:
        return 'Erro ao deletar disciplina, preciso do ID do disciplina para alterar informações', 404
    for disciplina in disciplinas:
        if disciplina['id'] == request.json['id']:
            encontrado = True
            i = disciplinas.index(disciplina)
            disciplinas.pop(i)
            nome = disciplina['nome']
            resp = f"disciplina de nome: {nome} deletado com sucesso"
    if not encontrado:
        return "Não encontrei um disciplina com esse ID", 404
    return resp, 201 
        
@app.route("/lista_disciplinas", methods=["GET"])
def lista_disciplina():
    resp = {"disciplinas": disciplinas}
    return resp if len(disciplinas) >= 1 else "Ainda não temos disciplinas registrados"

@app.route("/matricular_aluno", methods=["POST"])
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
                 "ID disciplina": id_disciplina,
                 "nome aluno": aluno_nome,
                 "nome disciplina": disciplina_nome}
    matriculas.append(matricula)
    return f"{matricula} aluno matriculado com sucesso", 201
@app.route("/lista_matriculas", methods=["GET"])
def lista_matriculas():
    resp = {"matriculas": matriculas}
    return resp if len(matriculas) >= 1 else "Ainda não temos matriculas registradas"
@app.route("/deletar_matricula", methods=["POST"])
def deletar_matriculas():
    matricula_encontrada = False
    for matricula in matriculas:
        matricula_encontrada = True
        if matricula['ID aluno'] == request.json['ID aluno']:
            i = matriculas.index(matricula)
            matriculas.pop(i)
    if not matricula_encontrada:
         return "Matricula nao encontrada", 404
    return "Matricula(s) deletada(s) com sucesso", 201
    
@app.route("/buscar_matriculas", methods=["POST"])
def buscar_matriculas():
    for matricula in matriculas:
        if matricula['ID aluno'] == request.json['ID aluno']:
            return matricula, 201
    return "Nenhuma matricula encontrada com esse ID, cheque se você envio o ID certo", 404 
if __name__ == "__main__":
    app.run(debug=True)