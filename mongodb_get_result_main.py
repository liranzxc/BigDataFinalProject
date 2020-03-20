from services.config_service import ConfigService
from services.mongodb_service import MongoDbService

config = ConfigService()

mongodb_service = MongoDbService(config)

records = mongodb_service.get_all_records(page=0, size=100000)

for record in records:
    print(record)
