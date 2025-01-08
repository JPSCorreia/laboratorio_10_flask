from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Criar a aplicação Flask
app = Flask(__name__)


# Configuração do URI do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desativa o histórico de alterações

# Inicialização do SQLAlchemy
db = SQLAlchemy(app)

# Definir o modelo Produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    nome = db.Column(db.String(80), nullable=False)  # Nome do produto (não pode ser nulo)

    def __repr__(self):
        return f'<Produto {self.nome}>'

# Definir a rota principal
@app.route("/")
def home():
    return "Ola, Flask!"

# Operação POST para adicionar um novo produto
@app.route('/produtos', methods=['POST'])
def add_produto():
    nome = request.json.get('nome')  # Obter o nome do JSON enviado
    novo_produto = Produto(nome=nome)
    db.session.add(novo_produto)  # Adicionar o produto à sessão
    db.session.commit()  # Guardar as alterações na base de dados
    return {"message": "Produto adicionado com sucesso!", "produto": {"id": novo_produto.id, "nome": novo_produto.nome}}, 201

# Operação GET para obter todos os produtos
@app.route('/produtos', methods=['GET'])
def get_produtos():
    produtos = Produto.query.all()  # Obter todos os produtos
    return {"produtos": [{"id": p.id, "nome": p.nome} for p in produtos]}

# Operação PUT para atualizar um produto
@app.route('/produtos/<int:id>', methods=['PUT'])
def update_produto(id):
    produto = Produto.query.get_or_404(id)  # Obter o produto ou retornar 404
    produto.nome = request.json.get('nome', produto.nome)  # Atualizar o nome, se fornecido
    db.session.commit()  # Guardar as alterações
    return {"message": "Produto atualizado com sucesso!", "produto": {"id": produto.id, "nome": produto.nome}}

# Operação DELETE para apagar um produto
@app.route('/produtos/<int:id>', methods=['DELETE'])
def delete_produto(id):
    produto = Produto.query.get_or_404(id)  # Obter o produto ou retornar 404
    db.session.delete(produto)  # Remover o produto
    db.session.commit()  # Confirmar a exclusão
    return {"message": f"Produto {id} apagado com sucesso!"}

# Iniciar a aplicação no modo de depuração
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria a tabela na base de dados
    app.run(debug=True)