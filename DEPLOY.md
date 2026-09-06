# Deploying KIARIT to Cloudflare

This guide assumes you have never used Cloudflare before. Follow it top to
bottom. Anything you must type is shown in a box — type it exactly.

The site will go live on a **free Cloudflare address** that looks like:

```
https://kiarit.<your-account-name>.workers.dev
```

You do **not** need to buy a domain to do this. When you buy
`kiaritpharmaceuticals.com` later, Part 5 explains how to attach it — the site
does not need rebuilding.

---

## Part 1 — Make a Cloudflare account (once, ~3 minutes)

1. Open <https://dash.cloudflare.com/sign-up> in your browser.
2. Enter your email address and pick a password. Use an email you actually
   read — Cloudflare sends a confirmation link.
3. Click **Sign Up**.
4. Go to your inbox, open the Cloudflare email, click the verification link.
5. You will land on the Cloudflare dashboard. It may ask you to "add a
   website" or pick a plan. **Skip both.** Choose the **Free** plan if it
   forces a choice. You do not need a domain for this guide.

You now have a Cloudflare account. Nothing has been charged; this site stays
inside the free tier.

---

## Part 2 — Connect your computer to Cloudflare (once, ~2 minutes)

You only have to do this the first time.

6. Open a terminal in the project folder (the folder containing `index.html`).
7. Type this and press Enter:

   ```
   npx wrangler login
   ```

8. Your browser will open a Cloudflare page saying an application wants
   access to your account. Click the blue **Allow** button.
9. Go back to the terminal. It should say you are logged in.

To confirm it worked, type:

```
npx wrangler whoami
```

It should print your email address and account name. **Write that account
name down** — it becomes part of your free web address.

---

## Part 3 — Put the site live (~1 minute)

10. In the same terminal, in the same folder, type:

    ```
    python3 tools/build_dist.py && npx wrangler deploy
    ```

11. Wait. When it finishes it prints a line like:

    ```
    https://kiarit.your-account.workers.dev
    ```

12. **Open that address in your browser.** The site is live on the internet.
    Anyone in the world can open that link.

That is the whole deployment. Two commands.

### What those two commands did

The first command (`build_dist.py`) copies the real website files into a
`dist/` folder — the HTML pages, images, CSS, fonts. It deliberately leaves
out things the public must never see, like the `tools/` scripts and the `.git`
history, and it stops with an error if anything unexpected sneaks in.

The second (`wrangler deploy`) uploads that folder to Cloudflare's network,
which has servers in hundreds of cities. A visitor in Delhi is served from
Delhi, one in London from London. That is why it will feel fast everywhere.

---

## Part 4 — Updating the site later

Whenever you change anything, run the same two commands again:

```
python3 tools/build_dist.py && npx wrangler deploy
```

The new version is live worldwide in a few seconds. There is no "publish"
button to press afterwards.

If you changed a page that is **generated** (every page except `index.html`),
rebuild the pages first:

```
python3 tools/pages_phase4.py && python3 tools/pages_phase5.py && python3 tools/pages_phase6.py
python3 tools/build_dist.py && npx wrangler deploy
```

### Previewing before you publish

To see changes on your own machine without putting them online:

```
npx wrangler dev
```

Then open <http://localhost:8787>. This behaves exactly like the live site —
same redirects, same headers. Press `Ctrl+C` to stop it.

---

## Part 5 — Attaching your real domain (when you buy one)

Do this only once you own `kiaritpharmaceuticals.com`.

13. In the Cloudflare dashboard, click **Add a domain** (sometimes **Add a
    site**), type your domain, and choose the **Free** plan.
14. Cloudflare shows you **two nameservers**, e.g. `dana.ns.cloudflare.com`.
15. Log in wherever you bought the domain (GoDaddy, Namecheap, BigRock…),
    find the **Nameservers** setting, delete what is there, and paste
    Cloudflare's two values in. Save.
16. Wait. This can take anywhere from 10 minutes to 24 hours. Cloudflare
    emails you when the domain is active.
17. Once active, open **Workers & Pages** in the dashboard → click **kiarit**
    → **Settings** → **Domains & Routes** → **Add** → **Custom domain**.
18. Type `www.kiaritpharmaceuticals.com` and confirm.

Cloudflare issues the HTTPS certificate automatically and for free. There is
nothing to install, renew, or pay for.

19. **One code change is needed.** The site currently tells search engines its
    address is `https://www.kiaritpharmaceuticals.com`. If your real domain
    differs even slightly, tell me and I will update it and redeploy —
    otherwise Google will index the wrong address.

### Recommended settings once the domain is attached

In the dashboard, under your domain:

- **SSL/TLS → Overview** → set to **Full (strict)**. Forces proper HTTPS.
- **SSL/TLS → Edge Certificates** → turn on **Always Use HTTPS**. Visitors
  typing `http://` get moved to the secure version.
- **Speed → Optimization → Image Optimization** → turn on **Polish** and set
  it to **Lossy**, with **WebP** ticked. This alone cuts roughly 500 KB off
  the product photography, and no code changes.

---

## How the site is configured (reference)

You do not need to read this to deploy. It is here so the choices are not a
mystery later.

| File | What it does |
|---|---|
| `wrangler.jsonc` | Tells Cloudflare the project is called `kiarit` and the files live in `dist/`. |
| `_headers` | Security headers and caching rules. Replaces the `mod_headers` part of `.htaccess`. |
| `_redirects` | Sends old `.html` addresses to the new clean ones, plus short aliases like `/shop`. |
| `tools/build_dist.py` | Assembles `dist/` safely and refuses to run if a private file would be published. |
| `.htaccess` | **Ignored by Cloudflare.** Kept only in case the site ever moves to normal shared hosting. |

### Addresses

The site uses clean addresses — `kiaritpharmaceuticals.com/about`, not
`/about.html`. Old `.html` addresses still work: they permanently redirect
(a "301") to the clean version, so any link already printed or shared keeps
working and search engines transfer their ranking across.

### Caching

Images, CSS, fonts and JavaScript are cached in visitors' browsers for a year,
because they never change without changing their filename. HTML pages are
never cached, so an edit is visible immediately after you deploy. You should
not need to "clear the cache" after updating.

### Cost

The site is static files with no server-side code, so Cloudflare serves it
without running anything billable. The free tier covers this comfortably. You
would only start paying if you later added server-side features and got very
large amounts of traffic.

---

## If something goes wrong

**`npx: command not found`** — Node.js is not installed. Get the LTS version
from <https://nodejs.org>, install it, close the terminal, open a new one.

**`Authentication error` / `not logged in`** — your session expired. Run
`npx wrangler login` again.

**`python3: command not found`** — try `python` instead of `python3`. On
Windows, install Python from <https://python.org> and tick *"Add Python to
PATH"* during setup.

**The deploy succeeded but the page looks broken** — you probably deployed
without rebuilding. Run `python3 tools/build_dist.py` first, then deploy.

**A change is not showing up** — confirm the deploy actually printed a URL and
no error. Then hard-refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac).

**You want to undo a bad deploy** — in the dashboard: **Workers & Pages** →
**kiarit** → **Deployments**. Every past version is listed; open the previous
one and choose **Rollback**.
