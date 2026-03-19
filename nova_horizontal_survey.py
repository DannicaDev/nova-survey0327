import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

# --- 1. 页面配置与邀请函风格适配 ---
st.set_page_config(page_title="AI 进阶路径诊断", layout="wide")

# 强制 CSS：解决乱码风险，优化字号配合，适配世纪公园清新风格
st.markdown("""
    <style>
    .stApp { background-color: #FDFDF5 !important; } /* 米白色背景 */
    html, body, [class*="st-"] { color: #2F4F4F !important; font-family: 'Arial', sans-serif; }
    
    /* 问卷卡片布局优化 */
    [data-testid="stForm"] { 
        background-color: white !important; border-radius: 15px; 
        padding: 30px; border: 1px solid #E0E0E0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }

    /* 解决乱码：图表外的中文用原生 H 标签 */
    h1, h2, h3 { color: #1B5E20 !important; font-family: "Microsoft YaHei", "SimSun", sans-serif; }
    
    /* 龙虾大图标样式 */
    .big-lobster { font-size: 120px; text-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin: 10px 0; }
    
    /* Insight 卡片 */
    .insight-box {
        background: #F1F8E9; border-left: 6px solid #4CAF50;
        padding: 20px; border-radius: 10px; margin-top: 15px;
        font-size: 16px; line-height: 1.6; color: #1B5E20;
    }
    
    /* 看板卡片 */
    .stat-card {
        background: white; border-radius: 10px; padding: 15px;
        text-align: center; border: 1px solid #C3E6CB;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 初始化全局数据 ---
if 'data' not in st.session_state:
    st.session_state.data = {"A": 2, "B": 2, "C": 1}

# --- 3. MiniMax 调用 (带强力兜底) ---
def call_minimax(p, fallback_text):
    api_key = st.secrets.get("MINIMAX_API_KEY")
    if not api_key: return fallback_text
    
    url = f"https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId={st.secrets.get('MINIMAX_GROUP_ID')}"
    payload = {
        "model": "abab6.5-chat",
        "messages": [{"sender_type": "USER", "sender_name": "Consultant", "text": p}],
        "bot_setting": [{"region": "China", "content": "你是一名资深AI战略顾问。"}]
    }
    try:
        r = requests.post(url, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, json=payload, timeout=10)
        return r.json()['reply']
    except:
        return fallback_text

# --- 4. 标题 ---
st.title("🦞 小龙虾时代 · 企业 AI 进阶全景诊断")
st.markdown("##### 世纪公园 · 一尺花园分享会专属版")

tab1, tab2 = st.tabs(["📋 个人诊断", "📊 现场洞察看板"])

with tab1:
    col_left, col_right = st.columns([6, 4])
    
    with col_left:
        with st.form("survey"):
            st.markdown("### 🧬 核心测评维度")
            # 采用 2x4 布局填充空间
            c1, c2 = st.columns(2)
            with c1:
                q1 = st.radio("1. 公有云 AI 使用态度", ["A. 效率优先", "B. 稳健监管", "C. 严格受控"])
                q2 = st.radio("2. 核心数据访问要求", ["A. 结果导向", "B. 大厂托管", "C. 物理不出场"])
                q3 = st.radio("3. 数据归属权倾向", ["A. 无所谓", "B. 合同约定", "C. 必须私有"])
                q4 = st.radio("4. AI 解决问题的深度", ["A. 文字润色", "B. 流程协同", "C. 核心决策"])
            with c2:
                q5 = st.radio("5. 操作习惯与界面", ["A. 灵活多变", "B. 统一标准", "C. 私有定制"])
                q6 = st.radio("6. 智能体矩阵预期", ["A. 个体使用", "B. 组织统筹", "C. 集群作战"])
                q7 = st.radio("7. 采购价值取向", ["A. 低门槛尝试", "B. 长期基建", "C. 价值溢价"])
                q8 = st.radio("8. 部署掌控感要求", ["A. 使用者", "B. 生态跟随", "C. 最高主权"])
            
            st.markdown("<br>", unsafe_allow_html=True)
            submitted = st.form_submit_button("🌱 提交诊断并生成洞察")

    with col_right:
        # 实时判定
        all_qs = [q1, q2, q3, q4, q5, q6, q7, q8]
        c_count = sum(1 for x in all_qs if "C." in x)
        
        # 视觉展示 - 使用 Emoji 解决图出不来的问题
        if c_count >= 5:
            icon, name, color, tag = "🦀", "殿堂·帝王蟹 (ME7)", "#0078D4", "CRAB"
        elif c_count >= 2:
            icon, name, color, tag = "🦞", "进阶·大龙虾 (Nova)", "#FF8C00", "BIG LOBSTER"
        else:
            icon, name, color, tag = "🦐", "敏捷·小龙虾 (OpenClaw)", "#FF4B4B", "SMALL LOBSTER"
        
        st.markdown(f"""
            <div style="background:white; border-radius:15px; padding:30px; text-align:center; border:2px solid {color};">
                <div class="big-lobster">{icon}</div>
                <h2 style="color:{color}; margin:0;">{name}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        if submitted:
            # 1. 雷达图 (英文标签避开乱码)
            res = {"A": sum(1 for x in all_qs if "A." in x), 
                   "B": sum(1 for x in all_qs if "B." in x), 
                   "C": c_count}
            
            fig_radar = go.Figure(data=go.Scatterpolar(
                r=[res["A"], res["B"], res["C"]],
                theta=['Agile(A)', 'Collab(B)', 'Sovereignty(C)'],
                fill='toself', line_color=color
            ))
            fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 8])), height=250, margin=dict(l=40,r=40,t=20,b=20))
            st.plotly_chart(fig_radar, use_container_width=True)
            
            # 2. 个人洞见
            fb = f"您的企业属于{name}路径。建议：强化数据主权，关注Nova Claw私有化部署。"
            insight = call_minimax(f"企业诊断为{name}，请给三条AI进阶建议", fb)
            st.markdown(f'<div class="insight-box"><strong>🤖 专属洞察：</strong><br>{insight}</div>', unsafe_allow_html=True)
            
            # 更新全局
            st.session_state.data[final_key := ("C" if c_count >= 5 else ("B" if c_count >= 2 else "A"))] += 1
            st.balloons()

with tab2:
    st.header("📊 现场调研实时看板")
    total = sum(st.session_state.data.values())
    
    # 三列排版
    kpi1, kpi2, kpi3 = st.columns([3, 4, 3])
    
    with kpi1:
        st.markdown(f'<div class="stat-card"><h5>参与人数</h5><div class="stat-val">{total}</div></div>', unsafe_allow_html=True)
        st.write("")
        st.markdown(f"""
            - 🦐 小龙虾: **{st.session_state.data['A']}**
            - 🦞 大龙虾: **{st.session_state.data['B']}**
            - 🦀 帝王蟹: **{st.session_state.data['C']}**
        """)

    with kpi2:
        # 环形图：手动配色 + 大字号
        fig_pie = px.pie(
            names=['OpenClaw (A)', 'Nova (B)', 'ME7 (C)'], # 英文名避乱码
            values=[st.session_state.data["A"], st.session_state.data["B"], st.session_state.data["C"]],
            color_discrete_sequence=['#FF4B4B', '#FF8C00', '#0078D4'],
            hole=0.5
        )
        fig_pie.update_traces(textinfo='percent+label', textfont_size=18) # 调大字体
        fig_pie.update_layout(showlegend=False, height=350, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    with kpi3:
        st.markdown("### 🏛️ 现场趋势分析")
        g_fb = "当前现场以主权型需求为主，建议关注私有化Agent矩阵。"
        g_insight = call_minimax(f"现场数据 A:{st.session_state.data['A']} B:{st.session_state.data['B']} C:{st.session_state.data['C']}，请分析趋势", g_fb)
        st.info(g_insight)
        
        st.markdown("""
        **🎁 特别环节提示**
        * 现场有机会抽取 **Mac Mini**
        * 优先加入 **“大龙虾计划”** 首批公测
        """)
