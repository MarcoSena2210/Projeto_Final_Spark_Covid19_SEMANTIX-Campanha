
# Projeto Final de Spark - Nível Básico
* ## Enviar os dados para o HDFS (através do namenode pelo terminal)

1) Pelo terminal do WSL2,como administrador, dentro da pasta spark, baixe o arquivo de dados .rar dentro da pasta spark:


```python
sudo curl -O https://mobileapps.saude.gov.br/esus-vepi/files/unAFkcaNDeXajurGB7LChj8SgQYS2ptm/04bd3419b22b9cc5c6efac2c6528100d_HIST_PAINEL_COVIDBR_06jul2021.rar
```

### Obs.: Caso o link venha a ficar inacessível, o arquivo está disponibilizado no diretório data do GitHub.
### Para instalar unrar no Ubuntu você precisa executar os seguintes comandos no terminal:


```python
sudo apt-get update
sudo apt-get install unrar
```


```python
2) Descompacte o arquivo .rar com o comando: sudo unrar x 04bd3419b22b9cc5c6efac2c6528100d_HIST_PAINEL_COVIDBR_06jul2021.rar
```


```python
3) Crie um diretório input dentro da pasta spark: mkdir input
```


```python
4) Envie os arquivos .csv para a pasta input: sudo mv *.csv /home/marco/projeto-final-spark/spark/input
```


```python
### Verificando
marco@DESKTOP-G2455QH:~/projeto-final-spark/spark$ ls ./input/
HIST_PAINEL_COVIDBR_2020_Parte1_06jul2021.csv  HIST_PAINEL_COVIDBR_2021_Parte1_06jul2021.csv
HIST_PAINEL_COVIDBR_2020_Parte2_06jul2021.csv  HIST_PAINEL_COVIDBR_2021_Parte2_06jul2021.csv
```


```python
5)Acesse o namenode utilizando o comando docker exec -it namenode bash.
marco@DESKTOP-G2455QH:~/projeto-final-spark/spark$  docker exec -it namenode bash
```


```python
6) Crie a pasta projeto-final-spark no HDFS para salvar os arquivos de dados .CSV: hdfs dfs -mkdir -p /user/marco/projeto-final-spark
    
root@namenode:/# hdfs dfs -mkdir -p /user/marco/projeto-final-spark
```


```python
7) Envie os arquivos de dados .CSV para a pasta projeto-final-spark no HDFS: hdfs dfs -put /input/*.csv /user/cicero/projeto-final-spark
root@namenode:/# hdfs dfs -put /input/*.csv /user/marco/projeto-final-spark

```


```python
8) Confirme se os arquivos foram enviados: hdfs dfs -ls /user/marco/projeto-final-spark
    root@namenode:/# hdfs dfs -ls /user/marco/projeto-final-spark
Found 4 items
-rw-r--r--   3 root supergroup   62492959 2022-04-26 02:39 /user/marco/projeto-final-spark/HIST_PAINEL_COVIDBR_2020_Parte1_06jul2021.csv
-rw-r--r--   3 root supergroup   76520681 2022-04-26 02:39 /user/marco/projeto-final-spark/HIST_PAINEL_COVIDBR_2020_Parte2_06jul2021.csv
-rw-r--r--   3 root supergroup   91120916 2022-04-26 02:39 /user/marco/projeto-final-spark/HIST_PAINEL_COVIDBR_2021_Parte1_06jul2021.csv
-rw-r--r--   3 root supergroup    3046774 2022-04-26 02:39 /user/marco/projeto-final-spark/HIST_PAINEL_COVIDBR_2021_Parte2_06jul2021.csv
r
```

# No jupyter notbook....

# Otimizar todos os dados do hdfs para uma tabela Hive particionada por município


```python
# Criar Sessão Spark
'''
As vantagens de se utilizar a Classe SparkSession é que a mesma fornece acesso às funcionalidades do spark:
•sql Executa as consultas Spark SQL
•catalog Gerenciar tabelas
•read função para ler dados de um arquivo ou outra fonte de dados
•conf objeto para gerenciar configurações de Spark
•sparkContext Core Spark API
'''
```




    '\nAs vantagens de se utilizar a Classe SparkSession é que a mesma fornece acesso às funcionalidades do spark:\n•sql Executa as consultas Spark SQL\n•catalog Gerenciar tabelas\n•read função para ler dados de um arquivo ou outra fonte de dados\n•conf objeto para gerenciar configurações de Spark\n•sparkContext Core Spark API\n'




```python
from pyspark.sql.functions import *

spark = SparkSession\
.builder\
.appName('Projeto final de Spark - Campanha Nacional de Vacinação contra Covid-19')\
.config('spark.some.config.option', 'some-value')\
.enableHiveSupport()\
.getOrCreate()

```


```python
from pyspark.sql  import *
from pyspark.sql.types import *
from pyspark.sql import SparkSession
```


```python
#Utilizando o option("inferSchema","true") para que automaticamente o spark identifique os tipos de dados das colunas
#df_painel_covidbr = spark.read.option("sep",";").option("header","true").option("inferSchema","true").csv("hdfs:///user/cicero/projeto-final-spark/")

df_painel_covidbr = spark.read.csv('hdfs://namenode/user/marco/projeto-final-spark/', 
                                   sep=";", #sep(padrão ,): define o único caractere como separador para cada campo e valor.
                                   header=True, #header(padrão false): usa a primeira linha como nomes de colunas.
                                   inferSchema=True, #inferSchema(padrão false): infere o esquema de entrada automaticamente a partir dos dados. 
                                   ignoreLeadingWhiteSpace=True, #ignoreLeadingWhiteSpace(padrão false): define se os espaços em branco iniciais dos valores que estão sendo lidos devem ser ignorados.
                                   ignoreTrailingWhiteSpace=True) #ignoreTrailingWhiteSpace(padrão false): define se os espa
```


```python
#Visualizar o schema
#df_painel_covidbr.dtypes
df_painel_covidbr.printSchema()
```

    root
     |-- regiao: string (nullable = true)
     |-- estado: string (nullable = true)
     |-- municipio: string (nullable = true)
     |-- coduf: integer (nullable = true)
     |-- codmun: integer (nullable = true)
     |-- codRegiaoSaude: integer (nullable = true)
     |-- nomeRegiaoSaude: string (nullable = true)
     |-- data: timestamp (nullable = true)
     |-- semanaEpi: integer (nullable = true)
     |-- populacaoTCU2019: integer (nullable = true)
     |-- casosAcumulado: decimal(10,0) (nullable = true)
     |-- casosNovos: integer (nullable = true)
     |-- obitosAcumulado: integer (nullable = true)
     |-- obitosNovos: integer (nullable = true)
     |-- Recuperadosnovos: integer (nullable = true)
     |-- emAcompanhamentoNovos: integer (nullable = true)
     |-- interior/metropolitana: integer (nullable = true)
    



```python
df_painel_covidbr.show()
```

    +------+------+---------+-----+------+--------------+---------------+-------------------+---------+----------------+--------------+----------+---------------+-----------+----------------+---------------------+----------------------+
    |regiao|estado|municipio|coduf|codmun|codRegiaoSaude|nomeRegiaoSaude|               data|semanaEpi|populacaoTCU2019|casosAcumulado|casosNovos|obitosAcumulado|obitosNovos|Recuperadosnovos|emAcompanhamentoNovos|interior/metropolitana|
    +------+------+---------+-----+------+--------------+---------------+-------------------+---------+----------------+--------------+----------+---------------+-----------+----------------+---------------------+----------------------+
    |Brasil|  null|     null|   76|  null|          null|           null|2020-02-25 00:00:00|        9|       210147125|             0|         0|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-02-26 00:00:00|        9|       210147125|             1|         1|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-02-27 00:00:00|        9|       210147125|             1|         0|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-02-28 00:00:00|        9|       210147125|             1|         0|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-02-29 00:00:00|        9|       210147125|             2|         1|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-03-01 00:00:00|       10|       210147125|             2|         0|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-03-02 00:00:00|       10|       210147125|             2|         0|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-03-03 00:00:00|       10|       210147125|             2|         0|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-03-04 00:00:00|       10|       210147125|             3|         1|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-03-05 00:00:00|       10|       210147125|             7|         4|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-03-06 00:00:00|       10|       210147125|            13|         6|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-03-07 00:00:00|       10|       210147125|            19|         6|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-03-08 00:00:00|       11|       210147125|            25|         6|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-03-09 00:00:00|       11|       210147125|            25|         0|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-03-10 00:00:00|       11|       210147125|            34|         9|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-03-11 00:00:00|       11|       210147125|            52|        18|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-03-12 00:00:00|       11|       210147125|            77|        25|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-03-13 00:00:00|       11|       210147125|            98|        21|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-03-14 00:00:00|       11|       210147125|           121|        23|              0|          0|            null|                 null|                  null|
    |Brasil|  null|     null|   76|  null|          null|           null|2020-03-15 00:00:00|       12|       210147125|           200|        79|              0|          0|            null|                 null|                  null|
    +------+------+---------+-----+------+--------------+---------------+-------------------+---------+----------------+--------------+----------+---------------+-----------+----------------+---------------------+----------------------+
    only showing top 20 rows
    



```python

#from pyspark.sql.functions import *
# Ajustando os dados e removendo a informação de hora, pois todas estão zeradas
df_painel_covidbr_limpo = df_painel_covidbr\
.withColumn('data',from_unixtime(unix_timestamp(df_painel_covidbr.data), 'yyyy-MM-dd'))

```


```python
#Mostrando o novo dataframe com o campo data ajustado
df_painel_covidbr_limpo.show(3, vertical=True)
```

    -RECORD 0----------------------------
     regiao                 | Brasil     
     estado                 | null       
     municipio              | null       
     coduf                  | 76         
     codmun                 | null       
     codRegiaoSaude         | null       
     nomeRegiaoSaude        | null       
     data                   | 2020-02-25 
     semanaEpi              | 9          
     populacaoTCU2019       | 210147125  
     casosAcumulado         | 0          
     casosNovos             | 0          
     obitosAcumulado        | 0          
     obitosNovos            | 0          
     Recuperadosnovos       | null       
     emAcompanhamentoNovos  | null       
     interior/metropolitana | null       
    -RECORD 1----------------------------
     regiao                 | Brasil     
     estado                 | null       
     municipio              | null       
     coduf                  | 76         
     codmun                 | null       
     codRegiaoSaude         | null       
     nomeRegiaoSaude        | null       
     data                   | 2020-02-26 
     semanaEpi              | 9          
     populacaoTCU2019       | 210147125  
     casosAcumulado         | 1          
     casosNovos             | 1          
     obitosAcumulado        | 0          
     obitosNovos            | 0          
     Recuperadosnovos       | null       
     emAcompanhamentoNovos  | null       
     interior/metropolitana | null       
    -RECORD 2----------------------------
     regiao                 | Brasil     
     estado                 | null       
     municipio              | null       
     coduf                  | 76         
     codmun                 | null       
     codRegiaoSaude         | null       
     nomeRegiaoSaude        | null       
     data                   | 2020-02-27 
     semanaEpi              | 9          
     populacaoTCU2019       | 210147125  
     casosAcumulado         | 1          
     casosNovos             | 0          
     obitosAcumulado        | 0          
     obitosNovos            | 0          
     Recuperadosnovos       | null       
     emAcompanhamentoNovos  | null       
     interior/metropolitana | null       
    only showing top 3 rows
    



```python
#Otimizar dados por tabelas particionadas por município
spark.sql("CREATE DATABASE IF NOT EXISTS covidbr")
df_painel_covidbr_limpo.write\
.mode('overwrite')\
.partitionBy('municipio')\
.format('csv')\
.saveAsTable('covidbr.municipio', path='hdfs://namenode:8020/user/hive/warehouse/covidbr/')

```


```python
#Confirmar se os dados foram salvos no diretório
!hdfs dfs -ls 'hdfs://namenode:8020/user/hive/warehouse/covidbr/'
```

    Found 5299 items
    -rw-r--r--   2 root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/_SUCCESS
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Abadia de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Abadia dos Dourados
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Abadiânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Abaetetuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Abaeté
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Abaiara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Abaré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Abatiá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Abaíra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Abdon Batista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Abel Figueiredo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Abelardo Luz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Abre Campo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Abreu e Lima
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Abreulândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Acaiaca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Acajutiba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Acarape
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Acaraú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Acari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Acará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Acauã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aceguá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Acopiara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Acorizal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Acrelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Acreúna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Adamantina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Adelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Adolfo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Adrianópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Adustina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Afogados da Ingazeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Afonso Bezerra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Afonso Cláudio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Afonso Cunha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Afrânio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Afuá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Agrestina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Agricolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Agrolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Agronômica
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aguanil
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aguaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Agudo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Agudos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Agudos do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aguiar
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aguiarnópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aimorés
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aiquara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aiuaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aiuruoca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ajuricaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alagoa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alagoa Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alagoa Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alagoinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alagoinha do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alagoinhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alambari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Albertina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alcantil
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alcinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alcobaça
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alcântara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alcântaras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aldeias Altas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alecrim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alegrete
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alegrete do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alegria
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alenquer
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alexandria
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alexânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alfenas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alfredo Chaves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alfredo Marcondes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alfredo Vasconcelos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alfredo Wagner
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Algodão de Jandaíra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alhandra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aliança
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aliança do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Almadina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Almas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Almeirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Almenara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Almino Afonso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Almirante Tamandaré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Almirante Tamandaré do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aloândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alpercata
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alpestre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alpinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alta Floresta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alta Floresta D%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Altair
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Altamira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Altamira do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Altamira do Paraná
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Altaneira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alterosa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Altinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Altinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Alegre do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Alegre do Pindaré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Alegre dos Parecis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Araguaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Bela Vista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Boa Vista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Caparaó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Feliz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Garças
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Horizonte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Jequitibá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Longá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Paraguai
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Paraná
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Paraíso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Paraíso de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Parnaíba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Piquiri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Rio Doce
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Rio Novo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Santo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto Taquari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alto do Rodrigues
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Altos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Altônia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alumínio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alvarenga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alvarães
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alvinlândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alvinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alvorada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alvorada D%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alvorada de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alvorada do Gurguéia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alvorada do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Alvorada do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Além Paraíba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Amajari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Amambai
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Amaporã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Amapá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Amapá do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Amaraji
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Amaral Ferrador
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Amaralina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Amarante
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Amarante do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Amargosa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Amaturá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Americana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Americano do Brasil
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ametista do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Amontada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Amorinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Amparo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Amparo de São Francisco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Amparo do Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ampére
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Amélia Rodrigues
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=América Dourada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Américo Brasiliense
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Américo de Campos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anadia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anagé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anahy
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anajatuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anajás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Analândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anamã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ananindeua
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ananás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anapu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anapurus
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anastácio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anaurilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anchieta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Andaraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Andirá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Andorinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Andradas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Andradina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Andrelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=André da Rocha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Angatuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Angelim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Angelina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Angelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Angical
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Angical do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Angico
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Angicos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Angra dos Reis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anguera
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Angélica
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anhanguera
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anhembi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anhumas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anicuns
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anita Garibaldi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anitápolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anori
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anta Gorda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Antas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Antonina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Antonina do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Antônio Almeida
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Antônio Cardoso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Antônio Carlos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Antônio Dias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Antônio Gonçalves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Antônio João
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Antônio Martins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Antônio Olinto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Antônio Prado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Antônio Prado de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anápolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Anísio de Abreu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aparecida
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aparecida d%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aparecida de Goiânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aparecida do Rio Doce
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aparecida do Rio Negro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aparecida do Taboado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aperibé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Apiacá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Apiacás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Apiaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Apicum-Açu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Apiúna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Apodi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aporá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aporé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Apuarema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Apucarana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Apuiarés
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Apuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aquidabã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aquidauana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aquiraz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arabutã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aracaju
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aracati
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aracatu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araci
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aracitaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aracoiaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aracruz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aragarças
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aragoiânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aragominas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araguacema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araguaiana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araguainha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araguanã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araguapaz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araguari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araguatins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araguaína
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araioses
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aral Moreira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aramari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arambaré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arame
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aramina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arandu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arantina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arapeí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arapiraca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arapoema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araponga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arapongas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araporã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arapoti
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araputanga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arapuá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arapuã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araquari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araranguá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araraquara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ararendá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araricá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araripe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araripina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araruama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araruna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arataca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aratiba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aratuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aratuípe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araucária
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arauá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araxá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araçagi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araçariguama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araçatuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araçaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araçoiaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araçoiaba da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araçuaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araçás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Araújos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arceburgo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arco-Íris
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arcos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arcoverde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Areado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Areal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arealva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Areia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Areia Branca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Areia de Baraúnas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Areial
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Areias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Areiópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arenápolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arenópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Argirita
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aricanduva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arinos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aripuanã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ariquemes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ariranha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ariranha do Ivaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Armazém
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Armação dos Búzios
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arneiroz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aroazes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aroeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aroeiras do Itaim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arraial
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arraial do Cabo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arraias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arroio Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arroio Trinta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arroio do Meio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arroio do Padre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arroio do Sal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arroio do Tigre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arroio dos Ratos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Artur Nogueira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aruanã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arujá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arvoredo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arvorezinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Arês
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ascurra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aspásia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Assaré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Assaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Assis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Assis Brasil
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Assis Chateaubriand
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Assunção
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Assunção do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Astolfo Dutra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Astorga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Atalaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Atalaia do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Atalanta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ataléia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Atibaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Atílio Vivacqua
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Augustinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Augusto Corrêa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Augusto Pestana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Augusto de Lima
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aurelino Leal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Auriflama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aurilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aurora
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aurora do Pará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aurora do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Autazes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Avanhandava
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Avaré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Avaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Aveiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Avelino Lopes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Avelinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Axixá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Axixá do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Açailândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Açu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Açucena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Babaçulândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bacabal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bacabeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bacuri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bacurituba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bady Bassitt
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Baependi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bagre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bagé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Baianópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Baixa Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Baixa Grande do Ribeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Baixio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Baixo Guandu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Baião
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Balbinos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Baldim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Baliza
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Balneário Arroio do Silva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Balneário Barra do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Balneário Camboriú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Balneário Gaivota
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Balneário Pinhal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Balneário Piçarras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Balneário Rincão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Balsa Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Balsas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bambu��
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Banabuiú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bananal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bananeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bandeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bandeira do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bandeirante
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bandeirantes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bandeirantes do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bannach
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Banzaê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Baraúna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barbacena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barbalha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barbosa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barbosa Ferraz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barcarena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barcelona
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barcelos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bariri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra Bonita
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra D%27Alcântara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra Funda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra Longa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra Mansa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra Velha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra da Estiva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra de Guabiraba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra de Santa Rosa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra de Santana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra de Santo Antônio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra de São Francisco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra de São Miguel
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra do Bugres
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra do Chapéu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra do Choça
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra do Corda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra do Garças
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra do Guarita
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra do Jacaré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra do Mendes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra do Ouro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra do Piraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra do Quaraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra do Ribeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra do Rio Azul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra do Rocha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra do Turvo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barra dos Coqueiros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barracão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barreira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barreiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barreiras do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barreirinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barreirinhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barreiros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barretos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barrinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barro Alto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barro Duro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barro Preto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barrocas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barrolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barroquinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barros Cassal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barroso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barueri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barão de Antonina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barão de Cocais
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barão de Cotegipe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barão de Grajaú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barão de Melgaço
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barão de Monte Alto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Barão do Triunfo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bastos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bataguassu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Batalha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Batatais
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Batayporã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Baturité
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bauru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bayeux
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Baía Formosa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Baía da Traição
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bebedouro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Beberibe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bela Cruz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bela Vista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bela Vista da Caroba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bela Vista de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bela Vista de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bela Vista do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bela Vista do Paraíso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bela Vista do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bela Vista do Toldo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Belford Roxo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Belmiro Braga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Belmonte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Belo Campo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Belo Horizonte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Belo Jardim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Belo Monte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Belo Oriente
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Belo Vale
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Belterra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Belágua
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Belém
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Belém de Maria
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Belém do Brejo do Cruz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Belém do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Belém do São Francisco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Beneditinos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Benedito Leite
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Benedito Novo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Benevides
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Benjamin Constant
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Benjamin Constant do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bento Fernandes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bento Gonçalves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bento de Abreu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bequimão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Berilo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Berizal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bernardino Batista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bernardino de Campos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bernardo Sayão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bernardo do Mearim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bertioga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bertolínia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bertópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Beruri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Betim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Betânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Betânia do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bezerros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bias Fortes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bicas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Biguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bilac
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Biquinhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Birigui
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Biritiba Mirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Biritinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bituruna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Blumenau
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boa Esperança
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boa Esperança do Iguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boa Esperança do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boa Hora
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boa Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boa Ventura
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boa Ventura de São Roque
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boa Viagem
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boa Vista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boa Vista da Aparecida
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boa Vista das Missões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boa Vista do Buricá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boa Vista do Cadeado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boa Vista do Gurupi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boa Vista do Incra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boa Vista do Ramos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boa Vista do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boa Vista do Tupim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boca da Mata
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boca do Acre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bocaina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bocaina de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bocaina do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bocaiúva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bocaiúva do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bodocó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bodoquena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bodó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bofete
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boituva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Conselho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Despacho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jardim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jardim da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jardim de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jardim de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jesus
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jesus da Lapa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jesus da Penha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jesus da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jesus das Selvas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jesus de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jesus do Amparo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jesus do Araguaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jesus do Galho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jesus do Itabapoana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jesus do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jesus do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jesus do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jesus do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Jesus dos Perdões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Lugar
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Princípio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Princípio do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Progresso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Repouso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Retiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Retiro do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Sucesso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Sucesso de Itararé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bom Sucesso do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bombinhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bonfim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bonfim do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bonfinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bonfinópolis de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boninal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bonito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bonito de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bonito de Santa Fé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bonópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boqueirão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boqueirão do Leão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boqueirão do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boquim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boquira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Boracéia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Borba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Borborema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Borda da Mata
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Borebi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Borrazópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Borá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bossoroca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Botelhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Botucatu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Botumirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Botuporã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Botuverá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bozano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Braga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Braganey
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bragança
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bragança Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Branquinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brasil Novo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brasileira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brasilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brasilândia de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brasilândia do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brasilândia do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brasiléia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brasnorte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brasília
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brasília de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brazabrantes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brazópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Braço do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Braço do Trombudo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Braúna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Braúnas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brejetuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brejinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brejinho de Nazaré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brejo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brejo Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brejo Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brejo Grande do Araguaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brejo Santo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brejo da Madre de Deus
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brejo de Areia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brejo do Cruz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brejo do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brejo dos Santos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brejolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brejão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brejões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Breu Branco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Breves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Britânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brochier
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brodowski
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brotas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brotas de Macaúbas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brumadinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brumado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brunópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brusque
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Brás Pires
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bueno Brandão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buenos Aires
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buenópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buerarema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bugre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bujari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bujaru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buritama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buriti
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buriti Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buriti Bravo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buriti de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buriti do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buriti dos Lopes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buriti dos Montes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buriticupu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buritinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buritirama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buritirana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buritis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buritizal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buritizeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Butiá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Buíque
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Bálsamo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caapiranga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caaporã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caarapó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caatiba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cabaceiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cabaceiras do Paraguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cabeceira Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cabeceiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cabeceiras do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cabedelo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cabixi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cabo Frio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cabo Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cabo de Santo Agostinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cabreúva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cabrobó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cabrália Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cacaulândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cacequi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cachoeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cachoeira Alta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cachoeira Dourada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cachoeira Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cachoeira Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cachoeira da Prata
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cachoeira de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cachoeira de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cachoeira de Pajeú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cachoeira do Arari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cachoeira do Piriá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cachoeira do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cachoeira dos Índios
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cachoeiras de Macacu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cachoeirinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cachoeiro de Itapemirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cacimba de Areia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cacimba de Dentro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cacimbas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cacimbinhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cacique Doble
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cacoal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caconde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caculé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caetanos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caetanópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caetité
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caeté
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caetés
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cafarnaum
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cafeara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cafelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cafezal do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caiabu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caiana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caiapônia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caibaté
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caibi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caicó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caieiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cairu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caiuá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caiçara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caiçara do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caiçara do Rio do Vento
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cajamar
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cajapió
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cajari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cajati
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cajazeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cajazeiras do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cajazeirinhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cajobi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cajueiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cajueiro da Praia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cajuri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cajuru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caldas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caldas Brandão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caldas Novas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caldazinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caldeirão Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caldeirão Grande do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Califórnia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Calmon
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Calumbi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Calçado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Calçoene
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Camacan
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Camacho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Camalaú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Camamu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Camanducaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Camapuã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Camaquã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Camaragibe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Camargo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Camaçari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cambará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cambará do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cambira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Camboriú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cambuci
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cambuquira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cambuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cambé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cametá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Camocim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Camocim de São Félix
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campanha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campanário
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campestre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campestre da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campestre de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campestre do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campina Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campina Grande do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campina Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campina da Lagoa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campina das Missões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campina do Monte Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campina do Simão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campinas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campinas do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campinas do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campinaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campinorte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campinápolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Alegre de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Alegre de Lourdes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Alegre do Fidalgo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Azul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Belo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Belo do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Bom
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Bonito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Erê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Florido
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Formoso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Grande do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Largo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Largo do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Limpo Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Limpo de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Magro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Maior
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Mourão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Novo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Novo de Rondônia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Novo do Parecis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Redondo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo do Brito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo do Meio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campo do Tenente
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campos Altos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campos Belos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campos Borges
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campos Gerais
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campos Lindos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campos Novos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campos Novos Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campos Sales
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campos Verdes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campos de Júlio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campos do Jordão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Campos dos Goytacazes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Camutanga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cana Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canabrava do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cananéia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canapi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canarana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canavieira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canavieiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canaã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canaã dos Carajás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Candeal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Candeias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Candeias do Jamari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Candelária
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Candiba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Candiota
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Candói
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canela
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canelinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canguaretama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canguçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canhoba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canhotinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canindé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canindé de São Francisco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canitar
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canoas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canoinhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cansanção
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cantagalo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cantanhede
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canto do Buriti
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cantá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canudos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canudos do Vale
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canutama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Canápolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capanema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caparaó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capela
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capela Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capela de Santana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capela do Alto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capela do Alto Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capelinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capetinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capim Branco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capim Grosso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capinzal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capinzal do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capistrano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capitão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capitão Andrade
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capitão Enéas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capitão Gervásio Oliveira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capitão Leônidas Marques
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capitão Poço
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capitão de Campos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capitólio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capivari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capivari de Baixo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capivari do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capixaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capoeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caputira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capão Alto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capão Bonito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capão Bonito do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capão da Canoa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capão do Cipó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Capão do Leão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caracaraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caracol
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caraguatatuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carambeí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caranaíba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carandaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carangola
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carapebus
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carapicuíba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caratinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carauari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caravelas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carazinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caraá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caraíbas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caraúbas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caraúbas do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carbonita
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cardeal da Silva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cardoso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cardoso Moreira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Careaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Careiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Careiro da Várzea
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cariacica
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caridade
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caridade do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carinhanha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cariri do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caririaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cariré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cariús
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carlinda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carlos Barbosa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carlos Chagas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carlos Gomes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carlópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carmo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carmo da Cachoeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carmo da Mata
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carmo de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carmo do Cajuru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carmo do Paranaíba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carmo do Rio Claro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carmo do Rio Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carmolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carmésia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carmópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carmópolis de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carnaubais
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carnaubal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carnaubeira da Penha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carnaíba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carnaúba dos Dantas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carneirinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carneiros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caroebe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carolina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carpina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carrancas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carrapateira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carrasco Bonito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caruaru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carutapera
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carvalhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Carvalhópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Casa Branca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Casa Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Casa Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Casca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cascalho Rico
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cascavel
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caseara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caseiros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Casimiro de Abreu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Casinhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Casserengue
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cassilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Castanhal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Castanheira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Castanheiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Castelo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Castelo do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Castelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Castilho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Castro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Castro Alves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cataguases
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Catalão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Catanduva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Catanduvas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Catarina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Catas Altas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Catas Altas da Noruega
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Catende
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Catiguá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Catingueira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Catolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Catolé do Rocha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Catu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Catuji
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Catunda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caturama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caturaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caturité
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Catuti
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Catuípe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caucaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cavalcante
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caxambu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caxambu do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caxias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caxias do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caxingó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caçador
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caçapava
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caçapava do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Caém
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ceará-Mirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cedral
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cedro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cedro de São João
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cedro do Abaeté
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Celso Ramos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Centenário
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Centenário do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Central
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Central de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Central do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Centralina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Centro Novo do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Centro do Guilherme
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cerejeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ceres
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cerqueira César
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cerquilho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cerrito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cerro Azul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cerro Branco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cerro Corá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cerro Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cerro Grande do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cerro Largo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cerro Negro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cesário Lange
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cezarina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chalé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chapada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chapada Gaúcha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chapada da Natividade
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chapada de Areia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chapada do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chapada dos Guimarães
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chapadinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chapadão do Céu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chapadão do Lageado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chapadão do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chapecó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Charqueada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Charqueadas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Charrua
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chaval
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chavantes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chaves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chiador
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chiapetta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chopinzinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chorozinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chorrochó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Choró
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chupinguaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chuvisca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chácara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chã Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chã Preta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Chã de Alegria
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cianorte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cidade Gaúcha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cidade Ocidental
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cidelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cidreira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cipotânea
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cipó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ciríaco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Claraval
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Claro dos Poções
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Clementina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Clevelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cláudia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cláudio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coaraci
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cocal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cocal de Telha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cocal do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cocal dos Alves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cocalinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cocalzinho de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cocos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Codajás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Codó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coelho Neto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coimbra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coité do Nóia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coivaras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Colares
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Colatina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Colina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Colinas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Colinas do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Colinas do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Colméia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Colniza
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Colombo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Colorado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Colorado do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coluna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Colíder
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Colômbia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Colônia Leopoldina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Colônia do Gurguéia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Colônia do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Combinado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Comendador Gomes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Comendador Levy Gasparian
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Comercinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Comodoro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição da Aparecida
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição da Barra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição da Barra de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição da Feira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição das Alagoas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição das Pedras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição de Ipanema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição de Macabu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição do Almeida
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição do Araguaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição do Canindé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição do Castelo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição do Coité
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição do Jacuípe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição do Lago-Açu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição do Mato Dentro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição do Pará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição do Rio Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conceição dos Ouros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conchal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conchas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Concórdia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Concórdia do Pará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Condado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Condeúba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Condor
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Confins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Confresa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Congo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Congonhal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Congonhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Congonhas do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Congonhinhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conquista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conquista D%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conselheiro Lafaiete
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conselheiro Mairinck
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Conselheiro Pena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Consolação
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Constantina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Contagem
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Contenda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Contendas do Sincorá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coqueiral
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coqueiro Baixo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coqueiro Seco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coqueiros do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coração de Jesus
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coração de Maria
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Corbélia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cordeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cordeiros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cordeirópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cordilheira Alta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cordisburgo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cordislândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coreaú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coremas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Corguinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coribe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Corinto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cornélio Procópio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coroaci
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coroados
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coroatá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coromandel
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coronel Barros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coronel Bicaco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coronel Domingos Soares
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coronel Ezequiel
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coronel Fabriciano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coronel Freitas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coronel José Dias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coronel João Pessoa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coronel João Sá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coronel Macedo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coronel Martins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coronel Murta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coronel Pacheco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coronel Pilar
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coronel Sapucaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coronel Vivida
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coronel Xavier Chaves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Correia Pinto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Corrente
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Correntes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Correntina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cortês
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Corumbataí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Corumbataí do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Corumbaíba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Corumbiara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Corumbá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Corumbá de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Corupá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coruripe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cosmorama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cosmópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Costa Marques
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Costa Rica
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cotegipe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cotia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cotiporã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cotriguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Couto Magalhães
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Couto de Magalhães de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coxilha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coxim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Coxixola
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Crateús
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Crato
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cravinhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cravolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Craíbas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Criciúma
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Crissiumal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cristais
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cristais Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cristal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cristal do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cristalina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cristalândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cristalândia do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cristiano Otoni
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cristianópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cristina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cristino Castro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cristinápolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cristália
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cristópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Crisólita
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Crisópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Crixás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Crixás do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Croatá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cromínia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Crucilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cruz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cruz Alta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cruz Machado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cruz das Almas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cruz do Espírito Santo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cruzaltense
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cruzeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cruzeiro da Fortaleza
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cruzeiro do Iguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cruzeiro do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cruzeiro do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cruzeta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cruzmaltina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cruzália
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cruzília
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cubati
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cubatão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cuiabá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cuitegi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cuité
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cuité de Mamanguape
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cujubim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cumari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cumaru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cumaru do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cumbe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cunha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cunha Porã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cunhataí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cuparaque
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cupira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Curaçá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Curimatá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Curionópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Curitiba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Curitibanos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Curiúva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Currais
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Currais Novos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Curral Novo do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Curral Velho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Curral de Cima
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Curral de Dentro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Curralinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Curralinhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cururupu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Curuá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Curuçá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Curvelo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Curvelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Custódia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cutias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cáceres
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cássia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cássia dos Coqueiros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cândido Godói
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cândido Mendes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cândido Mota
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cândido Rodrigues
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cândido Sales
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cândido de Abreu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Céu Azul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cícero Dantas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Córrego Danta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Córrego Fundo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Córrego Novo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Córrego do Bom Jesus
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Córrego do Ouro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Cônego Marinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Damianópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Damião
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Damolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Darcinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Datas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=David Canabarro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Davinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Delfim Moreira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Delfinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Delmiro Gouveia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Delta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Demerval Lobão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Denise
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Deodápolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Deputado Irapuan Pinheiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Derrubadas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Descalvado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Descanso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Descoberto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Desterro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Desterro de Entre Rios
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Desterro do Melo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dezesseis de Novembro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Diadema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Diamante
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Diamante D%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Diamante do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Diamante do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Diamantina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Diamantino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dianópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dias d%27Ávila
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dilermando de Aguiar
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Diogo de Vasconcelos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dionísio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dionísio Cerqueira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Diorama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dirce Reis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dirceu Arcoverde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Divina Pastora
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Divino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Divino das Laranjeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Divino de São Lourenço
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Divinolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Divinolândia de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Divinésia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Divinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Divinópolis de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Divinópolis do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Divisa Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Divisa Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Divisópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dobrada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dois Córregos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dois Irmãos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dois Irmãos das Missões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dois Irmãos do Buriti
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dois Irmãos do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dois Lajeados
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dois Riachos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dois Vizinhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dolcinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dom Aquino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dom Basílio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dom Bosco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dom Cavati
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dom Eliseu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dom Expedito Lopes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dom Feliciano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dom Inocêncio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dom Joaquim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dom Macedo Costa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dom Pedrito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dom Pedro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dom Pedro de Alcântara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dom Silvério
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dom Viçoso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Domingos Martins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Domingos Mourão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dona Emma
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dona Euzébia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dona Francisca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dona Inês
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dores de Campos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dores de Guanhães
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dores do Indaiá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dores do Rio Preto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dores do Turvo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Doresópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dormentes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Douradina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dourado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Douradoquara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dourados
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Doutor Camargo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Doutor Maurício Cardoso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Doutor Pedrinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Doutor Ricardo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Doutor Severiano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Doutor Ulysses
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Doverlândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dracena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Duartina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Duas Barras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Duas Estradas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dueré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dumont
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Duque Bacelar
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Duque de Caxias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Durandé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Dário Meira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Echaporã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ecoporanga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Edealina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Edéia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Eirunepé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Eldorado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Eldorado do Carajás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Eldorado do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Elesbão Veloso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Elias Fausto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Eliseu Martins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Elisiário
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Elísio Medrado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Elói Mendes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Emas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Embaúba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Embu das Artes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Embu-Guaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Emilianópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Encantado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Encanto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Encruzilhada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Encruzilhada do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Engenheiro Beltrão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Engenheiro Caldas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Engenheiro Coelho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Engenheiro Navarro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Engenheiro Paulo de Frontin
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Engenho Velho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Entre Folhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Entre Rios
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Entre Rios de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Entre Rios do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Entre Rios do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Entre-Ijuís
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Envira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Enéas Marques
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Epitaciolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Equador
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Erebango
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Erechim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ereré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ermo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ernestina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Erval Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Erval Seco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Erval Velho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ervália
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Escada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Esmeralda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Esmeraldas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Espera Feliz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Esperantina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Esperantinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Esperança
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Esperança Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Esperança do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Espigão Alto do Iguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Espigão D%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Espinosa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Esplanada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Espumoso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Espírito Santo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Espírito Santo do Dourado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Espírito Santo do Pinhal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Espírito Santo do Turvo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Estação
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Esteio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Estiva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Estiva Gerbi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Estreito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Estrela
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Estrela Dalva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Estrela Velha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Estrela d%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Estrela de Alagoas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Estrela do Indaiá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Estrela do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Estrela do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Estância
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Estância Velha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Euclides da Cunha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Euclides da Cunha Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Eugenópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Eugênio de Castro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Eunápolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Eusébio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ewbank da Câmara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Extrema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Extremoz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Exu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fagundes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fagundes Varela
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Faina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Faria Lemos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Farias Brito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Faro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Farol
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Farroupilha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fartura
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fartura do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Faxinal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Faxinal do Soturno
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Faxinal dos Guedes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Faxinalzinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fazenda Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fazenda Rio Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fazenda Vilanova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Feijó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Feira Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Feira Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Feira Nova do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Feira da Mata
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Feira de Santana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Felipe Guerra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Felisburgo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Felixlândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Feliz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Feliz Deserto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Feliz Natal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Felício dos Santos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fernandes Pinheiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fernandes Tourinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fernando Falcão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fernando Pedroza
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fernando Prestes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fernando de Noronha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fernandópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fernão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ferraz de Vasconcelos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ferreira Gomes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ferreiros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ferros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fervedouro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Figueira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Figueirão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Figueirópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Figueirópolis D%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Filadélfia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Firmino Alves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Firminópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Flexeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Flor da Serra do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Flor do Sertão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Flora Rica
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Floraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Floreal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Flores
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Flores da Cunha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Flores de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Flores do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Floresta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Floresta Azul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Floresta do Araguaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Floresta do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Florestal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Florestópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Floriano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Floriano Peixoto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Florianópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Florânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Florínea
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Flórida
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Flórida Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fonte Boa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fontoura Xavier
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Formiga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Formigueiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Formosa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Formosa da Serra Negra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Formosa do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Formosa do Rio Preto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Formosa do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Formoso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Formoso do Araguaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Forquetinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Forquilha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Forquilhinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fortaleza
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fortaleza de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fortaleza dos Nogueiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fortaleza dos Valos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fortim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fortuna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fortuna de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Foz do Iguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Foz do Jordão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fraiburgo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Franca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Francinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Francisco Alves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Francisco Ayres
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Francisco Badaró
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Francisco Beltrão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Francisco Dantas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Francisco Dumont
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Francisco Macedo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Francisco Morato
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Francisco Santos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Francisco Sá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Franciscópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Franco da Rocha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Frecheirinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Frederico Westphalen
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Frei Gaspar
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Frei Inocêncio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Frei Lagonegro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Frei Martinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Frei Miguelinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Frei Paulo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Frei Rogério
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fronteira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fronteira dos Vales
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fronteiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fruta de Leite
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Frutal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Frutuoso Gomes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fundão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Funilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fátima
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fátima do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Fênix
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gabriel Monteiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gado Bravo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Galiléia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Galinhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Galvão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gameleira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gameleira de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gameleiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gandu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Garanhuns
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gararu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Garibaldi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Garopaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Garrafão do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Garruchos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Garuva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Garça
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gaspar
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gastão Vidigal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gaurama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gavião
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gavião Peixoto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gaúcha do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Geminiano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=General Carneiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=General Câmara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=General Maynard
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=General Salgado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=General Sampaio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gentil
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gentio do Ouro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Getulina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Getúlio Vargas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gilbués
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Girau do Ponciano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Giruá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Glaucilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Glicério
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Glorinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Glória
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Glória D%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Glória de Dourados
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Glória do Goitá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Godofredo Viana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Godoy Moreira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Goiabeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Goiana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Goiandira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Goianinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Goianira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Goianorte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Goianá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Goianápolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Goianésia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Goianésia do Pará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Goiatins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Goiatuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Goioerê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Goioxim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Goiânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gongogi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gonzaga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gonçalves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gonçalves Dias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gouveia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gouvelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Governador Archer
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Governador Celso Ramos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Governador Dix-Sept Rosado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Governador Edison Lobão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Governador Eugênio Barros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Governador Jorge Teixeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Governador Lindenberg
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Governador Luiz Rocha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Governador Mangabeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Governador Newton Bello
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Governador Nunes Freire
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Governador Valadares
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gracho Cardoso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Grajaú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gramado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gramado Xavier
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gramado dos Loureiros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Grandes Rios
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Granito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Granja
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Granjeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gravatal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gravataí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gravatá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Graça
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Graça Aranha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Groaíras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Grossos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Grupiara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Grão Mogol
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Grão Pará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guabiju
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guabiruba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guadalupe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaimbê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guairaçá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaiçara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaiúba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guajará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guajará-Mirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guajeru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guamaré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guamiranga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guanambi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guanhães
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guapiara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guapiaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guapimirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guapirama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaporema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaporé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guapé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guapó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guarabira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaraci
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaraciaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaraciaba do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaraciama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaramiranga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaramirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guarani
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guarani d%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guarani das Missões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guarani de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaraniaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guarantã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guarantã do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaranésia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guarapari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guarapuava
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaraqueçaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guararapes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guararema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guarará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaratinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaratinguetá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaratuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaraçaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaraíta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guarda-Mor
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guareí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guariba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaribas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guarinos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guarujá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guarujá do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guarulhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guatambú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guatapará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaxupé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaçuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaíba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guaíra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guia Lopes da Laguna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guidoval
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guimarânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guimarães
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guiratinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guiricema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gurinhatã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gurinhém
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gurjão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gurupi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gurupá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Guzolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Gália
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Harmonia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Heitoraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Heliodora
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Heliópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Herculândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Herval
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Herval d%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Herveiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Hidrolina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Hidrolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Holambra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Honório Serpa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Horizonte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Horizontina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Hortolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Hugo Napoleão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Hulha Negra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Humaitá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Humberto de Campos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iacanga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iaciara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iacri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iapu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iaras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iati
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibaiti
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibarama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibaretama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibateguara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibatiba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibaté
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibertioga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibiam
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibiapina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibiara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibiassucê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibiaçá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibiaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibicaraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibicaré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibicoara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibicuitinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibicuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibimirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibipeba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibipitanga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibiporã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibiquera
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibiracatu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibiraci
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibiraiaras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibirajuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibirama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibirapitanga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibirapuitã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibirapuã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibirarema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibirataia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibiraçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibirité
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibirubá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibirá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibitiara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibitinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibitirama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibititá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibitiúra de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibituruna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibiá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibiúna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ibotirama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Icapuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Icaraí de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Icaraíma
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Icatu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ichu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iconha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Icém
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Icó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ielmo Marinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iepê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Igaci
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Igaporã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Igaracy
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Igarapava
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Igarapé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Igarapé Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Igarapé do Meio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Igarapé-Açu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Igarapé-Miri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Igarassu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Igaratinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Igaratá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Igaraçu do Tietê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Igrapiúna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Igreja Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Igrejinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iguaba Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iguape
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iguaracy
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iguaraçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iguatama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iguatemi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iguatu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iguaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ijaci
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ijuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ilha Comprida
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ilha Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ilha Solteira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ilha das Flores
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ilha de Itamaracá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ilhabela
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ilhota
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ilhéus
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ilicínea
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ilópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Imaculada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Imaruí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Imbaú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Imbituba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Imbituva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Imbuia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Imbé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Imbé de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Imigrante
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Imperatriz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Inaciolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Inajá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Inconfidentes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Indaiabira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Indaial
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Indaiatuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Independência
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Indiana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Indianópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Indiaporã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Indiara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Indiaroba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Indiavaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ingazeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ingaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ingá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Inhacorá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Inhambupe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Inhangapi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Inhapi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Inhapim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Inhaúma
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Inhuma
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Inhumas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Inimutaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Inocência
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Inácio Martins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Inúbia Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iomerê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipameri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipanema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipanguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipaporanga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipatinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipaumirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipaussu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipecaetá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iperó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipeúna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipiaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipiaú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipiguá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipiranga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipiranga de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipiranga do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipiranga do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipiranga do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipirá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipixuna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipixuna do Pará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipojuca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iporanga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iporá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iporã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iporã do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipuaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipubi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipueira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipueiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipuiúna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipumirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipupiara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipuã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ipê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iracema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iracema do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iraceminha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iracemápolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Irajuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iramaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iranduba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Irani
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Irapuru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Irapuã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iraquara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Irará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Irati
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Irauçuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iraí de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Irecê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iretama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Irineópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Irituia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Irupi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Isaías Coelho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Israelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itabaiana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itabaianinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itabela
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaberaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaberaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaberá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itabi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itabira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itabirinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itabirito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaboraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itabuna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itacajá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itacambira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itacarambi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itacaré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itacoatiara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itacuruba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itacurubi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaeté
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itagi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itagibá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itagimirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaguajé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaguara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaguari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaguaru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaguatins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaguaçu da Bahia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaguaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itainópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaipava do Grajaú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaipulândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaipé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaitinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaituba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaiçaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaiópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itajaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itajobi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaju
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaju do Colônia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itajubá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itajuípe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itajá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Italva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itamaraju
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itamarandiba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itamarati
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itamarati de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itamari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itambacuri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itambaracá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itambé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itambé do Mato Dentro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itamogi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itamonte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itanagra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itanhandu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itanhangá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itanhaém
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itanhomi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itanhém
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaobim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaoca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaocara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapaci
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapagipe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapajé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaparica
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapebi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapecerica
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapecerica da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapecuru Mirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapejara d%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapemirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaperuna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaperuçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapetim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapetinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapetininga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapeva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapevi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapicuru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapipoca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapiranga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapirapuã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapirapuã Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapiratins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapissuma
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapitanga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapiúna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaporanga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaporanga d%27Ajuda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapororoca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaporã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaporã do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapoá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapuca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapura
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapuranga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapuã do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itapé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaquaquecetuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaquara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaqui
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaquiraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaquitinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itarana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itarantim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itararé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itarema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itariri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itarumã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itati
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itatiaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itatiaiuçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itatiba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itatiba do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itatim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itatinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itatira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itatuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaubal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaueira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itauçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaverava
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaíba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaú de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaúba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaúna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itaúna do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itinga do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itiquira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itirapina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itirapuã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itiruçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itiúba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itobi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itororó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ituaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ituberá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itueta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ituiutaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itumbiara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itumirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itupeva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itupiranga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ituporanga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iturama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itutinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ituverava
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Itápolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iuiu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ivaiporã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ivatuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ivaté
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ivaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ivinhema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ivolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ivorá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ivoti
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Içara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Iúna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaboatão dos Guararapes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaborandi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaborá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaboti
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaboticaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaboticabal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaboticatubas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jacaraci
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jacaraú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jacareacanga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jacarezinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jacareí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jacaré dos Homens
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaci
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaciara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jacinto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jacinto Machado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jacobina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jacobina do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jacuizinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jacundá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jacupiranga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jacutinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jacuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jacuípe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaguapitã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaguaquara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaguarari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaguaraçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaguaretama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaguari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaguariaíva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaguaribara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaguaribe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaguaripe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaguariúna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaguaruana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaguaruna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaguarão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaguaré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaicós
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jales
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jambeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jampruca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Janaúba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jandaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jandaia do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jandaíra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jandira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Janduís
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jangada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Janiópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Januária
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Januário Cicco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Japaratinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Japaratuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Japaraíba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Japeri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Japi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Japira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Japoatã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Japonvar
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Japorã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Japurá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaqueira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaquirana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaraguari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaraguá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaraguá do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaramataia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jardim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jardim Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jardim Olinda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jardim de Angicos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jardim de Piranhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jardim do Mulato
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jardim do Seridó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jardinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jarinu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jataizinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jataí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jataúba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jateí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jati
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jatobá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jatobá do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaupaci
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jauru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaçanã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaíba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jaú do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jeceaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jenipapo de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jenipapo dos Vieiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jequeri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jequitaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jequitibá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jequitinhonha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jequiá da Praia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jequié
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jeremoabo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jericó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jeriquara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jerumenha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jerônimo Monteiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jesuânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jesuítas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jesúpolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ji-Paraná
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jijoca de Jericoacoara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jiquiriçá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jitaúna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Joanésia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Joanópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Joaquim Felício
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Joaquim Gomes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Joaquim Nabuco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Joaquim Pires
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Joaquim Távora
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Joaçaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Joaíma
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Joca Claudino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Joca Marques
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Joinville
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jordânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jordão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Joselândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Josenópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=José Boiteux
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=José Bonifácio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=José Gonçalves de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=José Raydan
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=José da Penha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=José de Freitas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Joviânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=João Alfredo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=João Costa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=João Câmara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=João Dias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=João Dourado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=João Lisboa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=João Monlevade
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=João Neiva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=João Pessoa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=João Pinheiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=João Ramalho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juarez Távora
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juarina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juatuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juazeirinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juazeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juazeiro do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juazeiro do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jucati
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jucurutu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jucuruçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jucás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juiz de Fora
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jumirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Junco do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Junco do Seridó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jundiaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jundiaí do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jundiá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Junqueiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Junqueirópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jupi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jupiá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juquitiba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juquiá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juramento
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juranda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jurema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juripiranga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juruaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juruena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juruti
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juruá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juscimeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jussara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jussari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jussiape
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jutaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juti
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juvenília
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Juína
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Jóia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Júlio Borges
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Júlio Mesquita
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Júlio de Castilhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Kaloré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lacerdópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ladainha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ladário
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lafaiete Coutinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagamar
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagarto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lages
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lago Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lago da Pedra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lago do Junco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lago dos Rodrigues
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa Bonita do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa Dourada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa Formosa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa Grande do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa Real
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa Salgada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa Santa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa Seca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa Vermelha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa d%27Anta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa da Canoa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa da Confusão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa da Prata
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa de Dentro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa de Itaenga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa de Pedras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa de São Francisco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa de Velhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa do Barro do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa do Carro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa do Mato
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa do Ouro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa do Sítio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa dos Gatos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa dos Patos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoa dos Três Cantos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoinha do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lagoão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Laguna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Laguna Carapã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Laje
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Laje do Muriaé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lajeado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lajeado Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lajeado Novo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lajeado do Bugre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lajedinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lajedo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lajedo do Tabocal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lajedão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lajes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lajes Pintadas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lajinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lamarão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lambari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lambari D%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lamim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Landri Sales
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lapa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lapão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Laranja da Terra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Laranjal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Laranjal Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Laranjal do Jari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Laranjeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Laranjeiras do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lassance
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lastro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Laurentino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lauro Müller
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lauro de Freitas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lavandeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lavras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lavras da Mangabeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lavras do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lavrinhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lavínia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Leandro Ferreira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lebon Régis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Leme
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Leme do Prado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lençóis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lençóis Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Leoberto Leal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Leopoldina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Leopoldo de Bulhões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Leópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Liberato Salzano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Liberdade
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Licínio de Almeida
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lidianópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lima Campos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lima Duarte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Limeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Limeira do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Limoeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Limoeiro de Anadia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Limoeiro do Ajuru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Limoeiro do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lindoeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lindolfo Collor
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lindóia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lindóia do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Linha Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Linhares
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Livramento
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Livramento de Nossa Senhora
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lizarda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Loanda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lobato
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Logradouro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Londrina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lontra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lontras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lorena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Loreto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lourdes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Louveira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lucas do Rio Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lucena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lucianópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Luciara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lucrécia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lucélia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Luisburgo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Luislândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Luiz Alves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Luiziana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Luiziânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Luminárias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lunardelli
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lupionópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lupércio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lutécia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Luz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Luzerna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Luzilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Luzinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Luziânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Luís Antônio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Luís Correia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Luís Domingues
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Luís Eduardo Magalhães
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Luís Gomes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Lábrea
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Macajuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Macambira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Macaparana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Macapá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Macarani
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Macatuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Macau
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Macaubal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Macaé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Macaíba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Macaúbas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Macedônia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maceió
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Machacalis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Machadinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Machadinho D%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Machado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Machados
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Macieira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Macuco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Macururé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Madalena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Madeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Madre de Deus
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Madre de Deus de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maetinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mafra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Magalhães Barata
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Magalhães de Almeida
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Magda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Magé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maiquinique
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mairi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mairinque
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mairiporã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mairipotaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Major Gercino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Major Isidoro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Major Sales
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Major Vieira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Malacacheta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Malhada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Malhada de Pedras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Malhada dos Bois
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Malhador
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mallet
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Malta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mamanguape
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mambaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mamborê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mamonas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mampituba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Manacapuru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Manaquiri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Manari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Manaus
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Manaíra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mandaguari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mandaguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mandirituba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Manduri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Manfrinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Manga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mangaratiba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mangueirinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Manhuaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Manhumirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Manicoré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Manoel Emídio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Manoel Ribas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Manoel Urbano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Manoel Viana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Manoel Vitorino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mansidão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mantena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mantenópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maquiné
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mar Vermelho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mar de Espanha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mara Rosa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marabá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marabá Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maracaju
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maracajá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maracanaú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maracanã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maracaçumé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maracaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maracás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maragogi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maragogipe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maraial
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marajá do Sena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maranguape
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maranhãozinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marapanim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marapoama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marataízes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maratá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marau
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maravilha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maravilhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maraã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maraú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marcação
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marcelino Ramos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marcelino Vieira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marcelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marcionílio Souza
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marcolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marcos Parente
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marechal Cândido Rondon
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marechal Deodoro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marechal Floriano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marechal Thaumaturgo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maria Helena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maria da Fé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marialva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mariana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mariana Pimentel
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mariano Moro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marianópolis do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maribondo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maricá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marilac
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marilena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mariluz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marilândia do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maringá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maripá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maripá de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marituba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marizópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mariápolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mariópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marliéria
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marmeleiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marmelópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marques de Souza
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marquinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Martinho Campos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Martins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Martins Soares
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Martinópole
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Martinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maruim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marumbi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marzagão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Marília
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mascote
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Massapê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Massapê do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Massaranduba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mata
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mata Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mata Roma
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mata Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mata de São João
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mataraca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mateiros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Matelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Materlândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mateus Leme
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mathias Lobato
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Matias Barbosa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Matias Cardoso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Matias Olímpio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Matina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Matinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Matinhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Matinhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Matipó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mato Castelhano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mato Grosso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mato Leitão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mato Queimado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mato Rico
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mato Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Matos Costa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Matozinhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Matrinchã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Matriz de Camaragibe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Matupá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maturéia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Matutina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Matão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Matões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Matões do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maurilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maurilândia do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mauriti
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mauá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mauá da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maués
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maxaranguape
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maximiliano de Almeida
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mazagão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Maçambará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Medeiros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Medeiros Neto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Medianeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Medicilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Medina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Meleiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Melgaço
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mendes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mendes Pimentel
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mendonça
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mercedes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mercês
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Meridiano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Meruoca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mesquita
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Messias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Messias Targino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mesópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Miguel Alves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Miguel Calmon
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Miguel Leão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Miguel Pereira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Miguelópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Milagres
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Milagres do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Milhã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Milton Brandão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mimoso de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mimoso do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Minador do Negrão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Minas Novas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Minas do Leão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Minaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Minduri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mineiros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mineiros do Tietê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ministro Andreazza
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mira Estrela
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mirabela
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Miracatu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Miracema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Miracema do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mirador
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Miradouro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Miraguaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Miranda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Miranda do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mirandiba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mirandópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mirangaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Miranorte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mirante
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mirante da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mirante do Paranapanema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Miraselva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mirassol
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mirassol d%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mirassolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Miravânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Miraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Miraíma
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mirim Doce
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mirinzal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Missal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Missão Velha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mocajuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mococa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Modelo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Moeda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Moema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mogeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mogi Guaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mogi Mirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mogi das Cruzes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Moiporá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Moita Bonita
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Moju
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mojuí dos Campos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mombaça
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mombuca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mondaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mongaguá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monjolos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monsenhor Gil
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monsenhor Hipólito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monsenhor Paulo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monsenhor Tabosa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Montadas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Montalvânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Montanha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Montanhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Montauri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Alegre de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Alegre de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Alegre de Sergipe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Alegre do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Alegre do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Alegre dos Campos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Alto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Aprazível
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Azul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Azul Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Belo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Belo do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Carlo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Carmelo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Castelo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Formoso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Horebe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Mor
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Negro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Santo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Santo de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Santo do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte Sião
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte das Gameleiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monte do Carmo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monteiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monteiro Lobato
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monteirópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Montenegro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Montes Altos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Montes Claros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Montes Claros de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Montezuma
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Montividiu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Montividiu do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monção
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Monções
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morada Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morada Nova de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Moraújo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Moreilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Moreira Sales
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Moreno
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mormaço
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morpará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morretes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morrinhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morrinhos do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morro Agudo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morro Agudo de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morro Cabeça no Tempo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morro Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morro Redondo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morro Reuter
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morro da Fumaça
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morro da Garça
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morro do Chapéu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morro do Chapéu do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morro do Pilar
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mortugaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Morungaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mossoró
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mossâmedes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mostardas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Motuca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mozarlândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Muaná
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mucajaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mucambo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mucugê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mucuri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mucurici
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Muitos Capões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Muliterno
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mulungu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mulungu do Morro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mundo Novo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Munhoz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Munhoz de Melo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Muniz Ferreira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Muniz Freire
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Muqui
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Muquém do São Francisco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Muriaé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Muribeca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Murici
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Murici dos Portelas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Muricilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Muritiba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Murutinga do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mutum
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mutunópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mutuípe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Muzambinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Muçum
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mário Campos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mâncio Lima
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mãe d%27Água
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Mãe do Rio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nacip Raydan
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nantes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nanuque
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Naque
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Narandiba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Natal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Natalândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Natividade
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Natividade da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Natuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Natércia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Navegantes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Naviraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nazareno
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nazarezinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nazaré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nazaré Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nazaré da Mata
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nazaré do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nazária
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nazário
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nepomuceno
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nerópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Neves Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Neópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nhamundá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nhandeara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nicolau Vergueiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nilo Peçanha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nilópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nina Rodrigues
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ninheira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nioaque
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nipoã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Niquelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Niterói
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nobres
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nonoai
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nordestina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Normandia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nortelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nossa Senhora Aparecida
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nossa Senhora da Glória
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nossa Senhora das Dores
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nossa Senhora das Graças
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nossa Senhora de Lourdes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nossa Senhora de Nazaré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nossa Senhora do Livramento
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nossa Senhora do Socorro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nossa Senhora dos Remédios
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Aliança
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Aliança do Ivaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Alvorada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Alvorada do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova América
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova América da Colina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Andradina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Araçá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Aurora
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Bandeirantes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Bassano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Belém
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Boa Vista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Brasilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Brasilândia D%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Bréscia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Campina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Canaã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Canaã Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Canaã do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Candelária
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Cantu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Castilho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Colinas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Crixás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Cruz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Era
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Erechim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Esperança
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Esperança do Piriá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Esperança do Sudoeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Esperança do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Europa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Floresta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Friburgo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Fátima
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Glória
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Granada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Guarita
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Guataporanga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Hartz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Ibiá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Iguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Iguaçu de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Independência
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Iorque
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Ipixuna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Itaberaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Itarana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Lacerda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Laranjeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Lima
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Londrina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Luzitânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Mamoré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Marilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Maringá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Monte Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Mutum
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Módica
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Nazaré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Odessa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Olinda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Olinda do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Olinda do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Olímpia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Palma
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Palmeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Petrópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Ponte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Porteirinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Prata
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Prata do Iguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Pádua
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Ramada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Redenção
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Resende
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Roma
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Roma do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Rosalândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Russas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Santa Bárbara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Santa Helena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Santa Rita
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Santa Rosa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Serrana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Soure
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Tebas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Timboteua
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Trento
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Ubiratã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova União
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Veneza
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Venécia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Viçosa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nova Xavantina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novais
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Acordo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Airão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Aripuanã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Barreiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Brasil
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Cabrais
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Cruzeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Gama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Hamburgo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Horizonte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Horizonte do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Horizonte do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Horizonte do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Itacolomi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Jardim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Lino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Machado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Mundo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Oriente
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Oriente de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Oriente do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Planalto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Progresso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Repartimento
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Santo Antônio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo São Joaquim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Tiradentes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Triunfo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novo Xingu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Novorizonte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nuporanga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Não-Me-Toque
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Nísia Floresta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ocara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ocauçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Oeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Oeiras do Pará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Oiapoque
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Olaria
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Olho D%27Água do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Olho d%27Água
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Olho d%27Água Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Olho d%27Água das Cunhãs
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Olho d%27Água das Flores
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Olho d%27Água do Borges
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Olho d%27Água do Casado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Olhos-d%27Água
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Olinda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Olinda Nova do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Olindina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Olivedos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Oliveira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Oliveira Fortes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Oliveira de Fátima
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Oliveira dos Brejinhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Olivença
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Olímpia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Olímpio Noronha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Onda Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Onça de Pitangui
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Oratórios
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Oriente
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Orindiúva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Oriximiná
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Orizona
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Orizânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Orleans
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Orlândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Orobó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Orocó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ortigueira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Orós
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Osasco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Oscar Bressane
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Osvaldo Cruz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Osório
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Otacílio Costa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ouricuri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ourilândia do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ourinhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ourizona
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ouriçangas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ouro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ouro Branco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ouro Fino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ouro Preto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ouro Preto do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ouro Velho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ouro Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ouro Verde de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ouro Verde de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ouro Verde do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ouroeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ourolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ourém
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ouvidor
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pacaembu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pacajus
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pacajá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pacaraima
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pacatuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pacoti
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pacujá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Padre Bernardo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Padre Carvalho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Padre Marcos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Padre Paraíso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paes Landim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pai Pedro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paial
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paim Filho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paineiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Painel
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pains
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paiva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paiçandu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pajeú do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palestina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palestina de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palestina do Pará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palhano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palhoça
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palma
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palma Sola
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmares
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmares Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmares do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmas de Monte Alto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmeira d%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmeira das Missões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmeira do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmeira dos Índios
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmeirais
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmeirante
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmeiras de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmeiras do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmeirina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmeirândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmeirópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmelo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palminópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmital
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmitinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmitos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmácia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palmópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Palotina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Panambi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Panamá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pancas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Panelas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Panorama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pantano Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Papagaios
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Papanduva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paquetá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paracambi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paracatu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paracuru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paragominas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paraguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paraguaçu Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paraibano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paraibuna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paraipaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paraisópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Parambu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paramirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paramoti
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paranacity
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paranaguá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paranaiguara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paranapanema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paranapoema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paranapuã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paranatama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paranatinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paranavaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paranaíba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paranaíta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paranhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paraná
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paranã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paraopeba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Parapuã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Parari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paratinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paraty
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Parauapebas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Parazinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paraíba do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paraíso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paraíso das Águas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paraíso do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paraíso do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paraíso do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paraú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paraúna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pardinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pareci Novo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Parecis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Parelhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pariconha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Parintins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paripiranga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paripueira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pariquera-Açu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Parisi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Parnaguá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Parnamirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Parnarama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Parnaíba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Parobé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pará de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Passa Quatro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Passa Sete
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Passa Tempo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Passa Vinte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Passa e Fica
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Passabém
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Passagem
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Passagem Franca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Passagem Franca do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Passira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Passo Fundo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Passo de Camaragibe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Passo de Torres
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Passo do Sobrado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Passos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Passos Maia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pastos Bons
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Patis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pato Bragado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pato Branco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Patos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Patos de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Patos do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Patrocínio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Patrocínio Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Patrocínio do Muriaé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Patu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paty do Alferes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pau Brasil
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pau D%27Arco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pau D%27Arco do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pau dos Ferros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paudalho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pauini
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paula Cândido
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paula Freitas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paulicéia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paulino Neves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paulistana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paulistas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paulistânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paulo Afonso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paulo Bento
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paulo Frontin
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paulo Jacinto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paulo Lopes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paulo Ramos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paulo de Faria
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paulínia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paverama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pavussu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pavão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Paço do Lumiar
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Peabiru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pederneiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedra Azul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedra Bela
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedra Bonita
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedra Branca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedra Branca do Amapari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedra Dourada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedra Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedra Lavrada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedra Mole
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedra Preta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedra do Anta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedra do Indaiá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedralva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedranópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedras Altas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedras Grandes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedras de Fogo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedras de Maria da Cruz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedregulho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedreira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedreiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedrinhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedrinhas Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedrinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedro Afonso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedro Alexandre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedro Avelino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedro Canário
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedro Gomes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedro II
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedro Laurentino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedro Leopoldo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedro Osório
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedro Régis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedro Teixeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedro Velho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedro de Toledo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedro do Rosário
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pedrão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Peixe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Peixe-Boi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Peixoto de Azevedo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pejuçara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pelotas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Penaforte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Penalva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pendências
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Penedo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Penha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pentecoste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Penápolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pequeri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pequi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pequizeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Perdigão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Perdizes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Perdões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pereira Barreto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pereiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pereiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Peri Mirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Periquito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Peritiba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Peritoró
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Perobal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Perolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Peruíbe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pescador
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pescaria Brava
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pesqueira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Petrolina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Petrolina de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Petrolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Petrópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Peçanha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piacatu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piancó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piatã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piau
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piaçabuçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Picada Café
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Picos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Picuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piedade
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piedade de Caratinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piedade de Ponte Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piedade do Rio Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piedade dos Gerais
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pilar
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pilar de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pilar do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pilão Arcado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pilões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pilõezinhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pimenta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pimenta Bueno
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pimenteiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pimenteiras do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pindamonhangaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pindaré-Mirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pindaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pindoba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pindobaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pindorama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pindorama do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pindoretama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pingo d%27Água
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pinhais
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pinhal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pinhal Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pinhal da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pinhal de São Bento
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pinhalzinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pinhalão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pinheiral
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pinheirinho do Vale
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pinheiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pinheiro Machado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pinheiro Preto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pinheiros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pinhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pintadas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pinto Bandeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pintópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pio IX
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pio XII
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piquerobi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piquet Carneiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piquete
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piracaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piracanjuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piracema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piracicaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piracuruca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piraju
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pirajuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pirajuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pirambu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piranga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pirangi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piranguinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piranguçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piranhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pirapemas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pirapetinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pirapora
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pirapora do Bom Jesus
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pirapozinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pirapó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piraquara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piraquê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pirassununga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piratini
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piratininga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piratuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piraí do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piraí do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piraúba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pirenópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pires Ferreira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pires do Rio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piripiri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piripá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piritiba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pirpirituba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pitanga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pitangueiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pitangui
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pitimbu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pium
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piumhi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piçarra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piên
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Piúma
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Placas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Planaltina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Planaltina do Paraná
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Planaltino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Planalto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Planalto Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Planalto da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Planura
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Platina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Plácido de Castro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pocinhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Poconé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pocrane
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pojuca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Poloni
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pombal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pombos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pomerode
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pompéia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pompéu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pongaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ponta Grossa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ponta Porã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ponta de Pedras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pontal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pontal do Araguaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pontal do Paraná
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pontalina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pontalinda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ponte Alta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ponte Alta do Bom Jesus
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ponte Alta do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ponte Alta do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ponte Branca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ponte Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ponte Preta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ponte Serrada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pontes Gestal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pontes e Lacerda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ponto Belo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ponto Chique
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ponto Novo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ponto dos Volantes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pontão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Populina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Poranga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porangaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porangatu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porciúncula
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porecatu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Portalegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porteiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porteirinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porteirão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Portel
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Portelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Acre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Alegre do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Alegre do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Alegre do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Amazonas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Barreiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Belo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Calvo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Esperidião
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Estrela
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Feliz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Ferreira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Firme
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Franco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Lucena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Mauá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Murtinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Nacional
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Real
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Real do Colégio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Rico
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Rico do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Seguro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto União
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Velho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Vera Cruz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Vitória
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Walter
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto Xavier
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto da Folha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto de Moz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto de Pedras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto do Mangue
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Porto dos Gaúchos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Portão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Posse
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Potengi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Potim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Potiraguá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Potirendaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Potiretama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Poté
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pouso Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pouso Alto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pouso Novo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pouso Redondo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Poxoréu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Poá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Poço Branco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Poço Dantas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Poço Fundo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Poço Redondo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Poço Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Poço das Antas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Poço das Trincheiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Poço de José de Moura
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Poços de Caldas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Poção
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Poção de Pedras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Poções
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pracinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pracuúba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Prado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Prado Ferreira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Prados
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pradópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Praia Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Praia Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Prainha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pranchita
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Prata
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Prata do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pratinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pratápolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pratânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Alves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Bernardes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Castello Branco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Castelo Branco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Dutra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Epitácio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Figueiredo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Getúlio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Juscelino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Jânio Quadros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Kennedy
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Kubitschek
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Lucena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Médici
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Nereu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Olegário
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Prudente
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Sarney
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Tancredo Neves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Vargas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Presidente Venceslau
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Primavera
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Primavera de Rondônia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Primavera do Leste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Primeira Cruz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Primeiro de Maio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Princesa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Princesa Isabel
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Professor Jamil
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Progresso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Promissão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Propriá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Protásio Alves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Prudente de Morais
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Prudentópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pugmil
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pureza
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Putinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Puxinanã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pão de Açúcar
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pé de Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pérola
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Pérola d%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quadra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quaraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quartel Geral
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quarto Centenário
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quatiguá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quatipuru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quatis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quatro Barras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quatro Irmãos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quatro Pontes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quatá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quebrangulo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quedas do Iguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Queimada Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Queimadas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Queimados
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Queiroz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Queluz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Queluzito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Querência
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Querência do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quevedos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quijingue
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quilombo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quinta do Sol
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quintana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quinze de Novembro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quipapá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quirinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quissamã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quitandinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quiterianópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quixaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quixabeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quixadá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quixelô
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quixeramobim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Quixeré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rafael Fernandes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rafael Godeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rafael Jambeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rafard
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ramilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rancharia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rancho Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rancho Alegre D%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rancho Queimado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Raposa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Raposos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Raul Soares
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Realeza
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rebouças
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Recife
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Recreio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Recursolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Redentora
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Redenção
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Redenção da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Redenção do Gurguéia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Reduto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Regeneração
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Regente Feijó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Reginópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Registro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Relvado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Remanso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Remígio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Renascença
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Reriutaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Resende
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Resende Costa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Reserva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Reserva do Cabaçal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Reserva do Iguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Resplendor
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ressaquinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Restinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Restinga Sêca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Retirolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riachinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riacho Frio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riacho da Cruz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riacho das Almas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riacho de Santana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riacho de Santo Antônio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riacho dos Cavalos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riacho dos Machados
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riachuelo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riachão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riachão das Neves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riachão do Bacamarte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riachão do Dantas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riachão do Jacuípe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riachão do Poço
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rialma
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rianápolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribamar Fiquene
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribas do Rio Pardo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeira do Amparo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeira do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeira do Pombal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeiro Gonçalves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeirão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeirão Bonito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeirão Branco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeirão Cascalheira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeirão Claro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeirão Corrente
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeirão Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeirão Pires
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeirão Preto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeirão Vermelho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeirão das Neves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeirão do Largo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeirão do Pinhal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeirão do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeirão dos Índios
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeirãozinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ribeirópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rifaina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rincão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Acima
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Azul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Bananal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Bom
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Bonito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Bonito do Iguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Branco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Branco do Ivaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Branco do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Brilhante
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Casca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Claro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Crespo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Doce
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Espera
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Formoso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Fortuna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Grande da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Grande do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Largo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Manso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Maria
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Negrinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Negro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Novo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Novo do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Paranaíba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Pardo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Pardo de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Piracicaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Pomba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Preto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Preto da Eva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Quente
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Real
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Rufino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Sono
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Tinto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Verde de Mato Grosso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio Vermelho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio da Conceição
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio das Antas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio das Flores
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio das Ostras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio das Pedras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio de Contas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio de Janeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio do Antônio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio do Campo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio do Fogo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio do Pires
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio do Prado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio dos Bois
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio dos Cedros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rio dos Índios
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riozinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riqueza
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ritápolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Riversul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Roca Sales
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rochedo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rochedo de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rodeio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rodeio Bonito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rodeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rodelas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rodolfo Fernandes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rodrigues Alves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rolador
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rolante
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rolim de Moura
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Romaria
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Romelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Roncador
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ronda Alta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rondinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rondolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rondon
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rondon do Pará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rondonópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Roque Gonzales
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rorainópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rosana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Roseira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rosário
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rosário Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rosário da Limeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rosário do Catete
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rosário do Ivaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rosário do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Roteiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rubelita
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rubiataba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rubim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rubinéia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rubiácea
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Rurópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Russas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ruy Barbosa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sabará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sabino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sabinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Saboeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sabáudia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sacramento
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sagrada Família
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sagres
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sairé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Saldanha Marinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sales
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sales Oliveira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salesópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salete
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salgadinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salgado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salgado Filho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salgado de São Félix
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salgueiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salinas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salinas da Margarida
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salitre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salmourão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Saloá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Saltinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salto Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salto Veloso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salto da Divisa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salto de Pirapora
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salto do Céu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salto do Itararé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salto do Jacuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salto do Lontra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salvador
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salvador das Missões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salvador do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Salvaterra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sambaíba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sampaio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sananduva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sanclerlândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sandolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sandovalina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sangão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sanharó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sant%27Ana do Livramento
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Adélia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Albertina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Amélia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Branca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Brígida
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Bárbara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Bárbara d%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Bárbara de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Bárbara do Leste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Bárbara do Monte Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Bárbara do Pará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Bárbara do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Bárbara do Tugúrio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Carmem
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cecília
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cecília do Pavão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cecília do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Clara d%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Clara do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz Cabrália
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz da Baixa Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz da Conceição
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz da Esperança
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz da Vitória
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz das Palmeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz de Monte Castelo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz de Salinas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz do Arari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz do Capibaribe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz do Escalvado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz do Rio Pardo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz do Xingu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Cruz dos Milagres
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Efigênia de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Ernestina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Filomena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Filomena do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Fé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Fé de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Fé de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Fé do Araguaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Fé do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Gertrudes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Helena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Helena de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Helena de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Inês
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Isabel
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Isabel do Ivaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Isabel do Rio Negro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Izabel do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Izabel do Pará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Juliana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Leopoldina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Luz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Luzia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Luzia D%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Luzia do Itanhy
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Luzia do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Luzia do Paruá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Luzia do Pará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Lúcia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Margarida
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Margarida do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Maria
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Maria Madalena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Maria da Boa Vista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Maria da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Maria da Vitória
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Maria das Barreiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Maria de Itabira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Maria de Jetibá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Maria do Cambucá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Maria do Herval
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Maria do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Maria do Pará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Maria do Salto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Maria do Suaçuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Maria do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Mariana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Mercedes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Mônica
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Quitéria
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Quitéria do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rita
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rita d%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rita de Caldas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rita de Cássia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rita de Ibitipoca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rita de Jacutinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rita de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rita do Araguaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rita do Itueto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rita do Novo Destino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rita do Pardo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rita do Passa Quatro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rita do Sapucaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rita do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rita do Trivelato
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rosa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rosa da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rosa de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rosa de Lima
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rosa de Viterbo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rosa do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rosa do Purus
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rosa do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Rosa do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Salete
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Teresa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Teresinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Tereza
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Tereza de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Tereza do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Tereza do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Terezinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Terezinha de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Terezinha de Itaipu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Terezinha do Progresso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Terezinha do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Vitória
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santa Vitória do Palmar
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santaluz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana da Boa Vista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana da Ponte Pensa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana da Vargem
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana de Cataguases
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana de Mangueira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana de Parnaíba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana de Pirapama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana do Acaraú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana do Araguaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana do Cariri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana do Deserto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana do Garambéu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana do Ipanema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana do Itararé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana do Jacaré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana do Manhuaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana do Matos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana do Mundaú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana do Paraíso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana do Riacho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana do Seridó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana do São Francisco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana dos Garrotes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santana dos Montes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santanópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santarém
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santarém Novo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santiago
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santiago do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Afonso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Amaro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Amaro da Imperatriz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Amaro das Brotas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Amaro do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Anastácio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo André
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio da Alegria
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio da Barra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio da Patrulha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio da Platina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio das Missões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio de Jesus
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio de Lisboa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio de Posse
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio de Pádua
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Amparo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Aracanguá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Aventureiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Caiuá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Descoberto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Grama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Itambé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Içá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Jacinto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Jardim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Leste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Leverger
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Monte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Palma
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Paraíso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Pinhal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Planalto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Retiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Rio Abaixo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Sudoeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio do Tauá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio dos Lopes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Antônio dos Milagres
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Augusto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Cristo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Estêvão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Expedito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Expedito do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Hipólito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Inácio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Inácio do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santo Ângelo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santos Dumont
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Santópolis do Aguapeí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sapeaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sapezal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sapiranga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sapopema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sapucaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sapucaia do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sapucaí-Mirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sapé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Saquarema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sarandi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sarapuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sardoá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sarutaiá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sarzedo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Satuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Satubinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Saubara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Saudade do Iguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Saudades
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Saúde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Schroeder
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Seabra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Seara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sebastianópolis do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sebastião Barros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sebastião Laranjeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sebastião Leal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Seberi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sede Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Segredo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Selbach
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Selvíria
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sem-Peixe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sena Madureira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senador Alexandre Costa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senador Amaral
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senador Canedo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senador Cortes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senador Elói de Souza
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senador Firmino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senador Georgino Avelino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senador Guiomard
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senador José Bento
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senador José Porfírio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senador La Rocque
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senador Modestino Gonçalves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senador Pompeu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senador Rui Palmeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senador Salgado Filho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senador Sá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sengés
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senhor do Bonfim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senhora de Oliveira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senhora do Porto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Senhora dos Remédios
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sentinela do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sento Sé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serafina Corrêa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sericita
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Seringueiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Seritinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Seropédica
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra Alta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra Azul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra Azul de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra Branca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra Caiada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra Dourada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra Negra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra Negra do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra Nova Dourada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra Preta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra Redonda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra Talhada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra da Raiz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra da Saudade
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra de São Bento
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra do Mel
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra do Navio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra do Ramalho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra do Salitre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serra dos Aimorés
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serrana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serrania
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serrano do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serranos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serranópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serranópolis de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serranópolis do Iguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serraria
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serrinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serrinha dos Pintos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serrita
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Serrolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sertaneja
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sertanópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sertânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sertão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sertão Santana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sertãozinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sete Barras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sete Lagoas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sete Quedas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sete de Setembro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Setubinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Severiano Melo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Severiano de Almeida
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Severínia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Siderópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sidrolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sigefredo Pacheco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Silva Jardim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Silvanópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Silveira Martins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Silveiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Silveirânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Silves
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Silvianópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Silvânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Simolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Simonésia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Simplício Mendes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Simão Dias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Simão Pereira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Simões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Simões Filho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sinimbu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sinop
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Siqueira Campos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sirinhaém
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Siriri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sobradinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sobrado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sobral
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sobrália
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Socorro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Socorro do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Soledade
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Soledade de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Solidão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Solonópole
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Solânea
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sombrio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sonora
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sooretama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sorocaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sorriso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sossêgo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Soure
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sousa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Souto Soares
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sucupira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sucupira do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sucupira do Riachão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sud Mennucci
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sul Brasil
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sulina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sumaré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sumidouro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sumé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Surubim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sussuapara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Suzano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Suzanápolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sátiro Dias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Benedito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Benedito do Rio Preto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Benedito do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Bentinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Bento
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Bento Abade
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Bento do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Bento do Sapucaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Bento do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Bento do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Bento do Trairí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Bento do Una
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Bernardino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Bernardo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Bernardo do Campo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Bonifácio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Borja
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Braz do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Brás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Brás do Suaçuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Caetano de Odivelas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Caetano do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Caitano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Carlos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Carlos do Ivaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Cristóvão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Cristóvão do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Desidério
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Domingos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Domingos das Dores
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Domingos do Araguaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Domingos do Azeitão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Domingos do Capim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Domingos do Cariri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Domingos do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Domingos do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Domingos do Prata
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Domingos do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Felipe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Felipe D%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Fernando
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Fidélis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Francisco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Francisco de Assis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Francisco de Assis do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Francisco de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Francisco de Itabapoana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Francisco de Paula
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Francisco de Sales
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Francisco do Brejão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Francisco do Conde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Francisco do Glória
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Francisco do Guaporé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Francisco do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Francisco do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Francisco do Pará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Francisco do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Francisco do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Félix
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Félix de Balsas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Félix de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Félix do Araguaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Félix do Coribe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Félix do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Félix do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Félix do Xingu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Gabriel
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Gabriel da Cachoeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Gabriel da Palha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Gabriel do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Geraldo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Geraldo da Piedade
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Geraldo do Araguaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Geraldo do Baixio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Gonçalo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Gonçalo do Abaeté
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Gonçalo do Amarante
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Gonçalo do Gurguéia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Gonçalo do Pará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Gonçalo do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Gonçalo do Rio Abaixo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Gonçalo do Rio Preto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Gonçalo do Sapucaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Gonçalo dos Campos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Gotardo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Jerônimo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Jerônimo da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Joaquim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Joaquim da Barra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Joaquim de Bicas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Joaquim do Monte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Jorge
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Jorge d%27Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Jorge do Ivaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Jorge do Patrocínio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José da Barra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José da Bela Vista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José da Boa Vista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José da Coroa Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José da Lagoa Tapada
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José da Laje
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José da Lapa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José da Safira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José da Tapera
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José da Varginha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José da Vitória
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José das Missões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José das Palmeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José de Caiana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José de Espinharas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José de Mipibu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José de Piranhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José de Princesa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José de Ribamar
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José de Ubá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Barreiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Belmonte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Bonfim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Brejo do Cruz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Calçado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Campestre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Cedro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Cerrito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Divino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Egito
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Goiabal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Herval
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Hortêncio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Inhacorá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Jacuri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Jacuípe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Mantimento
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Ouro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Peixe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Povo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Rio Claro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Rio Pardo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Rio Preto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Sabugi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Seridó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Vale do Rio Preto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José do Xingu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José dos Ausentes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José dos Basílios
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José dos Campos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José dos Cordeiros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José dos Pinhais
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José dos Quatro Marcos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São José dos Ramos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João Batista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João Batista do Glória
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João Evangelista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João Nepomuceno
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João d%27Aliança
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João da Baliza
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João da Barra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João da Boa Vista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João da Canabrava
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João da Fronteira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João da Lagoa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João da Mata
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João da Paraúna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João da Ponta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João da Ponte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João da Urtiga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João da Varjota
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João das Duas Pontes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João das Missões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João de Iracema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João de Meriti
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João de Pirabas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João del Rei
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Araguaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Arraial
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Caiuá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Cariri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Carú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Itaperiú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Ivaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Jaguaribe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Manhuaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Manteninha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Oriente
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Pacuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Paraíso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Pau d%27Alho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Polêsine
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Rio do Peixe
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Sabugi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Soter
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Tigre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João do Triunfo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São João dos Patos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Julião
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Leopoldo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Lourenço
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Lourenço da Mata
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Lourenço da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Lourenço do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Lourenço do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Lourenço do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Ludgero
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Luis do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Luiz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Luiz Gonzaga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Luiz do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Luiz do Paraitinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Luís
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Luís Gonzaga do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Luís de Montes Belos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Luís do Curu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Luís do Quitunde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Mamede
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Manoel do Paraná
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Manuel
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Marcos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Martinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Martinho da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Mateus
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Mateus do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Mateus do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel Arcanjo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel da Baixa Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel da Boa Vista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel das Matas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel das Missões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel de Taipu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel do Aleixo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel do Anta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel do Araguaia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel do Fidalgo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel do Gostoso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel do Guamá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel do Guaporé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel do Iguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel do Passa Quatro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel do Tapuio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel dos Campos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Miguel dos Milagres
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Nicolau
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Patrício
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Paulo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Paulo das Missões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Paulo de Olivença
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Paulo do Potengi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Pedro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Pedro da Aldeia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Pedro da Cipa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Pedro da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Pedro da União
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Pedro da Água Branca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Pedro das Missões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Pedro de Alcântara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Pedro do Butiá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Pedro do Iguaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Pedro do Ivaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Pedro do Paraná
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Pedro do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Pedro do Suaçuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Pedro do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Pedro do Turvo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Pedro dos Crentes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Pedro dos Ferros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Rafael
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Raimundo Nonato
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Raimundo das Mangabeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Raimundo do Doca Bezerra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Roberto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Romão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Roque
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Roque de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Roque do Canaã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Salvador do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião da Amoreira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião da Bela Vista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião da Boa Vista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião da Grama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião da Vargem Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião de Lagoa de Roça
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião do Alto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião do Anta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião do Caí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião do Paraíso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião do Passé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião do Rio Preto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião do Rio Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião do Uatumã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sebastião do Umbuzeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Sepé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Simão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Tiago
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Tomás de Aquino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Tomé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Tomé das Letras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Valentim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Valentim do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Valério
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Valério do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Vendelino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Vicente
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Vicente Ferrer
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Vicente Férrer
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Vicente de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Vicente do Seridó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=São Vicente do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sério
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sítio Novo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sítio Novo do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sítio d%27Abadia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sítio do Mato
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Sítio do Quinto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tabaporã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tabapuã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tabatinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tabaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tabira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tabocas do Brejo Velho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tabocão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taboleiro Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taboão da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tabuleiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tabuleiro do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tacaimbó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tacaratu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taciba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tacima
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tacuru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taguatinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taguaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taiaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tailândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taiobeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taipas do Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taipu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taió
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taiúva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Talismã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tamandaré
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tamarana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tambaú
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tamboara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tamboril
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tamboril do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tanabi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tangará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tangará da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tanguá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tanhaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tanque Novo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tanque d%27Arca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tanque do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tanquinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taparuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tapauá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tapejara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tapera
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taperoá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tapes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tapira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tapiramutá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tapiratiba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tapiraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tapurah
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taquara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taquaral
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taquaral de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taquarana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taquaraçu de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taquari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taquaritinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taquaritinga do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taquarituba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taquarivaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taquarussu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taquaruçu do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tarabai
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tarauacá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tarrafas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tartarugalzinho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tarumirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tarumã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tasso Fragoso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tatuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Taubaté
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tauá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tavares
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tefé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Teixeira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Teixeira Soares
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Teixeira de Freitas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Teixeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Teixeirópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tejupá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tejuçuoca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Telha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Telêmaco Borba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tenente Ananias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tenente Laurentino Cruz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tenente Portela
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tenório
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Teodoro Sampaio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Teofilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Teolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Teotônio Vilela
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Terenos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Teresina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Teresina de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Teresópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Terezinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Terezópolis de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Terra Alta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Terra Boa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Terra Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Terra Nova do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Terra Rica
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Terra Roxa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Terra Santa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Terra de Areia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tesouro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Teutônia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Teófilo Otoni
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Theobroma
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tianguá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tibagi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tibau
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tibau do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tietê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tigrinhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tijucas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tijucas do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Timbaúba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Timbaúba dos Batistas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Timbiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Timburi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Timbé do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Timbó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Timbó Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Timon
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Timóteo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tio Hugo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tiradentes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tiradentes do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tiros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tobias Barreto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tocantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tocantinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tocantínia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tocos do Moji
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Toledo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tomar do Geru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tomazina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tombos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tomé-Açu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tonantins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Toritama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Torixoréu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Toropi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Torre de Pedra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Torres
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Torrinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Touros
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Trabiju
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tracuateua
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tracunhaém
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Traipu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Trairi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Trairão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Trajano de Moraes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tramandaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Travesseiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tremedal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tremembé
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Treviso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Treze Tílias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Treze de Maio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Trindade
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Trindade do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Triunfo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Triunfo Potiguar
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Trizidela do Vale
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Trombas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Trombudo Central
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Três Arroios
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Três Barras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Três Barras do Paraná
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Três Cachoeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Três Corações
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Três Coroas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Três Forquilhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Três Fronteiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Três Lagoas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Três Marias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Três Palmeiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Três Passos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Três Pontas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Três Ranchos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Três Rios
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Três de Maio
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tubarão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tucano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tucumã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tucunduva
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tucuruí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tufilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tuiuti
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tumiritinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tunas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tunas do Paraná
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tuneiras do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tuntum
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tunápolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tupaciguara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tupanatinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tupanci do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tupanciretã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tupandi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tuparendi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tuparetama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tupi Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tupirama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tupiratins
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tupã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tupãssi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Turiaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Turilândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Turiúba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Turmalina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tururu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Turuçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Turvelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Turvo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Turvolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Turvânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Tutóia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uarini
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uauá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ubaitaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ubajara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ubaporanga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ubarana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ubatuba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ubatã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ubaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ubaíra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uberaba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uberlândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ubirajara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ubiratã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ubiretama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ubá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uchoa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uibaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uiramutã
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uirapuru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uiraúna
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ulianópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Umari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Umarizal
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Umbaúba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Umburanas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Umburatiba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Umbuzeiro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Umirim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Umuarama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Una
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Unaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uniflor
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Unistalda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=União
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=União Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=União da Serra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=União da Vitória
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=União de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=União do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=União do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=União dos Palmares
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Upanema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Urandi
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uraí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Urbano Santos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uru
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uruana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uruana de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uruará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uruaçu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Urubici
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uruburetama
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Urucará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Urucuia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Urucurituba
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Urucânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uruguaiana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uruoca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Urupema
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Urupá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Urupês
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Urussanga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Urutaí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uruçuca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Uruçuí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Urânia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Utinga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vacaria
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vale Real
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vale Verde
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vale de São Domingos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vale do Anari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vale do Paraíso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vale do Sol
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Valente
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Valentim Gentil
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Valença
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Valença do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Valinhos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Valparaíso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Valparaíso de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vanini
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vargem
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vargem Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vargem Alta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vargem Bonita
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vargem Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vargem Grande Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vargem Grande do Rio Pardo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vargem Grande do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vargeão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Varginha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Varjota
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Varjão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Varjão de Minas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Varre-Sai
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Varzedo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Varzelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vassouras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vazante
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Venda Nova do Imigrante
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Venha-Ver
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ventania
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Venturosa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Venâncio Aires
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vera
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vera Cruz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vera Cruz do Oeste
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vera Mendes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Veranópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Verdejante
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Verdelândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vereda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Veredinha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vermelho Novo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vertente do Lério
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vertentes
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Verê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Veríssimo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vespasiano
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vespasiano Corrêa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Viadutos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Viamão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Viana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vianópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vicente Dutra
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vicentina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vicentinópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Victor Graeff
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vicência
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vidal Ramos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Videira
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vieiras
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vieirópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vigia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vila Bela da Santíssima Trindade
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vila Boa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vila Flor
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vila Flores
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vila Lângaro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vila Maria
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vila Nova do Piauí
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vila Nova do Sul
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vila Nova dos Martírios
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vila Pavão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vila Propício
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vila Rica
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vila Valério
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vila Velha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vilhena
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vinhedo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Viradouro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Virgem da Lapa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Virginópolis
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Virgolândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Virgínia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Virmond
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Visconde do Rio Branco
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Viseu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vista Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vista Alegre do Alto
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vista Alegre do Prata
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vista Gaúcha
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vista Serrana
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vitor Meireles
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vitorino
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vitorino Freire
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vitória
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vitória Brasil
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vitória da Conquista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vitória das Missões
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vitória de Santo Antão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vitória do Jari
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vitória do Mearim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Vitória do Xingu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Viçosa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Viçosa do Ceará
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Volta Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Volta Redonda
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Votorantim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Votuporanga
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Várzea
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Várzea Alegre
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Várzea Branca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Várzea Grande
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Várzea Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Várzea Paulista
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Várzea da Palma
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Várzea da Roça
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Várzea do Poço
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Wagner
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Wall Ferraz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Wanderley
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Wanderlândia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Wenceslau Braz
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Wenceslau Guimarães
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Westfália
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Witmarsum
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Xambioá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Xambrê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Xangri-lá
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Xanxerê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Xapuri
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Xavantina
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Xaxim
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Xexéu
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Xinguara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Xique-Xique
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Zabelê
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Zacarias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Zortéa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Zé Doca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=__HIVE_DEFAULT_PARTITION__
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Água Azul do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Água Boa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Água Branca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Água Clara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Água Comprida
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Água Doce
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Água Doce do Maranhão
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Água Doce do Norte
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Água Fria
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Água Fria de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Água Limpa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Água Nova
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Água Preta
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Água Santa
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Águas Belas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Águas Formosas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Águas Frias
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Águas Lindas de Goiás
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Águas Mornas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Águas Vermelhas
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Águas da Prata
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Águas de Chapecó
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Águas de Lindóia
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Águas de Santa Bárbara
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Águas de São Pedro
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Águia Branca
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Álvares Florence
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Álvares Machado
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Álvaro de Carvalho
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Áurea
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Ângulo
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Érico Cardoso
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Óbidos
    drwxr-xr-x   - root supergroup          0 2022-04-27 08:44 hdfs://namenode:8020/user/hive/warehouse/covidbr/municipio=Óleo


# Criar as 3 visualizações pelo Spark com os dados enviados para o HDFS


```python
# Acessar os dados da tabela municipio do Banco de dados covidbr pelo SparkSQL
spark.sql("SHOW DATABASES").show() #Mostrar os anco de dados
```

    +------------+
    |databaseName|
    +------------+
    |     covidbr|
    |     default|
    +------------+
    



```python
# Selecionar o banco de dados covidbr 
spark.sql("USE covidbr")

```




    DataFrame[]




```python
# Acessar os dados da tabela municipio do Banco de dados covidbr pelo SparkSQL
spark.sql("SHOW TABLES").show() #Mostrar os anco de dados
```

    +--------+---------+-----------+
    |database|tableName|isTemporary|
    +--------+---------+-----------+
    | covidbr|municipio|      false|
    +--------+---------+-----------+
    


# Visualização 1 - Casos Recuperados | Em Acompanhamento
Obs.: Os resultados serão extraídos a partir da última data registrada que foi em 2021-07-06.


```python
## 1.1 Casos Recuperados
df_casos_recuperados = spark.sql("SELECT Recuperadosnovos as Casos_Recuperados FROM municipio order by 1 desc limit 1")
df_casos_recuperados.show()

## 1.2 Em Acompanhamento
df_em_acompanhamento = spark.sql("SELECT emAcompanhamentoNovos as Em_Acompanhamento FROM municipio WHERE order by 1 desc limit 1")
df_em_acompanhamento.show()
```

    +-----------------+
    |Casos_Recuperados|
    +-----------------+
    |         17262646|
    +-----------------+
    
    +-----------------+
    |Em_Acompanhamento|
    +-----------------+
    |          1317658|
    +-----------------+
    


### Visualização 2 - Casos Acumulado | Casos Novos | Incidência
Obs.: **Incidência:** Quantidade proporcional de casos confirmados para cada 1 milhão de habitantes. A população considerada no cálculo é a estimativa populacional para 2019 do Instituto Brasileiro de Geografia e Estatística (IBGE), salvo quando especificada referência distinta. **Método de cálculo: (casos confirmados * 1.000.000) / população**.
Fonte: https://www.coronavirus.sc.gov.br/sobre-os-dados/.
No caso no painel será utilizado **Método de cálculo: (casos confirmados * 100.000) / população**


```python
#2.1 Acumulado
df_casos_acumulados = spark.sql("SELECT casosAcumulado as Casos_Acumulados FROM municipio order by 1 desc limit 1")
df_casos_acumulados.show()

#2.2 Casos novos
df_casos_novos = spark.sql("SELECT casosNovos as Casos_Novos FROM municipio order by 1 desc limit 1")
df_casos_novos.show()

#2.3 Incidência (Casos acumulados)
df_incidencia = spark.sql("SELECT cast(((casosAcumulado*100000)/populacaoTCU2019) as decimal(5,1)) as Incidencia FROM municipio order by 1 desc limit 1")
df_incidencia.show()
```

    +----------------+
    |Casos_Acumulados|
    +----------------+
    |        18855015|
    +----------------+
    
    +-----------+
    |Casos_Novos|
    +-----------+
    |     115228|
    +-----------+
    
    +----------+
    |Incidencia|
    +----------+
    |    9999.8|
    +----------+
    


### Visualização 3 - Óbtos Acumulados | Óbtos Novos | Letalidade | Mortalidade
Obs.1: **Letalidade:** Taxa percentual de casos confirmados que evoluíram a óbito. **Método de cálculo: (número de óbitos x 100) / número de casos confirmados**.

Obs.2: **Mortalidade:** Quantidade proporcional de óbitos para cada 1 milhão habitantes, seguindo a mesma metodologia de cálculo da incidência de casos confirmados. **Método de cálculo: (óbitos * 1.000.000) / população**.
No caso no painel será utilizado **Método de cálculo: (óbitos * 100.000) / população**
Fonte: https://www.coronavirus.sc.gov.br/sobre-os-dados/


```python
#3.1 Óbitos acumulados
df_obitos_acumulados = spark.sql("SELECT obitosAcumulado as Obitos_Acumulados FROM municipio order by 1 desc limit 1")
df_obitos_acumulados.show()
```

    +-----------------+
    |Obitos_Acumulados|
    +-----------------+
    |           526892|
    +-----------------+
    



```python
#3.2 Obitos novos
df_obitos_novos = spark.sql("SELECT obitosNovos as Obitos_Novos FROM municipio order by 1 desc limit 1")
df_obitos_novos.show()

#3.3 Letalidade
df_letalidade = spark.sql("SELECT cast(((obitosAcumulado * 100) / casosAcumulado) as decimal(5,1)) as Letalidade FROM municipio order by 1 desc limit 1")
df_letalidade.show()

#3.4 Mortalidade
df_mortalidade = spark.sql("SELECT cast(((obitosAcumulado * 100000) / populacaoTCU2019) as decimal(4,1)) as Mortalidade FROM municipio order by 1 desc limit 1")
df_mortalidade.show()
```

    +------------+
    |Obitos_Novos|
    +------------+
    |        4249|
    +------------+
    
    +----------+
    |Letalidade|
    +----------+
    |    1500.0|
    +----------+
    
    +-----------+
    |Mortalidade|
    +-----------+
    |      999.1|
    +-----------+
    


## Salvar a primeira visualização como tabela Hive


```python
df_casos_recuperados.write.format('csv').saveAsTable('Recuperados')
```


```python
df_em_acompanhamento.write.format('csv').saveAsTable('Acompanhamento')
```


```python
#Visualizar as tabelas salvas 
spark.sql('SHOW TABLES').show()
```

    +--------+--------------+-----------+
    |database|     tableName|isTemporary|
    +--------+--------------+-----------+
    | covidbr|acompanhamento|      false|
    | covidbr|     municipio|      false|
    | covidbr|   recuperados|      false|
    +--------+--------------+-----------+
    


## Salvar a segunda visualização com formato parquet e compressão snappy


```python
df_casos_acumulados.write.option('compression', 'snappy').parquet('hdfs://namenode/user/marco/projeto-final-spark/visualizacao/Casos_Acumulados')
```


```python
df_casos_novos.write.option('compression', 'snappy').parquet('hdfs://namenode/user/marco/projeto-final-spark/visualizacao/Casos_Novos')

## Ocorreu o erro pois já existia... 
```


    ---------------------------------------------------------------------------

    Py4JJavaError                             Traceback (most recent call last)

    /opt/spark/python/pyspark/sql/utils.py in deco(*a, **kw)
         62         try:
    ---> 63             return f(*a, **kw)
         64         except py4j.protocol.Py4JJavaError as e:


    /opt/spark/python/lib/py4j-0.10.7-src.zip/py4j/protocol.py in get_return_value(answer, gateway_client, target_id, name)
        327                     "An error occurred while calling {0}{1}{2}.\n".
    --> 328                     format(target_id, ".", name), value)
        329             else:


    Py4JJavaError: An error occurred while calling o104.parquet.
    : org.apache.spark.sql.AnalysisException: path hdfs://namenode/user/marco/projeto-final-spark/visualizacao/Casos_Novos already exists.;
    	at org.apache.spark.sql.execution.datasources.InsertIntoHadoopFsRelationCommand.run(InsertIntoHadoopFsRelationCommand.scala:114)
    	at org.apache.spark.sql.execution.command.DataWritingCommandExec.sideEffectResult$lzycompute(commands.scala:104)
    	at org.apache.spark.sql.execution.command.DataWritingCommandExec.sideEffectResult(commands.scala:102)
    	at org.apache.spark.sql.execution.command.DataWritingCommandExec.doExecute(commands.scala:122)
    	at org.apache.spark.sql.execution.SparkPlan$$anonfun$execute$1.apply(SparkPlan.scala:131)
    	at org.apache.spark.sql.execution.SparkPlan$$anonfun$execute$1.apply(SparkPlan.scala:127)
    	at org.apache.spark.sql.execution.SparkPlan$$anonfun$executeQuery$1.apply(SparkPlan.scala:155)
    	at org.apache.spark.rdd.RDDOperationScope$.withScope(RDDOperationScope.scala:151)
    	at org.apache.spark.sql.execution.SparkPlan.executeQuery(SparkPlan.scala:152)
    	at org.apache.spark.sql.execution.SparkPlan.execute(SparkPlan.scala:127)
    	at org.apache.spark.sql.execution.QueryExecution.toRdd$lzycompute(QueryExecution.scala:80)
    	at org.apache.spark.sql.execution.QueryExecution.toRdd(QueryExecution.scala:80)
    	at org.apache.spark.sql.DataFrameWriter$$anonfun$runCommand$1.apply(DataFrameWriter.scala:668)
    	at org.apache.spark.sql.DataFrameWriter$$anonfun$runCommand$1.apply(DataFrameWriter.scala:668)
    	at org.apache.spark.sql.execution.SQLExecution$$anonfun$withNewExecutionId$1.apply(SQLExecution.scala:78)
    	at org.apache.spark.sql.execution.SQLExecution$.withSQLConfPropagated(SQLExecution.scala:125)
    	at org.apache.spark.sql.execution.SQLExecution$.withNewExecutionId(SQLExecution.scala:73)
    	at org.apache.spark.sql.DataFrameWriter.runCommand(DataFrameWriter.scala:668)
    	at org.apache.spark.sql.DataFrameWriter.saveToV1Source(DataFrameWriter.scala:276)
    	at org.apache.spark.sql.DataFrameWriter.save(DataFrameWriter.scala:270)
    	at org.apache.spark.sql.DataFrameWriter.save(DataFrameWriter.scala:228)
    	at org.apache.spark.sql.DataFrameWriter.parquet(DataFrameWriter.scala:557)
    	at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    	at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:62)
    	at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
    	at java.lang.reflect.Method.invoke(Method.java:498)
    	at py4j.reflection.MethodInvoker.invoke(MethodInvoker.java:244)
    	at py4j.reflection.ReflectionEngine.invoke(ReflectionEngine.java:357)
    	at py4j.Gateway.invoke(Gateway.java:282)
    	at py4j.commands.AbstractCommand.invokeMethod(AbstractCommand.java:132)
    	at py4j.commands.CallCommand.execute(CallCommand.java:79)
    	at py4j.GatewayConnection.run(GatewayConnection.java:238)
    	at java.lang.Thread.run(Thread.java:748)


    
    During handling of the above exception, another exception occurred:


    AnalysisException                         Traceback (most recent call last)

    <ipython-input-27-6c5df3bea6ed> in <module>()
    ----> 1 df_casos_novos.write.option('compression', 'snappy').parquet('hdfs://namenode/user/marco/projeto-final-spark/visualizacao/Casos_Novos')
    

    /opt/spark/python/pyspark/sql/readwriter.py in parquet(self, path, mode, partitionBy, compression)
        839             self.partitionBy(partitionBy)
        840         self._set_opts(compression=compression)
    --> 841         self._jwrite.parquet(path)
        842 
        843     @since(1.6)


    /opt/spark/python/lib/py4j-0.10.7-src.zip/py4j/java_gateway.py in __call__(self, *args)
       1255         answer = self.gateway_client.send_command(command)
       1256         return_value = get_return_value(
    -> 1257             answer, self.gateway_client, self.target_id, self.name)
       1258 
       1259         for temp_arg in temp_args:


    /opt/spark/python/pyspark/sql/utils.py in deco(*a, **kw)
         67                                              e.java_exception.getStackTrace()))
         68             if s.startswith('org.apache.spark.sql.AnalysisException: '):
    ---> 69                 raise AnalysisException(s.split(': ', 1)[1], stackTrace)
         70             if s.startswith('org.apache.spark.sql.catalyst.analysis'):
         71                 raise AnalysisException(s.split(': ', 1)[1], stackTrace)


    AnalysisException: 'path hdfs://namenode/user/marco/projeto-final-spark/visualizacao/Casos_Novos already exists.;'



```python
df_incidencia.write.option('compression', 'snappy').parquet('hdfs://namenode/user/marco/projeto-final-spark/visualizacao/Incidencia')
```


```python
#Visualizar os dodos na pasta do HDFS
!hdfs dfs -ls 'hdfs://namenode/user/marco/projeto-final-spark/visualizacao'
```

    Found 2 items
    drwxr-xr-x   - root supergroup          0 2022-04-27 09:23 hdfs://namenode/user/marco/projeto-final-spark/visualizacao/Casos_Novos
    drwxr-xr-x   - root supergroup          0 2022-04-27 09:25 hdfs://namenode/user/marco/projeto-final-spark/visualizacao/Incidencia


## Salvar a terceira visualização em um tópico no Kafka
⚠ Diferente dos formatos nativos do spark para salvamento direto no HDFS,o Kafka permite apenas salvamento de dados únicos de tipo String em DataFrames de formato JSON. Por isso, iremos convertêlos antes de salvarmos em um tópico.


```python
#3.1 Óbitos acumulados
obitos_acumulados_json = df_obitos_acumulados.select(to_json(struct('obitos_Acumulados')).alias('value'))
obitos_acumulados_json.show(n=1, truncate=False, vertical=False)
```

    +----------------------------+
    |value                       |
    +----------------------------+
    |{"obitos_Acumulados":526892}|
    +----------------------------+
    



```python
#3.2 Obitos novos
obitos_novos_json = df_obitos_novos.select(to_json(struct('obitos_Novos')).alias('value'))
obitos_novos_json.show(n=1, truncate=False, vertical=False)
```

    +---------------------+
    |value                |
    +---------------------+
    |{"obitos_Novos":4249}|
    +---------------------+
    



```python
#3.3 Letalidade
letalidade_json = df_letalidade.select(to_json(struct('Letalidade')).alias('value'))
letalidade_json.show(n=1, truncate=False, vertical=False)
```

    +---------------------+
    |value                |
    +---------------------+
    |{"Letalidade":1500.0}|
    +---------------------+
    



```python
#3.4 Mortalidade
mortalidade_json = df_mortalidade.select(to_json(struct('Mortalidade')).alias('value'))
mortalidade_json.show(n=1, truncate=False, vertical=False)
```

    +---------------------+
    |value                |
    +---------------------+
    |{"Mortalidade":999.1}|
    +---------------------+
    


## Salvando os Dataframes convertidos em JSON em tópicos do Kafka


```python
df_obitos_acumulados.selectExpr('to_json(struct(*)) As value')\
.write.format('kafka')\
.option('kafka.bootstrap.servers', 'kafka:9092')\
.option('topic', 'topic-obtidos_acumulados')\
.save()
```


```python
df_obitos_novos.selectExpr('to_json(struct(*)) As value')\
.write\
.format("kafka")\
.option("kafka.bootstrap.servers","kafka:9092")\
.option("topic","topic-obitos_novos")\
.save()
```


```python
df_letalidade.selectExpr('to_json(struct(*)) As value')\
.write\
.format("kafka")\
.option("kafka.bootstrap.servers","kafka:9092")\
.option("topic","topic-letalidade")\
.save()
```


```python
df_mortalidade.selectExpr('to_json(struct(*)) As value')\
.write\
.format("kafka")\
.option("kafka.bootstrap.servers","kafka:9092")\
.option("topic","topic-mortalidade")\
.save()
```

# Criar a visualização pelo Spark com os dados enviados para o HDFS


```python
df_spark = spark.sql('''SELECT regiao as Regiao, 
                     MAX(casosAcumulado) as Casos, 
                     MAX(obitosAcumulado) as Obitos, 
                     MAX(data) as Atualizacao 
                     FROM municipio 
                     GROUP BY regiao 
                     ORDER BY regiao''')

df_spark.show()

df_spark.printSchema()


```

    +------------+--------+------+-----------+
    |      Regiao|   Casos|Obitos|Atualizacao|
    +------------+--------+------+-----------+
    |      Brasil|18855015|526892| 2021-07-06|
    |Centro-Oeste|  686433| 19485| 2021-07-06|
    |    Nordeste| 1141612| 24428| 2021-07-06|
    |       Norte|  557708| 15624| 2021-07-06|
    |     Sudeste| 3809222|130389| 2021-07-06|
    |         Sul| 1308643| 31867| 2021-07-06|
    +------------+--------+------+-----------+
    
    root
     |-- Regiao: string (nullable = true)
     |-- Casos: decimal(10,0) (nullable = true)
     |-- Obitos: integer (nullable = true)
     |-- Atualizacao: string (nullable = true)
    



```python
    df_spark.limit(10).toPandas()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Regiao</th>
      <th>Casos</th>
      <th>Obitos</th>
      <th>Atualizacao</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Brasil</td>
      <td>18855015</td>
      <td>526892</td>
      <td>2021-07-06</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Centro-Oeste</td>
      <td>686433</td>
      <td>19485</td>
      <td>2021-07-06</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Nordeste</td>
      <td>1141612</td>
      <td>24428</td>
      <td>2021-07-06</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Norte</td>
      <td>557708</td>
      <td>15624</td>
      <td>2021-07-06</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Sudeste</td>
      <td>3809222</td>
      <td>130389</td>
      <td>2021-07-06</td>
    </tr>
    <tr>
      <th>5</th>
      <td>Sul</td>
      <td>1308643</td>
      <td>31867</td>
      <td>2021-07-06</td>
    </tr>
  </tbody>
</table>
</div>



Fontes de consultas:
pyspark.sql module: https://spark.apache.org/docs/2.0.2/api/python/pyspark.sql.html#module-pyspark.sql.functions
Spark SQL, DataFrames and Datasets Guide: https://spark.apache.org/docs/2.0.2/sql-programming-guide.html#sql
Spark SQL Guide: https://spark.apache.org/docs/latest/sql-getting-started.html
Como obter no SQL o último registro inserido de acordo com sua data: https://pt.stackoverflow.com/questions/13125/como-obter-no-sql-o-%C3%BAltimo-registro-inserido-de-acordo-com-sua-data
Sobre os dados do Coronavirus: https://www.coronavirus.sc.gov.br/sobre-os-dados/
Projeção da população do Brasil: https://www.ibge.gov.br/apps/populacao/projecao/index.html
CAST para DECIMAL no MySQL: https://stackoverflow.com/questions/11830509/cast-to-decimal-in-mysql
Tutorial: Usar o fluxo estruturado do Apache Spark com o Apache Kafka no HDInsight: https://docs.microsoft.com/pt-br/azure/hdinsight/hdinsight-apache-kafka-spark-structured-streaming
