import re
import json

class CitationExtractor:
    def __init__(self):
        # Various citation patterns for different legal sources
        self.patterns = {
            'case_citations': re.compile(r'\b([A-Z][a-zA-Z\s]+ v\.?\s+[A-Z][a-zA-Z\s]+),?\s+(\d+\s+[A-Za-z\.]+\s+\d+)\s+\((\d{4})\)'),
            'statutes': re.compile(r'\b(\d+\s+U\.S\.C\.?\s+§?\s*\d+)'),
            'federal_rules': re.compile(r'\b(Fed\.?\s*R\.?\s*Civ\.?\s*P\.?\s*\d+)'),
            'constitutional': re.compile(r'\b(U\.S\.?\s*Const\.?\s*[A-Za-z]*\.?\s*[IVX]+)')
        }
        
        # Load sample verified citations database
        self.verified_citations = self.load_verified_citations()
    
    def load_verified_citations(self):
        """Load a sample database of verified citations"""
        sample_citations = {
            "Brown v. Board of Education": {"citation": "347 U.S. 483 (1954)", "verified": True},
            "Marbury v. Madison": {"citation": "5 U.S. 137 (1803)", "verified": True},
            "Miranda v. Arizona": {"citation": "384 U.S. 436 (1966)", "verified": True},
            "Roe v. Wade": {"citation": "410 U.S. 113 (1973)", "verified": True},
            "Smith v. Jones": {"citation": "123 F.3d 456 (2023)", "verified": False}  # Fake case
        }
        return sample_citations
    
    def extract_citations(self, text):
        """Extract all types of citations from text"""
        citations_found = {}
        
        for citation_type, pattern in self.patterns.items():
            matches = pattern.findall(text)
            citations_found[citation_type] = matches
        
        return citations_found
    
    def verify_citations(self, citations):
        """Verify citations against known database"""
        verification_results = {}
        
        for citation_type, citation_list in citations.items():
            verification_results[citation_type] = []
            
            if citation_type == 'case_citations':
                for case_name, citation, year in citation_list:
                    is_verified = case_name in self.verified_citations
                    verification_results[citation_type].append({
                        'case_name': case_name,
                        'citation': citation,
                        'year': year,
                        'verified': is_verified,
                        'confidence': 0.9 if is_verified else 0.1
                    })
            else:
                # For other citation types, assume verified for now
                for citation in citation_list:
                    verification_results[citation_type].append({
                        'citation': citation,
                        'verified': True,
                        'confidence': 0.8
                    })
        
        return verification_results
    
    def get_citation_statistics(self, verification_results):
        """Generate statistics about citations found"""
        stats = {
            'total_citations': 0,
            'verified_citations': 0,
            'unverified_citations': 0,
            'verification_rate': 0
        }
        
        for citation_type, results in verification_results.items():
            stats['total_citations'] += len(results)
            for result in results:
                if result.get('verified', False):
                    stats['verified_citations'] += 1
                else:
                    stats['unverified_citations'] += 1
        
        if stats['total_citations'] > 0:
            stats['verification_rate'] = stats['verified_citations'] / stats['total_citations']
        
        return stats
