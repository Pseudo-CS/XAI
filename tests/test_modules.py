import unittest
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from document_parser import DocumentParser
from citation_extractor import CitationExtractor
from ai_detector import AIDetector

class TestDocumentValidator(unittest.TestCase):
    
    def setUp(self):
        self.parser = DocumentParser()
        self.extractor = CitationExtractor()
        self.detector = AIDetector()
    
    def test_citation_extraction(self):
        test_text = "In Brown v. Board of Education, 347 U.S. 483 (1954), the Court held..."
        citations = self.extractor.extract_citations(test_text)
        self.assertGreater(len(citations['case_citations']), 0)
    
    def test_ai_detection(self):
        ai_text = "Whereas the party hereby agrees pursuant to the aforementioned conditions..."
        result = self.detector.detect_ai_content(ai_text)
        self.assertIn('ai_probability', result)
        self.assertGreaterEqual(result['ai_probability'], 0)
        self.assertLessEqual(result['ai_probability'], 1)
    
    def test_text_cleaning(self):
        dirty_text = "This   has    extra   spaces!!!"
        cleaned = self.parser.clean_text(dirty_text)
        self.assertNotIn('   ', cleaned)

if __name__ == '__main__':
    unittest.main()
