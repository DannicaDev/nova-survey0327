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
        
        # 判定逻辑
        if c_val >= 5:
            icon, name, color = "🦀", "殿堂·帝王蟹 (ME7)", "#1565C0"
        elif c_val >= 2:
            icon, name, color = "🦞", "进阶·大龙虾 (NovaClaw)", "#EF6C00"
        else:
            icon, name, color = "🦐", "敏捷·小龙虾 (OpenClaw)", "#C62828"

        # --- 第一层：结果与能量图并排（横向压缩空间） ---
        st.markdown(f"""
            <div style="background:white; border-radius:15px; padding:15px; border:1px solid #E0E0E0; margin-bottom:15px; display: flex; align-items: center; justify-content: space-around;">
                <div style="text-align:center;">
                    <div style="font-size: 55px;">{icon}</div>
                    <div style="color:{color}; font-weight:bold; font-size:16px;">{name}</div>
                </div>
                <div style="width: 2px; height: 60px; background-color: #EEE;"></div>
                <div style="flex-grow: 1; margin-left: 20px;">
                    <p style="font-size:12px; color:#666; margin:0 0 5px 0;">进化维度能量分布</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # 在并排卡片中嵌入能量图
        # 这里通过 style 往回找位置，或者直接用下面的渲染方式：
        s = {"敏捷": sum(1 for x in ans if "A." in x), "协同": sum(1 for x in ans if "B." in x), "主权": c_val}
        fig = go.Figure(go.Bar(
            x=[s["敏捷"], s["协同"], s["主权"]],
            y=["Agile", "Collab", "Sovereign"],
            orientation='h', marker_color=color, text=[s["敏捷"], s["协同"], s["主权"]], textposition='inside'
        ))
        fig.update_layout(height=120, margin=dict(l=0,r=10,t=0,b=0), xaxis=dict(visible=False), yaxis=dict(autorange="reversed"), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        if submit:
            key = "C" if c_val >= 5 else ("B" if c_val >= 2 else "A")
            st.session_state.counts[key] += 1
            # 强化 Prompt
            p = f"诊断结果为{name}。请提供一份深刻的【首席顾问深度 Insight】，包含：1. 现状评估；2. 针对数据主权的落地建议；3. 长期数字化基建愿景。要求总字数约400字，分段清晰。"
            with st.spinner("AI 正在深度建模中..."):
                st.session_state.saved_insight = get_pro_insight(p, "正在为您规划{name}级别的进化路径...")
            st.balloons()

        # --- 第二层：内嵌滚动条的 Insight 区域 ---
        if st.session_state.saved_insight:
            st.markdown(f"""
                <div style="background: #E8F5E9; border-left: 6px solid #4CAF50; border-radius: 10px; padding: 20px; 
                            max-height: 480px; overflow-y: auto; color: #1B5E20;">
                    <h4 style="margin:0 0 15px 0;">🏛️ 首席顾问深度 Insight</h4>
                    <div style="line-height: 1.8; font-size: 16px; white-space: pre-wrap;">{st.session_state.saved_insight}</div>
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
            with gr:
            st.markdown("### 🏛️ 现场全景趋势分析")
            if st.button("🛰️ 启动全场 AI 进化扫描"):
                # 终极深度 Prompt
                gp = (
                    f"现场数据：A:{c['A']}人，B:{c['B']}人，C:{c['C']}人。总样本{total}。 "
                    "请作为首席数字化战略官提供深度报告。必须包含以下三个板块：\n"
                    "【现状透视】：分析为何现场管理者普遍处于‘效率与主权’的权衡期，解读数据背后隐藏的群体焦虑。\n"
                    "【深度逻辑】：剖析从 OpenClaw 迈向 NovaClaw 的本质是‘业务资产化’，解释主权意识（C型）为何是未来三年的胜负手。\n"
                    "【行动指南】：针对当前数据比例，预测未来12个月的算力投入重心。提及 Mac Mini 作为边缘主权算力的战略地位。\n"
                    "要求字数充实，观点犀利且富有启发性。"
                )
                with st.spinner("正在融合全场数据，生成战略白皮书..."):
                    grand_insight = get_pro_insight(gp, "全场数据正在解析中...")
                    st.markdown(f"""
                        <div style="background: #F1F8E9; border-radius: 15px; padding: 25px; border-top: 5px solid #1B5E20; margin-top:10px; line-height: 1.9; white-space: pre-wrap;">
                            {grand_insight}
                        </div>
                    """, unsafe_allow_html=True)
            st.success("现场演示 Tip：若主权型(C)占比较高，暗示现场观众更倾向于私有化 Agent 部署。")
