import tweepy
import dotenv
import os
from datetime import datetime
from time import sleep
from discord_webhook import DiscordWebhook
import utils.functions as functions
from pytz import timezone


DATA_INICIO_AULAS = "08/09/2022"
DATA_INICIO_FERIAS = "19/12/2022"


def main():
    dotenv.load_dotenv(dotenv.find_dotenv())
    api_key = str(os.getenv("API_KEY"))
    api_key_secrect = str(os.getenv("API_KEY_SECRET"))
    access_token = str(os.getenv("ACESS_TOKEN"))
    access_token_secret = str(os.getenv("ACESS_TOKEN_SECRET"))
    webhook_url = str(os.getenv("WEBHOOK_URL"))

    data_ferias_temp = datetime.strptime(DATA_INICIO_FERIAS, "%d/%m/%Y")
    dia_ferias = data_ferias_temp.day
    mes_ferias = data_ferias_temp.month
    ano_ferias = data_ferias_temp.year

    data_inicio_temp = datetime.strptime(DATA_INICIO_AULAS, "%d/%m/%Y")
    dia_inicio_aulas = data_inicio_temp.day
    mes_inicio_aulas = data_inicio_temp.month
    ano_inicio_aulas = data_inicio_temp.year

    auth = tweepy.OAuthHandler(api_key, api_key_secrect)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Verificar se a autenticação foi bem sucedida
    try:
        api.verify_credentials()
        print("Autenticação bem sucedida")
        webhook = DiscordWebhook(url=webhook_url, content='Aplicação autenticada com sucesso.')
        webhook.execute()
    except Exception as e:
        print("Erro durante a autenticação\n")
        print(e)
        webhook = DiscordWebhook(url=webhook_url, content='Erro durante a autenticação.')
        webhook.execute()
        webhook = DiscordWebhook(url=webhook_url, content=e)
        webhook.execute()

    while True:
        try:
            timeline = api.user_timeline(tweet_mode="extended")
            if len(timeline) > 0:
                ultimo_post = timeline[0].full_text
            else:
                ultimo_post = ''

            dias_inicio_ferias = functions.diferenca_de_dias(dia_ferias, mes_ferias, ano_ferias)
            dias_inicio_aulas = functions.diferenca_de_dias(dia_inicio_aulas, mes_inicio_aulas, ano_inicio_aulas)
            
            mensagem = functions.mensagens_enviar(dias_inicio_ferias, dias_inicio_aulas)

            hora_atual = datetime.now(timezone('America/Sao_Paulo'))
            hora_atual = hora_atual.strftime("%H")
            hora_atual = int(hora_atual)

            # Verificar se o inicio das aulas já começou
            if dias_inicio_aulas > 0:
                print(f"O dia de retorno as aulas nao chegou, faltam {dias_inicio_aulas} dia/s.")
                webhook = DiscordWebhook(url=webhook_url, content=f'O dia de retorno as aulas nao chegou, faltam {dias_inicio_aulas} dia/s.')
                webhook.execute()

            # Verifica se o último post é igual a mensagem que esta tentando ser enviada
            elif ultimo_post == mensagem:
                print("O post do dia já foi enviado.")
                webhook = DiscordWebhook(url=webhook_url, content='O post do dia já foi enviado.')
                webhook.execute()

            # Verifica se as férias já começaram
            elif dias_inicio_ferias < 0:
                print("As férias já começaram, nenhuma nova postagem será enviada.")
                print("Lembre-se de atualizar as datas de inicio das aulas e férias.")
                webhook = DiscordWebhook(url=webhook_url, content='As férias já começaram, nenhuma nova postagem será enviada.')
                webhook.execute()
                webhook = DiscordWebhook(url=webhook_url, content='Lembre-se de atualizar as datas no arquivo .env ou no site do repl.it')
                webhook.execute()

            # Verifica se é um horário válido para postar
            elif not (hora_atual >= 7 and hora_atual <= 13):
                print("Uma postagem esta disponível para ser realizada, mas o horário ideal para postar ainda não foi atingido.")
                webhook = DiscordWebhook(url=webhook_url, content='Uma postagem esta disponível para ser realizada, mas o horário ideal para postar ainda não foi atingido.')
                webhook.execute()

            # Caso os requisitos sejam atendidos, o post é realizado (ou seja, o último post não é igual a mensagem que será enviada, as férias ainda não começaram e é um horário válido para postar)
            else:
                api.update_status(mensagem)
                print("Um novo post acaba de ser realizado.")
                webhook = DiscordWebhook(url=webhook_url, content='Um novo post acaba de ser realizado.')
                webhook.execute()
                print(f'Conteúdo do post: {mensagem}')
                webhook = DiscordWebhook(url=webhook_url, content=f'Conteúdo do post: {mensagem}')
                webhook.execute()

            sleep(7200) # Delay de 2 hora (7200 segundos) para verificar novamente os requisitos para realizar um novo post
        
        except Exception as e:
            print("Erro durante a execução do programa, tentando novamente em 15 minutos. \nErro: ")
            print(e)
            webhook = DiscordWebhook(url=webhook_url, content='Erro durante a execução do programa, tentando novamente em 15 minutos. \nErro: ')
            webhook.execute()
            webhook = DiscordWebhook(url=webhook_url, content=e)
            webhook.execute()
            sleep(900) # Delay de 15 minutos (900 segundos) para tentar novamente em caso de erro


if __name__ == "__main__":
    main()

