from django import forms
from django.forms import ModelForm
from .models import *
import re
from django.contrib.auth.forms import PasswordChangeForm
import dns.resolver
from django.core.exceptions import ValidationError


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
    como_teve_conhecimento_existencia_fitclub = forms.ChoiceField(choices=Utilizadores.CONHECIMENTO_FITCLUB, widget=forms.Select(attrs={
        'class':'form-control'
    }))

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email:
            try:
                nome, dominio = email.split('@')

                # Consulta registros MX para o domínio
                registros_mx = dns.resolver.resolve(dominio, 'MX')

                # Se não houver registros MX, o domínio não tem servidor de e-mail
                if not registros_mx:
                    raise ValidationError(f"'{dominio}' não é válido.")

            except dns.resolver.NXDOMAIN:
                raise ValidationError(f"O domínio '{dominio}' não é válido.")

            except dns.resolver.NoAnswer:
                raise ValidationError(f"'{dominio}' não é válido.")

            except dns.exception.Timeout:
                raise ValidationError("Erro ao verificar o e-mail. Tente novamente mais tarde.")

        return email


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


class AlterarSenhaForm(PasswordChangeForm):
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Atual'}),
        label=''
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Nova Password'}),
        label=''
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Password'}),
        label=''
    )




class InformacoesPessoaisForm(forms.ModelForm):
    class Meta:
        model = Utilizadores
        fields = ['email', 'username', 'data_nascimento', 'genero', 'morada', 'codigo_postal', 'localidade', 'contacto',
                  'nif', 'pretende_recibo', 'profissao', 'classificacao_esforco_na_profissao', 'fumador', 'problemas_saude', 'limitacoes_para_pratica_exercicio_fisico', 'como_teve_conhecimento_existencia_fitclub']
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
                  'nif', 'pretende_recibo', 'profissao', 'classificacao_esforco_na_profissao', 'fumador', 'problemas_saude', 'limitacoes_para_pratica_exercicio_fisico', 'is_staff', 'como_teve_conhecimento_existencia_fitclub']
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
    dia_da_semana = forms.MultipleChoiceField(
        choices=Treino.DIAS_DA_SEMANA_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label="Dias da Semana"
    )


    




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



class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not Utilizadores.objects.filter(email=email).exists():
            raise forms.ValidationError("E-mail não encontrado.")
        return email


class SetNewPasswordForm(forms.Form):
    new_password1 = forms.CharField(label="Nova password", widget=forms.PasswordInput)
    new_password2 = forms.CharField(label="Confirmar password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords não coincidem.")
        return cleaned_data
