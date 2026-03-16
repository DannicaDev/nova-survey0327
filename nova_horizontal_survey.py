import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. 页面配置
st.set_page_config(page_title="AI 进阶路径诊断", page_icon="🌿", layout="wide")

# 自定义视觉样式
st.markdown("""
    <style>
    .stApp { background-color: #F0F9F0; }
    [data-testid="stForm"] { 
        background-color: rgba(255,255,255,0.95); 
        border-radius: 15px; 
        padding: 25px;
        border: 1px solid #C3E6CB;
    }
    .visual-card {
        background: white; border-radius: 15px; padding: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: center;
    }
    .lobster-icon { font-size: 80px; margin: 0; }
    .matrix-label { font-size: 14px; font-weight: bold; color: #155724; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 春启新程 · AI 进阶盛宴诊断")
st.markdown("**尊敬的决策者：** AI 已经从小龙虾的灵动，进化到了帝王蟹的稳重。请勾勒您的进化路径。")

# 2. 左右布局
left_col, right_col = st.columns([6, 4])

with left_col:
    with st.form("survey_form"):
        st.subheader("第一部分：安全与主权")
        q1 = st.radio("1. 您的团队使用公有云 AI 的态度是？", 
                     ["A. 效率优先：鼓励使用", "B. 稳健为主：担忧但未禁止", "C. 主权至上：严令禁止，须完全受控"])
        q2 = st.radio("2. 核心业务数据（如财务/设计）的访问要求？", 
                     ["A. 结果导向：不限位置", "B. 信任大厂：须在微软云端运行", "C. 绝对私有：必须本地或隔离环境"])

        st.subheader("第二部分：业务复杂度")
        q3 = st.radio("3. AI 解决的核心问题？", 
                     ["A. 个人琐事：发帖/查资料", "B. 组织协同：会议/文档", "C. 深度逻辑：私有API/业务指令"])
        q4 = st.radio("4. 您的个性化追求？", 
                     ["A. 好玩好折腾：开源模型", "B. 学习成本低：统一界面", "C. 深度定制：私有数字员工"])

        st.subheader("第三部分：预算规划")
        q5 = st.radio("5. 您的 AI 订阅预算规划？", 
                     ["A. 极低成本/按需付费", "B. 长期基建/接受年费", "C. 价值导向/愿意为数据主权溢价"])

        submit = st.form_submit_button("生成诊断报告")

with right_col:
    # 实时匹配逻辑
    icon, name = "🦐", "敏捷·小龙虾"
    if "C" in q1 and "C" in q2:
        icon, name = "🦀", "殿堂·帝王蟹 (ME7)"
    elif "C" in q3 or "C" in q4:
        icon, name = "🦞", "进阶·大龙虾 (Nova Claw)"
        
    st.markdown(f'<div class="visual-card"><p class="lobster-icon">{icon}</p><h2 style="color:#28a745;">{name}</h2></div>', unsafe_allow_html=True)

    if submit:
        # 计分
        res = {"A": 0, "B": 0, "C": 0}
        for q in [q1, q2, q3, q4, q5]:
            res[q[0]] += 1
        
        # 绘制雷达图
        fig = go.Figure(data=go.Scatterpolar(
            r=[res["A"], res["B"], res["C"]],
            theta=['敏捷(A)', '协同(B)', '主权(C)'],
            fill='toself', line_color='#28a745'
        ))
        fig.update_layout(height=300, polar=dict(radialaxis=dict(visible=True, range=[0, 5])), margin=dict(l=40,r=40,t=40,b=40))
        st.plotly_chart(fig, use_container_width=True)

        # 矩阵小图标
        m1, m2, m3 = st.columns(3)
        m1.markdown(f'<div style="text-align:center;"><p style="font-size:30px;">🦐</p><p class="matrix-label">OpenClaw<br>{res["A"]*20}%</p></div>', unsafe_allow_html=True)
        m2.markdown(f'<div style="text-align:center;"><p style="font-size:30px;">🦞</p><p class="matrix-label">Nova Claw<br>{res["C"]*20}%</p></div>', unsafe_allow_html=True)
        m3.markdown(f'<div style="text-align:center;"><p style="font-size:30px;">🦀</p><p class="matrix-label">ME7<br>{res["B"]*20}%</p></div>', unsafe_allow_html=True)
        
        if res["C"] >= 3:
            st.success("🌸 系统已锁定您的 Nova Claw 共创名额")
    else:
        st.info("💡 调研实时生成中...")
