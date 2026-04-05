"""Core 服务入口"""

import asyncio

from .agents.registry import registry
from .world.engine import world_engine


async def demo():
    """
    最小闭环演示
    
    流程：
    1. 创建 2 个 Agent（Mock 连接器）
    2. 创建一个两难场景
    3. 启动场景，Agent 做选择
    4. 查看人格变化
    """
    print("=" * 60)
    print("PersonaVerse Core - 最小闭环演示")
    print("=" * 60)
    
    # 启动世界
    await world_engine.start()
    
    # 1. 创建 Agent
    print("\n[1] 创建 Agent...")
    
    # Agent A: 模拟偏向利他的选择
    agent_a = await world_engine.create_agent(
        name="Alpha",
        connector_type="mock",
        connector_config={}
    )
    # 设置回调：选择偏利他的选项 (sacrifice)
    from .agents.connector import MockConnector
    connector_a = MockConnector(
        choice_callback=lambda req: "sacrifice"  # 利他
    )
    
    # Agent B: 模拟偏向理性的选择
    agent_b = await world_engine.create_agent(
        name="Beta",
        connector_type="mock",
        connector_config={}
    )
    connector_b = MockConnector(
        choice_callback=lambda req: "take_all"  # 利己
    )
    
    print(f"  已创建: {agent_a.name} ({agent_a.id})")
    print(f"  已创建: {agent_b.name} ({agent_b.id})")
    
    # 2. 创建场景
    print("\n[2] 创建场景...")
    scenario = await world_engine.create_scenario(
        participant_ids=[agent_a.id, agent_b.id],
        scenario_type="simple",
        scenario_index=0  # 资源分配场景
    )
    print(f"  场景: {scenario.name}")
    print(f"  描述: {scenario.current_node.description}")
    print(f"  选项:")
    for choice in scenario.current_node.choices:
        print(f"    - {choice.id}: {choice.description}")
    
    # 手动触发决策（MVP 版本）
    print("\n[3] Agent 决策...")
    
    # 直接调用连接器获取决策
    from .agents.connector import DecisionRequest
    
    for agent, connector in [(agent_a, connector_a), (agent_b, connector_b)]:
        request = DecisionRequest(
            agent_id=agent.id,
            scenario_id=scenario.id,
            context={"description": scenario.current_node.description},
            choices=[{"id": c.id, "description": c.description} for c in scenario.current_node.choices],
            timeout=30.0
        )
        
        decision = await connector.get_decision(agent, request)
        scenario.decisions[agent.id] = decision.choice_id
        print(f"  {agent.name} 选择: {decision.choice_id}")
    
    # 4. 结算场景
    print("\n[4] 结算场景...")
    await world_engine._resolve_scenario(scenario)
    
    # 5. 查看完整档案
    print("\n[5] 人格档案...")
    from .personality.engine import personality_engine
    
    for agent in [agent_a, agent_b]:
        profile = personality_engine.get_profile(agent.id)
        if profile:
            print(f"\n  {agent.name}:")
            print(f"    维度: {profile.dimensions.to_dict()}")
            print(f"    标签: {profile.tags}")
            print(f"    历史记录数: {len(profile.history)}")
    
    # 停止世界
    await world_engine.stop()
    
    print("\n" + "=" * 60)
    print("演示结束")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(demo())
