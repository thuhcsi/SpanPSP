'''
author: cxy
date: 2022/04/05
function: change the data format from raw to tree.
input:  猴子用尾巴荡秋千。
output: (TOP (S (n 猴)(n 子)(n 用))(n 尾)(n 巴)(n 荡)(n 秋)(n 千)(。 。))) 
'''
import re

punctuation_list = ['，','。','、','；','：','？','！','“','”','‘','’','—','…','（','）','《','》']

def data_pre_processing(x):
    x = re.sub('——','—', x)
    x = re.sub('……', '…', x)
    return x

def separate_each_character(x):
    '''
    input:  猴子用尾巴荡秋千。
    output: (n 猴)(n 子)(n 用)(n 尾)(n 巴)(n 荡)(n 秋)(n 千)(。 。)
    '''
    x_list = []
    for i in x:
        if i in punctuation_list:
            i = '(' + i + ' ' + i + ')'
            x_list.append(i)
        else:
            i = '(' + 'n' + ' ' + i + ')'
            x_list.append(i)    
    x = ''.join(x_list)
    return x

def seq2tree(x):
    '''
    input:  (n 猴)(n 子)(n 用)(n 尾)(n 巴)(n 荡)(n 秋)(n 千)(。 。)
    output: (TOP (S (n 猴)(n 子)(n 用)(n 尾)(n 巴)(n 荡)(n 秋)(n 千)(。 。)))
    '''
    tree = '(' + 'TOP' + ' ' + '(' + 'S' + ' ' + x + ')' + ')'
    return tree
        
def main():
    seq_data_path = './data/inference/raw_data/raw_data.txt'
    tree_data_path = './data/inference/tree_data/tree_data.txt'

    line_list = []
    with open(seq_data_path, 'r', encoding='utf-8') as s:
        lines = s.readlines()
        for line in lines:
            line = data_pre_processing(line.strip())
            line = separate_each_character(line)
            line = seq2tree(line)
            line_list.append(line)
        s.close()

    with open(tree_data_path, 'w', encoding='utf-8') as t:
        t.write('\n'.join(line_list))
        t.write('\n') 

if __name__ == '__main__':
    main()
