from random import randint

valid_char = [
    char
    for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890()-.,'!μ~#?[]"
]  # 定义有效字符
placeholder = "·"


def main(lines, hardMode=False):
    """_summary_

    Args:
        lines (int): 要猜的歌数
        hardMode (Boolean): 困难模式,默认False

    Raises:
        IndexError: 要猜的歌数大于已知歌曲数量
    """
    # 读取 start
    songsFile = open("./songsofarc.txt")  # 打开文件
    knownSongsList = []  # 已知的所有歌曲(从文件里读取)
    for i in songsFile.readlines():
        knownSongsList.append(i.strip("\n"))  # 逐行读取(并且去掉最后的换行)
    songsFile.close()  # 关闭文件
    if lines > len(knownSongsList):
        raise IndexError("输入的值大于已知歌曲数量!")
    # 读取 end
    # 随机抽取 start
    index = []
    while len(index) < lines:
        randnum = randint(
            0, len(knownSongsList) - 1
        )  # 随机数,范围为列表knownSongsList的元素个数
        if randnum in index:  # 若重复则跳过本循环,进入下一轮循环
            continue
        else:  # 不重复,将索引值写入索引列表
            index.append(randnum)
    result = []
    for i in range(lines):
        result.append(
            knownSongsList[index[i]]
        )  # 从已知的所有歌曲中，按照索引列表获得随机抽取后的结果
    # 随机抽取 end
    # 开字母 start
    guessed = [" "]
    laps = 1  # 轮数
    score = -1  # 分数
    if hardMode:  # 困难模式配置
        print("困难模式!!!")
        global valid_char
        valid_char = [
            char
            for char in "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ1234567890()-.,'!μ~#?[]"
        ]  # 去掉元音
        score = 10 * lines  # 按照总数确定总分数
    while True:
        print(f"\n第{laps}轮!")
        if hardMode:
            print(f"现在分数:{score}分")
        # 处理加密文本 start
        result_blocked = []  # 加密文本
        for i in result:  # 字符串
            temp = ""
            if i in guessed:  # 已被猜中,不用做星号处理
                temp = i
            else:  # 未被猜中,做星号处理
                for j in [char for char in i]:  # 字符数组
                    if j not in guessed:  # 字符没有被开
                        temp += placeholder
                    else:  # 字符已被开
                        temp += j
            result_blocked.append(temp)  # 添加进加密文本里
        # 显示已经开的字母
        guessed_charaters = []
        for i in guessed:
            if i in valid_char:  # 是有效字符
                guessed_charaters.append(i)
        if len(guessed_charaters) == 0:
            print("已开的字母:无")
        else:
            print(f"已开的字母:{guessed_charaters}")
        # 显示已经猜中的歌
        guessed_songs = []
        for i in guessed:
            if i in result:  # 是有效歌曲
                guessed_songs.append(i)
        if len(guessed_songs) == 0:
            print("已猜中的歌:无")
        else:
            print(f"已猜中的歌:{guessed_songs}")
        # 显示加密文本
        for i in range(lines):
            print(f"{i+1}.{result_blocked[i]}")
        # 处理加密文本 end
        # 游戏结束判断 start
        nostar = True
        for i in result_blocked:
            if placeholder in i:
                nostar = False
        if nostar and hardMode:
            print(f"星号已全部消失,游戏结束!一共猜了{laps-1}次!分数为{score}!")
            break
        elif nostar:
            print(f"星号已全部消失,游戏结束!一共猜了{laps-1}次!")
            break
        if hardMode and score <= 0:
            print(f"分数<=0,游戏结束!一共猜了{laps-1}次!正确答案为:")
            for i in range(lines):
                print(f"{i+1}.{result[i]}")
            break
        # 游戏结束判断 end
        # 输入判断 start
        user_input = input(
            "请输入一个字母(无需区分大小写)或者输入完整歌名(需全部为小写):"
        )
        if user_input in result:  # 猜中
            if user_input not in guessed:
                guessed.append(user_input)
            else:
                print(f"歌曲{user_input}已经被猜中了!")
        elif user_input in valid_char:  # 没猜中,开字母
            if user_input.lower() not in guessed:
                guessed.append(user_input.lower())
                if hardMode:  # 困难模式扣分
                    score -= 1
                    print("开一个字母,分数-1")
            else:
                print(f"字符{user_input.lower()}已经被开过了!")
        else:  # 其他
            if hardMode:  # 困难模式扣分
                score -= 2
                print("非法字符,或者歌名错误!!!分数-2")
            else:
                print("非法字符,或者歌名错误!!!")
        # 输入判断 end
        laps += 1
    # 开字母 end


if __name__ == "__main__":
    try:  # 异常处理
        num = int(input("要猜的歌数(请输入数字):"))
        hard = bool(
            int(
                input(
                    "\n是否启用困难模式?\n困难模式有如下规则:\n1.不可开元音字母(aeiou)\n2.采用计分制,满分为10x歌曲数量,开一个字母-1分,输入错误-2分\n启用请输入任意非0数字,否则输入0:"
                )
            )
        )
        main(num, hard)
    except KeyboardInterrupt:
        print("\n你使用了Ctrl+C,游戏结束!")
    except ValueError as e:
        print(f"ValueError:{e}\n输入错误!请输入数字!")
    except IndexError as e:
        print(f"IndexError:{e}")
    except FileNotFoundError as e:
        print(
            f"FileNotFoundError:{e}\ntxt文件未找到!请确定.py与.txt位于同一文件夹内,并cd到该文件夹!"
        )
