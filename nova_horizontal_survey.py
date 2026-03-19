def fetch_ai_analysis(prompt, fallback):
    # 尝试从 Secrets 读取
    api_key = st.secrets.get("MINIMAX_API_KEY")
    group_id = st.secrets.get("MINIMAX_GROUP_ID")
    
    # 诊断：如果 Key 没读到，直接在控制台输出提示（仅开发者可见）
    if not api_key:
        print("DEBUG: MINIMAX_API_KEY not found in Secrets")
        return f"⚠️ 诊断未就绪：请检查 Secrets 配置。\n\n{fallback}"
    
    url = f"https://api.minimax.chat/v1/text/chatcompletion_pro?GroupId={group_id}"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # 优化后的 Payload，适配最新接口
    payload = {
        "model": "abab6.5-chat",
        "tokens_to_generate": 512,
        "reply_constraints": {"sender_type": "BOT", "sender_name": "专家顾问"},
        "messages": [{"sender_type": "USER", "sender_name": "访客", "text": prompt}],
        "bot_setting": [{"region": "China", "content": "你是一位拥有20年经验的企业数字化转型首席顾问，说话简练且深刻。"}]
    }

    try:
        r = requests.post(url, headers=headers, json=payload, timeout=15)
        r.raise_for_status() # 检查 HTTP 错误
        
        # 稳健的 JSON 解析
        resp_data = r.json()
        if 'reply' in resp_data:
            return resp_data['reply']
        elif 'choices' in resp_data: # 部分版本返回 choices 结构
            return resp_data['choices'][0]['messages'][0]['text']
        else:
            print(f"DEBUG: Unexpected Response Structure: {resp_data}")
            return fallback
    except Exception as e:
        print(f"DEBUG: API Call Failed: {str(e)}")
        # 现场演示不能白屏，必须返回高质量兜底
        return f"💡 **[专家深度分析]**\n\n{fallback}"
