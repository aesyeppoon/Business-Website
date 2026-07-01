const DEFAULT_TO_EMAIL = "aes.yeppoon@gmail.com";
const DEFAULT_FROM_EMAIL = "Adaptive Electrical Solutions <noreply@adaptive-electrical.com.au>";
const MAX_FIELD_LENGTH = 160;
const MAX_MESSAGE_LENGTH = 5000;

const json = (body, status = 200, extraHeaders = {}) =>
  new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      ...extraHeaders,
    },
  });

const clean = (value, maxLength = MAX_FIELD_LENGTH) =>
  String(value ?? "")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, maxLength);

const cleanMessage = (value) =>
  String(value ?? "")
    .replace(/\r\n/g, "\n")
    .replace(/\n{4,}/g, "\n\n\n")
    .trim()
    .slice(0, MAX_MESSAGE_LENGTH);

const escapeHtml = (value) =>
  String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");

const isEmail = (value) =>
  value === "" || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);

const toEmailList = (value) =>
  String(value || DEFAULT_TO_EMAIL)
    .split(",")
    .map((email) => email.trim())
    .filter(Boolean);

const fieldRow = (label, value) => `
  <tr>
    <td style="padding:10px 12px;border-bottom:1px solid #e8ecef;color:#597078;font-weight:700;width:180px;">${escapeHtml(label)}</td>
    <td style="padding:10px 12px;border-bottom:1px solid #e8ecef;color:#1f2529;">${escapeHtml(value || "Not provided")}</td>
  </tr>
`;

export async function handleContactRequest(request, env = {}) {
  if (request.method !== "POST") {
    return json(
      { ok: false, message: "This endpoint only accepts quote requests." },
      405,
      { Allow: "POST" },
    );
  }

  let payload;

  try {
    const contentType = request.headers.get("content-type") || "";
    payload = contentType.includes("application/json")
      ? await request.json()
      : Object.fromEntries(await request.formData());
  } catch {
    return json(
      { ok: false, message: "We could not read the quote request. Please try again." },
      400,
    );
  }

  if (clean(payload.company)) {
    return json({
      ok: true,
      message: "Thanks, your request has been sent. We will be in touch shortly.",
    });
  }

  const details = {
    name: clean(payload.name),
    phone: clean(payload.phone),
    email: clean(payload.email, 240),
    location: clean(payload.location),
    service: clean(payload.service),
    message: cleanMessage(payload.message),
  };

  const errors = [];

  if (!details.name) errors.push("Name is required.");
  if (!details.phone) errors.push("Phone is required.");
  if (!details.location) errors.push("Property location is required.");
  if (!details.message) errors.push("Job details are required.");
  if (!isEmail(details.email)) errors.push("Please enter a valid email address.");

  if (errors.length > 0) {
    return json({ ok: false, message: errors[0] }, 400);
  }

  if (!env.RESEND_API_KEY) {
    console.error("Missing RESEND_API_KEY environment variable.");
    return json(
      {
        ok: false,
        message: "The quote form is not fully configured yet. Please call 0402 139 169.",
      },
      500,
    );
  }

  const subject = `Quote request from ${details.name} - ${details.location}`;
  const submittedAt = new Date().toLocaleString("en-AU", {
    timeZone: "Australia/Brisbane",
    dateStyle: "medium",
    timeStyle: "short",
  });

  const text = [
    subject,
    "",
    `Name: ${details.name}`,
    `Phone: ${details.phone}`,
    `Email: ${details.email || "Not provided"}`,
    `Property location: ${details.location}`,
    `Type of work: ${details.service || "Not provided"}`,
    `Submitted: ${submittedAt}`,
    "",
    "Job details:",
    details.message,
  ].join("\n");

  const html = `
    <div style="margin:0;padding:0;background:#f5f7f8;font-family:Arial,sans-serif;color:#1f2529;">
      <div style="max-width:680px;margin:0 auto;padding:28px;">
        <div style="background:#21262a;border-top:8px solid #f8c533;padding:28px;">
          <p style="margin:0 0 8px;color:#35c2d5;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;">Adaptive Electrical Solutions</p>
          <h1 style="margin:0;color:#ffffff;font-size:28px;line-height:1.2;">New quote request</h1>
        </div>
        <div style="background:#ffffff;padding:0 0 28px;">
          <table role="presentation" style="width:100%;border-collapse:collapse;">
            ${fieldRow("Name", details.name)}
            ${fieldRow("Phone", details.phone)}
            ${fieldRow("Email", details.email)}
            ${fieldRow("Property location", details.location)}
            ${fieldRow("Type of work", details.service)}
            ${fieldRow("Submitted", submittedAt)}
          </table>
          <div style="padding:24px 28px 0;">
            <h2 style="margin:0 0 12px;color:#1f2529;font-size:18px;">Job details</h2>
            <p style="margin:0;color:#394247;font-size:16px;line-height:1.6;white-space:pre-wrap;">${escapeHtml(details.message)}</p>
          </div>
        </div>
      </div>
    </div>
  `;

  const body = {
    from: env.RESEND_FROM_EMAIL || DEFAULT_FROM_EMAIL,
    to: toEmailList(env.CONTACT_TO_EMAIL),
    subject,
    html,
    text,
  };

  if (details.email) {
    body.reply_to = details.email;
  }

  try {
    const resendResponse = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${env.RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(body),
    });

    if (!resendResponse.ok) {
      const errorText = await resendResponse.text();
      console.error("Resend email send failed:", resendResponse.status, errorText);
      return json(
        {
          ok: false,
          message: "The quote request could not be sent right now. Please call 0402 139 169.",
        },
        502,
      );
    }

    return json({
      ok: true,
      message: "Thanks, your request has been sent. We will be in touch shortly.",
    });
  } catch (error) {
    console.error("Quote request send failed:", error);
    return json(
      {
        ok: false,
        message: "The quote request could not be sent right now. Please call 0402 139 169.",
      },
      502,
    );
  }
}
