# models.py
import datetime

class Usuario:
    """Define a estrutura para um Usuário."""
    def __init__(self, nome, cpf, senha, id_usuario=None):
        self.nome = nome
        self.cpf = cpf
        self.senha = senha  # A senha será tratada como hash no banco de dados
        self.id = id_usuario
        # A lista de semanas agora será consultada diretamente do banco de dados

class Semana:
    """Define a estrutura para uma Semana de um Imóvel."""
    def __init__(self, numero, periodo, preco, id=None, imovel_id=None, dono_id=None):
        self.id = id
        self.imovel_id = imovel_id
        self.numero = numero
        self.periodo = periodo
        self.preco = preco
        self.dono_id = dono_id # ID do usuário que possui a semana

class Imovel:
    """Define a estrutura para um Imóvel, que contém uma lista de Semanas."""
    def __init__(self, nome, localizacao, preco_total, quartos, banheiros, area, avaliacao, id=None):
        self.id = id
        self.nome = nome
        self.localizacao = localizacao
        self.preco_total = preco_total
        self.quartos = quartos
        self.banheiros = banheiros
        self.area = area
        self.avaliacao = avaliacao
        self.semanas = self._gerar_semanas()

    def _gerar_semanas(self):
        """Gera as 52 semanas do ano com preços diferenciados para alta temporada."""
        semanas_geradas = []
        data_inicio_ano = datetime.date(datetime.date.today().year, 1, 1)
        
        for i in range(1, 53):
            # Preços maiores em Dezembro (semanas 49-52) e Janeiro (semanas 1-4)
            if (i >= 49 and i <= 52) or (i >= 1 and i <= 4):
                preco_base = self.preco_total / 60  # Preço maior para alta temporada
            else:
                preco_base = self.preco_total / 100 # Preço normal para baixa temporada
            
            # Formata o preço para ter duas casas decimais
            preco = round(preco_base, 2)

            # Calcula o período da semana
            inicio_semana = data_inicio_ano + datetime.timedelta(weeks=i-1)
            fim_semana = inicio_semana + datetime.timedelta(days=6)
            periodo = f"{inicio_semana.strftime('%d/%m')} - {fim_semana.strftime('%d/%m')}"

            semanas_geradas.append(Semana(numero=i, periodo=periodo, preco=preco))
        return semanas_geradas