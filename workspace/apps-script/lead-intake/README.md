# D3X Workspace Lead Intake

This Google Apps Script Web App is the public buffer endpoint for `d3x.biz` diagnostic form submissions.

It stores public lead intake in Google Sheets. It does not call D3X internal services, does not call `d3x-orch`, does not send emails, and does not call external APIs.

## Architecture Rule

Approved flow:

```text
d3x.biz public form
-> Google Apps Script lead intake
-> Google Sheets / Google Workspace
-> internal D3X Workspace Importer
-> Policy Gate
-> draft-only commercial workflow
-> human approval
```

Blocked flow:

```text
d3x.biz public form
-> d3x-orch direct API call
```

## Create The Google Sheet

1. Create a new Google Sheet in the D3X Google Workspace account.
2. Name it something like `D3X Public Leads`.
3. Keep the first worksheet as the intake worksheet.
4. Add these headers in row 1, or let the script create them on the first valid submission:

```text
lead_id
created_at
source
source_channel
name
company
email
phone
business_type
process_problem
current_tools
urgency
budget_range
consent
status
import_status
notes
```

## Set LEADS_SHEET_ID

1. Open the Apps Script project.
2. Go to `Project Settings`.
3. Add a Script Property:

```text
Property: LEADS_SHEET_ID
Value: your Google Sheet ID
```

Do not hardcode the Sheet ID in `Code.gs`.

## Deploy As A Web App

1. In Apps Script, click `Deploy`.
2. Select `New deployment`.
3. Choose `Web app`.
4. Execute as the script owner or the dedicated Workspace automation account.
5. Set access according to the intended public intake policy.
6. Deploy and copy the Web App URL.

Do not paste real deployment URLs into this repository.

## Configure The Public Site

In the public static site JavaScript, set:

```javascript
const D3X_WORKSPACE_LEAD_ENDPOINT = "PASTE_GOOGLE_APPS_SCRIPT_WEB_APP_URL_HERE";
```

The public site must accept only URLs that start with:

```text
https://script.google.com/
```

## D3X Import Reminder

D3X must import later from Workspace through the governed internal Workspace Importer.

The public website must never call:

- `d3x-orch`
- `d3x-data`
- `d3x-compute`
- LAN IPs
- Tailscale URLs
- localhost URLs
- private hostnames
- direct public proxy routes into D3X

## Operational Restrictions

- No automatic email sending.
- No Gmail calls.
- No external API calls.
- No client contact without human approval.
- No final quote without human approval.
- No client system access without explicit approval.

## Response Shape

The endpoint returns:

```json
{
  "success": true,
  "status": "received",
  "message": "Lead received by Workspace intake.",
  "lead_id": "lead_example"
}
```

Errors return the same shape with `success: false` and without stack traces.
