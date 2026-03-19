import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests

# --- 1. 页面配置与高级感 CSS ---
st.set_page_config(page_title="AI 进阶路径诊断", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #F8FAF8 !important; }
    /* 放大 Tab 标签 */
    button[data-baseweb="tab"] { font-size: 24px !important; font-weight: 700 !important; color: #1B5E20 !important; }
    
    /* 结果卡片 */
    .res-card { 
        background: white; border-radius: 20px; padding: 30px; 
        border: 2px solid #E0E0E0; text-align: center; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); 
    }
    .big-icon { font-size: 100px; margin-bottom: 10px; }
    
    /* 专家洞见卡片：深度排版优化 */
    .insight-box { 
        background: linear-gradient(135deg, #F1F8E9 0%, #E8F5E9 100%); 
        border-left: 8px solid #4CAF50; padding: 25px; 
        border-radius: 12px; font-size: 17px; line-height: 1.8; 
        color: #1B5E20; margin-top: 20px;
        white-space: pre-wrap; /* 允许换行 */
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 数据初始化 ---
if 'counts' not in st.session_state:
    st.session_state.counts = {"A": 3, "B": 2, "C": 1}
if 'saved_insight' not in st.session_state:
    st.session_state.saved_insight = None
if 'saved_scores' not in st.session_state:
    st.session_state.saved_scores = {"敏捷": 0, "协同": 0, "主权": 0}

# --- 3. 深度 AI 调用函数 ---
def get_pro_insight(prompt, fallback):
    api_key = st.secrets.get("MINIMAX_API_KEY")
    if not api_key: return fallback
    url = "https://api.minimax.chat/v1/text/chatcompletion_v2"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "abab6.5-chat",
        "messages": [
            {"role": "system", "content": "你是一位资深AI战略顾问。请提供深度、长篇且排版优雅的专业分析，包含背景、痛点和三条具体的落地建议。"},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 800 # 确保长版本输出
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=20)
        return r.json()['choices'][0]['message']['content']
    except:
        return fallback

# --- 4. 主界面布局 ---
st.title("🌿 小龙虾时代 · 企业 AI 进阶诊断")
st.markdown("#### 世纪公园 · 一尺花园分享会 | NovaClaw 创始计划")

t_personal, t_group = st.tabs(["📋 个人评测", "📊 现场看板"])

with t_personal:
    l, r = st.columns([6, 4], gap="large")
    
    with l:
        with st.form("survey_form"):
            st.markdown("### 🧬 核心维度探测")
            q1_col, q2_col = st.columns(2)
            with q1_col:
                v1 = st.radio("1. 公有云使用态度", ["A. 效率优先", "B. 稳健监管", "C. 严格禁入"])
                v2 = st.radio("2. 核心数据访问", ["A. 结果导向", "B. 大厂托管", "C. 物理不出场"])
                v3 = st.radio("3. 数据所有权", ["A. 无所谓", "B. 合同约定", "C. 必须私有"])
                v4 = st.radio("4. 解决问题深度", ["A. 基础办公", "B. 业务协同", "C. 核心逻辑"])
            with q2_col:
                v5 = st.radio("5. 个性化界面", ["A. 标准化", "B. 模块化", "C. 深度定制"])
                v6 = st.radio("6. Agent预期", ["A. 零散工具", "B. 组织统筹", "C. 智能矩阵"])
                v7 = st.radio("7. 采购倾向", ["A. 试错优先", "B. 长期配置", "C. 价值与安全"])
                v8 = st.radio("8. 掌控感要求", ["A. 使用者", "B. 跟随者", "C. 主权者"])
            submit = st.form_submit_button("🌱 立即开启深度诊断报告")

    with r:
        ans = [v1, v2, v3, v4, v5, v6, v7, v8]
        c_val = sum(1 for x in ans if "C." in x)
        
        if c_val >= 5:
            icon, name, color = "🦀", "殿堂·帝王蟹 (ME7)", "#1565C0"
        elif c_val >= 2:
            icon, name, color = "🦞", "进阶·大龙虾 (NovaClaw)", "#EF6C00"
        else:
            icon, name, color = "🦐", "敏捷·小龙虾 (OpenClaw)", "#C62828"

        st.markdown(f"""
            <div class="res-card" style="border-top: 10px solid {color};">
                <div class="big-icon">{icon}</div>
                <h2 style="color:{color}; margin:0;">{name}</h2>
            </div>
        """, unsafe_allow_html=True)

        if submit:
            # 更新 Session 状态
            key = "C" if c_val >= 5 else ("B" if c_val >= 2 else "A")
            st.session_state.counts[key] += 1
            st.session_state.saved_scores = {
                "敏捷": sum(1 for x in ans if "A." in x),
                "协同": sum(1 for x in ans if "B." in x),
                "主权": c_val
            }
            # AI 深度长文案
            p = f"诊断结果为{name}。请给出深度分析，特别是针对{v3}和{v8}的情况，分点陈述建议。"
            f = f"【专家深度诊断报告】\n\n您的企业属于**{name}**级别，这表明您在数字化转型中极度重视资产的自持与安全。\n\n**建议落地路径：**\n1. **主权隔离**：针对{v3}，建议优先部署本地化算力中心，实现核心数据物理不出场。\n2. **定制化 Agent**：利用 NovaClaw 框架封装高频业务逻辑。\n3. **长期基建**：将 AI 视为企业无形资产，而不只是提效工具。"
            with st.spinner("AI 首席顾问正在撰写长篇诊断报告..."):
                st.session_state.saved_insight = get_pro_insight(p, f)
            st.balloons()

        # --- 能量图 (保留并美化) ---
        if sum(st.session_state.saved_scores.values()) > 0:
            st.markdown("#### ⚡ 进阶维度能量分布")
            s = st.session_state.saved_scores
            fig = go.Figure(go.Bar(
                x=[s["敏捷"], s["协同"], s["主权"]],
                y=["Agile", "Collab", "Sovereign"],
                orientation='h', marker_color=color,
                text=[s["敏捷"], s["协同"], s["主权"]], textposition='auto'
            ))
            fig.update_layout(height=180, margin=dict(l=0,r=20,t=0,b=0), xaxis=dict(range=[0,8], visible=False), yaxis=dict(autorange="reversed"), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # --- 长版本专家洞见渲染 ---
        if st.session_state.saved_insight:
            st.markdown(f"""
                <div class="insight-box">
                    <strong>🏛️ 首席顾问深度 Insight：</strong><br><br>
                    {st.session_state.saved_insight}
                </div>
            """, unsafe_allow_html=True)

with t_group:
    st.header("📊 现场实时洞察看板")
    c = st.session_state.counts
    total = sum(c.values())
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("总参与人数", total)
    k2.metric("小龙虾(A)", c["A"])
    k3.metric("大龙虾(B)", c["B"])
    k4.metric("帝王蟹(C)", c["C"])

    if total > 0:
        st.write("---")
        gl, gr = st.columns(2)
        with gl:
            fig_pie = px.pie(names=['OpenClaw', 'NovaClaw', 'ME7'], values=[c["A"], c["B"], c["C"]],
                           color_discrete_sequence=['#C62828', '#EF6C00', '#1565C0'], hole=0.5)
            fig_pie.update_traces(textinfo='percent+label', textfont_size=20)
            st.plotly_chart(fig_pie, use_container_width=True)
        with gr:
            st.markdown("### 🏛️ 现场全景解析")
            if st.button("🛰️ 扫描现场 AI 进化趋势"):
                # 强化版群体分析 Prompt
                gp = (
                    f"现场数据汇总：敏捷型(A):{c['A']}人，协同型(B):{c['B']}人，主权型(C):{c['C']}人。总计{total}位决策者。 "
                    "请作为首席AI战略顾问，给出一段极具煽动性且深刻的现场趋势分析。要求：\n"
                    "1. 分析当前群体表现出的‘管理焦虑’与‘技术渴望’之间的矛盾；\n"
                    "2. 针对主权意识的觉醒（C型）给出独家见解；\n"
                    "3. 预测未来12个月内，现场企业在 NovaClaw 这种私有化 Agent 上的潜在投入方向。\n"
                    "排版请使用：【现状透视】、【深度逻辑】、【行动指南】三个版块。"
                )
                with st.spinner("正在对全场数据进行多维建模分析..."):
                    grand_insight = get_pro_insight(gp, "全场数据表明，主权意识正在成为管理层的核心诉求。建议关注本地算力与 NovaClaw 的结合。")
                    st.markdown(f'<div class="insight-box">{grand_insight}</div>', unsafe_allow_html=True)
            st.info("🎁 提示：现场将随机抽取 **Mac Mini**，其本地算力正是实现‘主权级 AI’的物理基石。")
