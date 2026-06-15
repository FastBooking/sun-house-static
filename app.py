# app.py
# pip install streamlit pandas numpy plotly
# streamlit run app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

st.set_page_config(
    page_title="商辦包租代管 AI 定價系統",
    page_icon="🏢",
    layout="wide",
)

# =========================
# CSS
# =========================
st.markdown(
    """
<style>
:root {
    --bg: #f6f8fb;
    --card: #ffffff;
    --text: #1f2937;
    --muted: #6b7280;
    --green: #2f9e7e;
    --blue: #3b82f6;
    --orange: #f59e0b;
    --red: #ef4444;
    --line: #e5e7eb;
}

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f766e 0%, #155e75 100%);
}

[data-testid="stSidebar"] * {
    color: white !important;
}

.main-title {
    font-size: 32px;
    font-weight: 900;
    color: var(--text);
    margin-bottom: 4px;
}

.sub-title {
    color: var(--muted);
    font-size: 15px;
    margin-bottom: 20px;
}

.card {
    background: var(--card);
    border: 1px solid var(--line);
    border-radius: 20px;
    padding: 20px;
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
    margin-bottom: 16px;
}

.metric-card {
    background: white;
    border-radius: 18px;
    padding: 18px 20px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.05);
    min-height: 128px;
}

.metric-label {
    color: #6b7280;
    font-size: 14px;
    font-weight: 700;
}

.metric-value {
    color: #111827;
    font-size: 28px;
    font-weight: 900;
    margin-top: 8px;
}

.metric-note {
    font-size: 13px;
    margin-top: 8px;
    color: #6b7280;
}

.good {
    color: #059669;
    font-weight: 800;
}

.warn {
    color: #d97706;
    font-weight: 800;
}

.danger {
    color: #dc2626;
    font-weight: 800;
}

.badge {
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 800;
}

.badge-green {
    background: #dcfce7;
    color: #166534;
}

.badge-blue {
    background: #dbeafe;
    color: #1e40af;
}

.badge-orange {
    background: #ffedd5;
    color: #9a3412;
}

.badge-red {
    background: #fee2e2;
    color: #991b1b;
}

.info-box {
    border-radius: 18px;
    padding: 18px;
    background: linear-gradient(135deg, #eff6ff 0%, #ecfeff 100%);
    border: 1px solid #bfdbfe;
    margin-bottom: 16px;
}

.ai-box {
    border-radius: 20px;
    padding: 22px;
    background: linear-gradient(135deg, #ecfdf5 0%, #f0f9ff 50%, #fff7ed 100%);
    border: 1px solid #bbf7d0;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
}

.small-muted {
    color: #6b7280;
    font-size: 13px;
}

.table-title {
    font-size: 18px;
    font-weight: 900;
    color: #111827;
    margin-bottom: 8px;
}

hr {
    margin: 12px 0 16px 0;
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================
# 假資料
# =========================
CUSTOMERS = pd.DataFrame(
    [
        {
            "customer_id": "C001",
            "customer_name": "宏遠資產管理有限公司",
            "contact": "林先生",
            "phone": "0912-345-678",
            "email": "lin@hongyuan.com",
            "type": "法人屋主",
            "status": "合作中",
        },
        {
            "customer_id": "C002",
            "customer_name": "兆盛開發股份有限公司",
            "contact": "王小姐",
            "phone": "0922-111-888",
            "email": "wang@jhaosheng.com",
            "type": "建商",
            "status": "合作中",
        },
        {
            "customer_id": "C003",
            "customer_name": "永和置業投資",
            "contact": "陳先生",
            "phone": "0988-666-222",
            "email": "chen@yongho.com",
            "type": "個人投資戶",
            "status": "觀察中",
        },
    ]
)

PROPERTIES = pd.DataFrame(
    [
        {
            "property_id": "P001",
            "customer_id": "C001",
            "building": "信義金融中心",
            "floor": "12F",
            "unit": "整層",
            "district": "信義區",
            "address": "台北市信義區松仁路",
            "area_ping": 186,
            "current_rent": 558000,
            "occupancy": "已出租",
            "tenant": "雲端科技股份有限公司",
        },
        {
            "property_id": "P002",
            "customer_id": "C001",
            "building": "南京企業廣場",
            "floor": "8F",
            "unit": "整層",
            "district": "松山區",
            "address": "台北市松山區南京東路",
            "area_ping": 142,
            "current_rent": 355000,
            "occupancy": "待出租",
            "tenant": "-",
        },
        {
            "property_id": "P003",
            "customer_id": "C002",
            "building": "內湖科技大樓",
            "floor": "5F",
            "unit": "整層",
            "district": "內湖區",
            "address": "台北市內湖區瑞光路",
            "area_ping": 220,
            "current_rent": 484000,
            "occupancy": "已出租",
            "tenant": "智慧物流有限公司",
        },
        {
            "property_id": "P004",
            "customer_id": "C003",
            "building": "中山商務中心",
            "floor": "10F",
            "unit": "整層",
            "district": "中山區",
            "address": "台北市中山區民生東路",
            "area_ping": 96,
            "current_rent": 211200,
            "occupancy": "即將到期",
            "tenant": "禾豐顧問有限公司",
        },
    ]
)

NEARBY_MARKET = pd.DataFrame(
    [
        {"district": "信義區", "building": "信義金融中心", "avg_price_per_ping": 3100, "growth_rate": 5.8, "vacancy_rate": 4.2},
        {"district": "信義區", "building": "松仁商辦大樓", "avg_price_per_ping": 2980, "growth_rate": 4.9, "vacancy_rate": 5.1},
        {"district": "信義區", "building": "市府企業總部", "avg_price_per_ping": 3250, "growth_rate": 6.3, "vacancy_rate": 3.8},
        {"district": "松山區", "building": "南京企業廣場", "avg_price_per_ping": 2500, "growth_rate": 2.4, "vacancy_rate": 7.2},
        {"district": "松山區", "building": "復興商辦中心", "avg_price_per_ping": 2380, "growth_rate": 1.8, "vacancy_rate": 8.1},
        {"district": "松山區", "building": "敦北辦公大樓", "avg_price_per_ping": 2650, "growth_rate": 3.1, "vacancy_rate": 6.5},
        {"district": "內湖區", "building": "內湖科技大樓", "avg_price_per_ping": 2200, "growth_rate": 3.9, "vacancy_rate": 6.8},
        {"district": "內湖區", "building": "瑞光商辦園區", "avg_price_per_ping": 2150, "growth_rate": 3.4, "vacancy_rate": 7.4},
        {"district": "內湖區", "building": "港墘科技中心", "avg_price_per_ping": 2280, "growth_rate": 4.2, "vacancy_rate": 6.1},
        {"district": "中山區", "building": "中山商務中心", "avg_price_per_ping": 2200, "growth_rate": 1.1, "vacancy_rate": 9.0},
        {"district": "中山區", "building": "民生企業大樓", "avg_price_per_ping": 2140, "growth_rate": 0.8, "vacancy_rate": 9.8},
        {"district": "中山區", "building": "松江金融大樓", "avg_price_per_ping": 2320, "growth_rate": 1.9, "vacancy_rate": 8.5},
    ]
)


def generate_monthly_rent(property_id, base_rent):
    months = pd.date_range("2023-01-01", "2026-06-01", freq="MS")
    seed = int(property_id.replace("P", ""))
    rng = np.random.default_rng(seed)

    data = []
    rent = base_rent * rng.uniform(0.88, 0.95)

    for i, month in enumerate(months):
        if property_id == "P001":
            monthly_growth = rng.normal(0.0048, 0.006)
        elif property_id == "P002":
            monthly_growth = rng.normal(0.0012, 0.009)
        elif property_id == "P003":
            monthly_growth = rng.normal(0.0032, 0.007)
        else:
            monthly_growth = rng.normal(-0.0005, 0.008)

        if i in [12, 24, 36]:
            monthly_growth += rng.uniform(0.01, 0.025)

        rent = rent * (1 + monthly_growth)
        rent = max(rent, base_rent * 0.75)

        data.append(
            {
                "property_id": property_id,
                "month": month,
                "month_label": month.strftime("%Y-%m"),
                "rent": round(rent),
            }
        )

    df = pd.DataFrame(data)
    df["mom_growth"] = df["rent"].pct_change() * 100
    df["yoy_growth"] = df["rent"].pct_change(12) * 100
    return df


RENT_HISTORY = pd.concat(
    [
        generate_monthly_rent(row.property_id, row.current_rent)
        for row in PROPERTIES.itertuples()
    ],
    ignore_index=True,
)


# =========================
# Helper
# =========================
def money(value):
    return f"NT$ {value:,.0f}"


def pct(value):
    if pd.isna(value):
        return "-"
    return f"{value:.2f}%"


def get_growth_status(yoy_growth):
    if pd.isna(yoy_growth):
        return "資料不足", "badge-blue"
    if yoy_growth < 0:
        return "負成長警告", "badge-red"
    if yoy_growth < 2:
        return "成長偏低", "badge-orange"
    return "表現良好", "badge-green"


def ai_recommend_price(selected_property, market_df, rent_df):
    current_price_per_ping = selected_property["current_rent"] / selected_property["area_ping"]
    market_avg = market_df["avg_price_per_ping"].mean()
    market_growth = market_df["growth_rate"].mean()
    vacancy_rate = market_df["vacancy_rate"].mean()

    latest_yoy = rent_df["yoy_growth"].dropna().iloc[-1] if len(rent_df["yoy_growth"].dropna()) else 0

    score = 0
    score += min(max(market_growth, -5), 8) * 0.35
    score += min(max(latest_yoy, -5), 8) * 0.30
    score -= max(vacancy_rate - 5, 0) * 0.20

    if current_price_per_ping < market_avg * 0.95:
        score += 1.2
    elif current_price_per_ping > market_avg * 1.08:
        score -= 1.2

    adjustment_rate = np.clip(score / 100, -0.03, 0.08)

    recommended_price_per_ping = current_price_per_ping * (1 + adjustment_rate)

    lower_bound = market_avg * 0.96
    upper_bound = market_avg * 1.08
    recommended_price_per_ping = np.clip(recommended_price_per_ping, lower_bound, upper_bound)

    recommended_total = recommended_price_per_ping * selected_property["area_ping"]

    return {
        "current_price_per_ping": current_price_per_ping,
        "market_avg": market_avg,
        "market_growth": market_growth,
        "vacancy_rate": vacancy_rate,
        "latest_yoy": latest_yoy,
        "adjustment_rate": adjustment_rate * 100,
        "recommended_price_per_ping": recommended_price_per_ping,
        "recommended_total": recommended_total,
        "lower_total": lower_bound * selected_property["area_ping"],
        "upper_total": upper_bound * selected_property["area_ping"],
    }


# =========================
# Sidebar
# =========================
st.sidebar.markdown("## 🏢 商辦代管系統")
st.sidebar.markdown("包租代管 · 租金分析 · AI 定價")

page = st.sidebar.radio(
    "功能選單",
    [
        "總覽儀表板",
        "客人 DB",
        "物件 DB",
        "單戶租金分析",
        "AI 價格推薦",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 系統狀態")
st.sidebar.success("資料庫連線正常")
st.sidebar.info("AI 定價模型：Sample Mode")


# =========================
# Header
# =========================
st.markdown('<div class="main-title">商辦不動產包租代管系統</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">客人資料、物件資料、租金趨勢、附近行情與 AI 推薦價格整合管理</div>',
    unsafe_allow_html=True,
)


# =========================
# Page 1
# =========================
if page == "總覽儀表板":
    total_properties = len(PROPERTIES)
    total_customers = len(CUSTOMERS)
    total_rent = PROPERTIES["current_rent"].sum()
    avg_price_per_ping = (PROPERTIES["current_rent"] / PROPERTIES["area_ping"]).mean()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">管理物件數</div>
                <div class="metric-value">{total_properties}</div>
                <div class="metric-note">以一棟某樓整層為一戶</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">客人數</div>
                <div class="metric-value">{total_customers}</div>
                <div class="metric-note">支援一對一 / 一對多物件</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">月租金總額</div>
                <div class="metric-value">{money(total_rent)}</div>
                <div class="metric-note">目前委管物件合計</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">平均坪租</div>
                <div class="metric-value">{money(avg_price_per_ping)}</div>
                <div class="metric-note">每坪每月租金</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 物件租金分布")

    chart_df = PROPERTIES.copy()
    chart_df["price_per_ping"] = chart_df["current_rent"] / chart_df["area_ping"]
    chart_df["display_name"] = chart_df["building"] + " " + chart_df["floor"]

    fig = px.bar(
        chart_df,
        x="display_name",
        y="current_rent",
        color="district",
        text="current_rent",
        labels={
            "display_name": "物件",
            "current_rent": "目前月租金",
            "district": "行政區",
        },
        height=430,
    )
    fig.update_traces(texttemplate="NT$%{text:,.0f}", textposition="outside")
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis_tickprefix="NT$",
        yaxis_tickformat=",",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 近期租金風險提醒")

    warning_rows = []
    for prop in PROPERTIES.itertuples():
        rent_df = RENT_HISTORY[RENT_HISTORY["property_id"] == prop.property_id]
        latest_yoy = rent_df["yoy_growth"].dropna().iloc[-1]
        status, badge = get_growth_status(latest_yoy)

        if latest_yoy < 2:
            warning_rows.append(
                {
                    "物件": f"{prop.building} {prop.floor}",
                    "行政區": prop.district,
                    "目前月租金": money(prop.current_rent),
                    "年成長率": pct(latest_yoy),
                    "狀態": status,
                }
            )

    if warning_rows:
        st.dataframe(pd.DataFrame(warning_rows), use_container_width=True, hide_index=True)
    else:
        st.success("目前沒有租金成長異常物件")


# =========================
# Page 2
# =========================
elif page == "客人 DB":
    st.markdown("### 客人 DB")
    st.markdown(
        """
        <div class="info-box">
            客人是提供商辦大樓給公司代租的人，系統支援客人與物件一對一或一對多關聯。
        </div>
        """,
        unsafe_allow_html=True,
    )

    customer_view = CUSTOMERS.copy()
    property_count = PROPERTIES.groupby("customer_id")["property_id"].count().reset_index()
    property_count.columns = ["customer_id", "物件數"]
    customer_view = customer_view.merge(property_count, on="customer_id", how="left")
    customer_view["物件數"] = customer_view["物件數"].fillna(0).astype(int)

    customer_view = customer_view.rename(
        columns={
            "customer_id": "客人ID",
            "customer_name": "客人名稱",
            "contact": "聯絡人",
            "phone": "電話",
            "email": "Email",
            "type": "類型",
            "status": "狀態",
        }
    )

    st.dataframe(customer_view, use_container_width=True, hide_index=True)

    st.markdown("### 客人持有物件關聯")

    selected_customer_name = st.selectbox(
        "選擇客人",
        CUSTOMERS["customer_name"].tolist(),
    )

    selected_customer = CUSTOMERS[CUSTOMERS["customer_name"] == selected_customer_name].iloc[0]
    owned_properties = PROPERTIES[PROPERTIES["customer_id"] == selected_customer["customer_id"]]

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(
            f"""
            <div class="card">
                <div class="table-title">{selected_customer["customer_name"]}</div>
                <hr>
                <div>聯絡人：{selected_customer["contact"]}</div>
                <div>電話：{selected_customer["phone"]}</div>
                <div>Email：{selected_customer["email"]}</div>
                <div>類型：{selected_customer["type"]}</div>
                <br>
                <span class="badge badge-green">{selected_customer["status"]}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        display_df = owned_properties[
            [
                "property_id",
                "building",
                "floor",
                "district",
                "area_ping",
                "current_rent",
                "occupancy",
                "tenant",
            ]
        ].rename(
            columns={
                "property_id": "物件ID",
                "building": "大樓",
                "floor": "樓層",
                "district": "行政區",
                "area_ping": "坪數",
                "current_rent": "目前月租金",
                "occupancy": "狀態",
                "tenant": "承租方",
            }
        )
        st.dataframe(display_df, use_container_width=True, hide_index=True)


# =========================
# Page 3
# =========================
elif page == "物件 DB":
    st.markdown("### 物件 DB")

    property_view = PROPERTIES.merge(
        CUSTOMERS[["customer_id", "customer_name", "contact"]],
        on="customer_id",
        how="left",
    )

    property_view["price_per_ping"] = property_view["current_rent"] / property_view["area_ping"]

    property_view = property_view.rename(
        columns={
            "property_id": "物件ID",
            "customer_name": "客人名稱",
            "contact": "客人聯絡人",
            "building": "大樓",
            "floor": "樓層",
            "unit": "單位",
            "district": "行政區",
            "address": "地址",
            "area_ping": "坪數",
            "current_rent": "目前月租金",
            "price_per_ping": "每坪租金",
            "occupancy": "出租狀態",
            "tenant": "承租方",
        }
    )

    st.dataframe(
        property_view[
            [
                "物件ID",
                "客人名稱",
                "客人聯絡人",
                "大樓",
                "樓層",
                "單位",
                "行政區",
                "坪數",
                "目前月租金",
                "每坪租金",
                "出租狀態",
                "承租方",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### 物件狀態統計")

    status_df = PROPERTIES.groupby("occupancy")["property_id"].count().reset_index()
    status_df.columns = ["出租狀態", "數量"]

    fig = px.pie(
        status_df,
        names="出租狀態",
        values="數量",
        hole=0.55,
        height=420,
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)


# =========================
# Page 4
# =========================
elif page == "單戶租金分析":
    st.markdown("### 單戶租金分析")

    property_options = (
        PROPERTIES["building"]
        + " "
        + PROPERTIES["floor"]
        + "｜"
        + PROPERTIES["district"]
    ).tolist()

    selected_option = st.selectbox("選擇物件", property_options)
    selected_index = property_options.index(selected_option)
    selected_property = PROPERTIES.iloc[selected_index]

    rent_df = RENT_HISTORY[RENT_HISTORY["property_id"] == selected_property["property_id"]].copy()

    latest_rent = rent_df["rent"].iloc[-1]
    prev_rent = rent_df["rent"].iloc[-2]
    mom_growth = ((latest_rent - prev_rent) / prev_rent) * 100
    latest_yoy = rent_df["yoy_growth"].dropna().iloc[-1]
    avg_yoy = rent_df["yoy_growth"].dropna().tail(12).mean()

    status, badge = get_growth_status(latest_yoy)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">目前月租金</div>
                <div class="metric-value">{money(latest_rent)}</div>
                <div class="metric-note">{selected_property["building"]} {selected_property["floor"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        mom_class = "good" if mom_growth >= 0 else "danger"
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">月成長率</div>
                <div class="metric-value {mom_class}">{pct(mom_growth)}</div>
                <div class="metric-note">與上月相比</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        yoy_class = "good" if latest_yoy >= 2 else "danger" if latest_yoy < 0 else "warn"
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">年成長率</div>
                <div class="metric-value {yoy_class}">{pct(latest_yoy)}</div>
                <div class="metric-note">與去年同期相比</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">租金狀態</div>
                <div class="metric-value" style="font-size:22px;">
                    <span class="badge {badge}">{status}</span>
                </div>
                <div class="metric-note">系統自動判斷</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if latest_yoy < 0:
        st.error("警告：此戶租金年成長率為負，建議檢查合約價格、區域行情與出租條件。")
    elif latest_yoy < 2:
        st.warning("提醒：此戶租金年成長率偏低，建議重新評估續約價格或租金調整策略。")
    else:
        st.success("此戶租金成長表現正常。")

    st.markdown("### 每月租金長條圖")

    fig = px.bar(
        rent_df,
        x="month_label",
        y="rent",
        labels={"month_label": "月份", "rent": "月租金"},
        height=460,
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis_tickprefix="NT$",
        yaxis_tickformat=",",
        xaxis=dict(tickangle=-45),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 成長率趨勢")

    growth_df = rent_df.dropna(subset=["yoy_growth"]).copy()

    fig2 = px.line(
        growth_df,
        x="month_label",
        y="yoy_growth",
        markers=True,
        labels={"month_label": "月份", "yoy_growth": "年成長率"},
        height=420,
    )
    fig2.add_hline(y=0, line_dash="dash", annotation_text="負成長線")
    fig2.add_hline(y=2, line_dash="dash", annotation_text="低成長警戒線 2%")
    fig2.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis_ticksuffix="%",
        xaxis=dict(tickangle=-45),
    )
    st.plotly_chart(fig2, use_container_width=True)


# =========================
# Page 5
# =========================
elif page == "AI 價格推薦":
    st.markdown("### AI 價格推薦")

    property_options = (
        PROPERTIES["building"]
        + " "
        + PROPERTIES["floor"]
        + "｜"
        + PROPERTIES["district"]
    ).tolist()

    selected_option = st.selectbox("選擇欲定價物件", property_options)
    selected_index = property_options.index(selected_option)
    selected_property = PROPERTIES.iloc[selected_index]

    nearby_df = NEARBY_MARKET[
        NEARBY_MARKET["district"] == selected_property["district"]
    ].copy()

    rent_df = RENT_HISTORY[
        RENT_HISTORY["property_id"] == selected_property["property_id"]
    ].copy()

    result = ai_recommend_price(selected_property, nearby_df, rent_df)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">目前每坪租金</div>
                <div class="metric-value">{money(result["current_price_per_ping"])}</div>
                <div class="metric-note">目前總租金 {money(selected_property["current_rent"])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">附近平均坪租</div>
                <div class="metric-value">{money(result["market_avg"])}</div>
                <div class="metric-note">{selected_property["district"]} 附近商辦均價</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">AI 建議月租金</div>
                <div class="metric-value good">{money(result["recommended_total"])}</div>
                <div class="metric-note">建議坪租 {money(result["recommended_price_per_ping"])}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="ai-box">
            <h3 style="margin-top:0;">AI 推薦邏輯</h3>
            <p>
                系統會同時參考 <b>該戶歷史租金成長率</b>、<b>附近物件平均坪租</b>、
                <b>附近物件價格成長率</b>、<b>區域空置率</b> 與 <b>目前價格是否低於市場</b>。
            </p>
            <hr>
            <p><b>1. 區域行情：</b>{selected_property["district"]} 附近平均坪租為 {money(result["market_avg"])}。</p>
            <p><b>2. 市場成長：</b>附近物件平均租金成長率為 {pct(result["market_growth"])}。</p>
            <p><b>3. 物件表現：</b>此戶最近年成長率為 {pct(result["latest_yoy"])}。</p>
            <p><b>4. 出租風險：</b>附近平均空置率為 {pct(result["vacancy_rate"])}，空置率越高，建議漲幅越保守。</p>
            <p><b>5. AI 調整：</b>系統建議調整幅度為 {pct(result["adjustment_rate"])}。</p>
            <hr>
            <h4>建議定價區間</h4>
            <p>
                合理月租金區間約為
                <b>{money(result["lower_total"])}</b>
                至
                <b>{money(result["upper_total"])}</b>。
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 附近物件行情比較")

    compare_df = nearby_df.copy()
    compare_df["selected"] = compare_df["building"].apply(
        lambda x: "目前物件" if x == selected_property["building"] else "附近物件"
    )

    fig = px.bar(
        compare_df,
        x="building",
        y="avg_price_per_ping",
        color="selected",
        text="avg_price_per_ping",
        labels={
            "building": "物件",
            "avg_price_per_ping": "平均坪租",
            "selected": "類型",
        },
        height=420,
    )
    fig.update_traces(texttemplate="NT$%{text:,.0f}", textposition="outside")
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis_tickprefix="NT$",
        yaxis_tickformat=",",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### 附近物件資料")

    market_display = nearby_df.rename(
        columns={
            "district": "行政區",
            "building": "附近物件",
            "avg_price_per_ping": "平均坪租",
            "growth_rate": "租金成長率",
            "vacancy_rate": "空置率",
        }
    )

    st.dataframe(market_display, use_container_width=True, hide_index=True)

    st.markdown("### 可落地的 AI 定價公式")

    st.code(
        """
AI 建議租金 = 目前租金 × (1 + 建議調整率)

建議調整率由以下因素組成：

1. 附近物件租金成長率
   - 區域成長率越高，可接受漲幅越高

2. 該戶近一年租金成長率
   - 如果該戶本身成長率高，代表市場接受度佳
   - 如果該戶負成長，系統降低建議價格或發出警告

3. 目前價格與附近均價差距
   - 如果目前坪租低於市場均價 5% 以上，系統建議補漲
   - 如果目前坪租高於市場均價 8% 以上，系統建議保守

4. 區域空置率
   - 空置率越高，代表出租難度越高，價格建議越保守

5. 定價區間保護
   - 最後價格限制在附近均價的 96% 到 108% 之間
   - 避免 AI 推出過高或過低的不合理租金
        """,
        language="text",
    )