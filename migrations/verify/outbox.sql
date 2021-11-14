-- Verify outbox:outbox on pg

BEGIN;

SELECT id,
       aggregate_type,
       aggregate_id,
       type,
       payload
FROM app.outbox WHERE FALSE;

ROLLBACK;
