-- Revert outbox:x_uuid_ossp from pg

BEGIN;

DROP EXTENSION "uuid-ossp";

COMMIT;
