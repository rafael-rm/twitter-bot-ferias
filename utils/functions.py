from datetime import date
from datetime import datetime
from pytz import timezone


# Contar os dias restantes até uma determinada data
def dias_restantes_ferias(dia_ferias, mes_ferias, ano_ferias):

    # Pegar a data atual na timezone de São Paulo e converter para o formato date
    data_hoje = date.today()
    data_hoje = datetime(data_hoje.year, data_hoje.month, data_hoje.day)
    data_hoje = timezone('America/Sao_Paulo').localize(data_hoje)
    data_hoje = data_hoje.date()

    # Pegar a data das férias na timezone de São Paulo e converter para o formato date
    data_ferias = date(ano_ferias, mes_ferias, dia_ferias)

    # Calcular a diferença entre as datas
    delta = data_ferias - data_hoje
    return delta.days


# Verificar qual mensagem deve ser postada
def mensagens_enviar(dias_restantes):
    if dias_restantes == -1:
        mensagem = "Finalmente as férias começaram!"
    elif dias_restantes == 0:
        mensagem = "Hoje é o último dia de aula!"
    elif dias_restantes == 1:
        mensagem = "Falta apenas 1 dia para as férias =)"
    elif dias_restantes == 10:
        mensagem = "Restam apenas 10 dias de sofrimento!"
    else:
        mensagem = f"Faltam apenas {dias_restantes} dias para as férias!"
    return mensagem