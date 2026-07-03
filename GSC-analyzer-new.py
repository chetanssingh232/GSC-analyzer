import streamlit as st
import pandas as pd

st.set_page_config(page_title="SEO SaaS MVP", layout="wide")


# -----------------------------
# CLEAN NUMBER
# -----------------------------
def clean_number(v):
    try:
        if pd.isna(v):
            return 0
        return float(str(v).replace("%", "").strip())
    except:
        return 0


# -----------------------------
# SEO ENGINE
# -----------------------------
def analyze(clicks, impressions, ctr, position):

    score = 0
    actions = []

    if impressions > 1000 and ctr < 2:
        score += 40
        actions.append("Improve title/meta (CTR issue)")

    if position > 10:
        score += 30
        actions.append("Improve content depth")

    if clicks < 10:
        score += 20
        actions.append("Expand content")

    if score >= 60:
        priority = "HIGH 🔴"
    elif score >= 30:
        priority = "MEDIUM 🟠"
    else:
        priority = "LOW 🟢"

    return priority, actions


# -----------------------------
# DASHBOARD
# -----------------------------
def dashboard():

    st.title("🚀 SEO Dashboard")

    file = st.file_uploader("Upload Google Search Console CSV", type=["csv"])

    if file:

        df = pd.read_csv(file)

        results = []

        for _, row in df.iterrows():

            clicks = clean_number(row.get("Clicks", 0))
            impressions = clean_number(row.get("Impressions", 0))
            ctr = clean_number(row.get("CTR", 0))
            position = clean_number(row.get("Position", 0))

            priority, actions = analyze(clicks, impressions, ctr, position)

            results.append({
                "Page": row.get("Top pages", "Unknown"),
                "Clicks": clicks,
                "Impressions": impressions,
                "CTR": ctr,
                "Position": position,
                "Priority": priority,
                "Recommendations": " | ".join(actions)
            })

        out = pd.DataFrame(results)

        # -----------------------------
        # SUMMARY METRICS
        # -----------------------------
        total_clicks = out["Clicks"].sum()
        total_impressions = out["Impressions"].sum()

        col1, col2 = st.columns(2)

        col1.metric("Total Clicks", f"{int(total_clicks):,}")
        col2.metric("Total Impressions", f"{int(total_impressions):,}")

        st.divider()

        # -----------------------------
        # TOP PAGES
        # -----------------------------
        top_click_page = out.loc[out["Clicks"].idxmax()]
        top_impression_page = out.loc[out["Impressions"].idxmax()]

        col1, col2 = st.columns(2)

        with col1:
            st.success("🏆 Top Page by Clicks")
            st.write(f"**Page:** {top_click_page['Page']}")
            st.write(f"**Clicks:** {int(top_click_page['Clicks'])}")

        with col2:
            st.info("👁️ Top Page by Impressions")
            st.write(f"**Page:** {top_impression_page['Page']}")
            st.write(f"**Impressions:** {int(top_impression_page['Impressions'])}")

        st.divider()

        # -----------------------------
        # GRAPHS
        # -----------------------------
        st.subheader("📈 Clicks by Page")

        click_chart = out.sort_values(
            by="Clicks",
            ascending=False
        ).set_index("Page")[["Clicks"]]

        st.bar_chart(click_chart)

        st.subheader("📊 Impressions by Page")

        impression_chart = out.sort_values(
            by="Impressions",
            ascending=False
        ).set_index("Page")[["Impressions"]]

        st.bar_chart(impression_chart)

        st.divider()

        # -----------------------------
        # SEO TABLE
        # -----------------------------
        st.subheader("📋 SEO Insights")

        st.dataframe(
            out,
            use_container_width=True
        )

        st.download_button(
            "📥 Download SEO Report",
            out.to_csv(index=False),
            "seo_report.csv",
            mime="text/csv"
        )


dashboard()