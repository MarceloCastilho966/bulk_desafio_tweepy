from os import sep
import tweepy
import csv
import time

# Token de conexão entre Tweepy e Twitter
bearer_token = 'seu token aqui'

class MyStream(tweepy.StreamingClient):
    # Função é chamada quando stream está funcioando
    def on_connect(self):
        print("Conectado")
    

    # Função é chamada para ler e escrever os tweets
    def on_tweet(self, tweet):
       print(tweet.author_id, tweet.text)
       with open('eleicoes2022.csv', 'a') as f:
            writer = csv.writer(f, delimiter="|")
            writer.writerow([tweet.author_id, tweet.text, tweet.created_at])

    def on_disconnect(self):
        print("desconectado")

# Criação do Csv para escrita de dados
with open('eleicoes2022.csv', 'w') as f:
    writer = csv.writer(f, delimiter='|')
    writer.writerow(['ID', 'Text', 'Data'])
    

# Conectando com Twitter
stream = MyStream(bearer_token=bearer_token)

# Criação da regra de pesquisa, sem pegar retweets
rule = tweepy.StreamRule("""(#LulaNo1oturno OR #BolsonaroNoPrimeiroTurno22) 
-has:links -is:retweet -\n""")

stream.add_rules(rule)

stream.filter(expansions=['referenced_tweets.id'], tweet_fields=['author_id', 'created_at'])



