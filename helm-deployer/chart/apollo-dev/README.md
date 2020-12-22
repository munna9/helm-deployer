
Apollo server providing access to energy data

## Installation

To run the app, run this from the root:
```
brew install yarn
brew install node # "version 13.6.0"

yarn global add nodemon

yarn install --network-timeout 1000000000;  
yarn start
```

or use docker:
```
docker-compose up -d --build
```
## Development

Transpile typescript to javascript and watch file changes. Open a seperate terminal for each command below.
```
yarn start:watch
yarn start
```

## Deployment

Development GQL apollo server is running on lonnies EC2 in this folder: /home/sean/code/apolloserver. pull latest changes from github into this repo, then run ```docker-compose up -d --build```
If you are updating the apollo schema, update Hasura (see below)

Production - push to pipeline branch on Github then hit 'Build Now' in Jenkins: https://jenkins.prod.ep.shell.com/
ENV variables should be updated in the configmap in kubernetes.

## Playground
open http://localhost:4000 or whatever the server is running in your browser

## Security
Graphql authorizes access via an authorization token send in the header of the request. To set the authorization token for requests made in the Apollo Playground, click on the HTTP HEADERS tab at the bottom of the playground and add: 
```  
{
    "authorization": "token_goes_here"
}
  ```
 ## Monitoring / Logging
 https://engine.apollographql.com

## Hasura
Hasura provides CRUD GQL queries for every table in our Postgres DB.  

In addition, Hasura stitches every query from the Apollo graphql server. 
# Every time the Postgres DB is updated, you need to manually reload the DB in Hasura:
Go to the the Hasura console on port 4001, click on Remote Schemas, select apollserver, and hit reload.  
Hasura is located on "Lonnie's" EC2, port 4001:
It's config (only file) is here: /home/sean/code/hasura/docker-compose.yaml

## Typeorm Migrations

Generate migration file from entities
-n optopy is the name of migration
```
./node_modules/.bin/ts-node ./node_modules/typeorm/cli.js migration:generate -n <enter_descriptive_name> -f src/db/config/typeorm_migration.ts --connection <name_of_typeorm_connection(dbname)>
```

Migrate Up
```
./node_modules/.bin/ts-node ./node_modules/typeorm/cli.js migration:run -f src/db/config/typeorm_migration.ts --connection <name_of_typeorm_connection(dbname)>
```
or
```
./migrate_up.sh <name_of_typeorm_connection(dbname)>
```


Migrate Down
```
./node_modules/.bin/ts-node ./node_modules/typeorm/cli.js migration:revert -f src/db/config/typeorm_migration.ts --connection <name_of_typeorm_connection(dbname)>
```
or
```
./migrate_down.sh <name_of_typeorm_connection(dbname)>
```

Generate type-orm models from existing tables
```
npx typeorm-model-generator -h localhost -d postgres -u ep_read_user -x <ENTERpassword> -e postgres -o ./ -s ep_asset --case-entity none --case-file none --case-property none   --strictMode ? --relationIds true

```


Migrate Data
Migrate data in a schema from source DB to destination DB.
Generally, when migrating the stage or prod DB, we need to migrate all the data in ep_asset schema.

ADD the env variables used in this file to your .env.  Carefully check the code and everything before running the file.  THE CODE TRUNCATES ALL THE TABLES IN EP_ASSET IN THE DESTINATION DB.
```
./node_modules/.bin/ts-node src/db/scripts/migrate_data.ts
```


## (deprecated. use typeorm instead) Sequelize Migrations 
```
create migration file
npx sequelize migration:create --name ds_ercot_stubbed_tables

migrate up
npx sequelize db:migrate

migrate down
npx sequelize db:migrate:undo
```



