from flask import Flask, request
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


# Carrega as variáveis de ambiente do arquivo .cred (se disponível)
load_dotenv('.cred')

# Configurações para conexão com o banco de dados usando variáveis de ambiente
config = {
    'host': os.getenv('DB_HOST', 'localhost'),  # Obtém o host do banco de dados da variável de ambiente
    'user': os.getenv('DB_USER'),  # Obtém o usuário do banco de dados da variável de ambiente
    'password': os.getenv('DB_PASSWORD'),  # Obtém a senha do banco de dados da variável de ambiente
    'database': os.getenv('DB_NAME', 'db_escola'),  # Obtém o nome do banco de dados da variável de ambiente
    'port': int(os.getenv('DB_PORT', 3306)),  # Obtém a porta do banco de dados da variável de ambiente
    'ssl_ca': os.getenv('SSL_CA_PATH')  # Caminho para o certificado SSL
}

# Função para conectar ao banco de dados
def connect_db():
    """Estabelece a conexão com o banco de dados usando as configurações fornecidas."""
    try:
        # Tenta estabelecer a conexão com o banco de dados usando mysql-connector-python
        conn = mysql.connector.connect(**config)
        if conn.is_connected():
            return conn
    except Error as err:
        # Em caso de erro, imprime a mensagem de erro
        print(f"Erro: {err}")
        return None
 

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return "Web Service LVL 2 de Richarlison", 200

@app.route("/teste", methods= ["GET"])
def teste():
    return "Web Service funcionando", 200

@app.route("/aluno", methods=["POST"])
def cadastrar_aluno():
    sucess = False
    entrada_dados = request.json
    nome = entrada_dados['nome']
    idade = entrada_dados['idade']
    cpf = entrada_dados['cpf']
    if not bool(entrada_dados['nome']) or not bool(entrada_dados['idade']) or not bool(entrada_dados['cpf']):
        return 'Erro ao cadastrar aluno, faltaram informações', 404
    conn = connect_db()
    aluno_id = None
    if conn and conn.is_connected():
        try:
            cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
            sql = "INSERT INTO tbl_alunos (nome, cpf, idade) VALUES (%s, %s, %s)"  # Comando SQL para inserir um aluno
            values = (nome, cpf, idade)  # Dados a serem inseridos

            # Executa o comando SQL com os valores fornecidos
            print(f"Executando SQL: {sql} com valores: {values}")
            cursor.execute(sql, values)
            
            # Confirma a transação no banco de dados
            conn.commit()

            # Obtém o ID do registro recém-inserido
            aluno_id = cursor.lastrowid
            sucess = True
            
        except Error as err:
            # Em caso de erro na inserção, imprime a mensagem de erro
            print(f"Erro ao inserir aluno: {err}")
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()
    if sucess:
        return "Aluno cadastrado com sucesso", 201
    return "Internal error", 
@app.route("/aluno/<int:id>/", methods=["GET"])
def buscar_aluno(id):
    conn = connect_db()  # Conecta ao banco de dados
    if conn:
        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
        sql = "SELECT * FROM tbl_alunos WHERE id = %s"  # Comando SQL para buscar um aluno pelo ID

        try:
            # Executa o comando SQL com o ID fornecido
            cursor.execute(sql, (id))
            # Recupera o resultado da consulta
            aluno = cursor.fetchone()
            # Verifica se o aluno foi encontrado e imprime seus detalhes
            if aluno:
                d = {"nome": aluno['nome'], "idade":  aluno['idade'], "cpf": aluno['cpf'], "id": aluno['id']}
                return d
            else:
                return "Aluno não encontrado", 404
        except Error as err:
            # Em caso de erro na busca, imprime a mensagem de erro
            print(f"Erro ao buscar aluno: {err}")
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()

@app.route("/aluno/<int:id>/", methods=["PUT"])
def editar_aluno(id):
    erro = False
    entrada_dados = request.json
    if not entrada_dados['nome'] or not entrada_dados['idade'] or not entrada_dados['cpf']:
        return "Json missing arguments or mispelled", 404
    conn = connect_db()  # Conecta ao banco de dados
    if conn:
        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
        sql = "UPDATE tbl_alunos SET nome = %s, cpf = %s, idade = %s WHERE id = %s"  # Comando SQL para atualizar o aluno
        values = (entrada_dados['nome'], entrada_dados['cpf'], entrada_dados['idade'], id)  # Dados a serem atualizados

        try:
            # Executa o comando SQL com os valores fornecidos
            cursor.execute(sql, values)
            # Confirma a transação no banco de dados
            conn.commit()
            # Verifica se alguma linha foi afetada (atualizada)
            if cursor.rowcount:
                return "Aluno editado com sucesso"
            else:
                return "Aluno não encontrado"
        except Error as err:
            # Em caso de erro na atualização, imprime a mensagem de erro
            erro = True
            errormessage = err
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()
        if erro:
            return f"Erro: {err}"
        if cursor.rowcount:
            return "Aluno editado com sucesso"
        else:
            return "Aluno não encontrado"
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
    erro = False
    encontrado = False
    conn = connect_db()
    if conn:
        cursor = conn.cursor()  # Cria um cursor para executar comandos SQL
        sql = "SELECT * FROM tbl_alunos"  # Comando SQL para selecionar todos os alunos
        response = []
        try:
            # Executa o comando SQL
            cursor.execute(sql)
            # Recupera todos os registros da consulta
            alunos = cursor.fetchall()
            # Itera sobre os resultados e imprime os detalhes de cada aluno
            for aluno in alunos:
                d = {"nome": aluno['nome'], "idade":  aluno['idade'], "cpf": aluno['cpf'], "id": aluno['id']}
                encontrado = True
                response.append(d)
        except Error as err:
            erro = True
            errormessage = err
        finally:
            # Fecha o cursor e a conexão para liberar recursos
            cursor.close()
            conn.close()
    if erro:
        return errormessage
    if encontrado:
        return response
    
#disciplina
@app.route("/disciplina", methods=["POST"])
def cadastrar_disciplina():
    global local_id_disciplina
    entrada_dados = request.json
    if not bool(entrada_dados['nome']) or not bool(entrada_dados['aulas_semanais']):
        return 'Erro ao cadastrar disciplina, faltaram informações', 404
    entrada_dados['id'] = local_id_disciplina
    disciplinas.append(entrada_dados)
    resp = f"disciplina cadastrada com sucesso!, o id é {local_id_disciplina}"
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

 
