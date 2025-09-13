import genanki
import random
import os
from gtts import gTTS
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

                <!-- 结果显示区域 - 反面版本 -->
                <div id="result-back" style="text-align: center; margin-top: 20px; display: none; 
                     padding: 15px; border-radius: 4px; font-size: 18px; font-weight: bold;"></div>

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

                <script>
                    function verifyAnswerBack() {
                        var userInput = document.getElementById("user-input-back").value.trim();
                        var correctAnswer = "{{Pronunciation}}";
                        var resultDiv = document.getElementById("result-back");

                        if (userInput === "") {
                            resultDiv.innerHTML = "请输入答案";
                            resultDiv.style.backgroundColor = "#FFF3CD";
                            resultDiv.style.color = "#856404";
                            resultDiv.style.display = "block";
                            return;
                        }

                        if (userInput === correctAnswer) {
                            resultDiv.innerHTML = "✓ 答对了！继续加油！";
                            resultDiv.style.backgroundColor = "#D4EDDA";
                            resultDiv.style.color = "#155724";
                        } else {
                            resultDiv.innerHTML = "✗ 正确答案是: " + correctAnswer + " (再试试吧！)";
                            resultDiv.style.backgroundColor = "#F8D7DA";
                            resultDiv.style.color = "#721C24";
                        }

                        resultDiv.style.display = "block";

                        // 添加动画效果
                        resultDiv.style.animation = "fadeIn 0.3s ease";
                    }

                    function clearInputBack() {
                        document.getElementById("user-input-back").value = "";
                        document.getElementById("result-back").style.display = "none";
                        document.getElementById("user-input-back").focus();
                    }

                    // 反面初始化
                    document.addEventListener('DOMContentLoaded', function() {
                        // 设置输入框placeholder颜色
                        var style = document.createElement('style');
                        style.innerHTML = `
                            #user-input-back::placeholder {
                                color: #888;
                                opacity: 1;
                            }
                            #user-input-back:-ms-input-placeholder {
                                color: #888;
                            }
                            #user-input-back::-ms-input-placeholder {
                                color: #888;
                            }
                            .fade-in {
                                animation: fadeIn 0.3s ease;
                            }
                        `;
                        document.head.appendChild(style);

                        // 添加回车键支持
                        document.getElementById("user-input-back").addEventListener("keypress", function(event) {
                            if (event.key === "Enter") {
                                verifyAnswerBack();
                            }
                        });

                        // 自动聚焦到输入框
                        setTimeout(function() {
                            document.getElementById("user-input-back").focus();
                        }, 100);
                    });
                </script>
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


def text_to_speech(text, filename, lang='ja'):
    """使用gTTS将文本转换为语音并保存为MP3文件"""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        tts.save(filename)
        print(f"已生成音频: {filename}")
        return True
    except Exception as e:
        print(f"生成音频失败: {e}")
        return False


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
                    else:
                        # 自动生成例句
                        example, example_trans = generate_example(word, meaning)

                    vocabulary_list.append({
                        'word': word,
                        'pronunciation': pronunciation,
                        'meaning': meaning,
                        'example': example,
                        'example_trans': example_trans,
                        'section': current_section if current_section else "未分类"  # 确保有分类
                    })

    return vocabulary_list


def generate_example(word, meaning):
    """根据单词和意思自动生成例句"""
    # 简单的例句模板
    templates = [
        f"私は{word}が好きです。",
        f"これは{word}です。",
        f"{word}は大切です。",
        f"昨日{word}を見ました。",
        f"{word}について話しましょう。"
    ]

    trans_templates = [
        f"我喜欢{meaning}。",
        f"这是{meaning}。",
        f"{meaning}很重要。",
        f"昨天看到了{meaning}。",
        f"让我们谈谈{meaning}吧。"
    ]

    # 随机选择一个模板
    index = random.randint(0, len(templates) - 1)

    return templates[index], trans_templates[index]


def generate_audio_files(vocabulary_list, audio_dir="audio"):
    """为所有单词和例句生成音频文件"""
    # 创建音频目录
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)

    # 为每个单词生成音频
    for word_data in vocabulary_list:
        word = word_data['word']
        pronunciation = word_data['pronunciation']
        example = word_data['example']

        # 生成单词音频
        # 使用正则表达式清理文件名，防止特殊字符导致路径问题
        cleaned_word = re.sub(r'[^\w\s-]', '', word)
        word_audio_file = os.path.join(audio_dir, f"{cleaned_word}.mp3")
        if not os.path.exists(word_audio_file):
            print(f"正在生成单词音频: {word}")
            success = text_to_speech(pronunciation, word_audio_file)
            if not success:
                # 如果生成失败，等待一会儿再试
                time.sleep(2)
                text_to_speech(pronunciation, word_audio_file)

        # 生成例句音频（如果有例句）
        if example:
            example_audio_file = os.path.join(audio_dir, f"{cleaned_word}_example.mp3")
            if not os.path.exists(example_audio_file):
                print(f"正在生成例句音频: {word}")
                success = text_to_speech(example, example_audio_file)
                if not success:
                    # 如果生成失败，等待一会儿再试
                    time.sleep(2)
                    text_to_speech(example, example_audio_file)


def generate_anki_deck(vocabulary_list, output_file):
    """生成Anki牌组，并按章节分类"""

    # 顶层牌组名称
    top_deck_name = '圆圆-背词听写版'  # 修改为新的名称

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
        # 构建子牌组的完整名称，直接在顶层牌组下创建章节牌组
        full_deck_name = f"{top_deck_name}::{section_name}"  # 移除了 'N2日语词汇听写' 层级
        deck_id = random.randrange(1 << 30, 1 << 31)
        section_deck = genanki.Deck(deck_id, full_deck_name)

        for word_data in words_in_section:
            # 清理单词用于文件名
            cleaned_word = re.sub(r'[^\w\s-]', '', word_data['word'])

            # 生成音频文件名
            word_audio_file = f"{cleaned_word}.mp3"
            audio_filename = f"[sound:{word_audio_file}]"

            # 生成例句音频文件名（如果有例句）
            example_audio_filename = ""
            if word_data['example']:
                example_audio_file = f"{cleaned_word}_example.mp3"
                example_audio_filename = f"[sound:{example_audio_file}]"

            # 在例句中高亮显示单词
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
    # 读取词汇数据
    txt_file = "n2_vocabulary.txt"
    vocabulary_list = read_vocabulary_from_txt(txt_file)

    print(f"从 {txt_file} 中读取了 {len(vocabulary_list)} 个词汇")

    # 生成音频文件
    print("开始生成音频文件...")
    generate_audio_files(vocabulary_list)
    print("音频文件生成完成")

    # 生成Anki牌组
    output_file = "N2_日语词汇_圆圆背词听写版_优化.apkg"  # 修改输出文件名以匹配顶层牌组名
    generate_anki_deck(vocabulary_list, output_file)

    # 显示一些统计信息
    sections = {}
    for word in vocabulary_list:
        section = word['section']
        sections[section] = sections.get(section, 0) + 1

    print("\n各章节词汇数量:")
    for section, count in sections.items():
        print(f"{section}: {count} 个词汇")

    # 提供使用说明
    print("\n✨ 使用说明（优化版）:")
    print("📱 正面功能:")
    print("  • 显示单词和中文意思，要求输入假名读音")
    print("  • 支持键盘回车键快速提交")
    print("  • 实时答案验证和视觉反馈")
    print("  • 一键重新验证功能")

    print("\n📱 反面功能（最终简化版）:")
    print("  • ✅ 纯答案显示：反面只显示答案，简洁清晰")
    print("  • ✅ 完整信息：显示正确读音、音频、例句及翻译")
    print("  • ✅ 无复杂交互：专注于查看答案，不干扰学习")
    print("  • ✅ 标准Anki体验：使用底部评分按钮进行学习记录")

    print("\n🎯 学习建议:")
    print("  1. 在正面尝试回忆和输入答案")
    print("  2. 点击'显示答案'查看反面的完整答案")
    print("  3. 查看正确读音、听音频、学习例句")
    print("  4. 使用Anki底部的Again/Hard/Good/Easy按钮评分")
    print("  5. 简单直接的学习流程，专注于记忆效果")

    print("\n📊 生成完成:")
    print(f"  • 文件名: {output_file}")
    print(f"  • 音频文件: audio/ 文件夹")
    print(f"  • 总词汇量: {len(vocabulary_list)} 个")


if __name__ == "__main__":
    main()