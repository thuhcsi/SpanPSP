import re
import numpy as np

def remove_top(a):
    a = a.replace('(TOP (S ', '')
    a = a[::-1].replace('))', '', 1)[::-1]
    return a

def replace_n(a, i, j, num):
    a = a.replace(i, '*', num)
    a = a.replace('*', i, num-1)
    a = a.replace('*', j)
    return a


def replace1(a):
    a = re.sub('\n', '', a)
    for i in range(len(a)):
        num_left = 0
        num_right = 0
        flag = 0
        for j in range(len(a)):          
            if a[j] == '(' :
                num_left += 1
                if a[j+1] == 'S' and flag == 0:
                    b = a[j+1]
                    flag = 1
                if a[j+1] == '#' and flag == 0:
                    b = a[j+1] + a[j+2]
                    flag = 1
                    # print('mmmmm',b)
            elif a[j] == ')' :
                num_right += 1
                if num_right == num_left and a[j-1] == ')':
                    # print(num_right, b)
                    # print('mmmmmmm:',a)
                    a = replace_n(a, ')', b, num_left)
                    a = a.replace('('+b, '', 1)
                    break
    return a


def add_seg(a):
    a = re.sub(u"[\u4e00-\u9fa5]+", '*', a) 
    a = re.sub(r'[a-zA-Z]+', '*', a)   
    a = a.replace('(* *)', 'W')  
    a = re.sub(r'[^0-9A-Za-z]+', '', a)  
    return a


def format_conversion_tree2prosody(data_path):

    line_sen_list = []

    with open(data_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            sen_token_list = []
            
            if line != '\n' and line != '':
              
                ss = line
                sss = remove_top(ss)
                sss = replace1(sss)
                sen_token_list.append(sss)

                ssss = add_seg(sss)
                sen_token_list.append('|'+ssss+'\n')
                line_sen_list.append(''.join(sen_token_list))
        f.close()
    
    with open(data_path,'w+', encoding='utf-8') as o:
      o.write(''.join(line_sen_list))
      o.close()


################################################################################################################

def replace(data_path):
    '''
    sen_list output: ['102011202110210203121102113', '0102121010301110103', '011210212013', '121311210211311102113', '1103110213']
    '''
    sen_list = []
    s00_list = []
    s0_list = []
    with open(data_path, 'r', encoding='utf-8') as t:
        lines = t.readlines()
        num0 = 0
        for line in lines:
            seg = line.split('|')

            s00 = seg[0]
            
            s0 = seg[1]
           
            s = re.sub('\n', '', s0)

           
            compileX = re.compile(r'\d+')
            num_result = compileX.findall(s)
            for i in num_result:
                s = re.sub(i, max(i), s, 1)

            s = re.sub('W', '0', s)
            s = re.sub('01', '1', s)
            s = re.sub('02', '2', s)
            s = re.sub('03', '3', s)
            
            sen_list.append(s)
            s00_list.append(s00)
            s0_list.append(s0)
        t.close()
    return sen_list, s00_list, s0_list



def score(TP, FP, FN):
    if TP + FP == 0:
        precision = 0.01
    else:
        precision = TP / (TP + FP)
    if TP + FN == 0:
        recall = 0.01
    else:
        recall = TP / (TP + FN)
    f1score = 2 * precision * recall / (precision + recall)
    return precision, recall, f1score

def count(gold_path, predicted_path):

    format_conversion_tree2prosody(gold_path)
    format_conversion_tree2prosody(predicted_path)

    test_sen_list ,test_s00_list, test_s0_list = replace(gold_path)
    predicted_sen_list , predicted_s00_list, predicted_s0_list = replace(predicted_path)

    # a12: test 1, predicted 2
    a00 = a01 = a02 = a03 = a10 = a11 = a12 = a13 = a20 = a21 = a22 = a23 = a30 = a31 = a32 = a33 = 0
    num = 0
    num_match_sen = 0
    for i in range(len(test_sen_list)):
        t = test_sen_list[i]
        p = predicted_sen_list[i]

        if t == p:
            num_match_sen += 1

        
        if len(t) != len(p):
            num += 1
            print(num, '\n', t, test_s00_list[i], test_s0_list[i], '\n', p ,predicted_s00_list[i], predicted_s0_list[i])
        else:
            for j in range(len(t)):
                if t[j] == '0':
                    if p[j] == '0':
                        a00 += 1
                    if p[j] == '1':
                        a01 += 1
                    if p[j] == '2':
                        a02 += 1
                    if p[j] == '3':
                        a03 += 1
                if t[j] == '1':
                    if p[j] == '0':
                        a10 += 1
                    if p[j] == '1':
                        a11 += 1
                    if p[j] == '2':
                        a12 += 1
                    if p[j] == '3':
                        a13 += 1
                if t[j] == '2':
                    if p[j] == '0':
                        a20 += 1
                    if p[j] == '1':
                        a21 += 1
                    if p[j] == '2':
                        a22 += 1
                    if p[j] == '3':
                        a23 += 1
                if t[j] == '3':
                    if p[j] == '0':
                        a30 += 1
                    if p[j] == '1':
                        a31 += 1
                    if p[j] == '2':
                        a32 += 1
                    if p[j] == '3':
                        a33 += 1
   
    precision1, recall1, fscore1 = score(a11 + a12 + a13 + a21 + a22 + a23 + a31 + a32 + a33, a01 , a10 + a20 + a30) 
    precision2, recall2, fscore2 = score(a22 + a23 + a32 + a33, a02 + a03 + a12 + a13, a20 + a21 + a30 + a31) 
    precision3, recall3, fscore3 = score(a33, a03 + a13 + a23, a30 + a31 + a32)
    precision = float((precision1 + precision2 + precision3) *100 /3 )
    recall = float((recall1 + recall2 + recall3) *100 /3 )
    fscore = float((fscore1 + fscore2 + fscore3) *100 /3 )


    completematch = float(100 * num_match_sen/len(test_sen_list))

    print('PW:',precision1, recall1, fscore1)
    print('PPH:',precision2, recall2, fscore2)
    print('IPH:',precision3, recall3, fscore3)


    return recall, precision, fscore, completematch

