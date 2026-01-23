#!/usr/bin/env python3
"""
Playwright MCP Helper Utilities

Helper functions for common Playwright automation tasks.
These can be used alongside Claude Code's Playwright MCP tools.
"""

import json
import re
from typing import Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class FormField:
    """Represents a form field for browser_fill_form."""
    name: str
    field_type: str  # textbox, checkbox, radio, combobox, slider
    ref: str
    value: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "type": self.field_type,
            "ref": self.ref,
            "value": self.value
        }


def generate_form_fields(fields_config: list[dict]) -> str:
    """
    Generate JSON for browser_fill_form from a simple config.

    Example:
        fields = [
            {"name": "Username", "ref": "textbox[Username]", "value": "john"},
            {"name": "Email", "ref": "textbox[Email]", "value": "john@example.com"},
        ]
        print(generate_form_fields(fields))
    """
    form_fields = []
    for field in fields_config:
        # Infer type from ref pattern
        ref = field.get("ref", "")
        if ref.startswith("textbox["):
            field_type = "textbox"
        elif ref.startswith("checkbox["):
            field_type = "checkbox"
        elif ref.startswith("radio["):
            field_type = "radio"
        elif ref.startswith("combobox[") or ref.startswith("listbox["):
            field_type = "combobox"
        elif ref.startswith("slider["):
            field_type = "slider"
        else:
            field_type = field.get("type", "textbox")

        form_fields.append({
            "name": field["name"],
            "type": field_type,
            "ref": field["ref"],
            "value": str(field["value"])
        })

    return json.dumps(form_fields, indent=2)


def parse_snapshot_for_forms(snapshot_text: str) -> list[dict]:
    """
    Parse accessibility snapshot text to identify form fields.

    Returns list of identified form fields with their refs.
    """
    form_fields = []

    # Pattern to match form elements
    patterns = [
        (r'textbox\[([^\]]+)\]', 'textbox'),
        (r'checkbox\[([^\]]+)\]', 'checkbox'),
        (r'radio\[([^\]]+)\]', 'radio'),
        (r'combobox\[([^\]]+)\]', 'combobox'),
        (r'listbox\[([^\]]+)\]', 'combobox'),
        (r'slider\[([^\]]+)\]', 'slider'),
    ]

    for pattern, field_type in patterns:
        matches = re.findall(pattern, snapshot_text)
        for match in matches:
            form_fields.append({
                "name": match,
                "type": field_type,
                "ref": f"{field_type}[{match}]"
            })

    return form_fields


def parse_snapshot_for_buttons(snapshot_text: str) -> list[dict]:
    """
    Parse accessibility snapshot to find clickable elements.
    """
    buttons = []

    patterns = [
        (r'button\[([^\]]+)\]', 'button'),
        (r'link\[([^\]]+)\]', 'link'),
        (r'menuitem\[([^\]]+)\]', 'menuitem'),
        (r'tab\[([^\]]+)\]', 'tab'),
    ]

    for pattern, elem_type in patterns:
        matches = re.findall(pattern, snapshot_text)
        for match in matches:
            buttons.append({
                "element": match,
                "type": elem_type,
                "ref": f"{elem_type}[{match}]"
            })

    return buttons


def generate_extraction_function(selectors: dict) -> str:
    """
    Generate JavaScript extraction function for browser_evaluate.

    Example:
        selectors = {
            "title": ".product-title",
            "price": ".price",
            "description": ".description"
        }
        print(generate_extraction_function(selectors))
    """
    selector_mappings = ", ".join([
        f'{key}: el.querySelector("{sel}")?.textContent?.trim()'
        for key, sel in selectors.items()
    ])

    return f"""() => {{
    return Array.from(document.querySelectorAll('.item')).map(el => ({{
        {selector_mappings}
    }}));
}}"""


def generate_scroll_function(direction: str = "down", amount: int = 500) -> str:
    """
    Generate scroll JavaScript for browser_evaluate.

    Args:
        direction: "down", "up", "bottom", "top"
        amount: pixels to scroll (for up/down)
    """
    if direction == "bottom":
        return "() => window.scrollTo(0, document.body.scrollHeight)"
    elif direction == "top":
        return "() => window.scrollTo(0, 0)"
    elif direction == "up":
        return f"() => window.scrollBy(0, -{amount})"
    else:  # down
        return f"() => window.scrollBy(0, {amount})"


def generate_wait_for_element_function(selector: str, timeout: int = 10000) -> str:
    """
    Generate JavaScript to wait for element (for browser_evaluate).
    """
    return f"""() => {{
    return new Promise((resolve, reject) => {{
        const timeout = setTimeout(() => reject('Timeout waiting for element'), {timeout});
        const observer = new MutationObserver((mutations, obs) => {{
            const element = document.querySelector('{selector}');
            if (element) {{
                clearTimeout(timeout);
                obs.disconnect();
                resolve(element.textContent);
            }}
        }});
        observer.observe(document.body, {{ childList: true, subtree: true }});

        // Check if already exists
        const existing = document.querySelector('{selector}');
        if (existing) {{
            clearTimeout(timeout);
            observer.disconnect();
            resolve(existing.textContent);
        }}
    }});
}}"""


def generate_playwright_code(actions: list[dict]) -> str:
    """
    Generate Playwright code snippet for browser_run_code.

    Example:
        actions = [
            {"type": "click", "selector": "button[name='Submit']"},
            {"type": "fill", "selector": "input[name='email']", "value": "test@example.com"},
            {"type": "wait", "selector": ".success-message"}
        ]
        print(generate_playwright_code(actions))
    """
    code_lines = ["async (page) => {"]

    for action in actions:
        action_type = action.get("type")
        selector = action.get("selector", "")

        if action_type == "click":
            code_lines.append(f"    await page.locator('{selector}').click();")
        elif action_type == "fill":
            value = action.get("value", "")
            code_lines.append(f"    await page.locator('{selector}').fill('{value}');")
        elif action_type == "wait":
            code_lines.append(f"    await page.locator('{selector}').waitFor();")
        elif action_type == "screenshot":
            filename = action.get("filename", "screenshot.png")
            code_lines.append(f"    await page.screenshot({{ path: '{filename}' }});")
        elif action_type == "evaluate":
            js = action.get("js", "")
            code_lines.append(f"    const result = await page.evaluate(() => {{ {js} }});")

    code_lines.append("    return 'completed';")
    code_lines.append("}")

    return "\n".join(code_lines)


def format_timestamp(fmt: str = "%Y%m%d_%H%M%S") -> str:
    """Generate timestamp for filenames."""
    return datetime.now().strftime(fmt)


def generate_screenshot_filename(prefix: str = "screenshot", ext: str = "png") -> str:
    """Generate unique screenshot filename."""
    return f"{prefix}_{format_timestamp()}.{ext}"


# Example usage templates
TEMPLATES = {
    "login_form": [
        {"name": "Email", "type": "textbox", "ref": "textbox[Email]", "value": ""},
        {"name": "Password", "type": "textbox", "ref": "textbox[Password]", "value": ""},
    ],

    "contact_form": [
        {"name": "Name", "type": "textbox", "ref": "textbox[Name]", "value": ""},
        {"name": "Email", "type": "textbox", "ref": "textbox[Email]", "value": ""},
        {"name": "Subject", "type": "combobox", "ref": "combobox[Subject]", "value": ""},
        {"name": "Message", "type": "textbox", "ref": "textbox[Message]", "value": ""},
    ],

    "registration_form": [
        {"name": "First Name", "type": "textbox", "ref": "textbox[First Name]", "value": ""},
        {"name": "Last Name", "type": "textbox", "ref": "textbox[Last Name]", "value": ""},
        {"name": "Email", "type": "textbox", "ref": "textbox[Email]", "value": ""},
        {"name": "Password", "type": "textbox", "ref": "textbox[Password]", "value": ""},
        {"name": "Confirm Password", "type": "textbox", "ref": "textbox[Confirm Password]", "value": ""},
        {"name": "Accept Terms", "type": "checkbox", "ref": "checkbox[I accept the terms]", "value": "true"},
    ],
}


def get_form_template(template_name: str) -> list[dict]:
    """Get a predefined form template."""
    return TEMPLATES.get(template_name, [])


def fill_form_template(template_name: str, values: dict) -> str:
    """
    Fill a form template with values.

    Example:
        json_fields = fill_form_template("login_form", {
            "Email": "user@example.com",
            "Password": "secretpassword"
        })
    """
    template = get_form_template(template_name)
    for field in template:
        field_name = field["name"]
        if field_name in values:
            field["value"] = str(values[field_name])

    return json.dumps(template, indent=2)


if __name__ == "__main__":
    # Demo usage
    print("=== Form Fields Generator ===")
    fields = [
        {"name": "Username", "ref": "textbox[Username]", "value": "john_doe"},
        {"name": "Email", "ref": "textbox[Email]", "value": "john@example.com"},
        {"name": "Country", "ref": "combobox[Country]", "value": "United States"},
        {"name": "Subscribe", "ref": "checkbox[Subscribe to newsletter]", "value": "true"},
    ]
    print(generate_form_fields(fields))

    print("\n=== Login Template ===")
    print(fill_form_template("login_form", {
        "Email": "demo@example.com",
        "Password": "demopassword"
    }))

    print("\n=== Extraction Function ===")
    print(generate_extraction_function({
        "title": ".product-name",
        "price": ".product-price",
        "rating": ".star-rating"
    }))

    print("\n=== Scroll Functions ===")
    print(f"Scroll to bottom: {generate_scroll_function('bottom')}")
    print(f"Scroll down 300px: {generate_scroll_function('down', 300)}")

    print("\n=== Playwright Code ===")
    print(generate_playwright_code([
        {"type": "fill", "selector": "input[name='email']", "value": "test@test.com"},
        {"type": "click", "selector": "button[type='submit']"},
        {"type": "wait", "selector": ".success"}
    ]))
