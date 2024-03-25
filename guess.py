from random import sample
import re

valid_char = [
    char
    for char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890()-.,'!μ~#?[]"
]  # 定义有效字符
placeholder = "·"


def main(lines, hardMode=False, groupMode=False):
    """_summary_

    Args:
        lines (int): 要猜的歌数
        hardMode (Boolean): 困难模式,默认False
        groupMode (Boolean): 群聊模式,默认False

    Raises:
        IndexError: 要猜的歌数大于已知歌曲数量
    """
    # 读取 start
    songsFile = open(
        {True: "songsofarc_casediffered.txt", False: "songsofarc.txt"}[groupMode]
    )  # 打开文件
    knownSongsList = []  # 已知的所有歌曲(从文件里读取)
    for i in songsFile.readlines():
        knownSongsList.append(i.strip("\n"))  # 逐行读取(并且去掉最后的换行)
    songsFile.close()  # 关闭文件
    if lines > len(knownSongsList):
        raise IndexError("输入的值大于已知歌曲数量!")
    # 读取 end
    # 随机抽取 start
    result = sample(knownSongsList, lines)
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
    if groupMode:  # 群聊模式下先输出答案
        print(result)
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
                    if j.lower() not in guessed:  # 字符没有被开
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
        elif groupMode and re.match(r"ans [0-9]+", user_input) != None:  # ans
            guessed.append(result[int(re.search(r"[0-9]+", user_input).group()) - 1])
        elif groupMode and re.match(r"hack [0-9]+", user_input) != None:  # hack
            laps -= 1  # 用hack不算轮数
            hackTarget = result_blocked[
                int(re.search(r"[0-9]+", user_input).group()) - 1
            ]  # 要hack的目标
            print(hackTarget)
            for i in hack(hackTarget, knownSongsList, guessed):
                print(i)
        else:  # 其他
            if hardMode:  # 困难模式扣分
                score -= 2
                print("非法字符,或者歌名错误!!!分数-2")
            else:
                print("非法字符,或者歌名错误!!!")
        # 输入判断 end
        laps += 1
    # 开字母 end


def hack(hackTarget, knownSongsList, guessed):
    hackTarget_char = [char for char in hackTarget]  # 字符串转换成字符
    hackResult = []  # 所有可能的hack结果
    for i in knownSongsList:
        expected_result_char = [char for char in i]
        if len(expected_result_char) != len(hackTarget_char):  # 位数不对肯定不是
            continue
        temp = ""
        index = -1
        continueBool = False  # 子循环continue父循环辅助工具
        for j in expected_result_char:
            index += 1
            if (
                hackTarget_char[index] == " " and expected_result_char[index] != " "
            ) or (
                hackTarget_char[index] != " " and expected_result_char[index] == " "
            ):  # 空格位置不对,跳过
                continueBool = True
            elif (
                hackTarget_char[index] != placeholder
                and expected_result_char[index] != hackTarget_char[index]
            ):  # 与已开的字母不符,跳过
                continueBool = True
            elif (
                expected_result_char[index].lower() in guessed
                and hackTarget_char[index] == placeholder
            ):  # 我不会表达，请看这张图https://img2.imgtp.com/2024/03/24/jEW0FSyk.png
                continueBool = True
            else:
                temp += j
        if continueBool:
            continue
        hackResult.append(temp)
    return hackResult


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
        group = bool(
            int(
                input(
                    "\n是否启用群聊模式(不懂别启用)?\n启用请输入任意非0数字,否则输入0:"
                )
            )
        )
        main(num, hard, group)
    except KeyboardInterrupt:
        print("\n你使用了Ctrl+C,游戏结束!")
    except ValueError as e:
        print(f"ValueError:{e}\n输入错误!请输入有效的数字!")
    except IndexError as e:
        print(f"IndexError:{e}")
    except FileNotFoundError as e:
        print(
            f"FileNotFoundError:{e}\ntxt文件未找到!请确定.py与.txt位于同一文件夹内,并cd到该文件夹!"
        )
