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
url_rest = "https://api.github.com/repos/octocat/hello-world"  # Exemplo de URL REST
query_graphql = """
{
  repository(owner: "octocat", name: "hello-world") {
    name
    description
    owner {
      login
    }
  }
}
"""

# Coleta de dados para múltiplas execuções
repeticoes = 15
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

# Exibe os resultados
print("Resultados REST:", resultados_rest)
print("Resultados GraphQL:", resultados_graphql)

# Cálculo da média e análise estatística
media_tempo_rest = sum([r[0] for r in resultados_rest]) / repeticoes
media_tamanho_rest = sum([r[1] for r in resultados_rest]) / repeticoes

media_tempo_graphql = sum([r[0] for r in resultados_graphql]) / repeticoes
media_tamanho_graphql = sum([r[1] for r in resultados_graphql]) / repeticoes

print(f"\nMédia Tempo REST: {media_tempo_rest:.2f} ms")
print(f"Média Tamanho REST: {media_tamanho_rest / 1024:.2f} KB")
print(f"Média Tempo GraphQL: {media_tempo_graphql:.2f} ms")
print(f"Média Tamanho GraphQL: {media_tamanho_graphql / 1024:.2f} KB")
