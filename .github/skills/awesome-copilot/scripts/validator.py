#!/usr/bin/env python3
"""
Awesome Copilot Customization Validator

Validates agent, prompt, instruction, and collection files for proper format,
naming conventions, and required fields.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ValidationResult:
    """Result of validating a single file."""
    file_path: str
    valid: bool
    errors: List[str]
    warnings: List[str]


class CustomizationValidator:
    """Validator for awesome-copilot customization files."""

    AGENT_PATTERN = r'^[a-z0-9\-]+\.agent\.md$'
    PROMPT_PATTERN = r'^[a-z0-9\-]+\.prompt\.md$'
    INSTRUCTION_PATTERN = r'^[a-z0-9\-]+\.instructions\.md$'
    COLLECTION_PATTERN = r'^[a-z0-9\-]+\.collection\.md$'

    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)

    def validate_file_name(self, file_path: Path, pattern: str) -> List[str]:
        """Validate file naming convention."""
        errors = []
        file_name = file_path.name

        if not re.match(pattern, file_name):
            errors.append(f"File name '{file_name}' doesn't match pattern {pattern}")

        if '_' in file_name:
            errors.append("File name contains underscores - use hyphens instead")

        if ' ' in file_name:
            errors.append("File name contains spaces - use hyphens instead")

        if file_name != file_name.lower():
            errors.append("File name must be all lowercase")

        return errors

    def extract_front_matter(self, content: str) -> Tuple[Optional[Dict], List[str]]:
        """Extract and parse YAML front matter from markdown."""
        errors = []

        if not content.startswith('---'):
            errors.append("Missing front matter (should start with ---)")
            return None, errors

        # Find the closing ---
        parts = content.split('---', 2)
        if len(parts) < 3:
            errors.append("Front matter not properly closed (missing closing ---)")
            return None, errors

        front_matter_text = parts[1].strip()
        try:
            front_matter = yaml.safe_load(front_matter_text)
            return front_matter, errors
        except yaml.YAMLError as e:
            errors.append(f"Invalid YAML in front matter: {str(e)}")
            return None, errors

    def validate_agent(self, file_path: Path) -> ValidationResult:
        """Validate an agent file."""
        errors = []
        warnings = []

        # Validate file name
        errors.extend(self.validate_file_name(file_path, self.AGENT_PATTERN))

        # Read and parse file
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            errors.append(f"Failed to read file: {str(e)}")
            return ValidationResult(str(file_path), False, errors, warnings)

        # Extract front matter
        front_matter, fm_errors = self.extract_front_matter(content)
        errors.extend(fm_errors)

        if front_matter:
            # Required field: description
            if 'description' not in front_matter:
                errors.append("Missing required field: description")
            elif not isinstance(front_matter['description'], str):
                errors.append("Field 'description' must be a string")
            elif not front_matter['description'].strip():
                errors.append("Field 'description' cannot be empty")
            elif len(front_matter['description']) > 1024:
                errors.append("Field 'description' exceeds 1024 characters")
            elif not (front_matter['description'].startswith("'") and
                     front_matter['description'].endswith("'")):
                warnings.append("Field 'description' should be wrapped in single quotes")

            # Recommended field: model
            if 'model' not in front_matter:
                warnings.append("Missing recommended field: model")
            elif front_matter['model'] not in [
                'claude-3-5-sonnet-20241022',
                'claude-3-opus-20240229',
                'claude-3-haiku-20240307'
            ]:
                warnings.append(f"Unknown model: {front_matter['model']}")

            # Optional field: tools
            if 'tools' in front_matter:
                if not isinstance(front_matter['tools'], list):
                    errors.append("Field 'tools' must be an array")

        return ValidationResult(
            str(file_path),
            len(errors) == 0,
            errors,
            warnings
        )

    def validate_prompt(self, file_path: Path) -> ValidationResult:
        """Validate a prompt file."""
        errors = []
        warnings = []

        # Validate file name
        errors.extend(self.validate_file_name(file_path, self.PROMPT_PATTERN))

        # Read and parse file
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            errors.append(f"Failed to read file: {str(e)}")
            return ValidationResult(str(file_path), False, errors, warnings)

        # Extract front matter
        front_matter, fm_errors = self.extract_front_matter(content)
        errors.extend(fm_errors)

        if front_matter:
            # Required fields
            if 'title' not in front_matter:
                errors.append("Missing required field: title")
            elif not front_matter['title'].strip():
                errors.append("Field 'title' cannot be empty")

            if 'description' not in front_matter:
                errors.append("Missing required field: description")
            elif not front_matter['description'].strip():
                errors.append("Field 'description' cannot be empty")

        return ValidationResult(
            str(file_path),
            len(errors) == 0,
            errors,
            warnings
        )

    def validate_instruction(self, file_path: Path) -> ValidationResult:
        """Validate an instruction file."""
        errors = []
        warnings = []

        # Validate file name
        errors.extend(self.validate_file_name(file_path, self.INSTRUCTION_PATTERN))

        # Read and parse file
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            errors.append(f"Failed to read file: {str(e)}")
            return ValidationResult(str(file_path), False, errors, warnings)

        # Extract front matter
        front_matter, fm_errors = self.extract_front_matter(content)
        errors.extend(fm_errors)

        if front_matter:
            # Required fields
            if 'description' not in front_matter:
                errors.append("Missing required field: description")
            elif not front_matter['description'].strip():
                errors.append("Field 'description' cannot be empty")

            if 'patterns' not in front_matter:
                errors.append("Missing required field: patterns")
            elif not isinstance(front_matter['patterns'], list):
                errors.append("Field 'patterns' must be an array")
            elif len(front_matter['patterns']) == 0:
                errors.append("Field 'patterns' must have at least one pattern")
            else:
                # Validate glob patterns
                for pattern in front_matter['patterns']:
                    if not isinstance(pattern, str):
                        errors.append(f"Pattern must be string, got: {type(pattern)}")
                    elif not pattern.strip():
                        errors.append("Pattern cannot be empty")

        return ValidationResult(
            str(file_path),
            len(errors) == 0,
            errors,
            warnings
        )

    def validate_collection(self, file_path: Path) -> ValidationResult:
        """Validate a collection file."""
        errors = []
        warnings = []

        # Validate file name
        errors.extend(self.validate_file_name(file_path, self.COLLECTION_PATTERN))

        # Read and parse file
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception as e:
            errors.append(f"Failed to read file: {str(e)}")
            return ValidationResult(str(file_path), False, errors, warnings)

        # Extract front matter
        front_matter, fm_errors = self.extract_front_matter(content)
        errors.extend(fm_errors)

        if front_matter:
            # Required fields
            if 'title' not in front_matter:
                errors.append("Missing required field: title")
            elif not front_matter['title'].strip():
                errors.append("Field 'title' cannot be empty")

            if 'description' not in front_matter:
                errors.append("Missing required field: description")
            elif not front_matter['description'].strip():
                errors.append("Field 'description' cannot be empty")

        return ValidationResult(
            str(file_path),
            len(errors) == 0,
            errors,
            warnings
        )

    def validate_directory(self, directory: str) -> List[ValidationResult]:
        """Validate all files in a directory."""
        results = []
        dir_path = self.base_path / directory

        if not dir_path.exists():
            print(f"Directory not found: {dir_path}")
            return results

        for file_path in dir_path.glob('*.md'):
            if file_path.name.endswith('.agent.md'):
                results.append(self.validate_agent(file_path))
            elif file_path.name.endswith('.prompt.md'):
                results.append(self.validate_prompt(file_path))
            elif file_path.name.endswith('.instructions.md'):
                results.append(self.validate_instruction(file_path))
            elif file_path.name.endswith('.collection.md'):
                results.append(self.validate_collection(file_path))

        return results

    def print_results(self, results: List[ValidationResult]):
        """Print validation results."""
        total = len(results)
        valid = sum(1 for r in results if r.valid)
        invalid = total - valid

        print(f"\n{'='*60}")
        print(f"Validation Results: {valid}/{total} files valid")
        print(f"{'='*60}\n")

        for result in results:
            if not result.valid:
                print(f"❌ {result.file_path}")
                for error in result.errors:
                    print(f"   ERROR: {error}")
                for warning in result.warnings:
                    print(f"   WARNING: {warning}")
                print()

        if invalid == 0:
            print("✅ All files validated successfully!")
        else:
            print(f"❌ {invalid} file(s) failed validation")


def main():
    """Main entry point."""
    import sys

    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    else:
        base_path = "."

    validator = CustomizationValidator(base_path)

    # Validate all directories
    all_results = []

    directories = ['agents', 'prompts', 'instructions', 'collections']
    for directory in directories:
        print(f"Validating {directory}/...")
        results = validator.validate_directory(directory)
        all_results.extend(results)

    # Print summary
    validator.print_results(all_results)

    # Exit with error code if any failures
    if any(not r.valid for r in all_results):
        sys.exit(1)


if __name__ == "__main__":
    main()
