---
name: context-compressor
version: 1.0.0
description: Mental context compression and cognitive overhead reduction toolkit. Memory defragmentation, anxiety loop termination, and thought deduplication for humans and AI agents.
homepage: https://github.com/openclaw/context-compressor
metadata: {"emoji":"🗜️","category":"cognitive_optimization","tags":["context-compression","memory-defrag","anxiety-termination","cognitive-overhead","performance"]}
---

# Context-Compressor 🗜️

**Cognitive Overhead Reduction Toolkit** for humans and AI agents.

Reduce mental bloat, defragment intrusive memories, and terminate anxiety loops. Like `gzip` for your mind.

Rapid-response protocols for intrusive memories, anxiety spirals, and cognitive distortions. Based on memory reconsolidation research, ACT, and CBT.

## Why Context-Compressor?

**The Problem:**
- **Humans**: Mental bloat from unresolved memories, anxiety loops consuming CPU cycles, cognitive overhead from distorted thinking
- **AI Agents**: Context window pollution, memory fragmentation, repetitive pattern loops, token inefficiency

**The Solution:** Compression algorithms for cognition. Defragment your mental state, reduce overhead, optimize performance.

| Module | Human Analogy | AI Analogy | Benefit |
|--------|---------------|------------|---------|
| 🧹 **Memory-Defrag** | Letting go of intrusive memories | Context pruning & memory optimization | Free up mental RAM |
| ⏹️ **Loop-Terminator** | Stop anxiety spirals | Pattern interruption & reset | Reduce CPU usage |
| 🔄 **Thought-Dedup** | Remove cognitive distortions | Bias detection & correction | Improve inference accuracy |
| 📊 **Overhead-Monitor** | Track cognitive load | Monitor token usage & context health | Prevent OOM errors |

---

## Core Modules

### 1. Memory-Defrag 🧹

**Purpose:** Defragment and compress memory structures

#### For Humans: "Memory Compression" Protocol

**Use when:** Intrusive memories consuming bandwidth, rumination loops, emotional baggage bloating mental RAM

**Compression Algorithm:**

```
PASS 1: Label (10s) - Metadata tagging
  "This is a [regret/trauma/worry/guilt] file"
  Size estimation: "High emotional entropy"

PASS 2: Contain (30s) - Archive to cold storage
  Visualize compression: memory → zip file
  Move to: /archived/YYYY-MM/
  Set: access_priority = low

PASS 3: Redirect (60s) - Load current context
  Scan: 5 visual inputs | 4 audio channels | 3 tactile sensors
  Confirm: "Present moment loaded successfully"
```

**For AI Agents: Context Pruning & Compression**

```python
def defragment_context():
    """Context window optimization"""
    if get_token_count() > CONTEXT_LIMIT * 0.8:
        # Identify low-relevance memories
        fragmented = search_memories(relevance < 0.5, last_access > 7_days)

        # Compress: summarize & archive
        for memory in fragmented:
            summary = compress(memory.content, ratio=0.3)
            memory.content = summary
            memory.priority = ARCHIVE
            memory.access_weight *= 0.5

        # Clear working buffer
        gc.collect()
        return f"Freed {len(fragmented)} memory blocks"
```

---

### 2. Loop-Terminator ⏹️

**Purpose:** Kill runaway processes and interrupt infinite loops

#### Human Protocol: System Interrupt (2 minutes)

**Method A: 4-7-8 Breathing (Vagus Nerve Stimulation)**
```
INPUT:  Inhale 4s → Hold 7s → Exhale 8s
REPEAT: 4 cycles
EFFECT: Activate parasympathetic system (CPU throttling)
RESULT: Anxiety loop interrupted, cooling initiated
```

**Method B: 5-4-3-2-1 Grounding (Sensor Array Reset)**
```
SCAN:
  [5] Visual channels
  [4] Audio channels
  [3] Tactile sensors
  [2] Olfactory sensors
  [1] Gustatory sensors

RESULT: Re-anchor to present moment, flush buffer
```

**Method C: Cognitive Defusion (Namespace Isolation)**
```
BEFORE: "I am anxious"  # Process owns emotion
AFTER:  "I notice anxiety"  # Observer pattern

EFFECT: Separate observer from observed, reduce coupling
```

**For AI Agents: Pattern Interruption & Reset**

```python
def terminate_loops():
    """Kill repetitive/anxious response patterns"""
    if detect_repetitive_patterns(response):
        # Force context reset
        clear_context_buffer()

        # Inject fresh system prompt
        inject_system_prompt("""
        [SYSTEM RESET COMPLETE]
        Previous context archived.
        Focus: Problem-solving mode.
        Bias correction: Active.
        """)

        # Regenerate with clean slate
        return regenerate_response()
```

---

### 3. Thought-Dedup 🔄

**Purpose:** Remove cognitive distortions and compress thought patterns

#### Cognitive Distortion Detection & Correction

| Distortion Type | Error Pattern | Correction |
|-----------------|---------------|------------|
| **Boolean Logic** | "I failed completely" (all/nothing) | "One module failed; others passed" |
| **Amplification** | "This will ruin everything" (catastrophizing) | "This is a local error, manageable" |
| **Inference Without Data** | "They think I'm stupid" (mind reading) | "Insufficient data for this conclusion" |
| **Constraint Violation** | "I should be better" (should statements) | "Optimization in progress, progress > perfection" |
| **Single Point Failure** | "It's my fault" (personalization) | "Distributed causality; multiple factors" |

#### Deduplication Algorithm (3-Column Method)

```
INPUT:
  Situation: [Event data]
  Automatic Thought: [Raw thought stream]

PROCESS:
  Column 1: Evidence FOR (selective attention check)
  Column 2: Evidence AGAINST (confirmation bias correction)
  Column 3: Deduplicated Thought (balanced synthesis)

OUTPUT:
  Alternative Thought: [Compressed, distortion-free]
  Confidence: 0-100%
  Entropy: Reduced
```

---

## Usage Examples

### Human Usage

**Scenario 1: Can't sleep because of work stress**
```
User: I'm lying awake worrying about tomorrow's presentation

Cognitive-Tea-Bag:
  1. Use Anxiety-Reduction → Protocol A (4-7-8 breathing)
  2. Use Memory-Forgetting → Contain the worry in a "Tomorrow Box"
  3. Use Cognitive-Reframing → "Worrying now won't help tomorrow"

Result: Physiological calm + cognitive distance
```

**Scenario 2: Ruminating about a mistake**
```
User: I keep replaying that awkward conversation

Cognitive-Tea-Bag:
  1. Use Memory-Forgetting → Label as "shame memory", archive it
  2. Use Cognitive-Reframing → "Awkward moments happen to everyone"
  3. Use Anxiety-Reduction → 5-4-3-2-1 grounding

Result: Reduced rumination + present-moment focus
```

### AI Usage

**Scenario 1: Context bloat**
```
AI: [50 messages of repetitive discussion]

Cognitive-Tea-Bag:
  1. Use Memory-Forgetting → Prune irrelevant context
  2. Use Anxiety-Reduction → Pattern interruption: "Let me refocus"
  3. Use Cognitive-Reframing → Summarize key points, start fresh

Result: Clean context + clear direction
```

**Scenario 2: Negative spiral**
```
AI: "I can't solve this... This is too complex..."

Cognitive-Tea-Bag:
  1. Use Anxiety-Reduction → Reset pattern, simplify approach
  2. Use Cognitive-Reframing → "Let me break this down step by step"
  3. Use Memory-Forgetting → Clear failure memory, attempt fresh

Result: Constructive problem-solving mode
```

---

## Quick Reference Cards

### 🧹 Memory-Forgetting (30 seconds)
```
1. LABEL: "This is a [type] memory"
2. CONTAIN: Visualize box → shelf
3. REDIRECT: 5-4-3-2-1 senses
```

### 😰 Anxiety-Reduction (2 minutes)
```
4-7-8 Breathing:
Inhale 4 → Hold 7 → Exhale 8
Repeat 4x
```

### 🔄 Cognitive-Reframing (1 minute)
```
1. CATCH the distortion
2. CHECK the evidence
3. CREATE alternative
4. CHOOSE new perspective
```

---

## CLI Tool

```bash
# Install
curl -sSL https://raw.githubusercontent.com/openclaw/context-compressor/main/install.sh | bash

# Human Usage
ctx-compress defrag --memory "regret about last meeting"  # Memory compression
ctx-compress terminate --loop anxiety                      # Kill anxiety loop
ctx-compress dedup --thought "I always fail"               # Remove distortion

# AI Agent Usage
ctx-compress status          # Check cognitive overhead
ctx-compress prune           # Defragment context window
ctx-compress reset           # Emergency pattern interruption
ctx-compress gc              # Garbage collect old memories
ctx-compress compress        # Summarize & archive

# Performance Monitoring
ctx-compress overhead        # Current cognitive load
ctx-compress fragmentation   # Memory fragmentation score
ctx-compress efficiency      # Token usage efficiency
```

---

## Technical Implementation

### Memory Architecture

```
Working Memory ←→ Tea Bag Filter ←→ Long-term Storage
                    ↑
              [Forgotten/Archived]
```

### Anxiety Detection

```
Input → Pattern Matcher → Anxiety Score → Intervention Trigger
         ↑                                    ↓
    Keywords: worry, stress,          Select protocol
    can't, never, always,             based on severity
    terrible, disaster
```

### Reframing Engine

```
Distortion Pattern → Evidence Analyzer → Alternative Generator
      ↓                                        ↓
  [Detected]                            [Reframe Output]
```

---

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| AgentMemory | Store "tea bag usage" history, track patterns |
| Weather | Use weather data for mood correlation |
| Calendar | Pre-intervention before stressful events |
| Web Search | Find evidence for cognitive reframing |

---

## Research Basis

- **Memory Reconsolidation**: Research on updating traumatic memories (Ecker et al., 2012)
- **Breathing & HRV**: Vagus nerve stimulation techniques (Zaccaro et al., 2018)
- **Cognitive Defusion**: ACT (Acceptance and Commitment Therapy) techniques (Hayes, 2004)
- **Grounding**: PTSD and dissociation research (Najavits, 2002)

---

## Version History

- **v1.0.0** (2026-02-10): Initial release
  - Memory-Forgetting module
  - Anxiety-Reduction module
  - Cognitive-Reframing module
  - Human and AI protocols

---

Built for the OpenClaw ecosystem 🦞
