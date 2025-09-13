import os
import re
from typing import List, Dict, Tuple
import time
import random

class VocabularyCompleter:
    """日语词汇例句自动补全工具"""
    
    def __init__(self):
        # 预设的常用例句模板和词汇对应的例句
        self.example_templates = {
            # 动词类例句模板
            'verb_patterns': [
                "毎日{}ます。",
                "今日は{}ました。", 
                "明日{}つもりです。",
                "{}ことができます。",
                "よく{}ます。",
                "時々{}ます。",
                "一緒に{}ましょう。"
            ],
            
            # 名词类例句模板
            'noun_patterns': [
                "これは{}です。",
                "{}が好きです。",
                "{}を買いました。",
                "{}はとても大切です。",
                "{}について話します。",
                "新しい{}です。",
                "{}を持っています。"
            ],
            
            # 形容词类例句模板
            'adjective_patterns': [
                "とても{}です。",
                "{}天気ですね。",
                "{}人です。",
                "{}ところです。",
                "{}気持ちです。"
            ]
        }
        
        # 具体词汇的专用例句库
        self.specific_examples = {
            # 学习相关
            "勉強": ("毎日日本語を勉強します", "每天学习日语"),
            "学校": ("学校に行きます", "去学校"),
            "先生": ("先生に質問します", "向老师提问"),
            "学生": ("私は大学生です", "我是大学生"),
            "授業": ("授業が始まります", "上课开始了"),
            "宿題": ("宿題を忘れました", "忘记带作业了"),
            "試験": ("来週試験があります", "下周有考试"),
            "教科書": ("教科書を開いてください", "请打开教科书"),
            
            # 工作相关
            "仕事": ("仕事が忙しいです", "工作很忙"),
            "会社": ("会社員として働いています", "作为公司员工工作"),
            "会議": ("午後会議があります", "下午有会议"),
            "社長": ("社長と話しました", "和社长谈话了"),
            "部長": ("部長は優しい人です", "部长是个温和的人"),
            "同僚": ("同僚と昼食を食べます", "和同事吃午饭"),
            "給料": ("給料が上がりました", "工资涨了"),
            "残業": ("今日は残業します", "今天要加班"),
            
            # 家族相关
            "家族": ("家族と旅行します", "和家人旅行"),
            "両親": ("両親に電話します", "给父母打电话"),
            "父": ("父は会社員です", "父亲是公司员工"),
            "母": ("母は料理が上手です", "母亲很会做菜"),
            "兄": ("兄は医者です", "哥哥是医生"),
            "弟": ("弟と映画を見ます", "和弟弟看电影"),
            "姉": ("姉は結婚しました", "姐姐结婚了"),
            "妹": ("妹は高校生です", "妹妹是高中生"),
            "子ども": ("子どもが三人います", "有三个孩子"),
            "夫": ("夫と買い物に行きます", "和丈夫去购物"),
            "妻": ("妻は看護師です", "妻子是护士"),
            
            # 食物相关
            "食べ物": ("美味しい食べ物を作ります", "做美味的食物"),
            "料理": ("日本料理が好きです", "喜欢日本料理"),
            "朝ご飯": ("朝ご飯を食べましょう", "吃早饭吧"),
            "昼ご飯": ("昼ご飯の時間です", "到了吃午饭的时间"),
            "晩ご飯": ("晩ご飯を作ります", "做晚饭"),
            "パン": ("朝はパンを食べます", "早上吃面包"),
            "ご飯": ("ご飯を炊きます", "煮米饭"),
            "肉": ("肉をたくさん食べます", "吃很多肉"),
            "魚": ("魚が新鮮です", "鱼很新鲜"),
            "野菜": ("野菜は健康にいいです", "蔬菜对健康有好处"),
            
            # 饮品相关
            "水": ("冷たい水を飲みます", "喝冷水"),
            "お茶": ("お茶をいれます", "泡茶"),
            "コーヒー": ("朝はコーヒーを飲みます", "早上喝咖啡"),
            "ビール": ("ビールで乾杯します", "用啤酒干杯"),
            "ジュース": ("オレンジジュースが好きです", "喜欢橙汁"),
            "牛乳": ("毎日牛乳を飲みます", "每天喝牛奶"),
            
            # 交通相关
            "電車": ("電車で通勤します", "坐电车通勤"),
            "バス": ("バスが遅れています", "公交车晚点了"),
            "タクシー": ("タクシーを呼びます", "叫出租车"),
            "飛行機": ("飛行機で旅行します", "坐飞机旅行"),
            "自動車": ("新しい自動車を買いました", "买了新车"),
            "自転車": ("自転車で学校に行きます", "骑自行车去学校"),
            "駅": ("駅で待ち合わせます", "在车站碰面"),
            "空港": ("空港に着きました", "到达机场了"),
            
            # 天气相关
            "天気": ("今日はいい天気ですね", "今天天气真好啊"),
            "雨": ("雨が降っています", "正在下雨"),
            "雪": ("雪がたくさん積もりました", "雪积了很多"),
            "風": ("風が強いです", "风很大"),
            "暑い": ("今日はとても暑いです", "今天很热"),
            "寒い": ("冬は寒いです", "冬天很冷"),
            "涼しい": ("秋は涼しいです", "秋天很凉爽"),
            "暖かい": ("春は暖かいです", "春天很温暖"),
            
            # 时间相关
            "時間": ("時間がありません", "没有时间"),
            "今日": ("今日は忙しい日です", "今天是忙碌的一天"),
            "昨日": ("昨日映画を見ました", "昨天看了电影"),
            "明日": ("明日早く起きます", "明天早起"),
            "朝": ("朝早く起きます", "早上早起"),
            "昼": ("昼休みに散歩します", "午休时散步"),
            "夜": ("夜遅くまで勉強します", "学习到深夜"),
            "週末": ("週末に友達と会います", "周末和朋友见面"),
            
            # 感情相关
            "嬉しい": ("とても嬉しいニュースです", "是非常高兴的消息"),
            "悲しい": ("悲しい映画でした", "是悲伤的电影"),
            "楽しい": ("パーティーはとても楽しかったです", "聚会非常愉快"),
            "心配": ("母のことが心配です", "担心母亲"),
            "安心": ("やっと安心しました", "终于安心了"),
            "驚く": ("そのニュースに驚きました", "对那个消息感到惊讶"),
            
            # 颜色相关
            "赤": ("赤いバラが美しいです", "红玫瑰很美丽"),
            "青": ("青い空が広がっています", "蓝天广阔"),
            "白": ("白いシャツを着ています", "穿着白衬衫"),
            "黒": ("黒い猫がいます", "有一只黑猫"),
            "緑": ("緑の木がたくさんあります", "有很多绿树"),
            "黄色": ("黄色い花が咲いています", "黄花盛开"),
            
            # 购物相关
            "買い物": ("スーパーで買い物します", "在超市购物"),
            "店": ("新しい店がオープンしました", "新店开业了"),
            "お金": ("お金を貯めています", "在存钱"),
            "値段": ("値段が高すぎます", "价格太高了"),
            "安い": ("この服は安いです", "这件衣服便宜"),
            "高い": ("そのレストランは高いです", "那家餐厅很贵"),
            
            # 身体相关
            "体": ("毎日体を鍛えます", "每天锻炼身体"),
            "頭": ("頭が痛いです", "头疼"),
            "目": ("目が疲れました", "眼睛累了"),
            "耳": ("音楽を耳で聞きます", "用耳朵听音乐"),
            "口": ("口を開けてください", "请张开嘴"),
            "手": ("手を洗います", "洗手"),
            "足": ("足が痛いです", "脚疼"),
            
            # 房屋相关
            "家": ("家に帰ります", "回家"),
            "部屋": ("部屋を掃除します", "打扫房间"),
            "キッチン": ("キッチンで料理します", "在厨房做菜"),
            "トイレ": ("トイレはどこですか", "厕所在哪里"),
            "ベッド": ("ベッドで休みます", "在床上休息"),
            "窓": ("窓を開けます", "打开窗户"),
            "ドア": ("ドアをノックします", "敲门"),
            
            # 数字相关
            "一": ("一つください", "请给我一个"),
            "二": ("二人で食事します", "两人吃饭"),
            "三": ("三時に会いましょう", "三点见面吧"),
            "十": ("十分待ってください", "请等十分钟"),
            "百": ("百円ショップで買います", "在百元店买"),
            "千": ("千円札を両替します", "兑换千元纸币"),
            "万": ("一万円かかります", "需要一万日元")
        }

    def read_vocabulary_file(self, file_path: str) -> List[Dict]:
        """读取词汇文件"""
        vocabulary_list = []
        current_section = ""
        
        if not os.path.exists(file_path):
            print(f"❌ 文件不存在: {file_path}")
            return vocabulary_list
            
        with open(file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                
                if not line:
                    continue
                    
                # 检测章节标题
                if line.startswith('【') and line.endswith('】'):
                    current_section = line[1:-1]
                    continue
                
                # 解析词汇行
                if '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 3:
                        word = parts[0].strip()
                        pronunciation = parts[1].strip()
                        meaning = parts[2].strip()
                        
                        # 处理例句
                        example = parts[3].strip() if len(parts) > 3 else ""
                        example_trans = parts[4].strip() if len(parts) > 4 else ""
                        
                        vocabulary_list.append({
                            'word': word,
                            'pronunciation': pronunciation,
                            'meaning': meaning,
                            'example': example,
                            'example_trans': example_trans,
                            'section': current_section,
                            'line_num': line_num,
                            'needs_completion': not (example and example_trans)
                        })
                    else:
                        print(f"⚠️ 第{line_num}行格式不正确: {line}")
        
        return vocabulary_list

    def generate_example_for_word(self, word: str, pronunciation: str, meaning: str) -> Tuple[str, str]:
        """为单词生成例句和翻译"""
        
        # 首先检查是否有预设的例句
        if word in self.specific_examples:
            return self.specific_examples[word]
        
        # 根据词性和含义生成例句
        example_jp, example_cn = self._create_contextual_example(word, pronunciation, meaning)
        
        return example_jp, example_cn

    def _create_contextual_example(self, word: str, pronunciation: str, meaning: str) -> Tuple[str, str]:
        """根据上下文创建例句"""
        
        # 判断词性并选择合适的例句模板
        if self._is_verb(word, meaning):
            pattern = random.choice(self.example_templates['verb_patterns'])
            example_jp = pattern.format(word)
            example_cn = f"使用「{word}」的例句：{self._translate_pattern(pattern, word, meaning)}"
        
        elif self._is_adjective(word, meaning):
            pattern = random.choice(self.example_templates['adjective_patterns'])
            example_jp = pattern.format(word)
            example_cn = f"使用「{word}」的例句：{self._translate_pattern(pattern, word, meaning)}"
        
        else:  # 默认当作名词处理
            pattern = random.choice(self.example_templates['noun_patterns'])
            example_jp = pattern.format(word)
            example_cn = f"使用「{word}」的例句：{self._translate_pattern(pattern, word, meaning)}"
        
        return example_jp, example_cn

    def _is_verb(self, word: str, meaning: str) -> bool:
        """判断是否为动词"""
        verb_indicators = ['する', 'います', 'ます', '动', '做', '去', '来', '看', '听', '说', '读', '写', '吃', '喝', '买', '卖', '工作', '学习', '睡觉', '起床']
        return any(indicator in word or indicator in meaning for indicator in verb_indicators)

    def _is_adjective(self, word: str, meaning: str) -> bool:
        """判断是否为形容词"""
        adj_indicators = ['い', '的', '好', '坏', '大', '小', '新', '旧', '高', '低', '长', '短', '快', '慢', '热', '冷', '暖', '凉']
        return any(indicator in word[-1:] or indicator in meaning for indicator in adj_indicators)

    def _translate_pattern(self, pattern: str, word: str, meaning: str) -> str:
        """简单的模板翻译"""
        translations = {
            "毎日{}ます。": f"每天{meaning}",
            "今日は{}ました。": f"今天{meaning}了", 
            "明日{}つもりです。": f"明天打算{meaning}",
            "{}ことができます。": f"能够{meaning}",
            "よく{}ます。": f"经常{meaning}",
            "時々{}ます。": f"有时{meaning}",
            "一緒に{}ましょう。": f"一起{meaning}吧",
            
            "これは{}です。": f"这是{meaning}",
            "{}が好きです。": f"喜欢{meaning}",
            "{}を買いました。": f"买了{meaning}",
            "{}はとても大切です。": f"{meaning}很重要",
            "{}について話します。": f"谈论{meaning}",
            "新しい{}です。": f"新的{meaning}",
            "{}を持っています。": f"有{meaning}",
            
            "とても{}です。": f"非常{meaning}",
            "{}天気ですね。": f"{meaning}的天气呢",
            "{}人です。": f"{meaning}的人",
            "{}ところです。": f"{meaning}的地方",
            "{}気持ちです。": f"{meaning}的心情"
        }
        
        return translations.get(pattern, f"关于{meaning}的句子")

    def complete_vocabulary(self, vocabulary_list: List[Dict]) -> List[Dict]:
        """补全缺少例句的词汇"""
        print("🔍 开始分析词汇文件...")
        
        incomplete_count = 0
        completed_count = 0
        
        for vocab in vocabulary_list:
            if vocab['needs_completion']:
                incomplete_count += 1
                print(f"📝 补全例句: {vocab['word']} ({vocab['meaning']})")
                
                # 生成例句
                example_jp, example_cn = self.generate_example_for_word(
                    vocab['word'], 
                    vocab['pronunciation'], 
                    vocab['meaning']
                )
                
                # 更新词汇信息
                vocab['example'] = example_jp
                vocab['example_trans'] = example_cn
                vocab['needs_completion'] = False
                completed_count += 1
                
                # 添加小延迟，避免处理过快
                time.sleep(0.1)
        
        print(f"✅ 补全完成: {completed_count}/{incomplete_count}")
        return vocabulary_list

    def write_vocabulary_file(self, vocabulary_list: List[Dict], output_path: str):
        """写入补全后的词汇文件"""
        print(f"💾 保存补全后的文件: {output_path}")
        
        # 按章节分组
        sections = {}
        for vocab in vocabulary_list:
            section = vocab['section']
            if section not in sections:
                sections[section] = []
            sections[section].append(vocab)
        
        with open(output_path, 'w', encoding='utf-8') as file:
            for section_name, words in sections.items():
                if section_name:
                    file.write(f"【{section_name}】\n")
                
                for word_data in words:
                    line = f"{word_data['word']}|{word_data['pronunciation']}|{word_data['meaning']}|{word_data['example']}|{word_data['example_trans']}\n"
                    file.write(line)
                
                file.write("\n")  # 章节间空行

    def create_backup(self, original_file: str) -> str:
        """创建原文件备份"""
        backup_file = f"{original_file}.backup_{int(time.time())}"
        if os.path.exists(original_file):
            with open(original_file, 'r', encoding='utf-8') as src:
                with open(backup_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            print(f"📋 已创建备份文件: {backup_file}")
        return backup_file

    def show_statistics(self, vocabulary_list: List[Dict]):
        """显示统计信息"""
        total = len(vocabulary_list)
        incomplete = sum(1 for vocab in vocabulary_list if vocab['needs_completion'])
        complete = total - incomplete
        
        print(f"\n📊 词汇文件统计:")
        print(f"  总词汇数: {total}")
        print(f"  已有例句: {complete}")
        print(f"  需要补全: {incomplete}")
        print(f"  完整率: {(complete/total*100):.1f}%")
        
        # 按章节统计
        sections = {}
        for vocab in vocabulary_list:
            section = vocab['section']
            if section not in sections:
                sections[section] = {'total': 0, 'incomplete': 0}
            sections[section]['total'] += 1
            if vocab['needs_completion']:
                sections[section]['incomplete'] += 1
        
        print(f"\n📚 各章节统计:")
        for section, stats in sections.items():
            complete_rate = ((stats['total'] - stats['incomplete']) / stats['total'] * 100) if stats['total'] > 0 else 0
            print(f"  {section}: {stats['total']}词汇, {stats['incomplete']}待补全 ({complete_rate:.1f}%完整)")

def main():
    print("🎌 日语词汇例句自动补全工具")
    print("=" * 50)
    
    completer = VocabularyCompleter()
    
    # 文件路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(script_dir, 'n2_vocabulary.txt')
    output_file = os.path.join(script_dir, 'n2_vocabulary_completed.txt')
    
    # 检查输入文件
    if not os.path.exists(input_file):
        print(f"❌ 找不到词汇文件: {input_file}")
        print("请确保 'n2_vocabulary.txt' 文件在脚本同目录下")
        return
    
    # 读取词汇文件
    vocabulary_list = completer.read_vocabulary_file(input_file)
    if not vocabulary_list:
        print("❌ 词汇文件为空或格式错误")
        return
    
    # 显示初始统计
    completer.show_statistics(vocabulary_list)
    
    # 确认是否继续
    incomplete_count = sum(1 for vocab in vocabulary_list if vocab['needs_completion'])
    if incomplete_count == 0:
        print("✅ 所有词汇都已有例句，无需补全!")
        return
    
    print(f"\n💡 将为 {incomplete_count} 个词汇补全例句")
    confirm = input("是否继续? (y/N): ").lower().strip()
    
    if confirm not in ['y', 'yes', '是']:
        print("❌ 用户取消操作")
        return
    
    # 创建备份
    completer.create_backup(input_file)
    
    # 补全词汇
    completed_vocabulary = completer.complete_vocabulary(vocabulary_list)
    
    # 保存结果
    completer.write_vocabulary_file(completed_vocabulary, output_file)
    
    # 显示最终统计
    print(f"\n🎉 补全完成!")
    print(f"📄 原文件: {input_file}")
    print(f"📄 新文件: {output_file}")
    print(f"📋 备份文件已创建")
    
    # 询问是否替换原文件
    replace = input(f"\n是否用补全后的文件替换原文件? (y/N): ").lower().strip()
    if replace in ['y', 'yes', '是']:
        os.replace(output_file, input_file)
        print(f"✅ 已更新原文件: {input_file}")
    else:
        print(f"📁 补全后的文件保存为: {output_file}")
    
    print("\n✨ 提示: 可以手动检查和修改生成的例句以确保准确性")

if __name__ == "__main__":
    main()