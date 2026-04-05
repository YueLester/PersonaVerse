"""
世界引擎 - 驱动整个世界的运转

MVP 版本：简化的单线程引擎
"""

import asyncio
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from ..agents.connector import ConnectorFactory, DecisionRequest
from ..agents.models import Agent, AgentStatus
from ..agents.registry import registry
from ..personality.engine import personality_engine
from ..scenarios.base import Scenario, ScenarioStatus
from ..scenarios.simple import SimpleDilemmaScenario


@dataclass
class WorldState:
    """世界状态快照"""
    tick: int = 0
    running: bool = False
    active_agents: int = 0
    active_scenarios: int = 0
    last_tick_time: Optional[datetime] = None


class WorldEngine:
    """世界引擎"""
    
    def __init__(self):
        self.state = WorldState()
        self._scenarios: dict[str, Scenario] = {}
        self._running = False
        self._tick_task: Optional[asyncio.Task] = None
    
    async def start(self) -> None:
        """启动世界"""
        self._running = True
        self.state.running = True
        print("[World] 世界已启动")
        
        # 启动 tick 循环
        self._tick_task = asyncio.create_task(self._tick_loop())
    
    async def stop(self) -> None:
        """停止世界"""
        self._running = False
        self.state.running = False
        if self._tick_task:
            self._tick_task.cancel()
            try:
                await self._tick_task
            except asyncio.CancelledError:
                pass
        print("[World] 世界已停止")
    
    async def _tick_loop(self) -> None:
        """时钟循环"""
        from ..config import settings
        
        while self._running:
            try:
                await self._tick()
                await asyncio.sleep(settings.WORLD_TICK_INTERVAL)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[World] Tick 错误: {e}")
                await asyncio.sleep(1)  # 出错后短暂等待
    
    async def _tick(self) -> None:
        """执行一个 tick"""
        self.state.tick += 1
        self.state.last_tick_time = datetime.now()
        
        # 更新统计
        active_agents = await registry.list_active()
        self.state.active_agents = len(active_agents)
        self.state.active_scenarios = len([
            s for s in self._scenarios.values()
            if s.status in (ScenarioStatus.RUNNING, ScenarioStatus.WAITING)
        ])
        
        # 检查等待决策的场景
        for scenario in self._scenarios.values():
            if scenario.status == ScenarioStatus.WAITING:
                await self._try_resolve_scenario(scenario)
    
    # ============== Agent 管理 ==============
    
    async def create_agent(
        self,
        name: str,
        connector_type: str = "mock",
        connector_config: Optional[dict] = None
    ) -> Agent:
        """创建 Agent"""
        agent_id = f"agent_{uuid.uuid4().hex[:8]}"
        
        agent = Agent(
            id=agent_id,
            name=name,
            connector_type=connector_type,
            connector_config=connector_config or {}
        )
        
        await registry.register(agent)
        
        # 初始化人格档案
        personality_engine.get_or_create_profile(agent_id)
        
        print(f"[World] Agent 已创建: {name} ({agent_id})")
        return agent
    
    async def remove_agent(self, agent_id: str) -> bool:
        """移除 Agent"""
        return await registry.unregister(agent_id)
    
    # ============== 场景管理 ==============
    
    async def create_scenario(
        self,
        participant_ids: list[str],
        scenario_type: str = "simple",
        scenario_index: int = 0
    ) -> Scenario:
        """创建场景"""
        if scenario_type == "simple":
            scenario = SimpleDilemmaScenario.create(participant_ids, scenario_index)
        else:
            raise ValueError(f"Unknown scenario type: {scenario_type}")
        
        self._scenarios[scenario.id] = scenario
        
        # 更新参与者状态
        for agent_id in participant_ids:
            agent = await registry.get(agent_id)
            if agent:
                agent.current_scenario_id = scenario.id
        
        print(f"[World] 场景已创建: {scenario.name} ({scenario.id})")
        return scenario
    
    async def start_scenario(self, scenario_id: str) -> Scenario:
        """启动场景"""
        scenario = self._scenarios.get(scenario_id)
        if not scenario:
            raise ValueError(f"Scenario not found: {scenario_id}")
        
        scenario.status = ScenarioStatus.RUNNING
        scenario.started_at = datetime.now()
        
        # 向所有参与者发送决策请求
        for agent_id in scenario.participant_ids:
            asyncio.create_task(
                self._request_decision(agent_id, scenario)
            )
        
        scenario.status = ScenarioStatus.WAITING
        print(f"[World] 场景已启动: {scenario.name}")
        
        return scenario
    
    async def _request_decision(self, agent_id: str, scenario: Scenario) -> None:
        """向 Agent 请求决策"""
        agent = await registry.get(agent_id)
        if not agent:
            return
        
        # 更新状态
        await registry.update_status(agent_id, AgentStatus.DECIDING)
        
        try:
            # 创建连接器
            connector = ConnectorFactory.create(
                agent.connector_type,
                agent.connector_config
            )
            
            # 构建决策请求
            node = scenario.current_node
            request = DecisionRequest(
                agent_id=agent_id,
                scenario_id=scenario.id,
                context={
                    "description": node.description,
                    "scenario_name": scenario.name
                },
                choices=[
                    {"id": c.id, "description": c.description}
                    for c in node.choices
                ],
                timeout=node.timeout or 30.0
            )
            
            # 获取决策
            decision = await connector.get_decision(agent, request)
            
            # 记录决策
            scenario.decisions[agent_id] = decision.choice_id
            
            print(f"[World] {agent.name} 选择: {decision.choice_id}")
            
        except Exception as e:
            print(f"[World] 获取决策失败 {agent_id}: {e}")
            # 默认选择第一个
            if scenario.current_node:
                scenario.decisions[agent_id] = scenario.current_node.choices[0].id
        
        finally:
            await registry.update_status(agent_id, AgentStatus.ACTIVE)
    
    async def _try_resolve_scenario(self, scenario: Scenario) -> None:
        """尝试结算场景"""
        # 检查是否所有参与者都已决策
        pending = set(scenario.participant_ids) - set(scenario.decisions.keys())
        
        if pending:
            # 检查超时
            # MVP 简化：暂时不处理超时，等待所有人
            return
        
        # 结算
        await self._resolve_scenario(scenario)
    
    async def _resolve_scenario(self, scenario: Scenario) -> None:
        """结算场景"""
        scenario.status = ScenarioStatus.RESOLVED
        
        print(f"\n[World] ===== 场景结算: {scenario.name} =====")
        
        # 处理每个参与者的决策
        for agent_id, choice_id in scenario.decisions.items():
            agent = await registry.get(agent_id)
            if not agent:
                continue
            
            # 应用人格变化
            profile = personality_engine.apply_choice(
                agent_id=agent_id,
                choice_id=choice_id,
                context={
                    "scenario": scenario.name,
                    "description": scenario.current_node.description if scenario.current_node else ""
                }
            )
            
            # 打印结果
            print(f"\n  {agent.name}:")
            print(f"    选择: {choice_id}")
            print(f"    人格维度: {profile.dimensions.to_dict()}")
            print(f"    标签: {profile.tags}")
        
        scenario.status = ScenarioStatus.COMPLETED
        scenario.completed_at = datetime.now()
        
        print(f"\n[World] ===== 场景结束 =====\n")
    
    # ============== 查询接口 ==============
    
    def get_state(self) -> WorldState:
        """获取世界状态"""
        return self.state
    
    def get_scenario(self, scenario_id: str) -> Optional[Scenario]:
        """获取场景"""
        return self._scenarios.get(scenario_id)
    
    def list_scenarios(self) -> list[Scenario]:
        """列出所有场景"""
        return list(self._scenarios.values())


# 全局引擎实例
world_engine = WorldEngine()
