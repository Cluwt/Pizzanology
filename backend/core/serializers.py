from rest_framework import serializers
from .models import Usuario, Cliente, Pizza, Pedido, Pagamento

# Serializers responsáveis por transformar objetos em JSON para conexão do Back-End 
# com o Front-End.

#---------------------------------------------------------------------------------------#

# Serializer para o modelo de Usuário
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'cargo', 'dono_empresa']  # Campos a serem serializados

#---------------------------------------------------------------------------------------#

# Serializer para o modelo de Cliente
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome', 'telefone', 'email', 'endereco']  # Campos a serem serializados

#---------------------------------------------------------------------------------------#

# Serializer para o modelo de Pizza
class PizzaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pizza
        fields = ['id', 'nome', 'descricao', 'preco', 'disponivel']  # Campos a serem serializados        

#---------------------------------------------------------------------------------------#

# Serializer para o modelo de Pedido
class PedidoSerializer(serializers.ModelSerializer):
    # Permite definir os relacionamentos por ID na criação do pedido
    cliente = serializers.PrimaryKeyRelatedField(queryset=Cliente.objects.all())
    pizzas = serializers.PrimaryKeyRelatedField(many=True, queryset=Pizza.objects.all())
    usuario = serializers.PrimaryKeyRelatedField(read_only=True)  # Definido automaticamente como o usuário autenticado

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'usuario', 'pizzas', 'total', 'data_pedido', 'status']
        read_only_fields = ['total', 'data_pedido', 'status', 'usuario']

        
#---------------------------------------------------------------------------------------#

# Serializer para o modelo de Pagamento
class PagamentoSerializer(serializers.ModelSerializer):
    # Relacionamento com o pedido
    pedido = PedidoSerializer(read_only=True)  # Inclui os dados do pedido no pagamento

    class Meta:
        model = Pagamento
        fields = ['id', 'pedido', 'valor_pago', 'metodo_pagamento', 'data_pagamento', 'status']  # Campos a serem serializados