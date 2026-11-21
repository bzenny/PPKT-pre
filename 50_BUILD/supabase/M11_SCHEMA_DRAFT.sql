-- DRAFT / M1.1 synthetic-only schema. NOT APPLIED TO A LIVE DATABASE.
-- Run only on isolated Supabase staging after D1 human authorization.
BEGIN;
CREATE SCHEMA IF NOT EXISTS sandbox_finance;
CREATE TABLE IF NOT EXISTS sandbox_finance.demo_accounts (
 account_id text PRIMARY KEY, kind text NOT NULL,
 currency char(3) NOT NULL DEFAULT 'PHP' CHECK (currency='PHP'),
 created_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS sandbox_finance.demo_posting_batches (
 batch_id uuid PRIMARY KEY, transfer_id uuid, reason text NOT NULL,
 created_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS sandbox_finance.demo_journal_entries (
 entry_id uuid PRIMARY KEY, batch_id uuid NOT NULL REFERENCES sandbox_finance.demo_posting_batches,
 account_id text NOT NULL REFERENCES sandbox_finance.demo_accounts,
 side text NOT NULL CHECK (side in ('DEBIT','CREDIT')),
 amount_minor bigint NOT NULL CHECK(amount_minor>0),
 created_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS sandbox_finance.demo_transfers (
 transfer_id uuid PRIMARY KEY, actor_id uuid NOT NULL, idempotency_key text NOT NULL,
 quote_id uuid NOT NULL, state text NOT NULL,
 principal_minor bigint NOT NULL CHECK(principal_minor>0),
 fee_minor bigint NOT NULL CHECK(fee_minor>=0),
 provider_reference text UNIQUE, created_at timestamptz NOT NULL DEFAULT now(),
 UNIQUE(actor_id,idempotency_key));
CREATE TABLE IF NOT EXISTS sandbox_finance.demo_outbox (
 event_id uuid PRIMARY KEY, transfer_id uuid NOT NULL REFERENCES sandbox_finance.demo_transfers,
 event_type text NOT NULL, status text NOT NULL, created_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS sandbox_finance.demo_provider_events (
 provider_event_id text PRIMARY KEY, transfer_id uuid REFERENCES sandbox_finance.demo_transfers,
 payload_hash text NOT NULL, event_type text NOT NULL, received_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS sandbox_finance.demo_reconciliation_runs (
 run_id uuid PRIMARY KEY, transfer_id uuid NOT NULL REFERENCES sandbox_finance.demo_transfers,
 outcome text NOT NULL, evidence_hash text NOT NULL, created_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS sandbox_finance.demo_audit_events (
 audit_id uuid PRIMARY KEY, actor_id uuid, transfer_id uuid,
 action text NOT NULL, payload_hash text, created_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS sandbox_finance.demo_quotes (
 quote_id uuid PRIMARY KEY, actor_id uuid NOT NULL, principal_minor bigint NOT NULL,
 fee_minor bigint NOT NULL, expires_at timestamptz NOT NULL, created_at timestamptz NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS sandbox_finance.demo_personas (
 persona_id uuid PRIMARY KEY, alias text NOT NULL UNIQUE, created_at timestamptz NOT NULL DEFAULT now());
-- Do not permit direct public, anon or authenticated API access to the private schema.
REVOKE ALL ON SCHEMA sandbox_finance FROM PUBLIC, anon, authenticated;
REVOKE ALL ON ALL TABLES IN SCHEMA sandbox_finance FROM PUBLIC, anon, authenticated;
-- Defense in depth; detailed scoped privileged code/policies must be reviewed before implementation.
DO $$ DECLARE r record; BEGIN
 FOR r IN SELECT tablename FROM pg_tables WHERE schemaname='sandbox_finance' LOOP
  EXECUTE format('ALTER TABLE sandbox_finance.%I ENABLE ROW LEVEL SECURITY',r.tablename);
 END LOOP;
END $$;
COMMIT;
-- STOP: this is a draft structure, not a complete financial ledger implementation.
-- Pending: deferrable batch balancing trigger, immutable journal enforcement,
-- explicit state transition function, reconciler role contract, quote expiry, and migrations tests.
