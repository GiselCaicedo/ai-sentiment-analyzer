**STUDENT PROJECT  
SCENARIOS**

*Industry-oriented project assignments for students*

| **Subject Areas**   | Data Analytics, Version Control and Generative AI |
| ------------------- | ------------------------------------------------- |
| **Project Options** | 20 scenario-based projects                        |
| **Suggested Level** | Beginner to Advanced                              |

# About This Assignment Pack

This document contains practical, real-world project scenarios designed to help students apply programming, data analysis, version control and generative AI concepts. Students should focus on understanding the problem, implementing a working solution, testing the result and explaining their approach during a project demonstration.

## Learning Areas

  - NumPy and Pandas for numerical computing, data cleaning, analysis and reporting.

  - Git and GitHub for version control, collaboration, branching and project deployment.

  - Large Language Models (LLMs) for text generation, summarization, question answering and analysis.

  - Diffusion models for text-to-image and image-to-image generation.

  - Multimodal AI for working with combinations of text, images, audio and documents.

  - OpenAI and Hugging Face models for integrating pretrained AI capabilities into applications.

# Section 1 – NumPy & Pandas: Data Analytics Projects

## Project 1: Student Performance Prediction and Analysis

**Scenario:** A college wants to identify students who may be at risk of failing semester examinations.

**Suggested technology:** Python, NumPy, Pandas, Matplotlib or Power BI

**Student tasks:**

  - Load student marks from a CSV file into a Pandas DataFrame.

  - Use NumPy to calculate average, maximum and minimum marks.

  - Identify students scoring below the required pass mark.

  - Calculate subject-wise pass percentages.

  - Prepare a student performance summary.

**Expected output:** A student performance analysis report or dashboard.

## Project 2: E-Commerce Sales Analysis

**Scenario:** An online shopping company wants to identify its best-selling products and strongest sales regions.

**Suggested technology:** Python, NumPy, Pandas, Matplotlib

**Student tasks:**

  - Import sales records from CSV files.

  - Calculate total revenue using quantity multiplied by unit price.

  - Find the top 10 products by revenue.

  - Perform monthly and region-wise sales analysis.

  - Identify products with low sales performance.

**Expected output:** An e-commerce sales analysis report with charts.

## Project 3: Hospital Patient Data Analysis

**Scenario:** A hospital wants to understand patient admission trends and department workloads.

**Suggested technology:** Python, NumPy, Pandas

**Student tasks:**

  - Load patient admission records into Pandas.

  - Calculate department-wise patient counts.

  - Identify months with the highest number of admissions.

  - Group patients by age range.

  - Generate statistical summaries while protecting patient privacy.

**Expected output:** A hospital analytics report using anonymized or sample data.

# Section 2 – Git & GitHub: Collaborative Development Projects

## Project 4: College Event Management System

**Scenario:** A team of students must develop a website for managing college events.

**Suggested technology:** Git, GitHub, HTML, CSS, JavaScript

**Student tasks:**

  - Create a shared GitHub repository.

  - Divide the application into modules among team members.

  - Create separate branches for assigned features.

  - Commit and push code with meaningful messages.

  - Create pull requests and review team members' code.

  - Resolve a practice merge conflict.

**Expected output:** A collaboratively developed event management application with commit history.

## Project 5: Student Portfolio Website

**Scenario:** Each student wants to create an online portfolio to showcase skills and projects.

**Suggested technology:** Git, GitHub, HTML, CSS, JavaScript

**Student tasks:**

  - Build a portfolio using HTML, CSS and JavaScript.

  - Track code changes using Git.

  - Upload the project to a GitHub repository.

  - Create a branch for a new feature and merge it.

  - Deploy the website using GitHub Pages.

**Expected output:** A live portfolio website with a public GitHub repository.

# Section 3 – LLMs: Large Language Model Projects

## Project 6: AI College Assistant Chatbot

**Scenario:** Students regularly ask questions about college timings, fees, examinations and holidays. The college needs a chatbot that answers from approved information.

**Suggested technology:** Python, OpenAI API or Hugging Face, Streamlit

**Student tasks:**

  - Prepare a small knowledge base containing sample college information.

  - Connect an OpenAI or Hugging Face language model.

  - Accept questions from students through a simple interface.

  - Generate answers grounded in the supplied information.

  - Show a fallback response when the answer is not available.

  - Test the chatbot with at least 10 questions.

**Expected output:** A chatbot that answers questions using the supplied college information.

## Project 7: AI Resume Analyzer

**Scenario:** An HR team receives many resumes and wants to compare candidate skills with a job description.

**Suggested technology:** Python, PDF text extraction, OpenAI or Hugging Face

**Student tasks:**

  - Upload a sample resume in PDF or text format.

  - Extract resume text.

  - Send the resume and job description to an LLM.

  - Identify skills, education and experience mentioned in the resume.

  - Generate a structured comparison and improvement suggestions.

  - Include a note that the tool supports, but does not replace, human recruitment decisions.

**Expected output:** A resume analysis report with extracted skills and a job-match summary.

## Project 8: AI Notes Summarizer

**Scenario:** Students have lengthy study materials and want concise revision notes.

**Suggested technology:** Python, PDF extraction, OpenAI or Hugging Face

**Student tasks:**

  - Upload a text or PDF study document.

  - Extract and clean the document text.

  - Send manageable text sections to an LLM.

  - Generate a short summary and key points.

  - Generate practice questions from the supplied material.

  - Allow the student to review the generated output.

**Expected output:** A study assistant that creates summaries and revision questions.

# Section 4 – Diffusion Models: AI Image Generation Projects

A diffusion model learns to generate images by progressively removing noise from a noisy input during generation. Students can experiment with text prompts and pretrained image-generation models.

## Project 9: AI Text-to-Image Generator

**Scenario:** An advertising team wants to create concept images from written descriptions.

**Suggested technology:** Python, Hugging Face Diffusers, a suitable GPU or hosted inference service

**Student tasks:**

  - Accept a text prompt from the user.

  - Connect to an available pretrained diffusion model through Hugging Face.

  - Generate an image from the prompt.

  - Display the generated image in the application.

  - Allow the user to save the result and record the prompt.

**Expected output:** A simple text-to-image generation application.

## Project 10: AI Product Advertisement Generator

**Scenario:** An e-commerce seller wants to create promotional concepts for products.

**Suggested technology:** Python, Hugging Face Diffusers, OpenAI or Hugging Face LLM

**Student tasks:**

  - Accept a product name and short description.

  - Use a diffusion model to generate a suitable promotional background or concept image.

  - Use an LLM to draft a marketing caption.

  - Combine the generated visual and caption in a preview.

  - Clearly label generated images as AI-created.

**Expected output:** A product advertisement concept generator.

## Project 11: AI Interior Design Generator

**Scenario:** A homeowner wants to explore possible room styles before planning a renovation.

**Suggested technology:** Python, Hugging Face Diffusers, image-to-image model

**Student tasks:**

  - Use a sample room image or an image supplied with permission.

  - Accept a style prompt such as modern, minimal or traditional.

  - Use an image-to-image diffusion workflow where available.

  - Generate a redesigned room concept.

  - Display the original and generated images for comparison.

**Expected output:** An interior design concept application.

# Section 5 – Multimodal AI: Text, Image, Audio and Documents

## Project 12: AI Image Question Answering System

**Scenario:** A student wants to ask questions about an image and receive a text explanation.

**Suggested technology:** Python, OpenAI vision-capable model or Hugging Face vision-language model

**Student tasks:**

  - Allow the user to upload an image.

  - Connect a suitable vision-language model.

  - Accept a question about the uploaded image.

  - Generate an answer based on visible image content.

  - Optionally convert the answer into speech.

  - Test the system with different everyday images.

**Expected output:** An image question-answering application.

## Project 13: AI Voice Assistant for Students

**Scenario:** Students want to ask study-related questions by speaking instead of typing.

**Suggested technology:** Python, speech-to-text, OpenAI or Hugging Face, text-to-speech

**Student tasks:**

  - Capture audio through a microphone with user permission.

  - Convert speech into text using a speech-recognition model or service.

  - Send the recognized question to an LLM.

  - Generate a response.

  - Convert the response into speech using text-to-speech.

  - Display both the recognized question and response.

**Expected output:** A voice-based student assistant.

## Project 14: AI Document Understanding System

**Scenario:** A business receives invoices and certificates and wants to extract key information.

**Suggested technology:** Python, OCR, Pandas, OpenAI or Hugging Face

**Student tasks:**

  - Upload a sample document or scanned image.

  - Use OCR or a vision-language model to read the content.

  - Extract fields such as document number, date and total amount.

  - Summarize the document.

  - Export extracted fields to CSV or Excel.

  - Allow the user to verify extracted values before using them.

**Expected output:** A document extraction and summarization application.

# Section 6 – OpenAI / Hugging Face Model Integration

## Project 15: AI Interview Coach

**Scenario:** A job applicant wants to practise interview questions and receive feedback.

**Suggested technology:** OpenAI API or Hugging Face LLM

**Student tasks:**

  - Conduct a mock interview, generate role-specific questions, accept typed answers, and provide structured feedback.

**Expected output:** A mock interview practice application.

## Project 16: AI Code Explainer

**Scenario:** A beginner wants difficult Python code explained in simple language.

**Suggested technology:** OpenAI API or Hugging Face LLM

**Student tasks:**

  - Accept a code snippet, ask an LLM to explain it line by line, identify likely errors, and suggest a small example.

**Expected output:** A Python code explanation tool.

## Project 17: Language Translator

**Scenario:** Users need to translate short messages between Tamil, English and Hindi.

**Suggested technology:** Hugging Face Transformers

**Student tasks:**

  - Accept text and target language, use a suitable pretrained translation model, and display the translated result.

**Expected output:** A multilingual translation application.

## Project 18: AI News Summarizer

**Scenario:** A reader wants a short summary of a long news article supplied to the application.

**Suggested technology:** OpenAI API or Hugging Face LLM

**Student tasks:**

  - Accept article text or an authorized source, summarize key points, and display the summary with the original source reference.

**Expected output:** A news summarization tool.

## Project 19: AI Sentiment Analyzer

**Scenario:** A business wants to understand whether customer reviews are positive, negative or neutral.

**Suggested technology:** Hugging Face Transformers, Pandas

**Student tasks:**

  - Load sample reviews, use a pretrained sentiment model, classify each review, and calculate sentiment counts using Pandas.

**Expected output:** A customer feedback analysis report.

## Project 20: AI Question Generator

**Scenario:** A teacher wants to create practice questions from lesson notes.

**Suggested technology:** OpenAI API or Hugging Face LLM

**Student tasks:**

  - Accept lesson text, generate multiple-choice and short-answer questions, include suggested answers, and allow teacher review.

**Expected output:** A question-generation application for study practice.

# Section 7 – Suggested Project Architecture

Students may use the following high-level architecture. The exact components depend on the project selected.

<table>
<thead>
<tr class="header">
<th><strong>FRONTEND<br />
</strong>HTML, CSS, JavaScript or Streamlit</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><strong>PYTHON APPLICATION<br />
</strong>Python, NumPy and Pandas</td>
</tr>
<tr class="even">
<td><strong>AI MODEL LAYER<br />
</strong>OpenAI API or Hugging Face models; diffusion or multimodal model when required</td>
</tr>
<tr class="odd">
<td><strong>DATA LAYER<br />
</strong>MySQL, CSV or Excel, depending on project needs</td>
</tr>
<tr class="even">
<td><strong>VERSION CONTROL<br />
</strong>Git and GitHub for source control and collaboration</td>
</tr>
</tbody>
</table>

# 

# 

# Important Notes for Students

  - Use sample, public or properly authorized datasets. Do not upload confidential personal, medical or company information.

  - Keep API keys private. Store secrets in environment variables and never commit them to GitHub.

  - Check model outputs for accuracy. AI-generated answers and images may contain errors.

  - Review generated content before submitting or publishing it.

  - Include a README file explaining the problem, setup steps, tools, features and limitations.

  - For team projects, each member should make meaningful commits and be able to explain their contribution.

# Student Submission Checklist

  - [ ] Project title and problem statement

  - [ ] Source code and requirements file

  - [ ] GitHub repository link

  - [ ] Dataset or sample input with source details

  - [ ] Screenshots of important outputs

  - [ ] Testing results and known limitations

  - [ ] Short project presentation or demonstration
