-- Verify outbox:create_schema on pg

BEGIN;

SELECT pg_catalog.has_schema_privilege('app', 'usage');

ROLLBACK;
