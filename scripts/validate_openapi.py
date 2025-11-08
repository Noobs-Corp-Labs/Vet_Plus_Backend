import subprocess
import time
import requests
import sys
from openapi_spec_validator import validate_spec
from openapi_spec_validator.exceptions import OpenAPISpecValidatorError

# Configurações
OPENAPI_URL = "http://localhost:8000/openapi.json"
APP_MODULE = "app.main:app"
MAX_RETRIES = 7
RETRY_DELAY = 2

def run_validation():
    print("Iniciando o servidor Uvicorn em background...")
    server_process = None
    try:
        server_process = subprocess.Popen(
            ["uvicorn", APP_MODULE, "--host", "0.0.0.0", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
    except FileNotFoundError:
        print("\n[ERRO]: O comando 'uvicorn' não foi encontrado.")
        print("Certifique-se de que seu ambiente virtual está ativado e que 'uvicorn[standard]' está instalado.")
        sys.exit(1)

    try:
        print(f"Aguardando o servidor em {OPENAPI_URL}...")
        spec_json = None
        for i in range(MAX_RETRIES):
            time.sleep(RETRY_DELAY)
            
            if server_process.poll() is not None:
                stdout, stderr = server_process.communicate()
                print("\n[ERRO] FATAL: Servidor Uvicorn falhou ao iniciar (Processo Terminado).")
                if stderr:
                    print("\n--- Saída de Erro do Uvicorn (Stderr) ---")
                    print(stderr.decode(errors='ignore')) 
                else:
                    print("Nenhuma saída de erro específica do servidor foi detectada. Verifique logs do Uvicorn.")
                sys.exit(1)

            try:
                response = requests.get(OPENAPI_URL, timeout=5)
                response.raise_for_status()
                spec_json = response.json()
                print("Esquema OpenAPI baixado com sucesso.")
                break
            except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError, requests.exceptions.Timeout) as e:
                if i == MAX_RETRIES - 1:
                    print(f"Tentativa {i+1}/{MAX_RETRIES} falhou: {e}")
                    raise ConnectionError(f"Servidor não ficou acessível após {MAX_RETRIES * RETRY_DELAY} segundos.")
                print(f"Tentativa {i+1}/{MAX_RETRIES}: Conexão recusada/Timeout. Tentando novamente...")
                pass

        if spec_json is None:
            print(f"\n[ERRO] FATAL: Falha ao baixar o esquema.")
            sys.exit(1)

        print("\nIniciando a validação do esquema...")
        validate_spec(spec_json)
        print("[SUCESSO] VALIDAÇÃO SUCEDIDA: O esquema OpenAPI é válido.")
        
    except OpenAPISpecValidatorError as e:
        print("\n[ERRO] DE VALIDAÇÃO: O esquema OpenAPI contém erros.")
        print("--- Detalhes do Erro ---")
        print(e)
        print("------------------------")
        sys.exit(1)

    except ConnectionError as e:
        print(f"\n[ERRO] FATAL: {e}")
        print("Verifique se seu app principal inicia corretamente e se a porta 8000 está livre.")
        sys.exit(1)

    except Exception as e:
        print(f"\n[ERRO] INESPERADO durante o processo: {e}")
        sys.exit(1)

    finally:
        if server_process and server_process.poll() is None:
            print("\nParando o servidor Uvicorn...")
            server_process.terminate()
            server_process.wait(timeout=5)
            print("Servidor parado.")
        elif server_process:
             print("\nServidor Uvicorn já estava parado (crashed/finished).")

if __name__ == "__main__":
    run_validation()