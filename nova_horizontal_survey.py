import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

# --- 1. 页面配置 ---
st.set_page_config(page_title="AI 进阶路径诊断 | 现场版", page_icon="🌿", layout="wide")

# 强制深色文字 CSS
st.markdown("""
    <style>
    .stApp { background-color: #F0F9F0 !important; }
    html, body, [class*="st-"] { color: #155724 !important; font-family: 'Segoe UI', sans-serif; }
    [data-testid="stForm"] { background-color: white !important; border-radius: 20px; padding: 30px; border: 1px solid #C3E6CB; }
    .stat-card { background: white; border-radius: 10px; padding: 15px; text-align: center; border-top: 5px solid #28a745; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .stat-val { font-size: 36px; font-weight: bold; color: #155724; }
    .visual-panel { background: white !important; border-radius: 20px; padding: 20px; text-align: center; border: 2px solid #28a745; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 初始化全局数据 (保存在服务器内存) ---
if 'group_data' not in st.session_state:
    # 预设一些基础数据防止绘图报错，你可以根据需要调整或设为 0
    st.session_state.group_data = {"A": 1, "B": 1, "C": 1}

# --- 3. MiniMax 定义 ---
def ask_minimax(prompt_text):
    api_key = st.secrets.get("MINIMAX_API_KEY")
    group_id = st.secrets.get("MINIMAX_GROUP_ID")
    if not api_key: return "（未配置 API Key，无法生成动态 Insight）"
    
    url = f"https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId={group_id}"
    payload = {
        "model": "abab6.5-chat",
        "messages": [{"sender_type": "USER", "sender_name": "User", "text": prompt_text}],
        "bot_setting": [{"region": "China", "content": "你是一名资深 AI 战略专家。"}]
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        r = requests.post(url, headers=headers, json=payload)
        return r.json()['reply']
    except: return "AI 专家正在休假中..."

# --- 4. 主体布局 ---
st.title("🌿 春启新程 · AI 进阶路径诊断")

tab1, tab2 = st.tabs(["📋 个人诊断", "📊 现场洞察"])

with tab1:
    l, r = st.columns([6, 4])
    with l:
        with st.form("my_form"):
            st.markdown("### 第一部分：安全边界")
            q1 = st.radio("1. 公有云 AI 使用态度？", ["A. 效率优先", "B. 担忧合规", "C. 严格禁入"])
            q2 = st.radio("2. 核心数据访问要求？", ["A. 结果导向", "B. 大厂托管", "C. 物理不出场"])
            q3 = st.radio("3. 数据归属权？", ["A. 无所谓", "B. 合同约定", "C. 必须私有"])
            
            st.markdown("### 第二部分：业务深度")
            q4 = st.radio("4. AI 解决的问题？", ["A. 基础文字", "B. 流程协同", "C. 深度逻辑/API"])
            q5 = st.radio("5. 个性化要求？", ["A. 灵活多变", "B. 界面统一", "C. 专属定制"])
            q6 = st.radio("6. Agent 数量预期？", ["A. 零散个体", "B. 组织统筹", "C. 集群矩阵"])
            
            st.markdown("### 第三部分：投入规划")
            q7 = st.radio("7. 采购策略？", ["A. 低价开源", "B. 长期配置", "C. 价值溢价"])
            q8 = st.radio("8. 掌控感预期？", ["A. 工具导向", "B. 生态导向", "C. 主权导向"])
            
            submit = st.form_submit_button("🌱 提交结果")

    with r:
        # 实时逻辑
        choices = [q1, q2, q3, q4, q5, q6, q7, q8]
        c_count = sum(1 for x in choices if "C." in x)
        
        if c_count >= 5:
            icon, name, img = "🦀", "殿堂·帝王蟹 (ME7)", "https://img.icons8.com/?size=400&id=121153&format=png"
        elif c_count >= 2:
            icon, name, img = "🦞", "进阶·大龙虾 (Nova Claw)", "https://img.icons8.com/?size=400&id=mNInV8G1Gv8R&format=png"
        else:
            icon, name, img = "🦐", "敏捷·小龙虾 (OpenClaw)", "https://img.icons8.com/?size=400&id=121151&format=png"
            
        st.markdown(f"""
            <div class="visual-panel">
                <img src="{img}" style="width:250px;">
                <h2 style="margin:0;">{name}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        if submit:
            # 更新全局数据
            key = "C" if c_count >= 5 else ("B" if c_count >= 2 else "A")
            st.session_state.group_data[key] += 1
            st.balloons()
            st.success("诊断完成！请切换到 [现场洞察] 标签查看全场趋势。")

with tab2:
    st.header("📊 现场实时洞察看板")
    
    # 顶部统计
    total = sum(st.session_state.group_data.values())
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="stat-card">参与人数<br><span class="stat-val">{total}</span></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-card">小龙虾(A)<br><span class="stat-val">{st.session_state.group_data["A"]}</span></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="stat-card">大龙虾(B)<br><span class="stat-val">{st.session_state.group_data["B"]}</span></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="stat-card">帝王蟹(C)<br><span class="stat-val">{st.session_state.group_data["C"]}</span></div>', unsafe_allow_html=True)

    # 饼图修复逻辑：确保数据非空
    if total > 0:
        fig = px.pie(
            names=['敏捷型 (A)', '定制型 (B)', '主权型 (C)'],
            values=[st.session_state.group_data["A"], st.session_state.group_data["B"], st.session_state.group_data["C"]],
            color_discrete_sequence=['#ff4b4b', '#ff8c00', '#0078d4'],
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)

    # MiniMax 群体分析
    if st.button("🤖 开启 AI 现场实时趋势分析"):
        p = f"现场{total}人参与。A:{st.session_state.group_data['A']}, B:{st.session_state.group_data['B']}, C:{st.session_state.group_data['C']}。请简要分析趋势。"
        with st.spinner("MiniMax 正在思考..."):
            ans = ask_minimax(p)
            st.info(f"🏛️ **专家洞察**：\n\n{ans}")
