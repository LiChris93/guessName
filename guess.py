import random
valid_char = [char for char in 'abcdefghijklmnopqrstuvwxyz1234567890()-.,\'!μ~#?']#定义有效字符
placeholder = '·'
def main(lines):
    #读取 start
    songs = open('./songsofarc.txt')
    pattern = []
    for i in songs.readlines():
        pattern.append(i.strip("\n"))
    songs.close()
    #读取 end
    #随机抽取 start
    index = []
    while len(index) < lines:
        randnum = random.randint(0,len(pattern)-1)#随机数,范围为列表pattern
        if randnum in index:
            continue
        else:
            index.append(randnum)
    result = []
    for i in range(lines):
        result.append(pattern[index[i]])
    #随机抽取 end
    #开字母 start
    guessed = [' ']
    while True:
        #处理加密文本 start
        result_blocked = []#加密文本
        for i in result:#字符串
            temp=''
            if i in guessed:#已被猜中，不用做星号处理
                temp = i
            else:#未被猜中，做星号处理
                for j in [char for char in i]:#字符数组
                    if not j in guessed:#字符没有被开
                        temp += placeholder
                    else:#字符已被开
                        temp += j
            result_blocked.append(temp)#添加进加密文本里
        #显示已经开的字母
        guessed_charaters = []
        for i in guessed:
            if i in valid_char and i not in guessed_charaters:#是有效字符并且不重复
                guessed_charaters.append(i)
        if(len(guessed_charaters) == 0):
            print("已开的字母:无")
        else:
            print(f"已开的字母:{guessed_charaters}")
        #显示已经猜中的歌
        guessed_songs = []
        for i in guessed:
            if i in result and i not in guessed_songs and i != ' ':#是有效歌曲并且不重复
                guessed_songs.append(i)
        if(len(guessed_songs) == 0):
            print("已猜中的歌:无")
        else:
            print(f"已猜中的歌:{guessed_songs}")        
        #显示加密文本
        for i in range(lines):
            print(f"{i+1}.{result_blocked[i]}")
        #处理加密文本 end
        #游戏结束判断 start
        nostar = True
        for i in result_blocked:
            if placeholder in i:
                nostar = False
        if nostar:
            print("星号已全部消失，游戏结束！")
            break
        #游戏结束判断 end
        #输入判断 start
        user_input = input("请输入一个字母(无需区分大小写)或者输入完整歌名(需全部为小写):")
        if user_input in result:#猜中
            if user_input not in guessed:
                guessed.append(user_input)
            else:
                print(f'歌曲{user_input}已经被猜中了!')
        elif user_input in valid_char:#没猜中，开字母
            if user_input.lower() not in guessed:
                guessed.append(user_input.lower())
            else:
                print(f'字符{user_input.lower()}已经被开过了!')
        else:#其他
            print("非法字符，或者歌名错误!!!")
        #输入判断 end
    #开字母 end
if __name__ == '__main__':
    try:
        num = int(input("要猜的歌数(请输入数字):"))
        main(num)
    except KeyboardInterrupt:
        print("游戏结束！")
    except:
        print("输入错误！")
