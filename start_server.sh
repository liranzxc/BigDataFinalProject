cd big-data-servers
pip install -r requirements-controller.txt
docker-compose -f docker-compose-producer.yml build
docker-compose -f docker-compose-consumer.yml build
python controller_server.py
