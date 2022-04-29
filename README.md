<img align="center" src="https://semantix.com.br/wp-content/uploads/2021/03/smtx-logo-white.png" alt="Logo Semantix Inc." style="zoom:100%;" />

# Projeto Final Spark: Big Data Enginner

<p align="center">
    <img src="http://img.shields.io/static/v1?label=STATUS&message=EM%20DESENVOLVIMENTO&color=RED&style=for-the-badge"/>
    <img src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white"/>
    <img src="https://img.shields.io/badge/Hadoop-FFFFFF?style=for-the-badge&logo=hadoop&logoColor=#E35A16"/>
    <img src="https://img.shields.io/badge/Apache_Spark-FFFFFF?style=for-the-badge&logo=apachespark&logoColor=#E35A16"/>
	<img src="https://img.shields.io/badge/Elastic_Search-005571?style=for-the-badge&logo=elasticsearch&logoColor=white"/>
</p>

- Nome: Marco Antonio de Sena Campos
- Instituição: Semantix Academy
- Turma: Big Data Engineer 04-22
- Professor: Rodrigo Rebouças

#AcademySemantix

- [Treinamento](https://github.com/MarcoSena2210/BigDataSemantix)

## Tópicos 


- [Pré-requisitos](https://github.com/MarcoSena2210/Projeto_Final_Spark_Covid19_SEMANTIX-Campanha#pr%C3%A9-requisitos)
- [Descrição do projeto](https://github.com/MarcoSena2210/Projeto_Final_Spark_Covid19_SEMANTIX-Campanha#descri%C3%A7%C3%A3o-do-projeto)
- [Configurando o Docker em sua máquina]()
- [Preparando o ambiente](https://github.com/MarcoSena2210/Projeto_Final_Spark_Covid19_SEMANTIX-Campanha#preparando-o-ambiente)
- [Nível básico](https://github.com/MarcoSena2210/Projeto_Final_Spark_Covid19_SEMANTIX-Campanha#n%C3%ADvel-b%C3%A1sico)
  - [Objetivos](https://github.com/MarcoSena2210/Projeto_Final_Spark_Covid19_SEMANTIX-Campanha#objetivos)
  - [Projeto Final Spark - Nivel básico](https://github.com/MarcoSena2210/Projeto_Final_Spark_Covid19_SEMANTIX-Campanha#-projeto-final--spark---nivel-b%C3%A1sico)
  
- [Nível avançado](https://github.com/MarcoSena2210/Projeto_Final_Spark_Covid19_SEMANTIX-Campanha#n%C3%ADvel-avan%C3%A7ado)
  - [Objetivo](https://github.com/MarcoSena2210/Projeto_Final_Spark_Covid19_SEMANTIX-Campanha#objetivo)
  - [Passo a passo](https://github.com/MarcoSena2210/Projeto_Final_Spark_Covid19_SEMANTIX-Campanha#-passo-a-passo-1)

------

## Pré-requisitos

Para melhor compreensão e execução do projeto é necessário conhecimentos básicos (fundamentos) em: Linux, Big Data, Docker, Python, Kafka, Elastic e Spark. 

------

## Descrição do projeto

Esse projeto tem como objetivo desenvolver os conhecimentos adquiridos durante o treinamento de [Big Data Enginner](https://github.com/MarcoSena2210/big-data-engineer-sematix) promovido pela Semantix Inc no primeiro semestre de 2022. 


O projeto é dividido em duas partes (básico e avançado) sobre o tema Campanha Nacional de Vacinação contra Covid-19.Nesse momento iremos fazer o projeto básico.

⚠ **Observação: Todas as imagens de exemplo abaixo (Visualizações) são apenas para referencias, o projeto irá ter valores diferentes e as formas de se criar tabelas com dataframe/dataset das visualizações, pode ser realizado da maneira que preferir.**

------
## Configurando o Docker em sua máquina:

A fim de facilitar o desenvolvimento das etapas do projeto, abaixo segue um passo a passo de preparação de ambiente.

### Download Docker e Docker Compose:

### Download Docker - Windows

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Instalação Docker - Windows

1. Verificar se o Windows está atualizado. Caso seja inferiro a 18362, clique no link ao lado para atualizar o Windows 10. [Atualizar o Windows](https://www.microsoft.com/pt-br/software-download/windows10);
2. Pesquise por Ativar ou desativar recursos do Windows e siga os passos abaixo:
    - Desativar Hyper-V;
    - Desativar Plataforma do Hipervisor do Windows;
    - Habilitar a Plataforma de Máquina Virtual;
    - Habilitar o Subsistema do Windows para Linux (WSL).
3. Faça o Download do WSL 2 clicando no link ao lado: [Download WSL 2](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi);
4. Acesse a Microsoft Store, e faça download e instale a distribuição Linux Ubuntu 20.04 LTS (recomendado);
5. Instale o Docker Desktop no Windows: [Docker Desktop](https://hub.docker.com/editions/community/docker-ce-desktop-windows);
    - Obs: Abra o Docker Desktop e verifique se estão habilitados o "Enable integration with my default WSL distro" e "Ubuntu-20.04" em Settings->Resource->WSL Integration.

### Instalação Docker - Linux

- [Link para instalação do Docker Engine](https://docs.docker.com/engine/install/)
- [Link para instalação do Docker Compose](https://docs.docker.com/compose/install/)

### Instalação Docker - Mac
- [Link para instalação do Docker Desktop no Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac/)

----------

## Preparando o ambiente:

1. Abra o terminal do WSL2 e crie um diretório para o projeto no `~$/home/<seu-nome>` com o comando: `mkdir projeto-final-spark`
2. Acesse o diretório `cd projeto-final-spark`
3. No diretório projeto-final-spark, clone o cluster disponibilizado no treinamento: `git clone https://github.com/rodrigo-reboucas/docker-bigdata.git spark`
4. Confirme se o arquivo foi baixado com o comando de listar: `ls`
5. Entra na pasta spark `cd spark`
6. Configure o vm.max_map_count para 262144:
    1. Digite o comando `sudo nano /etc/sysctl.conf`
    2. Vá até o final do arquivo e incluia o parâmetro `vm.max_map_count=262144` 
    3. CTRL+O para salvar e CTRL+X para sair
    4. Verifique se funcionou utilizando o comando `grep vm.max_map_count /etc/sysctl.conf` no terminal.
Obs.: Sempre que iniciar o cluster, deve-se utilizar o comando `sudo sysctl -w vm.max_map_count=262144` para que os containers sejam ativos.
7. baixe as imagens com o comando `docker-compose -f docker-compose-parcial.yml pull`
8. Verifique se as imagens foram baixadas através do comando de listar `docker image ls`
9. Inicie todos os serviços com o comando: `docker-compose -f docker-compose-parcial.yml up -d`
Obs.: Cuidado para não iniciar o cluster completo (docker-compose-completo.yml), pois dependendo das congifurações da sua máquina, ficará pesado para executar.
10. Por fim, será necessário configurar que as tabelas Hive aceitem o formato parquet. 
    1. Faça downlod do arquivo .jar com o comando `curl -O https://repo1.maven.org/maven2/com/twitter/parquet-hadoop-bundle/1.6.0/parquet-hadoop-bundle-1.6.0.jar`
    2. Copie o arquivo para o diretório `/opt/spark/jars` com o comando `docker cp parquet-hadoop-bundle-1.6.0.jar jupyter-spark:/opt/spark/jars`

Agora sua máquina está configurada e seus arquivos estão prontos para serem utilizados no HDFS.
Continue os próximos passos pelo Jupyter-Notebook acessando pelo navegador a porta `http://localhost:8889/`. 
Depois crie um arquivo de tipo PySpark chamado projeto_final_spark_nivel_basico. Neste arquivo continuaremos com os próximos passos utilizando PySpark.

----------

## Nível básico

- Dados: https://mobileapps.saude.gov.br/esus-vepi/files/unAFkcaNDeXajurGB7LChj8SgQYS2ptm/04bd3419b22b9cc5c6efac2c6528100d_HIST_PAINEL_COVIDBR_06jul2021.rar
- Referência das Visualizações:
  - Site: https://covid.saude.gov.br/
  - Guia do Site: **Painel Geral**

### Objetivos

- ✅Enviar os dados para o HDFS
- ✅Otimizar todos os dados do HDFS para uma tabela Hive particionada por município
- ✅Criar as 3 visualizações pelo Spark com os dados enviados para o HDFS 
- ✅Salvar a primeira visualização como tabela Hive
- ✅Salvar a segunda visualização com formato parquet e compressão snappy
- ✅Salvar a terceira visualização em um tópico no Kafka
- ✅Criar a visualização pelo Spark com os dados enviados para o HDFS
- Salvar a visualização do exercício 6 em um tópico no Elastic
- Criar um dashboard no Elastic para visualização dos novos dados enviados

### ▶ [Projeto Final  Spark - Nivel básico](https://github.com/MarcoSena2210/Projeto_Final_Spark_Covid19_SEMANTIX-Campanha/blob/main/projeto_final_spark_nivel_basico.ipynb)


## Comandos básicos Docker

### Inicar os serviços
         docker-compose up -d        

### Verificar imagens
          docker image ls

### Verificar containers
          docker container ls

## SOLUCIONANDO PROBLEMAS 

### Parar um containers
         docker stop [nome do container]      

### Parar todos containers
         docker stop $(docker ps -a -q)
  
### Remover um container
         docker rm [nome do container]

### Remover todos containers
         docker rm $(docker ps -a -q)         

### Dados do containers
         docker container inspect [nome do container]

### Iniciar um container
         docker-compose up -d [nome do container]

### Iniciar todos os containers
         docker-compose up -d 

### Acessar log do container
         docker container logs [nome do container] 


## Acesso por shell

   ##### HDFS

          docker exec -it datanode bash

   ##### HBase

          docker exec -it hbase-master bash

   ##### Sqoop

          docker exec -it datanode bash
        
   ##### Kafka

          docker exec -it kafka bash

## Acesso JDBC

   ##### MySQL
          jdbc:mysql://database/employees

   ##### Hive

          jdbc:hive2://hive-server:10000/default

   ##### Presto

          jdbc:presto://presto:8080/hive/default

## Usuários e senhas

   ##### Hue
    Usuário: admin
    Senha: admin

   ##### Metabase
    Usuário: bigdata@class.com
    Senha: bigdata123 

   ##### MySQL
    Usuário: root
    Senha: secret
   
   ##### MongoDB
    Usuário: root
    Senha: root
    Authentication Database: admin

## Imagens   

[Docker Hub](https://hub.docker.com/u/fjardim)

## Acesso WebUI dos Frameworks
 
* HDFS *http://localhost:50070*
* Presto *http://localhost:8080*
* Hbase *http://localhost:16010/master-status*
* Mongo Express *http://localhost:8081*
* Kafka Manager *http://localhost:9000*
* Metabase *http://localhost:3000*
* Nifi *http://localhost:9090*
* Jupyter Spark *http://localhost:8889*
* Hue *http://localhost:8888*
* Spark *http://localhost:4040*


## Documentação Oficial

* https://zookeeper.apache.org/
* https://kafka.apache.org/
* https://nifi.apache.org/
* https://prestodb.io/
* https://spark.apache.org/
* https://www.mongodb.com/
* https://www.metabase.com/
* https://jupyter.org/
* https://hbase.apache.org/
* https://sqoop.apache.org/
* https://hadoop.apache.org/
* https://hive.apache.org/
* https://gethue.com/
* https://github.com/yahoo/CMAK
* https://www.docker.com/

Este repositório é um fork do [fabiogjardim](https://github.com/fabiogjardim/bigdata_docker) e 
[ciceroherique]https://github.com/cicerooficial/projeto-final-big-data-enginner-sematix)
