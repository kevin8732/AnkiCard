#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
指定文件PDF转Word转换器
支持多种方式指定文件进行转换
"""

import os
import sys
from pathlib import Path
from typing import Optional, List
import argparse

# ========== 文件处理类 ==========

class PDFConverter:
    """PDF转Word转换器"""
    
    def __init__(self):
        self.check_dependencies()
    
    def check_dependencies(self):
        """检查依赖是否安装"""
        try:
            from pdf2docx import Converter
            print("✅ pdf2docx 已安装")
            self.converter_available = True
        except ImportError:
            print("❌ pdf2docx 未安装")
            print("请先安装: pip install pdf2docx 或 pipx install pdf2docx")
            self.converter_available = False
    
    def convert_single_file(self, pdf_path: str, word_path: Optional[str] = None, **kwargs) -> bool:
        """转换单个PDF文件
        
        Args:
            pdf_path: PDF文件路径
            word_path: 输出Word文件路径（可选）
            **kwargs: 额外参数（start, end, pages等）
        
        Returns:
            bool: 转换是否成功
        """
        if not self.converter_available:
            return False
        
        from pdf2docx import Converter
        
        # 处理输入路径
        pdf_file = Path(pdf_path).expanduser().resolve()
        
        if not pdf_file.exists():
            print(f"❌ PDF文件不存在: {pdf_file}")
            return False
        
        if pdf_file.suffix.lower() != '.pdf':
            print(f"❌ 不是PDF文件: {pdf_file}")
            return False
        
        # 处理输出路径
        if word_path is None:
            word_file = pdf_file.with_suffix('.docx')
        else:
            word_file = Path(word_path).expanduser().resolve()
            # 确保输出目录存在
            word_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 检查文件是否已存在
        if word_file.exists():
            overwrite = input(f"文件 {word_file.name} 已存在，是否覆盖? (y/n): ").lower().strip()
            if overwrite != 'y':
                print("❌ 取消转换")
                return False
        
        try:
            print(f"🔄 开始转换: {pdf_file.name}")
            print(f"📊 文件大小: {pdf_file.stat().st_size / 1024 / 1024:.2f} MB")
            
            # 执行转换
            cv = Converter(str(pdf_file))
            cv.convert(str(word_file), **kwargs)
            cv.close()
            
            if word_file.exists():
                print(f"✅ 转换成功!")
                print(f"📁 输出文件: {word_file}")
                print(f"📊 输出大小: {word_file.stat().st_size / 1024 / 1024:.2f} MB")
                return True
            else:
                print("❌ 转换失败，未生成输出文件")
                return False
                
        except Exception as e:
            print(f"❌ 转换错误: {e}")
            return False

# ========== 不同的文件指定方式 ==========

def convert_by_file_path():
    """通过文件路径指定转换"""
    print("\n=== 📁 通过文件路径转换 ===")
    
    converter = PDFConverter()
    if not converter.converter_available:
        return
    
    # 获取文件路径
    pdf_path = input("请输入PDF文件路径（支持拖拽文件）: ").strip().strip('"\'')
    
    if not pdf_path:
        print("❌ 未输入文件路径")
        return
    
    # 可选：指定输出路径
    custom_output = input("指定输出路径（回车使用默认）: ").strip().strip('"\'')
    word_path = custom_output if custom_output else None
    
    # 执行转换
    converter.convert_single_file(pdf_path, word_path)

def convert_by_file_selection():
    """通过文件选择转换（模拟文件对话框）"""
    print("\n=== 📋 通过文件选择转换 ===")
    
    # 显示当前目录的PDF文件
    current_dir = Path.cwd()
    pdf_files = list(current_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ 当前目录 {current_dir} 中没有PDF文件")
        
        # 提示用户输入其他目录
        other_dir = input("请输入包含PDF文件的目录路径（回车跳过）: ").strip()
        if other_dir:
            search_dir = Path(other_dir).expanduser()
            if search_dir.exists():
                pdf_files = list(search_dir.glob("*.pdf"))
            else:
                print(f"❌ 目录不存在: {search_dir}")
                return
        
        if not pdf_files:
            print("❌ 未找到PDF文件")
            return
    
    # 显示文件列表
    print(f"\n📁 在 {pdf_files[0].parent} 中找到以下PDF文件:")
    for i, pdf_file in enumerate(pdf_files, 1):
        file_size = pdf_file.stat().st_size / 1024 / 1024
        print(f"{i:2d}. {pdf_file.name} ({file_size:.1f} MB)")
    
    # 用户选择文件
    try:
        choice = input(f"\n请选择要转换的文件 (1-{len(pdf_files)}): ").strip()
        if not choice:
            print("❌ 未选择文件")
            return
            
        file_index = int(choice) - 1
        if 0 <= file_index < len(pdf_files):
            selected_file = pdf_files[file_index]
            print(f"✅ 已选择: {selected_file.name}")
            
            # 转换文件
            converter = PDFConverter()
            converter.convert_single_file(str(selected_file))
        else:
            print("❌ 无效选择")
            
    except ValueError:
        print("❌ 请输入有效数字")

def convert_with_pages():
    """转换指定页面"""
    print("\n=== 📄 转换指定页面 ===")
    
    converter = PDFConverter()
    if not converter.converter_available:
        return
    
    # 获取文件路径
    pdf_path = input("请输入PDF文件路径: ").strip().strip('"\'')
    if not pdf_path:
        print("❌ 未输入文件路径")
        return
    
    print("\n页面选择选项:")
    print("1. 转换所有页面")
    print("2. 转换页面范围 (如: 1-5)")
    print("3. 转换指定页面 (如: 1,3,5)")
    
    choice = input("请选择 (1-3): ").strip()
    
    kwargs = {}
    
    if choice == "2":
        page_range = input("请输入页面范围 (如 1-5): ").strip()
        try:
            start_page, end_page = map(int, page_range.split('-'))
            kwargs['start'] = start_page - 1  # 转换为0开始索引
            kwargs['end'] = end_page
            print(f"将转换第 {start_page} 到 {end_page} 页")
        except ValueError:
            print("❌ 页面范围格式错误")
            return
    
    elif choice == "3":
        pages_input = input("请输入页面号码 (用逗号分隔，如 1,3,5): ").strip()
        try:
            pages = [int(p.strip()) - 1 for p in pages_input.split(',')]  # 转换为0开始索引
            kwargs['pages'] = pages
            print(f"将转换页面: {[p+1 for p in pages]}")
        except ValueError:
            print("❌ 页面格式错误")
            return
    
    # 执行转换
    converter.convert_single_file(pdf_path, **kwargs)

def convert_batch_specific():
    """批量转换指定的多个文件"""
    print("\n=== 📚 批量转换指定文件 ===")
    
    converter = PDFConverter()
    if not converter.converter_available:
        return
    
    pdf_files = []
    
    print("请输入要转换的PDF文件路径（每行一个，输入空行结束）:")
    while True:
        file_path = input("PDF文件路径: ").strip().strip('"\'')
        if not file_path:
            break
        
        pdf_path = Path(file_path).expanduser()
        if pdf_path.exists() and pdf_path.suffix.lower() == '.pdf':
            pdf_files.append(pdf_path)
            print(f"✅ 已添加: {pdf_path.name}")
        else:
            print(f"❌ 无效的PDF文件: {file_path}")
    
    if not pdf_files:
        print("❌ 没有有效的PDF文件")
        return
    
    # 确认转换
    print(f"\n📋 将转换以下 {len(pdf_files)} 个文件:")
    for i, pdf_file in enumerate(pdf_files, 1):
        print(f"{i}. {pdf_file.name}")
    
    confirm = input("\n确认开始批量转换? (y/n): ").lower().strip()
    if confirm != 'y':
        print("❌ 取消转换")
        return
    
    # 执行批量转换
    success_count = 0
    for pdf_file in pdf_files:
        print(f"\n{'='*50}")
        if converter.convert_single_file(str(pdf_file)):
            success_count += 1
    
    print(f"\n🎉 批量转换完成: {success_count}/{len(pdf_files)} 个文件成功")

# ========== 命令行参数处理 ==========

def parse_command_line():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description="PDF转Word转换器")
    parser.add_argument("input_file", nargs='?', help="输入PDF文件路径")
    parser.add_argument("-o", "--output", help="输出Word文件路径")
    parser.add_argument("-s", "--start", type=int, help="起始页码（从1开始）")
    parser.add_argument("-e", "--end", type=int, help="结束页码")
    parser.add_argument("-p", "--pages", help="指定页面，用逗号分隔 (如: 1,3,5)")
    parser.add_argument("--multi", action="store_true", help="使用多进程")
    
    return parser.parse_args()

def main():
    """主程序入口"""
    print("=== 📄 PDF转Word转换器 ===\n")
    
    # 检查命令行参数
    args = parse_command_line()
    
    if args.input_file:
        # 命令行模式
        converter = PDFConverter()
        if not converter.converter_available:
            return
        
        kwargs = {}
        
        # 处理页面参数
        if args.start is not None:
            kwargs['start'] = args.start - 1  # 转换为0开始索引
        if args.end is not None:
            kwargs['end'] = args.end
        if args.pages:
            try:
                pages = [int(p.strip()) - 1 for p in args.pages.split(',')]
                kwargs['pages'] = pages
            except ValueError:
                print("❌ 页面格式错误")
                return
        
        # 执行转换
        converter.convert_single_file(args.input_file, args.output, **kwargs)
    
    else:
        # 交互模式
        while True:
            print("\n请选择转换方式:")
            print("1. 📁 通过文件路径转换")
            print("2. 📋 从当前目录选择文件转换") 
            print("3. 📄 转换指定页面")
            print("4. 📚 批量转换指定文件")
            print("5. ❌ 退出")
            
            choice = input("\n请选择 (1-5): ").strip()
            
            if choice == "1":
                convert_by_file_path()
            elif choice == "2":
                convert_by_file_selection()
            elif choice == "3":
                convert_with_pages()
            elif choice == "4":
                convert_batch_specific()
            elif choice == "5":
                print("👋 再见!")
                break
            else:
                print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()


# ========== 使用示例 ==========

"""
使用方法:

1. 交互式使用:
   python pdf_converter.py

2. 命令行使用:
   python pdf_converter.py input.pdf
   python pdf_converter.py input.pdf -o output.docx
   python pdf_converter.py input.pdf --start 1 --end 5
   python pdf_converter.py input.pdf --pages "1,3,5"

3. 拖拽文件使用:
   运行程序后选择"通过文件路径转换"，然后拖拽PDF文件到终端
"""