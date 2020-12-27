## Welcome to Machine Learning Blogs
In this blog post, we will create a customized Albert (a lite Bert) language model from scratch using hugging face transformers on custom data set.

Since The Release of Bert, a pre-trained model by Google, language models have gained enormous attention in Natural Language Processing. We can use a language model to solve text-related downstream tasks like Text Classification, Named entity recognition, Text summarization, Question Answering Tasks, and Text Generation tasks.

### Language Modeling Techniques

The basic idea behind a language model is to learn a better and generalized representation for a language. Three common techniques have been used to train a language model i.e masked word prediction, next sentence prediction, and next-word prediction.

Bert uses Both Masked Word Prediction (Masking) and Next Sentence Prediction(NSP). Similarly, GPT-2 and GPT use Next Word Prediction to learn a generalized text representation. Albert and Roberta can also be trained using the same techniques.

In this article, we will learn how to create our language model (Albert) on our custom Data Set and custom language using the masked language modeling technique. You can apply similar code and technique on any other architecture like Bert, Roberta, Distill Bert, XLM-Roberta.

In the masked Language model, we will randomly mask 15% of tokens and our model will be trained to predict those 15% tokens.
Our loss function will be cross-entropy loss and it will only calculate the loss for masked tokens.

Let's say we have a sentence in English as: 

```markdown
I am going to train an Albert model on my custom data
```

We will transform it like 
```markdown
I am going <mask> train an Albert model <mask> my custom data
  
In the above case, we will train the model to predict masked tokens which are to, on.
```

### Why Albert? 
Albert (A lite bert) was released recently by Google, it focuses on reducing the parameters of Bert while achieving similar performance. Its results have been shared above.
We will be using Albert architecture as it has decreased parameters due to its sharing parameters capacity. Moreover, it has achieved better results on most of THE Natural Language Understanding tasks.

Let's start step by step,

### DataSet
We will use the ***Persian*** Language To train our Albert model. Create our custom data set in a text file in my case it is named ***Persian.txt***. ***Our data is stored in such a format that every sentence ends with a new line ‘\n’ character***.

Let's open our text file and see its contents
`with open('persian.txt','r') as txt_file:
     read_file = txt_file.readlines()
     print(read_file[:3])`
```markdown

ما امروز زبان فارسی را یاد خواهیم گرفت.
فارسی بیشتر توسط ایرانیان صحبت می شود.
ایران برای مسلمانان یک کشور تاریخی است.
```
It looks good.

### Create Tokenizer
After Preparing data in a text file, we will create a Tokenizer in our case it will be Sentence Piece Tokenizer. First of All, install the Sentence Piece dependency and import it. Let's train our Sentence Piece Tokenizer, here vocabulary size is important and it varies from language to language. The Original Albert Tokenizer has a vocabulary size of 32000. 

Note: Albert has some predefined tokens as well such as <PAD>, <UNK>, <sep>, </sep>, <CLS>, etc then final vocabulary size should include the special tokens as well. For Example, if the length of special tokens is 8, the vocabulary size should be 32008.

Let's install dependencies, 
`pip install transformers`
`pip install sentencepiece`

We have chosen a complete vocabulary size of 40000 for our language. We will train sentence piece tokenizer by keeping space of 10 tokens for Albert Special Tokens.
Note: If the vocabulary size is less than the number of words in your text file it will throw an exception to decrease your vocab size.

***model_prefix*** is the name by which sentencepiece tokenizer is saved in your current directory. By default, Tokenizer Library looks for ***spiece.model*** for loading sentence piece tokenizer so we will also use ***spiece*** as model_prefix.

```markdown
import sentencepiece as sp
sp.SentencePieceTrainer.train(input='persian.txt',model_prefix='spiece', vocab_size=39990)
#complete vocab size 40000
#39990 tokens of vocabulary for our custom data.
#40000-39990 for special tokens of albert
```

Once you run this code it will create a tokenizer and save it as ***spiece.model*** and ***spiece.vocab*** files.
Now create a directory as ***Persian_Model*** using following code and move ***spiece.model*** and spiece.vocab in ***Persian_Model***.

```markdown
import os
os.mkdir('Persian_Model')
os.rename('spiece.model','Persian_Model/spiece.model')
os.rename('spiece.vocab','Persian_Model/spiece.vocab')
```
Lets Import some necessary dependencies

`from transformers import AlbertForMaskedLM,AlbertConfig,AlbertTokenizer`

Lets load our created Tokenizer, it will add special tokens like 'PAD','MASK' etc that we did not add in our vocabulary.
`persian_tokenizer = AlbertTokenizer.from_pretrained('Persian_Model')`
 
Thats Great!
Now again save your model in same directory.
`persian_tokenizer.save_pretrained('Persian_Model')`

### Create DataLoader

As we have already prepared the data in text file there is not much work to do.
We need to load our sentences in tokenizer encoded format.
Just make sure that our sentences will be loaded using '\n' as separator
of sentences

```markdown
from transformers import LineByLineTextDataset
dataset = LineByLineTextDataset(
    tokenizer=persian_tokenizer,
    file_path="persian.txt",
    block_size=256,
)
```
block_size means number of tokens in a sequence. 

```markdown
from transformers import DataCollatorForLanguageModeling
data_collator = DataCollatorForLanguageModeling(tokenizer=persian_tokenizer,mlm=True, mlm_probability=0.15)
```
mlm_probability is the probability of tokens that are masked for each sequence,since we are using 15% masked tokens.

### Model Initilization
Next We will be initializing our model architecture that will act as backbone
of language model
We will be using Albert Large in this experiment.
lets initialize it from its default configuration

`config=AlbertConfig.from_pretrained('albert-large-v2')`

save this configuration in ***Persian_Model*** directory

`config.save_pretrained('Persian_Model')`

Now we can edit the parameters of this model to customize it but in our case we
will be modifying the vocab_size parameter from 32000 to 40000, as it is used
to initialize the embedding layer of model and save the config file.

lets Initialize our model from modified config.
`config=AlbertConfig.from_pretrained('Persian_Model')`
`persian_model = AlbertForMaskedLM(config=config)`
 
### Model Training

We can use Google Colaboratory for Training our model on its GPU.
We are all done with tokenization, dataset loading etc.
```markdown
from transformers import Trainer, TrainingArguments
batch_size=25
training_args = TrainingArguments(
    output_dir='persian_albert',
    overwrite_output_dir=True,
    num_train_epochs=3,
    learning_rate=5e-05,
    per_device_train_batch_size=batch_size,
    save_steps=len(data_set)/batch_size,
    save_total_limit=2,
    prediction_loss_only=True
)

trainer = Trainer(
    model=persian_model,
    args=training_args,
    data_collator=data_collator,
    train_dataset=dataset
    
)
 ```
Now call the .train function of trainer to start training our model. 
`trainer.train()`
 

Decrease the batch_size in case of cuda memory errors.
Once The training is complete, you are getting loss <1.0.
you have to save your Tokenizer again because trainer will only store model related files.

`persian_tokenizer.save_pretrained('persian_albert')`

Delete the unnecessary files like ***'optimizer.pt'*** file.
We have successfully created a persian language model, we can use it for our 
other tasks like Text Classification, Named Entity Recognition etc,Machine Translation etc.

In case of any query please write in comments.
Reference: HuggingFace
