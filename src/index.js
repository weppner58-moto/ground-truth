// contactpatchadvisory.com — a Worker with static assets (site/) and the Ground Truth registration gate.
//
// Static files are served from site/ by the ASSETS binding; _redirects in site/ handles the short links.
// The Worker runs first for /groundtruth/* and handles:
//   GET/POST /groundtruth/register/      the registration form; stores the record, sets the reader cookie
//   GET      /groundtruth/registrations  CSV export, Authorization: Bearer <ADMIN_TOKEN>
//   gate     /groundtruth/NN/   one URL per issue: the whole brief for readers with the cookie (served from
//            site/groundtruth/NN/full/index.html), the public page with the register panel for everyone else
//            /groundtruth/assets/GroundTruth-NN_Full-Brief.pdf needs the cookie; /groundtruth/NN/full/ redirects
//
// Bindings: ASSETS (assets), GT_LIST (KV), secrets GATE_SECRET and ADMIN_TOKEN; optional TURNSTILE_SITEKEY,
// TURNSTILE_SECRET, NOTIFY (send_email) + NOTIFY_TO. GATE_KEY in wrangler.toml [vars] stands in for GATE_SECRET
// until a real secret is set; with neither, nothing is gated and the full page is public.
import { registerGet, registerPost } from "./register.js";
import { registrationsCsv } from "./registrations.js";
import { readCookie } from "./lib.js";

const GATED_PDF = /^\/groundtruth\/assets\/GroundTruth-\d\d_Full-Brief\.pdf$/i;
const ISSUE = /^\/groundtruth\/(\d\d)\/$/;
const FULL = /^\/groundtruth\/(\d\d)\/full(\/.*)?$/;
const SHORT = /^\/(\d\d|gt)\/?$/;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const p = url.pathname;

    if (p === "/groundtruth/register" || p === "/groundtruth/register/") {
      if (request.method === "POST") return registerPost(request, env);
      if (request.method === "GET") return registerGet(request, env);
      return new Response("Method not allowed", { status: 405 });
    }
    if (p === "/groundtruth/registrations") return registrationsCsv(request, env);

    const secret = env.GATE_SECRET || env.GATE_KEY;
    const reader = secret ? await readCookie(secret, request) : null;

    // the old two-URL layout: send /NN/full/ to the issue URL
    const f = p.match(FULL);
    if (f) return Response.redirect(new URL(`/groundtruth/${f[1]}/${url.hash || ""}`, url).toString(), 301);

    // short links from the posts: /03 -> /groundtruth/03/, keeping ?p= so the campaign tag survives
    const sl = p.match(SHORT);
    if (sl) return Response.redirect(new URL(`/groundtruth/${sl[1] === "gt" ? "" : sl[1] + "/"}${url.search}`, url).toString(), 301);

    const i = p.match(ISSUE);
    if (i) {
      // one URL: the complete brief for a registered reader, the public page otherwise
      // the assets binding serves a directory's index.html at the directory URL (index.html itself redirects)
      const which = (!secret || reader) ? `/groundtruth/${i[1]}/full/` : `/groundtruth/${i[1]}/`;
      const r = await env.ASSETS.fetch(new Request(new URL(which, url), request));
      const h = new Headers(r.headers);
      h.set("cache-control", "private, no-store");
      h.set("vary", "Cookie");
      // ?p=1 on a post link marks which part sent the reader; kept in a cookie until they register
      const tag = (url.searchParams.get("p") || url.searchParams.get("utm_content") || "").replace(/[^\w.-]/g, "").slice(0, 24);
      if (tag) h.append("Set-Cookie", `gt_src=${i[1]}-${tag}; Path=/; Max-Age=2592000; SameSite=Lax; Secure`);
      return new Response(r.body, { status: r.status, headers: h });
    }

    if (secret && GATED_PDF.test(p) && !reader) {
      const to = new URL("/groundtruth/register/", url);
      to.searchParams.set("next", p + url.search);
      return Response.redirect(to.toString(), 302);
    }
    return env.ASSETS.fetch(request);
  },
};
