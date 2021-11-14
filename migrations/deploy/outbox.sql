-- Deploy outbox:outbox to pg

BEGIN;

SET client_min_messages = 'warning';

CREATE TABLE app.outbox (
    id             UUID        PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type TEXT        NOT NULL,
    aggregate_id   TEXT        NOT NULL,
    type           TEXT        NOT NULL,
    payload        TEXT        NOT NULL
);

COMMIT;
