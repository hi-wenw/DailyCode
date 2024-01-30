import time
    
import os

finance=[]
#显示欢迎信息
def ShowUI():
    os.system("cls")
    welcome='''
                 ()
                 || 
               ||||||
            ||||||||||||      
    |____||||||||||||||||||____|
  ================================
    ||                        ||
    ||    家庭财务分析系统    ||
    ||                        ||
    ||     1-显示财务记录     ||
    ||     2-添加财务记录     ||
    ||     3-删除财务记录     ||
    ||     4-修改财务记录     || 
    ||     5-分析财务记录     ||
    ||     6-退出系统         ||
  ================================
    '''
    print(welcome)
   
#1显示财务记录
def ShowFinalnfo():
    os.system("cls") 
    
    print("月份\t伙食费\t日杂费\t教育费\t服装费\t医疗费\t交通费\t娱乐费\t交际费")
    for finTemp in finance:
        print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(finTemp[0],finTemp[1],finTemp[2],finTemp[3],finTemp[4],finTemp[5],finTemp[6],finTemp[7],finTemp[8]))
    fo=open("../../../Desktop/Finalnfo.csv", "r")
    ls=[]
    for line in fo:
        line=line.replace("\n","")
        ls.append(line.split(","))
    print(ls)
    fo.close()

    input("按任意键返回")
    ShowUI()


#2添加财务记录
def AddFinalnfo():
    os.system("cls") 
    
    hs=input("请输入伙食费：")
    rz=input("请输入日杂费：")
    jy=input("请输入教育费：")
    fz=input("请输入服装费：")
    yl=input("请输入医疗费：")
    jt=input("请输入交通费：")
    yule=input("请输入娱乐费：")
    jj=input("请输入交际费：")
    
    # 定义一个列表，存放单月财务信息
    Finalnfo=[hs,rz,jy,fz,yl,jt,yule,jj]
    # 单月财务信息放入列表  
    finance.append(Finalnfo) 
    print("添加成功！")
    
    ShowFinalnfo()
    

#3删除财务记录
def DelFinalnfo():
    os.system("cls")
    time.sleep(15)



#程序主流程
def main():
    ShowUI()
    while True:
        func=input("请选择您的操作：")
        if func=='1':
            ShowFinalnfo()
        elif func=='2':
            AddFinalnfo()
        elif func=='3':
            DelFinalnfo()
        elif func=='4':
            ModiFinalnfo()
        elif func=='5':
            AnalyFinalnfo()
            print("谢谢使用该系统")
            break
        time.sleep(15)

if __name__=="__main__":
    main()
    time.sleep(15)

