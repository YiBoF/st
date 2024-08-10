import streamlit as st  # 引入Streamlit库，用于创建Web应用
import pandas as pd  # 引入Pandas库，用于数据处理和分析
import matplotlib.pyplot as plt  # 引入Matplotlib库，用于绘图
import seaborn as sns  # 引入Seaborn库，用于高级绘图
import plotly.express as px  # 引入Plotly Express库，用于交互式绘图
import numpy as np  # 引入NumPy库，用于科学计算
import torch  # 引入PyTorch库，用于机器学习和深度学习
import requests  # 引入Requests库，用于发送HTTP请求
from requests.auth import HTTPBasicAuth

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
            # 将响应数据解析为JSON格式
            result = response.json()
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
st.title("教育决策平台数据可视化")

# 从Druid加载数据
# data_from_druid = get_data_from_druid()
data_from_druid = None
# 检查是否成功获取数据
if data_from_druid is not None:
    st.markdown("### 使用Druid数据")
    # 将从Druid获取的数据存储在字典中
    dataframes = {'Druid数据': data_from_druid}
else:
    # 如果未能获取数据，则生成模拟数据
    dataframes = {'模拟数据': generate_data()}

# 选择要显示的数据表
table_names = list(dataframes.keys())  # 获取数据表名称列表
selected_table = st.selectbox("选择要显示的数据表", table_names)  # 创建下拉选择框供用户选择数据表
data = dataframes[selected_table]  # 根据用户选择加载对应的数据

# 选择要显示的数据项
columns = data.columns.tolist()  # 获取数据表的所有列名
# 创建多选框供用户选择要显示的列，默认选择前两列
selected_columns = st.multiselect("选择要显示的数据项", columns, default=columns[:2])

# 自定义图表样式的侧边栏
st.sidebar.header("自定义图表样式")  # 在侧边栏添加标题
# 创建下拉选择框供用户选择图表类型
chart_type = st.sidebar.selectbox("选择图表类型", ["面积图", "折线图", "柱状图", "散点图", "位置散点图", "热力图", "3D图"])

# 定义颜色列表，用于图表的颜色
color_palette = sns.color_palette("husl", len(selected_columns))

# 显示选定的数据项
st.write("### 选定的数据项", data[selected_columns])

# 根据选择的图表类型创建图表
if chart_type == "面积图":
    # 创建一个占位符
    placeholder = st.empty()
    stack = False
    with placeholder.container():
        # 创建一个布尔类型的选择框
        checkbox_value = st.checkbox('启用堆栈转换为蒸汽图')
        # 根据选择框的状态改变stack的值
        if checkbox_value:
            stack = "center"
        else:
            stack = False
    try:
        st.area_chart(data[selected_columns], stack=stack)
    except:
        placeholder.empty()
        st.area_chart(data[selected_columns])
    

elif chart_type == "折线图":
    
    st.line_chart(data[selected_columns])

elif chart_type == "柱状图":
    # 创建一个占位符
    placeholder = st.empty()
    stack = True
    with placeholder.container():
        # 创建一个布尔类型的选择框
        checkbox_value = st.checkbox('关闭堆叠')

        # 根据选择框的状态改变stack的值
        if checkbox_value:
            stack = False
        else:
            stack = True
    try:
        st.bar_chart(data[selected_columns], stack=stack)
    except:
        placeholder.empty()
        st.bar_chart(data[selected_columns])

elif chart_type == "散点图":

    st.scatter_chart(data[selected_columns])

elif chart_type == "位置散点图":
    if any(col in selected_columns for col in ['LAT', 'LATITUDE', 'lat', 'latitude']):
        if any(col in selected_columns for col in ['LON', 'LONGITUDE', 'lon', 'longitude']):
            st.map(data[selected_columns])
        else: st.error("请选择经度lon")

    else: st.error("请选择纬度lat和经度lon")

elif chart_type == "热力图":
    fig, ax = plt.subplots()  # 创建Matplotlib图和轴对象
    # 使用Seaborn绘制热力图，显示数据列的相关系数
    sns.heatmap(data[selected_columns].corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)  # 在Streamlit应用中显示图表

elif chart_type == "3D图":
    if len(selected_columns) >= 3:
        # 使用Plotly绘制3D散点图
        fig = px.scatter_3d(data, x=selected_columns[0], y=selected_columns[1], z=selected_columns[2])
        fig.update_traces(marker=dict(color=color_palette[0]))  # 更新标记颜色
        st.plotly_chart(fig)  # 在Streamlit应用中显示图表
    else:
        # 如果选定的列少于3列，显示错误信息
        st.error("请至少选择三列数据用于3D图表")

# 开发10套可视化模板
st.write("### 可视化模板")
templates = ["模板1", "模板2", "模板3", "模板4", "模板5", "模板6", "模板7", "模板8", "模板9", "模板10", "模板11", "模板12"]
# 创建下拉选择框供用户选择模板
selected_template = st.selectbox("选择可视化模板", templates)

st.write(f"您选择了: {selected_template}")

# 根据选择的模板显示相应的图表
if selected_template == "模板1":
    st.write("模板1: 面积图")
    st.area_chart(data[selected_columns])

elif selected_template == "模板2":
    st.write("模板2: 折线图")
    st.line_chart(data[selected_columns])

elif selected_template == "模板3":
    st.write("模板3: 柱状图")
    st.bar_chart(data[selected_columns])

elif selected_template == "模板4":
    st.write("模板4: 散点图")
    st.scatter_chart(data[selected_columns])

elif selected_template == "模板5":
    st.write("模板5: 位置散点图")
    st.map(data[selected_columns])

elif selected_template == "模板6":
    st.write("模板6: 热力图")
    fig, ax = plt.subplots()  # 创建Matplotlib图和轴对象
    # 使用Seaborn绘制热力图，显示数据列的相关系数
    sns.heatmap(data[selected_columns].corr(), annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)  # 在Streamlit应用中显示图表

elif selected_template == "模板7":
    st.write("模板7: 3D图")
    if len(selected_columns) >= 3:
        # 使用Plotly绘制3D散点图
        fig = px.scatter_3d(data, x=selected_columns[0], y=selected_columns[1], z=selected_columns[2])
        fig.update_traces(marker=dict(color=color_palette[0]))  # 更新标记颜色
        st.plotly_chart(fig)  # 在Streamlit应用中显示图表
    else:
        # 如果选定的列少于3列，显示错误信息
        st.error("请至少选择三列数据用于3D图表")

elif selected_template == "模板8":
    st.write("模板8: 箱线图")
    fig, ax = plt.subplots()  # 创建Matplotlib图和轴对象
    # 使用Seaborn绘制箱线图
    sns.boxplot(data=data[selected_columns], ax=ax)
    st.pyplot(fig)  # 在Streamlit应用中显示图表

elif selected_template == "模板9":
    st.write("模板9: 小提琴图")
    fig, ax = plt.subplots()  # 创建Matplotlib图和轴对象
    # 使用Seaborn绘制小提琴图
    sns.violinplot(data=data[selected_columns], ax=ax)
    st.pyplot(fig)  # 在Streamlit应用中显示图表

elif selected_template == "模板10":
    st.write("模板10: 密度图")
    fig, ax = plt.subplots()  # 创建Matplotlib图和轴对象
    # 使用Seaborn绘制密度图
    sns.kdeplot(data[selected_columns[0]], ax=ax, shade=True)
    st.pyplot(fig)  # 在Streamlit应用中显示图表

elif selected_template == "模板11":
    st.write("模板11: 直方图")
    fig, ax = plt.subplots()  # 创建Matplotlib图和轴对象
    # 绘制直方图
    data[selected_columns[0]].plot(kind='hist', ax=ax, color=color_palette[0])
    st.pyplot(fig)  # 在Streamlit应用中显示图表

elif selected_template == "模板12":
    st.write("模板12: 折线图（PyTorch生成数据）")
    # 使用PyTorch生成数据
    x = torch.linspace(0, 10, 100)
    y = torch.sin(x)
    fig, ax = plt.subplots()  # 创建Matplotlib图和轴对象
    # 绘制折线图
    ax.plot(x.numpy(), y.numpy(), color=color_palette[0])
    st.pyplot(fig)  # 在Streamlit应用中显示图表
