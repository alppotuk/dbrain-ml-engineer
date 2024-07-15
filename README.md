# Digital Brain Technologies ML Engineering Tasks

## Task 1

I utilized an environment that includes Zookeeper with Kafka. Here are the command line arguments I used to complete Task 1:

```bash
docker-compose up -d zookeeper kafka
docker-compose exec kafka /bin/sh
```

```bash
kafka-topics.sh --create --bootstrap-server kafka:9092 --topic ml-engineer --replication-factor 1 --partitions 1
kafka-console-producer.sh --bootstrap-server kafka:9092 --topic ml-engineer
kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic ml-engineer --from-beginning
```

## Task 2

For Task 2, I chose Python as my preferred programming language since I have used it to develop web scraping and REST API applications before. For web scraping, I utilized BeautifulSoup4, and for the REST API, I used Flask. I have also included Swagger UI since I am used to to using Swagger. Swagger UI is available at http://localhost:5000/apidocs. You can run the Docker containers simply with these commands:

```bash
docker-compose build --no-cache
docker-compose up
```

## Task 3

The repository you are currently viewing contains Task 3. I would like to mention that normally I use git to commit my changes after completing each task. However, since uploading to GitHub is a separate task, I performed it as the final step.
