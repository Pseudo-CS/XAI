import re
from collections import Counter
import math

class AIDetector:
    def __init__(self):
        # Common AI-generated text patterns
        self.ai_indicators = {
            'formal_words': ['whereas', 'hereby', 'aforementioned', 'pursuant', 'therein', 'thereof'],
            'repetitive_phrases': ['it is important to note', 'it should be noted', 'in conclusion'],
            'hedge_words': ['may', 'might', 'could', 'potentially', 'possibly', 'likely'],
            'generic_transitions': ['furthermore', 'moreover', 'additionally', 'consequently']
        }
    
    def analyze_word_frequency(self, text):
        """Analyze word frequency patterns typical of AI text"""
        words = re.findall(r'\b\w+\b', text.lower())
        word_freq = Counter(words)
        total_words = len(words)
        
        # Calculate metrics
        unique_words = len(word_freq)
        repetition_score = sum(1 for count in word_freq.values() if count > 3) / unique_words if unique_words > 0 else 0
        
        return {
            'total_words': total_words,
            'unique_words': unique_words,
            'repetition_score': repetition_score,
            'vocabulary_diversity': unique_words / total_words if total_words > 0 else 0
        }
    
    def check_ai_indicators(self, text):
        """Check for specific AI-generated text indicators"""
        text_lower = text.lower()
        scores = {}
        
        for category, words in self.ai_indicators.items():
            count = sum(text_lower.count(word) for word in words)
            scores[category] = count
        
        return scores
    
    def analyze_sentence_patterns(self, text):
        """Analyze sentence structure patterns"""
        sentences = re.split(r'[.!?]+', text)
        sentence_lengths = [len(sentence.split()) for sentence in sentences if sentence.strip()]
        
        if not sentence_lengths:
            return {'avg_length': 0, 'length_variance': 0, 'pattern_score': 0}
        
        avg_length = sum(sentence_lengths) / len(sentence_lengths)
        length_variance = sum((length - avg_length) ** 2 for length in sentence_lengths) / len(sentence_lengths)
        
        # AI text often has more uniform sentence lengths
        pattern_score = 1 / (1 + length_variance) if length_variance > 0 else 1
        
        return {
            'avg_length': avg_length,
            'length_variance': length_variance,
            'pattern_score': pattern_score
        }
    
    def detect_ai_content(self, text):
        """Main AI detection function"""
        if len(text) < 100:  # Too short to analyze
            return {'ai_probability': 0.5, 'confidence': 'low', 'details': 'Text too short for analysis'}
        
        # Analyze different aspects
        word_analysis = self.analyze_word_frequency(text)
        indicator_scores = self.check_ai_indicators(text)
        sentence_analysis = self.analyze_sentence_patterns(text)
        
        # Calculate AI probability based on weighted factors
        ai_score = 0
        
        # Word frequency indicators
        if word_analysis['repetition_score'] > 0.1:
            ai_score += 0.2
        
        # AI indicator words
        total_indicators = sum(indicator_scores.values())
        if total_indicators > 5:
            ai_score += 0.3
        
        # Sentence pattern uniformity
        if sentence_analysis['pattern_score'] > 0.8:
            ai_score += 0.2
        
        # Low vocabulary diversity
        if word_analysis['vocabulary_diversity'] < 0.3:
            ai_score += 0.1
        
        # High formal language usage
        if indicator_scores.get('formal_words', 0) > 3:
            ai_score += 0.2
        
        # Determine confidence level
        confidence = 'high' if ai_score > 0.7 or ai_score < 0.3 else 'medium'
        
        return {
            'ai_probability': min(ai_score, 1.0),
            'confidence': confidence,
            'details': {
                'word_analysis': word_analysis,
                'indicator_scores': indicator_scores,
                'sentence_analysis': sentence_analysis
            }
        }
