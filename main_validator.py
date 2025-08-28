from document_parser import DocumentParser
from citation_extractor import CitationExtractor
from ai_detector import AIDetector
import json
from datetime import datetime

class LegalDocumentValidator:
    def __init__(self):
        self.parser = DocumentParser()
        self.citation_extractor = CitationExtractor()
        self.ai_detector = AIDetector()
    
    def validate_document(self, document_path):
        """Main validation workflow"""
        print(f"Starting validation of: {document_path}")
        
        # Step 1: Parse document
        print("Step 1: Parsing document...")
        try:
            raw_text = self.parser.parse_document(document_path)
            cleaned_text = self.parser.clean_text(raw_text)
        except Exception as e:
            return {'error': f"Failed to parse document: {e}"}
        
        if not cleaned_text:
            return {'error': 'No text extracted from document'}
        
        # Step 2: Extract and verify citations
        print("Step 2: Extracting citations...")
        citations = self.citation_extractor.extract_citations(cleaned_text)
        citation_verification = self.citation_extractor.verify_citations(citations)
        citation_stats = self.citation_extractor.get_citation_statistics(citation_verification)
        
        # Step 3: Detect AI content
        print("Step 3: Analyzing for AI-generated content...")
        ai_analysis = self.ai_detector.detect_ai_content(cleaned_text)
        
        # Step 4: Generate comprehensive report
        print("Step 4: Generating validation report...")
        report = self.generate_report(
            document_path, 
            cleaned_text, 
            citations, 
            citation_verification, 
            citation_stats, 
            ai_analysis
        )
        
        return report
    
    def generate_report(self, document_path, text, citations, verification_results, citation_stats, ai_analysis):
        """Generate comprehensive validation report"""
        report = {
            'document_info': {
                'file_path': document_path,
                'analysis_date': datetime.now().isoformat(),
                'text_length': len(text),
                'word_count': len(text.split())
            },
            'citation_analysis': {
                'citations_found': citations,
                'verification_results': verification_results,
                'statistics': citation_stats
            },
            'ai_detection': ai_analysis,
            'overall_assessment': self.calculate_overall_score(citation_stats, ai_analysis),
            'recommendations': self.generate_recommendations(citation_stats, ai_analysis)
        }
        
        return report
    
    def calculate_overall_score(self, citation_stats, ai_analysis):
        """Calculate overall document reliability score"""
        citation_score = citation_stats.get('verification_rate', 0) * 100
        ai_confidence = (1 - ai_analysis.get('ai_probability', 0.5)) * 100
        
        overall_score = (citation_score * 0.6 + ai_confidence * 0.4)
        
        if overall_score >= 80:
            reliability = 'High'
        elif overall_score >= 60:
            reliability = 'Medium'
        else:
            reliability = 'Low'
        
        return {
            'overall_score': round(overall_score, 2),
            'reliability_level': reliability,
            'citation_score': round(citation_score, 2),
            'human_likelihood_score': round(ai_confidence, 2)
        }
    
    def generate_recommendations(self, citation_stats, ai_analysis):
        """Generate actionable recommendations"""
        recommendations = []
        
        if citation_stats.get('verification_rate', 1) < 0.8:
            recommendations.append("Verify unconfirmed citations with authoritative legal databases")
        
        if ai_analysis.get('ai_probability', 0) > 0.7:
            recommendations.append("High likelihood of AI generation - requires human legal expert review")
        
        if citation_stats.get('total_citations', 0) == 0:
            recommendations.append("Document contains no legal citations - verify legal validity")
        
        if not recommendations:
            recommendations.append("Document passed basic validation checks")
        
        return recommendations
    
    def save_report(self, report, output_path):
        """Save validation report to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"Report saved to: {output_path}")

# Example usage
if __name__ == "__main__":
    validator = LegalDocumentValidator()
    
    # Validate a document
    result = validator.validate_document("sample_legal_document.pdf")
    
    # Print summary
    if 'error' not in result:
        print("\n=== VALIDATION SUMMARY ===")
        print(f"Overall Score: {result['overall_assessment']['overall_score']}/100")
        print(f"Reliability: {result['overall_assessment']['reliability_level']}")
        print(f"Citations Found: {result['citation_analysis']['statistics']['total_citations']}")
        print(f"AI Probability: {result['ai_detection']['ai_probability']:.2f}")
        print("\nRecommendations:")
        for rec in result['recommendations']:
            print(f"- {rec}")
        
        # Save detailed report
        validator.save_report(result, "validation_report.json")
    else:
        print(f"Error: {result['error']}")
