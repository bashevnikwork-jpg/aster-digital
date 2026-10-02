/**
 * SkyBreeze Worker — three jobs:
 *   POST  /            → lead relay: saves the submission to the D1 database and
 *                        forwards it to Telegram (one or more chats in TG_CHAT_ID,
 *                        comma-separated). Bot token in secret TG_TOKEN.
 *   GET   /publish     → public "publish now" button: triggers the content-sync
 *                        GitHub Actions workflow (GH_PUBLISH_TOKEN). Guarded by PUBLISH_KEY.
 *   GET   /leads       → protected list of all saved leads (guarded by PUBLISH_KEY).
 * Deploy + secrets + D1: worker/README.md.
 */
const REPO = "bashevnikwork-jpg/aster-digital";
const BRANCH = "claude/astra-digital-redesign-olfqg2";
const WORKFLOW = "sync-content.yml";

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname.startsWith("/publish")) return publish(url, env);
    if (url.pathname.startsWith("/leads")) return leads(url, env);
    return relay(request, env);
  },
};

async function relay(request, env) {
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

  // 1) persist to the database (so a lead is never lost even if Telegram fails)
  if (env.DB) {
    try {
      await env.DB.prepare("INSERT INTO leads (ts, contact, topic, page) VALUES (?, ?, ?, ?)")
        .bind(when, contact, topic, page).run();
    } catch (e) { /* logging must never block delivery */ }
  }

  // 2) send to every configured Telegram chat
  const text =
    "🔔 *Нова заявка — SkyBreeze*\n\n" +
    "📞 *Контакт:* " + contact + "\n" +
    "📋 *Послуга:* " + topic + "\n" +
    "📅 *Час:* " + when + "\n" +
    "🌐 *Сторінка:* " + page;
  const chats = String(env.TG_CHAT_ID || "").split(",").map((s) => s.trim()).filter(Boolean);
  let okAny = false;
  for (const chat of chats) {
    try {
      const tg = await fetch("https://api.telegram.org/bot" + env.TG_TOKEN + "/sendMessage", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: chat, text, parse_mode: "Markdown" }),
      });
      if (tg.ok) okAny = true;
    } catch (e) { /* try the next chat */ }
  }
  return json({ ok: okAny }, 200, cors);
}

async function publish(url, env) {
  if (env.PUBLISH_KEY && url.searchParams.get("key") !== env.PUBLISH_KEY)
    return page("⛔ Невірне посилання", "Ключ у посиланні відсутній або невірний.", 403);
  if (!env.GH_PUBLISH_TOKEN)
    return page("⚙️ Ще не налаштовано", "Кнопку публікації ще не під'єднали до GitHub.", 503);
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
  if (r.status === 204)
    return page("✅ Публікацію запущено", "Сайт оновиться приблизно за 1–2 хвилини. Можна закривати цю сторінку.", 200);
  return page("⚠️ Не вдалося запустити", "GitHub відповів кодом " + r.status + ".", 502);
}

async function leads(url, env) {
  if (env.PUBLISH_KEY && url.searchParams.get("key") !== env.PUBLISH_KEY)
    return page("⛔ Невірне посилання", "Ключ у посиланні відсутній або невірний.", 403);
  if (!env.DB) return page("⚙️ База не підключена", "", 503);
  let rows = [];
  try {
    const res = await env.DB.prepare("SELECT ts, contact, topic, page FROM leads ORDER BY id DESC LIMIT 1000").all();
    rows = res.results || [];
  } catch (e) {
    return page("⚠️ Помилка бази", String(e).slice(0, 200), 502);
  }
  const esc = (s) => String(s || "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  const trs = rows.map((r) =>
    `<tr><td>${esc(r.ts)}</td><td>${esc(r.contact)}</td><td>${esc(r.topic)}</td><td class="muted">${esc(r.page)}</td></tr>`
  ).join("") || `<tr><td colspan="4" class="muted">Поки що заявок немає.</td></tr>`;
  const html = `<!doctype html><html lang="uk"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Заявки — SkyBreeze</title>
<style>
  body{margin:0;background:#0B0F14;color:#F8FAFC;font-family:'Inter Tight',system-ui,sans-serif;padding:28px}
  h1{font-size:1.6rem;letter-spacing:-.03em;margin:0 0 4px}
  .sub{color:#9CA3AF;margin:0 0 20px}
  table{width:100%;border-collapse:collapse;font-size:.95rem}
  th,td{text-align:left;padding:11px 14px;border-bottom:1px solid #1E293B;vertical-align:top}
  th{color:#9CA3AF;font-weight:600;font-size:.8rem;text-transform:uppercase;letter-spacing:.05em}
  td.muted,.muted{color:#6B7280}
  tr:hover td{background:#111827}
</style></head><body>
  <h1>Заявки SkyBreeze</h1>
  <p class="sub">Усього: ${rows.length} · оновлюється автоматично при кожній новій заявці</p>
  <table><thead><tr><th>Час (Київ)</th><th>Контакт</th><th>Послуга</th><th>Сторінка</th></tr></thead>
  <tbody>${trs}</tbody></table>
</body></html>`;
  return new Response(html, { status: 200, headers: { "Content-Type": "text/html; charset=utf-8" } });
}

function json(obj, status, cors) {
  return new Response(JSON.stringify(obj), { status, headers: { ...cors, "Content-Type": "application/json" } });
}
function page(title, msg, status) {
  const html = `<!doctype html><html lang="uk"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>${title} — SkyBreeze</title>
<style>body{margin:0;min-height:100vh;display:grid;place-items:center;background:#0B0F14;color:#F8FAFC;
font-family:'Inter Tight',system-ui,sans-serif;text-align:center;padding:24px}
h1{font-size:clamp(1.6rem,5vw,2.4rem);letter-spacing:-.03em;margin:0 0 12px}
p{color:#9CA3AF;font-size:1.05rem;line-height:1.5;margin:0}
a{display:inline-block;margin-top:24px;color:#3B82F6;text-decoration:none;font-weight:600}</style></head>
<body><div><h1>${title}</h1><p>${msg}</p><a href="https://skybreeze.agency/">← На сайт</a></div></body></html>`;
  return new Response(html, { status, headers: { "Content-Type": "text/html; charset=utf-8" } });
}
