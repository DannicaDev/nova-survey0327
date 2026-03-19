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
    button[data-baseweb="tab"] { font-size: 26px !important; font-weight: 700 !important; color: #1B5E20 !important; }
    /* 问卷文字字号 */
    .stRadio label { font-size: 19px !important; font-weight: 500 !important; color: #2C3E50 !important; }
    /* 结果卡片 */
    .res-card { background: white; border-radius: 20px; padding: 30px; border: 2px solid #E0E0E0; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
    .big-icon { font-size: 100px; margin-bottom: 10px; }
    /* 洞见卡片 */
    .insight-box { background: linear-gradient(135deg, #F1F8E9 0%, #DCEDC8 100%); border-left: 8px solid #4CAF50; padding: 25px; border-radius: 12px; font-size: 18px; line-height: 1.6; color: #1B5E20; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 数据初始化 (Session State) ---
if 'counts' not in st.session_state:
    st.session_state.counts = {"A": 5, "B": 3, "C": 2} # 初始数据让看板不为空
if 'my_insight' not in st.session_state:
    st.session_state.my_insight = None
if 'my_scores' not in st.session_state:
    st.session_state.my_scores = {"敏捷": 0, "协同": 0, "主权": 0}

# --- 3. 核心 API 调用函数 (带诊断逻辑) ---
def get_ai_content(prompt, fallback):
    # 优先检查 Secrets
    api_key = st.secrets.get("MINIMAX_API_KEY")
    group_id = st.secrets.get("MINIMAX_GROUP_ID")
    
    if not api_key:
        return f"💡 **[专家预设洞察]**\n\n{fallback}"

    url = f"https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId={group_id}"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "abab6.5-chat",
        "messages": [{"sender_type": "USER", "sender_name": "访客", "text": prompt}],
        "bot_setting": [{"region": "China", "content": "你是一位专业的AI战略顾问。"}]
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=10)
        # 兼容不同版本的返回格式
        data = r.json()
        if 'reply' in data: return data['reply']
        if 'choices' in data: return data['choices'][0]['text']
        return fallback
    except:
        return fallback

# --- 4. 主界面布局 ---
st.title("🌿 小龙虾时代 · 企业 AI 进阶路径全景诊断")
st.markdown("#### 世纪公园 · 一尺花园分享会 | 寻找您的数字化进化终点")

tab1, tab2 = st.tabs(["📋 个人评测", "📊 现场看板"])

with tab1:
    l, r = st.columns([6, 4], gap="large")
    
    with l:
        with st.form("main_form"):
            st.markdown("### 🧬 核心维度探测")
            # 双列填充留白
            q1_col, q2_col = st.columns(2)
            with q1_col:
                v1 = st.radio("1. 公有云 AI 态度", ["A. 效率优先", "B. 稳健监管", "C. 严格禁入"])
                v2 = st.radio("2. 核心数据访问", ["A. 结果导向", "B. 大厂托管", "C. 物理不出场"])
                v3 = st.radio("3. 数据归属权", ["A. 无所谓", "B. 合同约定", "C. 必须私有"])
                v4 = st.radio("4. 场景复杂度", ["A. 基础办公", "B. 流程协同", "C. 核心逻辑"])
            with q2_col:
                v5 = st.radio("5. 定制化要求", ["A. 标准化界面", "B. 模块化配置", "C. 深度定制"])
                v6 = st.radio("6. Agent 预期", ["A. 零散工具", "B. 组织统筹", "C. 智能矩阵"])
                v7 = st.radio("7. 采购核心价值", ["A. 试错优先", "B. 长期配置", "C. 价值与安全"])
                v8 = st.radio("8. 掌控感要求", ["A. 使用者", "B. 跟随者", "C. 最高主权"])
            
            submitted = st.form_submit_button("🌱 立即开启 AI 诊断报告")

    with r:
        # 计算结果
        ans = [v1, v2, v3, v4, v5, v6, v7, v8]
        c_count = sum(1 for x in ans if "C." in x)
        
        if c_count >= 5:
            icon, name, color = "🦀", "殿堂·帝王蟹 (ME7)", "#1565C0"
        elif c_count >= 2:
            icon, name, color = "🦞", "进阶·大龙虾 (Nova)", "#EF6C00"
        else:
            icon, name, color = "🦐", "敏捷·小龙虾 (OpenClaw)", "#C62828"

        # 结果展示
        st.markdown(f"""
            <div class="res-card" style="border-top: 10px solid {color};">
                <div class="big-icon">{icon}</div>
                <h2 style="color:{color}; margin:0;">{name}</h2>
            </div>
        """, unsafe_allow_html=True)

        if submitted:
            # 更新状态
            st.session_state.counts["C" if c_count >= 5 else ("B" if c_count >= 2 else "A")] += 1
            st.session_state.my_scores = {
                "敏捷": sum(1 for x in ans if "A." in x),
                "协同": sum(1 for x in ans if "B." in x),
                "主权": c_count
            }
            # 调用 AI
            p = f"诊断结果为{name}。请根据数据主权{v1}和定制化{v5}给出3条建议。"
            f = f"您的企业已进入{name}阶段。当前核心任务是确立‘数据主权’边界，建议优先将核心业务场景进行私有化 Agent 封装，实现智慧资产的永久留存。"
            with st.spinner("AI 顾问正在生成洞察..."):
                st.session_state.my_insight = get_ai_content(p, f)
            st.balloons()

        # --- 渲染能量条 (高级感替代三维图) ---
        if st.session_state.my_scores["敏捷"] + st.session_state.my_scores["主权"] > 0:
            st.markdown("#### ⚡ 进阶维度能量分布")
            fig = go.Figure(go.Bar(
                x=[st.session_state.my_scores[k] for k in ["敏捷", "协同", "主权"]],
                y=["Agile", "Collab", "Sovereign"],
                orientation='h', marker_color=color, text=[st.session_state.my_scores[k] for k in ["敏捷", "协同", "主权"]], textposition='auto'
            ))
            fig.update_layout(height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(range=[0,8], visible=False), yaxis=dict(autorange="reversed"))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # --- 专家洞见持久化显示 ---
        if st.session_state.my_insight:
            st.markdown(f'<div class="insight-box"><strong>🏛️ 专家建议：</strong><br>{st.session_state.my_insight}</div>', unsafe_allow_html=True)

with tab2:
    st.header("📊 现场实时洞察看板")
    c = st.session_state.counts
    tot = sum(c.values())
    
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("参与人数", tot)
    k2.metric("小龙虾(A)", c["A"])
    k3.metric("大龙虾(B)", c["B"])
    k4.metric("帝王蟹(C)", c["C"])

    if tot > 0:
        st.write("---")
        gl, gr = st.columns(2)
        with gl:
            fig_p = px.pie(names=['OpenClaw (A)', 'Nova (B)', 'ME7 (C)'], values=[c["A"], c["B"], c["C"]],
                           color_discrete_sequence=['#C62828', '#EF6C00', '#1565C0'], hole=0.5)
            fig_p.update_traces(textinfo='percent+label', textfont_size=20)
            st.plotly_chart(fig_p, use_container_width=True)
        with gr:
            st.markdown("### 🏛️ 全场趋势解析")
            if st.button("🛰️ 扫描现场全景"):
                gp = f"现场数据 A:{c['A']} B:{c['B']} C:{c['C']}。请分析管理者焦虑点。"
                gf = "现场数据显示，**主权意识（C型）** 正在成为主流。这标志着管理者已从单纯追求效率，转向追求数字化资产的深度自持。"
                with st.spinner("AI 分析中..."):
                    st.success(get_ai_content(gp, gf))
            st.info("🎁 提示：现场将抽取 **Mac Mini**，请确保已提交个人评测。")
