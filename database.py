from models import Usuario, Semana, Imovel

# --- Simulação do Banco de Dados em Memória ---
# Criando usuários de exemplo
usuarios_simulados = [
    Usuario("João Silva", "111.111.111-11", "senha123", "user_joao"),
    Usuario("Maria Oliveira", "222.222.222-22", "senha456", "user_maria")
]

# Criando imóveis de exemplo
# Os valores de preco_total são arbitrários para fins de exemplo
imovel_pastelzinho = Imovel(
    "PASTELZINHO DE CHOCOLATE",
    "Rua dos Doces, 789, São Paulo",
    1200000.00, # Preço total do imóvel
    4, 3, "150m²", "9.5 - Excelente"
)

imovel_zenith = Imovel(
    "ZenithPlace",
    "Avenida Principal, 123, Rio de Janeiro",
    1500000.00, # Preço total do imóvel
    5, 4, "200m²", "9.7 - Excelente"
)

imovel_topazio = Imovel(
    "Topázio Imperial Hotel",
    "Praia das Esmeraldas, 456, Salvador",
    2000000.00, # Preço total do imóvel
    6, 5, "250m²", "9.8 - Luxuoso"
)

# Atualiza as semanas dos imóveis com dados específicos se for o caso
# Essas semanas serão sobrescritas ou adicionadas conforme a lógica
# para que os valores batam com o que o usuário tinha no seu código inicial.
# A geração automática acima é mais genérica. Aqui, garantimos as semanas exatas
# que você tinha no seu primeiro snippet.
imovel_pastelzinho.semanas = [
    Semana('15', '12/04 - 19/04', 15000.00),
    Semana('22', '31/05 - 07/06', 18000.00),
    Semana('35', '30/08 - 06/09', 22000.00)
]
imovel_topazio.semanas = [
    Semana('28', '12/07 - 19/07 (Alta Temporada)', 35000.00),
    Semana('29', '19/07 - 26/07 (Alta Temporada)', 35000.00),
    Semana('41', '11/10 - 18/10', 28000.00)
]
# Para ZenithPlace, usaremos as semanas geradas automaticamente pela classe Imovel no models.py.

banco_dados_simulado = {
    "usuarios": {u.cpf: u for u in usuarios_simulados}, # Mapeia por CPF para login
    "imoveis": {
        "ZenithPlace": imovel_zenith,
        "PASTELZINHO DE CHOCOLATE": imovel_pastelzinho,
        "Topázio Imperial Hotel": imovel_topazio
    }
}
