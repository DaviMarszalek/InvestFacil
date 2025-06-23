# main.py
import tkinter as tk
from tkinter import ttk, messagebox

# MUDANÇA: Importa os novos módulos e os modelos
import database as db
import validation as val
from models import Usuario, Semana, Imovel

class Sistemainvestimento:
    def __init__(self, root):
        self.root = root
        self.root.title("InvestFacil - Sistema de Investimentos")
        self.root.geometry("800x600")
        self.root.resizable(True, True)

        # MUDANÇA: Inicia o banco de dados
        db.criar_tabelas()
        db.popular_dados_iniciais()

        self.container = tk.Frame(root)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.telas = {}
        self.usuario_logado = None
        self.imovel_selecionado = None # Para saber qual imóvel o usuário está vendo

        self.criar_frames_telas()
        self.configurar_tela_login()
        self.configurar_tela_cadastro()
        self.configurar_tela_principal()
        self.configurar_tela_perfil()
        self.configurar_tela_investimento()
        self.configurar_tela_imovel1() # ZenithPlace (tela de descrição)
        self.configurar_tela_imovel2() # Topázio Imperial Hotel (tela de descrição)
        self.configurar_tela_listar_imovel1() # Semanas de Petra Palace
        self.configurar_tela_listar_imovel2() # Semanas de Topázio Imperial Hotel
        self.configurar_tela_listar_imovel_zenith() # Semanas de ZenithPlace

        # Inicia mostrando a tela de login
        self.mostrar_tela("tela_login")

    def criar_frames_telas(self):
        nomes_telas = [
            "tela_login", "tela_cadastro", "tela_principal", "tela_perfil",
            "tela_investimento", "tela_descricao_imovel", "tela_listar_semanas"
        ]
        for nome_tela in nomes_telas:
            frame = tk.Frame(self.container, bg="#f0f0f0")
            self.telas[nome_tela] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def mostrar_tela(self, nome_tela, **kwargs):
        # MUDANÇA: Lógica para configurar telas dinamicamente
        if nome_tela == "tela_perfil":
            self.configurar_tela_perfil()
        elif nome_tela == "tela_investimento":
            self.configurar_tela_investimento()
        elif nome_tela == "tela_descricao_imovel":
            self.imovel_selecionado = kwargs.get('imovel')
            self.configurar_tela_descricao_imovel()
        elif nome_tela == "tela_listar_semanas":
            self.configurar_tela_listar_semanas()
        
        tela = self.telas[nome_tela]
        tela.tkraise()

    def configurar_tela_login(self):
        # Mantive seu layout original
        tela_login = self.telas["tela_login"]
        frame_login = tk.Frame(tela_login, bg="#f0f0f0", padx=30, pady=30, relief="groove", bd=2)
        frame_login.place(relx=0.5, rely=0.5, anchor="center")
        # ... (código dos labels e entries igual ao seu)
        titulo = tk.Label(frame_login, text="Login", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333333")
        titulo.grid(row=0, column=0, columnspan=2, pady=15)
        tk.Label(frame_login, text="CPF:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, sticky="e", pady=8, padx=5)
        self.cpf_login_entry = tk.Entry(frame_login, width=30, font=("Arial", 12), relief="solid", bd=1)
        self.cpf_login_entry.grid(row=1, column=1, sticky="w", pady=8, padx=5)
        tk.Label(frame_login, text="Senha:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, sticky="e", pady=8, padx=5)
        self.senha_login_entry = tk.Entry(frame_login, width=30, show="*", font=("Arial", 12), relief="solid", bd=1)
        self.senha_login_entry.grid(row=2, column=1, sticky="w", pady=8, padx=5)
        btn_logar = tk.Button(frame_login, text="Entrar", command=self.processar_login, font=("Arial", 13, "bold"), bg="#4CAF50", fg="white", relief="raised", bd=3, width=20)
        btn_logar.grid(row=3, column=0, columnspan=2, pady=15, sticky="ew")
        btn_cadastrar = tk.Button(frame_login, text="Não tem conta? Cadastre-se agora!", command=lambda: self.mostrar_tela("tela_cadastro"), font=("Arial", 10), bg="#2196F3", fg="white", relief="flat", bd=0)
        btn_cadastrar.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

    def processar_login(self):
        cpf = val.formatar_cpf(self.cpf_login_entry.get())
        senha = self.senha_login_entry.get()
        # MUDANÇA: Usa o banco de dados para verificar
        usuario = db.verificar_usuario(cpf, senha)
        if usuario:
            self.usuario_logado = usuario
            messagebox.showinfo("Login", f"Bem-vindo, {self.usuario_logado.nome}!")
            self.mostrar_tela("tela_principal")
        else:
            messagebox.showerror("Erro de Login", "CPF ou senha inválidos.")

    def configurar_tela_cadastro(self):
        # Mantive seu layout original
        tela_cadastro = self.telas["tela_cadastro"]
        frame_cadastro = tk.Frame(tela_cadastro, bg="#f0f0f0", padx=30, pady=30, relief="groove", bd=2)
        frame_cadastro.place(relx=0.5, rely=0.5, anchor="center")
        # ... (código dos labels e entries igual ao seu)
        titulo = tk.Label(frame_cadastro, text="Cadastro de Novo Usuário", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333333")
        titulo.grid(row=0, column=0, columnspan=2, pady=15)
        tk.Label(frame_cadastro, text="Nome Completo:", font=("Arial", 12), bg="#f0f0f0").grid(row=1, column=0, sticky="e", pady=8, padx=5)
        self.nome_cadastro_entry = tk.Entry(frame_cadastro, width=30, font=("Arial", 12), relief="solid", bd=1)
        self.nome_cadastro_entry.grid(row=1, column=1, sticky="w", pady=8, padx=5)
        tk.Label(frame_cadastro, text="CPF:", font=("Arial", 12), bg="#f0f0f0").grid(row=2, column=0, sticky="e", pady=8, padx=5)
        self.cpf_cadastro_entry = tk.Entry(frame_cadastro, width=30, font=("Arial", 12), relief="solid", bd=1)
        self.cpf_cadastro_entry.grid(row=2, column=1, sticky="w", pady=8, padx=5)
        tk.Label(frame_cadastro, text="Contato (Email/Tel):", font=("Arial", 12), bg="#f0f0f0").grid(row=3, column=0, sticky="e", pady=8, padx=5)
        self.contato_cadastro_entry = tk.Entry(frame_cadastro, width=30, font=("Arial", 12), relief="solid", bd=1)
        self.contato_cadastro_entry.grid(row=3, column=1, sticky="w", pady=8, padx=5)
        tk.Label(frame_cadastro, text="Senha:", font=("Arial", 12), bg="#f0f0f0").grid(row=4, column=0, sticky="e", pady=8, padx=5)
        self.senha_cadastro_entry = tk.Entry(frame_cadastro, width=30, show="*", font=("Arial", 12), relief="solid", bd=1)
        self.senha_cadastro_entry.grid(row=4, column=1, sticky="w", pady=8, padx=5)
        btn_cadastrar = tk.Button(frame_cadastro, text="Finalizar Cadastro", command=self.cadastrar_usuario, font=("Arial", 13, "bold"), bg="#FF9800", fg="white", relief="raised", bd=3, width=20)
        btn_cadastrar.grid(row=5, column=0, columnspan=2, pady=15, sticky="ew")
        btn_voltar = tk.Button(frame_cadastro, text="Voltar para Login", command=lambda: self.mostrar_tela("tela_login"), font=("Arial", 10), bg="#607D8B", fg="white", relief="flat", bd=0)
        btn_voltar.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

    def cadastrar_usuario(self):
        nome = self.nome_cadastro_entry.get()
        cpf = self.cpf_cadastro_entry.get()
        contato = self.contato_cadastro_entry.get()
        senha = self.senha_cadastro_entry.get()
        
        # MUDANÇA: Adiciona validação de CPF e usa o banco de dados
        cpf_formatado = val.formatar_cpf(cpf)
        if not val.validar_cpf(cpf_formatado):
            messagebox.showerror("Erro de Cadastro", "CPF inválido.")
            return
        if db.buscar_usuario_por_cpf(cpf_formatado):
            messagebox.showerror("Erro de Cadastro", "CPF já cadastrado.")
            return
        if not all([nome, contato, senha]):
            messagebox.showerror("Erro de Cadastro", "Todos os campos são obrigatórios.")
            return

        if db.adicionar_usuario(nome, cpf_formatado, contato, senha):
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.mostrar_tela("tela_login")
        else:
            messagebox.showerror("Erro", "Não foi possível cadastrar.")

    def configurar_tela_principal(self):
        # Seu layout, sem alterações
        tela_principal = self.telas["tela_principal"]
        frame_principal = tk.Frame(tela_principal, bg="#f0f0f0", padx=50, pady=50)
        frame_principal.place(relx=0.5, rely=0.5, anchor="center")
        titulo = tk.Label(frame_principal, text="INVESTFACIL", font=("Arial", 28, "bold"), bg="#f0f0f0", fg="#4A148C")
        titulo.grid(row=0, column=0, columnspan=3, pady=30)
        btn_perfil = tk.Button(frame_principal, text="Meu Perfil", width=20, height=2, command=lambda: self.mostrar_tela("tela_perfil"), font=("Arial", 14), bg="#00BCD4", fg="white", relief="raised", bd=3)
        btn_perfil.grid(row=1, column=0, pady=15, padx=15)
        btn_investimento = tk.Button(frame_principal, text="Investimentos", width=20, height=2, command=lambda: self.mostrar_tela("tela_investimento"), font=("Arial", 14), bg="#4CAF50", fg="white", relief="raised", bd=3)
        btn_investimento.grid(row=1, column=1, pady=15, padx=15)
        btn_saibamais = tk.Button(frame_principal, text="Saiba Mais", width=20, height=2, command=self.saiba_mais, font=("Arial", 14), bg="#FFC107", fg="#333333", relief="raised", bd=3)
        btn_saibamais.grid(row=1, column=2, pady=15, padx=15)
        btn_sair = tk.Button(frame_principal, text="Sair", command=self.sair, font=("Arial", 12), bg="#F44336", fg="white", relief="raised", bd=3, width=15)
        btn_sair.grid(row=2, column=0, columnspan=3, pady=30)
    
    def sair(self):
        self.usuario_logado = None
        self.mostrar_tela('tela_login')

    def configurar_tela_perfil(self):
        # MUDANÇA: Usa banco de dados e adiciona botão de vender
        tela_perfil = self.telas["tela_perfil"]
        for widget in tela_perfil.winfo_children(): widget.destroy()
        
        frame_perfil = tk.Frame(tela_perfil, bg="#f0f0f0", padx=30, pady=30, relief="groove", bd=2)
        frame_perfil.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(frame_perfil, text=f"Nome: {self.usuario_logado.nome}", font=("Arial", 12)).pack()
        tk.Label(frame_perfil, text=f"CPF: {self.usuario_logado.cpf}", font=("Arial", 12)).pack()
        
        tk.Label(frame_perfil, text="\nMinhas Semanas Adquiridas:", font=("Arial", 14, "bold")).pack()
        
        investimentos = db.buscar_investimentos_usuario(self.usuario_logado.id)
        
        colunas = ('imovel', 'semana', 'periodo', 'valor')
        self.tabela_perfil = ttk.Treeview(frame_perfil, columns=colunas, show='headings', height=8)
        for col in colunas: self.tabela_perfil.heading(col, text=col.replace('_', ' ').title())
        
        total_investido = 0
        if investimentos:
            for inv in investimentos:
                self.tabela_perfil.insert('', 'end', values=(inv['imovel_nome'], inv['numero'], inv['periodo'], f"{inv['preco']:.2f}"), iid=inv['semana_id'])
                total_investido += inv['preco']
        self.tabela_perfil.pack(pady=10)
        
        lucro_potencial = total_investido * 0.15
        tk.Label(frame_perfil, text=f"Total Investido: R$ {total_investido:,.2f}").pack()
        tk.Label(frame_perfil, text=f"Lucro Potencial (Estimado): R$ {lucro_potencial:,.2f}").pack()
        
        tk.Button(frame_perfil, text="Vender Semana Selecionada", command=self.vender_semana_selecionada).pack(pady=10)
        tk.Button(frame_perfil, text="Voltar", command=lambda: self.mostrar_tela("tela_principal")).pack()

    def vender_semana_selecionada(self):
        selecionado_id = self.tabela_perfil.focus()
        if not selecionado_id:
            messagebox.showwarning("Atenção", "Selecione um investimento para vender.")
            return
        
        item = self.tabela_perfil.item(selecionado_id)
        imovel_nome, semana_num = item['values'][0], item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"Deseja vender a semana {semana_num} do imóvel {imovel_nome}?"):
            db.vender_semana(int(selecionado_id))
            messagebox.showinfo("Sucesso", "Sua fração foi colocada à venda!")
            self.mostrar_tela("tela_perfil") # Atualiza a tela

    def configurar_tela_investimento(self):
        # MUDANÇA: Busca imóveis do banco de dados dinamicamente
        tela_investimento = self.telas["tela_investimento"]
        for widget in tela_investimento.winfo_children(): widget.destroy()
        
        frame_inv = tk.Frame(tela_investimento, bg="#f0f0f0", padx=30, pady=30, relief="groove", bd=2)
        frame_inv.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(frame_inv, text="Escolha o Empreendimento", font=("Arial", 18, "bold")).pack(pady=20)
        
        imoveis = db.buscar_imoveis()
        for imovel in imoveis:
            btn = tk.Button(frame_inv, text=imovel.nome, width=35, height=2, font=("Arial", 14),
                             command=lambda i=imovel: self.mostrar_tela("tela_descricao_imovel", imovel=i))
            btn.pack(pady=10)
        
        tk.Button(frame_inv, text="Voltar", command=lambda: self.mostrar_tela("tela_principal")).pack(pady=30)
        
    def configurar_tela_descricao_imovel(self):
        # MUDANÇA: Tela genérica para qualquer imóvel
        tela = self.telas["tela_descricao_imovel"]
        for widget in tela.winfo_children(): widget.destroy()
        imovel = self.imovel_selecionado
        
        frame = tk.Frame(tela, bg="#f0f0f0", padx=30, pady=30, relief="groove", bd=2)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        
        tk.Label(frame, text=imovel.nome, font=("Arial", 20, "bold")).pack(pady=15)
        tk.Label(frame, text=f"Localização: {imovel.localizacao}", font=("Arial", 12)).pack(pady=2)
        tk.Label(frame, text=f"Preço Total: R${imovel.preco_total:,.2f}", font=("Arial", 12)).pack(pady=2)
        tk.Label(frame, text=f"Quartos: {imovel.quartos} | Banheiros: {imovel.banheiros}", font=("Arial", 12)).pack(pady=2)
        tk.Label(frame, text=f"Área: {imovel.area} | Avaliação: {imovel.avaliacao}", font=("Arial", 12)).pack(pady=2)
        
        tk.Button(frame, text="Listar Semanas Disponíveis", command=lambda: self.mostrar_tela("tela_listar_semanas")).pack(pady=20)
        tk.Button(frame, text="Voltar", command=lambda: self.mostrar_tela("tela_investimento")).pack(pady=10)

        titulo = tk.Label(frame_investimento, text="Escolha o Empreendimento", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333333")
        titulo.pack(pady=20)

    
        btn_imovel_zenith = tk.Button(frame_investimento, text=f"Imóvel - {banco_dados_simulado['imoveis']['ZenithPlace'].nome}", width=35, height=2,
                                     command=lambda: self.mostrar_tela("tela_imovel1"), 
                                     font=("Arial", 14), bg="#5D4037", fg="white", relief="raised", bd=3)
        btn_imovel_zenith.pack(pady=10, padx=20)

        btn_imovel_petra = tk.Button(frame_investimento, text=f"Imóvel - {banco_dados_simulado['imoveis']['Petra Palace'].nome}", width=35, height=2,
                                     command=lambda: self.mostrar_tela("tela_listar_imovel1"), 
                                     font=("Arial", 14), bg="#5D4037", fg="white", relief="raised", bd=3)
        btn_imovel_petra.pack(pady=10, padx=20)


        btn_imovel_topazio = tk.Button(frame_investimento, text=f"Imóvel - {banco_dados_simulado['imoveis']['Topázio Imperial Hotel'].nome}", width=35, height=2,
                                      command=lambda: self.mostrar_tela("tela_imovel2"), 
                                      font=("Arial", 14), bg="#5D4037", fg="white", relief="raised", bd=3)
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

    def configurar_tela_listar_imovel1(self): 
        tela_listar = self.telas["tela_listar_imovel1"]
        for widget in tela_listar.winfo_children(): # Limpa widgets antigos
            widget.destroy()

        frame_listar = tk.Frame(tela_listar, pady=20, bg="#f0f0f0")
        frame_listar.pack(fill="both", expand=True)

        imovel_obj = banco_dados_simulado["imoveis"]["Petra Palace"]

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
            messagebox.showwarning("Atenção", "Selecione uma semana para comprar.")
            return

        item = self.tabela_semanas.item(selecionado[0], 'values')
        semana_id, status = int(item[0]), item[4]

        if "Disponível" not in status:
            messagebox.showerror("Erro", "Esta semana não está disponível para compra.")
            return

        if messagebox.askyesno("Confirmar", "Deseja confirmar a compra desta semana?"):
            if db.comprar_semana(semana_id, self.usuario_logado.id):
                messagebox.showinfo("Sucesso", "Parabéns! Você adquiriu uma nova fração.")
                self.mostrar_tela("tela_listar_semanas") # Atualiza a tela
            else:
                messagebox.showerror("Erro", "Não foi possível completar a compra. A semana pode ter sido adquirida por outra pessoa.")

    def saiba_mais(self):
        # Sua mensagem original, sem alterações
        messagebox.showinfo("O que é Investimento Fracionado?", "Acredita que ter um imóvel de luxo está fora do seu alcance? Pense novamente!\n\n...")

if __name__ == "__main__":
    root = tk.Tk()
    app = Sistemainvestimento(root)
    root.mainloop()