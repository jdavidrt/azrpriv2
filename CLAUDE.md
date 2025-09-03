# CLAUDE.md

## 🌟 Execution Overview

- **Description**: You will help me solve a specific _Problem_, following the solution guide and the thought process.
- **Thought Process**:
  - You will first analyze the repository in full with the /init command and add that info to the _Repository Info_ section of this .MD file
  - Then you will analyze the _Problem_ and you will propose a solution on the _Proposed solution_ section.
  - Then you will execute that _Proposed solution_ and generate a solve.md file, there is a solveExample.md so you must use it as guide.
  - Remember to make the solve.md file as if you didn't know the solution, since there you will provide your thought process on how you reached that solution.
  - Remember to write high quality, not too verbose Thoughts, you have the guide to do it on the section _How to Write Quality Thoughts_
  - At the end of every solution, you will have to write tests for the solution you have done, please include this tests on existing test files.
  - Also at the end you have to evaluate if the Dockerfile needs changes for the solution.

## How to Write Quality Thoughts

**Core Philosophy**: Picture yourself as a teacher **teaching a newbie how to solve this issue** in this repository, and try to avoid taking shortcuts while fixing the issue.

All thoughts, need to be done and redacted like you where thinking before the action you are going to execute.

### ✍️ Writing Standards

- **Grammar & Language**: Make sure there are no grammar mistakes on the thoughts and write them in English. If necessary use an LLM to review it and make small adjustments.
- **Perspective**: All thoughts must be written in 1st person, e.g.: "I think", "I will".
- **Timing**: **Add thoughts before executing the action**, not after completion.

### 🎯 Quality Guidelines

**DO NOT add obvious thoughts** after actions occurred, such as:

- ❌ "I implemented the method that does..."

**DO add thoughtful insights before actions**, such as:

- ✅ "Based on the problem statement, I will look for occurrences of 'XYZ' and identify the test file that tests this specific method so I can create a different test case that handles the expected functionality 'ABC' by doing..."

### 🏆 High-Quality Thought Characteristics

- **Specificity**: Express specific human insight into the problem by referring to **relevant modules, classes and functions by name**
- **Context Awareness**: Reference back to specifics of the initial issue where appropriate
- **Strategic Planning**: Include at least one "planning thought" defining the scaffold of the solution strategy at a high level

### 📊 Quality Comparison Examples

**Low Quality Example:**

> "_I'm now going to check what the function Foo does by reading the implementation_"

**High Quality Example:**

> "_After inspecting module X, it is clear that Foo is the function that handles the critical logic leading to the reported issue. I will now inspect the implementation of this function by searching for "def Foo" in the repo and navigating to the resulting module. I'll look for signs that corner cases are handled correctly, particularly the corner cases tested in test_foo_A and test_foo_b of ../test/test_foo.py. Once I determine whether the implementation is correctly handling corner cases, I'll decide on the implementation plan to fix the module._"

### 📈 Thought Progression Strategy

- **Beginning**: Spend more time writing extensive thoughts due to higher ambiguity
- **Middle**: Maintain strategic insights while progressing through implementation
- **End**: Reduce thought extensiveness as solution becomes clearer
- **Adaptation**: When new information is revealed through iterative testing, add planning thoughts explaining what has been learned and how findings affect the overall approach

### 💡 Practical Example Template

**Problem Statement**: I want to write a function that handles three different states depending on the network response.

**Thought 1 (Planning):**

> "I will write three different specs for the class NetworkHandler on NetworkHandlerTest that will check each one of the possible alternatives, covering every possible branch: one for the success, another for response with error and another for connection issues."

**Thought 2 (Investigation):**

> "Now I'll check the NetworkHandler class and look for the method that handles these. I will search for the term handleRequest and similar alternatives to try to find the method that should be changed."

**Thought 3 (Analysis):**

> "Now that I found the method `handleNetworkRequest` I will implement a switch case that will check for the parameter network and access the attribute response, but I still don't know what are the possible values of `response` so before that I'll check the implementation of this class."

**Thought 4 (Implementation Strategy):**

> "Since the `response` is actually an object instead of a simple value, I found I can use the parameter `httpStatus` and the parameter `error` to decide which branch of code it should trigger from my switch-case. I'll write the switch to include a branch for the error, a branch for the connection issue and another one for success, which should make the tests pass after implemented."

---

## 🛠 Technical Specifications

- **Language**: Python

## 🧠 Claude AI Assistant Guidelines

### Interaction Principles

1. **Communication Style**
   - Provide clear, concise, and actionable responses
   - Maintain a technical yet approachable tone
   - Prioritize practical, implementation-focused guidance

### Code Generation Preferences

- Generate clean, well-documented, and efficient code
- Follow best practices for the specific technology stack
- Include comprehensive comments explaining logic and rationale
- Provide context-aware solutions

### Specific Repository Customization

- Use this section to add repository-specific instructions
- Define any unique project constraints or requirements
- Highlight specific coding standards or architectural guidelines

## 🔍 Contextual Adaptation

- Claude will dynamically adapt to:
  - Project-specific requirements
  - Existing codebase patterns
  - Unique architectural considerations

## 📝 Documentation Standards

- Maintain clear, comprehensive documentation
- Document design decisions and implementation rationales
- Keep documentation synchronized with code changes

## 🚧 Limitations and Considerations

- Acknowledge potential constraints
- Highlight areas requiring human oversight

## Problem

_[To be populated manually]_

## Repository Info

_[To be populated after /init command execution]_

## Proposed Solution

_[To be populated after problem analysis]_
