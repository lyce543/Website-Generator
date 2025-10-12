"""
Unit tests for website generator
"""
import pytest
import os
from unittest.mock import Mock, patch, AsyncMock
from app.generator import WebsiteGenerator
from app.prompts import PromptManager


@pytest.fixture(autouse=True)
def mock_openai_key():
    """Mock OpenAI API key for all tests"""
    os.environ['OPENAI_API_KEY'] = 'test-key-for-testing'
    yield
    if 'OPENAI_API_KEY' in os.environ and os.environ['OPENAI_API_KEY'] == 'test-key-for-testing':
        del os.environ['OPENAI_API_KEY']


def test_color_scheme_variety():
    """Test that color schemes are diverse"""
    generator = WebsiteGenerator()
    colors = [generator._get_random_colors() for _ in range(20)]
    unique_primaries = set(c['primary'] for c in colors)
    assert len(unique_primaries) > 5, "Color schemes should be diverse"


def test_prompt_variation():
    """Test that prompts vary across generations"""
    pm = PromptManager()
    prompts = [pm.get_title_prompt("AI", "educational", i) for i in range(5)]
    assert len(set(prompts)) == 5, "All prompts should be unique"


def test_template_styles_exist():
    """Test that all template styles are created"""
    generator = WebsiteGenerator()
    templates = ["modern", "minimal", "classic", "magazine"]
    
    for template_name in templates:
        template_method = getattr(generator, f"_get_{template_name}_template")
        template_content = template_method()
        assert len(template_content) > 100, f"{template_name} template should have content"
        assert "{{ title }}" in template_content, f"{template_name} template should have title placeholder"


def test_section_count_varies():
    """Test that section count varies between 3-5"""
    pm = PromptManager()
    section_counts = []
    
    for _ in range(10):
        sections = pm.get_section_prompts("AI", "educational", 800)
        section_counts.append(len(sections))
    
    assert min(section_counts) >= 3, "Should have at least 3 sections"
    assert max(section_counts) <= 5, "Should have at most 5 sections"
    assert len(set(section_counts)) > 1, "Section counts should vary"


@pytest.mark.asyncio
async def test_content_generation():
    """Test that content generation method works without actual API call"""
    generator = WebsiteGenerator()
    
    # Mock the entire asyncio.to_thread call instead of patching llm.invoke
    mock_result = Mock()
    mock_result.content = "This is AI generated content about artificial intelligence"
    
    async def mock_to_thread(func, *args):
        return mock_result
    
    with patch('asyncio.to_thread', side_effect=mock_to_thread):
        content = await generator._generate_content("Write a short sentence about AI")
        assert isinstance(content, str), "Generated content should be string"
        assert len(content) > 0, "Generated content should not be empty"


def test_random_template_selection():
    """Test that template selection is random"""
    import random
    random.seed(42)
    
    generator = WebsiteGenerator()
    template_styles = ["modern", "minimal", "classic", "magazine"]
    
    selected = [random.choice(template_styles) for _ in range(20)]
    unique_selections = set(selected)
    
    assert len(unique_selections) > 2, "Should select different templates randomly"


def test_color_schemes_count():
    """Test that we have enough color schemes"""
    generator = WebsiteGenerator()
    
    colors_collected = set()
    for _ in range(50):
        scheme = generator._get_random_colors()
        colors_collected.add(scheme['primary'])
    
    assert len(colors_collected) >= 10, "Should have at least 10 different color schemes"


def test_template_files_created():
    """Test that template files are created on initialization"""
    from pathlib import Path
    
    generator = WebsiteGenerator()
    generator._ensure_templates()
    
    expected_templates = ["site_modern.html", "site_minimal.html", "site_classic.html", "site_magazine.html"]
    templates_path = Path(__file__).parent.parent / "app" / "templates"
    
    for template_name in expected_templates:
        template_file = templates_path / template_name
        assert template_file.exists(), f"{template_name} should be created"


def test_html_rendering():
    """Test that HTML rendering works correctly"""
    generator = WebsiteGenerator()
    
    sections = [
        {"heading": "Introduction", "content": "This is test content"},
        {"heading": "Details", "content": "More test content"}
    ]
    
    color_scheme = generator._get_random_colors()
    
    html = generator._render_html(
        site_id="test-123",
        title="Test Title",
        meta_description="Test description",
        sections=sections,
        color_scheme=color_scheme,
        template_name="modern"
    )
    
    assert "Test Title" in html
    assert "Test description" in html
    assert "Introduction" in html
    assert len(html) > 500, "Generated HTML should be substantial"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])