var LEAD_COLUMNS = [
  "lead_id",
  "created_at",
  "source",
  "source_channel",
  "name",
  "company",
  "email",
  "phone",
  "business_type",
  "process_problem",
  "current_tools",
  "urgency",
  "budget_range",
  "consent",
  "status",
  "import_status",
  "notes"
];

function doPost(e) {
  try {
    var payload = parsePayload_(e);

    if (isHoneypotFilled_(payload)) {
      return jsonResponse_({
        success: false,
        status: "rejected",
        message: "Submission rejected.",
        lead_id: null
      });
    }

    var validationMessage = validatePayload_(payload);
    if (validationMessage) {
      return jsonResponse_({
        success: false,
        status: "invalid",
        message: validationMessage,
        lead_id: null
      });
    }

    var sheetId = PropertiesService.getScriptProperties().getProperty("LEADS_SHEET_ID");
    if (!sheetId) {
      return jsonResponse_({
        success: false,
        status: "configuration_error",
        message: "Lead intake is not configured.",
        lead_id: null
      });
    }

    var leadId = generateLeadId_();
    var createdAt = new Date().toISOString();
    var lead = normalizeLead_(payload, leadId, createdAt);

    appendLead_(sheetId, lead);

    return jsonResponse_({
      success: true,
      status: "received",
      message: "Lead received by Workspace intake.",
      lead_id: leadId
    });
  } catch (error) {
    return jsonResponse_({
      success: false,
      status: "error",
      message: "Unable to process lead intake.",
      lead_id: null
    });
  }
}

function parsePayload_(e) {
  if (!e || !e.postData || !e.postData.contents) {
    throw new Error("Missing post body.");
  }
  return JSON.parse(e.postData.contents);
}

function validatePayload_(payload) {
  if (!payload || typeof payload !== "object") {
    return "Invalid payload.";
  }
  if (!String(payload.name || "").trim()) {
    return "Name is required.";
  }
  if (!isValidEmail_(String(payload.email || "").trim())) {
    return "Valid email is required.";
  }
  if (!String(payload.process_problem || "").trim()) {
    return "Process problem is required.";
  }
  if (!payload.consent || payload.consent.provided !== true) {
    return "Consent is required.";
  }
  return "";
}

function isHoneypotFilled_(payload) {
  return Boolean(payload && String(payload.website || "").trim());
}

function normalizeLead_(payload, leadId, createdAt) {
  return {
    lead_id: leadId,
    created_at: createdAt,
    source: "d3x.biz",
    source_channel: "public_website",
    name: cleanString_(payload.name),
    company: cleanString_(payload.company),
    email: cleanString_(payload.email),
    phone: cleanString_(payload.phone),
    business_type: cleanString_(payload.business_type),
    process_problem: cleanString_(payload.process_problem),
    current_tools: normalizeTools_(payload.current_tools),
    urgency: cleanString_(payload.urgency || "unknown"),
    budget_range: cleanString_(payload.budget_range || "unknown"),
    consent: true,
    status: "received",
    import_status: "pending_d3x_import",
    notes: ""
  };
}

function appendLead_(sheetId, lead) {
  var spreadsheet = SpreadsheetApp.openById(sheetId);
  var sheet = spreadsheet.getSheets()[0];
  ensureHeader_(sheet);
  sheet.appendRow(LEAD_COLUMNS.map(function(column) {
    return lead[column];
  }));
}

function ensureHeader_(sheet) {
  var firstRow = sheet.getRange(1, 1, 1, LEAD_COLUMNS.length).getValues()[0];
  var hasHeader = firstRow.some(function(value) {
    return String(value || "").trim();
  });

  if (!hasHeader) {
    sheet.getRange(1, 1, 1, LEAD_COLUMNS.length).setValues([LEAD_COLUMNS]);
  }
}

function generateLeadId_() {
  return "lead_" + Utilities.getUuid().replace(/-/g, "").slice(0, 24);
}

function normalizeTools_(tools) {
  if (Array.isArray(tools)) {
    return tools.map(cleanString_).filter(Boolean).join(", ");
  }
  return cleanString_(tools);
}

function cleanString_(value) {
  return String(value || "").trim().slice(0, 2000);
}

function isValidEmail_(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

function jsonResponse_(payload) {
  return ContentService
    .createTextOutput(JSON.stringify(payload))
    .setMimeType(ContentService.MimeType.JSON);
}
