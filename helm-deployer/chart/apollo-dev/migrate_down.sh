#!/bin/sh
./node_modules/.bin/ts-node ./node_modules/typeorm/cli.js migration:revert -f src/db/config/typeorm_migration.ts --connection $*