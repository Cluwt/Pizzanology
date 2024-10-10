from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Modelos e Serializers do Sistema:
from .models import Usuario, Cliente, Pizza, Pedido, Pagamento
from .serializers import UsuarioSerializer, ClienteSerializer, PizzaSerializer, PedidoSerializer, PagamentoSerializer

# Views responsáveis pelo controle do Sistema:

#-------------------------------------------------------------------------------------#

# View responsável por registrar o usuário ao sistema:

@api_view(['POST'])
# Permitir que qualquer pessoa acesse essa rota, sem precisar estar autenticada
@permission_classes([AllowAny])  
def registrar_usuario(request):

    # Capturando os dados da requisição
    username = request.data.get('username')
    password = request.data.get('password')

    # Validar se os campos foram preenchidos
    if not username or not password:
        return Response({"error": "Todos os campos são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

    # Verifica se o nome de usuário já existe
    if User.objects.filter(username=username).exists():
        return Response({"error": "Esse nome de usuário já está em uso."}, status=status.HTTP_400_BAD_REQUEST)

    # Criar o novo usuário
    user = User.objects.create(
        username=username,
        password=make_password(password)  # Hash da senha para segurança
    )

    return Response({"message": "Usuário registrado com sucesso!"}, status=status.HTTP_201_CREATED)

#-----------------------------------------------------------------------#

# View responsável por criar o pedido no Sistema.

@api_view(['POST'])
# Apenas usuários autenticados podem acessar essa rota "IsAuthenticated"
@permission_classes([AllowAny])  
def criar_pedido(request):

    # Extrai os dados do pedido a partir da requisição
    cliente_id = request.data.get('cliente')  # ID do cliente que está fazendo o pedido
    pizzas_ids = request.data.get('pizzas')    # Lista de IDs das pizzas que estão sendo pedidas

    # Verifica se os dados obrigatórios estão presentes
    if not cliente_id or not pizzas_ids:
        return Response({"error": "Cliente e pizzas são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Obtém a instância do cliente pelo ID fornecido
        cliente = Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
        return Response({"error": "Cliente não encontrado."}, status=status.HTTP_404_NOT_FOUND)

    try:
        # Obtém as instâncias das pizzas pelos IDs fornecidos
        pizzas = Pizza.objects.filter(id__in=pizzas_ids)
        if pizzas.count() != len(pizzas_ids):
            return Response({"error": "Uma ou mais pizzas não foram encontradas."}, status=status.HTTP_404_NOT_FOUND)
    except Pizza.DoesNotExist:
        return Response({"error": "Pizzas não encontradas."}, status=status.HTTP_404_NOT_FOUND)

    # Calcula o valor total do pedido somando os preços das pizzas
    total_pedido = sum([pizza.preco for pizza in pizzas])

    # Cria uma instância do pedido
    pedido = Pedido(cliente=cliente, usuario=request.user, total=total_pedido, status='preparando')

    # Salva o pedido no banco de dados (agora o pedido tem um ID)
    pedido.save()

    # Adiciona as pizzas ao pedido (relacionamento muitos-para-muitos)
    pedido.pizzas.set(pizzas)  # Define as pizzas do pedido usando as instâncias fornecidas

    # Serializa o pedido para retornar como resposta
    serializer = PedidoSerializer(pedido)

    # Retorna o pedido criado
    return Response(serializer.data, status=status.HTTP_201_CREATED)

#-----------------------------------------------------------------------#

# View responsável por listar todos os pedidos feitos no Sistema.

@api_view(['GET'])
@permission_classes([AllowAny])
def listar_pedidos(request):

    # Lógica para listar os pedidos (somente usuários autenticados podem acessar)
    pedidos = Pedido.objects.all()
    serializer = PedidoSerializer(pedidos, many=True)
    return Response(serializer.data)

#----------------------------------------------------------------------#

# ViewSets do Sistema:

# Um ViewSet define as operações que podem ser 
# realizadas em um recurso, como listar todos os registros, 
# buscar um registro específico, criar novos registros, atualizar 
# registros existentes e deletar registros.


# ViewSet para o modelo de Usuário
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()  # Busca todos os usuários
    serializer_class = UsuarioSerializer  # Usa o serializer de Usuário

#----------------------------------------------------------------------#


# ViewSet para o modelo de Cliente
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()  # Busca todos os clientes
    serializer_class = ClienteSerializer  # Usa o serializer de Cliente

#----------------------------------------------------------------------#


# ViewSet para o modelo de Pizza
class PizzaViewSet(viewsets.ModelViewSet):
    queryset = Pizza.objects.all()  # Busca todas as pizzas
    serializer_class = PizzaSerializer  # Usa o serializer de Pizza

#----------------------------------------------------------------------#


# ViewSet para o modelo de Pedido
class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()  # Busca todos os pedidos
    serializer_class = PedidoSerializer  # Usa o serializer de Pedido

#----------------------------------------------------------------------#


# ViewSet para o modelo de Pagamento
class PagamentoViewSet(viewsets.ModelViewSet):
    queryset = Pagamento.objects.all()  # Busca todos os pagamentos
    serializer_class = PagamentoSerializer  # Usa o serializer de Pagamento


#----------------------------------------------------------------------#
