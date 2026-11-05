# Report 034 — Phase-5 corpus source verification

Generated: 2026-11-02 18:47:15

## Summary table

| cat | dataset (config) | exists | gated | loadable | method | license | size | fields |
|---|---|---|---|---|---|---|---|---|
| long_text | `0xDing/wikipedia-cn-20230720-filtered` | True | False | YES | single-file:wikipedia-cn-20230720-filtered.json | cc-by-sa-3.0 | ['100K<n<1M'] 524.5MB files | completion, source |
| long_text | `pleisto/wikipedia-cn-20230720-filtered` | True | False | YES | single-file:wikipedia-cn-20230720-filtered.json | cc-by-sa-3.0 | ['100K<n<1M'] 524.5MB files | source, completion |
| long_text | `wikimedia/wikipedia` (20231101.zh) | True | False | YES | streaming | cc-by-sa-3.0,gfdl | train=6152 ['n<1K', '1K<n<10K', '10K<n<100K', '100K<n<1M', '1M<n<10M'] 71792.0MB files | id, url, title, text |
| long_text | `wdndev/webnovel-chinese` | True | False | YES | single-file:example.jsonl | apache-2.0 | ['1B<n<10B'] 39005.7MB files | title, chapter, text |
| long_text | `wangrui6/Zhihu-KOL` | True | False | YES | streaming | (none in card) | train=1006218 1501.2MB files | INSTRUCTION, RESPONSE, SOURCE, METADATA |
| long_text | `BAAI/CCI3-HQ` | True | auto | no | - | (none in card) | train=None 517919.6MB files | - |
| mrc | `hfl/cmrc2018` | True | False | YES | streaming | cc-by-sa-4.0 | train=10142;validation=3219;test=1002 ['10K<n<100K'] 4.9MB files | id, context, question, answers |
| mrc | `cmrc2018` | True | False | YES | streaming | cc-by-sa-4.0 | train=10142;validation=3219;test=1002 ['10K<n<100K'] 4.9MB files | id, context, question, answers |
| mrc | `clue` (cmrc2018) | True | False | YES | streaming | unknown | test=3861;train=34334;validation=4316 ['100K<n<1M'] 298.2MB files | id, context, question, answers |
| mrc | `clue` (drcd) | True | False | YES | streaming | unknown | test=3861;train=34334;validation=4316 ['100K<n<1M'] 298.2MB files | id, context, question, answers |
| mrc | `clue` (c3) | True | False | YES | streaming | unknown | test=3861;train=34334;validation=4316 ['100K<n<1M'] 298.2MB files | id, context, question, choice, answer |
| mrc | `PaddlePaddle/dureader_robust` | True | False | YES | parquet-convert:plain_text/train/0000.parquet | apache-2.0 | 0.0MB files | id, title, context, question, answers |
| mrc | `luozhouyang/dureader` | True | False | YES | parquet-convert:checklist/train/0000.parquet | (none in card) | 41.1MB files | id, title, context, question, is_impossible, answers, type |
| kdialog | `thu-coai/kdconv` | True | False | YES | streaming | apache-2.0 | 47.3MB files | messages, name |
| kdialog | `PaddlePaddle/duconv` | True | False | YES | streaming | apache-2.0 | 0.0MB files | id, goal, knowledge, conversation, history, response |
| instruct | `BelleGroup/train_1M_CN` | True | False | YES | single-file:Belle_open_source_1M.json | gpl-3.0 | ['100K<n<1M'] 457.7MB files | instruction, input, output |
| instruct | `silk-road/alpaca-data-gpt4-chinese` | True | False | YES | single-file:Alpaca_data_gpt4_zh.jsonl | apache-2.0 | ['10K<n<100K'] 78.4MB files | instruction_zh, input_zh, output_zh, instruction, input, output |
| kdialog | `xywang1/NaturalConv` | True | False | YES | parquet-convert:default/train/0000.parquet | other | ['10K<n<100K'] 52.6MB files | dialog_id, document_id, content |
| kdialog | `thu-coai/kd_conv_with_kb` | True | False | YES | streaming | apache-2.0 | train=1200;test=150;validation=150 ['1K<n<10K'] 10.2MB files | messages, name, domain |
| kdialog | `justhangingoutguy/NaturalConversations-36k` | True | False | YES | streaming | (none in card) | ['10K<n<100K'] 40.8MB files | messages |
| kdialog | `VITA-MLLM/Emotion_NaturalConv_FunctionCall` | True | False | no | - | (none in card) | 1982.6MB files | - |
| kdialog | `Fair-HV/NaturalConversations-36k` | True | False | YES | streaming | (none in card) | ['10K<n<100K'] 40.8MB files | messages |
| instruct | `m-a-p/COIG-CQIA` | True | False | YES | parquet-convert:chinese_traditional/train/0000.parquet | (none in card) | ['10K<n<100K'] 299.2MB files | instruction, input, output, task_type, domain, metadata, answer_from, human_verified, copyright |
| instruct | `YeungNLP/firefly-train-1.1M` | True | False | YES | streaming | (none in card) | 1171.2MB files | kind, input, target |
| instruct | `BAAI/COIG` | True | False | YES | streaming | apache-2.0 | 338.2MB files | instruction, conversations |
| instruct | `cver91/liu-software-firefly-data` | True | manual | no | - | (none in card) | 39990.0MB files | - |
| instruct | `BAAI/COIG-PC` | True | auto | no | - | unknown | full=321332879;train=208529583;valid=2087767;test=8094740;Top50PerTask=63643;Top100PerTask=127158;Top200PerTask=253558 126915.7MB files | - |
| instruct | `m-a-p/COIG-Kun` | True | False | YES | streaming | (none in card) | ['100K<n<1M'] 573.4MB files | instruction, output, Academic/Professional Field, Industry Category, Text type |

## Details

### `0xDing/wikipedia-cn-20230720-filtered`  [long_text]

- exists: True  gated: False  downloads: 4770  license: cc-by-sa-3.0 
- size: ['100K<n<1M'] 524.5MB files  loading script: False
- files (first 25): `.gitattributes (2379), README.md (1356), wikipedia-cn-20230720-filtered.json (524489333)`
- **loadable** via `single-file:wikipedia-cn-20230720-filtered.json` split=`train`
- structure:
```json
{
 "completion": "str",
 "source": "str"
}
```
- sample (record 0, ≤120 chars/field):
  - `completion`: 昭通机场（ZPZT）是位于中国云南昭通的民用机场，始建于1935年，1960年3月开通往返航班“昆明－昭通”，原来属军民合用机场。1986年机场停止使用。1991年11月扩建，于1994年2月恢复通航。是西南地区「文明机场」，通航城市...
  - `source`: wikipedia.zh2307
- elapsed: 56.2s

### `pleisto/wikipedia-cn-20230720-filtered`  [long_text]

- exists: True  gated: False  downloads: 4770  license: cc-by-sa-3.0 
- size: ['100K<n<1M'] 524.5MB files  loading script: False
- files (first 25): `.gitattributes (2379), README.md (1356), wikipedia-cn-20230720-filtered.json (524489333)`
- **loadable** via `single-file:wikipedia-cn-20230720-filtered.json` split=`train`
- structure:
```json
{
 "source": "str",
 "completion": "str"
}
```
- sample (record 0, ≤120 chars/field):
  - `source`: wikipedia.zh2307
  - `completion`: 昭通机场（ZPZT）是位于中国云南昭通的民用机场，始建于1935年，1960年3月开通往返航班“昆明－昭通”，原来属军民合用机场。1986年机场停止使用。1991年11月扩建，于1994年2月恢复通航。是西南地区「文明机场」，通航城市...
- elapsed: 73.8s

### `wikimedia/wikipedia` / config `20231101.zh`  [long_text]

- exists: True  gated: False  downloads: 297602  license: cc-by-sa-3.0,gfdl 
- size: train=6152 ['n<1K', '1K<n<10K', '10K<n<100K', '100K<n<1M', '1M<n<10M'] 71792.0MB files  loading script: False
- configs in card: ['20231101.ab', '20231101.ace', '20231101.ady', '20231101.af', '20231101.als', '20231101.alt', '20231101.am', '20231101.ami', '20231101.an', '20231101.ang', '20231101.anp', '20231101.ar', '20231101.arc', '20231101.ary', '20231101.arz', '20231101.as', '20231101.ast', '20231101.atj', '20231101.av', '20231101.avk']
- card splits: `[{"config": "20231101.ab", "splits": {"train": 6152}, "dataset_size": 4334455}, {"config": "20231101.ace", "splits": {"train": 13003}, "dataset_size": 5065801}, {"config": "20231101.ady", "splits": {"train": 706}, "dataset_size": 765030}, {"config": "20231101.af", "splits": {"train": 112518}, "dataset_size": 226672176}, {"config": "20231101.als", "splits": {"train": 30013}, "dataset_size": 81450196}, {"config": "20231101.alt", "splits": {"train": 1087}, "dataset_size": 6819963}, {"config": "20231101.am", "splits": {"train": 13906}, "dataset_size": 24218002}, {"config": "20231101.ami", "splits"`
- files (first 25): `.gitattributes (2307), 20231101.ab/train-00000-of-00001.parquet (1237796), 20231101.ace/train-00000-of-00001.parquet (1574258), 20231101.ady/train-00000-of-00001.parquet (347450), 20231101.af/train-00000-of-00001.parquet (124485544), 20231101.als/train-00000-of-00001.parquet (49452211), 20231101.alt/train-00000-of-00001.parquet (2910477), 20231101.am/train-00000-of-00001.parquet (10720027), 20231101.ami/train-00000-of-00001.parquet (2261859), 20231101.an/train-00000-of-00001.parquet (29573020), 20231101.ang/train-00000-of-00001.parquet (1789811), 20231101.anp/train-00000-of-00001.parquet (3355979), 20231101.ar/train-00000-of-00007.parquet (408241089), 20231101.ar/train-00001-of-00007.parquet`
- **loadable** via `streaming` split=`train`
- structure:
```json
{
 "id": "str",
 "url": "str",
 "title": "str",
 "text": "str"
}
```
- sample (record 0, ≤120 chars/field):
  - `id`: 13
  - `url`: https://zh.wikipedia.org/wiki/%E6%95%B0%E5%AD%A6
  - `title`: 数学
  - `text`: 数学，是研究數量、结构以及空间等概念及其变化的一門学科，屬於形式科學的一種。數學利用抽象化和邏輯推理，從計數、計算、量度、對物體形狀及運動的觀察發展而成。數學家們拓展這些概念，以公式化新的猜想，以及從選定的公理及定義出發，嚴謹地推導出...
- elapsed: 21.6s

### `wdndev/webnovel-chinese`  [long_text]

- exists: True  gated: False  downloads: 6858  license: apache-2.0 
- size: ['1B<n<10B'] 39005.7MB files  loading script: False
- files (first 25): `.gitattributes (2351), README.md (1002), data/webnovel_0.jsonl (4183415364), data/webnovel_1.jsonl (4198277512), data/webnovel_2.jsonl (4191247565), data/webnovel_3.jsonl (4191434074), data/webnovel_4.jsonl (4190892198), data/webnovel_5.jsonl (4187266263), data/webnovel_6.jsonl (4187251877), data/webnovel_7.jsonl (4206169131), data/webnovel_8.jsonl (4219093606), data/webnovel_9.jsonl (1234998491), example.jsonl (15667527)`
- **loadable** via `single-file:example.jsonl` split=`train`
- structure:
```json
{
 "title": "str",
 "chapter": "str",
 "text": "str"
}
```
- sample (record 0, ≤120 chars/field):
  - `title`: 斗破苍穹
  - `chapter`:  第一章 陨落的天才
  - `text`: “斗之力，三段！”\n望着测验魔石碑上面闪亮得甚至有些刺眼的五个大字，少年面无表情，唇角有着一抹自嘲，紧握的手掌，因为大力，而导致略微尖锐的指甲深深的刺进了掌心之中，带来一阵阵钻心的疼痛……\n“萧炎，斗之力，三段！级别：低级！”测验...
- elapsed: 8.3s

### `wangrui6/Zhihu-KOL`  [long_text]

- exists: True  gated: False  downloads: 1934  license: (none in card) 
- size: train=1006218 1501.2MB files  loading script: False
- card splits: `[{"config": null, "splits": {"train": 1006218}, "dataset_size": 2295601241}]`
- files (first 25): `.gitattributes (2265), README.md (571), data/train-00000-of-00005-a1278ede4e8c5cdb.parquet (306309311), data/train-00001-of-00005-1fc2da944397e9c2.parquet (303353725), data/train-00002-of-00005-68ced004a1458143.parquet (300499089), data/train-00003-of-00005-1dae36b67c12169f.parquet (291841874), data/train-00004-of-00005-c374cc9fbda9fda7.parquet (299200473)`
- **loadable** via `streaming` split=`train`
- structure:
```json
{
 "INSTRUCTION": "str",
 "RESPONSE": "str",
 "SOURCE": "str",
 "METADATA": "str"
}
```
- sample (record 0, ≤120 chars/field):
  - `INSTRUCTION`: 怎么说服男朋友买烤箱？
  - `RESPONSE`: emmmmm，首先想说的是，我买厨房用品一般是不用「说服」的，只是在厨房堆的满满当当的情况下会象征性的问一下我老公，他就会回答我说：你看看你还有地方放吗。然后我会思考一下，如果是特别想买的，就不会问他了。自己决定就好。 比如，前几天我...
  - `SOURCE`: Zhihu
  - `METADATA`: {"question_id": 357137111.0, "answer_id": 914332816.0, "url": "https://www.zhihu.com/question/357137111/answer/914332...
- elapsed: 57.2s

### `BAAI/CCI3-HQ`  [long_text]

- exists: True  gated: auto  downloads: 5453  license: (none in card) 
- size: train=None 517919.6MB files  loading script: True
- configs in card: ['default']
- card splits: `[{"config": null, "splits": {"train": null}, "dataset_size": null}]`
- files (first 25): `.gitattributes (41948), README.md (11606), README_zh.md (10993), data/part_000000.jsonl (1048862081), data/part_000001.jsonl (1056863005), data/part_000002.jsonl (1053618111), data/part_000003.jsonl (1027380329), data/part_000004.jsonl (1059223530), data/part_000005.jsonl (1057723949), data/part_000006.jsonl (1061737533), data/part_000007.jsonl (1037554877), data/part_000008.jsonl (1062791098), data/part_000009.jsonl (1059565016), data/part_000010.jsonl (1047292199), data/part_000011.jsonl (1063001839), data/part_000012.jsonl (1064931811), data/part_000013.jsonl (1033862110), data/part_000014.jsonl (1058117349), data/part_000015.jsonl (1063255523), data/part_000016.jsonl (1040855524), data/p`
- **NOT loadable**: `streaming: ConnectionError: Couldn't reach https://huggingface.co/datasets/BAAI/CCI3-HQ/resolve/d6f3aa30cebfef497e822ff968ed68a18bf90b8f/.huggingface.yaml (error 403) | parquet-convert: GatedRepoError: 403 Client Error. (Request ID: Root=1-6ae85817-55696feb10803fe03a13c551;b8d9ca63-7185-45b0-9b95-9f1d6e7dad0e)\n\nCannot access gated repo for url https://huggingface.co/datasets/BAAI/CCI3-HQ/resolve/refs%2Fconvert%2Fparquet/default/partial-train/0000.parquet.\nAccess to dataset BAAI/CCI3-HQ is re...`
- elapsed: 10.3s

### `hfl/cmrc2018`  [mrc]

- exists: True  gated: False  downloads: 2841  license: cc-by-sa-4.0 
- size: train=10142;validation=3219;test=1002 ['10K<n<100K'] 4.9MB files  loading script: False
- configs in card: ['default']
- card splits: `[{"config": null, "splits": {"train": 10142, "validation": 3219, "test": 1002}, "dataset_size": 22298754}]`
- files (first 25): `.gitattributes (1174), README.md (7851), data/test-00000-of-00001.parquet (394683), data/train-00000-of-00001.parquet (3365898), data/validation-00000-of-00001.parquet (1136115)`
- **loadable** via `streaming` split=`train`
- structure:
```json
{
 "id": "str",
 "context": "str",
 "question": "str",
 "answers": {
  "text": [
   "str",
   "len=1"
  ],
  "answer_start": [
   "int",
   "len=1"
  ]
 }
}
```
- sample (record 0, ≤120 chars/field):
  - `id`: TRAIN_186_QUERY_0
  - `context`: 范廷颂枢机（，），圣名保禄·若瑟（），是越南罗马天主教枢机。1963年被任为主教；1990年被擢升为天主教河内总教区宗座署理；1994年被擢升为总主教，同年年底被擢升为枢机；2009年2月离世。范廷颂于1919年6月15日在越南宁平省...
  - `question`: 范廷颂是什么时候被任为主教的？
  - `answers`: {"text": ["1963年"], "answer_start": [30]}
- context_keys: `["context"]`
- answer_start_keys: `["answers.answer_start"]`
- context_len: `{"n": 50, "min": 288, "max": 815, "median": 485.0, "mean": 505.2, "p10": 322, "p90": 815}`
- elapsed: 20.3s

### `cmrc2018`  [mrc]

- exists: True  gated: False  downloads: 2841  license: cc-by-sa-4.0 
- size: train=10142;validation=3219;test=1002 ['10K<n<100K'] 4.9MB files  loading script: False
- configs in card: ['default']
- card splits: `[{"config": null, "splits": {"train": 10142, "validation": 3219, "test": 1002}, "dataset_size": 22298754}]`
- files (first 25): `.gitattributes (1174), README.md (7851), data/test-00000-of-00001.parquet (394683), data/train-00000-of-00001.parquet (3365898), data/validation-00000-of-00001.parquet (1136115)`
- **loadable** via `streaming` split=`train`
- structure:
```json
{
 "id": "str",
 "context": "str",
 "question": "str",
 "answers": {
  "text": [
   "str",
   "len=1"
  ],
  "answer_start": [
   "int",
   "len=1"
  ]
 }
}
```
- sample (record 0, ≤120 chars/field):
  - `id`: TRAIN_186_QUERY_0
  - `context`: 范廷颂枢机（，），圣名保禄·若瑟（），是越南罗马天主教枢机。1963年被任为主教；1990年被擢升为天主教河内总教区宗座署理；1994年被擢升为总主教，同年年底被擢升为枢机；2009年2月离世。范廷颂于1919年6月15日在越南宁平省...
  - `question`: 范廷颂是什么时候被任为主教的？
  - `answers`: {"text": ["1963年"], "answer_start": [30]}
- context_keys: `["context"]`
- answer_start_keys: `["answers.answer_start"]`
- context_len: `{"n": 50, "min": 288, "max": 815, "median": 485.0, "mean": 505.2, "p10": 322, "p90": 815}`
- elapsed: 36.8s

### `clue` / config `cmrc2018`  [mrc]

- exists: True  gated: False  downloads: 8095  license: unknown 
- size: test=3861;train=34334;validation=4316 ['100K<n<1M'] 298.2MB files  loading script: False
- configs in card: ['afqmc', 'c3', 'chid', 'cluewsc2020', 'cmnli', 'cmrc2018', 'csl', 'diagnostics', 'drcd', 'iflytek', 'ocnli', 'tnews']
- card splits: `[{"config": "afqmc", "splits": {"test": 3861, "train": 34334, "validation": 4316}, "dataset_size": 4201506}, {"config": "c3", "splits": {"test": 1625, "train": 11869, "validation": 3816}, "dataset_size": 14263824}, {"config": "chid", "splits": {"test": 3447, "train": 84709, "validation": 3218}, "dataset_size": 274076122}, {"config": "cluewsc2020", "splits": {"test": 2574, "train": 1244, "validation": 304}, "dataset_size": 1007123}, {"config": "cmnli", "splits": {"test": 13880, "train": 391783, "validation": 12241}, "dataset_size": 72123639}, {"config": "cmrc2018", "splits": {"test": 2000, "tra`
- files (first 25): `.gitattributes (1174), README.md (21507), afqmc/test-00000-of-00001.parquet (211060), afqmc/train-00000-of-00001.parquet (1886804), afqmc/validation-00000-of-00001.parquet (239554), c3/test-00000-of-00001.parquet (475638), c3/train-00000-of-00001.parquet (3209206), c3/validation-00000-of-00001.parquet (1034116), chid/test-00000-of-00001.parquet (8693688), chid/train-00000-of-00001.parquet (182424589), chid/validation-00000-of-00001.parquet (7350530), cluewsc2020/test-00000-of-00001.parquet (270556), cluewsc2020/train-00000-of-00001.parquet (84085), cluewsc2020/validation-00000-of-00001.parquet (25970), cmnli/test-00000-of-00001.parquet (1720208), cmnli/train-00000-of-00001.parquet (51159964)`
- **loadable** via `streaming` split=`train`
- structure:
```json
{
 "id": "str",
 "context": "str",
 "question": "str",
 "answers": {
  "text": [
   "str",
   "len=1"
  ],
  "answer_start": [
   "int",
   "len=1"
  ]
 }
}
```
- sample (record 0, ≤120 chars/field):
  - `id`: TRAIN_186_QUERY_0
  - `context`: 范廷颂枢机（，），圣名保禄·若瑟（），是越南罗马天主教枢机。1963年被任为主教；1990年被擢升为天主教河内总教区宗座署理；1994年被擢升为总主教，同年年底被擢升为枢机；2009年2月离世。范廷颂于1919年6月15日在越南宁平省...
  - `question`: 范廷颂是什么时候被任为主教的？
  - `answers`: {"text": ["1963年"], "answer_start": [30]}
- context_keys: `["context"]`
- answer_start_keys: `["answers.answer_start"]`
- context_len: `{"n": 50, "min": 288, "max": 815, "median": 485.0, "mean": 505.2, "p10": 322, "p90": 815}`
- elapsed: 26.0s

### `clue` / config `drcd`  [mrc]

- exists: True  gated: False  downloads: 8095  license: unknown 
- size: test=3861;train=34334;validation=4316 ['100K<n<1M'] 298.2MB files  loading script: False
- configs in card: ['afqmc', 'c3', 'chid', 'cluewsc2020', 'cmnli', 'cmrc2018', 'csl', 'diagnostics', 'drcd', 'iflytek', 'ocnli', 'tnews']
- card splits: `[{"config": "afqmc", "splits": {"test": 3861, "train": 34334, "validation": 4316}, "dataset_size": 4201506}, {"config": "c3", "splits": {"test": 1625, "train": 11869, "validation": 3816}, "dataset_size": 14263824}, {"config": "chid", "splits": {"test": 3447, "train": 84709, "validation": 3218}, "dataset_size": 274076122}, {"config": "cluewsc2020", "splits": {"test": 2574, "train": 1244, "validation": 304}, "dataset_size": 1007123}, {"config": "cmnli", "splits": {"test": 13880, "train": 391783, "validation": 12241}, "dataset_size": 72123639}, {"config": "cmrc2018", "splits": {"test": 2000, "tra`
- files (first 25): `.gitattributes (1174), README.md (21507), afqmc/test-00000-of-00001.parquet (211060), afqmc/train-00000-of-00001.parquet (1886804), afqmc/validation-00000-of-00001.parquet (239554), c3/test-00000-of-00001.parquet (475638), c3/train-00000-of-00001.parquet (3209206), c3/validation-00000-of-00001.parquet (1034116), chid/test-00000-of-00001.parquet (8693688), chid/train-00000-of-00001.parquet (182424589), chid/validation-00000-of-00001.parquet (7350530), cluewsc2020/test-00000-of-00001.parquet (270556), cluewsc2020/train-00000-of-00001.parquet (84085), cluewsc2020/validation-00000-of-00001.parquet (25970), cmnli/test-00000-of-00001.parquet (1720208), cmnli/train-00000-of-00001.parquet (51159964)`
- **loadable** via `streaming` split=`train`
- structure:
```json
{
 "id": "str",
 "context": "str",
 "question": "str",
 "answers": {
  "text": [
   "str",
   "len=1"
  ],
  "answer_start": [
   "int",
   "len=1"
  ]
 }
}
```
- sample (record 0, ≤120 chars/field):
  - `id`: 1001-10-1
  - `context`: 2010年引進的廣州快速公交運輸系統，屬世界第二大快速公交系統，日常載客量可達100萬人次，高峰時期每小時單向客流高達26900人次，僅次於波哥大的快速交通系統，平均每10秒鐘就有一輛巴士，每輛巴士單向行駛350小時。包括橋樑在內的站...
  - `question`: 廣州的快速公交運輸系統每多久就會有一輛巴士？
  - `answers`: {"text": ["10秒鐘"], "answer_start": [84]}
- context_keys: `["context"]`
- answer_start_keys: `["answers.answer_start"]`
- context_len: `{"n": 50, "min": 282, "max": 651, "median": 472.0, "mean": 478.0, "p10": 315, "p90": 640}`
- elapsed: 83.7s

### `clue` / config `c3`  [mrc]

- exists: True  gated: False  downloads: 8095  license: unknown 
- size: test=3861;train=34334;validation=4316 ['100K<n<1M'] 298.2MB files  loading script: False
- configs in card: ['afqmc', 'c3', 'chid', 'cluewsc2020', 'cmnli', 'cmrc2018', 'csl', 'diagnostics', 'drcd', 'iflytek', 'ocnli', 'tnews']
- card splits: `[{"config": "afqmc", "splits": {"test": 3861, "train": 34334, "validation": 4316}, "dataset_size": 4201506}, {"config": "c3", "splits": {"test": 1625, "train": 11869, "validation": 3816}, "dataset_size": 14263824}, {"config": "chid", "splits": {"test": 3447, "train": 84709, "validation": 3218}, "dataset_size": 274076122}, {"config": "cluewsc2020", "splits": {"test": 2574, "train": 1244, "validation": 304}, "dataset_size": 1007123}, {"config": "cmnli", "splits": {"test": 13880, "train": 391783, "validation": 12241}, "dataset_size": 72123639}, {"config": "cmrc2018", "splits": {"test": 2000, "tra`
- files (first 25): `.gitattributes (1174), README.md (21507), afqmc/test-00000-of-00001.parquet (211060), afqmc/train-00000-of-00001.parquet (1886804), afqmc/validation-00000-of-00001.parquet (239554), c3/test-00000-of-00001.parquet (475638), c3/train-00000-of-00001.parquet (3209206), c3/validation-00000-of-00001.parquet (1034116), chid/test-00000-of-00001.parquet (8693688), chid/train-00000-of-00001.parquet (182424589), chid/validation-00000-of-00001.parquet (7350530), cluewsc2020/test-00000-of-00001.parquet (270556), cluewsc2020/train-00000-of-00001.parquet (84085), cluewsc2020/validation-00000-of-00001.parquet (25970), cmnli/test-00000-of-00001.parquet (1720208), cmnli/train-00000-of-00001.parquet (51159964)`
- **loadable** via `streaming` split=`train`
- structure:
```json
{
 "id": "int",
 "context": [
  "str",
  "len=2"
 ],
 "question": "str",
 "choice": [
  "str",
  "len=4"
 ],
 "answer": "str"
}
```
- sample (record 0, ≤120 chars/field):
  - `id`: 0
  - `context`: ["男：你今天晚上有时间吗?我们一起去看电影吧?", "女：你喜欢恐怖片和爱情片，但是我喜欢喜剧片，科幻片一般。所以……"]
  - `question`: 女的最喜欢哪种电影?
  - `choice`: ["恐怖片", "爱情片", "喜剧片", "科幻片"]
  - `answer`: 喜剧片
- context_keys: `["context"]`
- answer_start_keys: `[]`
- context_len: `{"n": 50, "min": 27, "max": 612, "median": 54.5, "mean": 115.8, "p10": 31, "p90": 612}`
- elapsed: 82.7s

### `PaddlePaddle/dureader_robust`  [mrc]

- exists: True  gated: False  downloads: 407  license: apache-2.0 
- size: 0.0MB files  loading script: True
- files (first 25): `.gitattributes (1567), README.md (31), dureader_robust.py (4549)`
- **loadable** via `parquet-convert:plain_text/train/0000.parquet` split=`train`
- structure:
```json
{
 "id": "str",
 "title": "str",
 "context": "str",
 "question": "str",
 "answers": {
  "text": [
   "str",
   "len=1"
  ],
  "answer_start": [
   "int",
   "len=1"
  ]
 }
}
```
- sample (record 0, ≤120 chars/field):
  - `id`: 0a25cb4bc1ab6f474c699884e04601e4
  - `title`: 
  - `context`: 第35集雪见缓缓张开眼睛，景天又惊又喜之际，长卿和紫萱的仙船驶至，见众人无恙，也十分高兴。众人登船，用尽合力把自身的真气和水分输给她。雪见终于醒过来了，但却一脸木然，全无反应。众人向常胤求助，却发现人世界竟没有雪见的身世纪录。长卿询问...
  - `question`: 仙剑奇侠传3第几集上天界
  - `answers`: {"text": ["第35集"], "answer_start": [0]}
- context_keys: `["context"]`
- answer_start_keys: `["answers.answer_start"]`
- context_len: `{"n": 50, "min": 105, "max": 768, "median": 215.0, "mean": 264.1, "p10": 113, "p90": 471}`
- elapsed: 41.6s

### `luozhouyang/dureader`  [mrc]

- exists: True  gated: False  downloads: 198  license: (none in card) 
- size: 41.1MB files  loading script: True
- files (first 25): `.gitattributes (1275), .gitignore (1297), README.md (529), dataset_infos.json (2853), dummy/checklist/1.0.0/dummy_data.zip (19408914), dummy/checklist/1.0.0/dummy_data.zip.lock (0), dummy/robust/1.0.0/dummy_data.zip (21712594), dummy/robust/1.0.0/dummy_data.zip.lock (0), dureader.py (8674)`
- **loadable** via `parquet-convert:checklist/train/0000.parquet` split=`train`
- structure:
```json
{
 "id": "str",
 "title": "str",
 "context": "str",
 "question": "str",
 "is_impossible": "str",
 "answers": {
  "text": [
   "str",
   "len=1"
  ],
  "answer_start": [
   "int",
   "len=1"
  ]
 },
 "type": "str"
}
```
- sample (record 0, ≤120 chars/field):
  - `id`: 73d5dc65c40a263cf2c2263e6462190c
  - `title`: 属鼠的想用五谷起小名 属鼠小名多米的寓意-十二星座网
  - `context`: ——使用叠字的小名是很好听的,对于刚刚出生的男孩来说,这样的名字是很方便记忆的,这也就拉近了孩子与家长之间的距离。糕,代表的是“用面粉所制成的食品”,那么此字在含义上是带有“多米”的含义,作为属鼠男孩的小名,寓意上是很不错的。
  - `question`: 属鼠小名多米的寓意
  - `is_impossible`: True
  - `answers`: {"text": [""], "answer_start": [-1]}
  - `type`: in-domain
- context_keys: `["context"]`
- answer_start_keys: `["answers.answer_start"]`
- context_len: `{"n": 50, "min": 62, "max": 754, "median": 132.0, "mean": 181.0, "p10": 79, "p90": 370}`
- elapsed: 42.6s

### `thu-coai/kdconv`  [kdialog]

- exists: True  gated: False  downloads: 349  license: apache-2.0 
- size: 47.3MB files  loading script: False
- files (first 25): `.gitattributes (2319), README.md (502), film/dev.json (1363416), film/kb_film.json (13033734), film/test.json (1547354), film/train.json (7892763), music/dev.json (945559), music/kb_music.json (7455368), music/test.json (1148564), music/train.json (4952078), travel/dev.json (904751), travel/kb_travel.json (1835419), travel/test.json (1100567), travel/train.json (5156841)`
- **loadable** via `streaming` split=`train`
- structure:
```json
{
 "messages": [
  {
   "attrs": "NoneType",
   "message": "str"
  },
  "len=30"
 ],
 "name": "str"
}
```
- sample (record 0, ≤120 chars/field):
  - `messages`: [{"attrs": null, "message": "知道重庆森林这部电影吗？"}, {"attrs": [{"attrname": "导演", "attrvalue": "王家卫", "name": "重庆森林（1994年王家卫...
  - `name`: 重庆森林（1994年王家卫执导电影）
- dialog_keys: `["messages", "messages[0].attrs"]`
- elapsed: 49.4s

### `PaddlePaddle/duconv`  [kdialog]

- exists: True  gated: False  downloads: 64  license: apache-2.0 
- size: 0.0MB files  loading script: True
- files (first 25): `.gitattributes (1737), README.md (28), duconv.py (5059)`
- **loadable** via `streaming` split=`train`
- structure:
```json
{
 "id": "str",
 "goal": [
  [
   "str",
   "len=3"
  ],
  "len=3"
 ],
 "knowledge": [
  [
   "str",
   "len=3"
  ],
  "len=16"
 ],
 "conversation": [
  "str",
  "len=8"
 ],
 "history": "list[empty]",
 "response": "str"
}
```
- sample (record 0, ≤120 chars/field):
  - `id`: 0
  - `goal`: [["START", "托马斯 · 桑斯特", "陈思宇"], ["托马斯 · 桑斯特", "出生 日期", "1990 - 5 - 16"], ["陈思宇", "出生 日期", "1990 - 5 - 16"]]
  - `knowledge`: [["托马斯 · 桑斯特", "血型", "A型"], ["托马斯 · 桑斯特", "标签", "口碑 很好"], ["托马斯 · 桑斯特", "获奖", "移动迷宫_提名 _ ( 2015 ； 第17届 ) _ 青少年选择奖 _ 青...
  - `conversation`: ["知道 外国 有 个 明星 长 得 很 萌 吗 ？", "这个 还 真 不知道 呢 ， 请问 是 谁 啊 ？", "是 托马斯 · 桑斯特 ， 颜值 太 高 了 。", "哦 ， 没 应 说过 呢 ， 你 能 给 大体 说说 么 ？...
  - `history`: []
  - `response`: 
- dialog_keys: `["goal", "knowledge", "conversation", "history", "response"]`
- elapsed: 11.2s

### `BelleGroup/train_1M_CN`  [instruct]

- exists: True  gated: False  downloads: 1144  license: gpl-3.0 
- size: ['100K<n<1M'] 457.7MB files  loading script: False
- files (first 25): `.gitattributes (2327), Belle_open_source_1M.json (457667956), README.md (941)`
- **loadable** via `single-file:Belle_open_source_1M.json` split=`train`
- structure:
```json
{
 "instruction": "str",
 "input": "str",
 "output": "str"
}
```
- sample (record 0, ≤120 chars/field):
  - `instruction`: 判断给定的文章是否符合语法规则。如果不符合，请提供修改建议。\n下面是一篇文章的开头: "为了探讨这个主题，本文将提供一系列数据和实例，以证明这一观点。"\n
  - `input`: 
  - `output`: 这个开头符合语法规则。
- elapsed: 7.9s

### `silk-road/alpaca-data-gpt4-chinese`  [instruct]

- exists: True  gated: False  downloads: 3597  license: apache-2.0 
- size: ['10K<n<100K'] 78.4MB files  loading script: False
- files (first 25): `.gitattributes (2327), Alpaca_data_gpt4_zh.jsonl (78401244), README.md (183)`
- **loadable** via `single-file:Alpaca_data_gpt4_zh.jsonl` split=`train`
- structure:
```json
{
 "instruction_zh": "str",
 "input_zh": "str",
 "output_zh": "str",
 "instruction": "str",
 "input": "str",
 "output": "str"
}
```
- sample (record 0, ≤120 chars/field):
  - `instruction_zh`: 给出三个保持健康的小贴士。
  - `input_zh`: 
  - `output_zh`: 1. 饮食要均衡且富有营养：确保你的餐食包含各种水果、蔬菜、瘦肉、全谷物和健康脂肪。这有助于为身体提供必要的营养，使其发挥最佳功能，并有助于预防慢性疾病。2. 经常参加体育锻炼：锻炼对于保持强壮的骨骼、肌肉和心血管健康至关重要。每周至...
  - `instruction`: Give three tips for staying healthy.
  - `input`: 
  - `output`: 1. Eat a balanced and nutritious diet: Make sure your meals are inclusive of a variety of fruits and vegetables, lean...
- elapsed: 7.8s

### `xywang1/NaturalConv`  [kdialog]

- exists: True  gated: False  downloads: 609  license: other (tencent-ai-lab-naturalconv-dataset-terms-and-conditions)
- size: ['10K<n<100K'] 52.6MB files  loading script: False
- configs in card: ['default']
- files (first 25): `.gitattributes (2462), LICENSE (3634), README.md (3324), dev.txt (1832), dialog_release.json (51726524), document_url_release.json (739488), test.txt (1824), train.txt (131469)`
- **loadable** via `parquet-convert:default/train/0000.parquet` split=`train`
- structure:
```json
{
 "dialog_id": "str",
 "document_id": "int",
 "content": [
  "str",
  "len=22"
 ]
}
```
- sample (record 0, ≤120 chars/field):
  - `dialog_id`: 0_2
  - `document_id`: 0
  - `content`: ["嗨！", "你好。", "你最近有听说过《中国女排》这部电影嘛？", "不好意思唉，我已经很久没有去关注电影了，你可以给我讲述一下这是什么电影嘛。", "当然可以了，这部片子主要是讲述了女排这些年的历史，而且听说这部戏里面的郎平教...
- dialog_keys: `["content"]`
- elapsed: 1562.7s

### `thu-coai/kd_conv_with_kb`  [kdialog]

- exists: True  gated: False  downloads: 312  license: apache-2.0 
- size: train=1200;test=150;validation=150 ['1K<n<10K'] 10.2MB files  loading script: True
- card splits: `[{"config": "travel_dialogues", "splits": {"train": 1200, "test": 150, "validation": 150}, "dataset_size": 4652610}, {"config": "travel_knowledge_base", "splits": {"train": 1154}, "dataset_size": 1517024}, {"config": "music_dialogues", "splits": {"train": 1200, "test": 150, "validation": 150}, "dataset_size": 4441109}, {"config": "music_knowledge_base", "splits": {"train": 4441}, "dataset_size": 5980643}, {"config": "film_dialogues", "splits": {"train": 1200, "test": 150, "validation": 150}, "dataset_size": 6708886}, {"config": "film_knowledge_base", "splits": {"train": 8090}, "dataset_size": `
- files (first 25): `.gitattributes (1174), README.md (10680), data.zip (10210217), kd_conv_with_kb.py (7801)`
- **loadable** via `streaming` split=`train`
- structure:
```json
{
 "messages": {
  "message": [
   "str",
   "len=20"
  ],
  "attrs": [
   {
    "attrname": "list[empty]",
    "attrvalue": "list[empty]",
    "name": "list[empty]"
   },
   "len=20"
  ]
 },
 "name": "str",
 "domain": "str"
}
```
- sample (record 0, ≤120 chars/field):
  - `messages`: {"message": ["你知道北京石刻艺术博物馆吗？", "知道，是第一座陈列北京地区石刻文物的专题性博物馆。", "都啥时候开放呢？", "9:00-16:00（周一闭馆）。", "地址呢？", "北京市海淀区五塔寺村24号（近...
  - `name`: 北京石刻艺术博物馆
  - `domain`: travel
- dialog_keys: `["messages", "messages.attrs"]`
- elapsed: 12.5s

### `justhangingoutguy/NaturalConversations-36k`  [kdialog]

- exists: True  gated: False  downloads: 36  license: (none in card) 
- size: ['10K<n<100K'] 40.8MB files  loading script: False
- files (first 25): `.gitattributes (2635), NaturalConversation-36k.jsonl (40759785), README.md (950)`
- **loadable** via `streaming` split=`train`
- structure:
```json
{
 "messages": [
  {
   "role": "str",
   "content": "str"
  },
  "len=12"
 ]
}
```
- sample (record 0, ≤120 chars/field):
  - `messages`: [{"role": "user", "content": "Have you tried that new vegan place in the student union?"}, {"role": "assistant", "con...
- dialog_keys: `["messages", "messages[0].content"]`
- elapsed: 10.8s

### `VITA-MLLM/Emotion_NaturalConv_FunctionCall`  [kdialog]

- exists: True  gated: False  downloads: 39  license: (none in card) 
- size: 1982.6MB files  loading script: False
- files (first 25): `.gitattributes (2791), Emotion_Control/QEmo/eval.json (2080156), Emotion_Control/QEmo/train.json (233680577), Emotion_Control/QNeutral/eval.json (2577523), Emotion_Control/QNeutral/train.json (166256169), Emotion_Control/emotion_qa.tar.gz (869253427), Function_Call/fc.tar.gz (105644637), Function_Call/fc1/eval.json (1667736), Function_Call/fc1/train.json (28004431), Function_Call/fc2/eval.json (720925), Function_Call/fc2/train.json (60835139), Natural_Conv/.DS_Store (6148), Natural_Conv/eval.json (4604097), Natural_Conv/natural.tar.gz (422890795), Natural_Conv/train.json (84415426)`
- **NOT loadable**: `single-file: HfHubHTTPError: Server error '504 Gateway Timeout' for url 'https://huggingface.co/api/datasets/VITA-MLLM/Emotion_NaturalConv_FunctionCall/tree/main?recursive=true&expand=false' (Request ID: Root=1-6ae86a10-299068095a8616dd43887ead;e3f27888-f673-4291-8680-41bae825025a)\nFor more information check: https://develo... | streaming: ValueError: Not able to read records in the JSON file at hf://datasets/VITA-MLLM/Emotion_NaturalConv_FunctionCall@d53036efe2588c6b5d1065aa6147d5199a309f67/Emotion_Control/QEmo/train.json. | parquet-convert: RevisionNotFoundError: 404 Client Error. (Request ID: Root=1-6ae86a33-37ac5b0846df77eb755fa580;e426e7df-00b6-488a-8e95-3d815d023f67)\n\nRevision Not Found for url: https://huggingface.co/api/datasets/VITA-MLLM/Emotion_NaturalConv_FunctionCall/tree/refs%2Fconvert%2Fparquet?recursive=true&expand=false.\nInvalid rev id: r...`
- elapsed: 36.6s

### `Fair-HV/NaturalConversations-36k`  [kdialog]

- exists: True  gated: False  downloads: 15  license: (none in card) 
- size: ['10K<n<100K'] 40.8MB files  loading script: False
- files (first 25): `.gitattributes (2635), NaturalConversation-36k.jsonl (40759785), README.md (950)`
- **loadable** via `streaming` split=`train`
- structure:
```json
{
 "messages": [
  {
   "role": "str",
   "content": "str"
  },
  "len=12"
 ]
}
```
- sample (record 0, ≤120 chars/field):
  - `messages`: [{"role": "user", "content": "Have you tried that new vegan place in the student union?"}, {"role": "assistant", "con...
- dialog_keys: `["messages", "messages[0].content"]`
- elapsed: 9.1s

### `m-a-p/COIG-CQIA`  [instruct]

- exists: True  gated: False  downloads: 11819  license: (none in card) 
- size: ['10K<n<100K'] 299.2MB files  loading script: False
- configs in card: ['chinese_traditional', 'coig_pc', 'exam', 'finance', 'douban', 'finance', 'human_value', 'logi_qa', 'ruozhiba', 'segmentfault', 'wiki', 'wikihow', 'xhs', 'zhihu']
- files (first 25): `.gitattributes (2949), COIG-CQIA-full.jsonl (149472971), README.md (12747), Yi_logo.svg (865), chinese_traditional/chengyu.jsonl (82480), chinese_traditional/poem.jsonl (30018), chinese_traditional/trad-multi-choice-100-2.jsonl (58480), chinese_traditional/trad-multi-choice-100.jsonl (59864), chinese_traditional/trad-multi-choice-40.jsonl (40859), chinese_traditional/translate_classical_chinese.jsonl (649287), coig_pc/coig_pc_core_sample.jsonl (4624040), douban/book_introduce.jsonl (718502), douban/book_reviews.jsonl (464357), douban/movie_anime_synopsis_more_prompt.jsonl (636004), douban/movie_documentary_synopsis_more_prompt.jsonl (134284), douban/movie_recommendation.jsonl (53315), douban`
- **loadable** via `parquet-convert:chinese_traditional/train/0000.parquet` split=`train`
- structure:
```json
{
 "instruction": "str",
 "input": "str",
 "output": "str",
 "task_type": {
  "major": [
   "str",
   "len=1"
  ],
  "minor": [
   "str",
   "len=1"
  ]
 },
 "domain": [
  "str",
  "len=2"
 ],
 "metadata": "str",
 "answer_from": "str",
 "human_verified": "bool",
 "copyright": "str"
}
```
- sample (record 0, ≤120 chars/field):
  - `instruction`: 暗度陈仓\n成语释义：
  - `input`: 
  - `output`: 指正面迷惑敌人，而从侧翼进行突然袭击。亦比喻暗中进行活动。陈仓，古县名，在今陕西省宝鸡市东，为通向汉中的交通孔道。\n成语出处：《史记·高祖本纪》……项王使卒三万人从，楚与诸侯之慕从者数万人，从杜南入蚀中。去辄烧绝栈道，以备诸侯盗兵袭...
  - `task_type`: {"major": ["文本生成"], "minor": ["成语释义"]}
  - `domain`: ["中国传统文化", "成语"]
  - `metadata`: 暂无元数据信息
  - `answer_from`: human
  - `human_verified`: true
  - `copyright`: 暂无版权及作者信息
- elapsed: 15.0s

### `YeungNLP/firefly-train-1.1M`  [instruct]

- exists: True  gated: False  downloads: 3371  license: (none in card) 
- size: 1171.2MB files  loading script: False
- files (first 25): `.gitattributes (2326), README.md (1237), firefly-train-1.1M.jsonl (1171119212), len_distribution.png (18830), task_distribution.png (43258)`
- **loadable** via `streaming` split=`train`
- structure:
```json
{
 "kind": "str",
 "input": "str",
 "target": "str"
}
```
- sample (record 0, ≤120 chars/field):
  - `kind`: NLI
  - `input`: 自然语言推理：\n前提：家里人心甘情愿地养他,还有几家想让他做女婿的\n假设：他是被家里人收养的孤儿
  - `target`: 中立
- elapsed: 9.0s

### `BAAI/COIG`  [instruct]

- exists: True  gated: False  downloads: 2678  license: apache-2.0 
- size: 338.2MB files  loading script: True
- files (first 25): `.gitattributes (2352), .gitignore (6), COIG.py (9580), README.md (6642), counterfactural_correction_multi_round_chat.tar.gz (154211474), exam_instructions.jsonl (76149003), human_value_alignment_instructions_part1.json (2222403), human_value_alignment_instructions_part2.json (17596776), leetcode_instructions.jsonl (31073674), translated_instructions.jsonl (56888574)`
- **loadable** via `streaming` split=`Default`
- structure:
```json
{
 "instruction": "str",
 "conversations": [
  {
   "question": "str",
   "answer": "str"
  },
  "len=5"
 ]
}
```
- sample (record 0, ≤120 chars/field):
  - `instruction`: 
  - `conversations`: [{"question": "特种珊瑚是一种海洋动物吗？", "answer": "特种珊瑚虽然生活在海洋中，但它属于珊瑚软体类的石珊瑚目，是一种动物。而海洋动物是海洋中所有异养型生物的总称，包括鱼类、鲸类、浮游动物和游泳动物等，特种...
- elapsed: 9.4s

### `cver91/liu-software-firefly-data`  [instruct]

- exists: True  gated: manual  downloads: 2134  license: (none in card) 
- size: 39990.0MB files  loading script: False
- files (first 25): `.gitattributes (2504), liu-software-firefly-20261026-1.tar (31151728640), liu-software-firefly-20261026-1.tar.sha256 (102), liu-software-firefly-20261026-2.tar (8838225920), liu-software-firefly-20261026-2.tar.sha256 (102)`
- **NOT loadable**: `streaming: ConnectionError: Couldn't reach https://huggingface.co/datasets/cver91/liu-software-firefly-data/resolve/8c330ecdf7d4eb2f58fc625f62bd40caebe79a40/.huggingface.yaml (error 403) | parquet-convert: RevisionNotFoundError: 404 Client Error. (Request ID: Root=1-6ae868dd-167a6fcd6111b96512a3c5b4;2e2b5438-3666-4a94-b730-41c914572202)\n\nRevision Not Found for url: https://huggingface.co/api/datasets/cver91/liu-software-firefly-data/tree/refs%2Fconvert%2Fparquet?recursive=true&expand=false.\nInvalid rev id: refs/conver...`
- elapsed: 3.6s

### `BAAI/COIG-PC`  [instruct]

- exists: True  gated: auto  downloads: 576  license: unknown 
- size: full=321332879;train=208529583;valid=2087767;test=8094740;Top50PerTask=63643;Top100PerTask=127158;Top200PerTask=253558 126915.7MB files  loading script: False
- configs in card: ['default']
- card splits: `[{"config": null, "splits": {"full": 321332879, "train": 208529583, "valid": 2087767, "test": 8094740, "Top50PerTask": 63643, "Top100PerTask": 127158, "Top200PerTask": 253558}, "dataset_size": 342747577547}]`
- files (first 25): `.gitattributes (2265), README.md (17151), assets/baai.png (27820), assets/bupt.png (92579), assets/hkust.png (88422), assets/linksoul.png (111691), assets/map.png (85527), assets/pku.png (22464), assets/sheffield.png (113051), assets/stardust.png (108757), assets/waterloo.png (245285), data/Top100PerTask-00000-of-00001-6e862db88ad4ae39.parquet (76929658), data/Top200PerTask-00000-of-00001-fe36897020230691.parquet (160399530), data/Top50PerTask-00000-of-00001-aaeff287493ab78e.parquet (37803331), data/full-00000-of-00398-97cc48b2a582f471.parquet (124648156), data/full-00001-of-00398-f2a13860f09f5385.parquet (83759832), data/full-00002-of-00398-5d603e3dea0734ef.parquet (87184973), data/full-000`
- **NOT loadable**: `streaming: ConnectionError: Couldn't reach https://huggingface.co/datasets/BAAI/COIG-PC/resolve/4ca2778d69d7a9c17a0a6c1668c6e989b102176b/.huggingface.yaml (error 403) | parquet-convert: GatedRepoError: 403 Client Error. (Request ID: Root=1-6ae868e4-1bb1316a299f74c07fa9171b;8027570a-d60c-4749-85e7-a9ae978cc61b)\n\nCannot access gated repo for url https://huggingface.co/datasets/BAAI/COIG-PC/resolve/refs%2Fconvert%2Fparquet/default/train/0000.parquet.\nAccess to dataset BAAI/COIG-PC is restricted...`
- elapsed: 7.5s

### `m-a-p/COIG-Kun`  [instruct]

- exists: True  gated: False  downloads: 816  license: (none in card) 
- size: ['100K<n<1M'] 573.4MB files  loading script: False
- configs in card: ['default']
- files (first 25): `.gitattributes (2612), Kun_white.png (490573), README.md (4620), Yi_logo.svg (865), m-a-p.png (5248), skypile_v1.jsonl (215079561), wanjuan_v1.jsonl (292727722), wudao_v1.jsonl (65053260)`
- **loadable** via `streaming` split=`wudao`
- structure:
```json
{
 "instruction": "str",
 "output": "str",
 "Academic/Professional Field": "str",
 "Industry Category": "str",
 "Text type": "str"
}
```
- sample (record 0, ≤120 chars/field):
  - `instruction`: 如何评价祁又一自编自导的电影《鸽子小姐》？
  - `output`: 《鸽子小姐》是一部由祁又一自编自导的电影。影片改编自小说《失踪女》。影片讲述的是怀揣着摇滚梦的北京孩子张大伟喜欢上一个经常失踪的女嬉皮士，这个叫鸽子的果儿每次失踪都将大张伟家洗劫一空。张大伟是个外表酷炫内心柔软的巨蟹座，他碍于摇滚明星...
  - `Academic/Professional Field`: Others
  - `Industry Category`: Others
  - `Text type`: Others
- elapsed: 13.0s

## Hub searches (sorted by downloads)

### [mrc] "dureader"

| id | downloads | gated | license | lang |
|---|---|---|---|---|
| ERROR ConnectError: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1010) | | | | |

### [mrc] "cmrc"

| id | downloads | gated | license | lang |
|---|---|---|---|---|
| ERROR ConnectError: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1010) | | | | |

### [mrc] "drcd"

| id | downloads | gated | license | lang |
|---|---|---|---|---|
| ERROR ConnectError: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1010) | | | | |

### [kdialog] "duconv"

| id | downloads | gated | license | lang |
|---|---|---|---|---|
| ERROR ConnectError: [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1010) | | | | |

### [kdialog] "kdconv"

| id | downloads | gated | license | lang |
|---|---|---|---|---|
| `thu-coai/kdconv` | 349 | False | apache-2.0 | language:zh |
| `thu-coai/kd_conv_with_kb` | 316 | False | ['apache-2.0'] | language:zh |

### [kdialog] "knowledge grounded dialogue chinese"

| id | downloads | gated | license | lang |
|---|---|---|---|---|

### [kdialog] "chinese knowledge dialogue"

| id | downloads | gated | license | lang |
|---|---|---|---|---|

### [kdialog] "naturalconv"

| id | downloads | gated | license | lang |
|---|---|---|---|---|
| `xywang1/NaturalConv` | 609 | False | other | language:zh |
| `justhangingoutguy/NaturalConversations-36k` | 36 | False | [] | language:en,language:es |
| `VITA-MLLM/Emotion_NaturalConv_FunctionCall` | 34 | False | [] |  |
| `Fair-HV/NaturalConversations-36k` | 15 | False | [] | language:en,language:es |
| `tolgaege/natural_conversation` | 5 | False | [] |  |
| `Cbatch/natural_conversation` | 4 | False | [] |  |

### [instruct] "COIG"

| id | downloads | gated | license | lang |
|---|---|---|---|---|
| `m-a-p/COIG-CQIA` | 11681 | False | [] | language:zh |
| `BAAI/COIG` | 2646 | False | apache-2.0 | language:zh |
| `BAAI/COIG-PC` | 804 | auto | unknown | language:zh |
| `m-a-p/COIG-Kun` | 792 | False | [] | language:zh |
| `BAAI/COIG-PC-Lite` | 519 | False | unknown | language:zh |
| `m-a-p/COIG-Writer` | 416 | False | apache-2.0 | language:zh |
| `m-a-p/COIG-P` | 396 | False | [] |  |
| `BAAI/COIG-PC-core` | 389 | False | unknown | language:zh |
| `hqili/COIG-CQIA` | 315 | False | [] | language:zh |
| `zhengr/COIG-CQIA` | 235 | False | [] | language:zh |
| `Starlento/SFT-COIG-CQIA-handbook` | 127 | False | [] | language:zh |
| `botp/COIG-CQIA` | 123 | False | [] | language:zh |
| `erhwenkuo/coig-pc-zhtw` | 90 | False | [] |  |
| `ssbuild/alpaca_coig` | 71 | False | apache-2.0 |  |
| `lorinma/EvolInstruct_zh_COIG-PC_Deepseek` | 69 | False | mit | language:zh |

### [instruct] "firefly"

| id | downloads | gated | license | lang |
|---|---|---|---|---|
| `YeungNLP/firefly-train-1.1M` | 3294 | False | [] |  |
| `cver91/liu-software-firefly-data` | 2134 | manual | [] |  |
| `YeungNLP/firefly-pretrain-dataset` | 600 | False | [] |  |
| `linhle80000/firefly` | 459 | False | [] |  |
| `open-llm-leaderboard-old/details_YeungNLP__firefly-llama-13b-v1.2` | 214 | False | [] |  |
| `firefly1709/mahathi_bottle` | 120 | False | [] |  |
| `erhwenkuo/firefly-train-chinese-zhtw` | 91 | False | [] | language:zh |
| `open-llm-leaderboard-old/details_YeungNLP__firefly-mixtral-8x7b-v1` | 91 | False | [] |  |
| `open-llm-leaderboard-old/details_YeungNLP__firefly-qwen1.5-en-7b` | 81 | False | [] |  |
| `contralabs/firefly-creative-campaign-trajectories` | 80 | False | cc-by-4.0 | language:en |
| `open-llm-leaderboard-old/details_YeungNLP__firefly-ziya-13b` | 76 | False | [] |  |
| `firefly1709/mahathi_bottle_pour` | 68 | False | [] |  |
| `Anticloud/anticloud-firefly` | 66 | False | [] |  |
| `open-llm-leaderboard-old/details_YeungNLP__firefly-llama-13b` | 64 | False | [] |  |
| `DialogueCharacter/chinese_firefly_unfiltered` | 59 | False | [] |  |

### [instruct] "chinese instruction"

| id | downloads | gated | license | lang |
|---|---|---|---|---|
| `LinkSoul/Chinese-LLaVA-Vision-Instructions` | 271 | False | apache-2.0 | language:en,language:zh |
| `dlface/code_instructions_120k_alpaca_chinese` | 97 | False | [] |  |
| `dlface/CodeFeedback-Filtered-Instruction-Chinese` | 78 | False | apache-2.0 |  |
| `DialogueCharacter/chinese_general_instruction_with_reward_score` | 76 | False | [] |  |
| `dkqkxx/chinese_instruction_sample` | 65 | False | [] |  |
| `jean1/45k_python_code_chinese_instruction` | 49 | False | [] |  |
| `g8603003/Chinese-LLaVA-Vision-Instructions` | 34 | False | apache-2.0 | language:en,language:zh |
| `DialogueCharacter/chinese_dialogue_instruction_with_reward_score_judged_by_13B_baichuan2` | 31 | False | [] |  |

### [instruct] "alpaca chinese"

| id | downloads | gated | license | lang |
|---|---|---|---|---|
| `silk-road/alpaca-data-gpt4-chinese` | 3585 | False | apache-2.0 | language:zh,language:en |
| `open-llm-leaderboard-old/details_hfl__chinese-alpaca-2-7b-rlhf` | 473 | False | [] |  |
| `FreedomIntelligence/alpaca-gpt4-chinese` | 324 | False | [] |  |
| `open-llm-leaderboard-old/details_hfl__chinese-alpaca-2-1.3b` | 117 | False | [] |  |
| `dlface/code_instructions_120k_alpaca_chinese` | 97 | False | [] |  |
| `open-llm-leaderboard-old/details_shibing624__chinese-alpaca-plus-13b-hf` | 72 | False | [] |  |
| `erhwenkuo/alpaca-data-gpt4-chinese-zhtw` | 67 | False | [] | language:zh |
| `open-llm-leaderboard-old/details_hfl__chinese-alpaca-2-1.3b-rlhf` | 66 | False | [] |  |
| `botp/silk-road_alpaca-data-gpt4-chinese` | 59 | False | apache-2.0 | language:zh,language:en |
| `aifeifei798/Chinese-DeepSeek-R1-Distill-data-110k-alpaca` | 58 | False | apache-2.0 |  |
| `open-llm-leaderboard-old/details_shibing624__chinese-alpaca-plus-7b-hf` | 54 | False | [] |  |
| `JiaweiGuo123/Alpaca-gpt4-Chinese-Part-Scoring-By-T5-Model` | 41 | False | [] |  |
| `silk-road/Vanilla-chinese-alpaca-luotuo` | 40 | False | apache-2.0 | language:zh |
| `saillab/alpaca-chinesesimplified-cleaned` | 40 | False | [] | language:zh |
| `xxastralxx/alpaca-data-gpt4-chinese` | 31 | False | apache-2.0 | language:zh,language:en |

### [instruct] "chinese system prompt"

| id | downloads | gated | license | lang |
|---|---|---|---|---|

### [instruct] "ifeval chinese"

| id | downloads | gated | license | lang |
|---|---|---|---|---|
