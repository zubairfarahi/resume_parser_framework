"""Example: Parse PDF resume using field-specific extractors.

This example demonstrates how to use the Resume Parser Framework to parse
a PDF resume and extract structured information (name, email, skills).
"""

from app.config.logging_config import setup_logging
from app.core.extractors import EmailExtractor, NameExtractor, SkillsExtractor
from app.core.framework import ResumeParserFramework


def main() -> None:
    """Parse a PDF resume and display extracted information."""
    # Setup logging
    setup_logging()

    # Define the path to the PDF resume
    resume_path = "path/to/resume.pdf"  # Update with actual path

    print("=" * 60)
    print("Resume Parser Framework - PDF Example")
    print("=" * 60)
    print(f"\nParsing resume: {resume_path}\n")

    # Step 1: Create field extractors
    extractors = {
        "name": NameExtractor(),
        "email": EmailExtractor(),
        "skills": SkillsExtractor(),  # Uses OpenAI (configure via .env)
    }

    # Step 2: Create the framework
    framework = ResumeParserFramework(extractors)

    try:
        # Step 3: Parse the resume
        print("Parsing PDF resume...")
        resume_data = framework.parse_resume(resume_path)

        # Step 4: Display results
        print("\n" + "=" * 60)
        print("EXTRACTION RESULTS")
        print("=" * 60)
        print(f"\nName:  {resume_data.name or 'Not found'}")
        print(f"Email: {resume_data.email or 'Not found'}")
        print(f"\nSkills ({len(resume_data.skills or [])} found):")
        if resume_data.skills:
            for skill in resume_data.skills:
                print(f"  • {skill}")
        else:
            print("  No skills found")

        # Step 5: Export to JSON
        print("\n" + "=" * 60)
        print("JSON OUTPUT")
        print("=" * 60)
        print(resume_data.to_json())

        print("\n✅ Parsing completed successfully!\n")

    except FileNotFoundError:
        print(f"\n❌ Error: File not found: {resume_path}")
        print("Please update the resume_path variable with the correct path.\n")

    except Exception as e:
        print(f"\n❌ Error occurred during parsing: {str(e)}")
        print(f"Error type: {type(e).__name__}\n")


if __name__ == "__main__":
    main()
