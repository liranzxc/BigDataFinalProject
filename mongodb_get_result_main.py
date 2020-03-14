from services.config_service import ConfigService
from services.mongodb_service import MongoDbService

configService = ConfigService()
config = configService.getConfig()

mongodb_service = MongoDbService(config)

records = mongodb_service.get_all_records()

for record in records:
    print(record)