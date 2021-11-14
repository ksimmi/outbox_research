-- Verify outbox:x_uuid_ossp on pg

BEGIN;

SELECT 1/count(*) FROM pg_extension WHERE extname = 'uuid-ossp';

ROLLBACK;
