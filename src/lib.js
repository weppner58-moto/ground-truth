// Shared helpers for the Ground Truth registration gate (Cloudflare Pages Functions).

const COOKIE = "gt_reader";
const YEAR = 60 * 60 * 24 * 365;

const enc = new TextEncoder();

async function hmac(secret, msg) {
  const key = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  const sig = await crypto.subtle.sign("HMAC", key, enc.encode(msg));
  return [...new Uint8Array(sig)].map(b => b.toString(16).padStart(2, "0")).join("");
}

const b64u = s => btoa(unescape(encodeURIComponent(s))).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
const unb64u = s => decodeURIComponent(escape(atob(s.replace(/-/g, "+").replace(/_/g, "/"))));

export async function makeCookie(secret, email) {
  const ts = Math.floor(Date.now() / 1000).toString();
  const body = `${ts}.${b64u(email)}`;
  const sig = await hmac(secret, body);
  return `${COOKIE}=v1.${body}.${sig}; Max-Age=${YEAR}; Path=/groundtruth; Secure; HttpOnly; SameSite=Lax`;
}

export async function readCookie(secret, request) {
  const raw = request.headers.get("Cookie") || "";
  const m = raw.match(new RegExp(`(?:^|;\\s*)${COOKIE}=v1\\.(\\d+)\\.([A-Za-z0-9_-]+)\\.([0-9a-f]{64})`));
  if (!m) return null;
  const [, ts, em, sig] = m;
  if ((await hmac(secret, `${ts}.${em}`)) !== sig) return null;
  if (Date.now() / 1000 - Number(ts) > YEAR) return null;
  try { return unb64u(em); } catch { return null; }
}

export function safeNext(next) {
  // Only ever send a reader back to a path on this site.
  if (typeof next !== "string" || !next.startsWith("/") || next.startsWith("//")) return "/groundtruth/";
  return next;
}

export const esc = s => String(s ?? "").replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
