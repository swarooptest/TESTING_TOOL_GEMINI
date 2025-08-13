from ai_engine.gemini_client import GeminiClient
from ai_engine.test_generator import TestGenerator
from runner.test_runner import TestRunner
from config import BASE_URL

def main():
    goal = input("Enter your testing goal:")

    print("[AI] Generating test code...")
    ai_client = GeminiClient()
    code = ai_client.generate_test_code(goal, BASE_URL)

    print("[System] Saving generated test...")
    generator = TestGenerator()
    test_file = generator.save_test(code, "test_generated_login.py")

    print("[Runner] Executing generated test...")
    runner = TestRunner()
    runner.run_tests(test_file)

if __name__ == "__main__":
    main()
