import tweepy
import dotenv
import os
from datetime import date
from time import sleep

dotenv.load_dotenv(dotenv.find_dotenv())
access_token_dot = os.getenv("ACESS_TOKEN")
access_token_secret_dot = os.getenv("ACESS_TOKEN_SECRET")
consumer_key_dot = os.getenv("CONSUMER_KEY")
consumer_secret_dot = os.getenv("CONSUMER_SECRET")


access_token_dot = str(access_token_dot)
access_token_secret_dot = str(access_token_secret_dot)
consumer_key_dot = str(consumer_key_dot)
consumer_secret_dot = str(consumer_secret_dot)

auth = tweepy.OAuthHandler(consumer_key_dot, consumer_secret_dot)
auth.set_access_token(access_token_dot, access_token_secret_dot)
api = tweepy.API(auth)

# Verificar se a autenticação foi bem sucedida
try:
    api.verify_credentials()
    print("Autenticação bem sucedida")
except Exception as e:
    print("Erro durante a autenticação\n")
    print(e)

# Calcular primeiro dia do ano até uma data
def dias_ate_data(dia, mes, ano, bissexto, meses_31, meses_30):
    dias = 0
    for i in range(1, mes):
        if i == 2:
            if bissexto:
                dias += 29
            else:
                dias += 28
        elif i in meses_31:
            dias += 31
        elif i in meses_30:
            dias += 30
    dias += dia
    return dias

# Função main
def main():

    # Loopin
    while True:
        data_atual = date.today()
        dia = data_atual.day
        mes = data_atual.month
        ano = data_atual.year

        # Meses 
        meses_31 = [1, 3, 5, 7, 8, 10, 12]
        meses_30 = [4, 6, 9, 11]

        bissexto = False

        # Calcular ano bissexto
        if ano % 4 == 0:
            if ano % 100 == 0:
                if ano % 400 == 0:
                    bissexto = True
                else:
                    bissexto = False
            else:
                bissexto = True

        dia_ferias = dias_ate_data(19, 12, 2022, bissexto, meses_31, meses_30)
        dia_atual = dias_ate_data(dia, mes, ano, bissexto, meses_31, meses_30)
        timeline = api.user_timeline()
        ultimo_post = timeline[0].text
        post_hoje = f"Faltam apenas {dia_ferias - dia_atual} dias para as férias de 2022!"
        if ultimo_post == post_hoje:
            print("Post já feito")
        else:
            api.update_status(post_hoje)
            print("Post feito com sucesso")
            
        sleep(300)

if __name__ == "__main__":
    main()
