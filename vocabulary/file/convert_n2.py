#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
转换指定的日语N2语法PDF文件
"""

import os
import sys
import urllib.parse
from pathlib import Path

def convert_n2_grammar_pdf():
    """转换N2语法PDF文件"""
    
    # 处理文件路径 - 从file:// URL转换为本地路径
    file_url = "file:///Users/xiaowen/Desktop/work/study/python/AnkiCard/TRY!%E6%96%B0%E6%97%A5%E8%AF%AD%E8%83%BD%E5%8A%9B%E8%80%83%E8%AF%95N2%E8%AF%AD%E6%B3%95%E5%BF%85%E5%A4%87.pdf"
    
    # 移除file://前缀并解码URL编码
    local_path = urllib.parse.unquote(file_url.replace('file://', ''))
    
    pdf_file = Path(local_path)
    
    print(f"🎯 目标文件: {pdf_file.name}")
    print(f"📁 文件路径: {pdf_file}")
    
    # 检查文件是否存在
    if not pdf_file.exists():
        print(f"❌ 文件不存在: {pdf_file}")
        print("请检查文件路径是否正确")
        return False
    
    # 显示文件信息
    file_size_mb = pdf_file.stat().st_size / (1024 * 1024)
    print(f"📊 文件大小: {file_size_mb:.2f} MB")
    
    # 生成输出文件名
    word_file = pdf_file.with_suffix('.docx')
    print(f"📝 输出文件: {word_file.name}")
    
    # 检查是否需要覆盖
    if word_file.exists():
        print(f"⚠️  输出文件已存在: {word_file.name}")
        overwrite = input("是否覆盖? (y/n): ").lower().strip()
        if overwrite != 'y':
            print("❌ 取消转换")
            return False
    
    # 尝试导入pdf2docx
    try:
        from pdf2docx import Converter
        print("✅ pdf2docx 可用")
    except ImportError:
        print("❌ 未找到pdf2docx")
        print("\n请先设置环境:")
        print("python3 -m venv pdf_env")
        print("source pdf_env/bin/activate")
        print("pip install pdf2docx")
        print("然后重新运行此脚本")
        return False
    
    try:
        print("\n🔄 开始转换...")
        print("⏳ 请稍等，正在处理...")
        
        # 执行转换
        cv = Converter(str(pdf_file))
        cv.convert(str(word_file))
        cv.close()
        
        # 检查结果
        if word_file.exists():
            output_size_mb = word_file.stat().st_size / (1024 * 1024)
            print(f"\n✅ 转换成功!")
            print(f"📁 输出文件: {word_file}")
            print(f"📊 输出大小: {output_size_mb:.2f} MB")
            
            # 尝试打开文件夹
            try:
                os.system(f"open '{word_file.parent}'")
                print("📂 已打开文件所在文件夹")
            except:
                pass
            
            return True
        else:
            print("❌ 转换失败，未生成输出文件")
            return False
            
    except Exception as e:
        print(f"❌ 转换过程中出错: {e}")
        print("\n可能的解决方案:")
        print("1. 确保PDF文件没有被其他程序打开")
        print("2. 检查文件是否损坏")
        print("3. 尝试转换部分页面")
        return False

def convert_with_page_options():
    """提供页面选择选项的转换"""
    
    file_url = "file:///Users/xiaowen/Desktop/work/study/python/AnkiCard/TRY!%E6%96%B0%E6%97%A5%E8%AF%AD%E8%83%BD%E5%8A%9B%E8%80%83%E8%AF%95N2%E8%AF%AD%E6%B3%95%E5%BF%85%E5%A4%87.pdf"
    local_path = urllib.parse.unquote(file_url.replace('file://', ''))
    pdf_file = Path(local_path)
    
    if not pdf_file.exists():
        print(f"❌ 文件不存在: {pdf_file}")
        return False
    
    # 导入检查
    try:
        from pdf2docx import Converter
    except ImportError:
        print("❌ 请先安装pdf2docx")
        return False
    
    print(f"🎯 文件: {pdf_file.name}")
    print(f"📊 大小: {pdf_file.stat().st_size / (1024 * 1024):.2f} MB")
    
    print("\n转换选项:")
    print("1. 转换全部页面")
    print("2. 转换指定页面范围 (如: 1-10)")
    print("3. 转换特定页面 (如: 1,5,10)")
    
    choice = input("\n请选择 (1-3): ").strip()
    
    kwargs = {}
    output_suffix = ""
    
    if choice == "2":
        page_range = input("请输入页面范围 (如 1-10): ").strip()
        try:
            start, end = map(int, page_range.split('-'))
            kwargs['start'] = start - 1  # 转换为0开始索引
            kwargs['end'] = end
            output_suffix = f"_pages_{start}-{end}"
            print(f"✅ 将转换第 {start} 到 {end} 页")
        except ValueError:
            print("❌ 页面范围格式错误，转换全部页面")
    
    elif choice == "3":
        pages_input = input("请输入页面号码 (用逗号分隔): ").strip()
        try:
            pages = [int(p.strip()) - 1 for p in pages_input.split(',')]  # 转换为0开始索引
            kwargs['pages'] = pages
            output_suffix = f"_pages_{'_'.join(str(p+1) for p in pages)}"
            print(f"✅ 将转换页面: {[p+1 for p in pages]}")
        except ValueError:
            print("❌ 页面格式错误，转换全部页面")
    
    # 生成输出文件名
    base_name = pdf_file.stem
    word_file = pdf_file.parent / f"{base_name}{output_suffix}.docx"
    
    try:
        print(f"\n🔄 开始转换到: {word_file.name}")
        
        cv = Converter(str(pdf_file))
        cv.convert(str(word_file), **kwargs)
        cv.close()
        
        if word_file.exists():
            print(f"✅ 转换成功: {word_file}")
            
            # 打开文件夹
            try:
                os.system(f"open '{word_file.parent}'")
            except:
                pass
                
            return True
        else:
            print("❌ 转换失败")
            return False
            
    except Exception as e:
        print(f"❌ 转换错误: {e}")
        return False

def main():
    """主程序"""
    print("=== 🎌 N2语法PDF转Word ===")
    print("TRY!新日语能力考试N2语法必备")
    
    print("\n选择转换方式:")
    print("1. 转换整个文件")
    print("2. 选择转换页面")
    
    choice = input("\n请选择 (1-2): ").strip()
    
    if choice == "2":
        convert_with_page_options()
    else:
        convert_n2_grammar_pdf()

if __name__ == "__main__":
    main()


# ============ 快速转换命令 ============
"""
如果你已经设置好环境，可以直接运行:

python3 -c "
import urllib.parse
from pathlib import Path
from pdf2docx import Converter

file_url = 'file:///Users/xiaowen/Desktop/work/study/python/AnkiCard/TRY!%E6%96%B0%E6%97%A5%E8%AF%AD%E8%83%BD%E5%8A%9B%E8%80%83%E8%AF%95N2%E8%AF%AD%E6%B3%95%E5%BF%85%E5%A4%87.pdf'
local_path = urllib.parse.unquote(file_url.replace('file://', ''))
pdf_file = Path(local_path)
word_file = pdf_file.with_suffix('.docx')

print(f'转换: {pdf_file.name}')
cv = Converter(str(pdf_file))
cv.convert(str(word_file))
cv.close()
print(f'完成: {word_file}')
"
"""