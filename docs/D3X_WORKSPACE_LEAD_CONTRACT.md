# D3X Workspace Lead Contract

## Purpose

This contract defines how leads collected from `d3x.biz` through Google Workspace are represented before D3X absorbs them through governed internal importers.

This is a schema and documentation contract only. It does not connect to Google APIs, D3X internal services, email systems, task systems, or production databases.

## Contract Files

- `schemas/d3x-workspace-lead.schema.json`
- `schemas/d3x-workspace-lead-event.schema.json`
- `examples/d3x-workspace-lead.example.json`
- `examples/d3x-workspace-lead-event.example.json`

## Security Position

Workspace is the buffer layer between the public website and D3X internals.

The public website never calls D3X internal APIs. D3X internal importers either pull from Workspace or receive manually exported Workspace data. Public intake must not expose internal URLs, API keys, tokens, LAN IPs, Tailscale URLs, localhost URLs, private hostnames, or direct proxy routes into D3X.

No outbound email, final quote, follow-up, or client system access may happen without explicit human approval.

## Lead Record

The lead record is the canonical Workspace-derived intake object. It describes the current known state of a commercial lead.

Required fields:

- `lead_id`
- `created_at`
- `source`
- `source_channel`
- `name`
- `email`
- `process_problem`
- `consent`
- `status`
- `import_status`

All other fields may be present as optional or nullable operational context.

Allowed status values:

- `received`
- `validated`
- `needs_review`
- `classified`
- `draft_created`
- `human_review_required`
- `approved_to_contact`
- `contacted`
- `closed`
- `rejected`
- `spam`

## Lead Event

The lead event record captures changes and decisions during absorption. Events provide an audit trail from Workspace intake through policy review, memory mapping, draft generation, human approval, and any eventual approved client contact.

Allowed event types:

- `lead_received`
- `lead_validated`
- `lead_rejected`
- `lead_classified`
- `lead_summary_created`
- `draft_response_created`
- `quote_draft_created`
- `human_review_requested`
- `human_approved`
- `human_rejected`
- `client_contacted`
- `lead_archived`

## External Action Rule

`external_action.attempted` must remain `false` unless a human has approved the action.

If `external_action.attempted` is `true`, then:

- `external_action.approved_by_human` must be `true`
- `requires_human_approval` must be `false`

This prevents a draft event from being treated as an approved outbound action.

## D3X Memory Mapping

`L0`: raw submitted lead and raw import event.

`L1`: current lead state, status, classification, recommended next action.

`L2`: reusable commercial insight, objections, business pattern, service opportunity.

Memory writes must preserve the Workspace source trace and must not trigger outbound communication.

## Absorption Flow

```text
d3x.biz public form
-> Google Apps Script or controlled public intake endpoint
-> Google Sheets / Google Workspace
-> internal D3X Workspace Importer
-> Policy Gate
-> L0/L1/L2 memory
-> Agency Runtime
-> draft-only commercial tasks
-> human approval
-> outbound response/cotizacion/follow-up
```

## Importer Responsibilities

The future D3X Workspace Importer must:

- read only approved Workspace sources
- validate lead rows against `d3x-workspace-lead.schema.json`
- emit events using `d3x-workspace-lead-event.schema.json`
- reject malformed rows
- flag missing consent
- flag possible secrets in free text
- deduplicate leads
- classify business type and process problem
- create only draft tasks before human approval
- write import status back to Workspace when integration exists

## Human Approval Requirements

Human approval is required before:

- sending an email
- making a call
- sending a message
- sending a quote
- scheduling a commercial follow-up
- asking for client system access
- moving from draft response to outbound response
- moving from quote draft to final quote

## Fake Data Rule

Examples must use fake sample data only.

Examples must not contain:

- real personal data
- secrets
- tokens
- credentials
- internal URLs
- LAN IPs
- Tailscale URLs
- localhost URLs
- private hostnames

## v0.1 Scope

In v0.1, this contract only defines schemas, examples, and documentation. It does not implement Google API calls, D3X importer code, memory writes, agency runtime tasks, outbound messaging, or production persistence.

## Remaining Integration Steps

1. Create a Google Sheet that matches the lead field model.
2. Add Google Apps Script or a controlled intake endpoint that writes only to Workspace.
3. Build an internal D3X Workspace Importer.
4. Add JSON Schema validation to the importer.
5. Add Policy Gate checks for consent, secrets, source, and outbound restrictions.
6. Add memory mapping for L0/L1/L2.
7. Add draft-only commercial task creation.
8. Add human approval workflow before any external action.
