from datetime import timedelta, datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage, send_mail
# from .tokens import account_activation_token
from django.contrib.auth import get_user_model
import json
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Q
from calendar import monthrange
from math import ceil
import openpyxl
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash


# PÁGINA DE ERRO 404 #
def custom_404(request, exception):
    return render(request, 'ERRORS/404.html', status=404)


# def base(request):
#     return render(request, 'base.html')


def signup(request):
    if request.method == 'POST':
        form = CriarContaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']

            if Utilizadores.objects.filter(email=email).exists():
                form.add_error('email', 'Este email já está em uso.')
            else:
                utilizador = Utilizadores.objects.create_user(
                    username=form.cleaned_data['nome'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    genero=form.cleaned_data['genero'],
                    data_nascimento=form.cleaned_data['data_nascimento'],
                    contacto=form.cleaned_data['contacto'],
                    nif=form.cleaned_data['nif'],
                    pretende_recibo=form.cleaned_data['pretende_recibo'],
                    profissao=form.cleaned_data['profissao'],
                    classificacao_esforco_na_profissao=form.cleaned_data['classificacao_esforco_na_profissao'],
                    fumador=form.cleaned_data['fumador'],
                    problemas_saude=form.cleaned_data['problemas_saude'],
                    limitacoes_para_pratica_exercicio_fisico=form.cleaned_data['limitacoes_para_pratica_exercicio_fisico'],
                    como_teve_conhecimento_existencia_fitclub=form.cleaned_data['como_teve_conhecimento_existencia_fitclub'],
                )
                utilizador.save()

                return redirect('login')
    else:
        form = CriarContaForm()

    return render(request, 'CONTAS/criar_conta.html', {'form': form})


def dologin(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('fcBase')
            else:
                form.add_error(None, 'Email ou password incorretos!')
    else:
        form = LoginForm()
    return render(request, 'CONTAS/login.html', {'form': form})



@login_required
def alterar_senha(request):
    if request.method == "POST":
        form = AlterarSenhaForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantém o usuário logado após a mudança de senha
            return redirect('alterar_senha_concluido')
    else:
        form = AlterarSenhaForm(user=request.user)
    
    return render(request, 'alterar_senha.html', {'form': form})

@login_required
def alterar_senha_concluido(request):
    return render(request, 'alterar_senha_concluido.html')




def logout_view(request):
    logout(request)
    return redirect('login')


# def activateEmail(request, user, to_email):
#     mail_subject = "FitClub - Confirmação de email."
#     message = render_to_string("template_activate_account.html", {
#         'user': user,
#         'domain': get_current_site(request).domain,
#         'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#         'token': account_activation_token.make_token(user),
#         "protocol": 'https' if request.is_secure() else 'http'
#     })
#     email = EmailMessage(mail_subject, message, to=[to_email])
#     if email.send():
#         messages.success(request, f'Email enviado para <b>{to_email}</b> clica no link enviado para confirmar e completar o registo \
#                 <b>Nota:</b> Verifica no spam. <b>ATENÇÃO:</b>  O link expira em 1 hora')
#     else:
#         messages.error(request, f'Problema ao enviar email para {to_email}, confirma que inseriste o email corretamente.')


# def activate(request, uidb64, token):
#     User = get_user_model()
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except:
#         user = None

#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()

#         messages.success(request, "Conta confirmada! Faz login para teres acesso.")
#         return redirect('login')
#     else:
#         messages.error(request, "Link de confirmação inválido!")

#     return redirect('signup')





########## FITCLUB APP ##########

def acesso_negado(request):
    return render(request, 'ERRORS/acesso_negado.html')


@login_required
def fcBase(request):
    if request.user.funcao != 'Ativo':
        return redirect('acesso_negado')
    return render(request, 'FC_APP/fcBase.html')





@login_required
def criar_treinos(request):
    if not request.user.is_staff:
        return render(request, 'ERRORS/403.html')

    if request.method == "POST":
        form = CriarTreinoForm(request.POST)
        if form.is_valid():
            tipo_treino = form.cleaned_data['tipo_treino']
            data_inicio = form.cleaned_data['data_inicio']
            data_fim = form.cleaned_data['data_fim']
            hora_inicio = form.cleaned_data['hora_inicio']
            hora_fim = form.cleaned_data['hora_fim']
            max_participantes = form.cleaned_data['max_participantes']
            max_lista_espera = form.cleaned_data['max_lista_espera']
            dias_da_semana = form.cleaned_data['dia_da_semana']
            reservas_horas_antes = form.cleaned_data['reservas_horas_antes']
            reservas_horas_fecho = form.cleaned_data['reservas_horas_fecho']

            # Mapeamento para exibição legível do tipo de treino
            TIPOS_TREINO_DISPLAY = dict(Treino.TIPO_TREINO_CHOICES)
            tipo_treino_display = TIPOS_TREINO_DISPLAY.get(tipo_treino, tipo_treino)  # Fallback para segurança

            current_date = data_inicio
            while current_date <= data_fim:
                for dia_da_semana in dias_da_semana:
                    dia_semana_map = {
                        'segunda-feira': 0,
                        'terça-feira': 1,
                        'quarta-feira': 2,
                        'quinta-feira': 3,
                        'sexta-feira': 4,
                        'sábado': 5,
                        'domingo': 6,
                    }

                    if current_date.weekday() == dia_semana_map[dia_da_semana]:
                        # Verifica se já existe um treino com o mesmo tipo e horário
                        if Treino.objects.filter(
                            tipo_treino=tipo_treino,
                            data_inicio=current_date,
                            hora_inicio=hora_inicio
                        ).exists():
                            messages.error(
                                request, 
                                f'Já existe um treino "{tipo_treino_display}" às {hora_inicio} dia {current_date.strftime("%d/%m/%Y")}.'
                            )
                            return redirect('criar_treino')

                        # Criação do treino
                        Treino.objects.create(
                            tipo_treino=tipo_treino,
                            data_inicio=current_date,
                            data_fim=current_date,
                            hora_inicio=hora_inicio,
                            hora_fim=hora_fim,
                            max_participantes=max_participantes,
                            max_lista_espera=max_lista_espera,
                            dia_da_semana=dia_da_semana,
                            reservas_horas_antes=reservas_horas_antes,
                            reservas_horas_fecho=reservas_horas_fecho,
                        )
                current_date += timedelta(days=1)

            return redirect('calendario')

    else:
        form = CriarTreinoForm()

    return render(request, 'FC_APP/fcCriar_treino.html', {'form': form})







@login_required
def definicoes(request):
    if request.user.funcao != 'Ativo':
        return redirect('acesso_negado')
    
    if request.method == 'POST':
        form = InformacoesPessoaisForm(request.POST or None, request.FILES or None, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('calendario')
    else:
        form = InformacoesPessoaisForm(instance=request.user)

    return render(request, 'FC_APP/fcDefinicoes.html', {'form': form})

@login_required
def calendario(request):
    if request.user.funcao != 'Ativo':
        return redirect('acesso_negado')
    
    treinos = Treino.objects.all().order_by('hora_inicio')
    current_datetime = timezone.now()  # Data e hora atual com timezone

    for treino in treinos:
        # Adiciona uma flag para indicar se o usuário reservou
        treino.user_reserved = Reservas.objects.filter(utilizador=request.user, treino=treino).exists()

        # Calcula se o treino já passou com base na data e hora completas
        treino_inicio = timezone.make_aware(
            timezone.datetime.combine(treino.data_inicio, treino.hora_inicio)
        )
        treino.has_passed = current_datetime > treino_inicio  # Indica se o treino já começou

    treinos_data = []
    for treino in treinos:
        treinos_data.append({
            'id': treino.id,
            'tipo_treino': treino.get_tipo_treino_display(),
            'data_inicio': treino.data_inicio.strftime('%Y-%m-%d'),
            'hora_inicio': treino.hora_inicio.strftime('%H:%M'),
            'hora_fim': treino.hora_fim.strftime('%H:%M'),
            'max_participantes': treino.max_participantes,
            'reservados': treino.total_reservas(),
            'reservar_url': reverse('reservas', args=[treino.id]),
            'detalhes_url': reverse('reservas_detalhes', args=[treino.id]),
            'user_reserved': treino.user_reserved,
            'has_passed': treino.has_passed  # Passa o status do treino
        })

    return render(request, 'FC_APP/fcCalendario.html', {
        'treinos': treinos,
        'treinos_json': json.dumps(treinos_data),
    })


@login_required
def dadosbiometricos(request):
    if request.user.funcao != 'Ativo':
        return redirect('acesso_negado')

    ano = int(request.GET.get('ano', datetime.now().year))
    mes = int(request.GET.get('mes', datetime.now().month))

    dados_biometricos = Dados_biometricos.objects.filter(
        utilizador=request.user,
        data_registo__year=ano,
        data_registo__month=mes,
    ).first()

    # Calcular idade do utilizador
    if request.user.data_nascimento:
        hoje = date.today()
        idade = hoje.year - request.user.data_nascimento.year - (
            (hoje.month, hoje.day) < (request.user.data_nascimento.month, request.user.data_nascimento.day)
        )
    else:
        idade = "Não informado"

    if not dados_biometricos:
        dados_biometricos = Dados_biometricos(utilizador=request.user, data_registo=datetime(ano, mes, 1))

    if request.method == 'POST':
        form = DadosBiometricosForm(request.POST, instance=dados_biometricos)
        if form.is_valid():
            novo_dado = form.save(commit=False)
            novo_dado.utilizador = request.user
            novo_dado.data_registo = datetime(ano, mes, 1)
            novo_dado.save()
            return redirect('dadosbiometricos')
        else:
            print(form.errors)  # Verifica se há erros no formulário

    else:
        form = DadosBiometricosForm(instance=dados_biometricos)

    meses = range(1, 13)

    return render(
        request,
        'FC_APP/fcDados_biometricos.html',
        {
            'form': form,
            'dados_biometricos': dados_biometricos,
            'ano': ano,
            'mes': mes,
            'meses': meses,
            'idade': idade,
        }
    )



@login_required
def editardadosbiometricos(request, user_id):
    if not request.user.is_staff:
        return render(request, 'ERRORS/403.html')

    # Obtém o mês e o ano da query string ou usa os valores atuais
    ano = int(request.GET.get('ano', datetime.now().year))
    mes = int(request.GET.get('mes', datetime.now().month))

    # VAI BUSCAR O UTILIZADOR PARA NO HTML APARECER O NOME DE UTILIZADOR QUE ESTOU A EDITAR
    utilizador = Utilizadores.objects.get(id=user_id)

    # Filtra os dados biométricos com base no mês, ano e utilizador
    dadobiometrico = Dados_biometricos.objects.filter(
        utilizador_id=user_id, 
        data_registo__year=ano,
        data_registo__month=mes,
    ).first()

    # Calcular idade do utilizador
    if utilizador.data_nascimento:
        hoje = date.today()
        idade = hoje.year - utilizador.data_nascimento.year - (
            (hoje.month, hoje.day) < (utilizador.data_nascimento.month, utilizador.data_nascimento.day)
        )
    else:
        idade = "Não informado"

    # Se nenhum dado for encontrado, cria um novo objeto para edição
    if not dadobiometrico:
        dadobiometrico = Dados_biometricos(utilizador_id=user_id, data_registo=datetime(ano, mes, 1))

    if request.method == 'POST':
        form = EditarDadosBiometricos(request.POST, instance=dadobiometrico)
        if form.is_valid():
            novo_dado = form.save(commit=False)
            novo_dado.utilizador_id = user_id
            novo_dado.data_registo = datetime(ano, mes, 1)
            novo_dado.save()
            return redirect(
                f'{reverse("editardadosbiometricos", kwargs={"user_id": user_id})}?ano={ano}&mes={mes}'
            )
    else:
        form = EditarDadosBiometricos(instance=dadobiometrico)

    # Lista de meses para o dropdown
    meses = range(1, 13)

    # Carrega as reservas do usuário (usando `utilizador_id` como filtro)
    reservas = Reservas.objects.filter(
        utilizador_id=user_id,
        treino__data_inicio__year=ano,
        treino__data_inicio__month=mes,
    ).select_related('treino')

    # Conta o número de reservas confirmadas
    total_reservas_confirmadas = reservas.filter(confirmado=True).count()

    # Conta o número de reservas não confirmadas
    total_reservas_nao_confirmadas = reservas.filter(confirmado=False).count()

    # Conta o número total de reservas
    total_reservas = reservas.count()

    # Cálculo da média semanal de frequência
    _, total_dias_no_mes = monthrange(ano, mes)
    semanas_uteis_no_mes = ceil(total_dias_no_mes / 7)
    dias_uteis_totais = semanas_uteis_no_mes * 5
    media_semanal = (total_reservas_confirmadas / dias_uteis_totais) * 100 if dias_uteis_totais > 0 else 0

    return render(
        request,
        'FC_APP/fcEditar_dados_biometricos.html',
        {
            'form': form,
            'utilizador': utilizador,
            'dadobiometrico': dadobiometrico,
            'ano': ano,
            'mes': mes,
            'meses': meses,
            'total_reservas_confirmadas': total_reservas_confirmadas,
            'total_reservas_nao_confirmadas': total_reservas_nao_confirmadas,
            'total_reservas': total_reservas,
            'media_semanal': media_semanal,
            'reservas': reservas,
            'assiduidade_url': reverse('verassiduidade', kwargs={'user_id': user_id}),
            'idade': idade,
        },
    )

@login_required
def detalhe_dadosbiometricos(request, user_id):
    if request.user.funcao != 'Ativo':
        return redirect('acesso_negado')
    
    dadobiometrico = get_object_or_404(Dados_biometricos, user__id=user_id)
    return render(request, 'FC_APP/fcDetalheUtilizadores.html', {'dadobiometrico': dadobiometrico})




@login_required
def membros(request):
    if request.user.funcao != 'Ativo':
        return redirect('acesso_negado')

    query = request.GET.get('q', '')  # Obtém o termo de pesquisa da URL
    utilizadores = Utilizadores.objects.all()

    if query:
        utilizadores = utilizadores.filter(username__icontains=query)  # Filtra pelo nome de usuário

    # Paginação
    paginator = Paginator(utilizadores, 10)  # 10 utilizadores por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'FC_APP/fcMembros.html', {'page_obj': page_obj, 'query': query})


@login_required
def editar_utilizador(request, user_id):
    if not request.user.is_staff:
        return render(request, 'ERRORS/403.html')

    utilizador = get_object_or_404(Utilizadores, id=user_id)

    if request.method == 'POST':
        form = EditarInformacoesPessoaisForm(request.POST, instance=utilizador)
        if form.is_valid():
            form.save()
            return redirect('detalhe_utilizador', user_id=user_id)
    else:
        form = EditarInformacoesPessoaisForm(instance=utilizador)

    return render(request, 'FC_APP/fcEditarUtilizador.html', {'form': form, 'utilizador': utilizador})





@login_required
def detalhe_utilizador(request, user_id):
    if not request.user.is_staff:
        return render(request, 'ERRORS/403.html')

    if request.user.funcao != 'Ativo':
        return redirect('acesso_negado')
    
    perfil = get_object_or_404(Utilizadores, id=user_id)
    return render(request, 'FC_APP/fcDetalheUtilizadores.html', {'perfil': perfil})


######################################################################



# @login_required
# def reservas(request, treino_id):
#     treino = get_object_or_404(Treino, id=treino_id)

#     # Verificar se o treino já começou
#     treino_inicio = timezone.make_aware(
#         timezone.datetime.combine(treino.data_inicio, treino.hora_inicio)
#     )
#     if timezone.now() > treino_inicio:
#         return render(request, 'FC_RESERVAS/fcReservas_tempo_passado.html', {'treino': treino})

#     # Verificar se o utilizador já tem reserva
#     reserva = Reservas.objects.filter(utilizador=request.user, treino=treino).first()
#     if reserva:
#         # Cancelar reserva e mover o primeiro da lista de espera para as reservas
#         reserva.delete()
#         primeiro_na_lista = ListaEspera.objects.filter(treino=treino).order_by('data_entrada').first()
#         if primeiro_na_lista:
#             Reservas.objects.create(utilizador=primeiro_na_lista.utilizador, treino=treino)
#             primeiro_na_lista.delete()
#         return redirect('calendario')

#     # Verificar se o treino está cheio
#     if Reservas.objects.filter(treino=treino).count() >= treino.max_participantes:
#         # Adicionar o utilizador à lista de espera
#         ListaEspera.objects.get_or_create(utilizador=request.user, treino=treino)

#         # Obter a lista de espera para renderizar no template
#         lista_espera = ListaEspera.objects.filter(treino=treino).order_by('data_entrada')
#         reservas_confirmadas = Reservas.objects.filter(treino=treino)
        
#         return render(request, 'FC_RESERVAS/fcReservas_detalhes.html', {
#             'treino': treino,
#             'lista_espera': lista_espera,
#             'reservas': reservas_confirmadas,  # Também passar reservas confirmadas
#         })

#     # Criar uma nova reserva
#     Reservas.objects.create(utilizador=request.user, treino=treino)
#     return redirect('calendario')

#     # CRIAR UMA NOVA RESERVA
#     Reservas.objects.create(utilizador=request.user, treino=treino)
#     return redirect('calendario')







@login_required
def reservas(request, treino_id):
    if request.user.funcao != 'Ativo':
        return redirect('acesso_negado')
    
    treino = get_object_or_404(Treino, id=treino_id)

    if not treino.reservas_abertas():
        now = timezone.now()
        inicio_treino = timezone.make_aware(
            timezone.datetime.combine(treino.data_inicio, treino.hora_inicio)
        )
        abertura_reservas = inicio_treino - timedelta(hours=treino.reservas_horas_antes)
        fechamento_reservas = inicio_treino - timedelta(hours=treino.reservas_horas_fecho)

        if now < abertura_reservas:
            contexto = {'treino': treino, 'abertura_reservas': abertura_reservas}
            return render(request, 'FC_RESERVAS/fcReservas_reservas_nao_abertas.html', contexto)
        else:
            contexto = {'treino': treino, 'fechamento_reservas': fechamento_reservas}
            return render(request, 'FC_RESERVAS/fcReservas_reservas_fechadas.html', contexto)

    treino_inicio = timezone.make_aware(
        timezone.datetime.combine(treino.data_inicio, treino.hora_inicio)
    )
    if timezone.now() > treino_inicio:
        return render(request, 'FC_RESERVAS/fcReservas_tempo_passado.html', {'treino': treino})

    # VERIFICAR SE O UTILIZADOR JÁ TEM UMA RESERVA NO MESMO DIA
    reserva_existente = Reservas.objects.filter(
        utilizador=request.user,
        treino__data_inicio=treino.data_inicio  # Verifica se já tem treino no mesmo dia
    ).first()

    if reserva_existente:
        if reserva_existente.treino == treino:
            # SE O USUÁRIO ESTÁ TENTANDO CANCELAR A MESMA RESERVA, CANCELAMOS
            reserva_existente.delete()
            primeiro_na_lista = ListaEspera.objects.filter(treino=treino).order_by('data_entrada').first()
            if primeiro_na_lista:
                Reservas.objects.create(utilizador=primeiro_na_lista.utilizador, treino=treino)
                primeiro_na_lista.delete()
            return redirect('calendario')
        else:
            # SE JÁ TIVER OUTRO TREINO NO MESMO DIA, BLOQUEAMOS A NOVA RESERVA
            messages.error(request, "Não é permitido fazer mais do que uma reserva por dia.")
            return redirect('calendario')

    # VERIFICAR SE O TREINO ESTÁ CHEIO
    if Reservas.objects.filter(treino=treino).count() >= treino.max_participantes:
        if ListaEspera.objects.filter(treino=treino).count() >= treino.max_lista_espera:
            return render(request, 'lista_espera_full.html', {'treino': treino})
    
        ListaEspera.objects.get_or_create(utilizador=request.user, treino=treino)
        return render(request, 'reservas_lista_espera.html', {'treino': treino})

    # CRIAR RESERVA
    Reservas.objects.create(utilizador=request.user, treino=treino)

    return redirect('calendario')







@login_required
def adicionar_utilizador_treino(request, treino_id):
    if request.user.funcao != 'Ativo':
        return redirect('acesso_negado')
    
    if not request.user.is_staff:
        return render(request, 'ERRORS/403.html')
        
    treino = get_object_or_404(Treino, id=treino_id)

    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        usuario = get_object_or_404(Utilizadores, id=usuario_id)
        
        # Verifica se já existe uma reserva para este utilizador e treino
        reserva, created = Reservas.objects.get_or_create(
            utilizador=usuario,
            treino=treino,
            defaults={'confirmado': None}  # Define a reserva como confirmada
        )
        
        if not created:
            # Caso já exista a reserva, garantimos que a confirmação seja False
            reserva.confirmado = False
            reserva.save()
        
        # Redireciona de volta para a página de detalhes do treino
        return redirect('reservas_detalhes', treino_id=treino.id)
    
    # Recupera os utilizadores que já tem uma reserva e os exclui da lista de utilizadores disponíveis
    utilizadores_com_reserva = Reservas.objects.filter(treino=treino).values_list('utilizador_id', flat=True)
    utilizadores_disponiveis = Utilizadores.objects.exclude(id__in=utilizadores_com_reserva)
    
    # Renderiza a página com a lista de utilizadores disponíveis
    return render(request, 'adicionar_utilizador_treino.html', {'treino': treino, 'usuarios': utilizadores_disponiveis})











@login_required
def lista_espera_view(request, treino_id):
    if request.user.funcao != 'Ativo':
        return redirect('acesso_negado')
    
    treino = get_object_or_404(Treino, id=treino_id)
    lista_espera = ListaEspera.objects.filter(treino=treino).order_by('data_entrada')
    return render(request, 'FC_RESERVAS/fcLista_espera.html', {'lista_espera': lista_espera, 'treino': treino})



@login_required
def cancelar_lista_espera(request, treino_id):
    if request.user.funcao != 'Ativo':
        return redirect('acesso_negado')
    
    treino = get_object_or_404(Treino, id=treino_id)
    lista_espera = ListaEspera.objects.filter(utilizador=request.user, treino=treino)

    if lista_espera.exists():
        lista_espera.delete()
        messages.success(request, "Você saiu da lista de espera com sucesso.")
    else:
        messages.error(request, "Você não está na lista de espera para este treino.")

    return redirect('reservas_detalhes', treino_id=treino.id)







################################################################################################



@login_required
def reservas_detalhes(request, treino_id):
    if request.user.funcao != 'Ativo':
        return redirect('acesso_negado')

    treino = get_object_or_404(Treino, id=treino_id)
    reservas = Reservas.objects.filter(treino=treino)
    lista_espera = ListaEspera.objects.filter(treino=treino).order_by('data_entrada')

    if request.method == 'POST':
        reservas_id = request.POST.get('reservas_id')
        reserva = get_object_or_404(Reservas, id=reservas_id)
        action = request.POST.get('action')

        if action == 'presente':
            reserva.confirmado = True  # Usuário está presente
            reserva.save()
        elif action == 'ausente':
            reserva.confirmado = False  # Usuário está ausente
            reserva.save()

            # Enviar e-mail ao usuário informando a ausência
            assunto = "FitClub - Ausência no Treino"
            mensagem = f"""
            Olá {reserva.utilizador.username},

            Marcaste reserva para o treino do dia {reserva.treino.data_inicio} às {reserva.treino.hora_inicio} mas não compareceste no mesmo.

            Não te esqueças de pagar a taxa de ausência até ao próximo treino!

            Com os melhores cumprimentos,  
            Equipa FitClub
            """
            
            remetente = "miguelcarvalho407@gmail.com"  # Altere para o seu e-mail configurado no Django
            destinatario = [reserva.utilizador.email]

            send_mail(assunto, mensagem, remetente, destinatario, fail_silently=False)

            messages.success(request, f"E-mail enviado para {reserva.utilizador.email} notificando ausência.")

        else:
            reserva.confirmado = None
            reserva.save()

        return redirect('reservas_detalhes', treino_id=treino.id)

    return render(
        request, 
        'FC_RESERVAS/fcReservas_detalhes.html', 
        {'treino': treino, 'reservas': reservas, 'lista_espera': lista_espera}
    )






@receiver(post_save, sender=Reservas)
def enviar_email_reserva_lista_espera(sender, instance, created, **kwargs):
    if created:  # Só interessa reservas recém-criadas
        treino = instance.treino

        # Verifica se essa reserva foi feita transferindo alguém da lista de espera
        primeiro_na_lista = ListaEspera.objects.filter(treino=treino).order_by('data_entrada').first()
        if primeiro_na_lista:
            # Obtém a data de início do treino (data_inicio)
            data_treino = treino.data_inicio.strftime('%d/%m/%Y')  # Formato da data: dd/mm/yyyy

            # Envia o e-mail para o usuário promovido
            send_mail(
                subject=f"Reserva confirmada para o treino de {data_treino} às {treino.hora_inicio}",
                message=(
                    f"Olá {primeiro_na_lista.utilizador.username},\n\n"
                    f"Alguém cancelou a reserva para o treino, e a tua reserva foi automaticamente confirmada.\n"
                    f"O treino acontecerá no dia {data_treino} às {treino.hora_inicio}.\n\n"
                    f"Se não conseguires estar presente cancela a tua reserva no nosso website.\n\n"
                    "Obrigado!"
                ),
                from_email='miguelcarvalho407@gmail.com',
                recipient_list=[primeiro_na_lista.utilizador.email],
                fail_silently=False,
            )





#CRUD

@login_required                                                                    
def editar_treino(request, treino_id):
    if not request.user.is_staff:
        return redirect('calendario')
    
    treino = get_object_or_404(Treino, id=treino_id)

    if request.method == 'POST':
        form = EditarTreinoForm(request.POST, instance=treino)
        if form.is_valid():
            form.save()
            return redirect('calendario')  # Redirecione para a página de lista de treinos
    else:
        form = EditarTreinoForm(instance=treino)

    return render(request, 'CRUD/fcEditar_treino.html', {'form': form, 'treino': treino})


@login_required
def apagartreino(request, pk):
    if not request.user.is_staff:
        return redirect('calendario')

    treino = Treino.objects.filter(pk=pk).first()
    if not treino:
        return redirect('calendario')

    if request.method == 'POST':

        detalhes_treino_cancelado = f"Treino de {treino.dia_da_semana} - {treino.data_inicio} às {treino.hora_inicio} foi cancelado"
        treino.delete()
        utilizadores = Utilizadores.objects.all()
        emails = [utilizador.email for utilizador in utilizadores if utilizador.email]

        send_mail(
            subject="Treino Cancelado",
            message=f"Olá,\n\nO {detalhes_treino_cancelado}\n\n\nCom os melhores cumprimentos",

            from_email="miguelcarvalho407@gmail.com",
            recipient_list=emails,
            fail_silently=False,
        )

        return redirect('calendario')

    return render(request, 'CRUD/fcApagar_tarefa.html', {'treino': treino})








@login_required
def apagar_treinos_em_massa(request):
    if not request.user.is_staff:
        return redirect('calendario')

    if request.method == 'POST':
        # Dados do formulário para filtragem
        data_inicio = request.POST.get('data_inicio')
        data_fim = request.POST.get('data_fim')
        tipo_treino = request.POST.get('tipo_treino')
        dia_da_semana = request.POST.get('dia_da_semana')
        hora_inicio = request.POST.get('hora_inicio')

        # Filtro inicial vazio
        filtros = Q()

        # Aplica filtros de acordo com os critérios preenchidos
        if data_inicio:
            filtros &= Q(data_inicio__gte=data_inicio)
        if data_fim:
            filtros &= Q(data_inicio__lte=data_fim)
        if tipo_treino:
            filtros &= Q(tipo_treino=tipo_treino)
        if dia_da_semana:
            filtros &= Q(dia_da_semana=dia_da_semana)
        if hora_inicio:
            filtros &= Q(hora_inicio=hora_inicio)

        # Apaga os treinos filtrados
        treinos_apagados = Treino.objects.filter(filtros).delete()

        # Redireciona após apagar
        return redirect('calendario')

    # Renderiza a página com o formulário
    return render(request, 'CRUD/fcApagar_treinos_em_massa.html')



@login_required
def recordes(request):
    if request.user.funcao != 'Ativo':
        return redirect('acesso_negado')
    
    if request.method == 'POST':
        form = CriarRecordesForm(request.POST, user=request.user)
        if form.is_valid():
            recorde = form.save(commit=False)
            recorde.utilizador = request.user
            recorde.save()

            return redirect('recordes')
    else:
        form = CriarRecordesForm(user=request.user)

    # Captura o valor do filtro na URL
    query = request.GET.get('q')

    # Filtra os recordes com base no nome do recorde ou no exercício predefinido
    if query:
        recorde = Recordes.objects.filter(
            utilizador=request.user
        ).filter(
            Q(nome__nome__icontains=query) | Q(predefinidos__icontains=query)
        )
    else:
        recorde = Recordes.objects.filter(utilizador=request.user)

    # Obtenha todos os nomes do modelo RecordesNomes
    nomes_disponiveis = RecordesNomes.objects.filter(utilizador=request.user)

    # OBTEM OS EXERCÍCIOS PREDEFINIDOS
    predefinidos_disponiveis = [
        {"value": choice[0], "label": choice[1]}
        for choice in Recordes.EXERCICIOS_PREDEFINIDOS_CHOICES
        if choice[0] != "vazio"  # Exclui a opção vazia
    ]

    # Combine as opções para o filtro
    opcoes_filtro = list(nomes_disponiveis.values_list('nome', flat=True)) + [
        choice["label"] for choice in predefinidos_disponiveis
    ]

    return render(request,'FC_APP/fcCriarRecorde.html',{'form': form,'recorde': recorde,'nomes_disponiveis': nomes_disponiveis,'predefinidos_disponiveis': predefinidos_disponiveis,'opcoes_filtro': opcoes_filtro,'query': query})




@login_required
def criarnomerecordes(request):
    if request.user.funcao != 'Ativo':
        return redirect('acesso_negado')
    
    if request.method == 'POST':
        form = CriarNomeRecordeForm(request.POST or None)
        if form.is_valid():
            nome = form.save(commit=False)
            nome.utilizador = request.user
            nome.save()

            return redirect('recordes')
    else:
        form = CriarNomeRecordeForm

    nome = RecordesNomes.objects.filter(utilizador=request.user)

    return render(request, 'FC_APP/fcCriar_recorde_nome.html', {'form': form, 'nome': nome})


@login_required
def ver_recordes_utilizador(request, user_id):
    if not request.user.is_staff:
        return render(request, 'ERRORS/403.html')

    utilizador = get_object_or_404(Utilizadores, id=user_id)

    # Buscar recordes criados pelo utilizador
    recordes_personalizados = Recordes.objects.filter(utilizador=utilizador)

    # Buscar recordes predefinidos
    predefinidos_disponiveis = [
        {"nome": choice[1], "valor": None}  # Inicializamos os valores como None
        for choice in Recordes.EXERCICIOS_PREDEFINIDOS_CHOICES
        if choice[0] != "vazio"  # Exclui a opção "vazio"
    ]

    # Substituir os valores None pelos valores reais se existirem no banco de dados
    for predefinido in predefinidos_disponiveis:
        recorde_existente = Recordes.objects.filter(
            utilizador=utilizador,
            predefinidos=predefinido["nome"],
        ).first()
        if recorde_existente:
            predefinido["valor"] = recorde_existente.valor
            predefinido["data_do_recorde"] = recorde_existente.data_do_recorde

    # Combinar recordes personalizados e predefinidos
    todos_recordes = list(recordes_personalizados) + predefinidos_disponiveis

    return render(request, 'FC_APP/fcVerRecordes.html', {
        'utilizador': utilizador,
        'recordes': todos_recordes,
    })



@login_required
def assiduidade(request):
    if request.user.funcao != 'Ativo':
        return redirect('acesso_negado')
    
    # Obtém o mês e o ano da URL ou usa o atual
    ano = int(request.GET.get('ano', datetime.now().year))
    mes = int(request.GET.get('mes', datetime.now().month))

    # Busca as reservas do usuário para o mês e ano selecionados
    reservas = Reservas.objects.filter(
        utilizador=request.user,
        treino__data_inicio__year=ano,
        treino__data_inicio__month=mes,
    ).select_related('treino')

    # Contar treinos confirmados
    total_reservas_confirmadas = reservas.filter(confirmado=True).count()

    # Contar treinos não confirmados
    total_reservas_nao_confirmadas = reservas.filter(confirmado=False).count()

    # Contar o total de treinos
    total_reservas = reservas.count()

    # Calcular a média semanal de frequência (5 dias úteis por semana)
    _, total_dias_no_mes = monthrange(ano, mes)
    semanas_uteis_no_mes = ceil(total_dias_no_mes / 7)  # Total de semanas no mês
    dias_uteis_totais = semanas_uteis_no_mes * 5  # Máximo de treinos possíveis no mês

    # Calcular a média semanal como porcentagem
    if dias_uteis_totais > 0:
        media_semanal = (total_reservas_confirmadas / dias_uteis_totais) * 100
    else:
        media_semanal = 0

    # Filtro por meses
    meses = range(1, 13)

    return render(
        request,
        'FC_APP/fcAssiduidade.html',
        {
            'ano': ano,
            'mes': mes,
            'meses': meses,
            'total_reservas_confirmadas': total_reservas_confirmadas,
            'total_reservas_nao_confirmadas': total_reservas_nao_confirmadas,
            'total_reservas': total_reservas,
            'media_semanal': media_semanal,
            'reservas': reservas,
        }
    )


def ver_assiduidade(request, user_id):
    if not request.user.is_staff:
        return render(request, 'ERRORS/403.html')

    # Obtém o mês e ano da query string ou usa os valores atuais
    ano = int(request.GET.get('ano', datetime.now().year))
    mes = int(request.GET.get('mes', datetime.now().month))

    # Busca o utilizador para mostrar no template
    utilizador = Utilizadores.objects.get(id=user_id)

    # Filtra as reservas com base no mês, ano e utilizador
    reservas = Reservas.objects.filter(
        utilizador_id=user_id,
        treino__data_inicio__year=ano,
        treino__data_inicio__month=mes,
    ).select_related('treino')

    # Conta o número de reservas confirmadas
    total_reservas_confirmadas = reservas.filter(confirmado=True).count()

    # Conta o número de reservas não confirmadas
    total_reservas_nao_confirmadas = reservas.filter(confirmado=False).count()

    # Conta o número total de reservas
    total_reservas = reservas.count()

    # Cálculo da média semanal de frequência
    # Número de dias no mês
    _, total_dias_no_mes = monthrange(ano, mes)
    # Número de semanas úteis no mês (5 dias úteis por semana)
    semanas_uteis_no_mes = ceil(total_dias_no_mes / 7)
    dias_uteis_totais = semanas_uteis_no_mes * 5  # Máximo de dias úteis no mês

    # Calcular a média semanal como porcentagem
    if dias_uteis_totais > 0:
        media_semanal = (total_reservas_confirmadas / dias_uteis_totais) * 100
    else:
        media_semanal = 0

    # Lista de meses para o dropdown
    meses = range(1, 13)

    return render(
        request,
        'FC_APP/fcVer_assiduidade.html',  # Template adaptado
        {
            'utilizador': utilizador,
            'reservas': reservas,
            'ano': ano,
            'mes': mes,
            'meses': meses,
            'total_reservas': total_reservas,
            'total_reservas_confirmadas': total_reservas_confirmadas,
            'total_reservas_nao_confirmadas': total_reservas_nao_confirmadas,
            'media_semanal': media_semanal,
        },
    )









#TESTES

# VER SE EXPORTA OS DADOS DE TODOS OS UTILIZADORES
def export_to_excel(request):
    # Cria uma nova planilha
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Dados Biométricos"

    # Cabeçalho da planilha
    columns = ['ID', 'Nome', 'Email', 'Contacto', 'Data de Nascimento', 'Morada', 'Código Postal', 'Localidade',
               'NIF', 'Pretende Recibo', 'Profissão', 'Classificação de Esforço na Profissão', 'Fumador', 'Problemas de Saúde', 'Limitações para a prática de exercício Físico']
    ws.append(columns)

    # VAI BUSCAR OS DADOS A BASE DE DADOS
    informacoes = Utilizadores.objects.all()

    # DADOS QUE VÃO SER PASSADOS PARA O EXCEL
    for data in informacoes:
        row = [
            data.id, 
            data.username, 
            data.email, 
            data.contacto, 
            data.data_nascimento, 
            data.morada, 
            data.codigo_postal, 
            data.localidade,
            data.nif,
            data.pretende_recibo,
            data.profissao,
            data.classificacao_esforco_na_profissao,
            data.fumador,
            data.problemas_saude,
            data.limitacoes_para_pratica_exercicio_fisico,
        ]  # Altere conforme os campos do seu modelo
        ws.append(row)

    # Criar o response com o arquivo Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="dados_totais.xlsx"'

    # Salvar o arquivo na resposta HTTP
    wb.save(response)
    return response





# EXPORTA OS DADOS DE UM UTILIZADOR ESPECIFICO
def export_user_data_to_excel(request, user_id):
    if not request.user.is_staff:
        return render(request, 'ERRORS/403.html')

    # BUSCAR O UTILIZADOR ESPECIFICO PELO ID
    utilizador = get_object_or_404(Utilizadores, id=user_id)

    # Criar uma nova planilha
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"Dados do utilizador {utilizador.username}"

    # Cabeçalho da planilha
    columns = ['ID', 'Nome', 'Email', 'Contacto', 'Data de Nascimento', 'Morada', 'Código Postal', 'Localidade',
               'NIF', 'Pretende Recibo', 'Profissão', 'Classificação de Esforço na Profissão', 'Fumador', 'Problemas de Saúde', 'Limitações para a prática de exercício Físico']
    ws.append(columns)

    # Adicionar os dados do utilizador selecionado
    row = [
        utilizador.id, 
        utilizador.username, 
        utilizador.email, 
        utilizador.contacto, 
        utilizador.data_nascimento, 
        utilizador.morada, 
        utilizador.codigo_postal, 
        utilizador.localidade,
        utilizador.nif,
        utilizador.pretende_recibo,
        utilizador.profissao,
        utilizador.classificacao_esforco_na_profissao,
        utilizador.fumador,
        utilizador.problemas_saude,
        utilizador.limitacoes_para_pratica_exercicio_fisico,
    ]
    ws.append(row)

    # Criar a resposta com o arquivo Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="dados_utilizador_{utilizador.username}.xlsx"'

    # Salvar o arquivo na resposta HTTP
    wb.save(response)
    return response





from django.contrib.auth.tokens import default_token_generator

def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            user = Utilizadores.objects.get(email=email)

            # Criando o token e a URL de recuperação
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            
            current_site = request.get_host()
            reset_url = f"http://{current_site}/reset/{uid}/{token}/"

            # Enviar o e-mail
            send_mail(
                "Redefinição de Password",
                f"Clica no link para redefinir a tua password: {reset_url}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )

            return redirect("login")
    else:
        form = PasswordResetRequestForm()

    return render(request, "CONTAS/password_reset_form.html", {"form": form})





def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Utilizadores.objects.get(pk=uid)
    except (Utilizadores.DoesNotExist, ValueError, TypeError):
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            form = SetNewPasswordForm(request.POST)
            if form.is_valid():
                user.set_password(form.cleaned_data["new_password1"])
                user.save()
                return redirect('login')
        else:
            form = SetNewPasswordForm()
        return render(request, "CONTAS/password_reset_confirm.html", {"form": form})
    else:
        return render(request, "CONTAS/password_reset_invalid.html")


@login_required
def cartao(request):
    return render(request, 'FC_APP/fcCartao.html')



