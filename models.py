import random # Necessário para gerar IDs de usuário simulados

# Define a estrutura para um Usuário
class Usuario:
    def __init__(self, nome, cpf, senha, id_usuario=None):
        self.nome = nome
        self.cpf = cpf
        self.senha = senha # Em um sistema real, senhas seriam hashadas
        self.id = id_usuario if id_usuario else str(random.randint(10000, 99999))
        self.semanas = [] # Lista de semanas que o usuário possui

# Define a estrutura para uma Semana de um Imóvel
class Semana:
    def __init__(self, numero, periodo, preco, dono=None):
        self.numero = numero # Número identificador da semana
        self.periodo = periodo # Período de datas da semana
        self.preco = preco # Preço da cota da semana
        self.dono = dono # Objeto Usuario que possui a semana, ou None se disponível

# Define a estrutura para um Imóvel, que contém uma lista de Semanas
class Imovel:
    def __init__(self, nome, localizacao, preco_total, quartos, banheiros, area, avaliacao):
        self.nome = nome # Nome do imóvel (e.g., "ZenithPlace")
        self.localizacao = localizacao # Endereço ou descrição da localização
        self.preco_total = preco_total
        self.quartos = quartos
        self.banheiros = banheiros
        self.area = area
        self.avaliacao = avaliacao
        self.semanas = self._dividir_em_semanas() # Geração automática das semanas

    def _dividir_em_semanas(self):
        semanas = []
        # Exemplo de lógica de preço por temporada
        for i in range(1, 53):
            # Alta temporada: dezembro a fevereiro (semanas 48-52 e 1-8)
            if (48 <= i <= 52) or (1 <= i <= 8):
                preco_semana = self.preco_total * 0.03 # 3% do valor total
            else:
                preco_semana = self.preco_total * 0.015 # 1.5% do valor total

            # Período genérico, pode ser aprimorado com datas reais
            periodo = f"{i}/JAN - {i}/JAN (Exemplo)"
            # Condicionais para os períodos específicos que você tinha nos snippets
            if i == 15: periodo = '12/04 - 19/04'
            if i == 22: periodo = '31/05 - 07/06'
            if i == 35: periodo = '30/08 - 06/09'
            if i == 28: periodo = '12/07 - 19/07 (Alta Temporada)'
            if i == 29: periodo = '19/07 - 26/07 (Alta Temporada)'
            if i == 41: periodo = '11/10 - 18/10'

            semanas.append(Semana(str(i), periodo, preco_semana))
        return semanas

