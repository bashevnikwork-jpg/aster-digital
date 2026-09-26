/**
 * SkyBreeze lead relay — Cloudflare Worker.
 *
 * Keeps the Telegram bot token OFF the public site: the form POSTs here, and the
 * token lives only in this Worker's secrets (TG_TOKEN, TG_CHAT_ID). Deploy steps
 * are in worker/README.md. Free tier is plenty for form volume.
 */
export default {
  async fetch(request, env) {
    const cors = {
      "Access-Control-Allow-Origin": "https://skybreeze.agency",
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };
    if (request.method === "OPTIONS") return new Response(null, { headers: cors });
    if (request.method !== "POST")
      return new Response("Method not allowed", { status: 405, headers: cors });

    let data;
    try { data = await request.json(); } catch {
      return new Response("Bad request", { status: 400, headers: cors });
    }

    const clip = (v) => String(v || "").slice(0, 300);
    const contact = clip(data.contact), topic = clip(data.topic), page = clip(data.page);
    if (!contact)
      return json({ ok: false, error: "no contact" }, 400, cors);

    const when = new Date().toLocaleString("uk-UA", { timeZone: "Europe/Kyiv" });
    const text =
      "🔔 *Нова заявка — SkyBreeze*\n\n" +
      "📞 *Контакт:* " + contact + "\n" +
      "📋 *Послуга:* " + topic + "\n" +
      "📅 *Час:* " + when + "\n" +
      "🌐 *Сторінка:* " + page;

    const tg = await fetch(
      "https://api.telegram.org/bot" + env.TG_TOKEN + "/sendMessage",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: env.TG_CHAT_ID, text, parse_mode: "Markdown" }),
      }
    );
    return json({ ok: tg.ok }, tg.ok ? 200 : 502, cors);
  },
};

function json(obj, status, cors) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { ...cors, "Content-Type": "application/json" },
  });
}
