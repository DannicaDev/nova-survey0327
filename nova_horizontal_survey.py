import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json

# --- 1. 页面配置与超感视觉样式 ---
st.set_page_config(page_title="AI 进阶路径诊断 | 现场互动版", page_icon="🌿", layout="wide")

# 公共高清图片链接
LOBSTER_IMG = "https://img.icons8.com/?size=400&id=121151&format=png" # 小龙虾
BIG_LOBSTER_IMG = "https://img.icons8.com/?size=400&id=mNInV8G1Gv8R&format=png" # 大龙虾
KING_CRAB_IMG = "https://img.icons8.com/?size=400&id=121153&format=png" # 帝王蟹

# 自定义 CSS：强制深色文字、美化排版、解决留白
st.markdown("""
    <style>
    /* 全局背景与字体 */
    .stApp { background-color: #F0F9F0 !important; }
    html, body, [class*="st-"] { color: #155724 !important; font-family: 'Segoe UI', 'Roboto', sans-serif; }
    
    /* 标题样式 */
    h1 { color: #155724 !important; font-weight: 700 !important; font-size: 42px !important; margin-bottom: 5px !important; }
    h3 { color: #155724 !important; font-weight: 600 !important; margin-top: 15px !important; font-size: 20px !important;}
    h5 { color: #155724 !important; font-weight: 400 !important; font-size: 16px !important; margin-bottom: 20px !important;}

    /* 问卷表单卡片 */
    [data-testid="stForm"] { 
        background-color: white !important; 
        border-radius: 20px; padding: 40px; 
        border: 1px solid #C3E6CB;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    
    /* 单选框样式 */
    div[data-testid="stRadio"] label { 
        color: #2c3e50 !important; 
        font-weight: 500 !important; 
        font-size: 15px !important; 
        margin-bottom: 5px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] { gap: 10px; } /* 选项间距 */

    /* 右侧视觉面板 */
    .visual-panel {
        background: white !important; border-radius: 20px; padding: 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1); text-align: center;
        margin-bottom: 20px;
        border: 2px solid #28a745;
    }
    .lobster-main-img { width: 90%; max-width: 320px; height: auto; margin: 20px auto; display: block; }
    
    /* 统计卡片与 Insight 卡片 */
    .stat-card { background: white; border-radius: 10px; padding: 15px; text-align: center; border-top: 5px solid #28a745; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
    .stat-val { font-size: 36px; font-weight: bold; color: #155724; }
    .insight-card {
        background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%) !important;
        border-radius: 15px; padding: 25px;
        margin-top: 20px; border-left: 5px solid #00796b;
        color: #004d40 !important; font-size: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 初始化全局数据 (保存在服务器内存) ---
if 'group_data' not in st.session_state:
    st.session_state.group_data = {"A": 1, "B": 1, "C": 1} # 预设数据防报错

# --- 3. MiniMax 定义 ---
def ask_minimax(prompt_text, bot_setting="你是一名资深 AI 战略专家。"):
    api_key = st.secrets.get("MINIMAX_API_KEY")
    group_id = st.secrets.get("MINIMAX_GROUP_ID")
    if not api_key: return "（未配置 MiniMax API Key，无法生成动态 Insight）"
    
    url = f"https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId={group_id}"
    payload = {
        "model": "abab6.5-chat",
        "messages": [{"sender_type": "USER", "sender_name": "User", "text": prompt_text}],
        "bot_setting": [{"region": "China", "content": bot_setting}]
    }
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    try:
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        return r.json()['reply']
    except: return "大模型正在闭关思考中，请稍后再试..."

# --- 4. 主体标题 ---
st.title("🌿 春启新程 · 企业 AI 进阶全景诊断")
st.markdown("##### 尊敬的决策者：请完成以下 8 个维度的测评，大模型将为您生成专属的数字化进化 Insight。")

# --- 5. 布局：使用 Tabs 分离个人与群体视角 ---
tab1, tab2 = st.tabs(["📋 个人诊断", "📊 现场洞察看板"])

with tab1:
    l_col, r_col = st.columns([65, 35]) # 调整比例
    
    with l_col:
        with st.form("my_form"):
            st.markdown("### 🧬 企业 AI 进化 8 维测评")
            
            # 使用内嵌 columns 将问题排成两列，解决留白问题
            q_col1, q_col2 = st.columns(2)
            
            with q_col1:
                st.markdown("#### 第一部分：安全与主权")
                q1 = st.radio("1. 公公有云 AI 使用态度？", ["A. 效率优先：鼓励使用", "B. 稳健为主：担忧泄密", "C. 主权至上：严令禁止"])
                q2 = st.radio("2. 核心业务数据的访问要求？", ["A. 结果导向：不限位置", "B. 信任大厂：须在微软云端", "C. 绝对隔离：数据不出场"])
                q3 = st.radio("3. 数据归属权？", ["A. 无所谓", "B. 合同约定归属", "C. 必须明确私有"])

                st.markdown("#### 第二部分：业务复杂度")
                q4 = st.radio("4. AI 解决的核心问题？", ["A. 基础文字场景", "B. 流程协同场景", "C. 深度逻辑/API调用"])

            with q_col2:
                q5 = st.radio("5. 个性化操作习惯要求？", ["A. 灵活多变", "B. 统一标准界面", "C. 私有定制专属数字员工"])
                q6 = st.radio("6. Agent 智能体数量预期？", ["A. 个体为主", "B. 组织统筹一套", "C. 集群作战 Agents 矩阵"])

                st.markdown("#### 第三部分：投入与灵活度")
                q7 = st.radio("7. AI 工具采购策略？", ["A. 低成本尝试/开源", "B. 长期基建/接受年费", "C. 价值溢价/数据保护"])
                q8 = st.radio("8. 掌控感预期？", ["A. 工具导向：使用者", "B. 生态导向：跟随大厂", "C. 主权导向：最高权限"])
            
            submit = st.form_submit_button("🌱 生成大模型诊断报告")

    with r_col:
        # --- 右侧上半部分：动态高清大图 (修复显示) ---
        visual_placeholder = st.empty()
        
        # 实时匹配逻辑
        choices = [q1, q2, q3, q4, q5, q6, q7, q8]
        # 简化判定：C 越多，主权越高
        c_count = sum(1 for x in choices if "C." in x)
        
        if c_count >= 5:
            current_img = KING_CRAB_IMG
            current_name = "殿堂·帝王蟹 (ME7)"
            current_color = "#0078d4"
        elif c_count >= 2:
            current_img = BIG_LOBSTER_IMG
            current_name = "进阶·大龙虾 (Nova Claw)"
            current_color = "#ff8c00"
        else:
            current_img = LOBSTER_IMG
            current_name = "敏捷·小龙虾 (OpenClaw)"
            current_color = "#ff4b4b"

        # 展示大图卡片
        visual_placeholder.markdown(f"""
            <div class="visual-panel">
                <img src="{current_img}" class="lobster-main-img">
                <h2 style="color:{current_color}; margin-top:10px;">{current_name}</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # --- 右侧下半部分：个人诊断结果 (找回雷达图 + 新增 LLM Insight) ---
        if submit:
            # 1.Balloon 效果
            st.balloons()
            
            # 2. 详细计分
            res = {"A": 0, "B": 0, "C": 0}
            for q in choices:
                res[q[0]] += 1
            
            # 3. 绘制雷达图 (找回并精美化)
            st.markdown("#### 📊 您的 AI 进化雷达图")
            fig = go.Figure(data=go.Scatterpolar(
                r=[res["A"], res["B"], res["C"]],
                theta=['敏捷(A)', '协同(B)', '主权(C)'],
                fill='toself', line_color='#155724', marker=dict(color='#155724')
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 8], tickfont=dict(color="#155724")),
                           angularaxis=dict(tickfont=dict(color="#155724"))),
                height=300, margin=dict(l=50,r=50,t=30,b=30),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

            # 4. 个人 MiniMax Insight (核心新增)
            st.markdown("#### 🤖 LLM 专属诊断 Insight")
            user_profile = f"安全要求: {q1}, 数据不出场: {q2}, 业务深度: {q4}, 定制化: {q5}"
            individual_prompt = f"作为企业咨询专家，基于企业画像：{user_profile}，结论是 {current_name} 路径。给出3条深刻的 Insight 和2条下一步建议。字数150字内。"

            with st.spinner("大模型正在深度思考您的进化路径..."):
                individual_insight = ask_minimax(individual_prompt, "你是一名资深企业数字化转型专家。")
                st.markdown(f'<div class="insight-card">{individual_insight}</div>', unsafe_allow_html=True)
            
            # 5. 更新全局数据
            final_key = "C" if c_count >= 5 else ("B" if c_count >= 2 else "A")
            st.session_state.group_data[final_key] += 1
            st.success("您的结果已匿名上传至 [现场洞察看板]！")

        else:
            st.markdown('<p style="text-align:center; color:#155724; font-size:14px;">💡 完成测评，解锁大模型专属 Insight 与雷达图谱...</p>', unsafe_allow_html=True)

with tab2:
    # --- 群体洞察版块 (保持稳定) ---
    st.header("📊 现场实时洞察看板")
    
    total = sum(st.session_state.group_data.values())
    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(f'<div class="stat-card">参与人数<br><span class="stat-val">{total}</span></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-card">敏捷·小龙虾(A)<br><span class="stat-val">{st.session_state.group_data["A"]}</span></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="stat-card">进阶·大龙虾(B)<br><span class="stat-val">{st.session_state.group_data["B"]}</span></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="stat-card">殿堂·帝王蟹(C)<br><span class="stat-val">{st.session_state.group_data["C"]}</span></div>', unsafe_allow_html=True)

    # 防止饼图报错
    if total > 0:
        st.markdown("---")
        fig_pie = px.pie(
            names=['敏捷型 (A)', '定制型 (B)', '主权型 (C)'],
            values=[st.session_state.group_data["A"], st.session_state.group_data["B"], st.session_state.group_data["C"]],
            color_discrete_sequence=['#ff4b4b', '#ff8c00', '#0078d4'],
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # MiniMax 群体分析
    if st.button("🤖 生成现场群体趋势分析"):
        p = f"现场{total}人参与。A:{st.session_state.group_data['A']}, B:{st.session_state.group_data['B']}, C:{st.session_state.group_data['C']}。请简要分析现场趋势。"
        with st.spinner("MiniMax 正在解析全场数据..."):
            group_ans = ask_minimax(p)
            st.info(f"🏛️ **全场专家洞察**：\n\n{group_ans}")
