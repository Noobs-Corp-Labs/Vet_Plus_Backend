"""
Responsabilidade: Inicializar collections baseado nos models.
Descobre models automaticamente e cria collections/índices.
"""
from pydantic import BaseModel
import importlib
import inspect
import pkgutil
from app.database import mongo_database_con


async def create_indexes(db, collection_name: str, indexes: list):
    """
    Cria índices para uma collection.
    
    Args:
        db: Instância do banco de dados
        collection_name: Nome da collection
        indexes: Lista de configurações de índices
                 Ex: [{"keys": [("field", 1)], "unique": True}]
    """
    collection = db[collection_name]
    
    for index_config in indexes:
        try:
            keys = index_config.get("keys")
            options = {k: v for k, v in index_config.items() if k != "keys"}
            
            await collection.create_index(keys, **options)
            
            # Formata a exibição dos índices
            keys_str = ", ".join([f"{k}: {v}" for k, v in keys])
            unique_str = " (unique)" if options.get("unique") else ""
            print(f"  📇 Índice criado: {{{keys_str}}}{unique_str}")
            
        except Exception as e:
            # Ignora erro se índice já existir
            if "already exists" not in str(e).lower():
                print(f"  ⚠️  Erro ao criar índice: {e}")


async def init_collections(run_command: bool = True):
    """
    Cria collections automaticamente com base nos models.
    
    Processo:
    1. Descobre todos os models Pydantic em app/models
    2. Cria a collection se não existir
    3. Aplica validação JSON Schema (se possível)
    4. Cria índices definidos no Config
    """
    print("🔄 Iniciando setup das collections MongoDB...")
    if (run_command):
        from app import models
    
        existing_collections = await mongo_database_con.list_collection_names()
        
        collections_created = 0
        collections_skipped = 0
        
        # Itera sobre todos os módulos em app/models
        for _, module_name, _ in pkgutil.iter_modules(models.__path__):
            try:
                # Importa o módulo
                module = importlib.import_module(f"app.models.{module_name}")
                
                # Procura por classes Pydantic no módulo
                for _, obj in inspect.getmembers(module):
                    # Verifica se é uma classe Pydantic (mas não a BaseModel)
                    if (inspect.isclass(obj) and 
                        issubclass(obj, BaseModel) and 
                        obj is not BaseModel and
                        hasattr(obj, 'Config')):
                        
                        # Pega o nome da collection do Config
                        if not hasattr(obj.Config, "collection"):
                            print(f"⚠️  Model {obj.__name__} não tem 'collection' definido no Config")
                            continue
                        
                        collection_name = obj.Config.collection
                        
                        # Cria a collection se não existir
                        if collection_name not in existing_collections:
                            print(f"🧱 Criando collection '{collection_name}'...")
                            await mongo_database_con.create_collection(collection_name)
                            collections_created += 1
                            
                            # Tenta aplicar validação JSON Schema
                            try:
                                schema = obj.schema()
                                # Remove campos que o MongoDB não aceita no validator
                                schema.pop('title', None)
                                schema.pop('description', None)
                                
                                await mongo_database_con.command({
                                    "collMod": collection_name,
                                    "validator": {"$jsonSchema": schema},
                                    "validationLevel": "moderate",
                                })
                                print(f"  ✅ Validação JSON Schema aplicada")
                            except Exception as e:
                                print(f"  ⚠️  Validação não aplicada: {e}")
                            
                            # Cria índices se definidos
                            if hasattr(obj.Config, 'indexes'):
                                await create_indexes(mongo_database_con, collection_name, obj.Config.indexes)
                        else:
                            print(f"ℹ️  Collection '{collection_name}' já existe")
                            collections_skipped += 1
                            
                            # Garante que os índices existam mesmo se a collection já existir
                            if hasattr(obj.Config, 'indexes'):
                                await create_indexes(mongo_database_con, collection_name, obj.Config.indexes)
                            
            except Exception as e:
                print(f"❌ Erro ao processar módulo '{module_name}': {e}")
        
        print(f"\n✅ Setup concluído!")
        print(f"   📦 {collections_created} collection(s) criada(s)")
        print(f"   ℹ️  {collections_skipped} collection(s) já existia(m)\n")
    else:
        print("ℹ️  Automatic Collection Update está desligado...")
        print("✅ Setup concluído!")