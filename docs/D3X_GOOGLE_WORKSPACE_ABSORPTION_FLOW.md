# D3X Google Workspace Absorption Flow

## Purpose

This document defines how D3X may absorb public lead and customer intake from `d3x.biz` without exposing internal D3X services to the internet.

The core rule is simple:

```text
d3x.biz receives interest.
Google Workspace receives data.
D3X imports later through governance.
```

## Approved Flow

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

## Blocked Flow

```text
d3x.biz public form
-> d3x-orch direct API call
```

This is blocked in every version unless the architecture is formally changed and a new security review approves it. The current target architecture does not require direct public access to `d3x-orch`.

## Why Workspace First

Google Workspace is the safe reception layer because it is designed to receive, store, inspect, filter, and review business information without exposing D3X runtime internals.

Workspace gives D3X:

- a public-safe buffer
- visible lead rows
- human review points
- simple auditability
- permission controls
- lower blast radius
- a stable source for internal importers

## Intake Layer

The public intake layer may be:

- a Squarespace form that writes to Google Workspace
- Google Apps Script Web App receiving form posts
- a controlled public intake endpoint that writes only to Workspace

The intake layer must not call `d3x-orch`, `d3x-data`, `d3x-compute`, private hosts, LAN IPs, Tailscale endpoints, or localhost services.

## Workspace Schema v0.1

Recommended lead sheet columns:

```text
received_at
source
name
company
email
phone
preferred_contact
service_interest
project_summary
budget_range
timeline
consent
status
review_notes
imported_at
import_status
```

Allowed status values:

```text
new
needs_review
approved_for_import
imported
rejected
duplicate
archived
```

## Disallowed Workspace Intake Values

The public form and Apps Script layer must not ask users for:

- passwords
- API keys
- access tokens
- private URLs
- production credentials
- payment card data
- government IDs
- internal D3X references
- secrets in file uploads

If users voluntarily include secrets in free text, the row must be flagged for human review before import.

## Internal Workspace Importer

The Workspace Importer is an internal D3X component. It reads from Google Workspace using approved internal credentials and runs inside the D3X internal boundary.

Importer responsibilities:

- read only approved sheets or ranges
- validate expected columns
- normalize lead records
- detect duplicates
- reject malformed records
- classify service interest
- flag sensitive or suspicious text
- write safe summaries to memory
- create draft-only commercial tasks
- mark import status back in Workspace

## Policy Gate

Before memory writes or runtime task creation, every imported lead must pass the Policy Gate.

The Policy Gate must check:

- source is Workspace-approved
- consent is present
- required fields are present
- no internal endpoint is requested
- no secrets appear in public fields
- lead is not rejected or archived
- lead has not already been imported
- outbound action remains draft-only

## Memory Path

After policy approval, imported data may be written into memory layers:

- `L0`: raw normalized intake metadata and source trace
- `L1`: summarized lead profile and service interest
- `L2`: longer-lived commercial context only after human-approved relevance

No memory layer may trigger client contact without human approval.

## Agency Runtime Path

The Agency Runtime may receive a draft commercial task such as:

- draft discovery questions
- draft project summary
- draft quote outline
- draft follow-up plan
- draft qualification notes

The runtime must not send email, message the client, publish a quote, or commit to scope automatically.

## Human Approval

Human approval is required before:

- outbound response
- quotation
- follow-up
- commercial commitment
- scheduling proposal
- request for more information
- moving a lead into active project workflow

Approval must be explicit and auditable.

## v0.1 Limitations

In v0.1:

- intake is public-safe only
- Workspace is the reception buffer
- importer is internal only
- tasks are draft-only
- outbound is manual or human-approved
- no direct public D3X API route exists
- no automatic email sending exists

## v0.2 Future Path

In v0.2:

- add Apps Script validation and spam checks
- add structured lead categories
- add importer run logs
- add per-row import decisions
- add review dashboard for intake
- add draft quote templates
- add human approval records

## v0.3 Future Path

In v0.3:

- add controlled public intake endpoint if needed
- add signed intake payloads
- add rate limiting and abuse protection
- add importer observability
- add consent lifecycle management
- add approved outbound queues
- preserve the no-direct-public-call rule for internal D3X services

## Publication Rule

A `d3x.biz` build is not safe for publication if public files contain:

- direct `d3x-orch` calls
- direct `d3x-data` calls
- direct `d3x-compute` calls
- LAN IPs
- Tailscale endpoints
- localhost URLs
- private hostnames
- API keys
- tokens
- public proxy routes into D3X
- automatic email sending logic
