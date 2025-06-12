import tkinter as tk
from tkinter import ttk, messagebox
# Importa as classes e o banco de dados simulado dos arquivos separados
from models import Usuario, Semana, Imovel
from database import banco_dados_simulado

# --- Classe Principal da Aplicação ---
class Sistemainvestimento:
    def __init__(self, root):
        self.root = root
        self.root.title("InvestFacil - Sistema de Investimentos")
        self.root.geometry("800x600") 
        self.root.resizable(True, True)

        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)

        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.telas = {} # Dicionário para armazenar as diferentes telas (frames)
        self.usuario_logado = None # Armazena o objeto do usuário logado

        # Cria todos os frames e os posiciona na grade
        self.criar_frames_telas()

        # Configura o conteúdo de cada tela
        self.configurar_tela_login()
        self.configurar_tela_cadastro()
        self.configurar_tela_principal()
        self.configurar_tela_perfil()
        self.configurar_tela_investimento()
        self.configurar_tela_imovel1() # ZenithPlace (tela de descrição)
        self.configurar_tela_imovel2() # Topázio Imperial Hotel (tela de descrição)
        self.configurar_tela_listar_imovel1() # Semanas de PASTELZINHO DE CHOCOLATE
        self.configurar_tela_listar_imovel2() # Semanas de Topázio Imperial Hotel
        self.configurar_tela_listar_imovel_zenith() # Semanas de ZenithPlace

        # Inicia mostrando a tela de login
        self.mostrar_tela("tela_login")

    # Método para criar e posicionar todos os frames das telas
    def criar_frames_telas(self):
        nomes_telas = [
            "tela_login", "tela_cadastro", "tela_principal", "tela_perfil",
            "tela_investimento", "tela_imovel1", "tela_imovel2",
            "tela_listar_imovel1", "tela_listar_imovel2", "tela_listar_imovel_zenith"
        ]
        for nome_tela in nomes_telas:
            frame = tk.Frame(self.container, bg="#f0f0f0") # Fundo claro para todas as telas
            self.telas[nome_tela] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    # Método para exibir uma tela específica
    def mostrar_tela(self, nome_tela):
        tela = self.telas[nome_tela]
        tela.tkraise()
        # Atualiza o conteúdo de telas específicas quando elas são exibidas
        if nome_tela == "tela_perfil" and self.usuario_logado:
            self.atualizar_tela_perfil()
        elif nome_tela == "tela_listar_imovel1":
            self.configurar_tela_listar_imovel1()
        elif nome_tela == "tela_listar_imovel2":
            self.configurar_tela_listar_imovel2()
        elif nome_tela == "tela_listar_imovel_zenith":
            self.configurar_tela_listar_imovel_zenith()


    def configurar_tela_login(self):
        tela_login = self.telas["tela_login"]
        frame_login = tk.Frame(tela_login, bg="#f0f0f0", padx=30, pady=30, relief="groove", bd=2)
        frame_login.place(relx=0.5, rely=0.5, anchor="center")

        titulo = tk.Label(frame_login, text="Login", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333333")
        titulo.grid(row=0, column=0, columnspan=2, pady=15)

        tk.Label(frame_login, text="CPF:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, sticky="e", pady=8, padx=5)
        self.cpf_login_entry = tk.Entry(frame_login, width=30, font=("Arial", 12), relief="solid", bd=1)
        self.cpf_login_entry.grid(row=1, column=1, sticky="w", pady=8, padx=5)

        tk.Label(frame_login, text="Senha:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, sticky="e", pady=8, padx=5)
        self.senha_login_entry = tk.Entry(frame_login, width=30, show="*", font=("Arial", 12), relief="solid", bd=1)
        self.senha_login_entry.grid(row=2, column=1, sticky="w", pady=8, padx=5)

        btn_logar = tk.Button(frame_login, text="Entrar", command=self.processar_login,
                              font=("Arial", 13, "bold"), bg="#4CAF50", fg="white", relief="raised", bd=3, width=20)
        btn_logar.grid(row=3, column=0, columnspan=2, pady=15, sticky="ew")

        btn_cadastrar = tk.Button(frame_login, text="Não tem conta? Cadastre-se agora!", command=lambda: self.mostrar_tela("tela_cadastro"),
                                  font=("Arial", 10), bg="#2196F3", fg="white", relief="flat", bd=0)
        btn_cadastrar.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

    def processar_login(self):
        cpf = self.cpf_login_entry.get()
        senha = self.senha_login_entry.get()

        usuario = banco_dados_simulado["usuarios"].get(cpf)

        if usuario and usuario.senha == senha:
            self.usuario_logado = usuario
            messagebox.showinfo("Login", f"Bem-vindo, {self.usuario_logado.nome}!")
            self.mostrar_tela("tela_principal")
        else:
            messagebox.showerror("Erro de Login", "CPF ou senha inválidos.")

    def configurar_tela_cadastro(self):
        tela_cadastro = self.telas["tela_cadastro"]
        frame_cadastro = tk.Frame(tela_cadastro, bg="#f0f0f0", padx=30, pady=30, relief="groove", bd=2)
        frame_cadastro.place(relx=0.5, rely=0.5, anchor="center")

        titulo = tk.Label(frame_cadastro, text="Cadastro de Novo Usuário", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333333")
        titulo.grid(row=0, column=0, columnspan=2, pady=15)

        tk.Label(frame_cadastro, text="Nome Completo:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, sticky="e", pady=8, padx=5)
        self.nome_cadastro_entry = tk.Entry(frame_cadastro, width=30, font=("Arial", 12), relief="solid", bd=1)
        self.nome_cadastro_entry.grid(row=1, column=1, sticky="w", pady=8, padx=5)

        tk.Label(frame_cadastro, text="CPF:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, sticky="e", pady=8, padx=5)
        self.cpf_cadastro_entry = tk.Entry(frame_cadastro, width=30, font=("Arial", 12), relief="solid", bd=1)
        self.cpf_cadastro_entry.grid(row=2, column=1, sticky="w", pady=8, padx=5)

        tk.Label(frame_cadastro, text="Senha:", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=0, sticky="e", pady=8, padx=5)
        self.senha_cadastro_entry = tk.Entry(frame_cadastro, width=30, show="*", font=("Arial", 12), relief="solid", bd=1)
        self.senha_cadastro_entry.grid(row=3, column=1, sticky="w", pady=8, padx=5)

        btn_cadastrar = tk.Button(frame_cadastro, text="Finalizar Cadastro", command=self.cadastrar_usuario,
                                  font=("Arial", 13, "bold"), bg="#FF9800", fg="white", relief="raised", bd=3, width=20)
        btn_cadastrar.grid(row=4, column=0, columnspan=2, pady=15, sticky="ew")

        btn_voltar = tk.Button(frame_cadastro, text="Voltar para Login", command=lambda: self.mostrar_tela("tela_login"),
                               font=("Arial", 10), bg="#607D8B", fg="white", relief="flat", bd=0)
        btn_voltar.grid(row=5, column=0, columnspan=2, pady=10, sticky="ew")

    def cadastrar_usuario(self):
        nome = self.nome_cadastro_entry.get()
        cpf = self.cpf_cadastro_entry.get()
        senha = self.senha_cadastro_entry.get()

        if not nome or not cpf or not senha:
            messagebox.showerror("Erro de Cadastro", "Todos os campos são obrigatórios.")
            return

        if cpf in banco_dados_simulado["usuarios"]:
            messagebox.showerror("Erro de Cadastro", "CPF já cadastrado. Tente outro CPF ou faça login.")
            return

        try:
            novo_usuario = Usuario(nome, cpf, senha)
            banco_dados_simulado["usuarios"][cpf] = novo_usuario
            messagebox.showinfo("Sucesso", f"Usuário {nome} cadastrado com sucesso!")
            self.mostrar_tela("tela_login")
        except Exception as e:
            messagebox.showerror("Erro Inesperado", f"Não foi possível cadastrar o usuário: {str(e)}")

    def configurar_tela_principal(self):
        tela_principal = self.telas["tela_principal"]
        frame_principal = tk.Frame(tela_principal, bg="#f0f0f0", padx=50, pady=50)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center")

        titulo = tk.Label(frame_principal, text="INVESTFACIL", font=("Arial", 28, "bold"), bg="#f0f0f0", fg="#4A148C")
        titulo.grid(row=0, column=0, columnspan=3, pady=30)

        btn_perfil = tk.Button(frame_principal, text="Meu Perfil", width=20, height=2,
                               command=lambda: self.mostrar_tela("tela_perfil"),
                               font=("Arial", 14), bg="#00BCD4", fg="white", relief="raised", bd=3)
        btn_perfil.grid(row=1, column=0, pady=15, padx=15)

        btn_investimento = tk.Button(frame_principal, text="Investimentos", width=20, height=2,
                                     command=lambda: self.mostrar_tela("tela_investimento"),
                                     font=("Arial", 14), bg="#4CAF50", fg="white", relief="raised", bd=3)
        btn_investimento.grid(row=1, column=1, pady=15, padx=15)

        btn_saibamais = tk.Button(frame_principal, text="Saiba Mais", width=20, height=2,
                                  command=self.saiba_mais,
                                  font=("Arial", 14), bg="#FFC107", fg="#333333", relief="raised", bd=3)
        btn_saibamais.grid(row=1, column=2, pady=15, padx=15)

        btn_sair = tk.Button(frame_principal, text="Sair", command=lambda: self.mostrar_tela("tela_login"),
                             font=("Arial", 12), bg="#F44336", fg="white", relief="raised", bd=3, width=15)
        btn_sair.grid(row=2, column=0, columnspan=3, pady=30)

    def configurar_tela_perfil(self):
        tela_perfil = self.telas["tela_perfil"]
        # Limpa widgets existentes para atualizar o conteúdo dinamicamente
        for widget in tela_perfil.winfo_children():
            widget.destroy()

        frame_perfil = tk.Frame(tela_perfil, bg="#f0f0f0", padx=30, pady=30, relief="groove", bd=2)
        frame_perfil.place(relx=0.5, rely=0.5, anchor="center")

        titulo = tk.Label(frame_perfil, text="Meu Perfil", font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333333")
        titulo.pack(pady=20)

        if self.usuario_logado:
            tk.Label(frame_perfil, text=f"Nome: {self.usuario_logado.nome}", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)
            tk.Label(frame_perfil, text=f"CPF: {self.usuario_logado.cpf}", font=("Arial", 12), bg="#f0f0f0").pack(pady=5)

            tk.Label(frame_perfil, text="\nMinhas Semanas Adquiridas:", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=15)

            if self.usuario_logado.semanas:
                # Criar uma tabela para exibir as semanas adquiridas
                colunas = ('imovel', 'semana', 'periodo', 'valor')
                tabela_semanas = ttk.Treeview(frame_perfil, columns=colunas, show='headings', height=8)
                tabela_semanas.heading('imovel', text='Imóvel')
                tabela_semanas.heading('semana', text='Semana Nº')
                tabela_semanas.heading('periodo', text='Período')
                tabela_semanas.heading('valor', text='Valor (R$)')

                tabela_semanas.column('imovel', width=150, anchor='center')
                tabela_semanas.column('semana', width=80, anchor='center')
                tabela_semanas.column('periodo', width=150, anchor='center')
                tabela_semanas.column('valor', width=120, anchor='center')

                for semana_adquirida in self.usuario_logado.semanas:
                    # Encontrar o nome do imóvel para a semana adquirida
                    nome_imovel = "Desconhecido"
                    for nome, imovel_obj in banco_dados_simulado["imoveis"].items():
                        if semana_adquirida in imovel_obj.semanas:
                            nome_imovel = nome
                            break
                    valor_formatado = f"{semana_adquirida.preco:,.2f}".replace('.', '#').replace(',', '.').replace('#', ',')
                    tabela_semanas.insert('', 'end', values=(nome_imovel, semana_adquirida.numero, semana_adquirida.periodo, valor_formatado))
                tabela_semanas.pack(pady=10, padx=10, fill="both", expand=True)
            else:
                tk.Label(frame_perfil, text="Você ainda não adquiriu nenhuma semana.", font=("Arial", 12), bg="#f0f0f0", fg="#888888").pack(pady=10)
        else:
            tk.Label(frame_perfil, text="Nenhum usuário logado. Por favor, faça login.", font=("Arial", 12), bg="#f0f0f0", fg="red").pack(pady=20)


        btn_voltar = tk.Button(frame_perfil, text="Voltar", command=lambda: self.mostrar_tela("tela_principal"),
                               font=("Arial", 12), bg="#607D8B", fg="white", relief="raised", bd=3)
        btn_voltar.pack(pady=20)

    # Função auxiliar para atualizar o conteúdo do perfil
    def atualizar_tela_perfil(self):
        # Chama configurar_tela_perfil novamente para reconstruir o conteúdo
        self.configurar_tela_perfil()
        # Garante que a tela esteja visível
        self.mostrar_tela("tela_perfil")

    def configurar_tela_investimento(self):
        tela_investimento = self.telas["tela_investimento"]
        frame_investimento = tk.Frame(tela_investimento, bg="#f0f0f0", padx=30, pady=30, relief="groove", bd=2)
        frame_investimento.place(relx=0.5, rely=0.5, anchor="center")

        titulo = tk.Label(frame_investimento, text="Escolha o Empreendimento", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333333")
        titulo.pack(pady=20)

        # Botão para Imóvel 1 (ZenithPlace)
        btn_imovel_zenith = tk.Button(frame_investimento, text=f"Imóvel - {banco_dados_simulado['imoveis']['ZenithPlace'].nome}", width=35, height=2,
                                     command=lambda: self.mostrar_tela("tela_imovel1"), # Vai para tela_imovel1 para descrição de ZenithPlace
                                     font=("Arial", 14), bg="#009688", fg="white", relief="raised", bd=3)
        btn_imovel_zenith.pack(pady=10, padx=20)

        # Botão para Imóvel Pastelzinho de Chocolate
        btn_imovel_pastelzinho = tk.Button(frame_investimento, text=f"Imóvel - {banco_dados_simulado['imoveis']['PASTELZINHO DE CHOCOLATE'].nome}", width=35, height=2,
                                     command=lambda: self.mostrar_tela("tela_listar_imovel1"), # Vai direto para a lista de semanas de Pastelzinho
                                     font=("Arial", 14), bg="#FF5722", fg="white", relief="raised", bd=3)
        btn_imovel_pastelzinho.pack(pady=10, padx=20)

        # Botão para Imóvel 2 (Topázio Imperial Hotel)
        btn_imovel_topazio = tk.Button(frame_investimento, text=f"Imóvel - {banco_dados_simulado['imoveis']['Topázio Imperial Hotel'].nome}", width=35, height=2,
                                      command=lambda: self.mostrar_tela("tela_imovel2"), # Vai para tela_imovel2 para descrição de Topázio
                                      font=("Arial", 14), bg="#795548", fg="white", relief="raised", bd=3)
        btn_imovel_topazio.pack(pady=10, padx=20)


        btn_voltar = tk.Button(frame_investimento, text="Voltar", command=lambda: self.mostrar_tela("tela_principal"),
                               font=("Arial", 12), bg="#607D8B", fg="white", relief="raised", bd=3)
        btn_voltar.pack(pady=30)

    def configurar_tela_imovel1(self): # Esta é a tela de descrição de ZenithPlace
        tela_imovel1 = self.telas["tela_imovel1"]
        # Limpa widgets existentes para evitar duplicação ao reconfigurar a tela
        for widget in tela_imovel1.winfo_children():
            widget.destroy()

        frame_imovel1 = tk.Frame(tela_imovel1, bg="#f0f0f0", padx=30, pady=30, relief="groove", bd=2)
        frame_imovel1.place(relx=0.5, rely=0.5, anchor="center")

        imovel = banco_dados_simulado["imoveis"]["ZenithPlace"]

        titulo = tk.Label(frame_imovel1, text=imovel.nome, font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333333")
        titulo.pack(pady=15)

        tk.Label(frame_imovel1, text=f"Localização: {imovel.localizacao}", font=("Arial", 12), bg="#f0f0f0").pack(pady=2)
        tk.Label(frame_imovel1, text=f"Preço Total: R${imovel.preco_total:,.2f}".replace('.', '#').replace(',', '.').replace('#', ','), font=("Arial", 12), bg="#f0f0f0").pack(pady=2)
        tk.Label(frame_imovel1, text=f"Quartos: {imovel.quartos} | Banheiros: {imovel.banheiros}", font=("Arial", 12), bg="#f0f0f0").pack(pady=2)
        tk.Label(frame_imovel1, text=f"Área: {imovel.area} | Avaliação: {imovel.avaliacao}", font=("Arial", 12), bg="#f0f0f0").pack(pady=2)

        descricao = tk.Label(frame_imovel1, text="Descrição detalhada do Imóvel ZenithPlace: Um oásis urbano com vistas deslumbrantes e amenidades de luxo. Perfeito para quem busca conforto e exclusividade.",
                             justify="center", wraplength=400, font=("Arial", 11, "italic"), bg="#f0f0f0", fg="#555555")
        descricao.pack(pady=20, padx=20)

        btn_listar = tk.Button(frame_imovel1, text="Listar Semanas Disponíveis",
                               command=lambda: self.mostrar_tela("tela_listar_imovel_zenith"), # Vai para a nova tela de listagem de Zenith
                               font=("Arial", 14), bg="#00796B", fg="white", relief="raised", bd=3)
        btn_listar.pack(pady=20)

        btn_voltar = tk.Button(frame_imovel1, text="Voltar", command=lambda: self.mostrar_tela("tela_investimento"),
                               font=("Arial", 12), bg="#607D8B", fg="white", relief="raised", bd=3)
        btn_voltar.pack(pady=10)

    def configurar_tela_imovel2(self): # Esta é a tela de descrição de Topázio Imperial Hotel
        tela_imovel2 = self.telas["tela_imovel2"]
        # Limpa widgets existentes para evitar duplicação ao reconfigurar a tela
        for widget in tela_imovel2.winfo_children():
            widget.destroy()

        frame_imovel2 = tk.Frame(tela_imovel2, bg="#f0f0f0", padx=30, pady=30, relief="groove", bd=2)
        frame_imovel2.place(relx=0.5, rely=0.5, anchor="center")

        imovel = banco_dados_simulado["imoveis"]["Topázio Imperial Hotel"]

        titulo = tk.Label(frame_imovel2, text=imovel.nome, font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333333")
        titulo.pack(pady=15)

        tk.Label(frame_imovel2, text=f"Localização: {imovel.localizacao}", font=("Arial", 12), bg="#f0f0f0").pack(pady=2)
        tk.Label(frame_imovel2, text=f"Preço Total: R${imovel.preco_total:,.2f}".replace('.', '#').replace(',', '.').replace('#', ','), font=("Arial", 12), bg="#f0f0f0").pack(pady=2)
        tk.Label(frame_imovel2, text=f"Quartos: {imovel.quartos} | Banheiros: {imovel.banheiros}", font=("Arial", 12), bg="#f0f0f0").pack(pady=2)
        tk.Label(frame_imovel2, text=f"Área: {imovel.area} | Avaliação: {imovel.avaliacao}", font=("Arial", 12), bg="#f0f0f0").pack(pady=2)

        descricao = tk.Label(frame_imovel2, text="Descrição do Topázio Imperial Hotel: Um refúgio à beira-mar com serviço impecável e comodidades de cinco estrelas. Ideal para férias inesquecíveis.",
                             justify="center", wraplength=400, font=("Arial", 11, "italic"), bg="#f0f0f0", fg="#555555")
        descricao.pack(pady=20, padx=20)

        btn_listar = tk.Button(frame_imovel2, text="Listar Semanas Disponíveis",
                               command=lambda: self.mostrar_tela("tela_listar_imovel2"),
                               font=("Arial", 14), bg="#5D4037", fg="white", relief="raised", bd=3)
        btn_listar.pack(pady=20)

        btn_voltar = tk.Button(frame_imovel2, text="Voltar", command=lambda: self.mostrar_tela("tela_investimento"),
                               font=("Arial", 12), bg="#607D8B", fg="white", relief="raised", bd=3)
        btn_voltar.pack(pady=10)

    def configurar_tela_listar_imovel1(self): # Semanas do PASTELZINHO DE CHOCOLATE
        tela_listar = self.telas["tela_listar_imovel1"]
        for widget in tela_listar.winfo_children(): # Limpa widgets antigos
            widget.destroy()

        frame_listar = tk.Frame(tela_listar, pady=20, bg="#f0f0f0")
        frame_listar.pack(fill="both", expand=True)

        imovel_obj = banco_dados_simulado["imoveis"]["PASTELZINHO DE CHOCOLATE"]

        titulo = tk.Label(frame_listar, text=f"Semanas Disponíveis - {imovel_obj.nome}",
                          font=("Arial", 16, "bold"), fg="#333333", bg="#f0f0f0")
        titulo.pack(pady=10)

        colunas = ('semana', 'periodo', 'valor', 'status')
        tabela = ttk.Treeview(frame_listar, columns=colunas, show='headings', height=15)
        tabela.heading('semana', text='Semana Nº')
        tabela.heading('periodo', text='Período')
        tabela.heading('valor', text='Valor da Cota (R$)')
        tabela.heading('status', text='Status')

        tabela.column('semana', width=80, anchor='center')
        tabela.column('periodo', width=150, anchor='center')
        tabela.column('valor', width=120, anchor='center')
        tabela.column('status', width=120, anchor='center')

        self.atualizar_tabela_semanas(tabela, imovel_obj)

        tabela.pack(pady=10, padx=20, fill="both", expand=True)

        btn_comprar = tk.Button(frame_listar, text="Comprar Semana Selecionada",
                                command=lambda: self.comprar_semana(tabela, imovel_obj),
                                font=("Arial", 12), bg="#FFA000", fg="white", relief="raised", bd=3)
        btn_comprar.pack(pady=10)

        btn_voltar = tk.Button(frame_listar, text="Voltar", command=lambda: self.mostrar_tela("tela_investimento"),
                               font=("Arial", 12), bg="#607D8B", fg="white", relief="raised", bd=3)
        btn_voltar.pack(pady=10)

    def configurar_tela_listar_imovel2(self): # Semanas do Topázio Imperial Hotel
        tela_listar = self.telas["tela_listar_imovel2"]
        for widget in tela_listar.winfo_children(): # Limpa widgets antigos
            widget.destroy()

        frame_listar = tk.Frame(tela_listar, pady=20, bg="#f0f0f0")
        frame_listar.pack(fill="both", expand=True)

        imovel_obj = banco_dados_simulado["imoveis"]["Topázio Imperial Hotel"]

        titulo = tk.Label(frame_listar, text=f"Semanas Disponíveis - {imovel_obj.nome}",
                          font=("Arial", 16, "bold"), fg="#333333", bg="#f0f0f0")
        titulo.pack(pady=10)

        colunas = ('semana', 'periodo', 'valor', 'status')
        tabela = ttk.Treeview(frame_listar, columns=colunas, show='headings', height=15)
        tabela.heading('semana', text='Semana Nº')
        tabela.heading('periodo', text='Período')
        tabela.heading('valor', text='Valor da Cota (R$)')
        tabela.heading('status', text='Status')

        tabela.column('semana', width=80, anchor='center')
        tabela.column('periodo', width=150, anchor='center')
        tabela.column('valor', width=120, anchor='center')
        tabela.column('status', width=120, anchor='center')

        self.atualizar_tabela_semanas(tabela, imovel_obj)

        tabela.pack(pady=10, padx=20, fill="both", expand=True)

        btn_comprar = tk.Button(frame_listar, text="Comprar Semana Selecionada",
                                command=lambda: self.comprar_semana(tabela, imovel_obj),
                                font=("Arial", 12), bg="#FFA000", fg="white", relief="raised", bd=3)
        btn_comprar.pack(pady=10)

        btn_voltar = tk.Button(frame_listar, text="Voltar", command=lambda: self.mostrar_tela("tela_imovel2"),
                               font=("Arial", 12), bg="#607D8B", fg="white", relief="raised", bd=3)
        btn_voltar.pack(pady=10)

    def configurar_tela_listar_imovel_zenith(self): # Nova tela para ZenithPlace
        tela_listar = self.telas["tela_listar_imovel_zenith"]
        for widget in tela_listar.winfo_children():
            widget.destroy()

        frame_listar = tk.Frame(tela_listar, pady=20, bg="#f0f0f0")
        frame_listar.pack(fill="both", expand=True)

        imovel_obj = banco_dados_simulado["imoveis"]["ZenithPlace"]

        titulo = tk.Label(frame_listar, text=f"Semanas Disponíveis - {imovel_obj.nome}",
                          font=("Arial", 16, "bold"), fg="#333333", bg="#f0f0f0")
        titulo.pack(pady=10)

        colunas = ('semana', 'periodo', 'valor', 'status')
        tabela = ttk.Treeview(frame_listar, columns=colunas, show='headings', height=15)
        tabela.heading('semana', text='Semana Nº')
        tabela.heading('periodo', text='Período')
        tabela.heading('valor', text='Valor da Cota (R$)')
        tabela.heading('status', text='Status')

        tabela.column('semana', width=80, anchor='center')
        tabela.column('periodo', width=150, anchor='center')
        tabela.column('valor', width=120, anchor='center')
        tabela.column('status', width=120, anchor='center')

        self.atualizar_tabela_semanas(tabela, imovel_obj)

        tabela.pack(pady=10, padx=20, fill="both", expand=True)

        btn_comprar = tk.Button(frame_listar, text="Comprar Semana Selecionada",
                                command=lambda: self.comprar_semana(tabela, imovel_obj),
                                font=("Arial", 12), bg="#FFA000", fg="white", relief="raised", bd=3)
        btn_comprar.pack(pady=10)

        btn_voltar = tk.Button(frame_listar, text="Voltar", command=lambda: self.mostrar_tela("tela_imovel1"),
                               font=("Arial", 12), bg="#607D8B", fg="white", relief="raised", bd=3)
        btn_voltar.pack(pady=10)

    # Função genérica para atualizar as tabelas de semanas
    def atualizar_tabela_semanas(self, tabela_widget, imovel_obj):
        for item in tabela_widget.get_children():
            tabela_widget.delete(item)

        for semana in imovel_obj.semanas:
            status_text = 'Disponível' if semana.dono is None else f'Ocupada por {semana.dono.nome}'
            valor_formatado = f"{semana.preco:,.2f}".replace('.', '#').replace(',', '.').replace('#', ',')
            tabela_widget.insert('', 'end', values=(semana.numero, semana.periodo, valor_formatado, status_text))

    def comprar_semana(self, tabela_atual, imovel_selecionado):
        if not self.usuario_logado:
            messagebox.showwarning("Atenção", "Você precisa estar logado para comprar uma semana.")
            self.mostrar_tela("tela_login")
            return

        selecionado = tabela_atual.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Por favor, selecione uma semana para comprar.")
            return

        item_id = selecionado[0]
        # Obter o número da semana da primeira coluna do item selecionado
        semana_numero_selecionado = tabela_atual.item(item_id, 'values')[0]

        semana_encontrada = None
        for semana in imovel_selecionado.semanas:
            if semana.numero == semana_numero_selecionado:
                semana_encontrada = semana
                break

        if semana_encontrada is None:
            messagebox.showerror("Erro", "Semana não encontrada. Tente novamente.")
            return

        if semana_encontrada.dono is not None:
            messagebox.showerror("Erro", f"A Semana {semana_encontrada.numero} já está ocupada por {semana_encontrada.dono.nome}.")
            return

        semana_encontrada.dono = self.usuario_logado
        self.usuario_logado.semanas.append(semana_encontrada)
        messagebox.showinfo("Sucesso",
                             f"Parabéns! A Semana {semana_encontrada.numero} do imóvel '{imovel_selecionado.nome}' "
                             f"foi adquirida por {self.usuario_logado.nome}!")

        # Re-atualiza a tabela para refletir a compra
        self.atualizar_tabela_semanas(tabela_atual, imovel_selecionado)


    def atualizar_cadastro(self):
        # Este método está presente no seu código original, mas não tem funcionalidade implementada.
        # Pode ser usado para futura implementação de atualização de dados de perfil.
        pass

    def saiba_mais(self):
        messagebox.showinfo("O que é Investimento Fracionado?",
        "Acredita que ter um imóvel de luxo está fora do seu alcance? Pense novamente!\n\n"
        "O investimento fracionado oferece a você a oportunidade de ser proprietário de um pedacinho do paraíso. "
        "São 52 semanas no ano, e sua fatia te dá o direito de uso ou de locação.\n\n"
        "Quer usar sua semana para relaxar? À vontade! Quer rentabilizar? "
        "Alugue sua semana de forma prática e segura, transformando seu investimento em uma fonte de renda.\n\n"
        "É a porta de entrada para um mercado exclusivo, com a flexibilidade e a rentabilidade que você sempre buscou.")

if __name__ == "__main__":
    root = tk.Tk()
    app = Sistemainvestimento(root)
    root.mainloop()
