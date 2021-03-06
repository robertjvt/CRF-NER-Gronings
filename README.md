# NER for Gronings
<b>About</b>

Named entity recognition based on Conditional Random Fields model for the regional language Gronings. Developed for my bachelor thesis in Information Science at the Rijksuniversiteit Groningen.


<b>Evaluation</b>

To evaluate the trained model I used precision, recall and f1-score. Ultimately the macro average of the f1-score is mostly used to estimate how well the model performs.

<i>Model</i>
| Label | Precision | Recall | F1-score | Support |
| ----- | --------- | ------ | -------- | ------- |
| O     | 0.996     | 0.998  | 0.997    | 29643   |
| B-LOC | 0.748     | 0.705  | 0.726    | 122     |
| I-LOC | 0.650     | 0.464  | 0.542    | 28      |
| B-MISC| 0.800     | 0.623  | 0.701    | 77      |
| I-MISC| 0.857     | 0.353  | 0.500    | 17      |
| B-ORG | 1.000     | 0.429  | 0.600    | 14      |
| I-ORG | 0.500     | 0.083  | 0.143    | 12      |
| B-PER | 0.926     | 0.933  | 0.929    | 507     |
| I-PER | 0.808     | 0.685  | 0.741    | 92      |
| |
| accuracy     |    |          | 0.992    | 30512   |
| macro avg    | 0.809 | 0.586 | <b>0.653</b>    | 30512   |
| weighted avg | 0.992 | 0.992 | 0.992    | 30512   |

<i>Model with hyperparameter optimization</i>
| Label | Precision | Recall | F1-score | Support |
| ----- | --------- | ------ | -------- | ------- |
| O     | 0.996     | 0.998  | 0.997    | 29643   |
| B-LOC | 0.730     | 0.689  | 0.709    | 122     |
| I-LOC | 0.632     | 0.429  | 0.511    | 28      |
| B-MISC| 0.742     | 0.636  | 0.685    | 77      |
| I-MISC| 0.667     | 0.353  | 0.462    | 17      |
| B-ORG | 1.000     | 0.429  | 0.600    | 14      |
| I-ORG | 0.500     | 0.083  | 0.143    | 12      |
| B-PER | 0.929     | 0.923  | 0.926    | 507     |
| I-PER | 0.886     | 0.674  | 0.765    | 92      |
| |
| accuracy     |    |          | 0.992    | 30512   |
| macro avg    | 0.787 | 0.579 | <b>0.644</b>    | 30512   |
| weighted avg | 0.992 | 0.992 | 0.992    | 30512   |


<b>Features used</b>
- Bias
- The word itself
- Whether the word's first letter is uppercase
- Whether the word is entirely uppercase
- Whether the word consists only of digits
- The shape of the word
- The suffix of the word (last 3 and last 2 letters)
- The prefix of the word (first 3 and first 2 letters)
- Whether the word exists in a gazetteer
- Whether the word is at the beginning or end of the sentence
- The word(s) before and after the word
- Whether the word(s) before/after first letter are uppercase
- Whether the word(s) before/after are entirely uppercase
- Whether the word(s) before/after consists only of digits
- Whether the word(s) before/after are punctuation tokens.


<b>Possible (future) to-do's</b>

- Retrain model on data with POS tags.
- Retrain model on more/better annotated data.
- Retrieve names of organizations in The Netherlands/Groningen from KVK.
