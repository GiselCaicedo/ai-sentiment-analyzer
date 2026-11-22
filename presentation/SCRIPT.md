# Presentation script — AI Sentiment Analyzer

Simple English (B1–B2). About 10 minutes: 7–8 minutes of slides + 2–3 minutes of live demo.
Tip: speak slowly, and stop for one second after each number.

## Slide 1 — Cover

Good evening, everyone. My name is Gisel Caicedo, and today I will present my project for the Gen AI Bootcamp: Project 19, the AI Sentiment Analyzer.

The main idea is simple. A pretrained AI model can read customer reviews, decide if each one is positive, neutral or negative, and create a feedback report in a few seconds. And it gets the same answer as a human 86% of the time.

## Slide 2 — The problem

First, the problem. A café chain called Bean & Leaf wants to know what its customers think. Bean & Leaf is not a real company. I created it for this project.

I wrote 80 reviews in English, from August to November 2026. They talk about 8 products, with 10 reviews for each product.

Reading every review by hand takes a lot of time. Also, two people can read the same review in different ways. And when you read one review at a time, it is hard to see patterns, for example which product has more problems, or which month was worse.

So the goal is to classify every review automatically, count the results, and give the business a clear report. Each review also has a human label, so I can check if the model is right.

## Slide 3 — Objectives

These are the four tasks from the project brief.

One: load the sample reviews. I read the CSV file and remove empty or repeated reviews.

Two: use a pretrained sentiment model. "Pretrained" means someone already trained it. I don't need to train anything, and I don't need an API key.

Three: classify each review as positive, neutral or negative. The model also gives a confidence score from 0 to 1.

Four: count the results with Pandas, in total and by product. With these numbers, the program writes the final report.

## Slide 4 — Technologies

Here are the tools I used. All of them are free and open source.

Python runs everything. Hugging Face Transformers gives me the pretrained model. The model is called RoBERTa, and it has three labels: positive, neutral and negative. Pandas reads the data and counts the results. The web page uses simple HTML, CSS and JavaScript. GitHub Pages publishes the page, and pytest runs eight automatic tests.

An important point: the model runs on a normal laptop. It takes about four seconds to load, and one or two seconds to classify all 80 reviews. And because there are no API keys, there is nothing secret in GitHub.

## Slide 5 — Implementation

Now, how does it work inside? The main code is in one Python file, with five small functions. One function for each step.

First, load_reviews reads the CSV with Pandas. Second, get_model loads the Hugging Face pipeline. It loads the model only once and then reuses it. Third, classify adds two new columns to the table: the sentiment and the confidence. Fourth, summarize counts the results. Fifth, to_markdown writes the report.

Here you can see the Pandas part. value_counts counts how many reviews are positive, neutral and negative. Then I calculate the percentages. And crosstab makes a table of products and sentiments.

## Slide 6 — Deployment and demo

The project brief asks us to deploy on GitHub Pages or Vercel. My page is on GitHub Pages, at this link.

But there is a problem: GitHub Pages can only show files. It cannot run Python, and the model needs Python. The model also needs about 880 megabytes of memory, and the free cloud servers only give 512.

So my solution is this: the page is online, and the model runs on my laptop with a small Python server. The page sends the reviews to the server, and the server sends back the results. If the server is off, the page shows the last saved report.

Now let me show you how it works.

> **Live demo (2–3 minutes)**
> 1. Show the terminal with the server running.
> 2. Open the GitHub Pages link. Point to "Connected: the model is running on this PC."
> 3. Type a review, for example: *"The coffee was cold and the staff ignored me."* Click **Classify**. Say: "The model says negative, with high confidence."
> 4. Click **Add to dataset**. Say: "Now the review is saved in the CSV, and the report is calculated again. Look, the negative percentage went up."
> 5. Click **Download report**. Say: "This is the customer feedback report, the expected output of the project."

## Slide 7 — Results by product

Now, the results. In total, 51% of the reviews are positive, 26% are neutral and 23% are negative.

But the most interesting part is by product. Look at the red bars: they are the negative reviews. The sandwich has 6 negative reviews out of 10. That is one third of all the complaints. It is the only product with more negative reviews than positive ones. So, if I were the manager, the sandwich is the first thing I would fix.

On the other side, matcha and bagel have the most positive reviews.

## Slide 8 — Results by month

When we count by month, we can see something else. In August and September there were only 2 negative reviews per month. But in October there were 13. That is 72% of all the negative reviews.

Six of them are about sandwiches. And when I read them, several mention "the new staff" or "the new kitchen crew". So the problem probably started with the changes in the kitchen. In November, it goes back to only one negative review.

This is the kind of pattern that is very hard to see if you read the reviews one by one.

## Slide 9 — Model evaluation

The brief also says we must check if the model is accurate. Each review has a human label, so I compared them.

In this table, the rows are the human labels and the columns are the model's answers. The numbers on the diagonal are the correct answers. The model was right in 69 of 80 reviews. That is 86.2% accuracy.

The most interesting mistakes are sarcasm. For example: "Great, a lovely green drink that tastes just like dishwater." For a person, this is clearly negative. But the model sees the words "great" and "lovely" and says positive, with 98% confidence. The model also has problems with mixed reviews, which have something good and something bad.

## Slide 10 — Next steps

To finish, these are the limitations and my next steps.

First, the sample is small and I wrote it myself, so the next step is to test with real reviews. Second, the model only understands English, so I would like to use a multilingual model for Spanish. Third, to catch sarcasm, the program can mark reviews with one or two stars that the model calls positive, so a person can check them. And fourth, one review can talk about many things, like the coffee, the food and the service. In the future, the model could give a sentiment for each one.

To summarize: with a pretrained model and Pandas, a business can understand its customers in seconds. The project is working, it has 8 passing tests, and it is online on GitHub Pages.

Thank you for listening. I'm happy to answer your questions.

---

## Useful phrases for questions

- "That's a good question. Let me show you in the code."
- "I'm not sure, but I think…"
- "Could you repeat the question, please?"
- "In this project, I decided to… because…"

## Likely questions (short answers)

- **Why didn't you train your own model?** — The brief asks for a pretrained model. RoBERTa was already trained with millions of tweets, so it works well without training.
- **Where do you use Pandas?** — To read the CSV, clean it, count the sentiments with value_counts, make the product table with crosstab, and calculate the accuracy.
- **Why does the model need your laptop?** — GitHub Pages cannot run Python, and the free servers don't have enough memory for the model.
- **Why doesn't the accuracy change when you add a review?** — Because the new review has no human label, so there is nothing to compare.
