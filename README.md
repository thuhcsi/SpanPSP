# SpanPSP
This repository contains code accompanying the paper **"A CHARACTER-LEVEL SPAN-BASED MODEL FOR MANDARIN PROSODIC STRUCTURE PREDICTION"** which is submitted to ICASSP 2022.

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
|   |   |   ├──raw_train.txt
|   |   |   ├──raw_validate.txt
|   |   |   └──raw_test.txt
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
|   |   └──pretrained_SpanPSP.pt
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
|   ├──train_seq2tree.py
|   ├──transliterate.py
|   ├──treebank.py
├──README.md
```


## Training and test with your dataset
### Data preprocessing
First prepare your own dataset into the following format, and divide it into training, validation and test named __*raw_train.txt*__, __*raw_validate.txt*__ and __*raw_test.txt*__ respectively.
Put them in the right place as shown in the above repository structure.
> 猴子#2用#1尾巴#2荡秋千#3。

Then use the following command to convert the data of the three above files from sequence format to tree format by changing the file path in the code respectively.
After that, you can get the __*tree_train.txt*__, __*tree_validate.txt*__ and __*tree_test.txt*__. 
```
$ python src/train_seq2tree.py
```
### Training
Train your model using:
```
$ python src/main.py  train  --train-path [your_training_data_path]  --dev-path [your_dev_data_path]  --model-path-base [your_saving_model_path] 
```
### Test
Test your model using:
```
$ python src/main.py  test  --model-path [your_trained_model_path]  --test-path [your_test_data_path]
```
## Using the pretrained model to automatically label the prosody structure of text data
### Data preprocessing
First prepare your own dataset into the following format, and put it in the right place as shown in the repository structure.
> 猴子用尾巴荡秋千。

Then use the following command to convert the dataset from sequence format to tree format:
```
$ python src/inference_seq2tree.py
```
### Download the pretrained model
The pretrained model will be released soon.
### Automatic labeling
```
$ python src/main.py  auto_labels  --model-path [your_pretrained_model_path]  --test-path [your_test_data_path]  --output-path [your_output_data_path]
```
