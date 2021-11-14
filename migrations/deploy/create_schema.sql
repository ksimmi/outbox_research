-- Deploy outbox:create_schema to pg

BEGIN;

CREATE SCHEMA IF NOT EXISTS app;

COMMIT;
