import requests
import time

# Configurações
TOKEN = ""
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
BASE_URL = "https://api.github.com"

def fetch_rest(endpoint):
    url = f"{BASE_URL}{endpoint}"
    response = requests.get(url, headers=HEADERS)
    return response.json(), len(response.content)

def measure_queries():
    queries = {
        "simples": "/repositories?per_page=5",
        "complexa": "/repos/octocat/hello-world",
        "agregacao": "/search/repositories?q=stars:>100000&per_page=5"
    }
    results = {}
    
    for query_type, endpoint in queries.items():
        start_time = time.time()
        total_size = 0
        for _ in range(15):
            _, size = fetch_rest(endpoint)
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
