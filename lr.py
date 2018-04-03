{
  "cells": [
    {
      "metadata": {
        "_cell_guid": "b1076dfc-b9ad-4769-8c92-a6c4dae69d19",
        "_uuid": "8f2839f25d086af736a60e9eeb907d3b93b6e0e5",
        "trusted": false,
        "collapsed": true
      },
      "cell_type": "code",
      "source": "# This Python 3 environment comes with many helpful analytics libraries installed\n# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python\n# For example, here's several helpful packages to load in \n\nimport numpy as np # linear algebra\nimport pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)\n\n# Input data files are available in the \"../input/\" directory.\n# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory\n\nimport os\nprint(os.listdir(\"../input\"))\n\n# Any results you write to the current directory are saved as output.\n\nfrom sklearn.model_selection import train_test_split, cross_val_score\nfrom sklearn.feature_extraction.text import TfidfVectorizer\nfrom sklearn.linear_model import LogisticRegression\nfrom scipy.sparse import hstack\nimport regex as re\nimport regex",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "79c7e3d0-c299-4dcb-8224-4455121ee9b0",
        "_uuid": "d629ff2d2480ee46fbb7e2d37f6b5fab8052498a",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "class_names = ['toxic', 'severe_toxic', 'obscene', 'threat', 'insult', 'identity_hate']\n\ntrain = pd.read_csv('../input/train.csv').fillna(' ')\ntest = pd.read_csv('../input/test.csv').fillna(' ')",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "49488c88-fc40-4114-bc72-76f3c9ebb3a7",
        "_uuid": "79e338279605e865298bc0d51afcba9a816c038c",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "train_links = train[\"comment_text\"].apply(lambda x: len(re.findall(\"(http:\\/\\/www\\.|https:\\/\\/www\\.|http:\\/\\/|https:\\/\\/)?[a-z0-9]+([\\-\\.]{1}[a-z0-9]+)*\\.[a-z]{2,5}(:[0-9]{1,5})?(\\/.*)?\",str(x)))).values.reshape(len(train), 1)\ntest_links = test[\"comment_text\"].apply(lambda x: len(re.findall(\"(http:\\/\\/www\\.|https:\\/\\/www\\.|http:\\/\\/|https:\\/\\/)?[a-z0-9]+([\\-\\.]{1}[a-z0-9]+)*\\.[a-z]{2,5}(:[0-9]{1,5})?(\\/.*)?\",str(x)))).values.reshape(len(test), 1)\n\n\nlinks_n = np.append(train_links, test_links)\nlinksmean = train_links.mean()\nlinksstd = test_links.std()\n\ntrain_links_n = (train_links - linksmean) / linksstd\ntest_links_n = (test_links - linksmean) / linksstd",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "86c42c57-87e7-40f4-ae1b-94a77f7a127c",
        "_uuid": "c602ff77ed52795dbdff91dcabcdea2e5641ea89",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "repl = {\n    \"yay!\": \" good \",\n    \"yay\": \" good \",\n    \"yaay\": \" good \",\n    \"yaaay\": \" good \",\n    \"yaaaay\": \" good \",\n    \"yaaaaay\": \" good \",\n    \":/\": \" bad \",\n    \":&gt;\": \" sad \",\n    \":')\": \" sad \",\n    \":-(\": \" frown \",\n    \":(\": \" frown \",\n    \":s\": \" frown \",\n    \":-s\": \" frown \",\n    \"&lt;3\": \" heart \",\n    \":d\": \" smile \",\n    \":p\": \" smile \",\n    \":dd\": \" smile \",\n    \"8)\": \" smile \",\n    \":-)\": \" smile \",\n    \":)\": \" smile \",\n    \";)\": \" smile \",\n    \"(-:\": \" smile \",\n    \"(:\": \" smile \",\n    \":/\": \" worry \",\n    \":&gt;\": \" angry \",\n    \":')\": \" sad \",\n    \":-(\": \" sad \",\n    \":(\": \" sad \",\n    \":s\": \" sad \",\n    \":-s\": \" sad \",\n    r\"\\br\\b\": \"are\",\n    r\"\\bu\\b\": \"you\",\n    r\"\\bhaha\\b\": \"ha\",\n    r\"\\bhahaha\\b\": \"ha\",\n    r\"\\bdon't\\b\": \"do not\",\n    r\"\\bdoesn't\\b\": \"does not\",\n    r\"\\bdidn't\\b\": \"did not\",\n    r\"\\bhasn't\\b\": \"has not\",\n    r\"\\bhaven't\\b\": \"have not\",\n    r\"\\bhadn't\\b\": \"had not\",\n    r\"\\bwon't\\b\": \"will not\",\n    r\"\\bwouldn't\\b\": \"would not\",\n    r\"\\bcan't\\b\": \"can not\",\n    r\"\\bcannot\\b\": \"can not\",\n    r\"\\bi'm\\b\": \"i am\",\n    \"m\": \"am\",\n    \"r\": \"are\",\n    \"u\": \"you\",\n    \"haha\": \"ha\",\n    \"hahaha\": \"ha\",\n    \"don't\": \"do not\",\n    \"doesn't\": \"does not\",\n    \"didn't\": \"did not\",\n    \"hasn't\": \"has not\",\n    \"haven't\": \"have not\",\n    \"hadn't\": \"had not\",\n    \"won't\": \"will not\",\n    \"wouldn't\": \"would not\",\n    \"can't\": \"can not\",\n    \"cannot\": \"can not\",\n    \"i'm\": \"i am\",\n    \"m\": \"am\",\n    \"i'll\" : \"i will\",\n    \"its\" : \"it is\",\n    \"it's\" : \"it is\",\n    \"'s\" : \" is\",\n    \"that's\" : \"that is\",\n    \"weren't\" : \"were not\",\n}\n\nkeys = [i for i in repl.keys()]\n\nnew_train_data = []\nnew_test_data = []\nltr = train[\"comment_text\"].tolist()\nlte = test[\"comment_text\"].tolist()\nfor i in ltr:\n    arr = str(i).split()\n    xx = \"\"\n    for j in arr:\n        j = str(j).lower()\n        if j[:4] == 'http' or j[:3] == 'www':\n            continue\n        if j in keys:\n            # print(\"inn\")\n            j = repl[j]\n        xx += j + \" \"\n    new_train_data.append(xx)\nfor i in lte:\n    arr = str(i).split()\n    xx = \"\"\n    for j in arr:\n        j = str(j).lower()\n        if j[:4] == 'http' or j[:3] == 'www':\n            continue\n        if j in keys:\n            # print(\"inn\")\n            j = repl[j]\n        xx += j + \" \"\n    new_test_data.append(xx)\ntrain[\"new_comment_text\"] = new_train_data\ntest[\"new_comment_text\"] = new_test_data\n\ntrate = train[\"new_comment_text\"].tolist()\ntete = test[\"new_comment_text\"].tolist()\nfor i, c in enumerate(trate):\n    trate[i] = re.sub('[^a-zA-Z ?!]+', '', str(trate[i]).lower())\nfor i, c in enumerate(tete):\n    tete[i] = re.sub('[^a-zA-Z ?!]+', '', tete[i])\ntrain[\"comment_text\"] = trate\ntest[\"comment_text\"] = tete\ndel trate, tete\ntrain.drop([\"new_comment_text\"], axis=1, inplace=True)\ntest.drop([\"new_comment_text\"], axis=1, inplace=True)",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "f8417452-7065-41e4-a796-0ee6b2ed9869",
        "_uuid": "6474a26bbf591a30e8f6baf58feb20334bb48846",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "# repl = {\n#     \"yay!\": \" good \",\n#     \"yay\": \" good \",\n#     \"yaay\": \" good \",\n#     \"yaaay\": \" good \",\n#     \"yaaaay\": \" good \",\n#     \"yaaaaay\": \" good \",\n#     \":/\": \" bad \",\n#     \":&gt;\": \" sad \",\n#     \":')\": \" sad \",\n#     \":-(\": \" frown \",\n#     \":(\": \" frown \",\n#     \":s\": \" frown \",\n#     \":-s\": \" frown \",\n#     \"&lt;3\": \" heart \",\n#     \":d\": \" smile \",\n#     \":p\": \" smile \",\n#     \":dd\": \" smile \",\n#     \"8)\": \" smile \",\n#     \":-)\": \" smile \",\n#     \":)\": \" smile \",\n#     \";)\": \" smile \",\n#     \"(-:\": \" smile \",\n#     \"(:\": \" smile \",\n#     \":/\": \" worry \",\n#     \":&gt;\": \" angry \",\n#     \":')\": \" sad \",\n#     \":-(\": \" sad \",\n#     \":(\": \" sad \",\n#     \":s\": \" sad \",\n#     \":-s\": \" sad \",\n#     r\"\\br\\b\": \"are\",\n#     r\"\\bu\\b\": \"you\",\n#     r\"\\bhaha\\b\": \"ha\",\n#     r\"\\bhahaha\\b\": \"ha\",\n#     r\"\\bdon't\\b\": \"do not\",\n#     r\"\\bdoesn't\\b\": \"does not\",\n#     r\"\\bdidn't\\b\": \"did not\",\n#     r\"\\bhasn't\\b\": \"has not\",\n#     r\"\\bhaven't\\b\": \"have not\",\n#     r\"\\bhadn't\\b\": \"had not\",\n#     r\"\\bwon't\\b\": \"will not\",\n#     r\"\\bwouldn't\\b\": \"would not\",\n#     r\"\\bcan't\\b\": \"can not\",\n#     r\"\\bcannot\\b\": \"can not\",\n#     r\"\\bi'm\\b\": \"i am\",\n#     \"m\": \"am\",\n#     \"r\": \"are\",\n#     \"u\": \"you\",\n#     \"haha\": \"ha\",\n#     \"hahaha\": \"ha\",\n#     \"don't\": \"do not\",\n#     \"doesn't\": \"does not\",\n#     \"didn't\": \"did not\",\n#     \"hasn't\": \"has not\",\n#     \"haven't\": \"have not\",\n#     \"hadn't\": \"had not\",\n#     \"won't\": \"will not\",\n#     \"wouldn't\": \"would not\",\n#     \"can't\": \"can not\",\n#     \"cannot\": \"can not\",\n#     \"i'm\": \"i am\",\n#     \"m\": \"am\",\n#     \"i'll\" : \"i will\",\n#     \"its\" : \"it is\",\n#     \"it's\" : \"it is\",\n#     \"'s\" : \" is\",\n#     \"that's\" : \"that is\",\n#     \"weren't\" : \"were not\",\n# }\n\n# keys = [i for i in repl.keys()]\n\n# new_train_data = []\n# new_test_data = []\n# ltr = train[\"comment_text\"].tolist()\n# lte = test[\"comment_text\"].tolist()\n# for i in ltr:\n#     arr = str(i).split()\n#     xx = \"\"\n#     for j in arr:\n#         j = str(j).lower()\n#         if j[:4] == 'http' or j[:3] == 'www':\n#             continue\n#         if j in keys:\n#             # print(\"inn\")\n#             j = repl[j]\n#         xx += j + \" \"\n#     new_train_data.append(xx)\n# for i in lte:\n#     arr = str(i).split()\n#     xx = \"\"\n#     for j in arr:\n#         j = str(j).lower()\n#         if j[:4] == 'http' or j[:3] == 'www':\n#             continue\n#         if j in keys:\n#             # print(\"inn\")\n#             j = repl[j]\n#         xx += j + \" \"\n#     new_test_data.append(xx)\n# train[\"new_comment_text\"] = new_train_data\n# test[\"new_comment_text\"] = new_test_data\n\n# trate = train[\"new_comment_text\"].tolist()\n# tete = test[\"new_comment_text\"].tolist()\n# for i, c in enumerate(trate):\n#     trate[i] = re.sub('[^a-zA-Z ?!]+', '', str(trate[i]).lower())\n# for i, c in enumerate(tete):\n#     tete[i] = re.sub('[^a-zA-Z ?!]+', '', tete[i])\n# train[\"comment_text\"] = trate\n# test[\"comment_text\"] = tete\n# del trate, tete\n# train.drop([\"new_comment_text\"], axis=1, inplace=True)\n# test.drop([\"new_comment_text\"], axis=1, inplace=True)\n\n# train_text = train['comment_text']\n# test_text = test['comment_text']",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "9bcb79f0-15ff-4b28-8167-6eb642a99739",
        "_uuid": "cd5f946b7380530bec94a780000786fb3a9897f9",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "train_text = train['comment_text']\ntest_text = test['comment_text']\nall_text = pd.concat([train_text, test_text])",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "b167a42d-e4b3-4fb0-81cd-74b52889129e",
        "_uuid": "a4761b2ef10adcae4413455d7396ebc7160f2727",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "import re, string\nre_tok = re.compile(f'([{string.punctuation}“”¨«»®´·º½¾¿¡§£₤‘’])')\ndef tokenize(s): return re_tok.sub(r' \\1 ', s).split()",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "c74cbaa6-dc79-4c25-ad39-2017a7f3f0c5",
        "_uuid": "d6183cee82fd9e429445f64ce912493a72f6b815",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "# train_word_n = train['comment_text'].apply(lambda x: len(x.split(' '))).values.reshape(len(train), 1)\n# test_word_n = test['comment_text'].apply(lambda x: len(x.split(' '))).values.reshape(len(test), 1)\n\n# word_n = np.append(train_word_n, test_word_n)\n# wnmean = word_n.mean()\n# wnstd = word_n.std()\n\n# train_word_nn = (train_word_n - wnmean) / wnstd\n# test_word_nn = (test_word_n - wnmean) / wnstd",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "752652a7-5e0e-441d-a208-7be303e160ae",
        "_uuid": "83daa58be09f103864f9afdc53533bb8d1b8a5d7",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "cont_patterns = [\n        (b'US', b'United States'),\n        (b'IT', b'Information Technology'),\n        (b'(W|w)on\\'t', b'will not'),\n        (b'(C|c)an\\'t', b'can not'),\n        (b'(I|i)\\'m', b'i am'),\n        (b'(A|a)in\\'t', b'is not'),\n        (b'(\\w+)\\'ll', b'\\g<1> will'),\n        (b'(\\w+)n\\'t', b'\\g<1> not'),\n        (b'(\\w+)\\'ve', b'\\g<1> have'),\n        (b'(\\w+)\\'s', b'\\g<1> is'),\n        (b'(\\w+)\\'re', b'\\g<1> are'),\n        (b'(\\w+)\\'d', b'\\g<1> would'),\n    ]\npatterns = [(re.compile(regex), repl) for (regex, repl) in cont_patterns]\n\n\ndef prepare_for_char_n_gram(text):\n    \"\"\" Simple text clean up process\"\"\"\n    # 1. Go to lower case (only good for english)\n    # Go to bytes_strings as I had issues removing all \\n in r\"\"\n    clean = bytes(text.lower(), encoding=\"utf-8\")\n    # 2. Drop \\n and  \\t\n    clean = clean.replace(b\"\\n\", b\" \")\n    clean = clean.replace(b\"\\t\", b\" \")\n    clean = clean.replace(b\"\\b\", b\" \")\n    clean = clean.replace(b\"\\r\", b\" \")\n    # 3. Replace english contractions\n    for (pattern, repl) in patterns:\n        clean = re.sub(pattern, repl, clean)\n    # 4. Drop puntuation\n    # I could have used regex package with regex.sub(b\"\\p{P}\", \" \")\n    exclude = re.compile(b'[%s]' % re.escape(bytes(string.punctuation, encoding='utf-8')))\n    clean = b\" \".join([exclude.sub(b'', token) for token in clean.split()])\n    # 5. Drop numbers - as a scientist I don't think numbers are toxic ;-)\n    clean = re.sub(b\"\\d+\", b\" \", clean)\n    # 6. Remove extra spaces - At the end of previous operations we multiplied space accurences\n    clean = re.sub(b'\\s+', b' ', clean)\n    # Remove ending space if any\n    clean = re.sub(b'\\s+$', b'', clean)\n    # 7. Now replace words by words surrounded by # signs\n    # e.g. my name is bond would become #my# #name# #is# #bond#\n    # clean = re.sub(b\"([a-z]+)\", b\"#\\g<1>#\", clean)\n    clean = re.sub(b\" \", b\"# #\", clean)  # Replace space\n    clean = b\"#\" + clean + b\"#\"  # add leading and trailing #\n\n    return str(clean, 'utf-8')\n\ndef count_regexp_occ(regexp=\"\", text=None):\n    \"\"\" Simple way to get the number of occurence of a regex\"\"\"\n    return len(re.findall(regexp, text))",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "8b639726-ad05-42c2-9626-bf2dd0773ca3",
        "_uuid": "7c4d1169c34c3fa788edc3b4f4d3510e22bdda74",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "def get_indicators_and_clean_comments(df):\n    \"\"\"\n    Check all sorts of content as it may help find toxic comment\n    Though I'm not sure all of them improve scores\n    \"\"\"\n    # Count number of \\n\n#     df[\"ant_slash_n\"] = df[\"comment_text\"].apply(lambda x: count_regexp_occ(r\"\\n\", x))\n    # Get length in words and characters\n    df[\"raw_word_len\"] = df[\"comment_text\"].apply(lambda x: len(x.split()))\n    df[\"raw_char_len\"] = df[\"comment_text\"].apply(lambda x: len(x))\n    # TODO chars per row\n    # Check number of upper case, if you're angry you may write in upper case\n    df[\"nb_upper\"] = df[\"comment_text\"].apply(lambda x: count_regexp_occ(r\"[A-Z]\", x))\n    # Number of F words - f..k contains folk, fork,\n    df[\"nb_fk\"] = df[\"comment_text\"].apply(lambda x: count_regexp_occ(r\"[Ff]\\S{2}[Kk]\", x))\n    # Number of S word\n    df[\"nb_sk\"] = df[\"comment_text\"].apply(lambda x: count_regexp_occ(r\"[Ss]\\S{2}[Kk]\", x))\n    # Number of D words\n    df[\"nb_dk\"] = df[\"comment_text\"].apply(lambda x: count_regexp_occ(r\"[dD]ick\", x))\n    # Number of occurence of You, insulting someone usually needs someone called : you\n    df[\"nb_you\"] = df[\"comment_text\"].apply(lambda x: count_regexp_occ(r\"\\W[Yy]ou\\W\", x))\n    # Just to check you really refered to my mother ;-)\n    df[\"nb_mother\"] = df[\"comment_text\"].apply(lambda x: count_regexp_occ(r\"\\Wmother\\W\", x))\n    # Just checking for toxic 19th century vocabulary\n    df[\"nb_ng\"] = df[\"comment_text\"].apply(lambda x: count_regexp_occ(r\"\\Wnigger\\W\", x))\n    # Some Sentences start with a <:> so it may help\n    df[\"start_with_columns\"] = df[\"comment_text\"].apply(lambda x: count_regexp_occ(r\"^\\:+\", x))\n    # Check for time stamp\n    df[\"has_timestamp\"] = df[\"comment_text\"].apply(lambda x: count_regexp_occ(r\"\\d{2}|:\\d{2}\", x))\n    # Check for dates 18:44, 8 December 2010\n    df[\"has_date_long\"] = df[\"comment_text\"].apply(lambda x: count_regexp_occ(r\"\\D\\d{2}:\\d{2}, \\d{1,2} \\w+ \\d{4}\", x))\n    # Check for date short 8 December 2010\n    df[\"has_date_short\"] = df[\"comment_text\"].apply(lambda x: count_regexp_occ(r\"\\D\\d{1,2} \\w+ \\d{4}\", x))\n    # Check for http links\n#     df[\"has_http\"] = df[\"comment_text\"].apply(lambda x: count_regexp_occ(r\"http[s]{0,1}://\\S+\", x))\n    # check for mail\n    df[\"has_mail\"] = df[\"comment_text\"].apply(\n        lambda x: count_regexp_occ(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+', x)\n    )\n    # Looking for words surrounded by == word == or \"\"\"\" word \"\"\"\"\n    df[\"has_emphasize_equal\"] = df[\"comment_text\"].apply(lambda x: count_regexp_occ(r\"\\={2}.+\\={2}\", x))\n    df[\"has_emphasize_quotes\"] = df[\"comment_text\"].apply(lambda x: count_regexp_occ(r\"\\\"{4}\\S+\\\"{4}\", x))\n\n    # Now clean comments\n    df[\"clean_comment\"] = df[\"comment_text\"].apply(lambda x: prepare_for_char_n_gram(x))\n\n    # Get the new length in words and characters\n    df[\"clean_word_len\"] = df[\"clean_comment\"].apply(lambda x: len(x.split()))\n    df[\"clean_char_len\"] = df[\"clean_comment\"].apply(lambda x: len(x))\n    # Number of different characters used in a comment\n    # Using the f word only will reduce the number of letters required in the comment\n    df[\"clean_chars\"] = df[\"clean_comment\"].apply(lambda x: len(set(x)))\n    df[\"clean_chars_ratio\"] = df[\"clean_comment\"].apply(lambda x: len(set(x))) / df[\"clean_comment\"].apply(\n        lambda x: 1 + min(99, len(x)))",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "7f34d086-1f52-4632-96b6-76d617cb410e",
        "_uuid": "2e532d3bcd0c30a312e61d5172836c72938b6d34",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "for df in [train, test]:\n   get_indicators_and_clean_comments(df)",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "331f0c62-b16e-4157-8b6f-016934510f49",
        "_uuid": "0ffa3c96072f297c8991a4ccd9e641a793701f13",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "num_features = [f_ for f_ in train.columns\n                if f_ not in [\"comment_text\", \"clean_comment\", \"id\", \"remaining_chars\", 'has_ip_address'] + class_names]\n\n# TODO: normalize\nfor f in num_features:\n    all_cut = pd.cut(pd.concat([train[f], test[f]], axis=0), bins=20, labels=False, retbins=False)\n    train[f] = all_cut.values[:train.shape[0]]\n    test[f] = all_cut.values[train.shape[0]:]\n\ntrain_num_features = train[num_features].values\ntest_num_features = test[num_features].values",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "558ef8bf-239f-4cbe-9239-8b4b69f8abec",
        "_uuid": "868c11ce2e8611cf1ddca015fe111d115f869d02",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "train_text = train['clean_comment'].fillna(\"\")\ntest_text = test['clean_comment'].fillna(\"\")\nall_text = pd.concat([train_text, test_text])",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "2cc07f31-d13b-4022-9bc5-401ec87504f3",
        "_uuid": "d342f73c05255f7f6d6c7ba56ec3fea2cc271eba",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "word_vectorizer = TfidfVectorizer(\n        sublinear_tf=True,\n        strip_accents='unicode',\n        tokenizer=lambda x: regex.findall(r'[^\\p{P}\\W]+', x),\n        analyzer='word',\n        token_pattern=None,\n        ngram_range=(1, 2),\n        max_features=20000) # TODO: maybe more\n\n# word_vectorizer = TfidfVectorizer(sublinear_tf=True,\n#                                   strip_accents='unicode',\n#                                   analyzer='word',\n#                                   token_pattern=r'\\w{1,}',\n#                                   ngram_range=(1,2),\n#                                   max_features=30000)\n\n# word_vectorizer = TfidfVectorizer(ngram_range=(1,2), tokenizer=tokenize,\n#                min_df=3, max_df=0.9, strip_accents='unicode', use_idf=1,\n#                smooth_idf=1, sublinear_tf=1 )",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "7f91b6ae-65a4-4630-9014-d26b81b60506",
        "_uuid": "e5173ed2fb4cfda15c12ff36fa4a769e9cec7cf7",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "word_vectorizer.fit(all_text)",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "3132cbf7-55f0-42bb-bde5-bdc149083caa",
        "_uuid": "245deb2db7068aaf15b626216d59a5f2ff901c75",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "train_word_features = word_vectorizer.transform(train_text)\ntest_word_features = word_vectorizer.transform(test_text)",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "85c3bb4b-53cd-4340-bb33-986417d35e18",
        "_uuid": "388a357633cb8705b0d327eac91f6b621d2002b5",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "def char_analyzer(text):\n    \"\"\"\n    This is used to split strings in small lots\n    I saw this in an article (I can't find the link anymore)\n    so <talk> and <talking> would have <Tal> <alk> in common\n    \"\"\"\n    tokens = text.split()\n    return [token[i: i + 3] for token in tokens for i in range(len(token) - 2)]",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "2ea29b1a-af70-468b-b0eb-9ebeb9d88ade",
        "_uuid": "aa9d1d441bc1c1252ad1bdfc5757bd06d1973bf4",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "char_vectorizer = TfidfVectorizer(\n        sublinear_tf=True,\n        strip_accents='unicode',\n        tokenizer=char_analyzer,\n        analyzer='word',\n        ngram_range=(1, 3),\n        max_df=0.9,\n        max_features=60000) #50k\nchar_vectorizer.fit(all_text)\ntrain_char_features = char_vectorizer.transform(train_text)\ntest_char_features = char_vectorizer.transform(test_text)",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "fe2159ab-8845-4ece-acc8-855073b623c8",
        "_uuid": "c4d192bc17efb69e94717fde34fc42a07ec58a3e",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "train_features = hstack([train_word_features, train_links_n, train_char_features, train_num_features]).tocsr()\ntest_features = hstack([test_word_features, test_links_n, test_char_features, test_num_features]).tocsr()",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "7b37c043-dd80-4322-9d7a-bd5d108ca1ec",
        "_uuid": "0c2f281a1956320bd79575ac12338875498929b9",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "print(train_features.shape)\nprint(test_features.shape)",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "8a1fb889-7b6c-4911-9514-407b68bfec6c",
        "_uuid": "a7522932404d44ab605995f6e34d6a6aa0b1c529",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "all_parameters = {\n                  'C'             : [1.048113, 0.1930, 0.596362, 0.25595, 0.449843, 0.25595],\n                  'tol'           : [0.1, 0.1, 0.046416, 0.0215443, 0.1, 0.01],\n                  'solver'        : ['lbfgs', 'newton-cg', 'lbfgs', 'newton-cg', 'newton-cg', 'lbfgs'],\n                  'fit_intercept' : [True, True, True, True, True, True],\n                  'penalty'       : ['l2', 'l2', 'l2', 'l2', 'l2', 'l2'],\n                  'class_weight'  : [None, 'balanced', 'balanced', 'balanced', 'balanced', 'balanced'],\n                 }",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "f8046eac-233b-4805-92d8-15d621cc4c8f",
        "_uuid": "24ba6d0e41abe0a336936fac3cbe23308a6b627e",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "# scores= []\n\n# for j, class_name in enumerate(class_names):\n#     classifier = LogisticRegression(\n#         C=all_parameters['C'][j],\n#         max_iter=200,\n#         tol=all_parameters['tol'][j],\n#         solver=all_parameters['solver'][j],\n#         fit_intercept=all_parameters['fit_intercept'][j],\n#         penalty=all_parameters['penalty'][j],\n#         dual=False,\n#         class_weight=all_parameters['class_weight'][j],\n#         verbose=0)\n\n#     train_target = train[class_name]\n\n#     cv_score = np.mean(cross_val_score(classifier, train_features, train_target, scoring='roc_auc'))\n    \n#     print('CV score for class {} is {}'.format(class_name, cv_score))\n#     scores.append(cv_score)\n\n# print('Total score is {}'.format(np.mean(scores)))",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "43e07a14-9fbb-4895-b6d5-082a3a27095d",
        "_uuid": "fdd999b422f6d96667e064cb893c00015b98660e",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "submission = pd.DataFrame.from_dict({'id': test['id']})",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "87087fd0-3336-4c05-b262-270cc4aa4fa2",
        "_uuid": "8a08272dc1dc0a67ac3bed50c64c5021dd86ff61",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "for j, class_name in enumerate(class_names):\n    classifier = LogisticRegression(\n        C=all_parameters['C'][j],\n        max_iter=200,\n        tol=all_parameters['tol'][j],\n        solver=all_parameters['solver'][j],\n        fit_intercept=all_parameters['fit_intercept'][j],\n        penalty=all_parameters['penalty'][j],\n        dual=False,\n        class_weight=all_parameters['class_weight'][j],\n        verbose=0)\n\n    train_target = train[class_name]\n    classifier.fit(train_features, train_target)\n    submission[class_name] = classifier.predict_proba(test_features)[:, 1]\n    print(class_name)",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "ec325bab-caed-471e-8c60-490fdda3e041",
        "_uuid": "f0e0afcf7438dfc6ce0411495ec7c612221e904a",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "submission.to_csv('submission.csv', index=False)",
      "execution_count": null,
      "outputs": []
    },
    {
      "metadata": {
        "_cell_guid": "d3a052bc-6180-41d7-9e1a-14ddd1dabb85",
        "_uuid": "cd1ad1a5d7da0cec4d1b1e2544a9ae2c6064e8a1",
        "collapsed": true,
        "trusted": false
      },
      "cell_type": "code",
      "source": "",
      "execution_count": null,
      "outputs": []
    }
  ],
  "metadata": {
    "language_info": {
      "mimetype": "text/x-python",
      "name": "python",
      "nbconvert_exporter": "python",
      "version": "3.6.4",
      "codemirror_mode": {
        "version": 3,
        "name": "ipython"
      },
      "file_extension": ".py",
      "pygments_lexer": "ipython3"
    },
    "kernelspec": {
      "display_name": "Python 3",
      "language": "python",
      "name": "python3"
    }
  },
  "nbformat": 4,
  "nbformat_minor": 1
}
