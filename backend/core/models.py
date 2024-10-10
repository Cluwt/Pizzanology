from django.contrib.auth.models import AbstractUser
from django.db import models

# O arquivo core/models.py deve conter os seguintes modelos:

# Usuário: Armazena os funcionários da pizzaria.
# Cliente: Armazena os dados dos clientes que fazem pedidos.
# Pizza: Armazena as pizzas disponíveis no menu da pizzaria.
# Pedido: Armazena os pedidos dos clientes, relacionando os clientes, funcionários e as pizzas pedidas.
# Pagamento: Armazena as informações sobre o pagamento dos pedidos, como método e status.

#----------------------------------------------------------------------------#

# Modelo de Usuário (Funcionários e Administrador)
class Usuario(AbstractUser):
    CARGOS = [
        ('admin', 'Administrador'),  # Dono da empresa
        ('atendente', 'Atendente'),  # Funcionário que lida com clientes
        ('caixa', 'Caixa'),          # Funcionário que gerencia pagamentos
    ]

    # Indica se o usuário é o dono da empresa
    dono_empresa = models.BooleanField(default=False)

    # Cargo do funcionário
    cargo = models.CharField(max_length=20, choices=CARGOS, default='atendente')

    # Adicionando related_name para evitar conflitos com o modelo auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuario_set',  # Evita conflito com auth.User.groups
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuario_permissions',  # Evita conflito com auth.User.user_permissions
        blank=True,
    )

    # Representação do objeto
    def __str__(self):
        return f"{self.username} ({self.get_cargo_display()})"

#----------------------------------------------------------------------------#

# Modelo de Cliente
# Este modelo armazena informações dos clientes que fazem pedidos na pizzaria
class Cliente(models.Model):
    # Nome completo do cliente
    nome = models.CharField(max_length=100)

    # Telefone de contato do cliente
    telefone = models.CharField(max_length=20)

    # E-mail do cliente (opcional)
    email = models.EmailField(blank=True, null=True)

    # Endereço do cliente (pode ser nulo se for retirada no local)
    endereco = models.TextField(blank=True, null=True)

    # Representação do cliente no Django admin e no shell
    def __str__(self):
        return self.nome  # Retorna o nome do cliente ao exibir o objeto

#----------------------------------------------------------------------------#

# Modelo de Pizza
# Este modelo armazena informações sobre as pizzas disponíveis no menu da pizzaria
class Pizza(models.Model):
    # Nome da pizza
    nome = models.CharField(max_length=100)

    # Descrição da pizza (por exemplo, os ingredientes principais)
    descricao = models.TextField(blank=True, null=True)

    # Preço da pizza
    preco = models.DecimalField(max_digits=6, decimal_places=2)

    # Indica se a pizza está disponível para pedidos
    disponivel = models.BooleanField(default=True)

    # Representação da pizza no Django admin e no shell
    def __str__(self):
        return self.nome  # Retorna o nome da pizza ao exibir o objeto

#--------------------------------------------------------------------------------#

# Modelo de Pedido
# Este modelo armazena informações sobre os pedidos realizados pelos clientes
class Pedido(models.Model):
    # Cliente que fez o pedido (relacionado ao modelo de Cliente)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    # Funcionário responsável pelo pedido (relacionado ao modelo de Usuário)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    # Pizzas pedidas (muitos para muitos: um pedido pode ter várias pizzas, e uma pizza pode estar em vários pedidos)
    pizzas = models.ManyToManyField(Pizza)

    # Valor total do pedido
    total = models.DecimalField(max_digits=6, decimal_places=2)

    # Data e hora em que o pedido foi realizado
    data_pedido = models.DateTimeField(auto_now_add=True)

    # Status do pedido (ex.: "preparando", "entregue")
    STATUS_OPCOES = [
        ('preparando', 'Preparando'),
        ('entregue', 'Entregue'),
        ('cancelado', 'Cancelado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_OPCOES, default='preparando')

    # Representação do pedido no Django admin e no shell
    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente.nome} - Total: {self.total}"

#----------------------------------------------------------------------------#

# Modelo de Pagamento
# Este modelo armazena informações sobre os pagamentos realizados pelos clientes
class Pagamento(models.Model):
    # Relacionamento com o pedido (cada pagamento pertence a um pedido)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)

    # Valor pago pelo cliente
    valor_pago = models.DecimalField(max_digits=6, decimal_places=2)

    # Métodos de pagamento disponíveis (ex.: cartão, dinheiro)
    METODOS_PAGAMENTO = [
        ('dinheiro', 'Dinheiro'),
        ('cartao_credito', 'Cartão de Crédito'),
        ('cartao_debito', 'Cartão de Débito'),
        ('pix', 'PIX'),
    ]
    metodo_pagamento = models.CharField(max_length=20, choices=METODOS_PAGAMENTO)

    # Data e hora em que o pagamento foi realizado
    data_pagamento = models.DateTimeField(auto_now_add=True)

    # Status do pagamento (pago ou pendente)
    STATUS_PAGAMENTO = [
        ('pago', 'Pago'),
        ('pendente', 'Pendente'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_PAGAMENTO, default='pendente')

    # Representação do pagamento no Django admin e no shell
    def __str__(self):
        return f"Pagamento {self.id} - Pedido {self.pedido.id} - Status: {self.status}"
