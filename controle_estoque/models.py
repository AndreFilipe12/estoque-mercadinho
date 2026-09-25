from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    codigo = models.CharField(max_length=50, unique=True)
    categoria = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=12, decimal_places=4)
    quantidade_estoque = models.IntegerField(default=0)
    estoque_minimo = models.IntegerField(default=0)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome


class MovimentacaoEstoque(models.Model):
    ENTRADA = 'entrada'
    SAIDA = 'saida'

    TIPO_CHOICES = [
        (ENTRADA, 'Entrada'),
        (SAIDA, 'Saída'),
    ]

    produto = models.ForeignKey(
        Produto,
        on_delete=models.CASCADE,
        related_name='movimentacoes'
    )

    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES
    )

    quantidade = models.PositiveIntegerField()

    data_movimentacao = models.DateTimeField(
        auto_now_add=True
    )

    observacao = models.CharField(
        max_length=255,
        blank=True
    )

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.produto.nome} - {self.quantidade}'