from django.urls import path
from . import views

urlpatterns = [
    path('', views.dologin, name='login'),

    path('signup/', views.signup, name='signup'),
    path('login/', views.dologin, name='login'),
    path('logout/', views.logout_view, name='logout'),
    # path('activate/<uidb64>/<token>', views.activate, name='activate'),

    path('acessonegado/', views.acesso_negado, name='acesso_negado'),
    path('fitclub/', views.fcBase, name='fcBase'),
    path('fitclub/calendario/', views.calendario, name='calendario'),
    path('fitclub/criar_treino/', views.criar_treinos, name='criar_treino'),

    path('fitclub/membros/', views.membros, name='membros'),
    path('fitclub/utilizador/<int:user_id>/', views.detalhe_utilizador, name='detalhe_utilizador'),

    path('fitclub/definicoes/', views.definicoes, name='definicoes'),
    path('fitclub/recordes/', views.recordes, name='recordes'),
    path('fitclub/criarnomerecordes/', views.criarnomerecordes, name='criarnomerecordes'),
    path('fitclub/dadosbiometricos/', views.dadosbiometricos, name='dadosbiometricos'),
    path('fitclub/utilizador/<int:user_id>/editar/', views.editar_utilizador, name='editar_utilizador'),
    path('fitclub/assiduidade/', views.assiduidade, name='assiduidade'),

    path('fitclub/reservas_detalhes/<int:treino_id>/', views.reservas_detalhes, name='reservas_detalhes'),
    path('reservas/<int:treino_id>/', views.reservas, name='reservas'),


    #CRUD
    path('fitclub/editar_treino/<int:treino_id>/', views.editar_treino, name='editar_treino'),
    path('fitclub/apagartreino/<int:pk>/', views.apagartreino, name='apagartarefa'),

    path('fitclub/utilizador/<int:user_id>/dadosbiometricos', views.editardadosbiometricos, name='editardadosbiometricos'),
    path('fitclub/utilizador/<int:user_id>/assiduidade/', views.ver_assiduidade, name='verassiduidade'),

    path('fitclub/apagartreinos/', views.apagar_treinos_em_massa, name='apagar_treinos_em_massa'),

    path('fitclub/utilizador/<int:user_id>/recordes/', views.ver_recordes_utilizador, name='ver_recordes_utilizador'),

    path('fitclub/listaespera/<int:treino_id>/', views.lista_espera_view, name='listaespera'),


    # EXPORTA OS DADOS DE TODOS OS UTILIZADORES
    path('exportar_excel/', views.export_to_excel, name='exportar_excel'),
    # EXPORTA OS DADOS DE UM UTILIZADOR ESPECIFICO
    path('exportar_utilizador/<int:user_id>/', views.export_user_data_to_excel, name='exportar_utilizador'),

]

