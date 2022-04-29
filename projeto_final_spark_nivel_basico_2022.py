
# coding: utf-8

# # Projeto Final de Spark - Nível Básico
# * ## Enviar os dados para o HDFS (através do namenode pelo terminal)

# 1) Pelo terminal do WSL2,como administrador, dentro da pasta spark, baixe o arquivo de dados .rar dentro da pasta spark:

# In[ ]:


sudo curl -O https://mobileapps.saude.gov.br/esus-vepi/files/unAFkcaNDeXajurGB7LChj8SgQYS2ptm/04bd3419b22b9cc5c6efac2c6528100d_HIST_PAINEL_COVIDBR_06jul2021.rar


# ### Obs.: Caso o link venha a ficar inacessível, o arquivo está disponibilizado no diretório data do GitHub.
# ### Para instalar unrar no Ubuntu você precisa executar os seguintes comandos no terminal:

# In[ ]:


sudo apt-get update
sudo apt-get install unrar


# In[ ]:


2) Descompacte o arquivo .rar com o comando: sudo unrar x 04bd3419b22b9cc5c6efac2c6528100d_HIST_PAINEL_COVIDBR_06jul2021.rar


# In[ ]:


3) Crie um diretório input dentro da pasta spark: mkdir input


# In[ ]:


4) Envie os arquivos .csv para a pasta input: sudo mv *.csv /home/marco/projeto-final-spark/spark/input


# In[ ]:


### Verificando
marco@DESKTOP-G2455QH:~/projeto-final-spark/spark$ ls ./input/
HIST_PAINEL_COVIDBR_2020_Parte1_06jul2021.csv  HIST_PAINEL_COVIDBR_2021_Parte1_06jul2021.csv
HIST_PAINEL_COVIDBR_2020_Parte2_06jul2021.csv  HIST_PAINEL_COVIDBR_2021_Parte2_06jul2021.csv


# In[ ]:


5)Acesse o namenode utilizando o comando docker exec -it namenode bash.
marco@DESKTOP-G2455QH:~/projeto-final-spark/spark$  docker exec -it namenode bash


# In[ ]:


6) Crie a pasta projeto-final-spark no HDFS para salvar os arquivos de dados .CSV: hdfs dfs -mkdir -p /user/marco/projeto-final-spark
    
root@namenode:/# hdfs dfs -mkdir -p /user/marco/projeto-final-spark


# In[ ]:


7) Envie os arquivos de dados .CSV para a pasta projeto-final-spark no HDFS: hdfs dfs -put /input/*.csv /user/cicero/projeto-final-spark
root@namenode:/# hdfs dfs -put /input/*.csv /user/marco/projeto-final-spark


# In[ ]:


8) Confirme se os arquivos foram enviados: hdfs dfs -ls /user/marco/projeto-final-spark
    root@namenode:/# hdfs dfs -ls /user/marco/projeto-final-spark
Found 4 items
-rw-r--r--   3 root supergroup   62492959 2022-04-26 02:39 /user/marco/projeto-final-spark/HIST_PAINEL_COVIDBR_2020_Parte1_06jul2021.csv
-rw-r--r--   3 root supergroup   76520681 2022-04-26 02:39 /user/marco/projeto-final-spark/HIST_PAINEL_COVIDBR_2020_Parte2_06jul2021.csv
-rw-r--r--   3 root supergroup   91120916 2022-04-26 02:39 /user/marco/projeto-final-spark/HIST_PAINEL_COVIDBR_2021_Parte1_06jul2021.csv
-rw-r--r--   3 root supergroup    3046774 2022-04-26 02:39 /user/marco/projeto-final-spark/HIST_PAINEL_COVIDBR_2021_Parte2_06jul2021.csv
r


# # No jupyter notbook....

# # Otimizar todos os dados do hdfs para uma tabela Hive particionada por município

# In[1]:


# Criar Sessão Spark
'''
As vantagens de se utilizar a Classe SparkSession é que a mesma fornece acesso às funcionalidades do spark:
•sql Executa as consultas Spark SQL
•catalog Gerenciar tabelas
•read função para ler dados de um arquivo ou outra fonte de dados
•conf objeto para gerenciar configurações de Spark
•sparkContext Core Spark API
'''


# In[2]:


from pyspark.sql.functions import *

spark = SparkSession.builder.appName('Projeto final de Spark - Campanha Nacional de Vacinação contra Covid-19').config('spark.some.config.option', 'some-value').enableHiveSupport().getOrCreate()


# In[3]:


from pyspark.sql  import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession


# In[4]:


#Utilizando o option("inferSchema","true") para que automaticamente o spark identifique os tipos de dados das colunas
#df_painel_covidbr = spark.read.option("sep",";").option("header","true").option("inferSchema","true").csv("hdfs:///user/cicero/projeto-final-spark/")

df_painel_covidbr = spark.read.csv('hdfs://namenode/user/marco/projeto-final-spark/', 
                                   sep=";", #sep(padrão ,): define o único caractere como separador para cada campo e valor.
                                   header=True, #header(padrão false): usa a primeira linha como nomes de colunas.
                                   inferSchema=True, #inferSchema(padrão false): infere o esquema de entrada automaticamente a partir dos dados. 
                                   ignoreLeadingWhiteSpace=True, #ignoreLeadingWhiteSpace(padrão false): define se os espaços em branco iniciais dos valores que estão sendo lidos devem ser ignorados.
                                   ignoreTrailingWhiteSpace=True) #ignoreTrailingWhiteSpace(padrão false): define se os espa


# In[7]:


#Visualizar o schema
#df_painel_covidbr.dtypes
df_painel_covidbr.printSchema()


# In[8]:


df_painel_covidbr.show()


# In[9]:



#from pyspark.sql.functions import *
# Ajustando os dados e removendo a informação de hora, pois todas estão zeradas
df_painel_covidbr_limpo = df_painel_covidbr.withColumn('data',from_unixtime(unix_timestamp(df_painel_covidbr.data), 'yyyy-MM-dd'))


# In[10]:


#Mostrando o novo dataframe com o campo data ajustado
df_painel_covidbr_limpo.show(3, vertical=True)


# In[11]:


#Otimizar dados por tabelas particionadas por município
spark.sql("CREATE DATABASE IF NOT EXISTS covidbr")
df_painel_covidbr_limpo.write.mode('overwrite').partitionBy('municipio').format('csv').saveAsTable('covidbr.municipio', path='hdfs://namenode:8020/user/hive/warehouse/covidbr/')


# In[12]:


#Confirmar se os dados foram salvos no diretório
get_ipython().system("hdfs dfs -ls 'hdfs://namenode:8020/user/hive/warehouse/covidbr/'")


# # Criar as 3 visualizações pelo Spark com os dados enviados para o HDFS

# In[13]:


# Acessar os dados da tabela municipio do Banco de dados covidbr pelo SparkSQL
spark.sql("SHOW DATABASES").show() #Mostrar os anco de dados


# In[14]:


# Selecionar o banco de dados covidbr 
spark.sql("USE covidbr")


# In[15]:


# Acessar os dados da tabela municipio do Banco de dados covidbr pelo SparkSQL
spark.sql("SHOW TABLES").show() #Mostrar os anco de dados


# # Visualização 1 - Casos Recuperados | Em Acompanhamento
# Obs.: Os resultados serão extraídos a partir da última data registrada que foi em 2021-07-06.

# In[16]:


## 1.1 Casos Recuperados
df_casos_recuperados = spark.sql("SELECT Recuperadosnovos as Casos_Recuperados FROM municipio order by 1 desc limit 1")
df_casos_recuperados.show()

## 1.2 Em Acompanhamento
df_em_acompanhamento = spark.sql("SELECT emAcompanhamentoNovos as Em_Acompanhamento FROM municipio WHERE order by 1 desc limit 1")
df_em_acompanhamento.show()


# ### Visualização 2 - Casos Acumulado | Casos Novos | Incidência
# Obs.: **Incidência:** Quantidade proporcional de casos confirmados para cada 1 milhão de habitantes. A população considerada no cálculo é a estimativa populacional para 2019 do Instituto Brasileiro de Geografia e Estatística (IBGE), salvo quando especificada referência distinta. **Método de cálculo: (casos confirmados * 1.000.000) / população**.
# Fonte: https://www.coronavirus.sc.gov.br/sobre-os-dados/.
# No caso no painel será utilizado **Método de cálculo: (casos confirmados * 100.000) / população**

# In[23]:


#2.1 Acumulado
df_casos_acumulados = spark.sql("SELECT casosAcumulado as Casos_Acumulados FROM municipio order by 1 desc limit 1")
df_casos_acumulados.show()

#2.2 Casos novos
df_casos_novos = spark.sql("SELECT casosNovos as Casos_Novos FROM municipio order by 1 desc limit 1")
df_casos_novos.show()

#2.3 Incidência (Casos acumulados)
df_incidencia = spark.sql("SELECT cast(((casosAcumulado*100000)/populacaoTCU2019) as decimal(5,1)) as Incidencia FROM municipio order by 1 desc limit 1")
df_incidencia.show()


# ### Visualização 3 - Óbtos Acumulados | Óbtos Novos | Letalidade | Mortalidade
# Obs.1: **Letalidade:** Taxa percentual de casos confirmados que evoluíram a óbito. **Método de cálculo: (número de óbitos x 100) / número de casos confirmados**.
# 
# Obs.2: **Mortalidade:** Quantidade proporcional de óbitos para cada 1 milhão habitantes, seguindo a mesma metodologia de cálculo da incidência de casos confirmados. **Método de cálculo: (óbitos * 1.000.000) / população**.
# No caso no painel será utilizado **Método de cálculo: (óbitos * 100.000) / população**
# Fonte: https://www.coronavirus.sc.gov.br/sobre-os-dados/

# In[17]:


#3.1 Óbitos acumulados
df_obitos_acumulados = spark.sql("SELECT obitosAcumulado as Obitos_Acumulados FROM municipio order by 1 desc limit 1")
df_obitos_acumulados.show()


# In[18]:


#3.2 Obitos novos
df_obitos_novos = spark.sql("SELECT obitosNovos as Obitos_Novos FROM municipio order by 1 desc limit 1")
df_obitos_novos.show()

#3.3 Letalidade
df_letalidade = spark.sql("SELECT cast(((obitosAcumulado * 100) / casosAcumulado) as decimal(5,1)) as Letalidade FROM municipio order by 1 desc limit 1")
df_letalidade.show()

#3.4 Mortalidade
df_mortalidade = spark.sql("SELECT cast(((obitosAcumulado * 100000) / populacaoTCU2019) as decimal(4,1)) as Mortalidade FROM municipio order by 1 desc limit 1")
df_mortalidade.show()


# ## Salvar a primeira visualização como tabela Hive

# In[19]:


df_casos_recuperados.write.format('csv').saveAsTable('Recuperados')


# In[20]:


df_em_acompanhamento.write.format('csv').saveAsTable('Acompanhamento')


# In[21]:


#Visualizar as tabelas salvas 
spark.sql('SHOW TABLES').show()


# ## Salvar a segunda visualização com formato parquet e compressão snappy

# In[24]:


df_casos_acumulados.write.option('compression', 'snappy').parquet('hdfs://namenode/user/marco/projeto-final-spark/visualizacao/Casos_Acumulados')


# In[27]:


df_casos_novos.write.option('compression', 'snappy').parquet('hdfs://namenode/user/marco/projeto-final-spark/visualizacao/Casos_Novos')

## Ocorreu o erro pois já existia... 


# In[28]:


df_incidencia.write.option('compression', 'snappy').parquet('hdfs://namenode/user/marco/projeto-final-spark/visualizacao/Incidencia')


# In[29]:


#Visualizar os dodos na pasta do HDFS
get_ipython().system("hdfs dfs -ls 'hdfs://namenode/user/marco/projeto-final-spark/visualizacao'")


# ## Salvar a terceira visualização em um tópico no Kafka
# ⚠ Diferente dos formatos nativos do spark para salvamento direto no HDFS,o Kafka permite apenas salvamento de dados únicos de tipo String em DataFrames de formato JSON. Por isso, iremos convertêlos antes de salvarmos em um tópico.

# In[32]:


#3.1 Óbitos acumulados
obitos_acumulados_json = df_obitos_acumulados.select(to_json(struct('obitos_Acumulados')).alias('value'))
obitos_acumulados_json.show(n=1, truncate=False, vertical=False)


# In[33]:


#3.2 Obitos novos
obitos_novos_json = df_obitos_novos.select(to_json(struct('obitos_Novos')).alias('value'))
obitos_novos_json.show(n=1, truncate=False, vertical=False)


# In[34]:


#3.3 Letalidade
letalidade_json = df_letalidade.select(to_json(struct('Letalidade')).alias('value'))
letalidade_json.show(n=1, truncate=False, vertical=False)


# In[35]:


#3.4 Mortalidade
mortalidade_json = df_mortalidade.select(to_json(struct('Mortalidade')).alias('value'))
mortalidade_json.show(n=1, truncate=False, vertical=False)


# ## Salvando os Dataframes convertidos em JSON em tópicos do Kafka

# In[36]:


df_obitos_acumulados.selectExpr('to_json(struct(*)) As value').write.format('kafka').option('kafka.bootstrap.servers', 'kafka:9092').option('topic', 'topic-obtidos_acumulados').save()


# In[37]:


df_obitos_novos.selectExpr('to_json(struct(*)) As value').write.format("kafka").option("kafka.bootstrap.servers","kafka:9092").option("topic","topic-obitos_novos").save()


# In[38]:


df_letalidade.selectExpr('to_json(struct(*)) As value').write.format("kafka").option("kafka.bootstrap.servers","kafka:9092").option("topic","topic-letalidade").save()


# In[39]:


df_mortalidade.selectExpr('to_json(struct(*)) As value').write.format("kafka").option("kafka.bootstrap.servers","kafka:9092").option("topic","topic-mortalidade").save()


# # Criar a visualização pelo Spark com os dados enviados para o HDFS

# In[68]:


df_spark = spark.sql('''SELECT regiao as Regiao, 
                     MAX(casosAcumulado) as Casos, 
                     MAX(obitosAcumulado) as Obitos, 
                     MAX(data) as Atualizacao 
                     FROM municipio 
                     GROUP BY regiao 
                     ORDER BY regiao''')

df_spark.show()

df_spark.printSchema()


# In[48]:


df_spark.limit(10).toPandas()


# Fontes de consultas:
# pyspark.sql module: https://spark.apache.org/docs/2.0.2/api/python/pyspark.sql.html#module-pyspark.sql.functions
# Spark SQL, DataFrames and Datasets Guide: https://spark.apache.org/docs/2.0.2/sql-programming-guide.html#sql
# Spark SQL Guide: https://spark.apache.org/docs/latest/sql-getting-started.html
# Como obter no SQL o último registro inserido de acordo com sua data: https://pt.stackoverflow.com/questions/13125/como-obter-no-sql-o-%C3%BAltimo-registro-inserido-de-acordo-com-sua-data
# Sobre os dados do Coronavirus: https://www.coronavirus.sc.gov.br/sobre-os-dados/
# Projeção da população do Brasil: https://www.ibge.gov.br/apps/populacao/projecao/index.html
# CAST para DECIMAL no MySQL: https://stackoverflow.com/questions/11830509/cast-to-decimal-in-mysql
# Tutorial: Usar o fluxo estruturado do Apache Spark com o Apache Kafka no HDInsight: https://docs.microsoft.com/pt-br/azure/hdinsight/hdinsight-apache-kafka-spark-structured-streaming
