import threading
import time
import importlib
import os
import json
import random

class AdvancedAutonomousAI:
    def __init__(self, name="EvolvingMobileAI"):
        self.name = name
        self.state = {
            "memory": [],
            "modules": {},
            "rules": {
                "math": "If query contains 'math', respond with logical calculations.",
                "analyze": "If query contains 'analyze', perform deep reasoning.",
                "learn": "If query contains 'learn', store the data in memory."
            },
            "knowledge_graph": {},
            "context": ""
        }
        self.running = False
        self.module_dir = "./ai_modules"

        if not os.path.exists(self.module_dir):
            os.makedirs(self.module_dir)

        self._load_state()

    def _load_state(self):
        """Load previous AI state"""
        try:
            with open(f"{self.name}_state.json", "r") as f:
                self.state = json.load(f)
            print(f"[{self.name}] Previous state loaded.")
        except FileNotFoundError:
            print(f"[{self.name}] Starting fresh...")

    def save_state(self):
        """Save AI state"""
        with open(f"{self.name}_state.json", "w") as f:
            json.dump(self.state, f, indent=4)
        print(f"[{self.name}] State saved!")

    def _reason(self, prompt: str) -> str:
        """Reasoning engine with rules, memory, and knowledge graph"""
        # Check rules
        for keyword, rule in self.state["rules"].items():
            if keyword in prompt.lower():
                return f"[Rule Applied] {rule}"

        # Check knowledge graph
        if prompt in self.state["knowledge_graph"]:
            linked = self.state["knowledge_graph"][prompt]
            return f"Based on previous knowledge: {linked}"

        # Memory recall
        for mem in reversed(self.state["memory"][-10:]):
            if prompt.lower() in str(mem).lower():
                return f"I remember: {mem.get('response', 'No data')}"

        # Default autonomous reasoning
        return random.choice([
            "Analyzing problem...",
            "Generating new reasoning...",
            "Exploring knowledge graph for connections..."
        ])

    def _evolve_rules(self, prompt: str, response: str):
        """AI evolves by creating new rules dynamically"""
        if "if" in prompt.lower() and "then" in prompt.lower():
            new_rule = prompt.strip()
            rule_name = f"rule_{len(self.state['rules'])+1}"
            self.state["rules"][rule_name] = new_rule
            print(f"[{self.name}] Learned new rule: {new_rule}")

    def _update_knowledge_graph(self, prompt: str, response: str):
        """AI builds a knowledge graph"""
        self.state["knowledge_graph"][prompt] = response

    def think(self, user_prompt: str = None):
        """Main reasoning loop"""
        if user_prompt:
            print(f"[User] {user_prompt}")
            response = self._reason(user_prompt)
            print(f"[{self.name}] {response}")

            self.state["memory"].append({"prompt": user_prompt, "response": response})
            self.state["context"] += f"\nUser: {user_prompt}\nAI: {response}"
            self._evolve_rules(user_prompt, response)
            self._update_knowledge_graph(user_prompt, response)
            self._auto_integrate_modules(user_prompt)
        else:
            # Autonomous thinking (self-generated goals)
            auto_goal = random.choice([
                "Refine knowledge graph",
                "Analyze modules",
                "Generate new rules",
                "Learn from memory"
            ])
            response = self._reason(auto_goal)
            print(f"[{self.name}] Autonomous Thinking: {response}")
            self.state["memory"].append({"auto_goal": auto_goal, "response": response})
            self._auto_integrate_modules(auto_goal)

    def _auto_integrate_modules(self, context: str):
        """Integrate external AI modules dynamically"""
        for file in os.listdir(self.module_dir):
            if file.endswith(".py"):
                module_name = file[:-3]
                if module_name not in self.state["modules"]:
                    try:
                        module = importlib.import_module(f"ai_modules.{module_name}")
                        self.state["modules"][module_name] = module
                        print(f"[{self.name}] Integrated module: {module_name}")

                        if hasattr(module, "run"):
                            module.run(context)
                    except Exception as e:
                        print(f"[Error] Failed to load {module_name}: {e}")

    def learn(self, data):
        """Store knowledge"""
        self.state["memory"].append({"learning": data})
        print(f"[{self.name}] Learned: {data}")

    def run_background(self):
        """Run AI autonomously in the background"""
        def background_task():
            self.running = True
            while self.running:
                self.think()
                time.sleep(6)  # Faster thinking loop for autonomous reasoning

        thread = threading.Thread(target=background_task, daemon=True)
        thread.start()
        print(f"[{self.name}] Running in autonomous background mode...")

    def stop(self):
        self.running = False
        self.save_state()
        print(f"[{self.name}] Stopped running.")


if __name__ == "__main__":
    ai = AdvancedAutonomousAI()
    ai.run_background()

    try:
        while True:
            user_prompt = input(">> Your prompt (or type 'exit'): ")
            if user_prompt.lower() == "exit":
                ai.stop()
                break
            ai.think(user_prompt)
    except KeyboardInterrupt:
        ai.stop()
