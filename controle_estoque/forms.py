from decimal import Decimal, InvalidOperation

from django import forms

from .models import Produto, MovimentacaoEstoque


class BrazilianDecimalField(forms.DecimalField):
    def to_python(self, value):
        if value in self.empty_values:
            return None

        if isinstance(value, str):
            value = value.strip()
            value = value.replace('R$', '').replace(' ', '')

            # Formato brasileiro:
            # 4.277,04 -> 4277.04
            if ',' in value:
                value = value.replace('.', '')
                value = value.replace(',', '.')

        try:
            return super().to_python(value)
        except (InvalidOperation, ValueError):
            raise forms.ValidationError(
                'Digite um preço válido. Exemplo: 4.277,04'
            )


class ProdutoForm(forms.ModelForm):

    preco = BrazilianDecimalField(
        max_digits=12,
        decimal_places=4,
        min_value=0,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex: 4.277,04',
            'inputmode': 'decimal'
        })
    )

    class Meta:
        model = Produto

        fields = [
            'nome',
            'codigo',
            'categoria',
            'preco',
            'quantidade_estoque',
            'estoque_minimo',
        ]

        labels = {
            'nome': 'Nome do produto',
            'codigo': 'Código do produto',
            'categoria': 'Categoria',
            'preco': 'Preço',
            'quantidade_estoque': 'Quantidade em estoque',
            'estoque_minimo': 'Estoque mínimo',
        }

        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'Digite o nome do produto'
            }),

            'codigo': forms.TextInput(attrs={
                'placeholder': 'Digite o código do produto'
            }),

            'categoria': forms.TextInput(attrs={
                'placeholder': 'Ex: Periféricos, Eletrônicos, Móveis...'
            }),

            'quantidade_estoque': forms.NumberInput(attrs={
                'placeholder': 'Quantidade disponível',
                'min': '0'
            }),

            'estoque_minimo': forms.NumberInput(attrs={
                'placeholder': 'Quantidade mínima',
                'min': '0'
            }),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']

        produtos = Produto.objects.filter(codigo=codigo)

        if self.instance.pk:
            produtos = produtos.exclude(pk=self.instance.pk)

        if produtos.exists():
            raise forms.ValidationError(
                'Já existe um produto cadastrado com este código.'
            )

        return codigo


class MovimentacaoForm(forms.ModelForm):

    class Meta:
        model = MovimentacaoEstoque

        fields = [
            'produto',
            'tipo',
            'quantidade',
            'observacao',
        ]

        labels = {
            'produto': 'Produto',
            'tipo': 'Tipo de movimentação',
            'quantidade': 'Quantidade',
            'observacao': 'Observação',
        }

        widgets = {
            'produto': forms.Select(),

            'tipo': forms.Select(),

            'quantidade': forms.NumberInput(attrs={
                'placeholder': 'Digite a quantidade',
                'min': '1'
            }),

            'observacao': forms.TextInput(attrs={
                'placeholder': 'Ex: Compra de mercadoria, venda, reposição...'
            }),
        }

    def clean_quantidade(self):
        quantidade = self.cleaned_data['quantidade']

        if quantidade < 1:
            raise forms.ValidationError(
                'A quantidade deve ser maior que zero.'
            )

        return quantidade