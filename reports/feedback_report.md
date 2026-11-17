# Bean & Leaf customer feedback report

Analyzed **80** reviews after dropping **0** blank or duplicate rows.

Model **cardiffnlp/twitter-roberta-base-sentiment-latest** · Generated 2026-11-17T23:35:56+00:00

## Sentiment breakdown

| Sentiment | Count | Share | Mean confidence |
| --- | ---: | ---: | ---: |
| Positive | 41 | 51.2% | 87.1% |
| Neutral | 21 | 26.2% | 76.7% |
| Negative | 18 | 22.5% | 76.3% |

## Sentiment by product

| Product | Positive | Neutral | Negative |
| --- | ---: | ---: | ---: |
| Bagel | 6 | 3 | 1 |
| Cold Brew | 6 | 2 | 2 |
| Croissant | 5 | 2 | 3 |
| Espresso | 5 | 3 | 2 |
| Latte | 5 | 3 | 2 |
| Matcha | 7 | 2 | 1 |
| Muffin | 5 | 4 | 1 |
| Sandwich | 2 | 2 | 6 |

## Monthly trend

| Month | Positive | Neutral | Negative |
| --- | ---: | ---: | ---: |
| 2026-08 | 9 | 5 | 2 |
| 2026-09 | 10 | 5 | 2 |
| 2026-10 | 11 | 7 | 13 |
| 2026-11 | 11 | 4 | 1 |

## What customers love

- “This was the best plain croissant I have had all month.” (review 35, 98.6% model confidence)
- “Wonderful, another blueberry muffin with exactly one blueberry.” (review 70, 98.4% model confidence)
- “I loved the peppery greens and the warm sourdough.” (review 72, 97.9% model confidence)

## What customers complain about

- “The bread was soggy and the filling was bland.” (review 75, 90.7% model confidence)
- “The new kitchen crew gave me the wrong sandwich twice.” (review 78, 90.5% model confidence)
- “It was so dry that I could not finish it.” (review 49, 88.6% model confidence)

## Evaluation

The model matched **86.2%** of the hand labels. It classified **21.7%** of 1–2 star reviews as positive or neutral.

| Reference / Predicted | Positive | Neutral | Negative |
| --- | ---: | ---: | ---: |
| Positive | 35 | 2 | 0 |
| Neutral | 4 | 16 | 0 |
| Negative | 2 | 3 | 18 |

### Misclassified reviews

- Review 28, Cold Brew (neutral → positive): “The drink was strong, which may suit some people.”
- Review 48, Bagel (neutral → positive): “I liked the spread but the bagel was a little tough.”
- Review 50, Bagel (negative → neutral): “The kitchen sent a plain bagel after I ordered sesame.”
- Review 57, Matcha (neutral → positive): “The matcha was stronger than the latte and lighter than the espresso.”
- Review 58, Matcha (negative → neutral): “The powder collected in lumps at the bottom.”
- Review 60, Matcha (negative → positive): “Great, a lovely green drink that tastes just like dishwater.”
- Review 61, Muffin (positive → neutral): “The blueberry muffin had real berries in every bite.”
- Review 64, Muffin (positive → neutral): “It was still warm and the chocolate pieces were melting.”
- Review 68, Muffin (neutral → positive): “The cake was a bit dense, but the topping was nice.”
- Review 70, Muffin (negative → positive): “Wonderful, another blueberry muffin with exactly one blueberry.”
- Review 76, Sandwich (negative → neutral): “I found an unripe tomato stem in the middle of my sandwich.”

## Limitations

The English model was trained on tweets. Sarcasm and mixed reviews can be difficult.
Accuracy describes this small, fictional dataset.
