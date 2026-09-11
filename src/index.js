// contactpatchadvisory.com — a Worker with static assets (site/) and the Ground Truth registration gate.
//
// Static files are served from site/ by the ASSETS binding; _redirects in site/ handles the short links.
// The Worker runs first for /groundtruth/* and handles:
//   GET/POST /groundtruth/register/      the registration form; stores the record, sets the reader cookie
//   GET      /groundtruth/registrations  CSV export, Authorization: Bearer <ADMIN_TOKEN>
//   gate     /groundtruth/NN/full/*  and  /groundtruth/assets/GroundTruth-NN_Full-Brief.pdf  need the cookie
//
// Bindings: ASSETS (assets), GT_LIST (KV), secrets GATE_SECRET and ADMIN_TOKEN; optional TURNSTILE_SITEKEY,
// TURNSTILE_SECRET, NOTIFY (send_email) + NOTIFY_TO. Without GATE_SECRET nothing is gated.
import { registerGet, registerPost } from "./register.js";
import { registrationsCsv } from "./registrations.js";
import { readCookie } from "./lib.js";

const GATED = [
  /^\/groundtruth\/assets\/GroundTruth-\d\d_Full-Brief\.pdf$/i,
  /^\/groundtruth\/\d\d\/full(\/|$)/i,
];

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

    if (env.GATE_SECRET && GATED.some(re => re.test(p))) {
      const email = await readCookie(env.GATE_SECRET, request);
      if (!email) {
        const to = new URL("/groundtruth/register/", url);
        to.searchParams.set("next", p + url.search);
        return Response.redirect(to.toString(), 302);
      }
    }
    return env.ASSETS.fetch(request);
  },
};
