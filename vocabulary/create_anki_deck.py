import genanki
import random
import os
import asyncio
import edge_tts
import time
import re

# 创建一个改进的Anki卡片模型
my_model = genanki.Model(
    random.randrange(1 << 30, 1 << 31),
    '日语听写模型改进版',
    fields=[
        {'name': 'Word'},  # 日语汉字
        {'name': 'Pronunciation'},  # 假名读音
        {'name': 'Meaning'},  # 中文意思
        {'name': 'Audio'},  # 单词读音音频文件链接
        {'name': 'Example'},  # 例句（日文）
        {'name': 'ExampleTrans'},  # 例句翻译（中文）
        {'name': 'ExampleAudio'},  # 例句音频（可选）
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '''
                <!-- 简洁设计，只使用白色文字 -->
                <div style="font-size: 36px; font-weight: bold; text-align: center; margin: 25px 0;">
                    {{Word}}
                </div>

                <div style="font-size: 22px; text-align: center; margin: 20px 0; ">
                    {{Meaning}}
                </div>

                <div style="font-size: 16px; text-align: center; margin: 15px 0; ">
                    （请默写/说出它的读音）
                </div>

                <!-- 输入区域 -->
                <div style="text-align: center; margin: 25px 0;">
                    <input type="text" id="user-input" placeholder="请输入假名读音" 
                           style="padding: 12px; width: 80%; font-size: 16px; 
                                  border: 1px solid #ccc; border-radius: 4px; 
                                  background: #fff; color: #000;">
                </div>

                <!-- 提交按钮 -->
                <div style="text-align: center;">
                    <button id="submit-btn" onclick="checkAnswer()" 
                            style="padding: 12px 40px; background: #4CAF50; color: white; 
                                   border: none; border-radius: 4px; cursor: pointer; 
                                   font-size: 16px; font-weight: bold; margin-top: 10px;">
                        提交答案
                    </button>
                </div>

                <!-- 结果显示区域 -->
                <div id="result" style="text-align: center; margin-top: 20px; display: none; 
                     padding: 15px; border-radius: 4px; font-size: 18px; font-weight: bold;"></div>

                <!-- 答案区域 - 初始隐藏 -->
                <div id="answer-section" style="display: none; margin-top: 30px; 
                     padding: 20px; border-radius: 4px; border: 1px solid #e0e0e0; background: #f9f9f9;">

                    <!-- 显示正确答案（读音） -->
                    <div style="font-size: 24px; text-align: center; color: #2E7D32; margin: 15px 0; font-weight: bold;">
                        正确答案: {{Pronunciation}}
                    </div>

                    <!-- 播放单词音频 -->
                    <div style="text-align: center; margin: 15px 0;">
                        {{Audio}}
                    </div>

                    <!-- 显示例句 -->
                    <div style="font-size: 18px; margin: 20px 0; text-align: center; color: #333;">
                        例句： {{Example}} <span style="color: #666; font-size: 16px;">({{ExampleTrans}})</span>
                    </div>

                    <!-- 播放例句音频 -->
                    <div style="text-align: center; margin: 15px 0;">
                        {{ExampleAudio}}
                    </div>
                </div>

                <script>
                    function checkAnswer() {
                        var userInput = document.getElementById("user-input").value.trim();
                        var correctAnswer = "{{Pronunciation}}";
                        var resultDiv = document.getElementById("result");
                        var answerSection = document.getElementById("answer-section");
                        var submitBtn = document.getElementById("submit-btn");

                        if (userInput === "") {
                            resultDiv.innerHTML = "请输入答案";
                            resultDiv.style.backgroundColor = "#FFF3CD";
                            resultDiv.style.color = "#856404";
                            resultDiv.style.display = "block";
                            return;
                        }

                        if (userInput === correctAnswer) {
                            resultDiv.innerHTML = "✓ 答对了！";
                            resultDiv.style.backgroundColor = "#D4EDDA";
                            resultDiv.style.color = "#155724";
                        } else {
                            resultDiv.innerHTML = "✗ 正确答案: " + correctAnswer;
                            resultDiv.style.backgroundColor = "#F8D7DA";
                            resultDiv.style.color = "#721C24";
                        }

                        resultDiv.style.display = "block";
                        answerSection.style.display = "block";

                        // 更改按钮为重新验证
                        submitBtn.innerHTML = "重新验证";
                        submitBtn.style.background = "#FF5722";
                        submitBtn.onclick = resetCard;

                        // 禁用输入框
                        document.getElementById("user-input").disabled = true;
                        document.getElementById("user-input").style.backgroundColor = "#f5f5f5";
                    }

                    function resetCard() {
                        // 重置卡片状态
                        document.getElementById("user-input").value = "";
                        document.getElementById("user-input").disabled = false;
                        document.getElementById("user-input").style.backgroundColor = "#fff";
                        document.getElementById("result").style.display = "none";
                        document.getElementById("answer-section").style.display = "none";

                        // 恢复提交按钮
                        var submitBtn = document.getElementById("submit-btn");
                        submitBtn.innerHTML = "提交答案";
                        submitBtn.style.background = "#4CAF50";
                        submitBtn.onclick = checkAnswer;
                    }

                    // 设置输入框placeholder颜色
                    document.addEventListener('DOMContentLoaded', function() {
                        var style = document.createElement('style');
                        style.innerHTML = `
                            #user-input::placeholder {
                                color: #888;
                                opacity: 1;
                            }
                            #user-input:-ms-input-placeholder {
                                color: #888;
                            }
                            #user-input::-ms-input-placeholder {
                                color: #888;
                            }
                        `;
                        document.head.appendChild(style);
                    });

                    // 添加回车键支持
                    document.addEventListener('DOMContentLoaded', function() {
                        document.getElementById("user-input").addEventListener("keypress", function(event) {
                            if (event.key === "Enter") {
                                var submitBtn = document.getElementById("submit-btn");
                                if (submitBtn.innerHTML === "提交答案") {
                                    checkAnswer();
                                } else {
                                    resetCard();
                                }
                            }
                        });
                    });
                </script>
            ''',
            'afmt': '''
                <!-- 卡片反面模板 - 优化版 -->
                <div style="font-size: 36px; font-weight: bold; text-align: center; margin: 25px 0;">
                    {{Word}}
                </div>

                <div style="font-size: 22px; text-align: center; margin: 20px 0;">
                    {{Meaning}}
                </div>

                <!-- 答案区域，始终显示 -->
                <div id="answer-section-back" style="display: block; margin-top: 30px; 
                     padding: 20px; border-radius: 4px; border: 1px solid #e0e0e0; background: #f9f9f9;">

                    <!-- 显示正确答案（读音） -->
                    <div style="font-size: 24px; text-align: center; color: #2E7D32; margin: 15px 0; font-weight: bold;">
                        正确读音: {{Pronunciation}}
                    </div>

                    <!-- 播放单词音频 -->
                    <div style="text-align: center; margin: 15px 0;">
                        {{Audio}}
                    </div>

                    <!-- 显示例句 -->
                    <div style="font-size: 18px; margin: 20px 0; text-align: center; color: #333;">
                        例句： {{Example}} <span style="color: #666; font-size: 16px;">({{ExampleTrans}})</span>
                    </div>

                    <!-- 播放例句音频 -->
                    <div style="text-align: center; margin: 15px 0;">
                        {{ExampleAudio}}
                    </div>
                </div>
            ''',
        },
    ],
    css='''
        .card {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 20px;
            background: #ffffff;
            color: #000000;
        }
        input {
            box-sizing: border-box;
        }
        input:focus {
            outline: none;
            border-color: #4CAF50 !important;
            box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
        }
        button {
            transition: all 0.2s ease;
        }
        button:hover {
            opacity: 0.9;
            transform: translateY(-1px);
        }
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }
        .highlight {
            color: #FF5722;
            font-weight: bold;
        }
        #user-input:disabled, #user-input-back:disabled {
            background-color: #f5f5f5 !important;
            color: #555;
        }
        #result, #result-back {
            transition: all 0.3s ease;
        }
        #answer-section, #answer-section-back {
            animation: fadeIn 0.3s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* 增强的按钮样式 */
        button:active {
            transform: translateY(1px);
        }

        /* 输入框动画 */
        input {
            transition: all 0.2s ease;
        }

        /* 响应式设计 */
        @media (max-width: 600px) {
            input {
                width: 95% !important;
                font-size: 14px !important;
            }
            button {
                padding: 10px 30px !important;
                font-size: 14px !important;
            }
        }
    '''
)

def sanitize_filename(text):
    """清理文件名中的非法字符，使用更安全的方法"""
    # 替换所有非字母数字字符为下划线
    safe_name = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff\u3040-\u309f\u30a0-\u30ff]', '_', text)
    # 移除连续的下划线
    safe_name = re.sub(r'_+', '_', safe_name)
    # 移除开头和结尾的下划线
    safe_name = safe_name.strip('_')
    # 如果清理后为空，使用哈希值
    if not safe_name:
        safe_name = str(hash(text))[:8]
    # 限制文件名长度
    if len(safe_name) > 50:
        safe_name = safe_name[:50]
    return safe_name

def get_default_voice():
    """返回默认的日语语音"""
    selected_voice = 'ja-JP-NanamiNeural'
    print(f"🎤 使用默认语音: {selected_voice} (女声，推荐)")
    return selected_voice

async def text_to_speech_edge(text, output_path, voice='ja-JP-NanamiNeural', rate='+0%', pitch='+0Hz'):
    """使用Edge TTS生成语音文件"""
    try:
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 创建TTS通信对象
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        
        # 生成音频文件
        await communicate.save(output_path)
        print(f"成功生成音频: {output_path}")
        return True
        
    except Exception as e:
        print(f"生成音频失败: {output_path}, 错误: {e}")
        return False

async def generate_audio_files_async(vocabulary_list, audio_dir="audio", selected_voice='ja-JP-NanamiNeural'):
    """异步为所有单词和例句生成音频文件"""
    # 创建音频目录
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)

    total_words = len(vocabulary_list)
    success_count = 0
    fail_count = 0

    print(f"开始为 {total_words} 个词汇生成音频文件...")

    # 创建所有音频生成任务
    tasks = []
    file_info = []

    for i, word_data in enumerate(vocabulary_list):
        word = word_data['word']
        pronunciation = word_data['pronunciation']
        example = word_data['example']

        # 生成安全的文件名
        safe_word = sanitize_filename(word)
        word_audio_file = os.path.join(audio_dir, f"{safe_word}.mp3")

        # 添加单词音频任务（如果不存在）
        if not os.path.exists(word_audio_file):
            task = text_to_speech_edge(pronunciation, word_audio_file, selected_voice)
            tasks.append(task)
            file_info.append(('word', word, word_audio_file))

        # 添加例句音频任务（如果有例句且不存在）
        if example:
            example_audio_file = os.path.join(audio_dir, f"{safe_word}_example.mp3")
            if not os.path.exists(example_audio_file):
                task = text_to_speech_edge(example, example_audio_file, selected_voice)
                tasks.append(task)
                file_info.append(('example', word, example_audio_file))

    print(f"需要生成 {len(tasks)} 个音频文件...")

    # 批量执行任务，控制并发数量避免过载
    batch_size = 10  # 每批处理10个任务
    
    for i in range(0, len(tasks), batch_size):
        batch_tasks = tasks[i:i+batch_size]
        batch_info = file_info[i:i+batch_size]
        
        print(f"处理第 {i//batch_size + 1} 批任务 ({len(batch_tasks)} 个文件)...")
        
        # 执行当前批次的任务
        results = await asyncio.gather(*batch_tasks, return_exceptions=True)
        
        # 统计结果
        for j, result in enumerate(results):
            if isinstance(result, bool) and result:
                success_count += 1
            else:
                fail_count += 1
                file_type, word, file_path = batch_info[j]
                print(f"❌ 生成失败: {word} ({file_type})")
        
        # 批次间休息
        if i + batch_size < len(tasks):
            await asyncio.sleep(2)

    print(f"音频生成完成！成功: {success_count}, 失败: {fail_count}")

def generate_audio_files(vocabulary_list, audio_dir="audio", selected_voice='ja-JP-NanamiNeural'):
    """同步包装器，调用异步音频生成函数"""
    # 检查是否有可用的事件循环
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 如果已有运行中的事件循环，创建新的事件循环
            import threading
            result = {'success': False}
            
            def run_async():
                new_loop = asyncio.new_event_loop()
                asyncio.set_event_loop(new_loop)
                try:
                    new_loop.run_until_complete(generate_audio_files_async(vocabulary_list, audio_dir, selected_voice))
                    result['success'] = True
                finally:
                    new_loop.close()
            
            thread = threading.Thread(target=run_async)
            thread.start()
            thread.join()
            return result['success']
        else:
            # 没有运行中的事件循环，直接运行
            return asyncio.run(generate_audio_files_async(vocabulary_list, audio_dir, selected_voice))
    except RuntimeError:
        # 没有事件循环，创建新的
        return asyncio.run(generate_audio_files_async(vocabulary_list, audio_dir, selected_voice))

def read_vocabulary_from_txt(file_path):
    """从文本文件读取词汇数据，支持例句和章节分类"""
    vocabulary_list = []
    current_section = ""

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            # 检测章节标题，并将其作为分类
            if line.startswith('【') and line.endswith('】'):
                current_section = line[1:-1]  # 移除【】
                continue

            # 解析词汇行
            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    word = parts[0].strip()
                    pronunciation = parts[1].strip()
                    meaning = parts[2].strip()

                    # 处理例句（如果有）
                    example = ""
                    example_trans = ""
                    if len(parts) >= 5:
                        example = parts[3].strip()
                        example_trans = parts[4].strip()
                    elif len(parts) == 4:  # 如果只有例句，没有翻译
                        example = parts[3].strip()
                        example_trans = ""  # 留空

                    vocabulary_list.append({
                        'word': word,
                        'pronunciation': pronunciation,
                        'meaning': meaning,
                        'example': example,
                        'example_trans': example_trans,
                        'section': current_section if current_section else "未分类"
                    })

    return vocabulary_list

def generate_anki_deck(vocabulary_list, output_file):
    """生成Anki牌组，并按章节分类"""

    # 顶层牌组名称
    top_deck_name = '圆圆-背词听写版'

    # 用于存放所有子牌组的列表
    all_decks = []

    # 按章节对词汇进行分组
    sections = {}
    for word_data in vocabulary_list:
        section_name = word_data['section']
        if section_name not in sections:
            sections[section_name] = []
        sections[section_name].append(word_data)

    # 为每个章节创建一个子牌组
    for section_name, words_in_section in sections.items():
        # 构建子牌组的完整名称
        full_deck_name = f"{top_deck_name}::{section_name}"
        deck_id = random.randrange(1 << 30, 1 << 31)
        section_deck = genanki.Deck(deck_id, full_deck_name)

        for word_data in words_in_section:
            # 生成安全的文件名
            safe_word = sanitize_filename(word_data['word'])

            # 生成音频文件名
            word_audio_file = f"{safe_word}.mp3"
            audio_filename = f"[sound:{word_audio_file}]"

            # 生成例句音频文件名（如果有例句）
            example_audio_filename = ""
            if word_data['example']:
                example_audio_file = f"{safe_word}_example.mp3"
                example_audio_filename = f"[sound:{example_audio_file}]"

            # 在例句中高亮显示单词
            highlighted_example = word_data['example']
            if word_data['example'] and word_data['word'] in word_data['example']:
                highlighted_example = word_data['example'].replace(
                    word_data['word'],
                    f'<span class="highlight">{word_data["word"]}</span>'
                )

            # 创建笔记
            note = genanki.Note(
                model=my_model,
                fields=[
                    word_data['word'],  # Word
                    word_data['pronunciation'],  # Pronunciation
                    word_data['meaning'],  # Meaning
                    audio_filename,  # Audio
                    highlighted_example,  # Example (高亮显示单词)
                    word_data['example_trans'],  # ExampleTrans
                    example_audio_filename,  # ExampleAudio
                ]
            )
            section_deck.add_note(note)

        all_decks.append(section_deck)

    # 创建Anki包
    package = genanki.Package(all_decks)

    # 添加音频文件到包中
    audio_files = []
    audio_dir = "audio"
    if os.path.exists(audio_dir):
        for file in os.listdir(audio_dir):
            if file.endswith('.mp3'):
                audio_files.append(os.path.join(audio_dir, file))
        package.media_files = audio_files

    # 保存牌组
    package.write_to_file(output_file)
    print(f"Anki牌组已生成: {output_file}")

def main():
    print("🎌 日语Anki卡片生成器 - Edge TTS版")
    print("=" * 50)
    
    # 使用默认语音
    selected_voice = get_default_voice()
    
    # 读取词汇数据
    script_dir = os.path.dirname(os.path.abspath(__file__))
    txt_file = os.path.join(script_dir, 'n2_vocabulary_completed.txt')
    
    if not os.path.exists(txt_file):
        print(f"❌ 错误: 找不到词汇文件 {txt_file}")
        print("请确保在脚本同目录下有 'n2_vocabulary_completed.txt' 文件")
        return
    
    vocabulary_list = read_vocabulary_from_txt(txt_file)
    print(f"📚 从 {txt_file} 中读取了 {len(vocabulary_list)} 个词汇")

    # 生成音频文件
    print(f"🎵 开始使用 {selected_voice} 生成音频...")
    
    success = generate_audio_files(vocabulary_list, "audio", selected_voice)
    
    if success:
        print("✅ 音频文件生成完成")
    else:
        print("⚠️ 音频生成过程中出现一些问题，但会继续生成Anki卡片")

    # 生成Anki牌组
    output_file = "N2_日语词汇_圆圆背词听写版_EdgeTTS.apkg"
    generate_anki_deck(vocabulary_list, output_file)

    # 显示统计信息
    sections = {}
    for word in vocabulary_list:
        section = word['section']
        sections[section] = sections.get(section, 0) + 1

    print("\n📊 各章节词汇数量:")
    for section, count in sections.items():
        print(f"  {section}: {count} 个词汇")

    print("\n✨ 使用说明:")
    print("📱 正面功能: 显示单词和中文意思，要求输入假名读音")
    print("📱 反面功能: 显示正确答案、音频和例句") 
    print("🎯 学习建议: 先尝试回忆，再查看答案，使用Anki评分按钮")
    print("🎤 语音特色: 使用微软Edge TTS，音质清晰自然")

    print(f"\n🎉 生成完成: {output_file}")
    print("💡 提示: 首次安装需要运行: pip install edge-tts genanki")

if __name__ == "__main__":
    main()