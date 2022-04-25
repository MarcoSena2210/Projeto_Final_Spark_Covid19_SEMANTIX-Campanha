Projeto Final Spark - proj_covid19_spark

Objetivo: Efetuar o levantamento de covid no ano no brasil 


O Problema: Efetuar o levantamento do covid com os dados em planilha execel e gerar uma POC para o cliente

O que?  Gerar demonstrativo com 
Painel 1: 
	Casos Recuperados  NN.NNN.NNN
	Em acompanhamentos NN.NNN.NNN
	
  Confirmados
	  Acumulado 	NN.NNN.NNN
	  Casos novos   NN.NNN.NNN
	  Incidência    NN.NNN.NNN
	  
  Óbitos Confirmados
	  Acumulado 	NN.NNN.NNN
	  Casos novos   NN.NNN.NNN
	  % Letalidade  NN,N %
	  Mortalidade   NNN.N
	  
	 
	 

regiao	estado	municipio	Coduf	codmun	codRegiaoSaude	nomeRegiaoSaude	data	semanaEpi	populacaoTCU2019	casosAcumulado	casosNovos	obitosAcumulado	obitosNovos	Recuperadosnovos	emAcompanhamentoNovos	interior/metropolitana

	 
Quando?

Como?
1. Enviar os dados para o hdfs
Solução: 
Como..

Entrar no site no endereço abaixo e baixar os dados a serem trabalhados no windows. (Poderia ser baixado diretamente no linux).
Prefiri dessa forma pois posso descompactar e abrir o arquivo neste ambiente.

Nível Básico:
Dados: https://mobileapps.saude.gov.br/esus-vepi/files/unAFkcaNDeXajurGB7LChj8SgQYS2ptm/04bd3419b22b9cc5c6efac2c6528100d_HIST_PAINEL_COVIDBR_06jul2021.rar
1-Entender os dados

3-Acessar o namenode 
Como já temos um ambiente linux instalado em um container docker no windows, vamos chamar o powershell (como administrador) e  
entrar no namenode. 
docker exec -it namenode bash


2-Criar uma pasta como nome do projeto "projeto_covid" onde serão armazenado os dados brutos desse projeto
marco@DESKTOP-G2455QH:~$ mkdir -p  projeto_covid/data/

3-Copiar os dados brutos do windows para o local em que foi criada a pasta no linux.

Dica: no menu iniciar windows digitar->  \\wsl$  clicar em --> abrir --><distribuição do seu linux>-->home\<seu usuario no linux> --> projeto_covid--data   
no windows(D:\ENGENHARIA_DADOS\Semantix\Projeto_final)
Irá abrir a o local acima no ambeinte linux.Agora ctrl +c  para copiar os arqivos e ctrl+v para colar do ambiente windows para o linux.



3.1-Criar uma pasta /user/aluno/marcosena/data/projcovid no namenode
root@namenode:/# hdfs dfs -mkdir -p /user/aluno/marcosena/data/projcovid

Verificar a /user/aluno/marcosena/data/projcovid e copiar os arquivos que iremos trabalhar

root@namenode:/# hdfs dfs -ls -R  /user/aluno/marcosena/data/projcovid
root@namenode:/#

Desafio:
Como copiamos os arquivos brutos para pasta "~/projeto_covid/data" oa tentar copiar para o hadoop não conseguiamos concluir a operação.

Solução:

1) Copiamos os arquivos para  ~/treinamentos/spark/input/covid  pois a pasta "input" está visível dentro do hadoop, acredito que deve está configurado .yml

marco@DESKTOP-G2455QH:~/treinamentos/spark/input$ docker exec -it namenode l
s /input/covid/
HIST_PAINEL_COVIDBR_2020_Parte1_06jul2021.csv
HIST_PAINEL_COVIDBR_2020_Parte2_06jul2021.csv
HIST_PAINEL_COVIDBR_2021_Parte1_06jul2021.csv
HIST_PAINEL_COVIDBR_2021_Parte2_06jul2021.csv
marco@DESKTOP-G2455QH:~/treinamentos/spark/input$



2) Acessar o namenode e verificarmos o que já temos nesta pasta.

2.1)marco@DESKTOP-G2455QH:~/treinamentos/spark/input$ docker exec -it namenode bash

2.2)root@namenode:/# hdfs dfs -ls /user/marco/data/
Found 19 items
-rw-r--r--   3 root supergroup         46 2022-04-05 17:10 /user/marco/data/README.md
-rw-r--r--   3 root supergroup       2089 2022-04-05 17:10 /user/marco/data/WordCount.java
drwxr-xr-x   - root supergroup          0 2022-04-05 17:10 /user/marco/data/beneficio
drwxr-xr-x   - root supergroup          0 2022-04-05 17:11 /user/marco/data/db-sql
drwxr-xr-x   - root supergroup          0 2022-04-05 17:11 /user/marco/data/economicFitness
drwxr-xr-x   - root supergroup          0 2022-04-05 17:11 /user/marco/data/empreendimento
-rw-r--r--   3 root supergroup         54 2022-04-05 17:11 /user/marco/data/entrada1.txt
-rw-r--r--   3 root supergroup         42 2022-04-05 17:11 /user/marco/data/entrada2.txt
drwxr-xr-x   - root supergroup          0 2022-04-05 17:11 /user/marco/data/escola
drwxr-xr-x   - root supergroup          0 2022-04-05 17:11 /user/marco/data/hnpStats
drwxr-xr-x   - root supergroup          0 2022-04-05 17:11 /user/marco/data/iris
drwxr-xr-x   - root supergroup          0 2022-04-05 17:11 /user/marco/data/juros_selic
-rw-r--r--   3 root supergroup        161 2022-04-05 17:11 /user/marco/data/map.py
drwxr-xr-x   - root supergroup          0 2022-04-05 17:11 /user/marco/data/names
drwxr-xr-x   - root supergroup          0 2022-04-05 17:12 /user/marco/data/namesbystate
drwxr-xr-x   - root supergroup          0 2022-04-05 17:12 /user/marco/data/ouvidoria
drwxr-xr-x   - root supergroup          0 2022-04-05 17:12 /user/marco/data/populacaoLA
drwxr-xr-x   - root supergroup          0 2022-04-14 19:45 /user/marco/data/projeto_python
-rw-r--r--   3 root supergroup        511 2022-04-05 17:12 /user/marco/data/reduce.py
root@namenode:/#

3) Vamos criar uma pasta em /data/ chamada covid e copiarmos nos arquivos Brutos

3.1)root@namenode:/# hdfs dfs -mkdir /user/marco/data/covid
3.2)root@namenode:/# hdfs dfs -ls /user/marco/data/covid
3.3)root@namenode:/# hdfs dfs -put /input/covid/*  /user/marco/data/covid/

3.4)root@namenode:/# hdfs dfs -ls /user/marco/data/covid/
Found 4 items
-rw-r--r--   3 root supergroup   62492959 2022-04-23 19:24 /user/marco/data/covid/HIST_PAINEL_COVIDBR_2020_Parte1_06jul2021.csv
-rw-r--r--   3 root supergroup   76520681 2022-04-23 19:24 /user/marco/data/covid/HIST_PAINEL_COVIDBR_2020_Parte2_06jul2021.csv
-rw-r--r--   3 root supergroup   91120916 2022-04-23 19:24 /user/marco/data/covid/HIST_PAINEL_COVIDBR_2021_Parte1_06jul2021.csv
-rw-r--r--   3 root supergroup    3046774 2022-04-23 19:24 /user/marco/data/covid/HIST_PAINEL_COVIDBR_2021_Parte2_06jul2021.csv
root@namenode:/#





) Fazer a lmpeza das linhas indesejadas.








XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
PArte antiga:
1) copiamos os arquivos para  ~/treinamentos/docker-bigdata/input/covid-data  pois a pasta "input" está visível dentro do hadoop, acredito que deve está configurado .yml
root@namenode:/# ls /input/covid-data/
HIST_PAINEL_COVIDBR_2020_Parte1_06jul2021.csv
HIST_PAINEL_COVIDBR_2020_Parte2_06jul2021.csv
HIST_PAINEL_COVIDBR_2021_Parte1_06jul2021.csv
HIST_PAINEL_COVIDBR_2021_Parte2_06jul2021.csv

2) precisamos copiar para o destino abaixo. /user/aluno/marcosena/data/projcovid
root@namenode:/# hdfs dfs -ls /user/aluno/marcosena/data/projcovid

origem --> detino       
hdfs dfs -put /input/covid-data/ /user/aluno/marcosena/data/projcovid

Listando hdfs
root@namenode:/# hdfs dfs -ls /user/aluno/marcosena/data/projcovid/covid-data
Found 4 items
-rw-r--r--   3 root supergroup   62492959 2022-04-20 00:50 /user/aluno/marcosena/data/projcovid/covid-data/HIST_PAINEL_COVIDBR_2020_Parte1_06jul2021.csv
-rw-r--r--   3 root supergroup   76520681 2022-04-20 00:50 /user/aluno/marcosena/data/projcovid/covid-data/HIST_PAINEL_COVIDBR_2020_Parte2_06jul2021.csv
-rw-r--r--   3 root supergroup   91120916 2022-04-20 00:51 /user/aluno/marcosena/data/projcovid/covid-data/HIST_PAINEL_COVIDBR_2021_Parte1_06jul2021.csv
-rw-r--r--   3 root supergroup    3046774 2022-04-20 00:51 /user/aluno/marcosena/data/projcovid/covid-data/HIST_PAINEL_COVIDBR_2021_Parte2_06jul2021.csv
root@namenode:/#


x2. Otimizar todos os dados do hdfs para uma tabela Hive particionada por município.


x3. Criar as 3 vizualizações pelo Spark com os dados enviados para o HDFS:

x4. Salvar a primeira visualização como tabela Hive

x5. Salvar a segunda visualização com formato parquet e compressão snappy

x6. Salvar a terceira visualização em um tópico no Kafka

x7. Criar a visualização pelo Spark com os dados enviados para o HDFS:

x8. Salvar a visualização do exercício 6 em um tópico no Elastic

x9. Criar um dashboard no Elastic para visualização dos novos dados enviados


regiao STRING,estado STRING,municipio STRING,coduf INT,codmun INT,codRegiaoSaude INT,nomeRegiaoSaude  STRING,data  STRING,semanaEpi INT,populacaoTCU2019 INT,casosAcumulado  INT,casosNovos INT,obitosAcumulado INT,obitosNovos INT,recuperadosnovos INT,emAcompanhamentoNovos INT,interior/metropolitana INT

='Brasil;a;b;76;c;d;;2021-01-01;53;210147125;7700578;24605;195411;462;6756284;748883;'),



regiao STRING,estado STRING,municipio STRING,coduf INT,codmun INT,codRegiaoSaude INT,nomeRegiaoSaude  STRING,data  STRING,semanaEpi INT,populacaoTCU2019 INT,

casosAcumulado  INT,
casosNovos INT,

obitosAcumulado INT,
obitosNovos INT,

recuperadosnovos INT,
emAcompanhamentoNovos INT,


interior/metropolitana INT