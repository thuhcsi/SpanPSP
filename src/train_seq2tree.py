'''
author: cxy
date: 2022/04/05
function: change the data format from raw to tree and split into train, validate and test.
input:  猴子#2用#1尾巴#2荡秋千#3。
output:   (TOP (S (#3 (#2 (#1 (n 猴)(n 子))) (#2 (#1 (n 用))(#1 (n 尾)(n 巴))) (#2 (#1 (n 荡)(n 秋)(n 千)))) (。 。))) 
'''
import re
from sklearn.model_selection import train_test_split


punctuation_list = ['，','。','、','；','：','？','！','“','”','‘','’','—','…','（','）','《','》']

def data_pre_processing(x):
    x = re.sub('——','—', x)
    x = re.sub('……', '…', x)
    return x



def separate_each_character(x):
    '''
    input:  猴子#2用#1尾巴#2荡秋千#3。
    output: (n 猴)(n 子)2(n 用)1(n 尾)(n 巴)2(n 荡)(n 秋)(n 千)3(。 。)
    '''
    x = re.sub('#','',x)
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
    '''
    input:  (n 猴)(n 子)2(n 用)1(n 尾)(n 巴)2(n 荡)(n 秋)(n 千)3(。 。)
    output: (TOP (S (#3 (#2 (#1 (n 猴)(n 子)))(#2 (#1 (n 用))(#1 (n 尾)(n 巴)))(#2 (#1 (n 荡)(n 秋)(n 千))))(。 。)))
    '''
    iph_list = x.split('3')
    iph_ = []
    for iph in iph_list[:-1]:
        pph_list = iph.split('2')
        pph_ = []
        for pph in pph_list:
            pw_list = pph.split('1')
            pw_ = []
            for pw in pw_list:
                pw = '(' + '#1' + ' ' + pw + ')'
                pw_.append(pw)
            pw_ = ''.join(pw_)
            pw_ = '(' + '#2' + ' ' + pw_ + ')'
            pph_.append(pw_)
        pph_ = ''.join(pph_)
        pph_ = '(' + '#3' + ' ' + pph_ + ')'
        iph_.append(pph_)
    iph_.append(iph_list[-1])
    iph_ = ''.join(iph_)
    tree = '(' + 'TOP' + ' ' + '(' + 'S' + ' ' + iph_ + ')' + ')'
    return tree
        

def write_data(output_path, line_sen_list):
    '''
    output_path: 需要写入的文件地址
    line_sen_list: 需要写入的文件内容行列表
    '''
    with open(output_path, 'w', encoding = 'utf-8') as o:
        o.write('\n'.join(line_sen_list))
        o.close()


def main():

    seq_data_path = './data/train/raw_data/raw_train.txt'
    train_data_path = './data/train/tree_data/tree_train.txt'
    validate_data_path = './data/train/tree_data/tree_validate.txt'
    test_data_path = './data/train/tree_data/tree_test.txt'

    ## raw2tree
    line_list = []
    with open(seq_data_path, 'r', encoding='utf-8') as s:
        lines = s.readlines()
        for line in lines:
            line = data_pre_processing(line.strip())
            line = separate_each_character(line)
            line = seq2tree(line)
            line_list.append(line)
        s.close()

    ## divide dataset into train, validate, test with 8:1:1
    X_train, X_validate_test, _, y_validate_test = train_test_split(line_list, [0] * len(line_list), test_size = 0.2, random_state = 42)
    X_validate, X_test, _, _ = train_test_split(X_validate_test, y_validate_test, test_size = 0.5, random_state = 42)

    write_data(train_data_path, X_train)
    write_data(validate_data_path, X_validate)
    write_data(test_data_path, X_test)


if __name__ == '__main__':
    main()

