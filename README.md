<div align="center">

# 🐍 Snakia Framework

![Code Quality](https://img.shields.io/codacy/grade/s)
![Code Size](https://img.shields.io/github/languages/code-size/ruject/snakia)
![License](https://img.shields.io/github/license/ruject/snakia)
![Open Issues](https://img.shields.io/github/issues-raw/ruject/snakia)
![Commit Activity](https://img.shields.io/github/commit-activity/m/ruject/snakia)

[API Reference](https://ruject.github.io/snakia/)
&nbsp;•&nbsp;
[Telegram Chat](https://t.me/RuJect_Community)

</div>

**Snakia** is a modern Python framework for creating applications with Entity-Component-System (ECS) architecture, event system, and reactive programming. Built with performance (maybe) and modularity in mind, Snakia provides a clean API for developing complex applications ranging from games to terminal user interfaces.

## 📋 Table of Contents

- [🐍 Snakia Framework](#-snakia-framework)
  - [📋 Table of Contents](#-table-of-contents)
  - [✨ Key Features](#-key-features)
  - [🚀 Installation](#-installation)
    - [Prerequisites](#prerequisites)
    - [Install from PyPi (recommended)](#install-from-pypi-recommended)
    - [Install from Source](#install-from-source)
  - [🎯 Roadmap \& TODO](#-roadmap--todo)
  - [🚀 Quick Start](#-quick-start)
  - [🏗️ Architecture](#️-architecture)
  - [📦 Examples](#-examples)
    - [Health System](#health-system)
    - [TUI Application](#tui-application)
  - [🤝 Contributing](#-contributing)
    - [How to Contribute](#how-to-contribute)
    - [Development Guidelines](#development-guidelines)

## ✨ Key Features

- 🏗️ **ECS Architecture** - Flexible entity-component-system for scalable game/app logic
- 📡 **Event System** - Asynchronous event handling with filters and priorities
- 🔌 **Plugin System** - Modular plugin architecture for extensibility
- 🎨 **TUI Framework** - Rich terminal user interface with reactive widgets
- ⚡ **Reactive Programming** - Observable data streams and reactive bindings
- 🛠️ **Rich Utilities** - Decorators, properties, platform abstraction, and more
- 🎯 **Type Safety** - Full type hints and Pydantic integration

> ⚠️ **Experimental Framework**  
> This framework is currently in **beta/experimental stage**. Not all features are fully implemented, there might be bugs, and the API is subject to change. Use at your own risk! 🚧

## 🚀 Installation

### Prerequisites

- **Python** >= 3.12
- **pip** or **uv** (recommended) package manager

### Install from PyPi (recommended)

```bash
pip install snakia
```

### Install from Source

```bash
git clone https://github.com/RuJect/Snakia.git
cd Snakia
pip install -e .
```

## 🎯 Roadmap & TODO

Here's what we're working on to make Snakia even better:

- [ ] Plugin Isolation: restrict plugin access to only events and components statically defined in manifest
- [ ] Async & Multithreading: implement proper async/await support and multithreading capabilities  
- [ ] Platform Support: expand platform abstraction to support more operating systems
- [ ] Random Implementations: add various random generations implementations
- [ ] TUI Widgets: create more ready-to-use TUI widgets and components
- [ ] Code Documentation: add comprehensive docstrings and inline comments
- [ ] Documentation: create detailed API documentation and tutorials

## 🚀 Quick Start

```python
from snakia.core.engine import Engine
from snakia.core.loader import Meta, Plugin, PluginProcessor
from snakia.core.ecs import Component
from snakia.types import Version

# Creating a component
class HealthComponent(Component):
    value: int = 100
    max_value: int = 100

# Creating a processor
class HealthProcessor(PluginProcessor):
    def process(self, system):
        for entity, (health,) in system.get_components(HealthComponent):
            if health.value <= 0:
                print(f"Entity {entity} died!")

# Creating a plugin
class HealthPlugin(Plugin, meta=Meta(
    name="health",
    version=Version.from_args(1, 0, 0),
    processors=(HealthProcessor,)
)):
    def on_load(self): pass
    def on_unload(self): pass

# Starting the engine
engine = Engine()
engine.loader.register(HealthPlugin)
engine.loader.load_all()
engine.start()
```

## 🏗️ Architecture

Snakia is built on a modular architecture with clear separation of concerns:

```plaintext
Snakia/
├── core/           # Framework core
│   ├── engine.py   # Main engine
│   ├── ecs/        # Entity-Component-System
│   ├── es/         # Event System
│   ├── loader/     # Plugin loading system
│   ├── rx/         # Reactive programming
│   └── tui/        # Terminal User Interface
├── decorators/    # Decorators
├── property/      # Property system
├── platform/      # Platform abstraction
├── utils/         # Utilities
├── random/        # Random number generation
├── field/         # Typed fields
└── types/         # Special types
```

## 📦 Examples

### Health System

```python
from snakia.core.engine import Engine
from snakia.core.ecs import Component
from snakia.core.es import Event
from snakia.core.loader import Meta, Plugin, PluginProcessor
from snakia.types import Version
from pydantic import Field

class HealthComponent(Component):
    max_value: int = Field(default=100, ge=0)
    value: int = Field(default=100, ge=0)

class DamageComponent(Component):
    damage: int = Field(ge=0)
    ticks: int = Field(default=1, ge=0)

class DeathEvent(Event):
    entity: int = Field()

class HealthProcessor(PluginProcessor):
    def process(self, system):
        # Processing damage
        for entity, (damage, health) in system.get_components(
            DamageComponent, HealthComponent
        ):
            health.value -= damage.damage
            damage.ticks -= 1
            
            if damage.ticks <= 0:
                system.remove_component(entity, DamageComponent)
            
            if health.value <= 0:
                system.remove_component(entity, HealthComponent)
                self.plugin.dispatcher.publish(DeathEvent(entity=entity))

class HealthPlugin(Plugin, meta=Meta(
    name="health",
    version=Version.from_args(1, 0, 0),
    processors=(HealthProcessor,)
)):
    def on_load(self): pass
    def on_unload(self): pass

# Usage
engine = Engine()
engine.loader.register(HealthPlugin)
engine.loader.load_all()

# Creating a player
player = engine.system.create_entity(
    HealthComponent(value=100, max_value=100)
)

# Dealing damage
engine.system.add_component(player, DamageComponent(damage=25, ticks=1))

engine.start()
```

### TUI Application

```python
from snakia.core.tui import CanvasChar, RenderContext
from snakia.core.tui.render import ANSIRenderer
from snakia.core.tui.widgets import TextWidget, BoxWidget, VerticalSplitWidget
import sys

class StdoutTarget:
    def write(self, text: str): sys.stdout.write(text)
    def flush(self): sys.stdout.flush()

def main():
    # Creating widgets
    title = TextWidget("Snakia TUI", CanvasChar(fg_color="cyan", bold=True))
    content = TextWidget("Welcome to Snakia!", CanvasChar(fg_color="white"))
    box = BoxWidget(20, 5, CanvasChar("█", fg_color="green"))
    
    # Layout
    layout = VerticalSplitWidget([title, content, box], "-")
    
    # Rendering
    renderer = ANSIRenderer(StdoutTarget())
    
    with RenderContext(renderer) as ctx:
        ctx.render(layout.render())

if __name__ == "__main__":
    main()
```

## 🤝 Contributing

We welcome contributions to Snakia development! Whether you're fixing bugs, adding features, or improving documentation, your help is appreciated.

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes
4. **Add** tests if applicable
5. **Commit** your changes (`git commit -m 'Add amazing feature'`)
6. **Push** to the branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

### Development Guidelines

- Add type hints to all new code
- Write clear commit messages
- Update documentation for new features
- Test your changes thoroughly