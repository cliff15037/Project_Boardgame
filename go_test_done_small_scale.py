import tkinter as tk
from tkinter.messagebox import *
from PIL import Image, ImageTk
import random
import math
import copy


def drawBoard():
    for i in range(9):
        mycanvas.create_line(30, (30 * i + 30), 270, (30 * i + 30))
        mycanvas.create_line((30* i + 30), 30, (30 * i + 30), 270)
    
    for i in range(9):
        UpperLetter = i+65
        mycanvas.create_text(30 + 30*i, 15, text=chr(UpperLetter), fill="black", font=('Helvetica 12'))
        mycanvas.create_text(15, 30 + 30*i, text=i+1, fill="black", font=('Helvetica 12'))
        pass

def callback(event):
    print(event.x)
    print(event.y)
    global click_x, click_y
    click_x  = event.x
    click_y = event.y
    # print("color in callback: ", turn)
    putpiece()
    # turn = change_turn(turn) #棋子顏色交換 B->W, W->B
    
def change_turn(input_turn):
    global turn
    print("start change")
    if input_turn=="black":
        turn = "white"
    elif input_turn=="white":
        turn = "black"
    # elif input_turn=="blue":
    #     turn = "black"

# 吃子     
def delete_eaten_piece(pieces_can_be_eat):
    global board_status, board_stack, board_pieceID_status, safe, eat
    print("In delete_eaten_piece")
    print("pieces_can_be_eat: ",pieces_can_be_eat)

    for E in pieces_can_be_eat:
        for e in E:
            i = e[0]
            j = e[1]
            print("i, j : ", i, j)
            mycanvas.delete(board_pieceID_status[i][j])
            board_pieceID_status[i][j]=-1
            board_status[i][j]=0
    
    pass


def dfs_CheckClose(i, j, copy_board_status, group):
    #只要還能接觸到0，就不會被吃掉
    print("In dfs_CheckClose i, j : ", i, j)
    global board_status, turn, safe
    m = len(board_status)
    n = len(board_status[0])
    print("m: ",m)
    print("n: ",n)
    if i<0 or j<0 or i>=m or j>=n or copy_board_status[i][j]==-1:
        return

    if copy_board_status[i][j]==0:
        print("In i, j, safe change to True", i ,j)
        safe=True
        return
    
    if copy_board_status[i][j]!=group:
        return
    copy_board_status[i][j] = -1
    dfs_CheckClose(i-1, j, copy_board_status, group)
    dfs_CheckClose(i, j-1, copy_board_status, group)
    dfs_CheckClose(i+1, j, copy_board_status, group)
    dfs_CheckClose(i, j+1, copy_board_status, group)

#落子時確認上下左右是否已經被包圍
def alreadyclosed(group, i, j):
    # i, j 是落子位置，group是落子的顏色
    # 以下是錯的，應該要用dfs判斷這顆下下去，相連的，自己的顏色是否還活著
    print("In alreadyclosed: ", i,j)
    print("group: ", group)
    global safe, board_status
    copy_board_status = copy.deepcopy(board_status) #深層複製一份棋盤現在的狀態
    m = len(board_status)
    n = len(board_status[0])
    copy_board_status[i][j] = -1
    print("board_status: ",board_status)
    print("safe 0 : ",safe)
    if i-1>=0:
        if board_status[i-1][j]==0:
            print("在這裡")
            safe=True
        elif board_status[i-1][j]==group:
            dfs_CheckClose(i-1, j, copy_board_status, group)
            print("在那裡")
        print("safe 1 : ",safe)
    if j-1>=0:
        if board_status[i][j-1]==0:
            safe=True
        elif board_status[i][j-1]==group:
            dfs_CheckClose(i, j-1, copy_board_status, group)
        print("safe 2 : ",safe)
    if i+1<m:
        if board_status[i+1][j]==0:
            safe=True
        elif board_status[i+1][j]==group:
            dfs_CheckClose(i+1, j, copy_board_status, group)
        print("safe 3 : ",safe)
    if j+1<n:
        if board_status[i][j+1]==0:
            safe=True
        elif board_status[i][j+1]==group:
            dfs_CheckClose(i, j+1, copy_board_status, group)
        print("safe 4 : ",safe)
    

#落子
def putpiece():
    print("step: ", 6)
    if(click_x>=30 and click_x<=270 and click_y>=30 and click_y<=270):
        pass
        print("範圍正確")
        if not gameOver:#遊戲尚未結束，才可以落子
            print("落子者:", turn)

            #設定落子只能在線的交界處
            if click_x%30 <= 30/2 :
                pos_x = math.floor(click_x/30)*30
            else:
                pos_x = math.ceil(click_x/30)*30
            if click_y%30 <= 30/2 :
                pos_y = math.floor(click_y/30)*30
            else:
                pos_y = math.ceil(click_y/30)*30
            
            global board_status, board_stack, board_pieceID_status, safe, eat, cannot_be_eaten_this_round
            print("落子前: ",board_status)
            print("turn 1 : ",turn)
            # 0是空，1是黑，2是白
            # 一個位子只能下一次
            i = int(pos_x/30)-1
            j = int(pos_y/30)-1
            print("i, j : ", i, j)
            if turn=="black":
                group=1
            elif turn=="white":
                group=2
            #### 基礎訊息處理完畢

             
            if board_status[i][j] == 0:
                piece_id = mycanvas.create_oval(pos_x - radius, pos_y - radius,
                                pos_x + radius, pos_y + radius,
                                fill = turn)
                txt = tk.StringVar()
                if turn=="black":
                    board_status[i][j] = 1
                    txt.set("換白棋走")
                elif turn=="white":
                    board_status[i][j] = 2
                    txt.set("換黑棋走")
                print("turn 2 : ",turn)
                label = tk.Label(root, textvariable=txt, font=("標楷體",15))
                label.grid(row = 1,column = 1)
                board_pieceID_status[i][j] = piece_id
            
            #看能不能吃子
            pieces_can_be_eat = CanEat(i, j)
            print("#2# pieces_can_be_eat : ",pieces_can_be_eat)
            if len(pieces_can_be_eat)>0:
                # 看看有沒有人現在吃到無敵星星(就是這輪不能被吃)
                super_star=[]
                illegal = False
                print("cannot_be_eaten_this_round 1 : ",cannot_be_eaten_this_round)
                if cannot_be_eaten_this_round:
                    super_star = cannot_be_eaten_this_round.pop()
                print("super star : ",super_star)
                print("#1# pieces_can_be_eat : ",pieces_can_be_eat)
                if super_star:
                    #看看吃掉的有沒有無敵星星，有舊不合法
                    for E in pieces_can_be_eat:
                        for e in E:
                            if super_star[0]==e[0] and super_star[1]==e[1]:
                                illegal = True
                                break
                            if illegal:
                                break
                print("illegal: ",illegal)

                if not illegal:
                    print("i, j放下去可以安心吃子", i,j)
                    eat.append(pieces_can_be_eat)
                    cannot_be_eaten_this_round.append([i,j])
                    print("cannot_be_eaten_this_round 2 : ",cannot_be_eaten_this_round)
                    board_stack.append([i, j, group, piece_id, True])#(i,j)是座標，group是黑子(1)白子(2)，piece_id代表image編號
                    #True or False代表這一步棋有沒有吃子
                    delete_eaten_piece(pieces_can_be_eat)
                    change_turn(turn) #棋子顏色交換 B->W, W->B
                else:
                    print("違法落子")
                    mycanvas.delete(piece_id)
                    board_pieceID_status[i][j] = -1
                    board_status[i][j]=0
                    if turn=="black":
                        txt.set("換黑棋走")
                    elif turn=="white":
                        txt.set("換白棋走")
                    label = tk.Label(root, textvariable=txt, font=("標楷體",15))
                    label.grid(row = 1,column = 1)
            else:
                safe=False
                alreadyclosed(group, i, j)
                print("safe after alreadyclosed : ",safe)
                print("turn 3 : ",turn)
                if safe:
                    print("安全落子")
                    board_stack.append([i, j, group, piece_id, False])
                    change_turn(turn) #棋子顏色交換 B->W, W->B
                else:
                    print("違法落子")
                    mycanvas.delete(piece_id)
                    board_pieceID_status[i][j] = -1
                    board_status[i][j]=0
                    if turn=="black":
                        txt.set("換黑棋走")
                    elif turn=="white":
                        txt.set("換白棋走")
                    label = tk.Label(root, textvariable=txt, font=("標楷體",15))
                    label.grid(row = 1,column = 1)
                
                    
            print("turn 5 : ",turn)

            safe=False
            print("safe in putpiece : ", safe)
            print("pieces_can_be_eat: ",pieces_can_be_eat)
            print("落子後: ",board_status)
            print("堆疊狀態: ", board_stack)
            pass
    pass

#悔棋功能
def withdraw():
    global board_status, board_stack, turn, board_pieceID_status, eat
    if len(board_stack)>0:
        current_piece = board_stack.pop()# 裡面的元素是: (x, y, whose turn, id of the piece used to delete icon有有沒有吃子)
        i = current_piece[0]
        j = current_piece[1]
        who_go_now = current_piece[2]
        current_id = current_piece[3]
        eat_or_not = current_piece[4]

        board_status[i][j]=0
        board_pieceID_status[i][j] = -1
        print("turn 1: ", turn)
        print("board_stack in withdraw 1 : ",board_stack)
        if eat_or_not:
            #悔棋的這手有吃掉對手
            piece_eaten = eat.pop()
            color = turn
            print("color: ",color)
            #需要將這些被吃掉的，已經被削除的image重建回來
            # board_status這些被吃掉的位子，已經改成0
            #但是重建後的image，id已經和原來的不同了，會對之後的操作產生問題
            # board_pieceID_status這些被吃掉的位子，已經改成-1，# 要根據每個重建的圖片id以及i,j修改
            new_image_pos_id=[]
            for E in piece_eaten:
                for e in E:
                    i=e[0]
                    j=e[1]
                    pos_x = (i+1)*30
                    pos_y = (j+1)*30
                    piece_id = mycanvas.create_oval(pos_x - radius, pos_y - radius,
                                   pos_x + radius, pos_y + radius,
                                   fill = turn)
                    board_pieceID_status[i][j]=piece_id
                    new_image_pos_id.append([i, j, piece_id])
                    if turn=="black":
                        board_status[i][j]=1
                    elif turn=="white":
                        board_status[i][j]=2
                    pass
            
            # 要根據每個重建的圖片(i,j)，修改其他有紀錄id的地方的id值，修改board_stack
            board_stack_temp=[]
            while board_stack:#堆疊尚未清空
                temp = board_stack.pop()
                #用for loop改掉image id
                for i in new_image_pos_id:
                    if temp[0]==i[0] and temp[1]==i[1]:
                        temp[3]=i[2] #圖片id修改
                board_stack_temp.append(temp)
            while board_stack_temp:
                temp = board_stack_temp.pop()
                board_stack.append(temp)
        print("board_stack in withdraw 2 : ",board_stack)
        print("board_pieceID_status: ", board_pieceID_status)
        
        print("turn: ",turn)
        mycanvas.delete(current_id)
        change_turn(turn) #棋子顏色交換 B->W, W->B
        print("turn: ",turn)
        
        if who_go_now == 1:
            who = "黑棋"
        elif who_go_now == 2:
            who = "白棋"

        txt = tk.StringVar()
        txt.set("換" + who +"走")
        label = tk.Label(root, textvariable=txt, font=("標楷體",15))
        label.grid(row = 1,column = 1)
    pass


def clear_board():
    global board_status, board_stack, turn
    mycanvas.delete("all")
    drawBoard()
    # 將記錄用的變數，恢復到初始設定
    turn = "black"
    txt = tk.StringVar()
    txt.set("換黑棋走")          
    label = tk.Label(root, textvariable=txt, font=("標楷體",15))
    label.grid(row = 1,column = 1)
    
    board_status = [[0 for _ in range(9)] for _ in range(9)]
    board_stack=[]


def dfs(i, j, copy_board_status, group, eat):
  #只要還能接觸到0，就不會被吃掉
  print("In dfs i, j : ", i, j)
  global board_status, turn, safe
  m = len(board_status)
  n = len(board_status[0])
  print("m: ",m)
  print("n: ",n)
  if i<0 or j<0 or i>=m or j>=n or copy_board_status[i][j]==-1:
    return []

  if copy_board_status[i][j]==0:
      print("In i, j, safe change to True", i ,j)
      safe=True
      return []

  if copy_board_status[i][j]!=group:
    return []

  # print("here 1")
  copy_board_status[i][j] = -1
  
  dfs(i-1, j, copy_board_status, group, eat)
  dfs(i, j-1, copy_board_status, group, eat)
  dfs(i+1, j, copy_board_status, group, eat)
  dfs(i, j+1, copy_board_status, group, eat)

  if safe==True:
    return[]
  else:
    eat.append([i,j])
    return eat

def CanEat(i, j):
    # i, j 是剛剛放下去的棋子位置
    global board_status, safe
    copy_board_status = copy.deepcopy(board_status) #深層複製一份棋盤現在的狀態
    # 根據i, j位置，朝上下左右看看，是否封殺了一片敵方
    canEat = [] #紀錄現在這顆子落下後，能被吃掉的區塊的落子訊息，一顆子4氣，canEat內最多4個list
    # upper (說是upper，但應該是left，因為畫出來的棋盤，行列和一般矩陣式相反的，但不影響計算)
    
    ally = board_status[i][j] #現在是黑色要吃別人，allay就是1，白色就是2
    # print("ally: ", ally)
    # print("copy_board_status 0: ", copy_board_status)

    #分4個方向看是不是可以吃掉那一塊，同時用copy_board_status檢查有沒有可能
    #有重複，譬如說，上方和左方其實是一個相同的區塊
    #將吃掉的區塊加入canEat
    
    m = len(board_status)
    n = len(board_status[0])

    if j-1>=0 and copy_board_status[i][j-1] != -1 and board_status[i][j-1]!=ally and board_status[i][j-1]!=0:
        
        group = board_status[i][j-1] #紀錄是哪個陣營的棋子
        eat=[]
        safe = False
        res = dfs(i, j-1, copy_board_status, group, eat)
        if len(res)>0:
            canEat.append(res)
        print("safe1 in CanEat: ", safe)
    # print("copy_board_status 1: ", copy_board_status)

    if i-1>=0 and copy_board_status[i-1][j] != -1 and board_status[i-1][j]!=ally and board_status[i-1][j]!=0:
        
        group = board_status[i-1][j] #紀錄是哪個陣營的棋子
        print("group: ", group)
        eat=[]
        safe = False
        res = dfs(i-1, j, copy_board_status, group, eat)
        if len(res)>0:
            canEat.append(res)
        print("safe2 in CanEat : ", safe)
    # print("copy_board_status 2: ", copy_board_status)

    if i+1<m and copy_board_status[i+1][j] != -1 and board_status[i+1][j]!=ally and board_status[i+1][j]!=0:
        group = board_status[i+1][j] #紀錄是哪個陣營的棋子
        eat=[]
        safe = False
        res = dfs(i+1, j, copy_board_status, group, eat)
        if len(res)>0:
            canEat.append(res)
        print("safe3 in CanEat : ", safe)
    # print("copy_board_status 3: ", copy_board_status)

    if j+1<n and copy_board_status[i][j+1] != -1 and board_status[i][j+1]!=ally and board_status[i][j+1]!=0:
        print("進入")
        group = board_status[i][j+1] #紀錄是哪個陣營的棋子
        eat=[]
        safe = False
        res = dfs(i, j+1, copy_board_status, group, eat)
        if len(res)>0:
            canEat.append(res)
        print("safe4 in CanEat : ", safe)
    # print("copy_board_status 4: ", copy_board_status)

    return canEat




if __name__ == '__main__':
    root = tk.Tk()
    root.title("自訂義圍棋")

    gameOver = False
    gameoverStr = 'Game Over Score '

    #先手是黑色
    turn = "black" #"white" 決定誰先走
    safe = False #在要吃子時，判斷是否能夠吃
    # 0是空，1是黑，2是白
    board_status = [[0 for _ in range(9)] for _ in range(9)]
    board_pieceID_status = [[-1 for _ in range(9)] for _ in range(9)]
    # print(board_status)
    # print(board_pieceID_status)
    board_stack=[] # 裡面的元素是: (x, y, whose turn, id of the piece used to delete icon, 有沒有吃子)
    eat = []# stack用來記錄某次成功吃子時，被吃掉的子有哪些[[],[]...]
    # 設定棋盤
    radius=10 # 棋子半徑
    mycanvas = tk.Canvas(root, bg='#cb9d06', width=480, height=480)
    mycanvas.grid(row = 0, column = 0, rowspan = 10) #合併鄰近的多個網格來放置一個元件
    
    # 一個stack，紀錄剛剛吃了別人的棋子，不能馬上被吃回去
    cannot_be_eaten_this_round=[]

    drawBoard()
    

    button1 = tk.Button(root, text="重 来",font=('標楷體', 15),fg='blue',width=10,height=2,command = clear_board)
    button1.grid(row = 4,column = 1)
    button2 = tk.Button(root, text="悔 棋",font=('標楷體', 15),fg='red',width=10,height=2, command=withdraw)
    button2.grid(row = 5,column = 1)

    # mycanvas.pack() # grid已經被使用時，不要用pack()
    txt = tk.StringVar()
    txt.set("黑棋先走")
    label = tk.Label(root, textvariable=txt, font=("標楷體",15))
    label.grid(row = 1,column = 1)

    # Tkinter 在mainloop()生命週期中，等待事件的發生: 事件可能是 按键按下, 滑鼠點擊, 滑鼠移動...
    #將發生的事件和回應函數做結合bind
    # <Button-1>是滑鼠左鍵，當前位置x,y儲存在event中，給callback
    mycanvas.bind("<Button-1>", callback) 

    root.mainloop()