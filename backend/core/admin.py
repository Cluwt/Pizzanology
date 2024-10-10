from django.contrib import admin
from .models import Usuario, Cliente, Pizza, Pedido, Pagamento

# Registrando os modelos para o Django Admin
admin.site.register(Usuario)
admin.site.register(Cliente)
admin.site.register(Pizza)
admin.site.register(Pedido)
admin.site.register(Pagamento)
