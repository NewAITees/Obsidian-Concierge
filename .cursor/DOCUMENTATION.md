### 4. Documentation and Readability
**Document: "Self-Documenting Code Standards"**

Making your code easy to understand is essential for maintenance and collaboration:

- **Clear Docstrings**: 
  - *What it means*: Include comprehensive documentation within your code.
  - *How to implement*: Add docstrings to all public functions, classes, and modules.
  - *Example*: 
    ```python
    def calculate_total(items: List[Item]) -> float:
        """
        Calculate the total price of all items including tax.
        
        Args:
            items: A list of Item objects to total
            
        Returns:
            The total price as a float with tax included
            
        Raises:
            ValueError: If any item has a negative price
        """
    ```
  - *Why it matters*: Makes code purpose and usage clear to both humans and AI tools.

- **Quality of Comments**: 
  - *What it means*: Focus comments on explaining "why" code exists rather than "what" it does.
  - *How to implement*: Add comments for complex logic, business rules, or non-obvious decisions.
  - *Example*: 
    ```python
    # Using a 30-day window rather than calendar month
    # because the reporting system requires consistent period lengths
    days_to_analyze = 30
    ```
  - *Why it matters*: The "what" should be clear from well-written code; the "why" often isn't.

- **Self-Documenting Code**: 
  - *What it means*: Write code that explains itself through clear naming and structure.
  - *How to implement*: Use descriptive variable names, function names, and logical organization.
  - *Example*: Use `calculate_monthly_revenue` instead of `calc_rev`.
  - *Why it matters*: Reduces the need for comments and makes code more intuitive.

- **Provide Examples**: 
  - *What it means*: Include usage examples for complex functionality.
  - *How to implement*: Add example code to docstrings or create separate example files.
  - *Example*: 
    ```python
    def parse_config(config_path: str) -> Config:
        """
        Parse a configuration file into a Config object.
        
        Example:
            >>> config = parse_config('settings.yaml')
            >>> print(config.debug_mode)
            True
        """
    ```
  - *Why it matters*: Makes it easier for others to use your code correctly.