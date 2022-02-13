aws dynamodb create-table --table-name Hockey \
--attribute-definitions AttributeName=ScoreIndex,AttributeType=N \
--key-schema AttributeName=ScoreIndex,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=20,WriteCapacityUnits=20

sleep 10

aws dynamodb batch-write-item --request-items file://./hockey.json \
--return-consumed-capacity INDEXES \
--return-item-collection-metrics SIZE \
--return-consumed-capacity TOTAL



aws dynamodb create-table --table-name Baseball \
--attribute-definitions AttributeName=ScoreIndex,AttributeType=N \
--key-schema AttributeName=ScoreIndex,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=20,WriteCapacityUnits=20

sleep 10

aws dynamodb batch-write-item --request-items file://./baseball.json \
--return-consumed-capacity INDEXES \
--return-item-collection-metrics SIZE \
--return-consumed-capacity TOTAL

aws dynamodb create-table --table-name Soccer \
--attribute-definitions AttributeName=ScoreIndex,AttributeType=N \
--key-schema AttributeName=ScoreIndex,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=20,WriteCapacityUnits=20

sleep 10

aws dynamodb batch-write-item --request-items file://./soccer.json \
--return-consumed-capacity INDEXES \
--return-item-collection-metrics SIZE \
--return-consumed-capacity TOTAL