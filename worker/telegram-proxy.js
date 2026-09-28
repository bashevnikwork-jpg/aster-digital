/**
 * SkyBreeze Worker — two jobs:
 *   POST  /            → lead relay: forwards form submissions to Telegram, with
 *                        the bot token held in secrets (TG_TOKEN, TG_CHAT_ID).
 *   GET   /publish     → public "publish now" button: triggers the GitHub Actions
 *                        content-sync workflow, using GH_PUBLISH_TOKEN (a narrow
 *                        fine-grained PAT). Optional PUBLISH_KEY guards the link.
 * Deploy + secrets: worker/README.md.
 */
const REPO = "bashevnikwork-jpg/aster-digital";
const BRANCH = "claude/astra-digital-redesign-olfqg2";
const WORKFLOW = "sync-content.yml";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    if (url.pathname === "/publish" || url.pathname === "/publish/") {
      return publish(url, env);
    }

    // default: lead relay
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
    if (!contact) return json({ ok: false, error: "no contact" }, 400, cors);

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

async function publish(url, env) {
  if (env.PUBLISH_KEY && url.searchParams.get("key") !== env.PUBLISH_KEY) {
    return page("⛔ Невірне посилання", "Ключ у посиланні відсутній або невірний.", 403);
  }
  if (!env.GH_PUBLISH_TOKEN) {
    return page("⚙️ Ще не налаштовано", "Кнопку публікації ще не під'єднали до GitHub.", 503);
  }
  const r = await fetch(
    `https://api.github.com/repos/${REPO}/actions/workflows/${WORKFLOW}/dispatches`,
    {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + env.GH_PUBLISH_TOKEN,
        "Accept": "application/vnd.github+json",
        "User-Agent": "skybreeze-publish",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ ref: BRANCH }),
    }
  );
  if (r.status === 204) {
    return page("✅ Публікацію запущено", "Сайт оновиться приблизно за 1–2 хвилини. Можна закривати цю сторінку.", 200);
  }
  const body = await r.text();
  return page("⚠️ Не вдалося запустити", "GitHub відповів кодом " + r.status + ". " + body.slice(0, 200), 502);
}

function json(obj, status, cors) {
  return new Response(JSON.stringify(obj), {
    status, headers: { ...cors, "Content-Type": "application/json" },
  });
}

function page(title, msg, status) {
  const html = `<!doctype html><html lang="uk"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>${title} — SkyBreeze</title>
<style>
  body{margin:0;min-height:100vh;display:grid;place-items:center;background:#0B0F14;color:#F8FAFC;
       font-family:'Inter Tight',system-ui,sans-serif;text-align:center;padding:24px}
  .card{max-width:32rem}
  h1{font-size:clamp(1.6rem,5vw,2.4rem);letter-spacing:-.03em;margin:0 0 12px}
  p{color:#9CA3AF;font-size:1.05rem;line-height:1.5;margin:0}
  a{display:inline-block;margin-top:24px;color:#3B82F6;text-decoration:none;font-weight:600}
</style></head><body><div class="card">
  <h1>${title}</h1><p>${msg}</p>
  <a href="https://skybreeze.agency/">← На сайт</a>
</div></body></html>`;
  return new Response(html, {
    status, headers: { "Content-Type": "text/html; charset=utf-8" },
  });
}
