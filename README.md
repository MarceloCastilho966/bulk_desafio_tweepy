<h1 align="center">Desafio Bulk Consulting</h1>

## Criação de uma Stream com Tweeter utilizando a API Tweepy, com uma breve analise dos dados coletados.

1. Primeiro é necessário a criação de um perfil de desenvolvedor no Twitter no link:
https://developer.twitter.com/en

2. Após a criação do seu perfil, será informado seu Bearer Token, que utilizaremos para criar a conexão

3. Agora criamos nossa conexão Stream utilizando Twitter API v2

'''
bearer_token = 'Seu Token aqui'


'''

4. Criamos o código para a execução da nossa Stream

'''
class MyStream(tweepy.StreamingClient):
    def on_connect(self): ## Chamado quando feita a conexão
        print("Conectado")  
        
    def on_connection_error(self): ## Caso apareça algum erro, é desconectado
        self.disconnect()
    
    def on_tweet(self, tweet): ## Pegando Tweets e salvando no csv
       print(tweet.author_id, tweet.text)
       with open('eleicoes2022.csv', 'a') as f:
            writer = csv.writer(f, delimiter="|")
            writer.writerow([tweet.author_id, tweet.text, tweet.created_at])
    
    def on_disconnect(self): ## Chamado quando desconectado
        print("Desconectado")

'''

5. Criação do Header do CSV

'''
with open('eleicoes2022.csv', 'w') as f:
    writer = csv.writer(f, delimiter='|')
    writer.writerow(['ID', 'Text', 'Data'])
    
'''

6. Conectando com Twitter

'''
stream = MyStream(bearer_token=bearer_token)

'''

7. Criação da regra para filtrar tweets

''''
rule = tweepy.StreamRule("""(#LulaNo1oturno OR #BolsonaroNoPrimeiroTurno22) 
-has:links -is:retweet -\n""") ## Pegando ambas as hashtags, sem links e sem retweets

stream.add_rules(rule)

'''

8. Iniciando a Stream, pegando o ID, Texto e Data/Hora

'''
stream.filter(expansions=['referenced_tweets.id'], tweet_fields=['author_id', 'created_at'])

'''

## Nossa Stream está pronta, funcionando, pegando os tweets e jogando para o CSV "eleições2022.csv"

#### Agora é hora de fazermos uma breve analise desses dados:


1.  Leitura e limpeza dos dados recebidos

'''
df = spark.read.csv('/home/marcelo/eleicoes2022.csv',header=True, sep='|', multiLine=True, escape='"')
df.show(5)

'''

2. To Pandas

'''
pandasDF = df.toPandas()

'''

3. Criando DF das duas hashtags buscadas

'''
bolsonaro = pandasDF.query('Text.str.contains("#BolsonaroNoPrimeiroTurno22")', engine='python')

lula = pandasDF.query('Text.str.contains("#LulaNo1oturno")', engine='python')

'''

4. Contagem de Tweets:

'''
count_total = pandasDF['ID'].count()
count_bolsonaro = bolsonaro['Text'].count()
count_lula = lula['Text'].count()
print('Contagem de Tweets: \n')
print('-'*40)
print(f'Total: {count_total} \n')
print(f'BolsonaroNoPrimeiroTurno22: {count_bolsonaro} \n')
print(f'LulaNo1oturno: {count_lula}')
print('-'*40)

'''
Contagem de Tweets: 

----------------------------------------
Total: 3229 

BolsonaroNoPrimeiroTurno22: 1631 

LulaNo1oturno: 637
----------------------------------------


5. Criando Gŕafico da contagem

'''
nomes = ['Total', 'Bolsonaro', 'Lula']
valores = [count_total, count_bolsonaro, count_lula]

plt.figure(figsize=(15, 5))
plt.subplot(131)
plt.bar(nomes, valores)

'''

### Contador das palavras mais utilizadas nos tweets e seu respectivo gráfico

1. Geral 

'''
top_N = 5
a = pandasDF['Text'].str.cat(sep=' ')
words = nltk.tokenize.word_tokenize(a)
words = [word for word in words if len(word) > 4]
word_dist = nltk.FreqDist(words)
rslt = pd.DataFrame(word_dist.most_common(top_N),
                    columns=['Palavra', 'Frequencia'])
display(rslt)

'''

'''
df1 = sns.load_dataset('tips')
plt.figure(figsize=(15, 5))
sns.lineplot(data=rslt, x="Palavra", y="Frequencia")
plt.show()

'''

2. #BolsonaroNoPrimeiroTurno22

'''
top_N = 5
a = bolsonaro['Text'].str.cat(sep=' ')
words = nltk.tokenize.word_tokenize(a)
words = [word for word in words if len(word) > 4]
word_dist = nltk.FreqDist(words)
rslt1 = pd.DataFrame(word_dist.most_common(top_N),
                    columns=['Palavra', 'Frequencia'])
display(rslt1)

'''

'''
df1 = sns.load_dataset('tips')
plt.figure(figsize=(15, 5))
sns.lineplot(data=rslt1, x="Palavra", y="Frequencia")
plt.show()

'''

3. #LulaNo1oturno

'''
top_N = 5
a = lula['Text'].str.cat(sep=' ')
words = nltk.tokenize.word_tokenize(a)
words = [word for word in words if len(word) > 3]
word_dist = nltk.FreqDist(words)
rslt2 = pd.DataFrame(word_dist.most_common(top_N),
                    columns=['Palavra', 'Frequencia'])
display(rslt2)

'''

'''
df1 = sns.load_dataset('tips')
plt.figure(figsize=(15, 5))
sns.lineplot(data=rslt2, x="Palavra", y="Frequencia")
plt.show()

'''












