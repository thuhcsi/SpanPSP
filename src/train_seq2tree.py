## input:  猴子#2用#1尾巴#2荡秋千#3。
## output:   (TOP (S (#3 (#2 (#1 (n 猴)(n 子))) (#2 (#1 (n 用))(#1 (n 尾)(n 巴))) (#2 (#1 (n 荡)(n 秋)(n 千)))) (。 。))) 

import re

punctuation_list = ['，','。','、','；','：','？','！','“','”','‘','’','—','…','（','）','《','》']

def data_pre_processing(x):
    x = re.sub('——','—', x)
    x = re.sub('……', '…', x)
    x = re.sub('#','',x)
    return x

def separate_each_character(x):
    x_list = []
    for i in x:
        if i in ['1', '2', '3']:
            x_list.append(i)
        elif i in punctuation_list:
            i = '(' + i + ' ' + i + ')'
            x_list.append(i)
        else:
            i = '(' + 'n' + ' ' + i + ')'
            x_list.append(i)    
    x = ''.join(x_list)
    return x

def seq2tree(x):
    iph_list = x.split('3')
    iph_ = []
    # print(iph_list)
    for iph in iph_list[:-1]:
        pph_list = iph.split('2')
        # print(pph_list)
        pph_ = []
        for pph in pph_list:
            pw_list = pph.split('1')
            # print('hhh',pw_list)
            pw_ = []
            for pw in pw_list:
                pw = '(' + '#1' + ' ' + pw + ')'
                pw_.append(pw)
            # print('nnn',pw_)
            pw_ = ''.join(pw_)
            # print(pw_)
            pw_ = '(' + '#2' + ' ' + pw_ + ')'
            pph_.append(pw_)
        pph_ = ''.join(pph_)
        pph_ = '(' + '#3' + ' ' + pph_ + ')'
        iph_.append(pph_)
    iph_.append(iph_list[-1])
    iph_ = ''.join(iph_)
    tree = '(' + 'TOP' + ' ' + '(' + 'S' + ' ' + iph_ + ')' + ')'
    return tree
        

def main():
    seq_data_path = './data/train/raw_data/raw_train.txt'
    tree_data_path = './data/train/tree_data/tree_train.txt'

    line_list = []
    with open(seq_data_path, 'r', encoding='utf-8') as s:
        lines = s.readlines()
        for line in lines:
            if line[-1] == '\n':
                line = line[0:-1]
            line = re.sub('4','3',line)
            line = data_pre_processing(line)
            line = separate_each_character(line)
            line = seq2tree(line)
            line_list.append(line)
        s.close()

    with open(tree_data_path, 'w', encoding='utf-8') as t:
        t.write('\n'.join(line_list)) 

main()
