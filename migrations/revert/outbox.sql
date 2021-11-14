-- Revert outbox:outbox from pg

BEGIN;

DROP TABLE app.outbox;

COMMIT;
