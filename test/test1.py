import streamlit as st  # 引入Streamlit库，用于创建Web应用
import pandas as pd  # 引入Pandas库，用于数据处理和分析
import requests  # 引入Requests库，用于发送HTTP请求
from requests.auth import HTTPBasicAuth
import json

USERNAME = "admin"
PASSWORD = "password1"

# 从Druid数据仓库获取数据的函数
def get_data_from_druid():
    try:
        # 设置Druid连接参数，包含URL和查询语句
        # druid_url = 'http://10.60.55.200:8081/druid/v2/sql'
        druid_url = 'http://127.0.0.1:8082/druid/v2/sql'
        query = {
            "query": "SELECT * FROM 测试数据"  # 将此处的查询改为适合你的Druid表的实际查询
        }
        # 发送HTTP POST请求到Druid，获取数据
        
        response = requests.post(druid_url, json=query, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth(USERNAME, PASSWORD))
        # 检查响应状态码是否为200（表示成功）
        if response.status_code == 200:
            text = response.text
            clean_data = text.replace('\ufeff', '')  # 去除 BOM 字符
            # 将响应数据解析为JSON格式
            result = json.loads(clean_data)
            # 将JSON数据转换为Pandas DataFrame
            df = pd.DataFrame(result)
            return df  # 返回数据框
        else:
            # 如果请求失败，显示错误信息
            st.error(f"请求失败: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        # 捕捉所有异常并显示错误信息
        st.error(f"从Druid获取数据时出错: {e}")
        return None

# 设置页面标题
st.title("测试数据仓库Druid数据源获取")

dataFrame = get_data_from_druid()
st.write(dataFrame)