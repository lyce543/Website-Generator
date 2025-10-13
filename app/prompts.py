"""
Prompt templates and management
"""
import random
from typing import List, Dict


class PromptManager:  
    def __init__(self):
        self.title_variations = [
            "Create a compelling title about {topic}. Style: {style}. Be unique and engaging.",
            "Generate an innovative title for {topic}. Use {style} tone. Be creative.",
            "Craft a distinctive title covering {topic}. {style} approach. Make it memorable.",
            "Design a captivating title for {topic}. Apply {style} style. Stand out.",
            "Produce an original title focused on {topic}. {style} perspective. Avoid clichés."
        ]
        
        self.meta_variations = [
            "Write a meta description (150-160 chars) for a {style} website about {topic}.",
            "Create an SEO-optimized meta description about {topic}. Style: {style}. Under 160 characters.",
            "Generate a unique meta description for {topic}. Use {style} tone. 150-160 characters.",
            "Craft an engaging meta description covering {topic}. {style} style. Optimize for search."
        ]
        
        self.section_types = {
            "educational": [
                {"heading": "Introduction", "type": "intro"},
                {"heading": "Understanding the Fundamentals", "type": "fundamentals"},
                {"heading": "Key Concepts Explained", "type": "concepts"},
                {"heading": "Real-World Applications", "type": "applications"},
                {"heading": "Common Challenges and Solutions", "type": "challenges"},
                {"heading": "Best Practices", "type": "best_practices"},
                {"heading": "Future Outlook", "type": "future"},
                {"heading": "Getting Started", "type": "getting_started"},
                {"heading": "Resources and Tools", "type": "resources"},
                {"heading": "Conclusion", "type": "conclusion"}
            ],
            "marketing": [
                {"heading": "Why This Matters", "type": "value_prop"},
                {"heading": "Transform Your Business", "type": "transformation"},
                {"heading": "Proven Benefits", "type": "benefits"},
                {"heading": "Success Stories", "type": "testimonials"},
                {"heading": "How It Works", "type": "process"},
                {"heading": "Get Started Today", "type": "cta"},
                {"heading": "Industry Leadership", "type": "authority"},
                {"heading": "What Sets Us Apart", "type": "differentiation"},
                {"heading": "ROI and Value", "type": "roi"},
                {"heading": "Join Thousands of Satisfied Users", "type": "social_proof"}
            ],
            "technical": [
                {"heading": "Technical Overview", "type": "overview"},
                {"heading": "Architecture and Design", "type": "architecture"},
                {"heading": "Implementation Details", "type": "implementation"},
                {"heading": "API and Integration", "type": "api"},
                {"heading": "Performance Considerations", "type": "performance"},
                {"heading": "Security Features", "type": "security"},
                {"heading": "Scalability", "type": "scalability"},
                {"heading": "Code Examples", "type": "examples"},
                {"heading": "Troubleshooting", "type": "troubleshooting"},
                {"heading": "Advanced Topics", "type": "advanced"}
            ]
        }
    
    def get_title_prompt(self, topic: str, style: str, index: int) -> str:
        """Get varied title prompt"""
        variation_suffix = [
            " Focus on innovation.",
            " Emphasize practical aspects.",
            " Highlight cutting-edge developments.",
            " Stress accessibility and clarity.",
            " Showcase real-world impact.",
            " Emphasize technical depth.",
            " Focus on business value.",
            " Highlight emerging trends."
        ]
        
        base_prompt = random.choice(self.title_variations).format(
            topic=topic,
            style=style
        )
        return base_prompt + variation_suffix[index % len(variation_suffix)]
    
    def get_meta_prompt(self, topic: str, style: str) -> str:
        """Get meta description prompt"""
        return random.choice(self.meta_variations).format(
            topic=topic,
            style=style
        )
    
    def get_section_prompts(
        self,
        topic: str,
        style: str,
        max_tokens: int
    ) -> List[Dict]:
        """Get randomized section prompts"""
        style_key = style if style in self.section_types else "educational"
        available_sections = self.section_types[style_key].copy()
        
        num_sections = random.randint(3, 5)
        selected_sections = random.sample(available_sections, min(num_sections, len(available_sections)))
        
        section_prompts = []
        for section in selected_sections:
            prompt = self._create_section_prompt(
                topic=topic,
                heading=section["heading"],
                section_type=section["type"],
                style=style,
                max_tokens=max_tokens
            )
            section_prompts.append({
                "heading": section["heading"],
                "prompt": prompt
            })
        
        return section_prompts
    
    def _create_section_prompt(
        self,
        topic: str,
        heading: str,
        section_type: str,
        style: str,
        max_tokens: int
    ) -> str:
        base_prompts = {
            "intro": "Write an engaging introduction about {topic}. Set context. Style: {style}. Length: {tokens} words.",
            "fundamentals": "Explain fundamental concepts of {topic}. Clear and accessible. Style: {style}. Length: {tokens} words.",
            "applications": "Describe real-world applications of {topic}. Specific examples. Style: {style}. Length: {tokens} words.",
            "challenges": "Discuss challenges and solutions for {topic}. Be practical. Style: {style}. Length: {tokens} words.",
            "future": "Explore future trends in {topic}. Be forward-thinking. Style: {style}. Length: {tokens} words.",
            "value_prop": "Explain why {topic} matters. Be persuasive. Style: {style}. Length: {tokens} words.",
            "benefits": "List key benefits of {topic}. Focus on outcomes. Style: {style}. Length: {tokens} words.",
            "process": "Describe how {topic} works. Be methodical. Style: {style}. Length: {tokens} words.",
            "technical": "Provide technical details about {topic}. Be specific. Style: {style}. Length: {tokens} words.",
            "architecture": "Explain architecture of {topic}. Be detailed. Style: {style}. Length: {tokens} words."
        }
        
        template = base_prompts.get(
            section_type,
            "Write comprehensive content about {topic} for '{heading}'. Style: {style}. Length: {tokens} words."
        )
        
        word_count = int(max_tokens * 0.75)
        
        return template.format(
            topic=topic,
            heading=heading,
            style=style,
            tokens=word_count

        )
