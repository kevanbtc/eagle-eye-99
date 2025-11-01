"""
Eagle Eye Agent Executor
Runs trained agents (OpenAI, Ollama, HuggingFace) with MCP tools and memory
"""

import json
import uuid
import sys
from datetime import datetime
from typing import Optional, Dict, List, Any, Callable
from enum import Enum
from dataclasses import dataclass, field, asdict
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import get_settings


# ============================================================================
# AGENT STATE & MEMORY MANAGEMENT
# ============================================================================

class AgentRole(Enum):
    """Agent specialization roles"""
    ORCHESTRATOR = "orchestrator"  # Coordinates full workflow
    COMPLIANCE = "compliance"       # Focuses on code checks
    PRICING = "pricing"             # Focuses on cost estimation
    PROPOSAL = "proposal"           # Focuses on client communications


@dataclass
class ConversationMessage:
    """Single message in agent conversation history"""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_results: Optional[List[Dict[str, Any]]] = None


@dataclass
class AgentMemory:
    """Persistent memory for agent operations"""
    agent_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    conversation_history: List[ConversationMessage] = field(default_factory=list)
    decision_log: List[Dict[str, Any]] = field(default_factory=list)
    tool_call_log: List[Dict[str, Any]] = field(default_factory=list)
    error_log: List[Dict[str, Any]] = field(default_factory=list)
    project_context: Dict[str, Any] = field(default_factory=dict)
    execution_state: str = "idle"  # idle, running, completed, error

    def add_message(self, role: str, content: str, tool_calls=None, tool_results=None):
        """Add message to conversation history"""
        msg = ConversationMessage(
            role=role,
            content=content,
            tool_calls=tool_calls,
            tool_results=tool_results
        )
        self.conversation_history.append(msg)

    def log_decision(self, decision: str, reasoning: str, outcome: str):
        """Log a decision made by the agent"""
        self.decision_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "decision": decision,
            "reasoning": reasoning,
            "outcome": outcome
        })

    def log_tool_call(self, tool_name: str, input_params: Dict, result: Any, duration_ms: float):
        """Log tool execution"""
        self.tool_call_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "tool": tool_name,
            "input": input_params,
            "result": result,
            "duration_ms": duration_ms
        })

    def log_error(self, error_type: str, message: str, recovery_action: Optional[str] = None):
        """Log error and recovery"""
        self.error_log.append({
            "timestamp": datetime.utcnow().isoformat(),
            "type": error_type,
            "message": message,
            "recovery_action": recovery_action
        })

    def save(self, output_dir: str = "./.agent_memory"):
        """Save memory to disk"""
        Path(output_dir).mkdir(exist_ok=True)
        filepath = Path(output_dir) / f"{self.agent_id}.json"
        
        # Convert dataclasses to dicts
        memory_dict = {
            "agent_id": self.agent_id,
            "conversation_history": [asdict(msg) for msg in self.conversation_history],
            "decision_log": self.decision_log,
            "tool_call_log": self.tool_call_log,
            "error_log": self.error_log,
            "project_context": self.project_context,
            "execution_state": self.execution_state
        }
        
        with open(filepath, 'w') as f:
            json.dump(memory_dict, f, indent=2)
        
        return str(filepath)

    @classmethod
    def load(cls, filepath: str) -> "AgentMemory":
        """Load memory from disk"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        memory = cls(agent_id=data["agent_id"])
        
        # Reconstruct conversation history
        for msg_data in data.get("conversation_history", []):
            msg = ConversationMessage(
                role=msg_data["role"],
                content=msg_data["content"],
                timestamp=msg_data.get("timestamp"),
                tool_calls=msg_data.get("tool_calls"),
                tool_results=msg_data.get("tool_results")
            )
            memory.conversation_history.append(msg)
        
        memory.decision_log = data.get("decision_log", [])
        memory.tool_call_log = data.get("tool_call_log", [])
        memory.error_log = data.get("error_log", [])
        memory.project_context = data.get("project_context", {})
        memory.execution_state = data.get("execution_state", "idle")
        
        return memory


# ============================================================================
# AGENT EXECUTOR
# ============================================================================

class EagleEyeAgent:
    """Main agent executor for autonomous operation"""

    def __init__(
        self,
        role: AgentRole = AgentRole.ORCHESTRATOR,
        llm_provider: str = "openai",  # openai, ollama, huggingface
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        memory: Optional[AgentMemory] = None
    ):
        """
        Initialize agent
        
        Args:
            role: Agent specialization
            llm_provider: Which LLM to use
            model: Specific model (uses default if None)
            api_key: API key (uses config if None)
            memory: Existing memory (creates new if None)
        """
        self.role = role
        self.llm_provider = llm_provider
        self.memory = memory or AgentMemory()
        
        # Load settings from config
        settings = get_settings()
        
        # Configure based on provider
        if llm_provider == "openai":
            self.model = model or settings.openai.model
            self.api_key = api_key or settings.openai.api_key
            self.base_url = "https://api.openai.com/v1"
        elif llm_provider == "ollama":
            self.model = model or settings.ollama.model
            self.api_key = settings.ollama.api_token
            self.base_url = settings.ollama.base_url
        elif llm_provider == "huggingface":
            self.model = model or settings.huggingface.model
            self.api_key = api_key or settings.huggingface.api_key
            self.base_url = "https://api-inference.huggingface.co"
        else:
            raise ValueError(f"Unknown LLM provider: {llm_provider}")
        
        self.tool_registry = {}

    def register_tool(self, name: str, handler: Callable):
        """Register a tool handler"""
        self.tool_registry[name] = handler

    def build_system_prompt(self) -> str:
        """Build system prompt based on role"""
        from agents.agent_training import (
            SYSTEM_PROMPT_BASE,
            SYSTEM_PROMPT_COMPLIANCE,
            SYSTEM_PROMPT_PRICING,
            SYSTEM_PROMPT_PROPOSAL,
            TOOL_SPECS
        )
        
        base = SYSTEM_PROMPT_BASE
        
        if self.role == AgentRole.COMPLIANCE:
            base += "\n" + SYSTEM_PROMPT_COMPLIANCE
        elif self.role == AgentRole.PRICING:
            base += "\n" + SYSTEM_PROMPT_PRICING
        elif self.role == AgentRole.PROPOSAL:
            base += "\n" + SYSTEM_PROMPT_PROPOSAL
        
        # Add tools available to this agent
        base += "\n\n## Tool Specifications\n"
        base += "```json\n"
        base += json.dumps(TOOL_SPECS, indent=2)
        base += "\n```"
        
        return base

    def format_tools_for_llm(self) -> List[Dict[str, Any]]:
        """Format registered tools for LLM provider"""
        from agents.agent_training import format_tool_spec_for_agent, TOOL_SPECS
        
        all_tools = []
        
        # Flatten tool specs by category
        for category, tools in TOOL_SPECS.items():
            for tool_spec in tools:
                formatted = format_tool_spec_for_agent(tool_spec, self.llm_provider)
                all_tools.append(formatted)
        
        return all_tools

    async def execute_workflow(
        self,
        workflow_name: str,
        workflow_params: Dict[str, Any],
        max_iterations: int = 10
    ) -> Dict[str, Any]:
        """
        Execute a workflow with the agent
        
        Args:
            workflow_name: Name of workflow template
            workflow_params: Parameters for workflow
            max_iterations: Max turns before stopping
        
        Returns:
            Workflow execution result
        """
        from agents.agent_training import WORKFLOW_TEMPLATES
        
        if workflow_name not in WORKFLOW_TEMPLATES:
            raise ValueError(f"Unknown workflow: {workflow_name}")
        
        workflow = WORKFLOW_TEMPLATES[workflow_name]
        self.memory.execution_state = "running"
        self.memory.project_context = workflow_params
        
        result = {
            "workflow": workflow_name,
            "status": "completed",
            "steps_executed": [],
            "output": {},
            "errors": []
        }
        
        # TODO: Implement actual workflow execution
        # This would call the LLM in a loop, handle tool calls, etc.
        
        self.memory.execution_state = "completed"
        self.memory.save()
        
        return result

    def handle_tool_call(self, tool_name: str, params: Dict[str, Any]) -> Any:
        """Handle a tool call from the LLM"""
        if tool_name not in self.tool_registry:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        try:
            result = self.tool_registry[tool_name](params)
            self.memory.log_tool_call(tool_name, params, result, 0)  # TODO: actual duration
            return result
        except Exception as e:
            self.memory.log_error("tool_call_error", str(e))
            raise

    def get_conversation_history(self) -> str:
        """Format conversation history for context"""
        lines = []
        for msg in self.memory.conversation_history:
            lines.append(f"{msg.role.upper()}: {msg.content}")
            if msg.tool_calls:
                lines.append(f"[Tool calls: {json.dumps(msg.tool_calls)}]")
            if msg.tool_results:
                lines.append(f"[Tool results: {json.dumps(msg.tool_results)}]")
        return "\n".join(lines)

    def get_execution_report(self) -> Dict[str, Any]:
        """Generate execution report with audit trail"""
        return {
            "agent_id": self.memory.agent_id,
            "role": self.role.value,
            "llm_provider": self.llm_provider,
            "model": self.model,
            "execution_state": self.memory.execution_state,
            "conversation_turns": len(self.memory.conversation_history),
            "tool_calls": len(self.memory.tool_call_log),
            "decisions": len(self.memory.decision_log),
            "errors": len(self.memory.error_log),
            "decision_log": self.memory.decision_log,
            "tool_call_log": self.memory.tool_call_log,
            "error_log": self.memory.error_log,
            "project_context": self.memory.project_context
        }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("EAGLE EYE AGENT EXECUTOR")
    print("=" * 80)
    print()
    
    # Create agents for different roles
    print("Creating Agents")
    print("-" * 80)
    
    orchestrator = EagleEyeAgent(
        role=AgentRole.ORCHESTRATOR,
        llm_provider="openai"
    )
    print(f"[+] Orchestrator Agent (OpenAI: {orchestrator.model})")
    
    compliance = EagleEyeAgent(
        role=AgentRole.COMPLIANCE,
        llm_provider="ollama"
    )
    print(f"[+] Compliance Agent (Ollama: {compliance.model})")
    
    pricing = EagleEyeAgent(
        role=AgentRole.PRICING,
        llm_provider="huggingface"
    )
    print(f"[+] Pricing Agent (HuggingFace: {pricing.model})")
    
    print()
    print("SUCCESS: Agents ready for deployment!")
    print("=" * 80)
