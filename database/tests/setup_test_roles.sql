-- Read-only role used by test_table_permissions.py.
-- Run once against a local database before the permission tests:
--   psql -h localhost -U postgres -d ks_bd -f database/tests/setup_test_roles.sql
CREATE ROLE member LOGIN PASSWORD 'member';
GRANT SELECT ON TABLE public."USERS" TO member;
