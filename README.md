# Wordle
My friends could play wordle and I couldn't so I wrote python code to beat them. You make a guess on wordle and write the feed the feedback you get from wordle onto the code!

## How to install
In your terminal write the following command. You must have python installed to run it.
```
pip3 install git+https://github.com/QuantumStatic/wordle
```

## Requirements
- Python 3.6+

## Runtime
Your first guess may take upto a minute but after that it's smooth sailing. 

## How to run
### Import statment
In your file import the wordle object from the wordle file as follows
```python
from Wordle import Wordle
```
### Driver Code
`add_try` function has to be used to add your guess. The function takes the guess you made and the feedback the [wordle website](https://www.powerlanguage.co.uk/wordle/) gave you. Following is an example of running a successful wordle where the final word is supposed to be '*tweet*'.
```python
wordle.add_try("outer", (-1, -1, 0, 1, -1))
```
Above line code means the word "outer" was the guess and the feedback is (-1, -1, 0, 1, -1). 
#### Creating Feedback
The letter 'o' *doesn't belong* in the final word, hence we give the value -1 ie. (**-1**, -1, 0, 1, -1). 
<br/>
The letter 'u' *doesn't belong* in the final word, hence we give the value -1 ie. (-1, **-1**, 0, 1, -1). 
<br/>
The letter 't' *belongs* in the final word but is *wrongly placed*, hence we give the value 0 i.e. (-1, -1, **0**, 1, -1). 
<br/>
The letter 'e' *belongs* in the final word and is *correctly placed* hence we give the value 1 i.e. (-1, -1, 0, **1**, -1). 
<br/>
The letter 'r' *doesn't belong* in the final word hence we give the value -1 ie. (-1, -1, 0, 1, **-1**).

### Making a Prediction using code
`make_a_suggestion` function needs to be used to let the code make a prediction. it would look something like this.
```python
wordle.make_a_suggestion(all_available_words = False, prediction = True)
```
if `all_available_words` is set to True, the code will print all the possible, by default it's set to False, i.e. to not print all available words.
<br/>
if `prediction` is set to False, the code will not make a prediction, by default it's set to True, i.e. to recommend a word.

## Example
Here is an example to guess the word '*tweet*' 
```python
from Wordle import Wordle

wordle = Wordle()
wordle.add_try("outer", (-1, -1, 0, 1, -1))
wordle.add_try("tepee", (1, 0, -1, 0, 0))
wordle.make_a_suggestion()
```
