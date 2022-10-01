from datetime import date
from datetime import datetime
from pytz import timezone


# Contar a diferença entre as datas
def diferenca_de_dias(dia, mes, ano):

    # Pegar a data atual na timezone de São Paulo e converter para o formato date
    data_hoje = datetime.now(timezone('America/Sao_Paulo'))
    data_hoje = data_hoje.date()

    # Pegar a data das férias na timezone de São Paulo e converter para o formato date
    data = date(ano, mes, dia)

    # Calcular a diferença entre as datas
    delta = data - data_hoje
    return delta.days


# Verificar qual mensagem deve ser postada
def mensagens_enviar(dias_restantes, dias_inicio):
    if dias_inicio == 0:
        mensagem = f"Hoje é o primeiro dia de longos {dias_restantes} dias até as férias. Boa sorte a todos!"
    elif dias_restantes <= 0:
        mensagem = "Finalmente as férias começaram!!"
    elif dias_restantes == 1:
        mensagem = "Hoje é o último dia de aula!!"
    elif dias_restantes <= 10:
        mensagem = f"Restam apenas {dias_restantes} dias de sofrimento!"
    elif dias_restantes <= 20:
        mensagem = f"Estamos na contagem regressiva para as férias! Faltam {dias_restantes} dias."
    elif dias_restantes <= 30:
        mensagem = f"Faltam apenas {dias_restantes} dias para as férias!"
    else:
        mensagem = f"Faltam {dias_restantes} dias para as férias!"
    return mensagem
