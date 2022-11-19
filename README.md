
# twitter-bot-ferias

twitter-bot-ferias é uma aplicação que realiza postagens diárias contendo os dias restantes paras as férias.


## Demonstração

![imagem](https://i.imgur.com/8rca06e.png)
## Instalação

Para rodar a aplicação é necessário instalar as seguintes bibliotecas:

```bash
    pip install tweepy
    pip install python-dotenv
    pip install pytz
    pip install discord-webhook
```
## Variáveis de Ambiente

As seguintes variáveis de ambiente devem ser preenchidas no .env

`API_KEY`

`API_KEY_SECRET`

`ACESS_TOKEN`

`ACESS_TOKEN_SECRET`

`WEBHOOK_URL`

Para obter estas chaves é necessário criar uma
[conta de desenvolvedor](https://developer.twitter.com/en/portal/dashboard) no twitter

**Observação:** É necessário 
[solicitar acesso elevado](https://developer.twitter.com/en/portal/products/elevated) a API do twitter.
## FAQ


#### 1- Posso remover o Webhook do Discord?

Sim, caso deseje remover a integração com o webhook basta remover todas as linhas de código que se inicie com `webhook`.

#### 2- A aplicação envia posts durante as férias?

Não, após o ínicio das férias a aplicação realiza avisos pedindo que novas datas sejam configuradas.

#### 3- Posso deixar a aplicação já configurada antes do ínicio das aulas?

Sim, você já pode deixar os campos `DATA_INICIO_AULAS` e `DATA_INICIO_FERIAS` configurados antes mesmo do ínicio das aulas.
Os posts só são realizadas após o ínicio das aulas.

#### 4- A aplicação realiza varias postagens no dia?

Não, a aplicação realiza a cada duas horas uma verificação para tentar realizar um novo post.
Caso o post do dia já tenha sido enviado uma nova postagem não é realizada.

#### 5- As postagens são sempre iguais?

Não, as mensagens podem variar de acordo com os dias restantes de aula. Caso queira adicionar mais
variedades de mensagens basta editar a função `mensagens_enviar` localizada no arquivo `utils/functions.py`.
#### 6- A postagem é realizada em qualquer hórario do dia?

Não, o hórario predefinido para as postagens é de 7 horas da manhã até as 13:59 da tarde. Se por algum motivo todas as tentativas de postagens
falharem nesse hórario uma nova postagem será realizada apenas no dia seguinte.

#### 7- Qual fuso hórario a aplicação utiliza?

Por padrão a aplicação utiliza o fuso hórario `America/Sao_Paulo`,
## Licença

[MIT](https://choosealicense.com/licenses/mit/)

