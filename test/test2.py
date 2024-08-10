import streamlit as st  # 引入Streamlit库，用于创建Web应用
import pandas as pd  # 引入Pandas库，用于数据处理和分析
import numpy as np  # 引入NumPy库，用于科学计算


# 生成模拟数据的函数
def generate_data():
    # 固定随机数种子以确保每次运行生成相同的数据
    np.random.seed(42)
    # 生成包含4列随机数据的数据框，每列有100个数据点
    data = pd.DataFrame({
        'A': np.random.randn(100),
        'B': np.random.randn(100),
        'C': np.random.randn(100),
        'D': np.random.randn(100),
        'lat': np.random.randn(100) / 40 + 23,  # 35.0, 105.0 是中国的中心位置
        'lon': np.random.randn(100) / 40 + 113.8,  # 35.0, 105.0 是中国的中心位置
    })
    # # 限制纬度和经度范围在中国境内
    # data['lat'] = data['lat'].clip(lower=30, upper=50)  # 纬度范围
    # data['lon'] = data['lon'].clip(lower=73, upper=135)  # 经度范围
    return data  # 返回生成的数据框

# 设置页面标题
st.title("测试模拟数据生成")

data_from_druid = None
# 检查是否成功获取数据
if data_from_druid is not None:
    st.markdown("### 使用Druid数据")
    # 将从Druid获取的数据存储在字典中
    dataframes = {'Druid数据': data_from_druid}
else:
    # 如果未能获取数据，则生成模拟数据
    dataframes = {'模拟数据': generate_data()}

st.write(generate_data())