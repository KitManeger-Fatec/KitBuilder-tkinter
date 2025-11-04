import customtkinter as ctk
from PIL import Image
from app.utils.logger_config import get_logger
from app.config.themes.colors import COLORS
from app.config.themes.fonts import FONTS
from app.controllers.cadastroView_controller import CadastroViewController
from app.models.funcionarios import Funcionario
from app.database import SessionLocal
from sqlalchemy import select
from CTkListbox import CTkListbox
from app.utils.session_manager import SessionManager

import os

logger = get_logger(__name__)

class CadastroView(ctk.CTkFrame):
    """
    CadastroView como frame que ocupa o root, com layout de duas colunas (imagem/formulario).
    """


    def __init__(self, parent, controller=None, router=None):
        logger.debug("Inicializando CadastroView (CustomTkinter)")
        super().__init__(parent, fg_color=COLORS["bg"])
        self.controller = controller  # <-- Aqui você guarda o controller
        self.router = router
        # No início da CadastroView
        self.chefes_disponiveis = []
        self.chefes_selecionados = []



        # Configura grid para responsividade
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1, uniform="a")
        self.grid_columnconfigure(1, weight=1, uniform="a")

        self._setup_ui()
        logger.debug("CadastroView inicializada com sucesso")

        # Carrega chefes automaticamente
        self.carregar_chefes()

    def _setup_ui(self):
        logger.debug("Configurando interface do CadastroView")
        
        # Container central que segura todo o conteúdo
        container = ctk.CTkFrame(self, fg_color=COLORS["panel"], corner_radius=14)
        container.grid(row=0, column=0, columnspan=2, padx=40, pady=60, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        # Left: área de imagem / branding (Idêntica à LoginView)
        left = ctk.CTkFrame(container, fg_color=COLORS["panel"], corner_radius=10)
        left.grid(row=0, column=0, sticky="nsew", padx=(24,12), pady=24)
        left.grid_rowconfigure(0, weight=1)
        left.grid_columnconfigure(0, weight=1)

        try:
            # Tenta carregar a imagem, se não conseguir, mostra placeholder
            img = Image.open("assets/images/Logo.jpg")
            max_size = (560, 560)
            img.thumbnail(max_size, Image.LANCZOS)
            self.logo_image = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            ctk.CTkLabel(left, image=self.logo_image, text="").grid(row=0, column=0, sticky="n", padx=12, pady=20)
            logger.debug("Logo carregada com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar logo: {e}")
            placeholder = ctk.CTkFrame(left, fg_color=COLORS["bg"], corner_radius=8, height=300, width=400)
            placeholder.grid(row=0, column=0, padx=12, pady=12)
            ctk.CTkLabel(placeholder, text="LOGO", font=FONTS["title"], text_color=COLORS["fg"]).place(relx=0.5, rely=0.5, anchor="center")
            logger.debug("Placeholder de logo criado")

        ctk.CTkLabel(left, text=os.getenv("BRAND_NAME"), font=FONTS["title"], text_color=COLORS["fg"]).grid(row=1, column=0, pady=(6,2))
        ctk.CTkLabel(left, text="Cadastro de Novo Funcionário", font=FONTS["text"], text_color=COLORS["muted"]).grid(row=2, column=0, pady=(0,16))

        
        # Container para as caixas
        frame_chefes = ctk.CTkFrame(left, fg_color=COLORS["panel"], corner_radius=10)
        frame_chefes.grid(row=3, column=0, pady=(12, 12), sticky="nsew")
        frame_chefes.grid_columnconfigure(0, weight=1)
        frame_chefes.grid_columnconfigure(2, weight=1)

        # Caixa de chefes disponíveis

        ctk.CTkLabel(frame_chefes, text="Chefes Disponíveis", font=FONTS["text"], text_color=COLORS["fg"]).grid(row=0, column=0, padx=12, pady=(12,0))
        self.textbox_disponiveis = CTkListbox(frame_chefes, width=200, height=120)
        self.textbox_disponiveis.grid(row=1, column=0, padx=(12,6), pady=6)
        self.chefes_disponiveis = []
        self.chefes_selecionados = []
        self.carregar_chefes()

        # Botão ADD
        self.btn_add_chefe = ctk.CTkButton(frame_chefes, text="Add →", width=60, command=self.adicionar_chefes_selecionados)
        self.btn_add_chefe.grid(row=1, column=1, padx=6, pady=6)

        # Caixa de chefes selecionados
        ctk.CTkLabel(frame_chefes, text="Chefes Selecionados", font=FONTS["text"], text_color=COLORS["fg"]).grid(row=0, column=2, padx=12, pady=(12,0))
        self.textbox_selecionados = ctk.CTkTextbox(frame_chefes, width=200, height=120)
        self.textbox_selecionados.grid(row=1, column=2, padx=(6,12), pady=6)

        # Right: formulário de cadastro (com scroll)
        right = ctk.CTkFrame(container, fg_color=COLORS["bg"], corner_radius=10)
        right.grid(row=0, column=1, sticky="nsew", padx=(12,24), pady=24)
        right.grid_rowconfigure(0, weight=1)
        right.grid_columnconfigure(0, weight=1)

        # Holder do formulário (agora é um scrollable frame)
        form_holder = ctk.CTkScrollableFrame(right, fg_color=COLORS["panel"], corner_radius=5)
        form_holder.grid(row=0, column=0, sticky="nsew", padx=40, pady=40)
        form_holder.grid_columnconfigure(0, weight=1)

        # Títulos do formulário
        ctk.CTkLabel(form_holder, text="Cadastro de Colaborador", font=FONTS["subtitle2"], text_color=COLORS["fg"]).grid(row=0, column=0, pady=(22,6), sticky="n")

        row = 1
        
        # --- Campo Nome Completo ---
        ctk.CTkLabel(form_holder, text="Nome Completo", font=FONTS["text"], text_color=COLORS["muted"]).grid(row=row, column=0, sticky="w", padx=24, pady=(8,0)); row+=1
        self.nome_entry = ctk.CTkEntry(form_holder, width=340)
        self.nome_entry.grid(row=row, column=0, pady=(6,12), padx=20); row+=1

        # --- Campo CPF ---
        ctk.CTkLabel(form_holder, text="CPF", font=FONTS["text"], text_color=COLORS["muted"]).grid(row=row, column=0, sticky="w", padx=24, pady=(8,0)); row+=1
        self.cpf_entry = ctk.CTkEntry(form_holder, width=340)
        self.cpf_entry.bind("<KeyRelease>", self.aplicar_mascara_cpf)
        self.cpf_entry.grid(row=row, column=0, pady=(6,12), padx=20); row+=1


        # --- Campo Usuário (Login) ---
        ctk.CTkLabel(form_holder, text="Usuário (Login)", font=FONTS["text"], text_color=COLORS["muted"]).grid(row=row, column=0, sticky="w", padx=24, pady=(8,0)); row+=1
        self.usuario_entry = ctk.CTkEntry(form_holder, width=340)
        self.usuario_entry.grid(row=row, column=0, pady=(6,12), padx=20); row+=1
        
        # --- Campo E-mail ---
        ctk.CTkLabel(form_holder, text="E-mail", font=FONTS["text"], text_color=COLORS["muted"]).grid(row=row, column=0, sticky="w", padx=24, pady=(8,0)); row+=1
        self.email_entry = ctk.CTkEntry(form_holder, width=340)
        self.email_entry.grid(row=row, column=0, pady=(6,12), padx=20); row+=1
        
        # --- Campo Senha ---
        ctk.CTkLabel(form_holder, text="Senha", font=FONTS["text"], text_color=COLORS["muted"]).grid(row=row, column=0, sticky="w", padx=24, pady=(8,0)); row+=1
        self.senha_entry = ctk.CTkEntry(form_holder, show="*", width=340)
        self.senha_entry.grid(row=row, column=0, pady=(6,12)); row+=1
        
        # --- Campo Confirmação de Senha ---
        ctk.CTkLabel(form_holder, text="Confirmar Senha", font=FONTS["text"], text_color=COLORS["muted"]).grid(row=row, column=0, sticky="w", padx=24, pady=(8,0)); row+=1
        self.confirmar_senha_entry = ctk.CTkEntry(form_holder, show="*", width=340)
        self.confirmar_senha_entry.grid(row=row, column=0, pady=(6,12)); row+=1

        # --- Campo Cargo ---
        ctk.CTkLabel(form_holder, text="Cargo", font=FONTS["text"], text_color=COLORS["muted"]).grid(row=row, column=0, sticky="w", padx=24, pady=(8,0)); row+=1
        # Assumindo que você terá uma lista de cargos
        cargos = self._carregar_cargos()
        if "Outro cargo" not in cargos:
            cargos.append("Outro cargo")
        self.cargo_combobox = ctk.CTkComboBox(
            form_holder, 
            values=cargos, 
            width=340,
            command=self._ao_mudar_cargo  # <- evento para detectar seleção
        )
        self.cargo_combobox.grid(row=row, column=0, pady=(6,12)); row+=1

        # Campo oculto inicialmente, só aparece se escolher "Outro cargo"
        self.novo_cargo_entry = ctk.CTkEntry(form_holder, width=340, placeholder_text="Digite o novo cargo")
        self.novo_cargo_entry.grid(row=row, column=0, pady=(6,12))
        self.novo_cargo_entry.grid_remove()  # <- esconde o campo
        row += 1

        # --- Campo Nível de funcionario  ---
        ctk.CTkLabel(form_holder, text="Nivel do Colaborador", font=FONTS["text"], text_color=COLORS["muted"]).grid(row=row, column=0, sticky="w", padx=24, pady=(8,0)); row+=1
        nivel = self._carregar_nivel()
        self.nivel_combobox = ctk.CTkComboBox(
            form_holder, 
            values=nivel, 
            width=340,
        )
        self.nivel_combobox.grid(row=row, column=0, pady=(6,12)); row+=1

        # Mensagem de erro
        self.msg_label = ctk.CTkLabel(form_holder, text="", font=FONTS["text"], text_color=COLORS["error"])
        self.msg_label.grid(row=row, column=0, pady=(4,6)); row+=1

        # Botão Cadastrar
        self.cadastro_button = ctk.CTkButton(
            form_holder, text="Cadastrar Funcionário",
            command=(lambda: self.ao_clicar_cadastrar()) if self.controller else None,
            fg_color=COLORS["accent"], text_color=COLORS["button_text"],
            font=FONTS["button"], width=340, height=44
        )
        self.cadastro_button.grid(row=row, column=0, pady=(10,10)); row+=1



    def get_dados(self):
        """Coleta todos os dados do formulário."""
        dados = {
            "nome": self.nome_entry.get(),
            "cpf": self.cpf_entry.get(),
            "usuario": self.usuario_entry.get(),
            "email": self.email_entry.get(),
            "senha": self.senha_entry.get(),
            "confirmar_senha": self.confirmar_senha_entry.get(),
            "cargo": self.cargo_combobox.get(),
        }
        logger.debug(f"Dados do formulário de cadastro coletados: {list(dados.keys())}")
        return dados

    def _carregar_cargos(self):
        """Usa o controller para obter cargos únicos do banco."""
        if self.controller:
            try:
                cargos = self.controller.obter_cargos_unicos()
                return cargos if cargos else ["Nenhum cargo encontrado"]
            except Exception as e:
                print(f"Erro ao carregar cargos: {e}")
                return ["Erro ao carregar"]
        return ["Controller não definido"]
    
    def _ao_mudar_cargo(self, valor):
        """Mostra ou esconde o campo de novo cargo."""
        if valor == "Outro cargo":
            self.novo_cargo_entry.grid()  # mostra o campo
        else:
            self.novo_cargo_entry.grid_remove()  # esconde o campo

    def mostrar_erro(self, mensagem):
        logger.warning(f"Exibindo mensagem de erro no cadastro: {mensagem}")
        try:
            self.msg_label.configure(text=mensagem)
        except Exception as e:
            logger.error(f"Erro ao exibir mensagem de erro: {e}")

    def destruir(self):
        logger.debug("Destruindo CadastroView")
        try:
            self.destroy()
        except Exception as e:
            logger.error(f"Erro ao destruir CadastroView: {e}")

    def get_dados(self):
        """Coleta todos os dados do formulário."""
        cargo_selecionado = self.cargo_combobox.get()
        if cargo_selecionado == "Outro cargo":
            cargo = self.novo_cargo_entry.get().strip()
        else:
            cargo = cargo_selecionado

        dados = {
            "nome": self.nome_entry.get(),
            "cpf": self.cpf_entry.get(),
            "usuario": self.usuario_entry.get(),
            "email": self.email_entry.get(),
            "senha": self.senha_entry.get(),
            "confirmar_senha": self.confirmar_senha_entry.get(),
            "cargo": cargo,
        }
        logger.debug(f"Dados do formulário de cadastro coletados: {list(dados.keys())}")
        return dados

    def ao_clicar_cadastrar(self):
        """Envia os dados para o controller exibir."""
        dados = self.get_dados()
        self.controller.exibir_dados_cadastro(dados)


    def carregar_chefes(self):
        """Carrega chefes únicos (sem repetição)."""
        self.textbox_disponiveis.delete(0, "end")
        nomes_unicos = set()

        try:
            with SessionLocal() as session:
                stmt = select(Funcionario).order_by(Funcionario.nome_funcionario)
                chefes = session.scalars(stmt).all()

                for chefe in chefes:
                    nome = chefe.nome_funcionario.strip()
                    cargo = chefe.cargo_funcionario or "Sem cargo"
                    if nome not in nomes_unicos:
                        self.textbox_disponiveis.insert("end", f"{nome} - {cargo}")
                        nomes_unicos.add(nome)
            logger.info("Chefes carregados com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar chefes: {e}")

    def adicionar_chefes_selecionados(self):
            """Adiciona o chefe selecionado à lista da direita."""
            selecionado = self.textbox_disponiveis.get()  # retorna apenas 1 item
            if not selecionado:
                logger.warning("Nenhum chefe selecionado.")
                return

            if selecionado not in self.chefes_selecionados:
                self.chefes_selecionados.append(selecionado)
                self.textbox_selecionados.insert("end", selecionado + "\n")
                logger.info(f"Chefe adicionado: {selecionado}")
            else:
                logger.debug(f"Chefe '{selecionado}' já está na lista de selecionados.")

    def _carregar_nivel(self):
        """Carrega o nível atual do funcionário e gera lista de níveis até 1."""
        try:
            # ID do funcionário logado ou em edição
            id_funcionario = SessionManager.get_usuario_id()

            niveis = CadastroViewController.obter_nivel(id_funcionario)

            if not niveis:
                niveis = [1]  # fallback para evitar lista vazia

            logger.debug(f"Níveis carregados: {niveis}")
            return [str(n) for n in niveis]  # converte em texto para CTkComboBox
        except Exception as e:
            logger.error(f"Erro ao carregar níveis: {e}")
            return ["1"]

    def ao_clicar_cadastrar(self):
        """Valida os campos antes de enviar para o controller."""
        dados = self.get_dados()
        faltando = []

        # --- validação de preenchimento ---
        if not dados["nome"].strip():
            faltando.append("Nome completo")
        if not dados["cpf"].strip():
            faltando.append("CPF")
        # --- validação do usuário ---
        if not dados["usuario"].strip():
            faltando.append("Usuário (Login)")
        else:
            # verifica se já existe no banco
            if self.controller.usuario_existe(dados["usuario"]):
                self.mostrar_erro(f"Usuário '{dados['usuario']}' já existe. Escolha outro.")
                self.usuario_entry.focus()
                return
        if not dados["email"].strip():
            faltando.append("E-mail")
        if not dados["senha"].strip():
            faltando.append("Senha")
        if not dados["confirmar_senha"].strip():
            faltando.append("Confirmação de senha")

        # --- validação do cargo ---
        if not dados["cargo"].strip() or dados["cargo"] in ["Nenhum cargo encontrado", "Erro ao carregar"]:
            faltando.append("Cargo")

        # --- validação do nível ---
        nivel_selecionado = self.nivel_combobox.get()
        if nivel_selecionado in ["", "Escolher Nível"]:
            faltando.append("Nível do colaborador")

        # --- validação das senhas ---
        if dados["senha"] and dados["confirmar_senha"]:
            if dados["senha"] != dados["confirmar_senha"]:
                self.mostrar_erro("As senhas não coincidem.")
                return

        # --- caso haja campos faltando ---
        if faltando:
            msg = "Preencha os seguintes campos obrigatórios:\n- " + "\n- ".join(faltando)
            self.mostrar_erro(msg)
            return

        # --- Tudo certo, salvar ---
        dados["nivel"] = int(self.nivel_combobox.get())  # adiciona nível ao dict

        sucesso = self.controller.salvar_funcionario(dados, self.chefes_selecionados)

        if sucesso:
            self.mostrar_erro("Funcionário cadastrado com sucesso!")  # ou criar cor verde
            self.controller.limpar_formulario(self)
        else:
            self.mostrar_erro("Erro ao salvar funcionário no banco.")


    def aplicar_mascara_cpf(self, event=None):
        valor = self.cpf_entry.get()
        pos = self.cpf_entry.index("insert")

        # Remove tudo que não for número
        numeros = ''.join(filter(str.isdigit, valor))

        # Limita a 11 dígitos
        numeros = numeros[:11]

        # Aplica a máscara
        cpf_formatado = ''
        partes = []

        if len(numeros) > 0:
            partes.append(numeros[:3])
        if len(numeros) >= 4:
            partes.append(numeros[3:6])
        if len(numeros) >= 7:
            partes.append(numeros[6:9])
        if len(numeros) >= 10:
            partes.append(numeros[9:11])

        if len(partes) >= 4:
            cpf_formatado = '.'.join(partes[:3]) + '-' + partes[3]
        else:
            cpf_formatado = '.'.join(partes)

        # Calcula a nova posição do cursor
        new_pos = pos

        # Ajusta o cursor se um ponto ou traço foi inserido antes do cursor
        if event and event.keysym.lower() != "backspace":
            count = 0
            for i, c in enumerate(cpf_formatado):
                if i >= new_pos:
                    break
                if not c.isdigit():
                    count += 1
            new_pos += count

        # Atualiza o entry
        self.cpf_entry.delete(0, "end")
        self.cpf_entry.insert(0, cpf_formatado)
        self.cpf_entry.icursor(new_pos)

