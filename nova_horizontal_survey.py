import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests

# --- 1. 页面配置与超强视觉样式 ---
st.set_page_config(page_title="AI 进阶路径诊断", layout="wide")

st.markdown("""
    <style>
    /* 基础背景与森林绿配色 */
    .stApp { background-color: #F8FAF8 !important; }
    
    /* 强力修复：放大 Tabs 标签字号 */
    button[data-baseweb="tab"] { font-size: 24px !important; font-weight: 600 !important; color: #2E7D32 !important; padding: 10px 20px !important; }
    button[aria-selected="true"] { border-bottom: 4px solid #2E7D32 !important; background-color: #E8F5E9 !important; }

    /* 统一文字颜色与字号 */
    h1, h2, h3 { color: #1B5E20 !important; font-family: "Microsoft YaHei", sans-serif; }
    .stRadio label { font-size: 18px !important; color: #37474F !important; font-weight: 500 !important; }
    
    /* 诊断结果卡片 */
    .result-card {
        background: white; border-radius: 20px; padding: 30px;
        border: 2px solid #E0E0E0; box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        text-align: center; margin-bottom: 20px;
    }
    .big-icon { font-size: 110px; margin: 0; }
    
    /* 专家洞见卡片：高级青绿渐变 */
    .insight-card {
        background: linear-gradient(145deg, #ffffff, #f1f8e9);
        border-left: 8px solid #4CAF50; border-radius: 12px;
        padding: 25px; margin-top: 25px;
        box-shadow: 4px 4px 15px rgba(0,0,0,0.05);
        color: #1B5E20; font-size: 17px; line-height: 1.8;
    }
    
    /* 隐藏 Plotly 模式栏提高高级感 */
    .modebar { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. 数据持久化逻辑 ---
if 'group_results' not in st.session_state:
    st.session_state.group_results = {"A": 3, "B": 2, "C": 1} # 预设初始值
if 'saved_insight' not in st.session_state:
    st.session_state.saved_insight = None
if 'user_scores' not in st.session_state:
    st.session_state.user_scores = {"Agile": 0, "Collab": 0, "Sovereignty": 0}

# --- 3. 稳定的大模型调用函数 ---
def fetch_ai_analysis(prompt, fallback):
    key = st.secrets.get("MINIMAX_API_KEY")
    gid = st.secrets.get("MINIMAX_GROUP_ID")
    if not key: return fallback
    try:
        url = f"https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId={gid}"
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        payload = {
            "model": "abab6.5-chat",
            "messages": [{"sender_type": "USER", "sender_name": "User", "text": prompt}],
            "bot_setting": [{"region": "China", "content": "你是一位拥有20年经验的企业数字化转型首席顾问。"}]
        }
        r = requests.post(url, headers=headers, json=payload, timeout=12)
        return r.json()['reply']
    except:
        return fallback

# --- 4. 标题部分 ---
st.title("🦞 小龙虾时代 · 企业 AI 进阶路径全景诊断")
st.markdown("#### 世纪公园 · 一尺花园分享会 | 探索您的企业 AI 进化终点")

tab_personal, tab_group = st.tabs(["📋 个人路径诊断", "📊 现场洞察看板"])

with tab_personal:
    col_survey, col_result = st.columns([6, 4], gap="large")
    
    with col_survey:
        with st.form("main_survey"):
            st.markdown("### 🧬 核心维度探测")
            s1, s2 = st.columns(2)
            with s1:
                v1 = st.radio("1. 公有云 AI 态度", ["A. 效率优先", "B. 稳健监管", "C. 严格禁入"])
                v2 = st.radio("2. 核心数据访问", ["A. 结果导向", "B. 大厂托管", "C. 物理不出场"])
                v3 = st.radio("3. 数据所有权", ["A. 无所谓", "B. 合同约定", "C. 必须私有"])
                v4 = st.radio("4. 业务场景复杂度", ["A. 文字基础", "B. 流程协同", "C. 核心逻辑"])
            with s2:
                v5 = st.radio("5. 定制化要求", ["A. 标准化", "B. 模块化", "C. 深度定制"])
                v6 = st.radio("6. 智能体矩阵", ["A. 散点工具", "B. 组织统筹", "C. 矩阵作战"])
                v7 = st.radio("7. 采购核心价值", ["A. 快速尝试", "B. 长期基建", "C. 价值溢价"])
                v8 = st.radio("8. 掌控感要求", ["A. 使用者", "B. 跟随者", "C. 最高主权"])
            
            st.write("")
            btn_submit = st.form_submit_button("🌱 立即生成 AI 诊断报告")

    with col_result:
        # 实时计算分类
        all_ans = [v1, v2, v3, v4, v5, v6, v7, v8]
        c_val = sum(1 for x in all_ans if "C." in x)
        
        if c_val >= 5:
            icon, name, color = "🦀", "殿堂·帝王蟹 (ME7)", "#1565C0"
        elif c_val >= 2:
            icon, name, color = "🦞", "进阶·大龙虾 (Nova)", "#EF6C00"
        else:
            icon, name, color = "🦐", "敏捷·小龙虾 (OpenClaw)", "#C62828"

        # 结果展示卡片
        st.markdown(f"""
            <div class="result-card" style="border-top: 8px solid {color};">
                <div class="big-icon">{icon}</div>
                <h2 style="color:{color}; margin-top:0;">{name}</h2>
                <p style="color:#666; font-size:16px;">基于您的安全主权与业务深度判定</p>
            </div>
        """, unsafe_allow_html=True)

        if btn_submit:
            # 更新统计
            key = "C" if c_val >= 5 else ("B" if c_val >= 2 else "A")
            st.session_state.group_results[key] += 1
            
            # 更新能量条分数 (存入 session_state)
            st.session_state.user_scores = {
                "Agile": sum(1 for x in all_ans if "A." in x),
                "Collab": sum(1 for x in all_ans if "B." in x),
                "Sovereignty": c_val
            }
            
            # 生成洞见并保存
            p = f"企业诊断为{name}，偏向{v1}和{v2}。请给出三条针对性的进阶建议，150字内。"
            fb = f"**专家建议**：您的企业已进入{name}阶段。当前核心任务是确立‘数据主权’边界，建议优先将{v4[3:]}场景进行私有化 Agent 封装，实现智慧资产的永久留存。"
            with st.spinner("AI 正在深度扫描您的数字化基因..."):
                st.session_state.saved_insight = fetch_ai_analysis(p, fb)
            st.balloons()

        # --- 核心升级：高级感能量条展示 (Bullet Chart) ---
        if st.session_state.user_scores["Agile"] + st.session_state.user_scores["Collab"] + st.session_state.user_scores["Sovereignty"] > 0:
            st.markdown("#### ⚡ 进阶维度能量分布")
            s = st.session_state.user_scores
            # 使用 Plotly 条形图替代雷达图，视觉更清爽
            fig_bar = go.Figure()
            categories = ['Agile', 'Collab', 'Sovereign']
            values = [s["Agile"], s["Collab"], s["Sovereignty"]]
            colors = ['#FFCDD2', '#FFE0B2', '#BBDEFB'] # 柔和色
            
            fig_bar.add_trace(go.Bar(
                y=categories, x=values, orientation='h',
                marker=dict(color=[color, color, color], line=dict(width=0)),
                text=values, textposition='auto',
            ))
            fig_bar.update_layout(
                height=220, margin=dict(l=10, r=10, t=10, b=10),
                xaxis=dict(range=[0, 8], showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(autorange="reversed"), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})

        # --- 专家洞见持久化显示 ---
        if st.session_state.saved_insight:
            st.markdown(f"""
                <div class="insight-card">
                    <strong>🏛️ 大模型首席顾问 Insight：</strong><br>
                    {st.session_state.saved_insight}
                </div>
            """, unsafe_allow_html=True)

with tab_group:
    st.header("📊 现场实时洞察看板")
    counts = st.session_state.group_results
    total = sum(counts.values())
    
    # 顶部 KPI：更大、更清晰
    k1, k2, k3, k4 = st.columns(4)
    k1.markdown(f'<div class="result-card">参与人数<br><b style="font-size:40px;">{total}</b></div>', unsafe_allow_html=True)
    k2.markdown(f'<div class="result-card">小龙虾(A)<br><b style="font-size:40px;color:#C62828;">{counts["A"]}</b></div>', unsafe_allow_html=True)
    k3.markdown(f'<div class="result-card">大龙虾(B)<br><b style="font-size:40px;color:#EF6C00;">{counts["B"]}</b></div>', unsafe_allow_html=True)
    k4.markdown(f'<div class="result-card">帝王蟹(C)<br><b style="font-size:40px;color:#1565C0;">{counts["C"]}</b></div>', unsafe_allow_html=True)

    if total > 0:
        st.write("---")
        g_left, g_right = st.columns([5, 5])
        with g_left:
            # 环形图：手动锁定专业色，字号加大
            fig_pie = px.pie(
                names=['OpenClaw (A)', 'Nova (B)', 'ME7 (C)'],
                values=[counts["A"], counts["B"], counts["C"]],
                color_discrete_sequence=['#C62828', '#EF6C00', '#1565C0'],
                hole=0.5
            )
            fig_pie.update_traces(textinfo='percent+label', textfont_size=20, marker=dict(line=dict(color='#FFFFFF', width=2)))
            fig_pie.update_layout(showlegend=False, height=450)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with g_right:
            st.markdown("### 🏛️ 全场 AI 进化趋势解析")
            if st.button("🛰️ 启动全景数据扫描"):
                gp = f"全场共{total}人。A:{counts['A']}, B:{counts['B']}, C:{counts['C']}。请给出一段极具煽动性且专业的现场分析。"
                g_fb = "现场数据显示，**主权意识（C型）** 正在成为主流。这标志着管理者已从单纯追求效率，转向追求数字化资产的深度自持。这正是‘大龙虾计划’的核心使命。"
                with st.spinner("AI 正在分析全场管理者焦虑点..."):
                    res_g = fetch_ai_analysis(gp, g_fb)
                    st.success(res_g)
            else:
                st.info("点击上方按钮，获取 AI 对全场趋势的深度解析。")
            
            st.warning("🎁 提示：现场将随机抽取 **Mac Mini**，请确保已提交个人评测。")
