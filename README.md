# NER for Gronings
<b>About</b>

Named entity recognition based on Conditional Random Fields model for the regional language Gronings. Developed for a bachelor thesis in Information Science at the Rijksuniversiteit Groningen.


<b>Evaluation</b>

<i>Model with 'O'</i>
| Label | Precision | Recall | F1-score | Support |
| ----- | --------- | ------ | -------- | ------- |
| O     | 0.996     | 0.998  | 0.997    | 29643   |
| B-LOC | 0.748     | 0.705  | 0.726    | 122     |
| I-LOC | 0.650     | 0.464  | 0.542    | 20      |

<i>Model without 'O'</i>
| Label | Precision | Recall | F1-score | Support |
| ----- | --------- | ------ | -------- | ------- |
| O     | 0.996     | 0.998  | 0.997    | 29643   |
| B-LOC | 0.748     | 0.705  | 0.726    | 122     |
| I-LOC | 0.650     | 0.464  | 0.542    | 20      |


<b>To-do's</b>
- Retrain model on data with POS tags.
- Retrain model on more/better annotated data.
- Retrieve names of organizations in The Netherlands/Groningen from KVK.
