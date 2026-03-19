import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import json

# --- 1. 页面配置 ---
st.set_page_config(page_title="AI 进阶路径诊断 | 群体洞察版", page_icon="🌿", layout="wide")

# --- 2. 模拟全局数据搜集 (现场演示用) ---
# 注意：Streamlit Cloud 重启会清空此数据。如需永久保存，需对接数据库。
if 'group_results' not in st.session_state:
    st.session_state.group_results = {"A": 12, "B": 18, "C": 8} # 预置一些初始模拟数据，让图表不为空

# --- 3. MiniMax 调用函数预留 ---
def call_minimax(prompt):
    group_id = st.secrets.get("MINIMAX_GROUP_ID")
    api_key = st.secrets.get("MINIMAX_API_KEY")
    
    if not api_key or not group_id:
        return "（提示：请配置 MiniMax API Key 以激活 AI 深度实时分析）"
    
    url = f"https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId={group_id}"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    
    payload = {
        "model": "abab6.5-chat", # 或者你使用的具体型号
        "messages": [{"sender_type": "USER", "sender_name": "Consultant", "text": prompt}],
        "bot_setting": [{"region": "China", "content": "你是一名资深企业数字化转型专家，擅长从群体数据中洞察商业趋势。"}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json()['reply']
    except Exception as e:
        return f"AI 分析暂时离线: {e}"

# --- 4. UI 样式 ---
st.markdown("""
    <style>
    .stApp { background-color: #F8FFF8 !important; }
    .stat-card { background: white; border-radius: 10px; padding: 15px; text-align: center; border-top: 5px solid #28a745; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
    .stat-val { font-size: 32px; font-weight: bold; color: #155724; }
    </style>
    """, unsafe_allow_html=True)

# --- 5. 主体布局 ---
tab1, tab2 = st.tabs(["📋 个人诊断", "📊 现场群体洞察"])

with tab1:
    left_col, right_col = st.columns([6, 4])
    with left_col:
        with st.form("survey_form"):
            st.markdown("### 企业 AI 进化 8 维测评")
            # (此处省略 8 道题的具体 radio 代码，保持之前的 A/B/C 逻辑)
            # 示例题目
            q1 = st.radio("1. 员工使用公有云 AI 的态度？", ["A. 效率优先", "B. 稳健监管", "C. 严格受控"])
            q2 = st.radio("2. 核心数据访问要求？", ["A. 结果导向", "B. 信任大厂云", "C. 绝对私有隔离"])
            # ... 其他 6 道题 ...
            
            submit = st.form_submit_button("🌱 提交并查看我的路径")

    if submit:
        # 计算逻辑
        res_type = "A" # 假设根据选择判定为 A
        if "C" in q1 and "C" in q2: res_type = "C"
        
        # 更新全局搜集结果
        st.session_state.group_results[res_type] += 1
        st.success("您的结果已匿名上传至现场实时动态看板！")

with tab2:
    st.header("📈 现场调研实时看板")
    
    # 顶部统计卡片
    total_votes = sum(st.session_state.group_results.values())
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="stat-card">参与人数<br><span class="stat-val">{total_votes}</span></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-card">敏捷·小龙虾<br><span class="stat-val">{st.session_state.group_results["A"]}</span></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="stat-card">进阶·大龙虾<br><span class="stat-val">{st.session_state.group_results["B"]}</span></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="stat-card">殿堂·帝王蟹<br><span class="stat-val">{st.session_state.group_results["C"]}</span></div>', unsafe_allow_html=True)

    # 饼图展示分布
    fig = px.pie(
        values=list(st.session_state.group_results.values()), 
        names=['敏捷型 (OpenClaw)', '协同型 (ME7)', '主权型 (Nova Claw)'],
        color_discrete_sequence=['#ff4b4b', '#0078d4', '#ff8c00'],
        hole=0.4
    )
    st.plotly_chart(fig, use_container_width=True)

    # MiniMax 实时群体分析
    if st.button("🤖 生成现场群体趋势分析"):
        group_prompt = f"""
        现场共有 {total_votes} 位管理者参与了 AI 路径调研。
        结果如下：选择敏捷型路径的占 {st.session_state.group_results['A']} 人，
        协同型占 {st.session_state.group_results['B']} 人，
        选择主权型（数据不出场、深度定制）的占 {st.session_state.group_results['C']} 人。
        请以此数据为基础，分析当前行业对 AI 的核心焦虑点，并针对占比较大的群体给出一段充满前瞻性的寄语。
        """
        with st.spinner("MiniMax 正在解析现场数据..."):
            group_analysis = call_minimax(group_prompt)
            st.markdown(f"""
                <div style="background:#fff3e0; padding:20px; border-radius:10px; border-left:5px solid #ff8c00;">
                    <strong>🏛️ 专家实时点评：</strong><br>{group_analysis}
                </div>
            """, unsafe_allow_html=True)
