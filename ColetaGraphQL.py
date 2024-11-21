import requests
import time

# Configurações
TOKEN = ""
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}
GRAPHQL_URL = "https://api.github.com/graphql"

# Consultas GraphQL
QUERIES = {
    "simples": """
        query {
            search(query: "stars:>100000", type: REPOSITORY, first: 5) {
                edges {
                    node {
                        name
                        owner {
                            login
                        }
                    }
                }
            }
        }
    """,
    "complexa": """
        query {
            repository(owner: "octocat", name: "hello-world") {
                name
                description
                stargazerCount
                forks {
                    totalCount
                }
                issues(first: 5) {
                    edges {
                        node {
                            title
                        }
                    }
                }
            }
        }
    """,
    "agregacao": """
        query {
            search(query: "stars:>100000", type: REPOSITORY, first: 5) {
                repositoryCount
                edges {
                    node {
                        name
                        stargazerCount
                    }
                }
            }
        }
    """
}

def fetch_graphql(query):
    response = requests.post(GRAPHQL_URL, headers=HEADERS, json={"query": query})
    return response.json(), len(response.content)

def measure_queries():
    results = {}
    
    for query_type, query in QUERIES.items():
        start_time = time.time()
        total_size = 0
        for _ in range(15):
            _, size = fetch_graphql(query)
            total_size += size
        end_time = time.time()
        
        results[query_type] = {
            "tempo_total": end_time - start_time,
            "tamanho_total_respostas": total_size
        }
    
    return results

if __name__ == "__main__":
    results = measure_queries()
    for query_type, metrics in results.items():
        print(f"{query_type.upper()}:")
        print(f"  Tempo total: {metrics['tempo_total']:.2f} segundos")
        print(f"  Tamanho total das respostas: {metrics['tamanho_total_respostas']} bytes")
