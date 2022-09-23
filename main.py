import tweepy
import dotenv
import os
from datetime import datetime
from time import sleep
from discord_webhook import DiscordWebhook
import utils.functions as functions

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
# access_token_dot = os.environ['ACESS_TOKEN']
# access_token_secret_dot = os.environ['ACESS_TOKEN_SECRET']
# consumer_key_dot = os.environ['CONSUMER_KEY']
# consumer_secret_dot = os.environ['CONSUMER_SECRET']
# webhook_url_dot = os.environ['WEBHOOK_URL']
# data_ferias_dot  = os.environ['DATA_FERIAS'] 

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

    # Loopin
    while True:
        timeline = api.user_timeline()
        ultimo_post = timeline[0].text
        dias_ferias = functions.dias_restantes_ferias(dia_ferias_dot, mes_ferias_dot, ano_ferias_dot)
        mensagem = functions.mensagens_enviar(dias_ferias)
        print(dias_ferias)
        if ultimo_post == mensagem:
            print("Um post já foi realizado hoje.")
            webhook = DiscordWebhook(url=webhook_url_dot, content='Um post já foi realizado hoje.')
            webhook.execute()
        elif dias_ferias < -1:
            print("As férias já começaram, nenhuma nova postagem será enviada.")
            print("Lembre-se de atualizar o dia, mês e ano das férias no arquivo .env")
            webhook = DiscordWebhook(url=webhook_url_dot, content='As férias já começaram, nenhuma nova postagem será enviada.')
            webhook.execute()
            webhook = DiscordWebhook(url=webhook_url_dot, content='Lembre-se de atualizar a data das férias / retorno das aulas no arquivo .env')
            webhook.execute()
        else:
            api.update_status(mensagem)
            print("Um novo post acaba de ser realizado.")
            webhook = DiscordWebhook(url=webhook_url_dot, content='Um novo post acaba de ser realizado.')
            webhook.execute()
        sleep(600)

if __name__ == "__main__":
    main()

