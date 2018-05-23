CREATE USER {{ postgres_metrics_user }} PASSWORD '{{ postgres_metrics_user_password }}';
ALTER USER {{ postgres_metrics_user }} SET SEARCH_PATH TO {{ postgres_metrics_user }},pg_catalog;

-- If deploying as non-superuser (for example in AWS RDS)
-- GRANT {{ postgres_metrics_user }} TO :MASTER_USER;
CREATE SCHEMA {{ postgres_metrics_user }} AUTHORIZATION {{ postgres_metrics_user }};

CREATE VIEW {{ postgres_metrics_user }}.pg_stat_activity
AS
  SELECT * from pg_catalog.pg_stat_activity;

GRANT SELECT ON {{ postgres_metrics_user }}.pg_stat_activity TO {{ postgres_metrics_user }};

CREATE VIEW {{ postgres_metrics_user }}.pg_stat_replication AS
  SELECT * from pg_catalog.pg_stat_replication;

GRANT SELECT ON {{ postgres_metrics_user }}.pg_stat_replication TO {{ postgres_metrics_user }};