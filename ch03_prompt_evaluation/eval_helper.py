import json
import re
import ast

from statistics import mean

from chat_helper import ChatHelper

class EvalHelper:

    def __init__(self, client, model):
        self.chat_helper = ChatHelper(client, model)


    # Generate a dataset for evaluation
    def generate_dataset(self):
        prompt = """
            Generate an evaluatin dataset for prompt evaluation. 
            The dataset will be used to evaluate prompts that generate Python, JSON, or Regex specifically for AWS-related tasks. 
            Generate an array of JSON, each representing a task that requires Python, JSON, or Regex to complete.
            For each task, include solution criteria.
            
            Example output:
            ```json
            [
                {
                    "task": "Description of task",
                    "format": "json" or "python" or "regex",
                    "solution_crieteria": "Solution criteria to be satisfied."
                }
                ... additional
            ]
            ```
            
            * Focus on tasks that can be solved by writing a single Python function, a single JSON object, or a single Regex.
            * Focus on tasks that do not require wrinting much code.
            
            Please generate 3 objects.
            """

        messages = []
        
        self.chat_helper.add_user_message(messages, prompt)
        self.chat_helper.add_assistant_message(messages, "```json")
        
        text = self.chat_helper.chat(messages, stop_sequences=["```"])
        
        return json.loads(text)  


    # Save the dataset to a file
    def save_dataset(self, dataset):
        with open("dataset.json", "w") as f:
            json.dump(dataset, f, indent=2)


    # Run prompt and get response        
    def run_prompt(self, test_case):
        """Merges the prompt and test case input, then returns the result"""
        
        prompt = f"""
            Please solve the following task:
    
            {test_case["task"]}

            * Respond only with Python, JSON, or plain Regex.
            * Do not add any comments, commentary, or explanation.
            """

        messages = []
        
        self.chat_helper.add_user_message(messages, prompt)
        self.chat_helper.add_assistant_message(messages, "```code")
        
        output = self.chat_helper.chat(messages, stop_sequences=["```"])
        
        return output


    # Run a test case
    def run_test_case(self, test_case):
        """Calls run_prompt, then grades the result"""

        output = self.run_prompt(test_case)

        # Grading
        model_grade = self.grade_by_model(test_case, output)
        model_score = model_grade["score"]
        reasoning = model_grade["reasoning"]

        syntax_score = self.grade_syntax(test_case, output)

        score = (model_score + syntax_score) / 2

        return {
            "test_case": test_case,
            "output": output,
            "score": score,
            "reasoning": reasoning
        }


    # Run an evaluation
    def run_eval(self, dataset):
        """Load the dataset, then calls run_test_case with each case"""

        results = []

        for test_case in dataset:
            result = self.run_test_case(test_case)
            results.append(result)

        average_score = mean(result["score"] for result in results) 
        print(f"Average Score: {average_score}")
            
        return results


    # Grade the output using a model
    def grade_by_model(self, test_case, output):
        eval_prompt = f"""
        You aren an expert AWS code reviewer. Your task is to evaluate the following AI-generated solution.
        
        Original Task:
        <task>
        {test_case["task"]}
        </task>

        Solution to Evaluate:
        <solution>
        {output}
        </solution>

        Solution Criteria:
        <criteria>
        {test_case["solution_criteria"]}
        </criteria>

        Check if all solution criteria have been satisfied.

        Output Format:
        Provide your evaluation as a structured JSON object with the following fields, in this specific order:
        - "strengths": An array of 1-3 key areas of strength
        - "weaknesses": An array of 1-3 key areas for improvement
        - "reasoning": A concise explanation of your overall assessment
        - "score": A number between 1 and 10

        Respond with JSON. Keep your response concise and direct.
        Example response shape:
        {{
            "strengths": string[],
            "weaknesses": string[],
            "reasoning": string,
            "score": number
        }}
        """

        messages = []
        
        self.chat_helper.add_user_message(messages, eval_prompt)
        self.chat_helper.add_assistant_message(messages, "```json")
        eval_text = self.chat_helper.chat(messages, stop_sequences=["```"])

        return json.loads(eval_text)


    # Validate JSON output format
    def validate_json(self, text):
        try:
            json.loads(text.strip())
            return 10
        except json.JSONDecodeError:
            return 0


    # Validate Python output format
    def validate_python(self, text):
        try:
            ast.parse(text.strip())
            return 10
        except SyntaxError:
            return 0


    # Validate Regex output format
    def validate_regex(self, text):
        try:
            re.compile(text.strip())
            return 10
        except re.error:
            return 0


    # Grade output syntax
    def grade_syntax(self, test_case, response):
        format = test_case["format"]
        if format == "json":
            return self.validate_json(response)
        elif format == "python":
            return self.validate_python(response)
        else:
            return self.validate_regex(response)
            