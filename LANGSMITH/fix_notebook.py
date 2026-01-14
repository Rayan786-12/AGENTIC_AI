import json
import os

nb_path = r"c:\Users\Rayan Ahmed.R\Downloads\LANGSMITH\multiagent.ipynb"

if not os.path.exists(nb_path):
    print(f"Error: File not found at {nb_path}")
    exit(1)

try:
    with open(nb_path, "r", encoding="utf-8") as f:
        nb = json.load(f)

    modified = False
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            source_str = "".join(cell["source"])
            if "class SupervisorState(MessagesState):" in source_str:
                # Target cell found.
                print("Found SupervisorState class definition.")
                
                # We replace the source with the corrected version including next_agent and current_task
                new_source = [
                    "from typing import Dict,List,Any\n",
                    "from langchain_core.messages import AIMessage\n",
                    "\n",
                    "class SupervisorState(MessagesState):\n",
                    "    \"\"\"State for the supervisor multi-agent system\"\"\"\n",
                    "    current_agent: str = \"\"\n",
                    "    task_assingments: Dict[str,List[str]] = {}\n",
                    "    agent_outputs: Dict[str,Any] = {}\n",
                    "    workflow_stage: str = \"initial\"\n",
                    "    iteration_count: int = 0\n",
                    "    max_interations: int = 10\n",
                    "    final_output: str = \"\"\n",
                    "    next_agent: str = \"\"\n",
                    "    current_task: str = \"\""
                ]
                
                # Check if modification is needed
                if cell["source"] != new_source:
                    cell["source"] = new_source
                    modified = True
                    print("Applied fix to SupervisorState.")
                else:
                    print("SupervisorState already up to date.")
                break
    
    if modified:
        with open(nb_path, "w", encoding="utf-8") as f:
            json.dump(nb, f, indent=1)
        print("Notebook saved successfully.")
    else:
        print("No changes needed.")

except Exception as e:
    print(f"An error occurred: {e}")
