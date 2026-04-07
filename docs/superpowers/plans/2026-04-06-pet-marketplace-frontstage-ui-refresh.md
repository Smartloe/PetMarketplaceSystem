# Pet Marketplace Frontstage UI Refresh Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild the frontstage storefront into a warmer, more trustworthy, less template-like shopping experience without changing the existing backend contracts.

**Architecture:** Keep the existing Vue 3 + Element Plus application structure, but tighten it around one shared visual shell, one coherent token system, and page-specific refreshes for the approved first-round routes. Prefer editing existing page/view files and only introduce one new shared component where repetition is obvious, so the redesign stays compatible with the current API and route flow.

**Tech Stack:** Vue 3, Vue Router 4, Vuex 4, Element Plus, Axios, scoped CSS, global CSS custom properties

---

## Execution Notes

- The current repository is dirty. Do not revert unrelated user changes in:
  - `backstage/pet_shop/.env.template`
  - `backstage/pet_shop/pet_shop_backup.sql`
  - `backstage/pet_shop/pyproject.toml`
  - `backstage/pet_shop/uv.lock`
  - `docs/DEVELOPMENT.md`
  - `frontstage/pet_shop/package.json`
  - `frontstage/pet_shop/package-lock.json`
  - `frontstage/pet_shop/src/api/index.js`
  - `frontstage/pet_shop/src/views/CommodityList.vue`
  - `frontstage/pet_shop/src/views/Login.vue`
  - `frontstage/pet_shop/vue.config.js`
- If execution moves to a dedicated worktree, first make sure the current frontend auth/runtime fixes are preserved there. Do not start from a clean `HEAD` snapshot that omits the uncommitted fixes above.
- Backend and frontend should already be runnable before UI work starts:
  - Backend: `cd /Volumes/有庭树/PROJECTS/PetMarketplaceSystem/backstage/pet_shop && uv run python manage.py runserver 0.0.0.0:8000`
  - Frontend: `cd /Volumes/有庭树/PROJECTS/PetMarketplaceSystem/frontstage/pet_shop && npm run serve`
- This round intentionally does **not** add a new automated frontend test runner. Verification uses the existing `lint` and `build` scripts plus route-by-route manual smoke checks.

## File Map

### Shared foundation

- Modify: `frontstage/pet_shop/src/main.js`
  - Import the final global styles in the correct order and keep the current bootstrap logic intact.
- Modify: `frontstage/pet_shop/src/App.vue`
  - Add the storefront shell wrapper around the routed content.
- Modify: `frontstage/pet_shop/src/assets/design-system.css`
  - Replace the current bright/orange-heavy token set with the approved warm-premium token system and shared primitives.
- Modify: `frontstage/pet_shop/src/assets/style.css`
  - Retire the current legacy template CSS and turn this file into the global shell/layout/Element Plus override layer.

### Shared components

- Modify: `frontstage/pet_shop/src/components/Header.vue`
  - Rebuild navigation hierarchy, account entry, and mobile navigation.
- Modify: `frontstage/pet_shop/src/components/Footer.vue`
  - Rebuild the service promise and footer help block.
- Create: `frontstage/pet_shop/src/components/AuthSplitLayout.vue`
  - Shared visual/layout wrapper for login and register pages.

### Page refreshes

- Modify: `frontstage/pet_shop/src/views/Home.vue`
  - Replace the template-like hero/carousel/emoji card structure with a curated storefront homepage.
- Modify: `frontstage/pet_shop/src/views/CommodityList.vue`
  - Rebuild the directory layout, guest preview handling, and unlock feedback.
- Modify: `frontstage/pet_shop/src/views/CommodityDetail.vue`
  - Rebuild the detail layout around the purchase decision path.
- Modify: `frontstage/pet_shop/src/views/Login.vue`
  - Move the login experience onto the shared auth layout.
- Modify: `frontstage/pet_shop/src/views/Register.vue`
  - Move the registration experience onto the shared auth layout.
- Modify: `frontstage/pet_shop/src/views/UserCenter.vue`
  - Reframe the account page around profile summary and friendlier address management.

### Conditional touch points

- Verify only, do not proactively rewrite unless visual regressions remain after the shared shell pass:
  - `frontstage/pet_shop/src/views/Favorites.vue`
  - `frontstage/pet_shop/src/views/Messages.vue`
  - `frontstage/pet_shop/src/views/Orders.vue`
  - `frontstage/pet_shop/src/views/ShoppingCart.vue`
  - `frontstage/pet_shop/src/views/AIPetExpert.vue`

## Task 1: Stabilize the Global Design Foundation

**Files:**
- Modify: `frontstage/pet_shop/src/main.js`
- Modify: `frontstage/pet_shop/src/App.vue`
- Modify: `frontstage/pet_shop/src/assets/design-system.css`
- Modify: `frontstage/pet_shop/src/assets/style.css`
- Test: `frontstage/pet_shop/package.json` via `npm run lint` and `npm run build`

- [ ] **Step 1: Replace the token layer in `design-system.css`**

  Introduce the approved palette, spacing, radius, shadow, type, and motion tokens. Keep the file focused on:
  - CSS custom properties
  - base reset
  - typography scale
  - reusable layout utilities
  - shared button/card/input primitives

  Critical snippet to preserve in spirit:

  ```css
  :root {
    --bg-canvas: #f7f3ed;
    --bg-surface: rgba(255, 252, 247, 0.92);
    --text-strong: #2d241f;
    --text-muted: #6f645d;
    --brand-primary: #db7c5d;
    --brand-primary-strong: #c76546;
    --brand-accent: #7fa2a6;
    --line-soft: rgba(82, 57, 46, 0.12);
    --shadow-soft: 0 18px 40px rgba(83, 56, 40, 0.08);
    --radius-lg: 24px;
    --motion-standard: 220ms ease;
  }
  ```

- [ ] **Step 2: Replace `style.css` with the actual storefront shell layer**

  Remove the current dead template styles and repurpose the file for:
  - page background textures/gradients
  - shared shell spacing
  - Element Plus visual overrides
  - shared empty/loading/notice styling
  - responsive adjustments that should not live inside one view

  Do **not** leave any of the current Barlow/demo-nav/template rules behind.

- [ ] **Step 3: Import the global style stack in `main.js`**

  Make sure `main.js` imports both global CSS files in a deterministic order:

  ```js
  import './assets/design-system.css';
  import './assets/style.css';
  ```

  Keep the existing app bootstrap, store, router, and ResizeObserver shim intact.

- [ ] **Step 4: Add the routed content shell in `App.vue`**

  Replace the bare `Header -> router-view -> Footer` structure with a shell wrapper so every route sits inside a consistent surface:

  ```vue
  <template>
    <div class="app-shell">
      <Header />
      <main class="app-main-shell">
        <router-view />
      </main>
      <Footer />
    </div>
  </template>
  ```

- [ ] **Step 5: Verify the foundation changes**

  Run:

  ```bash
  cd /Volumes/有庭树/PROJECTS/PetMarketplaceSystem/frontstage/pet_shop
  npm run lint
  npm run build
  ```

  Expected:
  - `lint` passes
  - `build` completes successfully (warnings are acceptable only if they were already present before the UI refresh)

- [ ] **Step 6: Commit the foundation pass**

  ```bash
  git add frontstage/pet_shop/src/main.js frontstage/pet_shop/src/App.vue frontstage/pet_shop/src/assets/design-system.css frontstage/pet_shop/src/assets/style.css
  git commit -m "feat: establish storefront design foundation"
  ```

## Task 2: Rebuild Header and Footer Into a Real Storefront Shell

**Files:**
- Modify: `frontstage/pet_shop/src/components/Header.vue`
- Modify: `frontstage/pet_shop/src/components/Footer.vue`
- Test: `frontstage/pet_shop/package.json` via `npm run lint` and `npm run build`

- [ ] **Step 1: Rework header navigation around route-aware link data**

  Replace hard-coded emoji links with a compact route config that keeps only the core first-level items in the main nav:

  ```js
  const primaryNav = [
    { label: '首页', href: '/' },
    { label: '在售商品', href: '/commodity' },
    { label: 'AI 宠物顾问', href: '/ai-pet-expert' },
    { label: '购物车', href: '/trade/shopping-carts' }
  ];
  ```

  Move `收藏 / 订单 / 留言` into the account area instead of keeping them beside core browsing links.

- [ ] **Step 2: Rebuild the account entry and mobile navigation**

  Keep the current login-state logic, but change the UI to:
  - show a calm “账户 / 登录” entry instead of emoji/avatar circles
  - group account actions cleanly
  - present mobile navigation as sections instead of a single long list
  - close menus reliably on outside click and route change

- [ ] **Step 3: Rebuild the footer with service promises and light help links**

  The footer should expose:
  - 2-3 concise service/value points
  - a lighter secondary link row
  - a more polished brand close than the current default link strip

- [ ] **Step 4: Verify header/footer behavior manually**

  Start the frontend and verify:
  - desktop nav has no emoji
  - mobile menu opens/closes cleanly
  - guest account entry and logged-in account entry both render correctly
  - footer feels visually connected to the new shell

- [ ] **Step 5: Run lint/build**

  ```bash
  cd /Volumes/有庭树/PROJECTS/PetMarketplaceSystem/frontstage/pet_shop
  npm run lint
  npm run build
  ```

- [ ] **Step 6: Commit the shared shell refresh**

  ```bash
  git add frontstage/pet_shop/src/components/Header.vue frontstage/pet_shop/src/components/Footer.vue
  git commit -m "feat: refresh storefront navigation shell"
  ```

## Task 3: Turn the Homepage Into a Curated Storefront

**Files:**
- Modify: `frontstage/pet_shop/src/views/Home.vue`
- Test: `frontstage/pet_shop/package.json` via `npm run lint` and `npm run build`

- [ ] **Step 1: Remove the template-style loading and hero treatment**

  Delete the current full-screen loading overlay, neon gradient background, and emoji-led service cards. Replace them with a first screen that uses:
  - existing brand image assets
  - one clear headline
  - one primary CTA
  - one secondary CTA

- [ ] **Step 2: Rebuild the homepage into named storefront sections**

  Use the approved structure:
  - hero
  - quick category or browse shortcuts
  - featured product preview
  - trust / buying guidance strip
  - secondary AI consultant entry

  Keep content density moderate. Do not replace one template block stack with another.

- [ ] **Step 3: Rewrite homepage copy to sound like a calm guide**

  Replace promotional filler with concrete, believable text. Favor copy such as:
  - “适合新手家庭”
  - “支持同城看宠”
  - “近期活跃商家优先展示”

  Avoid copy such as:
  - “火爆热卖”
  - “全网最低”
  - “顶级品质”

- [ ] **Step 4: Verify the homepage on desktop and mobile widths**

  Manual checks:
  - hero reads cleanly at desktop width
  - mobile first screen still shows headline + CTA without awkward overflow
  - AI assistant entry reads as secondary, not equal to the storefront CTA

- [ ] **Step 5: Run lint/build**

  ```bash
  cd /Volumes/有庭树/PROJECTS/PetMarketplaceSystem/frontstage/pet_shop
  npm run lint
  npm run build
  ```

- [ ] **Step 6: Commit the homepage rewrite**

  ```bash
  git add frontstage/pet_shop/src/views/Home.vue
  git commit -m "feat: redesign storefront homepage"
  ```

## Task 4: Rebuild the Commodity List Around Guest Preview and Unlock Feedback

**Files:**
- Modify: `frontstage/pet_shop/src/views/CommodityList.vue`
- Verify only, do not rewrite unless required: `frontstage/pet_shop/src/api/index.js`
- Test: `frontstage/pet_shop/package.json` via `npm run lint` and `npm run build`

- [ ] **Step 1: Keep the existing data behavior, then rebuild the layout**

  Preserve the working logic for:
  - category fetch
  - search
  - `preview_limit`
  - logged-in full list unlock

  Rebuild the UI around:
  - page intro block
  - refined category panel
  - search/result summary row
  - premium-feeling product cards

- [ ] **Step 2: Make guest preview feel intentional instead of blocked**

  Keep the current slice behavior, but present it as a guided preview:

  ```js
  const effectiveCommodities = computed(() => {
    if (isLoggedIn.value) return filteredCommodities.value || [];
    return (filteredCommodities.value || []).slice(0, guestPreviewLimit.value || 6);
  });
  ```

  UX requirements:
  - show real products first
  - show a softer unlock cue after the preview area
  - never hard-stop the guest with a modal for browsing

- [ ] **Step 3: Add an explicit “unlocked” feedback state after login**

  When the user logs in and the list refreshes, show a lightweight, inline confirmation that the full catalog is now available. Keep it in the page flow; do not use an intrusive modal.

- [ ] **Step 4: Strengthen card information hierarchy**

  Each card should clearly prioritize:
  - image
  - title
  - price
  - one or two lightweight decision hints

  Do not leave cards as image + title + gray price only.

- [ ] **Step 5: Manually verify the list flow**

  Manual flow:
  - open `/commodity` as guest
  - confirm the preview count matches `preview_limit` or falls back to 6
  - confirm unlock messaging appears after the preview, not before the first products
  - log in from `/accounts/login`
  - confirm redirect to `/commodity` still works and the list becomes visibly fuller
  - search and click a category after login to confirm the list still uses full data

- [ ] **Step 6: Run lint/build**

  ```bash
  cd /Volumes/有庭树/PROJECTS/PetMarketplaceSystem/frontstage/pet_shop
  npm run lint
  npm run build
  ```

- [ ] **Step 7: Commit the list refresh**

  ```bash
  git add frontstage/pet_shop/src/views/CommodityList.vue
  git commit -m "feat: redesign commodity directory experience"
  ```

## Task 5: Reframe the Commodity Detail Page Around Purchase Decisions

**Files:**
- Modify: `frontstage/pet_shop/src/views/CommodityDetail.vue`
- Test: `frontstage/pet_shop/package.json` via `npm run lint` and `npm run build`

- [ ] **Step 1: Rebuild the top of the detail page into a decision-first layout**

  The first viewport should answer:
  - what is this
  - how much is it
  - why should I trust it
  - what should I do next

  Keep the current data fetch behavior; change the presentation order and weight.

- [ ] **Step 2: Establish one primary CTA and one secondary CTA**

  Keep both actions, but do not style them as equals:
  - primary: add to cart / immediate buy-style action
  - secondary: favorite

  If the design calls for “咨询” language, keep the actual existing cart behavior intact and only change UI wording if it does not confuse the action.

- [ ] **Step 3: Replace hard-coded generic trust chips**

  Remove the current fixed tags such as “正品保证 / 79元包邮 / 30天退货” unless the underlying data really supports them. Prefer calmer, believable support text or neutral highlights derived from the existing page context.

- [ ] **Step 4: Keep login gating friendlier**

  Preserve the current `ensureLoggedIn()` behavior, but make sure:
  - UI copy explains the benefit before redirecting
  - the page itself does not feel locked to guests
  - reviews/detail tabs still read cleanly after the visual rewrite

- [ ] **Step 5: Manually verify the detail flow**

  Manual flow:
  - open a product from `/commodity`
  - confirm the hero section is readable on desktop and mobile
  - as guest, click the primary CTA and confirm login redirection still works
  - as logged-in user, add to cart and add to favorites to confirm no regression

- [ ] **Step 6: Run lint/build**

  ```bash
  cd /Volumes/有庭树/PROJECTS/PetMarketplaceSystem/frontstage/pet_shop
  npm run lint
  npm run build
  ```

- [ ] **Step 7: Commit the detail refresh**

  ```bash
  git add frontstage/pet_shop/src/views/CommodityDetail.vue
  git commit -m "feat: redesign commodity detail page"
  ```

## Task 6: Build the Shared Auth Layout and Refresh Login/Register

**Files:**
- Create: `frontstage/pet_shop/src/components/AuthSplitLayout.vue`
- Modify: `frontstage/pet_shop/src/views/Login.vue`
- Modify: `frontstage/pet_shop/src/views/Register.vue`
- Test: `frontstage/pet_shop/package.json` via `npm run lint` and `npm run build`

- [ ] **Step 1: Create `AuthSplitLayout.vue`**

  Build one shared layout component with slots/props for:
  - visual panel
  - headline and supporting copy
  - form area
  - footer switch link

  Keep it simple. The layout exists to avoid duplicating the same shell in `Login.vue` and `Register.vue`.

- [ ] **Step 2: Move `Login.vue` onto the shared layout**

  Keep the existing captcha and login submission behavior, but redesign the page to:
  - explain why logging in is useful
  - make the captcha feel integrated
  - use a calmer primary CTA such as “进入商城” or “登录查看完整内容”

- [ ] **Step 3: Move `Register.vue` onto the shared layout**

  Keep the current validation logic, but change the page to feel like a guided start instead of a raw form card.

  Fix the existing route target while you are here:

  ```js
  const goToLogin = () => {
    router.push('/accounts/login');
  };
  ```

- [ ] **Step 4: Verify auth flow end-to-end**

  Manual flow:
  - open `/accounts/login`
  - confirm captcha still refreshes as username changes
  - log in successfully and confirm redirect to `/commodity`
  - open `/accounts/register`
  - confirm switch links between login and register use the correct routes

- [ ] **Step 5: Run lint/build**

  ```bash
  cd /Volumes/有庭树/PROJECTS/PetMarketplaceSystem/frontstage/pet_shop
  npm run lint
  npm run build
  ```

- [ ] **Step 6: Commit the auth refresh**

  ```bash
  git add frontstage/pet_shop/src/components/AuthSplitLayout.vue frontstage/pet_shop/src/views/Login.vue frontstage/pet_shop/src/views/Register.vue
  git commit -m "feat: refresh storefront auth experience"
  ```

## Task 7: Turn User Center Into an Account Space

**Files:**
- Modify: `frontstage/pet_shop/src/views/UserCenter.vue`
- Test: `frontstage/pet_shop/package.json` via `npm run lint` and `npm run build`

- [ ] **Step 1: Reorganize the page around summary-first hierarchy**

  Keep all current data capabilities, but change the visual structure to:
  - profile summary at the top
  - profile editing block below
  - address management as a second major section

- [ ] **Step 2: Soften the address management experience**

  Keep the current CRUD logic, but make the address section feel less like a back-office table. If a full card-grid rewrite becomes too risky for this round, keep the table logic but wrap it in a more polished surface and action bar.

- [ ] **Step 3: Keep avatar upload and profile update flows intact**

  Do not rewrite API behavior. Only improve structure, labels, help text, and visual grouping.

- [ ] **Step 4: Verify the account flows manually**

  Manual flow:
  - open `/accounts/user-center` while logged in
  - confirm profile data loads
  - update one editable field and save
  - upload an avatar
  - add or edit an address and confirm the dialog still works

- [ ] **Step 5: Run lint/build**

  ```bash
  cd /Volumes/有庭树/PROJECTS/PetMarketplaceSystem/frontstage/pet_shop
  npm run lint
  npm run build
  ```

- [ ] **Step 6: Commit the account center refresh**

  ```bash
  git add frontstage/pet_shop/src/views/UserCenter.vue
  git commit -m "feat: redesign account center"
  ```

## Task 8: Finish With Secondary-Page Shell Checks and Full Regression Pass

**Files:**
- Verify only, modify only if required:
  - `frontstage/pet_shop/src/views/Favorites.vue`
  - `frontstage/pet_shop/src/views/Messages.vue`
  - `frontstage/pet_shop/src/views/Orders.vue`
  - `frontstage/pet_shop/src/views/ShoppingCart.vue`
  - `frontstage/pet_shop/src/views/AIPetExpert.vue`
- Test: `frontstage/pet_shop/package.json` via `npm run lint` and `npm run build`

- [ ] **Step 1: Smoke-check the secondary pages against the new shell**

  Visit:
  - `/favorites`
  - `/messages`
  - `/trade/orders`
  - `/trade/shopping-carts`
  - `/ai-pet-expert`

  Only make page-local edits if the new global shell causes obvious spacing, overflow, or contrast regressions.

- [ ] **Step 2: Check mobile layouts**

  In responsive mode, verify the following routes at a phone width:
  - `/`
  - `/commodity`
  - product detail opened from the list
  - `/accounts/login`
  - `/accounts/register`
  - `/accounts/user-center`

- [ ] **Step 3: Run the final verification suite**

  ```bash
  cd /Volumes/有庭树/PROJECTS/PetMarketplaceSystem/frontstage/pet_shop
  npm run lint
  npm run build
  ```

- [ ] **Step 4: Summarize any follow-up items**

  If anything remains outside the approved first-round scope, write it down before the final commit as a short follow-up list rather than quietly expanding the implementation.

- [ ] **Step 5: Commit the final polish pass**

  If Task 8 required no code changes, skip this commit. If Task 8 did require follow-up fixes, stage **only** the files touched during that polish pass, then commit:

  ```bash
  git add <exact files touched in Task 8>
  git commit -m "feat: complete storefront UI refresh"
  ```

## Manual Smoke Checklist

Use this checklist after Task 8:

- [ ] Guest sees a polished homepage with no emoji-led nav or template gradient overload.
- [ ] Guest opening `/commodity` sees real products first, then a soft login-to-unlock cue.
- [ ] Logged-in user returning to `/commodity` clearly sees a fuller catalog and an inline unlock confirmation.
- [ ] Product detail presents one obvious primary action and keeps guest login gating intact.
- [ ] Login and register share the same visual system and route correctly between each other.
- [ ] User center reads as an account page, not a back-office form.
- [ ] Secondary pages still render inside the new shell without obvious visual breakage.
- [ ] Desktop and mobile both feel intentional rather than compressed.
