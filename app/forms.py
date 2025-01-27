from django import forms
from django.forms import ModelForm
from .models import *
import re


class CriarContaForm(forms.Form):
    nome = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class':'form-control',
        'id':'nome',
        'placeholder':'Primeiro e Último'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'Insere o teu email'
    }))
    data_nascimento = forms.DateField(widget=forms.DateInput(attrs={
        'class':'form-control',
        'type':'date'
    }))
    contacto = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': '910 000 000'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Insere a password'
    }))
    confirmar_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Repete a password'
    }))
    genero = forms.ChoiceField(choices=Utilizadores.GENERO_CHOICES, widget=forms.Select(attrs={
        'class':'form-control'
    }))
    chave = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'Chave fornecida'
    }))

    # OUTROS DADOS

    nif = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class': 'form-control',
        'placeholder': 'Número de Identificação Fiscal'
    }))
    pretende_recibo = forms.ChoiceField(choices=Utilizadores.PRETENDE_RECIBO, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    profissao = forms.CharField(max_length=255, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    classificacao_esforco_na_profissao = forms.ChoiceField(choices=Utilizadores.CLASSIFICACAO_ESFORCO, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    fumador = forms.ChoiceField(choices=Utilizadores.FUMADOR, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    problemas_saude = forms.ChoiceField(choices=Utilizadores.PROBLEMAS_SAUDE, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    limitacoes_para_pratica_exercicio_fisico = forms.ChoiceField(choices=Utilizadores.LIMITACOES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirmar_password = cleaned_data.get('confirmar_password')
        chave = cleaned_data.get('chave')

        if password and len(password) < 8:
            self.add_error('password', 'A password deve conter pelo menos 8 caracteres!')

        if password != confirmar_password:
            self.add_error('confirmar_password', 'As passwords não correspondem!')

        #DEFINIÇÃO DA CHAVE
        if chave != 'Fitclubns17_2025!':
            self.add_error('chave', 'Chave incorreta!')

        return cleaned_data


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class':'form-control',
        'placeholder':'exemplo@gmail.com'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class':'form-control',
        'placeholder':'**********'
    }))


class InformacoesPessoaisForm(forms.ModelForm):
    class Meta:
        model = Utilizadores
        fields = ['email', 'username', 'data_nascimento', 'genero', 'morada', 'codigo_postal', 'localidade', 'contacto',
                  'nif', 'pretende_recibo', 'profissao', 'classificacao_esforco_na_profissao', 'fumador', 'problemas_saude', 'limitacoes_para_pratica_exercicio_fisico', 'is_staff']
        widgets = {
            'email':forms.EmailInput(attrs={
                'readonly': 'readonly'
            }),
            'data_nascimento':forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'codigo_postal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0000-000',
            }),
            'contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '910 000 000',
            }),
            'morada':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escreva a sua morada'
            })

        }
        labels = {
            'username': ('Nome'),
            'data_nascimento': ('Data de Nascimento'),
            'morada': ('Morada (Opcional)'),
            'codigo_postal': ('Código Postal (Opcional)'),
            'localidade': ('Localidade (Opcional)'),
            'contacto': ('Contacto'),
            'genero': ('Género'),
        }




class EditarInformacoesPessoaisForm(forms.ModelForm):
    is_staff = forms.ChoiceField(
        choices=[
            ('True', 'Sim'),
            ('False', 'Não'),
        ],
    )
    class Meta:
        model = Utilizadores
        fields = ['username', 'email', 'contacto', 'data_nascimento', 'genero', 'morada', 'codigo_postal', 'localidade', 'funcao',
                  'nif', 'pretende_recibo', 'profissao', 'classificacao_esforco_na_profissao', 'fumador', 'problemas_saude', 'limitacoes_para_pratica_exercicio_fisico', 'is_staff']
        widgets = {
            'email':forms.EmailInput(attrs={
                'readonly': 'readonly'
            }),
            'data_nascimento':forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'codigo_postal': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '0000-000',
            }),
            'contacto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '910 000 000',
            }),
            'morada':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Escreva a sua morada'
            }),
            'is_staff':forms.TextInput(attrs={
                'class': 'form-control',
            })
        }
        labels = {
            'username': ('Nome'),
            'data_nascimento': ('Data Nascimento'),
            'genero': ('Género'),
            'codigo_postal': ('Código Postal'),
            'funcao': ('Função'),
        }


def clean_codigo_postal(self):
    codigo_postal = self.cleaned_data.get('codigo_postal')

    re.match(r'^\d{4}-\d{3}$', codigo_postal)

    return codigo_postal


class DadosBiometricosForm(forms.ModelForm):
    class Meta:
        model = Dados_biometricos
        fields = ['idade', 'altura', 'peso', 'massa_gorda', 'massa_muscular', 'agua', 'gordura_visceral', 'idade_biologica', 'nivel_fisico']  # Removido 'imc'
        widgets = {
            'idade': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'altura': forms.NumberInput(),
            'peso': forms.NumberInput(),
            'massa_gorda': forms.NumberInput(),
            'massa_muscular': forms.NumberInput(),
            'agua': forms.NumberInput(),
            'gordura_visceral': forms.NumberInput(),
            'idade_biologica': forms.NumberInput(),
            'nivel_fisico': forms.NumberInput(),
        }


class EditarDadosBiometricos(forms.ModelForm):
    class Meta:
        model = Dados_biometricos
        fields = ['idade', 'altura', 'peso', 'massa_gorda', 'massa_muscular', 'agua', 'gordura_visceral', 'idade_biologica', 'nivel_fisico']  # Removido 'imc'
        widgets = {
            'idade': forms.NumberInput(attrs={'readonly': 'readonly'}),
            'altura': forms.NumberInput(),
            'peso': forms.NumberInput(),
            'massa_gorda': forms.NumberInput(),
            'massa_muscular': forms.NumberInput(),
            'agua': forms.NumberInput(),
            'gordura_visceral': forms.NumberInput(),
            'idade_biologica': forms.NumberInput(),
            'nivel_fisico': forms.NumberInput(),
        }


class CriarTreinoForm(forms.Form):
    tipo_treino = forms.ChoiceField(
        choices=[
            ('treino_funcional', 'Treino Funcional'),
            ('mobilidade', 'Mobilidade'),
            ('força', 'Força'),
            ('total_fit', 'Total FIT'),
        ],
        label="Tipo de Treino"
    )
    data_inicio = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        label="Data de Início"
    )
    data_fim = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        label="Data de Fim"
    )
    hora_inicio = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        input_formats=['%H:%M'],
        label="Hora de Início"
    )
    hora_fim = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        input_formats=['%H:%M'],
        label="Hora de Fim"
    )
    max_participantes = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'number', 'min': '1'}),
        label="Máximo de Participantes"
    )
    max_lista_espera = forms.IntegerField(
        widget=forms.NumberInput(attrs={'type': 'number', 'min': '0'}),
        label="Máximo na Lista de Espera"
    )
    reservas_horas_antes = forms.ChoiceField(
        choices=[
            (1, '1 hora antes'),
            (6, '6 horas antes'),
            (12, '12 horas antes'),
            (24, '24 horas antes'),
            (48, '48 horas antes')
        ],
        label="Abertura das Reservas",
        initial=24,  # Valor padrão: 24 horas antes
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    reservas_horas_fecho = forms.ChoiceField(
        choices=[
            (0, 'No início do treino'),
            (1, '1 hora antes'),
            (2, '2 horas antes'),
            (6, '6 horas antes'),
            (12, '12 horas antes'),
        ],
        label="Fechamento das Reservas",
        initial=1,  # Valor padrão: 1 hora antes
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    dia_da_semana = forms.ChoiceField(
        choices=[
            ('segunda-feira', 'Segunda-feira'),
            ('terça-feira', 'Terça-feira'),
            ('quarta-feira', 'Quarta-feira'),
            ('quinta-feira', 'Quinta-feira'),
            ('sexta-feira', 'Sexta-feira'),
            ('sábado', 'Sábado'),
            ('domingo', 'Domingo'),
        ],
        label="Dia da Semana"
    )

    def clean(self):
        cleaned_data = super().clean()

        # Obter dados
        data_inicio = cleaned_data.get('data_inicio')
        data_fim = cleaned_data.get('data_fim')
        hora_inicio = cleaned_data.get('hora_inicio')
        hora_fim = cleaned_data.get('hora_fim')
        reservas_horas_antes = cleaned_data.get('reservas_horas_antes')
        reservas_horas_fecho = cleaned_data.get('reservas_horas_fecho')
        max_participantes = cleaned_data.get('max_participantes')
        max_lista_espera = cleaned_data.get('max_lista_espera')

        # Converter valores de abertura e fechamento para inteiros
        try:
            reservas_horas_antes = int(reservas_horas_antes)
            reservas_horas_fecho = int(reservas_horas_fecho)
            cleaned_data['reservas_horas_antes'] = reservas_horas_antes
            cleaned_data['reservas_horas_fecho'] = reservas_horas_fecho
        except (ValueError, TypeError):
            raise forms.ValidationError("Os valores de 'Abertura' e 'Fechamento' devem ser números válidos.")

        # Validações
        if reservas_horas_antes < 0:
            raise forms.ValidationError("O número de horas antes deve ser maior ou igual a 0.")

        if reservas_horas_fecho < 0:
            raise forms.ValidationError("O fechamento das reservas deve ser maior ou igual a 0.")

        if reservas_horas_fecho >= reservas_horas_antes:
            raise forms.ValidationError(
                "O fechamento das reservas deve ocorrer antes do período de abertura."
            )

        if data_inicio and data_fim and data_inicio > data_fim:
            raise forms.ValidationError("A data de início deve ser anterior ou igual à data de fim.")

        if hora_inicio and hora_fim and hora_inicio >= hora_fim:
            raise forms.ValidationError("A hora de início deve ser anterior à hora de fim.")

        if max_participantes is not None and max_participantes <= 0:
            raise forms.ValidationError("O número máximo de participantes deve ser maior que 0.")

        if max_lista_espera is not None and max_lista_espera < 0:
            raise forms.ValidationError("O número máximo de participantes na lista de espera deve ser maior ou igual a 0.")

        return cleaned_data
    




class EditarTreinoForm(ModelForm):
    class Meta:
        model = Treino
        fields = [
            'tipo_treino', 'data_inicio', 'data_fim', 'hora_inicio', 'hora_fim',
            'max_participantes', 'max_lista_espera', 'reservas_horas_antes',
            'reservas_horas_fecho', 'dia_da_semana',
        ]




class CriarRecordesForm(ModelForm):
    predefinidos = forms.ChoiceField(
        choices=[
            ('vazio', 'Escolhe uma opção'),
            ('peso_morto', 'Peso Morto'),
            ('agachamento_com_barra', 'Agachamento c/barra'),
            ('remada', 'Remada'),
            ('press_ombro', 'Press de Ombro'),
            ('flexoes', 'Flexões'),
            ('burpees', 'Burpees'),
            ('elevacao', 'Elevação'),
            ('agachamento_livre', 'Agachamento livre'),
        ],
        required=False  # PERMITE QUE SEJA OPCIONAL
    )

    data_do_recorde = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Recordes
        fields = ['nome', 'valor', 'data_do_recorde', 'predefinidos']

    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get('nome')
        predefinidos = cleaned_data.get('predefinidos')

        if not nome and (not predefinidos or predefinidos == 'vazio'):
            raise forms.ValidationError("Preencha pelo menos um dos campos: 'Nome' ou 'Exercícios Predefinidos'.")

        return cleaned_data

               

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['nome'].queryset = RecordesNomes.objects.filter(utilizador=user)

    


class CriarNomeRecordeForm(forms.ModelForm):
    class Meta:
        model = RecordesNomes
        fields = ['nome']

