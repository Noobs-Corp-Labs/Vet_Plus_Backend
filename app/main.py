from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database.database_init import init_collections
from app.api import api_router
from app.middleware import add_middlewares
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gerencia o ciclo de vida da aplicação.
    """
    # Startup
    print("🚀 Iniciando aplicação...")
    await init_collections(False)
    
    yield

app = FastAPI(
    title="Vet Plus Backend",
    description="""
API do **Vet Plus**, sistema para gestão, análise de saúde e produção de rebanhos leiteiros.
""",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)
add_middlewares(app)

app.include_router(api_router)

@app.get('/', include_in_schema=False)
def root():
    return {'message': 'Enhanced FastAPI App'}

# Anotations:
# Description documentation (Swagger)
# ### 🐄 Funcionalidades principais
# - Cadastro e gerenciamento de usuários
# - Registro de animais e histórico de saúde
# - Análises preditivas sobre produção de leite
# - Controle nutricional, reprodutivo e sanitário
# ### 🔐 Autenticação
# - Login com JWT
# - Permissões por tipo de usuário (admin e padrão)
# terms_of_service="https://vetplus.com/termos",
# contact={
#     "name": "Equipe Vet Plus",
#     "url": "https://vetplus.com/suporte",
#     "email": "suporte@vetplus.com",
# },
# license_info={
#     "name": "MIT License",
#     "url": "https://opensource.org/licenses/MIT",
# },
