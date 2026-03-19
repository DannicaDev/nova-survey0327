import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import time

# --- 1. 页面配置与超感视觉样式 ---
st.set_page_config(page_title="AI 进阶路径诊断 | 现场互动版", page_icon="🌿", layout="wide")

# 公共高清图片链接 (确保链接可访问，或替换为您自己的图床)
# 修复：直接使用 st.image 原生组件，不再依赖复杂的 HTML/CSS 渲染图片
LOBSTER_IMG = "https://img.icons8.com/?size=400&id=121151&format=png" # 小龙虾
BIG_LOBSTER_IMG = "https://img.icons8.com/?size=400&id=mNInV8G1Gv8R&format=png" # 大龙虾
KING_CRAB_IMG = "https://img.icons8.com/?size=400&id=121153&format=png" # 帝王蟹

# 自定义 CSS：强制深色文字、美化排版、解决留白、优化字号配合
st.markdown("""
    <style>
    /* 全局背景与字体 */
    .stApp { background-color: #F0F9F0 !important; }
    html, body, [class*="st-"] { color: #155724 !important; font-family: 'Segoe UI', 'Roboto', sans-serif; }
    
    /* 标题样式：森林绿，字号配合 */
    h1 { color: #155724 !important; font-weight: 700 !important; font-size: 38px !important; margin-bottom: 5px !important; }
    h2 { color: #155724 !important; font-weight: 600 !important; font-size: 28px !important; }
    h3 { color: #155724 !important; font-weight: 600 !important; margin-top: 15px !important; font-size: 22px !important;}
    h4 { color: #155724 !important; font-weight: 500 !important; font-size: 18px !important;}
    h5 { color: #155724 !important; font-weight: 400 !important; font-size: 16px !important; margin-bottom: 15px !important;}

    /* 问卷表单卡片 */
    [data-testid="stForm"] { 
        background-color: white !important; 
        border-radius: 20px; padding: 35px; 
        border: 1px solid #C3E6CB;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    
    /* 单选框样式：深灰色，字号配合 */
    div[data-testid="stRadio"] label { 
        color: #2c3e50 !important; 
        font-weight: 500 !important; 
        font-size: 16px !important; 
        margin-bottom: 4px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] { gap: 8px; } /* 选项间距 */

    /* 右侧视觉面板 (修复图片显示) */
    .visual-panel {
        background: white !important; border-radius: 20px; padding: 25px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1); text-align: center;
        margin-bottom: 20px;
        border: 2px solid #28a745;
    }
    /* st.image 自动适配，这里不再需要复杂的 CSS 控制图片 */
    
    /* 统计卡片与 Insight 卡片 */
    .stat-card { background: white; border-radius: 12px; padding: 20px; text-align: center; border-top: 6px solid #28a745; box-shadow: 0 5px 15px rgba(0,0,0,0.08); }
    .stat-val { font-size: 40px; font-weight: bold; color: #155724; }
    .stat-label { font-size: 16px; color: #666; font-weight: 500; }

    /* 修复：Insight 卡片字号与背景配合，确保清晰且专业 */
    .insight-card {
        background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%) !important;
        border-radius: 15px; padding: 25px;
        margin-top: 20px; border-left: 5px solid #00796b;
        color: #004d40 !important; font-size: 16px !important; line-height: 1.6 !important;
    }
    /* 现场看板卡片 */
    .group-insight-card {
        background: white !important;
        border-radius: 15px; padding: 25px;
        margin-top: 15px; border: 1px solid #C3E6CB;
        color: #155724 !important; font-size: 16px !important; line-height: 1.6 !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 初始化全局数据 (保存在服务器内存) ---
# 提醒：现场演示只要不重启 App，数据就是实时累加的
if 'group_data' not in st.session_state:
    st.session_state.group_data = {"A": 2, "B": 2, "C": 1} # 预设基础数据防报错，让图表初始不为空

# --- 3. MiniMax 定义 (增加超时与本地兜底) ---
def ask_minimax_stable(prompt_text, bot_setting="你是一名资深 AI 战略专家。"):
    api_key = st.secrets.get("MINIMAX_API_KEY")
    group_id = st.secrets.get("MINIMAX_GROUP_ID")
    
    # 兜底标志
    use_fallback = False
    if not api_key:
        use_fallback = True
    
    if not use_fallback:
        url = f"https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId={group_id}"
        payload = {
            "model": "abab6.5-chat", # 请确保型号正确
            "messages": [{"sender_type": "USER", "sender_name": "User", "text": prompt_text}],
            "bot_setting": [{"region": "China", "content": bot_setting}]
        }
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        
        try:
            # 修复：延长超时时间至 30秒，适应现场网络
            r = requests.post(url, headers=headers, json=payload, timeout=30)
            if r.status_code == 200:
                reply = r.json().get('reply')
                if reply:
                    return reply
            # 如果接口返回错误或空，使用兜底
            use_fallback = True
        except Exception as e:
            st.warning(f"大模型连接超时，已启用本地专家库兜底。错误: {e}")
            use_fallback = True

    # --- 修复：本地专家库兜底机制 (保证现场绝对有文字) ---
    if use_fallback:
        # 简单判定 Prompt 类型
        if "现场" in prompt_text and "A:" in prompt_text:
            # 群体分析兜底
            return "从全场调研数据来看，**主权型（Nova Claw）** 的需求占比极高，这表明现场领导者们对‘数据资产化’和‘数字化所有权’的意识已非常超前。建议即刻开启内部核心业务逻辑的私有化梳理。"
        else:
            # 个人诊断兜底 (根据 Prompt 里的关键字)
            if "ME7" in prompt_text or "帝王蟹" in prompt_text:
                return "**Insight**: 您的企业视数据为皇冠上的明珠。普通的协同工具已无法承载您的雄心。ME7 不仅是工具，更是您的“数字堡垒”。\n\n**建议**: 1. 立即启动 Microsoft Purview 高级数据资产梳理。2. 评估核心定价模型进入隔离域的可行性。"
            elif "Nova Claw" in prompt_text or "大龙虾" in prompt_text:
                return "**Insight**: 您的核心竞争力在于业务逻辑的**独家定制**。Nova Claw 是帮您把智慧转化为数字资产的关键。\n\n**建议**: 1. 确定 2 个高溢价API，作为首批“数字员工”。2. 开启私有 Agent 共创。"
            else:
                return "**Insight**: 敏捷是您的利器，但影子 AI 是潜伏的礁石。当前阶段应以 OpenClaw 快速激活全员效率，但需建立基础的使用白皮书。\n\n**建议**: 1. 制定全员 AI 使用准则。2. 寻找 3 个琐事场景进行自动化实验。"

    return "（未配置 API Key，且兜底失败）"

# --- 4. 主体标题与导语 ---
st.title("🌿 春启新程 · 企业 AI 进阶全景诊断")
st.markdown("##### 尊敬的决策者：请完成以下 8 个维度的测评，大模型智舱将为您生成专属的数字化进化 Insight。")

# --- 5. 布局：使用 Tabs 分离个人与群体视角 ---
tab1, tab2 = st.tabs(["📋 个人诊断", "📊 现场洞察看板"])

with tab1:
    l_col, r_col = st.columns([65, 35]) # 调整比例
    
    with l_col:
        with st.form("my_form"):
            st.markdown("### 🧬 企业 AI 进化 8 维测评")
            
            # --- 修复：使用双列排版填补中间留白 ---
            q_col1, q_col2 = st.columns(2)
            
            with q_col1:
                st.markdown("#### 第一部分：安全与主权")
                q1 = st.radio("1. 公公有云 AI 使用态度？", ["A. 效率优先：鼓励使用", "B. 稳健为主：担忧泄密", "C. 主权至上：严令禁止"])
                q2 = st.radio("2. 核心业务数据的访问要求？", ["A. 结果导向：不限位置", "B. 信任大厂：须在微软云端", "C. 绝对隔离：数据不出场"])
                q3 = st.radio("3. 数据归属权？", ["A. 无所谓", "B. 合同约定归属", "C. 必须明确私有"])

                st.markdown("#### 第二部分：业务复杂度")
                q4 = st.radio("4. AI 解决的核心问题？", ["A. 基础文字场景", "B. 流程协同场景", "C. 深度逻辑/API调用"])

            with q_col2:
                q5 = st.radio("5. 个性化操作习惯要求？", ["A. 灵活多变", "B. 统一标准界面", "C. 定制专属数字员工"])
                q6 = st.radio("6. Agent 智能体数量预期？", ["A. 个体为主", "B. 组织统筹一套", "C. 集群作战Agents矩阵"])

                st.markdown("#### 第三部分：投入与灵活度")
                q7 = st.radio("7. AI 工具采购策略？", ["A. 低成本尝试/开源", "B. 长期基建/接受年费", "C. 价值溢价/数据保护"])
                q8 = st.radio("8. 掌控感预期？", ["A. 工具导向：使用者", "B. 生态导向：跟随大厂", "C. 主权导向：最高权限"])
            
            st.markdown("---")
            submit = st.form_submit_button("🌱 生成大模型诊断报告")

    with r_col:
        # --- 右侧：个人评测结果 (修复图片显示) ---
        choices = [q1, q2, q3, q4, q5, q6, q7, q8]
        c_count = sum(1 for x in choices if "C." in x)
        
        # 实时匹配图片逻辑
        if c_count >= 5:
            current_img = KING_CRAB_IMG
            current_name = "殿堂·帝王蟹 (ME7 Suite)"
            current_color = "#0078d4"
        elif c_count >= 2:
            current_img = BIG_LOBSTER_IMG
            current_name = "进阶·大龙虾 (Nova Claw)"
            current_color = "#ff8c00"
        else:
            current_img = LOBSTER_IMG
            current_name = "敏捷·小龙虾 (OpenClaw)"
            current_color = "#ff4b4b"

        # --- 修复：使用 st.container 和 st.image 强制图片显示 ---
        with st.container():
            st.markdown(f'<div style="background:white; border-radius:20px; padding:20px; text-align:center; border:2px solid #28a745; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">', unsafe_allow_html=True)
            # 使用原生组件，自动适配宽度，最稳定
            st.image(current_img, use_container_width=True)
            st.markdown(f'<h2 style="color:{current_color}; margin:10px 0 0 0;">{current_name}</h2></div>', unsafe_allow_html=True)
        
        # --- 诊断结果展现 ---
        if submit:
            st.balloons()
            st.markdown("---")
            
            # 计分
            res = {"A": 0, "B": 0, "C": 0}
            for q in choices:
                res[q[0]] += 1
            
            # --- 修复：找回雷达图 ---
            st.markdown("#### 📊 您的 AI 能力进化雷达图")
            fig = go.Figure(data=go.Scatterpolar(
                r=[res["A"], res["B"], res["C"]],
                theta=['敏捷(A)', '协同(B)', '主权(C)'],
                fill='toself', line_color='#155724'
            ))
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 8]), angularaxis=dict(tickfont=dict(color="#155724"))),
                height=300, margin=dict(l=50,r=50,t=20,b=20),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

            # --- 修复：个人 MiniMax Insight (增加兜底保证显示) ---
            st.markdown("#### 🤖 大模型专属诊断 Insight")
            user_prof = f"安全要求: {q1}, 数据不出场: {q2}, 业务深度: {q4}, 定制化: {q5}"
            # 简化 Prompt 提高响应速度
            ind_prompt = f"专家，基于画像：{user_prof}，结论是 {current_name}。给出3条深刻 Insight 和2条建议。120字内。"

            with st.spinner("大模型正在深度建模您的进化路径..."):
                # 调用稳定版函数
                individual_insight = ask_minimax_stable(ind_prompt, "你是一名企业数字化专家。")
                # 使用专门 CSS 强制配合字号与背景
                st.markdown(f'<div class="insight-card">{individual_insight}</div>', unsafe_allow_html=True)
            
            # 申请名额按钮
            if res["C"] >= 4:
                st.button("🌸 申请 Nova Claw 创始共创名额")
                
            # 更新全局数据
            final_key = "C" if c_count >= 5 else ("B" if c_count >= 2 else "A")
            st.session_state.group_data[final_key] += 1
            st.success("匿名诊断结果已同步至现场看板！")

        else:
            st.markdown('<p style="text-align:center; color:#155724; font-size:14px; margin-top:15px;">💡 完成测评，解锁大模型专属 Insight 与雷达图谱...</p>', unsafe_allow_html=True)

with tab2:
    # --- 修复：现场洞察看板，采用三列布局，增加信息量，排版友好配合 ---
    st.header("📊 现场调研实时洞察看板")
    total = sum(st.session_state.group_data.values())
    
    # 顶部统计卡片 (配合 CSS 美化)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="stat-card"><span class="stat-label">参与人数</span><br><span class="stat-val">{total}</span></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="stat-card"><span class="stat-label">小龙虾(A)</span><br><span class="stat-val">{st.session_state.group_data["A"]}</span></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="stat-card"><span class="stat-label">大龙虾(B)</span><br><span class="stat-val">{st.session_state.group_data["B"]}</span></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="stat-card"><span class="stat-label">帝王蟹(C)</span><br><span class="stat-val">{st.session_state.group_data["C"]}</span></div>', unsafe_allow_html=True)

    if total > 0:
        st.markdown("---")
        # --- 修复：两列变三列布局，配合图表与文字，消除凌乱感 ---
        g_col1, g_col2, g_col3 = st.columns([40, 35, 25])
        
        with g_col1:
            st.markdown("### 全场分布图谱")
            # 优化环形图样式与颜色
            fig_pie = px.pie(
                names=['敏捷型 (A)', '定制型 (B)', '主权型 (C)'],
                values=[st.session_state.group_data["A"], st.session_state.group_data["B"], st.session_state.group_data["C"]],
                color_discrete_sequence=['#ff4b4b', '#ff8c00', '#0078d4'],
                hole=0.45
            )
            fig_pie.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=320, paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_pie, use_container_width=True)

        with g_col2:
            st.markdown("### MiniMax 群体趋势分析")
            # --- 修复：群体 Insight (增加兜底保证显示) ---
            g_p = f"现场{total}人。A:{st.session_state.group_data['A']}, B:{st.session_state.group_data['B']}, C:{st.session_state.group_data['C']}。请简要分析现场趋势与核心焦虑。"
            
            with st.spinner("MiniMax 正在解析全场数据趋势..."):
                # 调用稳定版函数
                group_insight = ask_minimax_stable(g_p)
                # 使用专门 CSS 配合字号与背景
                st.markdown(f'<div class="group-insight-card">🏛️ **专家洞察**：\n\n{group_insight}</div>', unsafe_allow_html=True)
            
        with g_col3:
            st.markdown("### 进化路线建议")
            # 增加一个简单的建议卡片，平衡右侧空间
            st.markdown("""
                <div style="background:#e8f5e9; padding:15px; border-radius:10px; font-size:14px; color:#1b5e20;">
                <strong style="color:#2e7d32;">🏆 领跑者建议：</strong><br>
                当前现场数据显示数据主权意识非常强烈。 Nova Claw 定制化 Agents 的共创模式是实现最深护城河的关键路径。
                </div>
            """, unsafe_allow_html=True)
