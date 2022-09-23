from datetime import date
from time import sleep

def dias_restantes_ferias(dia_ferias, mes_ferias, ano_ferias):
    data_hoje = date.today()
    data_ferias = date(ano_ferias, mes_ferias, dia_ferias)
    delta = data_ferias - data_hoje
    return delta.days

# Qual mensagem será enviada
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