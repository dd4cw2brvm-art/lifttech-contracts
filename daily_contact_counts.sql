-- Run once in Supabase Dashboard -> SQL Editor.
-- The primary key guarantees exactly one record per Riyadh calendar date.

create table if not exists public.daily_contact_counts (
    record_date date primary key,
    maintenance_count integer not null default 0
        check (maintenance_count >= 0),
    installation_count integer not null default 0
        check (installation_count >= 0),
    updated_at timestamptz not null default now(),
    entered_by text not null
        check (length(trim(entered_by)) > 0)
);

alter table public.daily_contact_counts enable row level security;

comment on table public.daily_contact_counts is
    'One manually entered customer-count record per Riyadh date.';
