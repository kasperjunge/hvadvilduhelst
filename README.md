# Hvad Vil Du Helst? (What Would You Rather?) - Danish Preference Dataset

A comprehensive dataset of Danish "Would You Rather" questions designed for evaluating Large Language Models (LLMs) in Danish language understanding and preference modeling.

## 🌟 Overview

This dataset contains a collection of Danish "Would You Rather" questions across various categories, making it an excellent resource for:
- Evaluating LLM performance in Danish language understanding
- Testing preference modeling capabilities
- Assessing cultural and linguistic nuances in Danish
- Benchmarking model responses to ethical and personal choice scenarios

## 📊 Dataset Structure

The dataset is organized into multiple categories, each containing carefully curated questions. Each entry includes:
- `questions`: The "Would You Rather" question in Danish
- `answer_A`: First choice option
- `answer_B`: Second choice option
- `category`: The thematic category of the question

### Categories Include:
- Arbejde (Work)
- Børn (Children)
- Dating
- Familie (Family)
- Film, Spil & TV
- Mad (Food)
- Musik
- Sport
- And many more...

## 🚀 Usage

### Loading the Dataset

```python
from datasets import load_dataset

# Load the dataset from Hugging Face
dataset = load_dataset("your-username/hygdk-dataset")
```

### Example Question

```python
{
    "questions": "Ville du helst arbejde hjemmefra hver dag eller aldrig arbejde hjemmefra?",
    "answer_A": "Arbejde hjemmefra hver dag",
    "answer_B": "Aldrig arbejde hjemmefra",
    "category": "arbejde"
}
```

## 🎯 Evaluation Use Cases

1. **Preference Modeling**
   - Test how well LLMs understand and predict human preferences
   - Evaluate consistency in preference modeling

2. **Cultural Understanding**
   - Assess model comprehension of Danish cultural context
   - Test understanding of local references and norms

3. **Ethical Decision Making**
   - Evaluate model responses to ethical dilemmas
   - Test consistency in moral reasoning

4. **Language Proficiency**
   - Assess Danish language understanding
   - Test comprehension of nuanced expressions

## 📈 Dataset Statistics

- Multiple categories covering diverse aspects of life
- Carefully curated questions to ensure quality and relevance
- Balanced representation of different types of choices
- Natural language variations in question formulation

## 🤝 Contributing

We welcome contributions to expand and improve the dataset! If you'd like to contribute:
1. Fork the repository
2. Add your questions in the appropriate category
3. Submit a pull request

## 📝 Citation

If you use this dataset in your research, please cite it as:

```bibtex
@misc{hygdk-dataset,
    author = {Your Name},
    title = {Hvad Vil Du Helst? - Danish Preference Dataset},
    year = {2024},
    publisher = {Hugging Face},
    url = {https://huggingface.co/datasets/your-username/hygdk-dataset}
}
```

## 📄 License

This dataset is released under the [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

## 🔗 Links

- [Dataset on Hugging Face](https://huggingface.co/datasets/your-username/hygdk-dataset)
- [GitHub Repository](https://github.com/your-username/hygdk-dataset)

## 🙏 Acknowledgments

This dataset is based on the "Hvad Vil Du Helst?" questions from [hyg.dk](https://hyg.dk/hvad-vil-du-helst/), a Danish website dedicated to fun and engaging questions. We extend our sincere gratitude to hyg.dk for providing the original content that made this dataset possible.

Thanks to all contributors who have helped create and curate this dataset. Special thanks to the Danish NLP community for their support and feedback.