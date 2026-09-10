// GET  /groundtruth/register/?next=...   renders the form
// POST /groundtruth/register/            stores the registration, sets the cookie, sends the reader on
//
// Bindings (Pages project settings):
//   GATE_SECRET        secret, any long random string; signs the reader cookie
//   GT_LIST            KV namespace; one key per email
//   ADMIN_TOKEN        secret; unlocks /groundtruth/registrations (CSV export)
//   TURNSTILE_SITEKEY  optional; renders the Turnstile widget when set
//   TURNSTILE_SECRET   optional; verifies it
//   NOTIFY_TO          optional; email address to notify on each registration
//   NOTIFY             optional; send_email binding (Email Routing) used with NOTIFY_TO
import { makeCookie, safeNext, esc } from "../../_lib.js";

const page = (env, { next, error = "", values = {} }) => `<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Register · Ground Truth · Contact Patch Advisory</title>
<meta name="robots" content="noindex">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@700;800&family=IBM+Plex+Mono:wght@400;500&family=Public+Sans:wght@400;500;600&display=swap">
${env.TURNSTILE_SITEKEY ? '<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>' : ""}
<style>
:root{--ground:#E9E6DF;--ground-2:#DFDCD4;--ink:#15171A;--ink-2:#4A4E54;--ink-3:#7C8189;--rule:#C4C0B6;--rule-2:#A9A499;--cyan:#0D6F7D;--magenta:#A81F58;--tape:#15171A;--tape-ink:#E9E6DF;
--f-mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;--f-body:"Public Sans",-apple-system,BlinkMacSystemFont,Helvetica,Arial,sans-serif;--f-disp:"Big Shoulders Display","Public Sans",Impact,sans-serif}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--ground:#0B0C0E;--ground-2:#101215;--ink:#E7E9EB;--ink-2:#A2A8AF;--ink-3:#6C7379;--rule:#23272B;--rule-2:#343A40;--cyan:#4FC3D2;--magenta:#D6437A;--tape:#E7E9EB;--tape-ink:#0B0C0E}}
:root[data-theme="dark"]{--ground:#0B0C0E;--ground-2:#101215;--ink:#E7E9EB;--ink-2:#A2A8AF;--ink-3:#6C7379;--rule:#23272B;--rule-2:#343A40;--cyan:#4FC3D2;--magenta:#D6437A;--tape:#E7E9EB;--tape-ink:#0B0C0E}
*{box-sizing:border-box}body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--f-body);font-size:16.5px;line-height:1.6}
.wrap{max-width:640px;margin:0 auto;padding:clamp(28px,6vw,72px) clamp(18px,4vw,52px) 80px}
.mark{font-family:var(--f-disp);font-weight:800;text-transform:uppercase;font-size:21px;letter-spacing:.02em;color:var(--ink);text-decoration:none}.mark span{color:var(--cyan)}
.tape{display:inline-block;margin-top:36px;background:var(--tape);color:var(--tape-ink);font-family:var(--f-mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;padding:5px 10px 4px}
h1{font-family:var(--f-disp);font-weight:800;text-transform:uppercase;font-size:clamp(40px,8vw,64px);line-height:.92;margin:14px 0 12px;text-wrap:balance}
p{max-width:58ch;color:var(--ink-2);margin:12px 0}
form{margin-top:28px;display:grid;gap:16px}
label{display:grid;gap:6px;font-family:var(--f-mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3)}
input{font:inherit;font-family:var(--f-body);font-size:16px;padding:11px 12px;border:1px solid var(--rule-2);background:var(--ground-2);color:var(--ink);border-radius:0}
input:focus-visible{outline:2px solid var(--cyan);outline-offset:2px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:16px}@media (max-width:520px){.two{grid-template-columns:1fr}}
.consent{display:flex;gap:10px;align-items:flex-start;font-family:var(--f-body);font-size:14px;text-transform:none;letter-spacing:0;color:var(--ink-2)}
.consent input{width:18px;height:18px;margin-top:2px;flex:none}
button{font-family:var(--f-mono);font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;background:var(--tape);color:var(--tape-ink);border:0;padding:14px 20px;cursor:pointer;justify-self:start}
button:hover{background:var(--cyan)}
.err{border-left:3px solid var(--magenta);padding:8px 12px;color:var(--ink);background:var(--ground-2);font-size:14.5px}
.fine{font-family:var(--f-mono);font-size:11.5px;color:var(--ink-3);line-height:1.7;margin-top:28px}
.fine a{color:var(--cyan)}
</style></head><body><div class="wrap">
<a class="mark" href="/">CONTACT&nbsp;<span>PATCH</span> ADVISORY</a>
<div class="tape">Ground Truth &middot; Registered readers</div>
<h1>The brief in full.</h1>
<p>The carousels on LinkedIn and the pages here are open. The complete briefs as PDF, with every figure linked to its filing, the corrections log and the open items, go to registered readers. Name and email, nothing else, and you are through for a year on this browser.</p>
${error ? `<div class="err">${esc(error)}</div>` : ""}
<form method="post" action="/groundtruth/register/">
  <input type="hidden" name="next" value="${esc(next)}">
  <div class="two">
    <label>Name<input id="name" name="name" required autocomplete="name" value="${esc(values.name)}"></label>
    <label>Email<input id="email" name="email" type="email" required autocomplete="email" value="${esc(values.email)}"></label>
  </div>
  <div class="two">
    <label>Company <span style="color:var(--rule-2)">optional</span><input id="company" name="company" autocomplete="organization" value="${esc(values.company)}"></label>
    <label>Role <span style="color:var(--rule-2)">optional</span><input id="role" name="role" autocomplete="organization-title" value="${esc(values.role)}"></label>
  </div>
  <label class="consent"><input id="consent" name="consent" type="checkbox" required value="yes"><span>Send me new Ground Truth issues and corrections by email. Unsubscribe any time; the list is not sold or shared.</span></label>
  <div style="position:absolute;left:-9999px" aria-hidden="true"><input name="website" tabindex="-1" autocomplete="off"></div>
  ${env.TURNSTILE_SITEKEY ? `<div class="cf-turnstile" data-sitekey="${esc(env.TURNSTILE_SITEKEY)}" data-theme="auto"></div>` : ""}
  <button type="submit">Register and continue</button>
</form>
<p class="fine">Contact Patch Advisory, William Weppner. What is collected: the fields above, the date, and which issue sent you. What it is used for: sending the series and, occasionally, a note about the practice. <a href="/groundtruth/privacy/">Privacy notice</a>.</p>
</div></body></html>`;

const html = (body, status = 200, headers = {}) =>
  new Response(body, { status, headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store", ...headers } });

export async function onRequestGet({ request, env }) {
  const next = safeNext(new URL(request.url).searchParams.get("next"));
  return html(page(env, { next }));
}

export async function onRequestPost({ request, env }) {
  const form = await request.formData();
  const v = k => String(form.get(k) ?? "").trim().slice(0, 200);
  const next = safeNext(v("next"));
  const values = { name: v("name"), email: v("email").toLowerCase(), company: v("company"), role: v("role") };

  if (v("website")) return Response.redirect(new URL(next, request.url).toString(), 303); // honeypot: pretend it worked
  if (!values.name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(values.email))
    return html(page(env, { next, values, error: "A name and a working email address are needed." }), 400);
  if (form.get("consent") !== "yes")
    return html(page(env, { next, values, error: "Tick the box to receive the series; that is what registration is for." }), 400);

  if (env.TURNSTILE_SECRET) {
    const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", {
      method: "POST", headers: { "content-type": "application/json" },
      body: JSON.stringify({ secret: env.TURNSTILE_SECRET, response: form.get("cf-turnstile-response"), remoteip: request.headers.get("CF-Connecting-IP") }),
    }).then(r => r.json()).catch(() => ({ success: false }));
    if (!r.success) return html(page(env, { next, values, error: "The verification did not go through. Try once more." }), 400);
  }

  const record = {
    ...values,
    registered: new Date().toISOString(),
    source: next,
    referer: request.headers.get("Referer") || "",
    country: request.headers.get("CF-IPCountry") || "",
  };
  if (env.GT_LIST) {
    const prior = await env.GT_LIST.get(values.email, "json");
    await env.GT_LIST.put(values.email, JSON.stringify(prior ? { ...prior, ...record, first: prior.first || prior.registered } : record));
  }
  if (env.NOTIFY && env.NOTIFY_TO) {
    try {
      const { EmailMessage } = await import("cloudflare:email");
      const from = `groundtruth@${new URL(request.url).hostname}`;
      const body = Object.entries(record).map(([k, val]) => `${k}: ${val}`).join("\n");
      const raw = `From: Ground Truth <${from}>\r\nTo: ${env.NOTIFY_TO}\r\nSubject: Ground Truth registration: ${values.name}\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n${body}\r\n`;
      await env.NOTIFY.send(new EmailMessage(from, env.NOTIFY_TO, raw));
    } catch (e) { /* notification is best effort; the record is already stored */ }
  }

  const headers = { Location: new URL(next, request.url).toString() };
  if (env.GATE_SECRET) headers["Set-Cookie"] = await makeCookie(env.GATE_SECRET, values.email);
  return new Response(null, { status: 303, headers });
}
