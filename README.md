# SpanPSP
This repository contains code accompanying the paper **"A CHARACTER-LEVEL SPAN-BASED MODEL FOR MANDARIN PROSODIC STRUCTURE PREDICTION"** published on ICASSP 2022.

##  [TTS Samples](https://thuhcsi.github.io/SpanPSP/) | [Paper](https://arxiv.org/abs/2203.16922)

## Environment
* Python 3.7 or higher.
* Pytorch 1.6.0, or any compatible version.
* NLTK 3.2, torch-struct 0.4, transformers 4.3.0, or compatible.
* pytokenizations 0.7.2 or compatible.

## Repository structure
```
SpanPSP
├──bert-base-chinese
|   ├──config.json
|   ├──pytorch_model.bin
|   └──vocab.txt
├──data
|   ├──train
|   |   ├──raw_data
|   |   |   └──raw_data.txt
|   |   └──tree_data
|   |       ├──tree_train.txt
|   |       ├──tree_validate.txt
|   |       └──tree_test.txt
|   └──inference
|       ├──raw_data
|       |   └──raw_data.txt
|       ├──tree_data
|           └──tree_data.txt
├──models
|   ├──pretrained_model
|   |   └──pretrained_SpanPSP_Databaker.pt
|   └──yours
├──src
|   ├──benepar
|       ├── ...
|   ├──count_fscore.py
|   ├──evaluate.py
|   ├──export.py
|   ├──inference_seq2tree.py
|   ├──learning_rate.py
|   ├──main.py
|   ├──seq_with_label.py
|   ├──train_raw2tree.py
|   ├──transliterate.py
|   ├──treebank.py
├──README.md
```

## Download pretrained model
You can download the pre-trained models from the link below and put them in the right place as shown in the repository structure.
* ### bert-base-chinese
> Link: https://huggingface.co/bert-base-chinese
* ### SpanPSP_Databaker，SpanPSP_PeopleDaily
> Link: https://pan.baidu.com/s/1bwwFbyP1WoEr3fLbbGeXpQ

> Password: 9r2h


## Training and test with your dataset
### Data preprocessing
First prepare your own dataset into the following format, and put it (__*raw_data.txt*__) in the right place as shown in the above repository structure.
> 猴子#2用#1尾巴#2荡秋千#3。

Then use the following command to convert the data of the above raw file from sequence format to tree format, and devide it into training, validation, and test with the ratio of 8:1:1.
```
$ python src/train_raw2tree.py
```
After that, you can get the __*tree_train.txt*__, __*tree_validate.txt*__ and __*tree_test.txt*__. 
### Training
Train your model using:
```
$ python src/main.py  train  --train-path [your_training_data_path]  --dev-path [your_dev_data_path]  --model-path-base [your_saving_model_path] 
```
For example:
```
$ python src/main.py  train  --train-path data/train/tree_data/tree_train.txt  --dev-path data/train/tree_data/tree_validate.txt  --model-path-base models/my_model 
```
### Test
Test your model using:
```
$ python src/main.py  test  --model-path [your_trained_model_path]  --test-path [your_test_data_path]
```
For example:
```
$ python src/main.py  test  --model-path models/my_model.pt  --test-path data/train/tree_data/tree_test.txt
```
## Inference
### Data preprocessing
First prepare your own dataset into the following format, and put it (__*raw_data.txt*__) in the right place as shown in the repository structure.
> 猴子用尾巴荡秋千。

Then use the following command to convert the dataset from sequence format to tree format:
```
$ python src/inference_seq2tree.py
```
After that, you can get the __*tree_data.txt*__. 
### inference
Inference with your data using:
```
$ python src/main.py  inference  --model-path [your_pretrained_model_path]  --test-path [your_test_data_path]  --output-path [your_output_data_path]
```
For example:
```
$ python src/main.py  inference  --model-path models/pretrained_model/pretrained_SpanPSP_Databaker.pt  --test-path data/inference/tree_data/tree_data.txt  --output-path data/inference/output_data.txt
```
