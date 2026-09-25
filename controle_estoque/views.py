from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import (
    F,
    Sum,
    DecimalField,
    ExpressionWrapper,
    Q,
    Case,
    When,
    Value,
    IntegerField,
)
from django.db import transaction
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Produto, MovimentacaoEstoque
from .forms import ProdutoForm, MovimentacaoForm
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    produtos = Produto.objects.all()

    busca = request.GET.get('busca', '').strip()

    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca) |
            Q(codigo__icontains=busca) |
            Q(categoria__icontains=busca)
        )

    categoria = request.GET.get('categoria', '').strip()

    if categoria:
        produtos = produtos.filter(categoria=categoria)

    # Produtos com estoque baixo aparecem primeiro
    produtos = produtos.annotate(
        estoque_baixo_ordem=Case(
            When(
                quantidade_estoque__lte=F('estoque_minimo'),
                then=Value(0)
            ),
            default=Value(1),
            output_field=IntegerField()
        )
    ).order_by(
        'estoque_baixo_ordem',
        'nome'
    )

    # Indicadores do dashboard
    total_produtos = produtos.count()

    total_unidades = produtos.aggregate(
        total=Sum('quantidade_estoque')
    )['total'] or 0

    estoque_baixo = produtos.filter(
        quantidade_estoque__lte=F('estoque_minimo')
    ).count()

    valor_total_estoque = produtos.aggregate(
        total=Sum(
            ExpressionWrapper(
                F('preco') * F('quantidade_estoque'),
                output_field=DecimalField()
            )
        )
    )['total'] or 0

    # Categorias disponíveis
    categorias = Produto.objects.values_list(
        'categoria',
        flat=True
    ).distinct().order_by('categoria')

    # Paginação: 10 produtos por página
    paginator = Paginator(produtos, 10)

    pagina = request.GET.get('pagina')

    produtos_paginados = paginator.get_page(pagina)

    return render(
        request,
        'controle_estoque/home.html',
        {
            'produtos': produtos_paginados,
            'total_produtos': total_produtos,
            'total_unidades': total_unidades,
            'estoque_baixo': estoque_baixo,
            'valor_total_estoque': valor_total_estoque,
            'busca': busca,
            'categoria': categoria,
            'categorias': categorias,
            'pagina_obj': produtos_paginados,
        }
    )

@login_required
def novo_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Produto cadastrado com sucesso!'
            )

            return redirect('home')
    else:
        form = ProdutoForm()

    return render(
        request,
        'controle_estoque/novo_produto.html',
        {'form': form}
    )

@login_required
def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Produto atualizado com sucesso!'
            )

            return redirect('home')
    else:
        form = ProdutoForm(instance=produto)

    return render(
        request,
        'controle_estoque/editar_produto.html',
        {
            'form': form,
            'produto': produto
        }
    )

@login_required
def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        produto.delete()

        messages.success(
            request,
            'Produto excluído com sucesso!'
        )

    return redirect('home')

@login_required
def movimentar_estoque(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)

        if form.is_valid():
            movimentacao = form.save(commit=False)
            movimentacao.produto = produto

            with transaction.atomic():

                if movimentacao.tipo == MovimentacaoEstoque.ENTRADA:
                    produto.quantidade_estoque += movimentacao.quantidade
                    produto.save()

                    movimentacao.save()

                    messages.success(
                        request,
                        'Entrada de estoque registrada com sucesso!'
                    )

                    return redirect('home')

                elif movimentacao.tipo == MovimentacaoEstoque.SAIDA:

                    if movimentacao.quantidade > produto.quantidade_estoque:
                        form.add_error(
                            'quantidade',
                            'A quantidade de saída não pode ser maior que o estoque disponível.'
                        )

                    else:
                        produto.quantidade_estoque -= movimentacao.quantidade
                        produto.save()

                        movimentacao.save()

                        messages.success(
                            request,
                            'Saída de estoque registrada com sucesso!'
                        )

                        return redirect('home')

    else:
        form = MovimentacaoForm()

    return render(
        request,
        'controle_estoque/movimentar_estoque.html',
        {
            'form': form,
            'produto': produto
        }
    )

@login_required
def historico_movimentacoes(request):
    movimentacoes = MovimentacaoEstoque.objects.select_related(
        'produto'
    ).order_by('-data_movimentacao')

    tipo = request.GET.get('tipo', '').strip()

    if tipo in [
        MovimentacaoEstoque.ENTRADA,
        MovimentacaoEstoque.SAIDA
    ]:
        movimentacoes = movimentacoes.filter(tipo=tipo)

    produto_id = request.GET.get('produto', '').strip()

    if produto_id.isdigit():
        movimentacoes = movimentacoes.filter(
            produto_id=produto_id
        )
    else:
        produto_id = ''

    data_inicio = request.GET.get('data_inicio', '').strip()

    if data_inicio:
        movimentacoes = movimentacoes.filter(
            data_movimentacao__date__gte=data_inicio
        )

    data_fim = request.GET.get('data_fim', '').strip()

    if data_fim:
        movimentacoes = movimentacoes.filter(
            data_movimentacao__date__lte=data_fim
        )

    # Resumo das movimentações filtradas
    total_movimentacoes = movimentacoes.count()

    total_entradas = movimentacoes.filter(
        tipo=MovimentacaoEstoque.ENTRADA
    ).aggregate(
        total=Sum('quantidade')
    )['total'] or 0

    total_saidas = movimentacoes.filter(
        tipo=MovimentacaoEstoque.SAIDA
    ).aggregate(
        total=Sum('quantidade')
    )['total'] or 0

    quantidade_movimentada = total_entradas + total_saidas

    produtos_historico = Produto.objects.all().order_by('nome')

    return render(
        request,
        'controle_estoque/historico_movimentacoes.html',
        {
            'movimentacoes': movimentacoes,
            'tipo': tipo,
            'produto_id': produto_id,
            'produtos_historico': produtos_historico,
            'data_inicio': data_inicio,
            'data_fim': data_fim,
            'total_movimentacoes': total_movimentacoes,
            'total_entradas': total_entradas,
            'total_saidas': total_saidas,
            'quantidade_movimentada': quantidade_movimentada,
        }
    )