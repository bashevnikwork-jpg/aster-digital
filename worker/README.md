# Secure lead relay (Telegram token off the site)

Today the contact form sends leads to Telegram **directly from the browser**, so the
bot token sits in `script.js` — visible to anyone (public site + public repo). This
Worker moves the token server-side. After it's deployed, the token is removed from the site.

## Deploy (≈ 5 minutes, one time)

1. Create a free **Cloudflare** account: <https://dash.cloudflare.com/sign-up>.
2. **Workers & Pages → Create → Workers → Create Worker** → name it `skybreeze-lead` → **Deploy**.
3. **Edit code** → paste the contents of `telegram-proxy.js` → **Deploy**.
4. **Settings → Variables and Secrets** → add two **Secrets**:
   - `TG_TOKEN` — a **fresh** bot token from @BotFather (see below)
   - `TG_CHAT_ID` — `7578353801`
5. Copy the Worker URL (looks like `https://skybreeze-lead.<subdomain>.workers.dev`) and
   send it to the developer. The developer then points the form at it and deletes the token
   from `script.js` — after that the site carries no token.

## Rotate the token (do this too — the old one leaked)

The current token was public, so treat it as compromised:
1. In Telegram open **@BotFather → /token** (or **/revoke**) → get a new token for the bot.
2. Put the **new** token into the Worker secret `TG_TOKEN` (step 4). The old one stops working.

## Why not just rotate the token in `script.js`?

Because a token in `script.js` is always downloadable by visitors. Rotating without the
Worker just puts a new public token on the site. The Worker is what actually hides it.
