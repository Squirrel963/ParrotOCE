import streamlit as st
import time
import random
import sys
from io import StringIO
import pandas as pd
import importlib
import subprocess
from decimal import Decimal
import numpy
#import translators as ts
import importlib

version = "1.38"

st.set_page_config(
    page_title="Parrot OCE",
    page_icon="🦜",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Squirrel963/ParrotOCE',
        'Report a bug': "https://github.com/Squirrel963/ParrotOCE/issues",
        'About': f'''# Parrot Online Code Environment v{version}  
        用于python在线运行、调试  
        开源许可证：GPL-3.0'''
    }
)

st.title("Parrot OCE")
st.caption(f'''Parrot Online Code Environment： v{version}        
python：{sys.version}''')

@st.dialog("Python运行结果",width="large")
def vote(text, allowta:bool, allowdown=True, types='normal', colors="blue"):
    try:
        if allowdown:
            st.download_button(
                label=":material/save_alt: 下载输出内容",
                data=f"{text}",
                #type="primary",
                file_name="output.txt",
            )
        if types == 'normal':
            st.code(f"{text}")
        elif types == 'bool':
            st.badge(f"{text}",color=colors)
        if allowta:
            with st.expander("翻译为中文"):
                if st.button(":material/translate:  立即翻译"):
                    with st.spinner("翻译中..."):
                        translation = translat(f"{text}")
                        st.write(translation)
    except ValueError as e:
        st.error(":material/warning:  int数字大小超限!")

@st.dialog("POCE运行错误",width="large")
def errors(text):
    e = RuntimeError(f":material/warning:  {text}")
    st.error(e)
    if st.button("确定"):
        st.rerun()

def run(command : list):
    #command = ["ping", "127.0.0.1", "-n", "4"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process.wait()

    stdout, stderr = process.communicate()
    #print(stdout)
    #print(stderr)
    #print("退出代码：")
    reback = {
        "code":process.returncode,
        "out":stdout,
        "error":stderr
    }
    return reback

def format_to_scientific(value, precision=6):
    if isinstance(value, (int, float)):
        decimal_value = Decimal(str(value))
        return "{:.{}e}".format(decimal_value, precision)
    elif isinstance(value, str):
        return value
    else:
        return str(value)

def split_text_into_chunks(text, max_length):
    # 按照换行符分割文本
    lines = text.splitlines()
 
    chunks = []
    current_chunk = ""
    
    for line in lines:
        if len(current_chunk) + len(line) + 1 > max_length:
            chunks.append(current_chunk)
            current_chunk = line
        else:
            if current_chunk:
                current_chunk += "\n" + line
            else:
                current_chunk = line
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks
#https://github.com/UlionTse/translators
def translat(text):
    translated_text=text
    trans_text = ""
    for line in split_text_into_chunks(translated_text, 1000): 
        trans_text+=ts.translate_text(line,from_language='en',to_language='zh')
    return trans_text


# 示例用法
# print(format_to_scientific(123456789))          # 输出: 1.234568e+08
# print(format_to_scientific(0.000123456))        # 输出: 1.234568e-04
# print(format_to_scientific("Hello, World!"))    # 输出: Hello, World!
# print(format_to_scientific("12345"))            # 输出: 12345

# @st.dialog("确认运行")
# def vpass(passl, code):
#     print(f"远程终端申请运行命令：{passl}")
#     st.write("请输入本地控制台输出的密钥来确认运行")
#     passc = st.text_input("passkey")#,label_visibility="collapsed")
#     if st.button("确定"):
#         if passc == passl:
#             exec(code)
#         else:
#             st.rerun()
            
# litters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
# def randoc(seed : int):
#     random.shuffle(litters)
#     resultdoc = ""
#     randseed = list(str(random.randint(int('1'+'0'*(seed-1)),int('9'*seed))))
#     #print(randseed)
#     for i in range(seed):
#         resultdoc += str(litters[int(randseed[i])])
#     return resultdoc


# passcode = randoc(6)
# #st.write(passcode)
# #key_button = st.text_input("pass key")


Unsupported = [
    "input",
    "turtle",
    "pygame",
    "os",
    "sys",
    "subprocess",
    "importlib",
    "Ropen",
    "Rinput",
    "streamlit",
    "Radmin_code",
    "Rvote"
]

col1, col2 = st.columns([0.7,0.3])
with col1:
    codes = st.text_area(":material/code:  Python代码块",height=400,value='''print("hello POCE!")
print("I love python3.10!")''')
    st.download_button(
        label=":material/download: 下载代码块",
        data=codes,
        #type="primary",
        file_name="POCE_code.py",
    )

with col2:
    #with st.container(border=True):
        option = st.radio(
        ":material/memory:  运行器",
        ("POCE内置", "Eval", "WT远程执行"),
        captions=[
            "用于处理复杂代码",
            "适用于数学及字符串运算",
            "在远程WT服务器上执行",
        ],
        )
        if option == "WT远程执行":
            WT_address = st.text_input("WT服务器地址")
            WT_password = st.text_input("WT服务器密钥")
        elif option == "Eval":
            snf = st.toggle("结果采用科学计数法")
        if st.button(":material/build:  运行",use_container_width=True):
            with st.spinner("运行代码中..."):
                code = codes
                result = "没有可用结果输出"
                allowth = True
                sp = True
                found_usp = []
                for i in Unsupported:
                        if not 'R' in i:
                            if f"import {i}" in code:
                                sp = False
                                found_usp.append(i)
                        else:
                            if i.replace("R","") in code:
                                sp = False
                                found_usp.append(i.replace("R",""))
                if sp:
                    if option == "POCE内置":
                        captured_output = StringIO()
                        original_stdout = sys.stdout
                        sys.stdout = captured_output
                        code_to_execute = codes
                        try:
                            exec(code_to_execute, globals())
                            result_vars = locals()
                        except Exception as e:
                            result = f"运行错误: {str(e)}"
                        else:
                            output = captured_output.getvalue().strip()
                            result = output or result_vars.get('result', None)
                        finally:
                            sys.stdout = original_stdout
                        if result == "没有可用结果输出":
                            allowth = False
                        vote(result,allowta=allowth,allowdown=allowth)
                    elif option == "Eval":
                        try:
                            if eval(code) == True:
                                vote(":material/check: 成立",types='bool',colors='green',allowta=False,allowdown=False)
                            elif eval(code) == False:
                                vote(":material/close: 不成立",types='bool',colors='red',allowta=False,allowdown=False)
                            else:
                                if snf:
                                    vote(format_to_scientific(eval(code)),allowta=True)
                                else:
                                    vote(eval(code),allowta=True)
                        except:
                            errors(f'''请检查您的eval函数代码块语法，如想运行复杂代码，请使用POCE内置运行器''')
                else:
                    errors(f'''代码块中出现了POCE不支持的库或方法！{found_usp}''')
                
with st.sidebar:
    st.title("模块操作面板")
    st.subheader(":material/widgets:  模块安装管理")
    model_name = st.text_input("模块名称",label_visibility='collapsed',placeholder="模块名称")
    option_map = {
    0: ":material/zoom_in: 检查模式",
    1: ":material/archive: 安装模式",
    }
    selection = st.segmented_control(
        "Tool",label_visibility="collapsed",default=0,
        options=option_map.keys(),
        format_func=lambda option: option_map[option],
        selection_mode="single",
    )
    if st.button(":material/settings:  执行"):
        if not((" " in model_name) or ("--" in model_name) or (model_name == '')):
            if selection == 0:
                try:
                    importlib.import_module(model_name)
                    st.success(f"模块'{model_name}'已安装")
                except:
                    st.warning(f"模块'{model_name}'未安装")
            elif selection == 1:
                with st.status("安装模块中...", expanded=True) as status:
                    st.write("检查模块可用性...")
                    try:
                        importlib.import_module(model_name)
                        st.write("*模块已安装且处于可用状态")
                        status.update(
                            label="模块安装成功!", state="complete"
                        )
                    except:
                        st.write("调用pip安装中...")
                        pipcode = run(["pip","install",model_name])['code']
                        if pipcode == 0:
                            st.write("测试模块中...")
                            try:
                                importlib.import_module(model_name)
                                st.write("*模块处于可用状态")
                                status.update(
                                    label="模块安装成功!", state="complete"
                                )
                            except:
                                st.write("*模块处于不可用状态")
                                status.update(
                                    label=f"模块安装失败", state="error"
                                )
                        else:
                            status.update(
                                label=f"模块安装失败：{pipcode}", state="error"
                            )
        else:
            st.error("模块名非法!")
    st.divider()
    st.subheader(":material/find_in_page:  模块方法查询")
    serc_name = st.text_input("模块名",label_visibility='collapsed',placeholder="模块名称")
    skill_name = st.text_input("方法关键字",label_visibility='collapsed',placeholder="方法关键字（可选）")
    if st.button(":material/search:  搜索"):
        if not((" " in serc_name) or ("--" in serc_name) or (serc_name == '')):
            try:
                methodss = importlib.import_module(f"{serc_name}")
                methods =  [method for method in dir(methodss) if not method.startswith('__')]
                with st.spinner("搜索中..."):
                    with st.container(border=True):
                        if skill_name != "":
                            methodswithserch = []
                            for i in methods:
                                if skill_name in i:
                                    methodswithserch.append(i)
                            st.caption(f"搜索结果 (共{len(methodswithserch)}个)")
                            st.json(methodswithserch)
                        else:
                            st.caption(f"搜索结果 (共{len(methods)}个)")
                            st.json(methods)
            except:
                st.error("模块导入失败")
