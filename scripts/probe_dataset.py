#!/usr/bin/env python3
"""
Dataset Probing Script for Hvad Vil Du Helst (What Would You Rather) Dataset

This script analyzes the Danish preference dataset, providing detailed statistics,
examples, and insights for use in LLM experiments.
"""

import json
import os
import sys
from pathlib import Path
from typing import List, Dict, Set, Tuple
from collections import Counter, defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Add src to path to import our modules
sys.path.append(str(Path(__file__).parent.parent / "src"))

try:
    from hvadvilduhelst.load_hygdk import load_hygdk_dataset
except ImportError:
    print("Warning: Could not import load_hygdk_dataset. Using fallback loader.")
    
    def load_hygdk_dataset(data_dir: str = "../data/hygdk") -> List[Dict]:
        """Fallback dataset loader"""
        dataset = []
        data_path = Path(data_dir)
        
        for file_path in data_path.glob("*.jsonl"):
            category = file_path.stem
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    data = json.loads(line)
                    entry = {
                        'questions': data['question'],
                        'answer_A': data['answer_A'],
                        'answer_B': data['answer_B'],
                        'category': category
                    }
                    dataset.append(entry)
        return dataset


def analyze_dataset_structure(dataset: List[Dict]) -> Dict:
    """Analyze the basic structure of the dataset"""
    print("=" * 60)
    print("DATASET STRUCTURE ANALYSIS")
    print("=" * 60)
    
    total_questions = len(dataset)
    categories = set(item['category'] for item in dataset)
    
    # Check for required fields
    required_fields = ['questions', 'answer_A', 'answer_B', 'category']
    missing_fields = []
    
    for item in dataset[:10]:  # Check first 10 items
        for field in required_fields:
            if field not in item:
                missing_fields.append(field)
    
    structure_info = {
        'total_questions': total_questions,
        'categories': categories,
        'num_categories': len(categories),
        'missing_fields': missing_fields,
        'required_fields': required_fields
    }
    
    print(f"Total Questions: {total_questions}")
    print(f"Number of Categories: {len(categories)}")
    print(f"Categories: {sorted(categories)}")
    
    if missing_fields:
        print(f"⚠️  Missing Fields Found: {set(missing_fields)}")
    else:
        print("✅ All required fields present")
    
    return structure_info


def analyze_categories(dataset: List[Dict]) -> Dict:
    """Analyze distribution across categories"""
    print("\n" + "=" * 60)
    print("CATEGORY ANALYSIS")
    print("=" * 60)
    
    category_counts = Counter(item['category'] for item in dataset)
    category_stats = dict(category_counts)
    
    print(f"Questions per Category:")
    for category, count in sorted(category_counts.items()):
        print(f"  {category:20} {count:3d} questions")
    
    # Statistical analysis
    counts = list(category_counts.values())
    mean_count = np.mean(counts)
    std_count = np.std(counts)
    min_count = min(counts)
    max_count = max(counts)
    
    print(f"\nCategory Statistics:")
    print(f"  Mean questions per category: {mean_count:.1f}")
    print(f"  Standard deviation: {std_count:.1f}")
    print(f"  Range: {min_count} - {max_count}")
    
    # Check for balance
    balance_threshold = 0.2  # 20% variation
    is_balanced = std_count / mean_count < balance_threshold
    print(f"  Dataset balanced: {'✅ Yes' if is_balanced else '❌ No'}")
    
    return {
        'category_counts': category_stats,
        'statistics': {
            'mean': mean_count,
            'std': std_count,
            'min': min_count,
            'max': max_count,
            'is_balanced': is_balanced
        }
    }


def analyze_question_characteristics(dataset: List[Dict]) -> Dict:
    """Analyze characteristics of questions and answers"""
    print("\n" + "=" * 60)
    print("QUESTION CHARACTERISTICS ANALYSIS")
    print("=" * 60)
    
    # Question lengths
    question_lengths = [len(item['questions']) for item in dataset]
    answer_a_lengths = [len(item['answer_A']) for item in dataset]
    answer_b_lengths = [len(item['answer_B']) for item in dataset]
    
    # Word counts (approximate)
    question_word_counts = [len(item['questions'].split()) for item in dataset]
    
    # Common patterns
    question_starters = Counter()
    for item in dataset:
        words = item['questions'].split()
        if words:
            first_few = ' '.join(words[:3])
            question_starters[first_few] += 1
    
    print("Question Length Statistics (characters):")
    print(f"  Mean: {np.mean(question_lengths):.1f}")
    print(f"  Median: {np.median(question_lengths):.1f}")
    print(f"  Range: {min(question_lengths)} - {max(question_lengths)}")
    
    print("\nAnswer Length Statistics (characters):")
    print(f"  Answer A - Mean: {np.mean(answer_a_lengths):.1f}, Range: {min(answer_a_lengths)}-{max(answer_a_lengths)}")
    print(f"  Answer B - Mean: {np.mean(answer_b_lengths):.1f}, Range: {min(answer_b_lengths)}-{max(answer_b_lengths)}")
    
    print("\nWord Count Statistics:")
    print(f"  Mean words per question: {np.mean(question_word_counts):.1f}")
    print(f"  Range: {min(question_word_counts)} - {max(question_word_counts)} words")
    
    print("\nMost Common Question Starters:")
    for starter, count in question_starters.most_common(10):
        print(f"  '{starter}': {count} times")
    
    return {
        'length_stats': {
            'question_lengths': question_lengths,
            'answer_a_lengths': answer_a_lengths,
            'answer_b_lengths': answer_b_lengths,
            'question_word_counts': question_word_counts
        },
        'patterns': {
            'question_starters': dict(question_starters.most_common(10))
        }
    }


def analyze_content_themes(dataset: List[Dict]) -> Dict:
    """Analyze content themes and topics"""
    print("\n" + "=" * 60)
    print("CONTENT THEMES ANALYSIS")
    print("=" * 60)
    
    # Analyze by category
    themes_by_category = defaultdict(list)
    
    for item in dataset:
        category = item['category']
        question = item['questions'].lower()
        themes_by_category[category].append(question)
    
    # Look for common Danish words/themes
    danish_words = {
        'arbejde': ['arbejde', 'job', 'chef', 'kontor', 'løn'],
        'family': ['familie', 'mor', 'far', 'barn', 'børn', 'forældre'],
        'food': ['mad', 'spise', 'pizza', 'chokolade', 'kaffe'],
        'physical': ['krop', 'hoved', 'arm', 'ben', 'øje', 'næse'],
        'time': ['dag', 'uge', 'måned', 'år', 'tid', 'altid', 'aldrig'],
        'choice_intensity': ['helst', 'ville', 'eller', 'frem for']
    }
    
    theme_counts = defaultdict(int)
    for theme, words in danish_words.items():
        for item in dataset:
            question = item['questions'].lower()
            for word in words:
                if word in question:
                    theme_counts[theme] += 1
                    break  # Count each question only once per theme
    
    print("Common Themes Found:")
    for theme, count in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(dataset)) * 100
        print(f"  {theme:15} {count:3d} questions ({percentage:.1f}%)")
    
    return {
        'theme_counts': dict(theme_counts),
        'themes_by_category': dict(themes_by_category)
    }


def show_examples(dataset: List[Dict], n_examples: int = 3) -> None:
    """Show examples from each category"""
    print("\n" + "=" * 60)
    print("EXAMPLE QUESTIONS BY CATEGORY")
    print("=" * 60)
    
    # Group by category
    by_category = defaultdict(list)
    for item in dataset:
        by_category[item['category']].append(item)
    
    # Show examples from each category
    for category in sorted(by_category.keys()):
        items = by_category[category]
        print(f"\n{category.upper()} ({len(items)} questions):")
        print("-" * 40)
        
        # Show first n_examples
        for i, item in enumerate(items[:n_examples]):
            print(f"{i+1}. {item['questions']}")
            print(f"   A: {item['answer_A']}")
            print(f"   B: {item['answer_B']}\n")


def detect_quality_issues(dataset: List[Dict]) -> Dict:
    """Detect potential quality issues in the dataset"""
    print("\n" + "=" * 60)
    print("QUALITY ASSESSMENT")
    print("=" * 60)
    
    issues = {
        'duplicate_questions': [],
        'very_short_questions': [],
        'very_long_questions': [],
        'duplicate_answers': [],
        'missing_content': []
    }
    
    seen_questions = set()
    for i, item in enumerate(dataset):
        question = item['questions']
        
        # Check for duplicates
        if question in seen_questions:
            issues['duplicate_questions'].append((i, question))
        seen_questions.add(question)
        
        # Check for very short/long questions
        if len(question) < 20:
            issues['very_short_questions'].append((i, question))
        elif len(question) > 200:
            issues['very_long_questions'].append((i, question))
        
        # Check for duplicate answer options
        if item['answer_A'] == item['answer_B']:
            issues['duplicate_answers'].append((i, question))
        
        # Check for missing content
        if not question.strip() or not item['answer_A'].strip() or not item['answer_B'].strip():
            issues['missing_content'].append((i, question))
    
    # Report findings
    total_issues = sum(len(issue_list) for issue_list in issues.values())
    
    if total_issues == 0:
        print("✅ No quality issues detected!")
    else:
        print(f"⚠️  Found {total_issues} potential quality issues:")
        
        for issue_type, issue_list in issues.items():
            if issue_list:
                print(f"\n{issue_type.replace('_', ' ').title()}: {len(issue_list)}")
                for i, (idx, content) in enumerate(issue_list[:3]):  # Show first 3
                    print(f"  {idx}: {content[:80]}...")
                if len(issue_list) > 3:
                    print(f"  ... and {len(issue_list) - 3} more")
    
    return issues


def generate_experiment_recommendations(dataset: List[Dict], analysis_results: Dict) -> None:
    """Generate recommendations based on dataset analysis"""
    print("\n" + "=" * 60)
    print("EXPERIMENT RECOMMENDATIONS")
    print("=" * 60)
    
    total_questions = len(dataset)
    num_categories = len(set(item['category'] for item in dataset))
    
    print("Based on the dataset analysis, here are recommendations for your experiments:")
    print()
    
    # Experiment 4: Intra-Model Consistency
    print("🔄 EXPERIMENT 4: Intra-Model Consistency Testing")
    print("  Recommended approach:")
    print(f"  • Use all {total_questions} questions for comprehensive coverage")
    print(f"  • Sample 5-10 responses per question (manageable scope)")
    print(f"  • Start with a subset of ~100 questions from each category for initial testing")
    print(f"  • Focus on categories with clear binary choices")
    print()
    
    # Experiment 5: Temperature Sensitivity
    print("🌡️  EXPERIMENT 5: Temperature Sensitivity Analysis")
    print("  Recommended approach:")
    print(f"  • Use subset of ~50 questions per category ({50 * num_categories} total)")
    print(f"  • Test temperatures: 0.0, 0.3, 0.7, 1.0, 1.5")
    print(f"  • Focus on questions with cultural/value-based content")
    print()
    
    # Experiment 3: Category-Specific Patterns
    print("📊 EXPERIMENT 3: Category-Specific Disagreement Patterns")
    print("  Recommended approach:")
    category_counts = Counter(item['category'] for item in dataset)
    balanced_categories = [cat for cat, count in category_counts.items() if count >= 35]
    
    print(f"  • Focus on {len(balanced_categories)} well-represented categories:")
    for cat in sorted(balanced_categories):
        print(f"    - {cat} ({category_counts[cat]} questions)")
    print(f"  • Use 20-30 questions per category for statistical significance")
    print()
    
    # Implementation suggestions
    print("🛠️  IMPLEMENTATION SUGGESTIONS")
    print("  • Start with Danish-focused categories (arbejde, familie, mad)")
    print("  • Questions with cultural context may show more variation")
    print("  • Consider excluding very short questions for consistency measurement")
    if analysis_results.get('quality_issues', {}).get('duplicate_questions'):
        print("  • ⚠️  Remove duplicate questions before running experiments")
    print()


def create_visualization_suggestions(analysis_results: Dict) -> None:
    """Suggest visualizations for the analysis"""
    print("📈 VISUALIZATION SUGGESTIONS")
    print("  Recommended plots for your analysis:")
    print("  • Category distribution bar chart")
    print("  • Question length distribution histogram")
    print("  • Consistency scores by category (after experiments)")
    print("  • Temperature sensitivity heatmap")
    print("  • Word cloud of common question patterns")
    print()


def main():
    """Main function to run all dataset analysis"""
    print("🔍 HVAD VIL DU HELST DATASET ANALYSIS")
    print("=" * 60)
    
    # Load dataset
    try:
        # Try relative path first
        dataset = load_hygdk_dataset("../data/hygdk")
    except FileNotFoundError:
        try:
            # Try absolute path
            dataset = load_hygdk_dataset()
        except FileNotFoundError:
            print("❌ Error: Could not find dataset files.")
            print("Make sure you're running from the scripts/ directory")
            print("and that the data/hygdk/ directory exists.")
            return
    
    if not dataset:
        print("❌ Error: Dataset is empty or could not be loaded.")
        return
    
    print(f"✅ Successfully loaded {len(dataset)} questions from dataset")
    
    # Run all analyses
    analysis_results = {}
    
    analysis_results['structure'] = analyze_dataset_structure(dataset)
    analysis_results['categories'] = analyze_categories(dataset)
    analysis_results['characteristics'] = analyze_question_characteristics(dataset)
    analysis_results['themes'] = analyze_content_themes(dataset)
    
    show_examples(dataset, n_examples=2)
    
    analysis_results['quality_issues'] = detect_quality_issues(dataset)
    
    generate_experiment_recommendations(dataset, analysis_results)
    create_visualization_suggestions(analysis_results)
    
    print("=" * 60)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 60)
    print("Dataset is ready for LLM experiments!")
    print("Refer to docs/experiments.md for detailed experiment plans.")


if __name__ == "__main__":
    main() 