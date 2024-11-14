import requests
import time

# Token de autenticação
TOKEN = 'seu_token_github'

# Cabeçalhos para autenticação
HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

# Função para medir tempo e tamanho da resposta de uma consulta REST
def consulta_rest(url):
    inicio = time.time()
    resposta = requests.get(url, headers=HEADERS)
    fim = time.time()
    tamanho_resposta = len(resposta.content)
    tempo_resposta = (fim - inicio) * 1000  # em milissegundos
    return tempo_resposta, tamanho_resposta

# Função para medir tempo e tamanho da resposta de uma consulta GraphQL
def consulta_graphql(query):
    inicio = time.time()
    resposta = requests.post('https://api.github.com/graphql', headers=HEADERS, json={"query": query})
    fim = time.time()
    tamanho_resposta = len(resposta.content)
    tempo_resposta = (fim - inicio) * 1000  # em milissegundos
    return tempo_resposta, tamanho_resposta

# Definição das consultas
# 1. Simples
url_rest_simples = "https://api.github.com/repos/octocat/hello-world"  # REST simples
query_graphql_simples = """
{
  repository(owner: "octocat", name: "hello-world") {
    name
    description
  }
}
"""

# 2. Complexa
url_rest_complexa = "https://api.github.com/repos/octocat/hello-world/contributors"  # REST complexa
query_graphql_complexa = """
{
  repository(owner: "octocat", name: "hello-world") {
    name
    description
    collaborators(first: 10) {
      nodes {
        login
      }
    }
  }
}
"""

# 3. Agregação
url_rest_aggregacao = "https://api.github.com/repos/octocat/hello-world/issues?state=all"  # REST agregação
query_graphql_aggregacao = """
{
  repository(owner: "octocat", name: "hello-world") {
    issues {
      totalCount
    }
    stargazers {
      totalCount
    }
    forks {
      totalCount
    }
  }
}
"""

# Função para executar as medições
def realizar_testes(url_rest, query_graphql, repeticoes=15):
    resultados_rest = []
    resultados_graphql = []

    # Executa a consulta REST
    for _ in range(repeticoes):
        tempo, tamanho = consulta_rest(url_rest)
        resultados_rest.append((tempo, tamanho))

    # Executa a consulta GraphQL
    for _ in range(repeticoes):
        tempo, tamanho = consulta_graphql(query_graphql)
        resultados_graphql.append((tempo, tamanho))

    return resultados_rest, resultados_graphql

# Executando para cada tipo de consulta
resultados_simples_rest, resultados_simples_graphql = realizar_testes(url_rest_simples, query_graphql_simples)
resultados_complexa_rest, resultados_complexa_graphql = realizar_testes(url_rest_complexa, query_graphql_complexa)
resultados_aggregacao_rest, resultados_aggregacao_graphql = realizar_testes(url_rest_aggregacao, query_graphql_aggregacao)

# Função para calcular a média e exibir resultados
def calcular_media(resultados):
    media_tempo = sum([r[0] for r in resultados]) / len(resultados)
    media_tamanho = sum([r[1] for r in resultados]) / len(resultados)
    return media_tempo, media_tamanho

# Exibe resultados
print("Consulta Simples REST:", calcular_media(resultados_simples_rest))
print("Consulta Simples GraphQL:", calcular_media(resultados_simples_graphql))

print("Consulta Complexa REST:", calcular_media(resultados_complexa_rest))
print("Consulta Complexa GraphQL:", calcular_media(resultados_complexa_graphql))

print("Consulta Agregação REST:", calcular_media(resultados_aggregacao_rest))
print("Consulta Agregação GraphQL:", calcular_media(resultados_aggregacao_graphql))
