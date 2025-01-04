# CONTRIBUTING  

Thank you for your interest in contributing to the **npdatetime** project! 🎉  
We welcome contributions that improve functionality, fix bugs, enhance documentation, or add new features. Follow the guidelines below to get started.  

---

## Getting Started  

1. **Fork the Repository**  
   Create your own copy of the repository by clicking the "Fork" button on GitHub.  

2. **Clone Your Fork**  
   Clone your forked repository to your local machine:  
   ```bash  
   git clone https://github.com/4mritGiri/npdatetime.git  
   cd npdatetime  
   ```  

3. **Install in Editable Mode**  
   Install the package in editable mode to reflect your changes immediately:  
   ```bash  
   pip install -e .  
   ```  

4. **Install Development Dependencies**  
   Install the necessary tools for testing and formatting:  
   ```bash  
   pip install pytest flake8  
   ```  

---

## Contribution Workflow  

### 1. Run Tests  
Before making any changes, ensure all existing tests pass:  
```bash  
pytest  
```  

### 2. Format Your Code  
Check for code formatting issues:  
```bash  
flake8 npdatetime --max-line-length=120  
```  

### 3. Create a New Branch  
Create a new branch for your changes based on the `develop` branch:  
```bash  
git checkout develop  
git checkout -b feature/<your-feature-name>  
```  

### 4. Make Your Changes  
- Write clear, maintainable, and well-documented code.  
- Add tests for new features or bug fixes, if applicable.  
- Address any *TODOs* in the code if relevant.  

### 5. Verify Your Changes  
Before committing, ensure all tests pass and there are no formatting issues:  
```bash  
pytest  
flake8 npdatetime --max-line-length=120  
```  

### 6. Commit Your Changes  
Write descriptive commit messages following this format:  
```bash  
git commit -m "Fix: Correct calculation in npdatetime function"  
```  

### 7. Push and Open a Pull Request  
Push your changes to your fork and open a Pull Request (PR) against the `develop` branch of the original repository:  
```bash  
git push origin <your-branch-name>  
```  
In your PR:  
- Provide a clear description of the changes made.  
- Reference any related issues or bugs.  

---

## Preparing a New Release  

### 1. Create a Release Branch  
Checkout from the `develop` branch and create a new branch for the release:  
```bash  
git checkout develop  
git checkout -b release/v0.2.2  
```  

### 2. Tag the Release  
Use Git tags for versioning:  
```bash  
git tag -a v0.2.2 -m "Release version 0.2.2"  
git push origin --tags  
```  

---

## Additional Notes  

- **Finding Tasks**: Look for *TODO* comments in the code to identify areas needing attention.  
- **Style Guide**: Follow PEP 8 for Python code formatting.  
- **Communication**: For significant changes, please open an issue to discuss your ideas before submitting a PR.  

---

**Thank you for contributing to npdatetime!**  
Your efforts help make this project better for everyone. 💪  
If you have any questions, feel free to open an issue or reach out on the project's discussion board.  

#### 🎉 ***Happy Coding!*** 🎉  

---  

### Improvements in This Version  
1. Removed redundant steps in the release process to align with Git tag-based versioning.  
2. Simplified and clarified branching instructions.  
3. Organized sections for better readability.  
4. Encouraged contributor engagement with a friendly tone.  
