# 使用Word2Vec在中文wiki上进行训练
## 1 下载中文wiki语料
下载地址：https://dumps.wikimedia.org/zhwiki/latest/
从此处可以下载最新的中文wiki原始数据。目前（2017-9-26）可以下载到的是一个1.47G的压缩文件。文件名为zhwiki-latest-pages-articles.xml.bz2。不需要解压，里边是网页标签形式的数据，我们需要进行抽取有效的内容。
## 2 使用Wikipedia Extractor抽取内容
使用Git进行下载源码并安装

```
$ git clone https://github.com/attardi/wikiextractor.git wikiextractor
$ cd wikiextractor
$ sudo Python setup.py install
$ ./WikiExtractor.py -b 1024M -o extracted zhwiki-latest-pages-articles.xml.bz2
```
参数-b 1024M表示以1024M为单位切分文件，默认是1M。由于最后生成的正文文本约1.17G，把参数设置的大一些可以保证最后的抽取结果全部存在一个文件里。这里我们设为1024M，可以分成一个1.07G的大文件和一个92.2M的小文件，后续的步骤可以先在小文件上实验，再应用到大文件上。
在我的机器上（macOS 1.7GHz 4G）最终的结果是：
> INFO: Finished 3-process extraction of 963027 articles in 4298.3s (224.0 art/s)

这里，我们得到了2个文本文件：wiki_00, wiki_01。大小分别为：1.07G, 92.2M。
## 3 繁体转简体
维基百科的中文数据是繁简混杂的，里面包含大陆简体、台湾繁体、港澳繁体等多种不同的数据。有时候在一篇文章的不同段落间也会使用不同的繁简字。
为了处理方便起见，我们直接使用了开源项目opencc。参照安装说明的方法，安装完成之后，使用下面的命令进行繁简转换，整个过程也很快：

```
$ sudo apt-get install opencc
$ opencc -i wiki_00 -o zh_wiki_00 -c t2s.json
$ opencc -i wiki_01 -o zh_wiki_01 -c t2s.json
```
## 4 符号处理
由于Wikipedia Extractor抽取正文时，会将有特殊标记的外文直接剔除。我们最后再将「」『』这些符号替换成引号，顺便删除空括号，额外的HTML标签和空白行，以及非中文、英文和数字的其他字符（如：韩语，日语，等。对分词以及分类没有太多帮助的字符）就大功告成了！代码如下：

```
#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import sys
import codecs

def myfun(input_file):
    p1 = re.compile('-\{.*?(zh-hans|zh-cn):([^;]*?)(;.*?)?\}-')
    p2 = re.compile('[（\(][，；。？！\s]*[）\)]')
    p3 = re.compile('[「『]')
    p4 = re.compile('[」』]')
    p5 = re.compile('</?\w+[^>]*>')
    p6 = re.compile('^\s+$')
    p7 = re.compile('[^\u4e00-\u9fa5 \n\rA-Za-z0-9_。？！，、；：“”‘’（）【】——《》]')
    outfile = codecs.open('std_' + input_file, 'w', 'utf-8')
    with codecs.open(input_file, 'r', 'utf-8') as myfile:
        for line in myfile:
            line = p1.sub('\2', line)
            line = p2.sub('', line)
            line = p3.sub('“', line)
            line = p4.sub('”', line)
            line = p5.sub('', line)
            line = p6.sub('', line)
            line = p7.sub('', line)
            outfile.write(line)
    outfile.close()
if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: Python script.py inputfile")
        sys.exit()
    input_file = sys.argv[1]
    myfun(input_file)
```
将上述代码保存到exec.py文件，并将该文件放到与数据文件相同的目录，执行命令：

```
$ python exec.py zh_wiki_00
$ python exec.py zh_wiki_01
```
这里，我们又得到2个格式化文件：std_zh_wiki_00，std_zh_wiki_01。大小分别为：968.5M，81.8M。大小比之前的文件要小，因为修改删除了文件中的符号。
> 注：有些语料可能还需要进一步进行编码转换的处理。统一将编码转换为UTF-8编码，方便下一步分词处理。具体转换方法如下：
`$ iconv -c -t UTF-8 zh_wiki_01 > utf8_zh_wiki_01`

## 5 语料数据合并
通过程序merge.py进行合并，其使用方法如下：
`$ python merge.py [-h] [-fs FILES [FILES ...]] [-o [OUTPUT]] > outputsplitpoint`
-h --help：显示使用说明；
-fs --files：要合并的文件列表；
-o --output：输出的语料数据文件；
outputsplitpoint：输出原样分割点数据到该文件，若未指定则输出到标准输出设备（屏幕）。
例如：
`$ Python merge.py -fs data/ltp_test data/ltp_train -o data/ltp_corpus > data/splitpoint`
## 6 中文分词
### 6.1 pyNLPIR分词
中文分词之前一直采用了中科院ICTCLAS的分词程序，其分词准确率高且识别的专业词汇较多。经过多年的发展更新，现在的ICTCLAS已经更新为pyNLPITR，可以直接在Python中调用。安装方式：
`$ pip install pynlpir --upgrade`
### 6.2 jieba（结巴）分词
目前在Python中比较好的一种分词工具。其使用比较简单，且分词效果不错。安装方式：
`$ pip install jieba --upgrade`
### 6.3 LTP平台
哈工大社会计算与信息检索研究中心（HITSCIR）推出的自然语言处理平台pyltp。可以进行分词、词性标注、命名实体识别、依存句法分析等。安装方式：
`$ pip install pyltp --upgrade`
安装完成后，还需要下载对应版本的pyltp模型。其下载地址是：[百度云](http://pan.baidu.com/share/link?shareid=1988562907&uk=2738088569)。这里需要注意pyltp和资源模型的版本对应关系。目前使用的是pyltp(0.1.9.1)和模型（3.4.0）
### 6.4 调用分词工具进行分词
使用tokenizer.py进行分词。其使用方法如下：
`$ python tokenizer.py [-h] [-s SEGMENTER] [-l] [-p] < inputdatafile > outputdatafile`
-h --help：显示使用说明；
-s --segmenter：选取分词器。目前实现了jieba、PyNLPIR和pyltp三种分词器分词，默认是pyltp；
-l --labeled：原始语料中行首是否包含类别标签，默认为否；
-p --postagging：是否进行词性标注，默认为否；
inputdatafile：输入数据，通过重定向方式指定文件输入；
outputdatafile：输出结果到该文件，若未指定则输出到标准输出设备（屏幕）。
例如：
`$ python tokenizer.py -s jieba -l -p > data/ltp_seg`
> 注：
> tokenizer.py程序需要读取对应的tokenizer.cfg配置文件进行分词器的选择和分词特征的选择。
> 典型的tokenizer.cfg配置文件如下：
> 
```
{
    "jieba": {
        "utilname": "jiebautil", 
        "classname": "JiebaSegmenter"
    }, 
    "pynlpir": {
        "utilname": "pynlpirutil", 
        "classname": "PyNLPIRSegmenter"
    }, 
    "pyltp": {
        "utilname": "pyltputil", 
        "classname": "PyltpSegmenter"
    }
}
```

## 7 其他句法分析功能
依托于HITSCIR的LTP平台pyltp，我们可以完成命名实体识别（NERecognize）依存句法分析（Parser）等功能。
### 7.1 命名实体识别
通过程序来调用pyltp中命名实体识别功能：
`$ python nerecognizer.py < inputdatafile > outputdatafile`
inputdatafile：输入数据，通过重定向方式指定文件输入；
outputdatafile：输出结果到该文件，若未指定则输出到标准输出设备（屏幕）。
> 注：
> 命名实体识别需要首先经过分词和词性标注。因此输入数据必须要有此两项特征。另外，也可以使用jieba或者PyNLPIR作为分词器与词性标注器。

### 7.2 依存句法分析
通过程序来调用pyltp中依存句法分析功能：
`$ Python parser.py < inputdatafile > outputdatafile`
inputdatafile：输入数据，通过重定向方式指定文件输入；
outputdatafile：输出结果到该文件，若未指定则输出到标准输出设备（屏幕）。
> 注：
> 依存句法分析也需要首先经过分词和词性标注。因此输入数据必须要有此两项特征。另外，也可以使用jieba或者PyNLPIR作为分词器与词性标注器。
> 
-------
> **Tips：由于分词、词性标注、命名实体识别与依存句法分析模块的数据输入与输出均采用了重定向方式，因此可以利用管线命令（|）来依次递进完成各个功能。如：**
> `$ python tokenizer.py -s pyltp -l -p < data/ltp_corpus | python nerecognizer.py | python parser.py > data/ltp_seg`
> **就完成了利用pyltp在有类别标签的数据上进行分词、词性标注、命名实体识别与依存句法分析，并将结果保存到data/ltp_seg文件中。**

## 8 安装LibSVM和Liblinear[SVM分类使用]
直接采用HomeBrew进行安装即可。

```
$ brew install libsvm
$ brew install liblinear
```
安装完成后即可使用LibSVM中的svm-train、svm-predict和svm-scale三个程序以及Liblinear中的train和predict程序。
> 注：
1. LibSVM和Liblinear的数据格式为：
`<label> <index1>:<value1> <index2>:<value2> ...`
一行一条数据，以回车符换行（\n）。在分类情况下，label可以是一个整数，支持多分类。在回归情况下，label作为目标值可以是任意实数。一对`<index>:<value>`作为一个特征，多个特征用空格分割。特征键（index）为从1开始的整数，特征值（value）为实数。只有在precomputed kernel中特征键从0开始（Liblinear中的特征键从1开始）。**需要【特别注意】的是，特征键必须从【小到大升序排列】，特征值为0的特征可以省略不写。**测试集中的特征键作为预测结果是否正确的判断，如果没有可以填充任意整数。
2. svm-train的参数及格式：
`svm-train [options] training_set_file [model_file]
options:
-t kernel_type : set type of kernel function (default 2)
* 0 -- linear: u'\*v
* 2 -- radial basis function: exp(-gamma\*|u-v|^2)
-v n: n-fold cross validation mode`
3. svm-predict的参数及格式：
`Usage: svm-predict [options] test_file model_file output_file`
4. train的参数及格式：
`train [options] training_set_file [model_file]`
5. predict的参数及格式：
`predict [options] test_file model_file output_file`

## 9 语料数据预处理
### 9.1 特征抽取
经过浅层句法分析后，源语料数据将被处理成为json形式的数据，其格式如下所示：
> 
```
{"label": "DES_ABBR", "words": [{"term": "ACLU", "pos": "ws", "ne": "O", "head": 3, "rel": "ATT"}, {"term": "\u7684", "pos": "u", "ne": "O", "head": 1, "rel": "RAD"}, {"term": "\u5168\u79f0", "pos": "n", "ne": "O", "head": 4, "rel": "SBV"}, {"term": "\u662f", "pos": "v", "ne": "O", "head": 0, "rel": "HED"}, {"term": "\u4ec0\u4e48", "pos": "r", "ne": "O", "head": 4, "rel": "VOB"}]}
```

该数据是语料中一条问题所形成的json格式数据。其主要包含两个字典项：label和words。
label是指该问题的类别标签；
words是由该问题中每一个词的所有句法特征所构成的列表。包含：
> term：词项；
pos：词性；
ne：命名实体标记；
head：核心词；
rel：依存关系。

接下来进行特征抽取。首先通过features.cfg文件来编写特征模版。典型的features.cfg文件内容如下：

```
{
  "baseline":
  {
    "bow": "term",
    "pos": "pos",
    "ne": "ne"
  },
  "b+q+r":
  {
    "bow": "term",
    "pos": "pos",
    "ne": "ne",
    "qw": "@get_qw",
    "rel": "@get_rel"
  }
}

```
该文件通过json格式编码，主要包含模版名称，如baseline、b+q+r。以及模版中各特征对应数据文件中的特征名称。如词袋特征（bow）对应数据文件中的term等。基本特征可以采取直接对应方式。复杂特征无法直接对应，因此在特征模版配置文件中使用@fun_name的方式进行编写。另外要在**cplxfeature.py文件中进行对应的实现**。具体实现方式可以参见该文件。
特征抽取采用程序：
`$ python extfeatures.py [-h] [-f FEATURES] < inputdatafile > outputdatafile`
-h --help：显示使用说明；
-f --features：从特征模版配置文件中选取一种特征模版，默认采用baseline；
inputdatafile：输入数据，通过重定向方式指定文件输入；
outputdatafile：输出结果到该文件，若未指定则输出到标准输出设备（屏幕）。
例如：
`$ Python extfeatures.py -f baseline < data/ltp_seg > data/ltp_baseline`
经过采用baseline方式特征抽取后的数据格式如下：
> 
```
{"label": "DES_ABBR", "bow": ["ACLU", "\u7684", "\u5168\u79f0", "\u662f", "\u4ec0\u4e48"], "pos": ["ws", "u", "n", "v", "r"], "ne": ["O", "O", "O", "O", "O"]}
```

经过采用b+q+r（baseline+疑问词+疑问相关词）方式特征抽取后数据格式如下：
> 
```
{"label": "DES_MEANING", "bow": ["IT", "\u662f", "\u4ec0\u4e48", "\u610f\u601d"], "pos": ["ws", "v", "r", "n"], "ne": ["O", "O", "O", "O"], "qw": ["\u4ec0\u4e48"], "rel": ["\u610f\u601d"]}
```

## 10 特征编码
### 10.1 WordSet Encoding（词集编码）
采用词集（WordSet）方式编码的核心思想就是通过将同一种特征列表转换为集合，从而去除同一种特征中重复为某一个特征项进行编码（SVM要求特征不能重复）。然后将不同种特征进行向量拼接从而形成一个特征向量。
通过程序来完成特征编码：
`$ python wordset_encoding.py [-h] [-t] [-f FEATURES] [-o] < inputdatafile > outputdatafile`
-h --help：显示使用说明；
-t --taxonomy：采用大类分类还是小类分类，默认false（小类）；
-f --features：从特征模版配置文件中选取一种特征模版，默认采用baseline；
-o --output：是否输出各个特征辞典文件，默认false；
inputdatafile：输入数据，通过重定向方式指定文件输入；
outputdatafile：输出结果到该文件，若未指定则输出到标准输出设备（屏幕）。
例如：
`$ python wordset_encoding.py -f baseline -o < data/ltp_baseline > data/ltp_baseline_vec`
通过特征编码后得到的特征向量形式如下：
> 1 178:1 909:1 1254:1 4307:1 5777:1 8310:1 8323:1 8333:1 8334:1 8335:1 8337:1 
> 
-------
> 注：
> 在指定-o参数后，该程序会在data目录中生成label.vocab和各个特征名.vocab的字典文件。每一个字典文件中都包含3列，分别是 item index freq。

### 10.2 One-Hot Encoding
<TODO:>
### 10.3 Word2Vec Encoding
<TODO:>
## 11 数据分割（针对SVM进行预测需要）
在SVM分类器中需要训练集和测试集，由于我们之前对语料数据进行统一处理将training set和testing set进行了合并（merged）因此，此处需要再对合并后的数据集分割。分割的标准目前实现了按原顺序分割（seq）、按原规模随机分割（ran）以及按类别标签分割（tag）**按标签分割要求数据集本身含有标签**。分割点信息在合并时已保存至split point文件中。因此要读取该文件信息。分割后产生已数字顺序结尾的数据集文件。其顺序含义参考合并时的顺序。
通过程序来完成分割：
`$ python split.py [-h] [-f FILE] [-sp SPLITPOINT] [-s {seq,ran,tag}]`
-h --help：显示使用说明；
-f --file：将要被分割文件；
-sp --splitpoint：分割点文件；
-s --sequence：分割方式，可选seq, ran, tag。默认：seq。
例如：
`$ Python split.py -f data/baseline_fine_vec -sp data/splitpoint -s seq`
## 12 使用LibSVM进行分类
主要流程为：
1. 语料数据预处理（合并） -> merge.py
2. 分词 -> tokenizer.py；句法分析 -> nerecognizer.py -> parser.py
3. 特征抽取 -> extfeatures.py
4. 特征编码 -> wordset_encoding.py
5. 分割数据 -> split.py
6. 训练模型 -> svm_train(train)
7. 预测 -> svm_perdict(perdict)
> 以下提供一个完整流程的示例：
> 
```
$ python merge.py -fs data/test data/train -o data/corpora > data/splitpoint
$ python tokenizer.py -s pyltp -l -p < data/corpora | python nerecognizer.py | python parser.py > data/seg
$ python extfeatures.py -f baseline < data/seg > data/baseline
$ python wordset_encoding.py -f baseline < data/baseline > data/baseline_fine_vec
$ python wordset_encoding.py -t -f baseline < data/baseline > data/baseline_coarse_vec
$ python split.py -f data/baseline_fine_vec -sp data/splitpoint -s seq
$ python split.py -f data/baseline_coarse_vec -sp data/splitpoint -s seq
$ svm-train -t 0 data/baseline_fine_vec_2 data/baseline_fine_model
$ svm-train -t 0 data/baseline_coarse_vec_2 data/baseline_coarse_model
$ svm-predict data/baseline_fine_vec_1 data/baseline_fine_model data/baseline_fine_result
$ svm-train -t 0 -v 10 data/baseline_fine_vec
```
> 在使用LTP语料情况下(train|test/4966|1300)，仅使用baseline特征(bow+pos+ne)的小类分类精度为：**74% (962/1300) (classification)**。其大类分类精度为**87.9231% (1143/1300) (classification)**。用全体数据进行10倍交叉验证其小类精度为**77.8168%**。大类精度为**89.5787%**。
在使用了性能和准确性更好的Liblinear进行训练预测，过程如下：
>
```
$ train data/baseline_fine_vec_2 data/baseline_fine_line_model
$ train data/baseline_coarse_vec_2 data/baseline_coarse_line_model
$ predict data/baseline_fine_vec_1 data/baseline_fine_line_model data/baseline_fine_line_result
$ predict data/baseline_coarse_vec_1 data/baseline_coarse_line_model data/baseline_coarse_line_result
$ train -v 10 data/baseline_fine_vec
$ train -v 10 data/baseline_coarse_vec
```
> 同样仅使用baseline特征(bow+pos+ne)的小类分类精度为：**78.3077% (1018/1300)**。其大类分类精度为**89% (1157/1300)**。用全体数据进行10倍交叉验证其小类精度为**81.5991%**。大类精度为**90.4883%**。
> 为了方便使用各个模块进行预测分析。还提供了*.sh的脚本文件来进行批量处理。
> 分别是：
> preprocessing.sh  对数据进行合并，分词，词性标注，命名实体识别。生成对应的seg和splitpoint文件
> extfeatures.sh    根据指定的特征进行特征提取，生成指定特征的数据文件
> encoding.sh   根据需要进行编码，并分割为训练集和测试集。
> svm.sh    进行训练和预测。
> funqa.sh  调用上述各个脚本。根据features.in文件的内容或者指定特征以及特征文件名的方式进行批处理。


## 13 LSTM



