
# with open('Finalnfo.csv','r',encoding='gbk') as f:
#     context = f.read().strip().split('\n')
# print(context)
# for i in context:
#     finTemp = i.strip().split(',')
#     print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(finTemp[0], finTemp[1], finTemp[2], finTemp[3], finTemp[4], finTemp[5],
#                                                 finTemp[6], finTemp[7], finTemp[8]))
# -*- coding: gbk -*-
import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('Finalnfo.csv',
                     names=['�·�','��ʳ��','���ӷ�','������','��װ��','ҽ�Ʒ�','��ͨ��','���ַ�','���ʷ�']
                        ,encoding='gbk')
    print(df)

