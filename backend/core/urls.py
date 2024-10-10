from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsuarioViewSet, ClienteViewSet, PizzaViewSet, PedidoViewSet, PagamentoViewSet, criar_pedido)
from .views import registrar_usuario, listar_pedidos

# Definindo as rotas da API usando o DefaultRouter do DRF
router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet)  # Rota para os usuários
router.register(r'clientes', ClienteViewSet)  # Rota para os clientes
router.register(r'pizzas', PizzaViewSet)  # Rota para as pizzas

router.register(r'pagamentos', PagamentoViewSet)  # Rota para os pagamentos

# Incluindo as rotas do router e rotas personalizadas no urlpatterns
urlpatterns = [

    # Inclui as rotas geradas pelo router
    path('', include(router.urls)),  

    # Páginas com funcionamentos do Sistema:
    path('registrar/', registrar_usuario, name='registrar_usuario'),
    path('pedidos/criar/', criar_pedido, name='criar_pedido'),
    path('pedidos/listar/', listar_pedidos, name='listar_pedidos'),
    
]
