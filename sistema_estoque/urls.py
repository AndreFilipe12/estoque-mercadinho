from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from controle_estoque.views import (
    home,
    novo_produto,
    editar_produto,
    excluir_produto,
    movimentar_estoque,
    historico_movimentacoes,
)


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'login/',
        LoginView.as_view(
            template_name='controle_estoque/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),

    path(
        '',
        home,
        name='home'
    ),

    path(
        'novo-produto/',
        novo_produto,
        name='novo_produto'
    ),

    path(
        'editar-produto/<int:id>/',
        editar_produto,
        name='editar_produto'
    ),

    path(
        'excluir-produto/<int:id>/',
        excluir_produto,
        name='excluir_produto'
    ),

    path(
        'movimentar-estoque/<int:id>/',
        movimentar_estoque,
        name='movimentar_estoque'
    ),

    path(
        'historico/',
        historico_movimentacoes,
        name='historico_movimentacoes'
    ),
]