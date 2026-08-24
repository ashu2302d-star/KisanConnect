* { box-sizing: border-box; }

:root {
    --green: #1f7a4d;
    --green-dark: #145236;
    --green-light: #eaf7ef;
    --cream: #f8f6ef;
    --text: #17251d;
    --muted: #65736a;
    --white: #ffffff;
    --border: #dfe7e1;
    --shadow: 0 12px 35px rgba(22, 62, 39, 0.08);
}

body {
    margin: 0;
    font-family: Arial, Helvetica, sans-serif;
    background: var(--cream);
    color: var(--text);
}

a { color: inherit; text-decoration: none; }

.navbar {
    background: var(--white);
    border-bottom: 1px solid var(--border);
    min-height: 70px;
    padding: 0 6%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: sticky;
    top: 0;
    z-index: 10;
}

.brand {
    font-size: 22px;
    font-weight: 800;
    color: var(--green-dark);
}

.navlinks {
    display: flex;
    gap: 20px;
    align-items: center;
}

.navlinks a {
    color: #405046;
    font-size: 14px;
    font-weight: 600;
}

.navlinks a:hover { color: var(--green); }

.menu-btn { display: none; }

.container {
    width: min(1180px, 92%);
    margin: 0 auto;
    padding: 35px 0 60px;
}

.hero {
    display: grid;
    grid-template-columns: 1.5fr 1fr;
    gap: 30px;
    align-items: center;
    padding: 55px 0;
}

.hero h1 {
    font-size: clamp(40px, 6vw, 72px);
    line-height: .98;
    margin: 15px 0 20px;
    letter-spacing: -2px;
}

.hero h1 span { color: var(--green); }

.hero p {
    color: var(--muted);
    font-size: 18px;
    line-height: 1.7;
    max-width: 680px;
}

.pill {
    display: inline-block;
    padding: 7px 11px;
    background: var(--green-light);
    color: var(--green-dark);
    border-radius: 999px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: .8px;
}

.hero-actions { display: flex; gap: 12px; margin-top: 25px; flex-wrap: wrap; }

.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border: 0;
    border-radius: 10px;
    padding: 12px 18px;
    font-weight: 800;
    cursor: pointer;
    font-size: 14px;
}

.btn.primary { background: var(--green); color: white; }
.btn.primary:hover { background: var(--green-dark); }
.btn.secondary { background: white; color: var(--green-dark); border: 1px solid var(--border); }
.btn.full { width: 100%; }

.hero-card, .form-card, .result-card, .feature-card, .product-card, .scheme-card, .listing-card, .market-card, .empty {
    background: white;
    border: 1px solid var(--border);
    border-radius: 18px;
    box-shadow: var(--shadow);
}

.hero-card {
    padding: 35px;
    text-align: center;
    background: linear-gradient(145deg, #ffffff, #eaf7ef);
}

.farmer-icon, .big-emoji { font-size: 70px; }

.stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin: 10px 0 55px;
}

.stats div {
    background: white;
    border: 1px solid var(--border);
    padding: 22px;
    border-radius: 15px;
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.stats b { font-size: 30px; color: var(--green); }
.stats span { color: var(--muted); font-size: 13px; }

.section-title {
    margin: 45px 0 18px;
    font-size: 28px;
}

.feature-grid, .cards {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
}

.feature-card, .product-card, .scheme-card, .listing-card {
    padding: 24px;
    transition: transform .2s;
}

.feature-card:hover, .product-card:hover, .scheme-card:hover {
    transform: translateY(-3px);
}

.feature-icon, .product-icon { font-size: 34px; }

.feature-card p, .scheme-card p, .product-card p, .listing-card p {
    color: var(--muted);
    line-height: 1.6;
}

.page-head {
    padding: 30px 0;
}

.page-head h1 {
    font-size: 46px;
    margin: 12px 0;
}

.page-head p { color: var(--muted); }

.two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 25px;
    align-items: start;
}

.form-card, .result-card { padding: 28px; }

.form-card label {
    display: block;
    font-weight: 700;
    margin: 14px 0 7px;
}

input, select, textarea {
    width: 100%;
    border: 1px solid #ccd8cf;
    border-radius: 9px;
    padding: 12px;
    font: inherit;
    background: white;
}

textarea { min-height: 80px; resize: vertical; }

.form-card button { margin-top: 22px; }

.result-card { min-height: 320px; }

.recommend {
    background: var(--green-light);
    color: var(--green-dark);
    padding: 14px;
    border-radius: 10px;
    margin: 10px 0;
    font-weight: 800;
}

.note { color: var(--muted); line-height: 1.6; }

.crop-tag {
    display: inline-block;
    padding: 5px 9px;
    border-radius: 999px;
    background: #eef4ef;
    color: var(--green-dark);
    font-size: 11px;
    font-weight: 800;
}

.price {
    font-size: 26px;
    font-weight: 900;
    color: var(--green);
    margin: 10px 0;
}

.verified {
    display: block;
    color: var(--green-dark);
    font-size: 12px;
    font-weight: 800;
    margin: 12px 0 18px;
}

.listing-stack { display: grid; gap: 14px; }

.market-card {
    padding: 20px;
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 12px;
    align-items: start;
}

.mini-form {
    display: grid;
    gap: 8px;
    padding-top: 10px;
    min-width: 260px;
}

.delete-btn {
    background: transparent;
    border: 0;
    color: #a44;
    cursor: pointer;
    font-size: 12px;
}

.alert {
    padding: 13px 16px;
    border-radius: 10px;
    margin-bottom: 15px;
    font-weight: 700;
}

.alert.success { background: #e6f6eb; color: #166235; }
.alert.error { background: #fde9e7; color: #8f2f25; }

.empty {
    padding: 45px;
    text-align: center;
}

footer {
    background: #153b28;
    color: white;
    text-align: center;
    padding: 30px 15px;
}

footer small { opacity: .7; }

@media (max-width: 850px) {
    .navlinks {
        display: none;
        position: absolute;
        left: 0;
        right: 0;
        top: 70px;
        background: white;
        padding: 20px 6%;
        flex-direction: column;
        align-items: flex-start;
        border-bottom: 1px solid var(--border);
    }

    .navlinks.open { display: flex; }
    .menu-btn { display: block; border: 0; background: transparent; font-size: 24px; }
    .hero, .two-col { grid-template-columns: 1fr; }
    .stats { grid-template-columns: repeat(2, 1fr); }
    .feature-grid, .cards { grid-template-columns: 1fr 1fr; }
}

@media (max-width: 550px) {
    .feature-grid, .cards, .stats { grid-template-columns: 1fr; }
    .hero h1 { font-size: 42px; }
    .page-head h1 { font-size: 36px; }
    .market-card { grid-template-columns: 1fr; }
    .mini-form { min-width: 0; }
}
