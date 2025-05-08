from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Configuração do Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
db = SQLAlchemy(app)

# Modelo do Banco de Dados
class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10), unique=True, nullable=False)
    gaveta_inicio = db.Column(db.Float, default=0.0)
    gaveta_fim = db.Column(db.Float, default=0.0)
    valor_entrada = db.Column(db.Float, default=0.0)
    cartao = db.Column(db.Float, default=0.0)
    retirada = db.Column(db.Float, default=0.0)
    vale = db.Column(db.Float, default=0.0)
    entrada_produtos = db.Column(db.Float, default=0.0)
    pagamentos_gerais = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            "data": self.data,
            "gaveta_inicio": self.gaveta_inicio,
            "gaveta_fim": self.gaveta_fim,
            "valor_entrada": self.valor_entrada,
            "cartao": self.cartao,
            "retirada": self.retirada,
            "vale": self.vale,
            "entrada_produtos": self.entrada_produtos,
            "pagamentos_gerais": self.pagamentos_gerais
        }

# Rotas
@app.route("/")
def home():
    return redirect(url_for('patrao'))

@app.route("/funcionario", methods=['GET', 'POST'])
def funcionario():
    if request.method == 'POST':
        try:
            # Verifica se a data já existe
            data = request.form['data']
            if Registro.query.filter_by(data=data).first():
                flash('Data já cadastrada!', 'warning')
                return redirect(url_for('funcionario'))

            # Converte valores com vírgula para float
            def parse_value(val):
                return float(val.replace(',', '.')) if val else 0.0

            novo_registro = Registro(
                data=data,
                gaveta_inicio=parse_value(request.form['gaveta_inicio']),
                gaveta_fim=parse_value(request.form['gaveta_fim']),
                valor_entrada=parse_value(request.form['valor_entrada']),
                cartao=parse_value(request.form['cartao']),
                retirada=parse_value(request.form['retirada']),
                vale=parse_value(request.form['vale']),
                entrada_produtos=parse_value(request.form['entrada_produtos']),
                pagamentos_gerais=parse_value(request.form['pagamentos_gerais'])
            )
            
            db.session.add(novo_registro)
            db.session.commit()
            flash('Dados salvos com sucesso!', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao salvar dados: {str(e)}', 'danger')

    registros = Registro.query.order_by(Registro.data.desc()).all()
    return render_template('funcionario.html', registros=registros)

@app.route("/patrao")
def patrao():
    registros = Registro.query.order_by(Registro.data.desc()).all()
    datas = [r.data for r in registros]
    return render_template('patrao.html', datas=datas)

@app.route("/api/dados/<data>")
def api_dados(data):
    registro = Registro.query.filter_by(data=data).first()
    if registro:
        return jsonify({
            "status": "success",
            "data": registro.to_dict()
        })
    return jsonify({
        "status": "error",
        "message": "Data não encontrada"
    }), 404

@app.route("/delete/<int:id>", methods=['POST'])
def delete_registro(id):
    registro = Registro.query.get_or_404(id)
    try:
        db.session.delete(registro)
        db.session.commit()
        flash('Registro excluído com sucesso!', 'success')
    except:
        db.session.rollback()
        flash('Erro ao excluir registro', 'danger')
    return redirect(url_for('funcionario'))

# Inicialização do Banco de Dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)