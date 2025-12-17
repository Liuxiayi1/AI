import streamlit as st
import pdfplumber
import pandas as pd
import fitz  # PyMuPDF
import io
from PIL import Image

# 设置页面配置
st.set_page_config(page_title="PDF工具箱", page_icon="📄", layout="wide")

st.title("📄 PDF 表格与图片提取工具")
st.markdown("上传 PDF 文件，轻松提取其中的表格和图片。")

# 文件上传
uploaded_file = st.file_uploader("请上传或者拖拽 PDF 文件", type=["pdf"])

if uploaded_file:
    # 读取文件内容，以便多次使用
    file_bytes = uploaded_file.read()
    
    # 创建两个 Tab
    tab1, tab2 = st.tabs(["📊 表格提取", "🖼️ 图片提取"])

    # --- 表格提取部分 ---
    with tab1:
        st.header("提取的表格")
        
        extract_btn = st.button("开始提取表格")
        
        if extract_btn:
            all_tables = []
            with st.spinner("正在提取表格..."):
                try:
                    # 使用 pdfplumber 打开
                    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                        for i, page in enumerate(pdf.pages):
                            tables = page.extract_tables()
                            for table in tables:
                                # 处理可能为空的表头或数据
                                if not table:
                                    continue
                                    
                                # 处理表头：转为字符串并处理 None
                                headers = []
                                if table[0]:
                                    headers = [str(c) if c is not None else f"Col_{k}" for k, c in enumerate(table[0])]
                                else:
                                    # 如果第一行为空，自动生成列名
                                    headers = [f"Col_{k}" for k in range(len(table[0] if len(table)>0 else []))]

                                # 创建 DataFrame
                                if len(table) > 1:
                                    df = pd.DataFrame(table[1:], columns=headers)
                                else:
                                    # 只有表头的情况
                                    df = pd.DataFrame([], columns=headers)
                                    
                                all_tables.append((i + 1, df))
                    
                    if not all_tables:
                        st.warning("未在 PDF 中检测到表格。")
                    else:
                        st.success(f"共提取到 {len(all_tables)} 个表格。")
                        
                        # 准备用于导出的 Excel Writer
                        output = io.BytesIO()
                        try:
                            # 使用 engine='openpyxl'
                            writer = pd.ExcelWriter(output, engine='openpyxl')
                            saved_sheets = 0
                            
                            for idx, (page_num, df) in enumerate(all_tables):
                                st.subheader(f"表格 {idx + 1} (第 {page_num} 页)")
                                st.dataframe(df)
                                
                                try:
                                    # 构建 Sheet 名称
                                    sheet_name = f"Page_{page_num}_Table_{idx+1}"
                                    # 清理非法字符
                                    invalid_chars = [':', '\\', '/', '?', '*', '[', ']']
                                    for char in invalid_chars:
                                        sheet_name = sheet_name.replace(char, '_')
                                    # 截断长度
                                    if len(sheet_name) > 31:
                                        sheet_name = sheet_name[:31]
                                    
                                    # 写入
                                    df.to_excel(writer, sheet_name=sheet_name, index=False)
                                    saved_sheets += 1
                                except Exception as e_sheet:
                                    st.warning(f"无法写入表格 {idx+1} 到 Excel: {e_sheet}")

                            # 只有成功写入至少一个 Sheet 才保存
                            if saved_sheets > 0:
                                writer.close()
                                output.seek(0)
                                st.download_button(
                                    label="📥 导出所有表格为 Excel",
                                    data=output,
                                    file_name="extracted_tables.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                            else:
                                st.warning("未能生成有效的 Excel 文件（没有表格被成功写入）。")
                                
                        except Exception as e_excel:
                            st.error(f"生成 Excel 文件时发生错误: {e_excel}")
                        
                except Exception as e:
                    st.error(f"提取表格时出错: {e}")

    # --- 图片提取部分 ---
    with tab2:
        st.header("提取的图片")
        
        extract_img_btn = st.button("开始提取图片")
        
        if extract_img_btn:
            with st.spinner("正在提取图片..."):
                try:
                    # 使用 PyMuPDF (fitz) 打开
                    doc = fitz.open(stream=file_bytes, filetype="pdf")
                    image_count = 0
                    
                    # 准备显示图片的列
                    cols = st.columns(3)
                    
                    for page_index in range(len(doc)):
                        page = doc[page_index]
                        image_list = page.get_images(full=True)
                        
                        if image_list:
                            for image_index, img in enumerate(image_list):
                                xref = img[0]
                                base_image = doc.extract_image(xref)
                                image_bytes = base_image["image"]
                                image_ext = base_image["ext"]
                                
                                # 使用 PIL 处理图片以便显示
                                image = Image.open(io.BytesIO(image_bytes))
                                
                                # 在列中显示
                                col = cols[image_count % 3]
                                with col:
                                    st.image(image, caption=f"第 {page_index + 1} 页 - 图片 {image_index + 1}", use_container_width=True)
                                    
                                    # 单张下载按钮
                                    st.download_button(
                                        label="📥 下载",
                                        data=image_bytes,
                                        file_name=f"page_{page_index+1}_img_{image_index+1}.{image_ext}",
                                        mime=f"image/{image_ext}",
                                        key=f"btn_{page_index}_{image_index}"
                                    )
                                
                                image_count += 1
                    
                    if image_count == 0:
                        st.warning("未在 PDF 中检测到图片。")
                    else:
                        st.success(f"共提取到 {image_count} 张图片。")
                        
                except Exception as e:
                    st.error(f"提取图片时出错: {e}")

else:
    st.info("请在上方上传 PDF 文件以开始使用。")
