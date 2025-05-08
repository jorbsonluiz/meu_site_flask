from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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