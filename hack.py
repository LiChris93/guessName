def hack(hackTarget, knownSongsList, guessed=[], placeholder="·"):
    """_summary_

    Args:
        hackTarget (str): 要hack的目标
        knownSongsList (list): 已知的所有曲目
        guessed (list, optional): 已开的字母. Defaults to [].
        placeholder (str, optional): 占位符. Defaults to '·'.

    Returns:
        list: 所有可能的hack结果
    """
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
                break  # 这个break只是跳出子循环(其实没有也无妨,但加上可以节省资源)
            elif (
                hackTarget_char[index] != placeholder
                and expected_result_char[index] != hackTarget_char[index]
            ):  # 与已开的字母不符,跳过
                continueBool = True
                break
            elif (
                expected_result_char[index].lower() in guessed
                and hackTarget_char[index] == placeholder
            ):  # 我不会表达,请看这张图https://img2.imgtp.com/2024/03/24/jEW0FSyk.png
                continueBool = True
                break
            else:
                temp += j
        if continueBool:
            continue
        hackResult.append(temp)
    return hackResult


if __name__ == "__main__":
    songsFile = open("songsofarc_casediffered.txt")  # 打开文件
    knownSongsList = []  # 已知的所有歌曲(从文件里读取)
    for i in songsFile.readlines():
        knownSongsList.append(i.strip("\n"))  # 逐行读取(并且去掉最后的换行)
    songsFile.close()  # 关闭文件
    print(
        hack(
            input("要hack的目标:"),
            knownSongsList,
            input("已开的字母(用,隔开):").split(","),
            input("占位符:"),
        )
    )
