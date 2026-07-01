import { handleContactRequest } from "../../src/server/contact-email.js";

const methodNotAllowed = () =>
  new Response(JSON.stringify({ ok: false, message: "Method not allowed." }), {
    status: 405,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      Allow: "POST",
    },
  });

export const onRequest = ({ request, env }) =>
  request.method === "POST" ? handleContactRequest(request, env) : methodNotAllowed();
