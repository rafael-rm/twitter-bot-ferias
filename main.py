import tweepy
import dotenv
import os
from datetime import datetime
from time import sleep
from discord_webhook import DiscordWebhook
import utils.functions as functions
from pytz import timezone

# USAR NO LOCALHOST
# Carregando as variáveis de ambiente
dotenv.load_dotenv(dotenv.find_dotenv())
access_token_dot = os.getenv("ACESS_TOKEN")
access_token_secret_dot = os.getenv("ACESS_TOKEN_SECRET")
consumer_key_dot = os.getenv("CONSUMER_KEY")
consumer_secret_dot = os.getenv("CONSUMER_SECRET")
webhook_url_dot = os.getenv("WEBHOOK_URL")
data_ferias_dot = os.getenv("DATA_FERIAS")

# USAR NO REPL.IT
# Carregando as variáveis de ambiente
#access_token_dot = os.environ['ACESS_TOKEN']
#access_token_secret_dot = os.environ['ACESS_TOKEN_SECRET']
#consumer_key_dot = os.environ['CONSUMER_KEY']
#consumer_secret_dot = os.environ['CONSUMER_SECRET']
#webhook_url_dot = os.environ['WEBHOOK_URL']
#data_ferias_dot  = os.environ['DATA_FERIAS'] 

access_token_dot = str(access_token_dot)
access_token_secret_dot = str(access_token_secret_dot)
consumer_key_dot = str(consumer_key_dot)
consumer_secret_dot = str(consumer_secret_dot)

data_ferias_temp = datetime.strptime(data_ferias_dot, "%d/%m/%Y")
dia_ferias_dot = data_ferias_temp.day
mes_ferias_dot = data_ferias_temp.month
ano_ferias_dot = data_ferias_temp.year

auth = tweepy.OAuthHandler(consumer_key_dot, consumer_secret_dot)
auth.set_access_token(access_token_dot, access_token_secret_dot)
api = tweepy.API(auth)

# Verificar se a autenticação foi bem sucedida
try:
    api.verify_credentials()
    print("Autenticação bem sucedida")
    webhook = DiscordWebhook(url=webhook_url_dot, content='Aplicação autenticada com sucesso.')
    webhook.execute()
except Exception as e:
    print("Erro durante a autenticação\n")
    print(e)
    webhook = DiscordWebhook(url=webhook_url_dot, content='Erro durante a autenticação.')
    webhook.execute()
    webhook = DiscordWebhook(url=webhook_url_dot, content=e)
    webhook.execute()


# Função main
def main():

    while True:

        try:
            timeline = api.user_timeline()
            if len(timeline) > 0:
                ultimo_post = timeline[0].text
            else:
                ultimo_post = ''

            dias_ferias = functions.dias_restantes_ferias(dia_ferias_dot, mes_ferias_dot, ano_ferias_dot)
            mensagem = functions.mensagens_enviar(dias_ferias)

            # Pegar a hora atual na timezone de São Paulo
            hora_atual = datetime.now(timezone('America/Sao_Paulo'))
            hora_atual = hora_atual.strftime("%H")
            hora_atual = int(hora_atual)

            # Verifica se o último post é igual a mensagem que esta tentando ser enviada
            if ultimo_post == mensagem:
                print("O post do dia já foi enviado.")
                webhook = DiscordWebhook(url=webhook_url_dot, content='O post do dia já foi enviado.')
                webhook.execute()

            # Verifica se as férias já começaram
            elif dias_ferias < 0:
                print("As férias já começaram, nenhuma nova postagem será enviada.")
                print("Lembre-se de atualizar o dia, mês e ano das férias no arquivo .env ou no site do repl.it")
                webhook = DiscordWebhook(url=webhook_url_dot, content='As férias já começaram, nenhuma nova postagem será enviada.')
                webhook.execute()
                webhook = DiscordWebhook(url=webhook_url_dot, content='Lembre-se de atualizar o dia, mês e ano das férias no arquivo .env ou no site do repl.it')
                webhook.execute()

            # Verifica se é um horário válido para postar
            elif not (hora_atual >= 8 and hora_atual <= 12):
                print("Uma postagem esta disponível para ser realizada, mas o horário ainda não foi atingido.")
                webhook = DiscordWebhook(url=webhook_url_dot, content='Uma postagem esta disponível para ser realizada, mas o horário ainda não foi atingido.')
                webhook.execute()

            # Caso os requisitos sejam atendidos, o post é realizado (ou seja, o último post não é igual a mensagem que será enviada, as férias ainda não começaram e é um horário válido para postar)
            else:
                api.update_status(mensagem)
                print("Um novo post acaba de ser realizado.")
                webhook = DiscordWebhook(url=webhook_url_dot, content='Um novo post acaba de ser realizado.')
                print(f'Conteúdo do post: {mensagem}')
                webhook = DiscordWebhook(url=webhook_url_dot, content=f'Conteúdo do post: {mensagem}')
                webhook.execute()

            sleep(3600) # Delay de 1 hora (3600 segundos) para verificar novamente os requisitos para realizar um novo post
        
        except Exception as e:
            print("Erro durante a execução do programa, tentando novamente em 15 minutos. \nErro: ")
            print(e)
            webhook = DiscordWebhook(url=webhook_url_dot, content='Erro durante a execução do programa, tentando novamente em 15 minutos. \nErro: ')
            webhook.execute()
            webhook = DiscordWebhook(url=webhook_url_dot, content=e)
            webhook.execute()
            sleep(900) # Delay de 15 minutos (900 segundos) para tentar novamente em caso de erro


if __name__ == "__main__":
    main()

