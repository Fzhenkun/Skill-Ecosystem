# Investigation Framework / 调查框架

This is a single framework with adjustable scale. Ask the following questions in order.

## 1. Scope / 界定对象

- What exactly is being analyzed?
- What decision, learning goal, or risk is the user addressing?
- What is in scope, out of scope, and supported by available evidence?

## 2. Global or Context Map / 全局或上下文地图

For complex subjects:

- Who are the actors and owners?
- What are the components and responsibilities?
- What enters, changes, and leaves the system?
- How do data, control, money, or decisions flow?
- What dependencies, lifecycle states, external constraints, and failure surfaces matter?
- What timeline or version history might explain the present shape?

For simple subjects, answer the same questions at minimum scale: what it is, what it interacts with, what goes in, what comes out, and where it is used.

## 3. Key Mechanisms / 关键机制

For each selected mechanism, write:

`condition/input -> mechanism -> state change or decision -> output/effect`

Then answer:

- Why is this mechanism central to the user’s question?
- What assumption does it rely on?
- What would be observable if the explanation were true?

## 4. Anomaly and History / 反常点与历史

- What looks irrational, overly complex, inconsistent, or broken?
- Is the observation confirmed by code, tests, documents, logs, or behavior?
- Could compatibility, migration, old incidents, ownership, performance, or external constraints explain it?
- Which explanation is confirmed, which is only a hypothesis, and which constraints remain?

## 5. Boundaries and Costs / 边界与代价

- Where does it work and where does it fail?
- What are the performance, memory, complexity, safety, operational, migration, and lock-in costs?
- What alternative wins under a different constraint?
- What misuse is likely even if the mechanism is technically correct?

## 6. Practice and Verification / 实践与验证

- What is the smallest reproduction, experiment, inspection, measurement, or scenario walkthrough?
- What observation would support or falsify the claim?
- What did the check actually establish, and what remains unknown?

## 7. Synthesis / 综合

- What is the essence in one sentence?
- Which findings are facts and which are inferences?
- What stance or action follows from the evidence?
- What risks and open questions remain?
