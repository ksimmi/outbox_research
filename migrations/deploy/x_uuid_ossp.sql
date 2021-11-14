-- Deploy outbox:x_uuid_ossp to pg

BEGIN;

SET search_path TO 'app';

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

COMMIT;
