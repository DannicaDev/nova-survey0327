import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

# --- 1. 页面配置 ---
st.set_page_config(page_title="AI 进阶路径诊断", layout="wide")

# --- 2. 增强版 CSS (适配世纪公园清新风格 + 解决排版) ---
st.markdown("""
    <style>
    .stApp { background-color: #FDFDF5 !important; }
    h1, h2, h3 { color: #1B5E20 !important; font-family: "Microsoft YaHei", sans-serif; }
    [data-testid="stForm"] { background-color: white !important; border-radius: 15px; padding: 30px; border: 1px solid #E0E0E0; }
    .big-icon { font-size: 100px; margin: 10px 0; }
    /* 专家洞见卡片样式 - 确保显眼 */
    .insight-box {
        background: #E8F5E9; border-left: 6px solid #4CAF50;
        padding: 20px; border-radius: 10px; margin-top: 20px;
        color: #1B5E20; font-size: 16px; line-height: 1.6;
    }
    .stat-card { background: white; border-radius: 10px; padding: 15px; text-align: center; border: 1px solid #C3E6CB; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 初始化持久化数据 ---
if 'group_counts' not in st.session_state:
    st.session_state.group_counts = {"A": 2, "B": 2, "C": 1}
if 'personal_insight' not in st.session_state:
    st.session_state.personal_insight = None

# --- 4. MiniMax 调用函数 (带超强兜底) ---
def get_ai_insight(prompt, fallback):
    api_key = st.secrets.get("MINIMAX_API_KEY")
    if not api_key: return fallback
    url = f"https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId={st.secrets.get('MINIMAX_GROUP_ID')}"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": "abab6.5-chat",
        "messages": [{"sender_type": "USER", "sender_name": "Consultant", "text": prompt}],
        "bot_setting": [{"region": "China", "content": "你是一位资深AI架构师，擅长根据企业数据主权和业务复杂度提供建议。"}]
    }
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=12)
        return r.json()['reply']
    except:
        return fallback

# --- 5. 标题 ---
st.title("🌿 小龙虾时代 · 企业 AI 进阶诊断")
st.markdown("##### 欢迎来到一尺花园分享会 | 寻找您的企业 AI 进化路径")

t1, t2 = st.tabs(["📋 个人评测", "📊 现场看板"])

with t1:
    col_left, col_right = st.columns([6, 4])
    
    with col_left:
        with st.form("survey_form"):
            st.markdown("### 🧬 核心维度测评")
            # 双列布局解决留白
            q_left, q_right = st.columns(2)
            with q_left:
                v1 = st.radio("1. 公有云使用态度", ["A. 效率优先", "B. 稳健监管", "C. 严格禁入"])
                v2 = st.radio("2. 核心数据访问", ["A. 结果导向", "B. 大厂托管", "C. 物理不出场"])
                v3 = st.radio("3. 数据所有权", ["A. 无所谓", "B. 合同约定", "C. 必须私有"])
                v4 = st.radio("4. 解决问题深度", ["A. 基础办公", "B. 业务协同", "C. 核心逻辑"])
            with q_right:
                v5 = st.radio("5. 个性化界面", ["A. 标准化", "B. 模块化", "C. 深度定制"])
                v6 = st.radio("6. Agent预期", ["A. 零散工具", "B. 组织统筹", "C. 智能矩阵"])
                v7 = st.radio("7. 采购倾向", ["A. 试错优先", "B. 长期配置", "C. 价值与安全"])
                v8 = st.radio("8. 掌控感要求", ["A. 使用者", "B. 跟随者", "C. 主权者"])
            
            submit_btn = st.form_submit_button("🌱 提交并开启 AI 诊断")

    with col_right:
        # 结果计算逻辑
        all_vals = [v1, v2, v3, v4, v5, v6, v7, v8]
        c_num = sum(1 for x in all_vals if "C." in x)
        
        if c_num >= 5:
            icon, name, color = "🦀", "殿堂·帝王蟹 (ME7)", "#0078D4"
        elif c_num >= 2:
            icon, name, color = "🦞", "进阶·大龙虾 (Nova)", "#FF8C00"
        else:
            icon, name, color = "🦐", "敏捷·小龙虾 (OpenClaw)", "#FF4B4B"

        # 始终显示的视觉卡片
        st.markdown(f"""
            <div style="background:white; border-radius:15px; padding:30px; text-align:center; border:2px solid {color}; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                <div class="big-icon">{icon}</div>
                <h2 style="color:{color}; margin:0;">{name}</h2>
            </div>
        """, unsafe_allow_html=True)

        if submit_btn:
            # 1. 更新全局统计
            key = "C" if c_num >= 5 else ("B" if c_num >= 2 else "A")
            st.session_state.group_counts[key] += 1
            
            # 2. 调用 AI 并存入 session_state 确保不丢失
            prompt = f"企业诊断结果为{name}，核心诉求是：{v1}, {v2}, {v4}。请给出3条专业的AI进阶建议，150字以内。"
            fallback = f"【专家建议】：您的企业属于{name}模式。当前应重点关注数据主权边界，建议分步推进私有化 Agent 部署，确保核心资产不出场。"
            
            with st.spinner("专家正在生成深度洞察..."):
                st.session_state.personal_insight = get_ai_insight(prompt, fallback)
            st.balloons()

        # 3. 渲染专家洞见 (只要有数据就显示，不管是不是刚点完提交)
        if st.session_state.personal_insight:
            st.markdown(f"""
                <div class="insight-box">
                    <strong>🤖 大模型专家洞察：</strong><br>
                    {st.session_state.personal_insight}
                </div>
            """, unsafe_allow_html=True)
            
            # 雷达图 (英文标签避乱码)
            scores = {"Agile": sum(1 for x in all_vals if "A." in x), 
                      "Collab": sum(1 for x in all_vals if "B." in x), 
                      "Sovereignty": c_num}
            fig_r = go.Figure(data=go.Scatterpolar(
                r=list(scores.values()), theta=list(scores.keys()), fill='toself', line_color=color
            ))
            fig_r.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 8])), height=250, margin=dict(l=40,r=40,t=30,b=30))
            st.plotly_chart(fig_r, use_container_width=True)

with t2:
    st.header("📊 现场实时洞察看板")
    counts = st.session_state.group_counts
    total = sum(counts.values())
    
    # 顶部 KPI
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f'<div class="stat-card">人数<br><span style="font-size:30px;font-weight:bold;">{total}</span></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="stat-card">小龙虾(A)<br><span style="font-size:30px;font-weight:bold;color:#FF4B4B;">{counts["A"]}</span></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="stat-card">大龙虾(B)<br><span style="font-size:30px;font-weight:bold;color:#FF8C00;">{counts["B"]}</span></div>', unsafe_allow_html=True)
    k4.markdown(f'<div class="stat-card">帝王蟹(C)<br><span style="font-size:30px;font-weight:bold;color:#0078D4;">{counts["C"]}</span></div>', unsafe_allow_html=True)

    if total > 0:
        st.markdown("---")
        g_left, g_right = st.columns([5, 5])
        
        with g_left:
            # 环形图适配大字号和专业色
            fig_p = px.pie(
                names=['OpenClaw (A)', 'Nova (B)', 'ME7 (C)'],
                values=[counts["A"], counts["B"], counts["C"]],
                color_discrete_sequence=['#FF4B4B', '#FF8C00', '#0078D4'],
                hole=0.45
            )
            fig_p.update_traces(textinfo='percent+label', textfont_size=18)
            fig_p.update_layout(showlegend=False, height=400)
            st.plotly_chart(fig_p, use_container_width=True)
            
        with g_right:
            st.markdown("### 🏛️ 现场群体趋势分析")
            if st.button("生成现场实时洞察"):
                g_prompt = f"现场数据 A:{counts['A']}, B:{counts['B']}, C:{counts['C']}。请简要分析现场管理者的AI焦虑点和进阶机会。"
                g_fallback = "现场数据显示，管理者对**数据主权与定制化能力**（B/C型）表现出极高关注。这与‘大龙虾计划’的核心价值高度契合。"
                with st.spinner("AI正在扫描现场全景..."):
                    g_res = get_ai_insight(g_prompt, g_fallback)
                    st.info(g_res)
            else:
                st.write("点击上方按钮，获取 AI 对全场趋势的深度解析。")
            
            st.success("🎁 提示：优先提交问卷可获得“大龙虾计划”首批测试名额，现场将随机抽取 Mac Mini！")
