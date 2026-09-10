// GET /groundtruth/registrations  with  Authorization: Bearer <ADMIN_TOKEN>  ->  CSV of the list.
export async function onRequestGet({ request, env }) {
  const auth = request.headers.get("Authorization") || "";
  if (!env.ADMIN_TOKEN || auth !== `Bearer ${env.ADMIN_TOKEN}`) return new Response("Not found", { status: 404 });
  if (!env.GT_LIST) return new Response("No list binding", { status: 500 });
  const cols = ["email", "name", "company", "role", "registered", "first", "source", "country"];
  const q = s => `"${String(s ?? "").replace(/"/g, '""')}"`;
  let out = cols.join(",") + "\n", cursor;
  do {
    const page = await env.GT_LIST.list({ cursor });
    for (const k of page.keys) {
      const r = await env.GT_LIST.get(k.name, "json");
      if (r) out += cols.map(c => q(r[c])).join(",") + "\n";
    }
    cursor = page.list_complete ? undefined : page.cursor;
  } while (cursor);
  return new Response(out, { headers: { "content-type": "text/csv; charset=utf-8", "content-disposition": "attachment; filename=groundtruth-registrations.csv", "cache-control": "no-store" } });
}
