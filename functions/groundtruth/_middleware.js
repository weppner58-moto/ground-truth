// Gate: the registered-readers page of each issue (/groundtruth/NN/full/) and the full-brief PDFs
// need a reader cookie. The public pages, the series pages and the carousel PDFs (the same cards
// that run on LinkedIn) stay open. Without GATE_SECRET set nothing is gated, so a preview deploy
// with no bindings still serves the whole site.
import { readCookie } from "../_lib.js";

const GATED = [
  /^\/groundtruth\/assets\/GroundTruth-\d\d_Full-Brief\.pdf$/i,
  /^\/groundtruth\/\d\d\/full\/?/i,
];

export async function onRequest({ request, env, next }) {
  const url = new URL(request.url);
  if (!env.GATE_SECRET || !GATED.some(re => re.test(url.pathname))) return next();
  const email = await readCookie(env.GATE_SECRET, request);
  if (email) return next();
  const to = new URL("/groundtruth/register/", url);
  to.searchParams.set("next", url.pathname + url.search);
  return Response.redirect(to.toString(), 302);
}
