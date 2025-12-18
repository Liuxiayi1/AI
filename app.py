import streamlit as st
import pandas as pd
import os

# 设置页面标题和说明
st.title('企业数字化转型指数查询系统')
st.write('本系统基于1999-2023年的数据，支持通过股票代码查询企业的数字化转型指数')

# 读取jgb.csv和gjc.csv文件
try:
    # 读取主要数据文件jgb.csv，包含数字化转型指数，将股票代码列设置为字符串类型
    jgb_df = pd.read_csv('jgb.csv', dtype={'股票代码': str})
    
    # 读取补充数据文件gjc.csv，将股票代码列设置为字符串类型
    gjc_df = pd.read_csv('gjc.csv', dtype={'股票代码': str})
    
    st.success('数据加载成功！')
    
except FileNotFoundError:
    st.error('找不到数据文件(jgb.csv或gjc.csv)，请确保文件在正确的目录下')
    st.stop()

# 获取所有股票代码列表
stock_codes = jgb_df['股票代码'].unique().tolist()
stock_codes.sort()  # 排序以便用户查找

# 获取所有年份列表
years = jgb_df['年份'].unique().tolist()
years.sort()  # 排序以便用户查找

# 添加股票代码输入框
selected_stock = st.text_input('请输入股票代码', placeholder='例如：000921')

# 添加年份选择器
selected_year = st.selectbox('请选择年份', options=years)

# 查询按钮
if st.button('查询'):
    if not selected_stock:
        st.warning('请输入股票代码')
    else:
        # 过滤数据
        result = jgb_df[(jgb_df['股票代码'] == selected_stock) & (jgb_df['年份'] == selected_year)]
        
        if result.empty:
            st.warning(f'未找到股票代码{selected_stock}在{selected_year}年的数据')
        else:
            # 显示查询结果
            st.subheader('查询结果')
            st.write(f'股票代码：{result.iloc[0]["股票代码"]}')
            st.write(f'企业名称：{result.iloc[0]["企业名称"]}')
            st.write(f'年份：{result.iloc[0]["年份"]}')
            st.write(f'数字化转型指数(0-100分)：{result.iloc[0]["数字化转型指数(0-100分)"]}')
            
            # 显示更多相关数据
            st.subheader('详细技术词频数据')
            tech_columns = ['人工智能词频数', '大数据词频数', '云计算词频数', '区块链词频数', '数字技术运用词频数']
            for col in tech_columns:
                st.write(f'{col}：{result.iloc[0][col]}')

# 添加数据概览部分
st.subheader('数据概览')
# 显示数据的基本统计信息
st.write(f'数据年份范围：{min(years)}-{max(years)}')
st.write(f'包含企业数量：{len(stock_codes)}家')

# 添加数据可视化示例（可选）
if st.checkbox('显示数字化转型指数分布'):
    import matplotlib.pyplot as plt
    
    # 按年份显示数字化转型指数的分布
    fig, ax = plt.subplots(figsize=(10, 6))
    jgb_df.boxplot(column='数字化转型指数(0-100分)', by='年份', ax=ax, rot=45)
    plt.title('各年份数字化转型指数分布')
    plt.suptitle('')  # 移除默认标题
    plt.ylabel('数字化转型指数(0-100分)')
    st.pyplot(fig)

# 添加显示原始数据表格的功能
st.subheader('查看原始数据')
# 创建选项卡
selected_tab = st.radio('选择要查看的数据集：', ['1999-2023年数字化转型指数结果表', '1999-2023年年报技术关键词统计'])

# 根据选择显示不同的数据表格
if selected_tab == '1999-2023年数字化转型指数结果表':
    st.write('1999-2023年数字化转型指数结果表文件内容：')
    st.dataframe(jgb_df)
else:
    st.write('1999-2023年年报技术关键词统计文件内容：')
    st.dataframe(gjc_df)