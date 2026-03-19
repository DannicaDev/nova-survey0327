import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests

# --- 1. 页面配置与超强视觉样式 (精修版) ---
st.set_page_config(page_title="AI 进阶路径诊断 | 现场版", page_icon="🌿", layout="wide")

# 强制 CSS：锁定字号、颜色配合、解决留白、优化排版配合
st.markdown("""
    <style>
    /* 全局背景与字体 */
    .stApp { background-color: #F0F9F0 !important; }
    html, body, [class*="st-"] { color: #155724 !important; font-family: 'Segoe UI', 'Roboto', sans-serif; }
    
    /* 标题样式 */
    h1 { color: #155724 !important; font-weight: 700 !important; font-size: 38px !important; margin-bottom: 5px !important; }
    h3 { color: #155724 !important; font-weight: 600 !important; margin-top: 15px !important; font-size: 22px !important;}
    h4 { color: #155724 !important; font-weight: 500 !important; font-size: 18px !important; margin-bottom: 10px !important;}
    h5 { color: #155724 !important; font-weight: 400 !important; font-size: 16px !important; margin-bottom: 15px !important;}

    /* 问卷表单卡片 */
    [data-testid="stForm"] { 
        background-color: white !important; border-radius: 20px; 
        padding: 35px; border: 1px solid #C3E6CB;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    
    /* 单选框样式：字号配合 */
    div[data-testid="stRadio"] label { color: #2c3e50 !important; font-weight: 500 !important; font-size: 16px !important; }
    
    /* 右侧视觉面板 (修复图片显示) */
    .visual-panel {
        background: white !important; border-radius: 20px; padding: 25px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1); text-align: center;
        margin-bottom: 20px; border: 2px solid #28a745;
    }
    .lobster-main-img { width: 90%; max-width: 320px; height: auto; margin: 20px auto; display: block; }
    
    /* Insight 卡片 (精修字号与换行排版) */
    .insight-card {
        background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%) !important;
        border-radius: 15px; padding: 25px;
        margin-top: 20px; border-left: 5px solid #00796b;
        color: #004d40 !important; 
        font-size: 16px !important; line-height: 1.8 !important; /* 增加行高 */
    }
    /* 现场看板卡片 */
    .stat-card { background: white; border-radius: 12px; padding: 20px; text-align: center; border-top: 6px solid #28a745; box-shadow: 0 5px 15px rgba(0,0,0,0.08); }
    .stat-val { font-size: 40px; font-weight: bold; color: #155724; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 初始化全局数据 (保存在服务器内存) ---
if 'group_data' not in st.session_state:
    st.session_state.group_data = {"A": 2, "B": 2, "C": 1} # 预设数据防报错

# --- 3. MiniMax 调用预留 ---
def call_minimax(prompt_text):
    # (预留 MiniMax 调用，目前使用 fallback 兜底，现场网络不通也不怕)
    api_key = st.secrets.get("MINIMAX_API_KEY")
    # 增加 Fallback 机制：现场如果网络不通，直接返回这段预设的高价值文案
    if "蟹" in prompt_text or "ME7" in prompt_text:
        return "**Insight**: 您的企业视数据为主权。普通的协同工具已无法承载您的雄心。ME7 不仅是工具，更是您的“数字堡垒”。\n\n**建议**: 1. 立即启动 Microsoft Purview 高级数据资产全景梳理。2. 评估核心定价模型进入帝王蟹级隔离域的可行性。"
    elif "龙虾" in prompt_text or "NovaClaw" in prompt_text:
        # **修复：更名为 NovaClaw**
        return "**Insight**: 您的核心竞争力在于业务逻辑的**独家定制**。NovaClaw 是帮您把智慧转化为数字资产的关键。\n\n**建议**: 1. 确定 2 个具有高溢价能力的业务 API，作为 NovaClaw 的首批“数字员工”。2. 开启私有 Agent 共创模式。"
    else:
        return "**Insight**: 敏捷是您的利器，但影子 AI 是潜伏的礁石。当前阶段应以 OpenClaw 快速激活全员效率，但需建立基础的使用准则。\n\n**建议**: 1. 制定企业全员 AI 使用白皮书。2. 寻找 3 个高频琐事场景进行自动化替代实验。"

# --- 4. 主体布局 ---
st.title("🌿 春启新程 · 企业 AI 进阶全景诊断")
st.markdown("##### 尊敬的决策者：请完成以下 8 个维度的测评，我们将为您生成专属的数字化进化 Insight。")

tab1, tab2 = st.tabs(["📋 个人诊断", "📊 现场洞察看板"])

with tab1:
    l_col, r_col = st.columns([65, 35]) # 调整比例
    with l_col:
        with st.form("my_form"):
            st.markdown("### 🧬 企业 AI 进化 8 维测评")
            # --- 修复：使用双列排版填补中间留白 ---
            q_col1, q_col2 = st.columns(2)
            with q_col1:
                st.markdown("#### 第一部分：安全边界")
                q1 = st.radio("1. 公有云 AI 使用态度？", ["A. 效率优先", "B. 担忧合规", "C. 严格禁入"])
                q2 = st.radio("2. 核心数据访问要求？", ["A. 结果导向", "B. 信任大厂云", "C. 物理不出场"])
                q3 = st.radio("3. 数据归属权趋势？", ["A. 无所谓", "B. 合同约定", "C. 必须私有隔离"])
                st.markdown("#### 第二部分：业务深度")
                q4 = st.radio("4. AI 解决的问题？", ["A. 文字基础", "B. 流程协同", "C. 深度逻辑/API"])
            with q_col2:
                q5 = st.radio("5. 定制化个性习惯要求？", ["A. 标准界面", "B. 模块化配置", "C. 私有专属员工"])
                q6 = st.radio("6. Agent 预期数量？", ["A. 零散工具", "B. 组织统筹", "C. 集群作战矩阵"])
                st.markdown("#### 第三部分：投入规划")
                q7 = st.radio("7. AI 采购价值取向？", ["A. 快速尝试", "B. 长期配置", "C. 价值溢价/资产保护"])
                q8 = st.radio("8. 掌控感预期？", ["A. 工具使用者", "B. 生态跟随", "C. 最高主权"])
            
            submit = st.form_submit_button("🌱 提交结果")

    with r_col:
        # --- 修复：右侧实时高清大图 (龙虾图片回归且变大) ---
        visual_placeholder = st.empty()
        # 实时判定
        all_qs = [q1, q2, q3, q4, q5, q6, q7, q8]
        c_count = sum(1 for x in all_qs if "C." in x)
        
        # 龙虾/帝王蟹回归
        if c_count >= 5:
            # 殿堂·帝王蟹 (ME7)
            img = "https://img.icons8.com/?size=400&id=121153&format=png"
            name, color = "殿堂·帝王蟹 (ME7 Suite)", "#0078d4"
        elif c_count >= 2:
            # 进阶·大龙虾 (NovaClaw)
            # **修复：更名为 NovaClaw**
            img = "https://img.icons8.com/?size=400&id=mNInV8G1Gv8R&format=png"
            name, color = "进阶·大龙虾 (NovaClaw)", "#ff8c00"
        else:
            # 敏捷·小龙虾 (OpenClaw)
            img = "https://img.icons8.com/?size=400&id=121151&format=png"
            name, color = "敏捷·小龙虾 (OpenClaw)", "#ff4b4b"
            
        # 展示大图卡片 (修复图片变小问题，通过 CSS `lobster-main-img` 控制)
        visual_placeholder.markdown(f"""
            <div class="visual-panel">
                <img src="{img}" class="lobster-main-img">
                <h2 style="color:{color}; margin-top:10px;">{name}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        if submit:
            # Balloons!
            st.balloons()
            st.markdown("---")
            
            # 雷达图 (找回并精美化)
            st.markdown("#### 您的 AI 进化雷达图")
            scores = {"A": sum(1 for x in all_qs if "A." in x), 
                      "B": sum(1 for x in all_qs if "B." in x), 
                      "C": c_count}
            fig = go.Figure(data=go.Scatterpolar(
                r=[scores["A"], scores["B"], scores["C"]],
                theta=['敏捷(A)', '协同(B)', '主权(C)'],
                fill='toself', line_color='#155724'
            ))
            # 调整分数为 0-8，适应 8 题版
            fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 8])), height=250, margin=dict(l=40,r=40,t=20,b=20))
            st.plotly_chart(fig, use_container_width=True)

            # 专家 Insight (增加换行，提高可读性)
            st.markdown("#### 🤖 大模型专家诊断 Insight")
            user_profile = f"数据安全: {q1}, 核心数据: {q2}, 业务深度: {q4}, 定制化: {q5}"
            # 这里调用本地兜底，确保现场没问题
            insight_content = call_minimax(user_profile)
            # 使用 CSS 控制字号与换行配合
            st.markdown(f'<div class="insight-card">{insight_content}</div>', unsafe_allow_html=True)
            
            # 申请名额按钮 (主权型 C>=4 出现)
            if scores["C"] >= 4:
                st.button("🌸 申请 NovaClaw 创始共创名额")
                
            # 更新全局数据
            key = "C" if c_count >= 5 else ("B" if c_count >= 2 else "A")
            st.session_state.group_data[key] += 1
            st.success("匿名诊断结果已同步至现场看板！")
        else:
            st.markdown('<p style="text-align:center; color:#155724; font-size:14px; margin-top:15px;">💡 完成测评，解锁大模型专属 Insight 与雷达图谱...</p>', unsafe_allow_html=True)

with tab2:
    # --- 群体洞察版块 (看板大改版) ---
    st.header("📊 现场实时洞察看板")
    total = sum(st.session_state.group_data.values())
    
    # 看板布局大改，增加信息量，消除凌乱感，字号配合
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f'<div class="stat-card">参与人数<br><span class="stat-val">{total}</span></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="stat-card">小龙虾(A)<br><span class="stat-val">{st.session_state.group_data["A"]}</span></div>', unsafe_allow_html=True)
    # **修复：更名为 NovaClaw**
    k3.markdown(f'<div class="stat-card">NovaClaw(B)<br><span class="stat-val">{st.session_state.group_data["B"]}</span></div>', unsafe_allow_html=True)
    k4.markdown(f'<div class="stat-card">帝王蟹(C)<br><span class="stat-val">{st.session_state.group_data["C"]}</span></div>', unsafe_allow_html=True)

    if total > 0:
        st.markdown("---")
        # 增加饼图，展示专业配色配合字号大字号
        # 采用两列横向布局解决留白凌乱
        g_col1, g_col2 = st.columns([6, 4])
        with g_col1:
            st.markdown("### 全场分布图谱")
            # 手动配色配合
            fig_pie = px.pie(
                names=['敏捷型 (A)', '协同型 (B)', '主权型 (C)'],
                values=[st.session_state.group_data["A"], st.session_state.group_data["B"], st.session_state.group_data["C"]],
                color_discrete_sequence=['#ff4b4b', '#ff8c00', '#0078d4'],
                hole=0.4
            )
            # 调大占比字号配合
            fig_pie.update_traces(textinfo='percent+label', textfont_size=18, marker=dict(line=dict(color='#FFFFFF', width=2)))
            fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=350)
            st.plotly_chart(fig_pie, use_container_width=True)

        with g_col2:
            st.markdown("### 群体分析建议")
            # MiniMax 分析群体
            g_p = f"现场{total}人参与。A:{st.session_state.group_data['A']}, B:{st.session_state.group_data['B']}, C:{st.session_state.group_data['C']}。请分析管理者焦虑点。"
            # 这里调用本地兜底，现场没问题
            group_insight = call_minimax(g_p)
            # 配合换行
            st.info(f"🏛️ **专家洞察**：\n\n{group_insight}")
            st.markdown("""
                <div style="background:#e8f5e9; padding:15px; border-radius:10px; font-size:14px; color:#1b5e20;">
                **提示**: 现场将随机抽取 **Mac Mini**，确保您的诊断结果属于 C 型（主权型）以增加中奖几率！
                </div>
            """, unsafe_allow_html=True)
