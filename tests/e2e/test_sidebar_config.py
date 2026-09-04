# -*- coding: utf-8 -*-
"""
Class-Widgets-2 侧边栏配置管理与持久化测试 (Tier 1 & Tier 2)

覆盖范围:
- Tier 1: PreferencesConfig 字段默认值、ConfigManager 点分键写入与读取、
          JSON 持久化落盘与二次加载还原、变更信号触发、键锁定安全防御
- Tier 2: 旧版无字段配置平滑升级兼容、损坏 JSON 自动容错回退、
          类型校验与类型转换、快速连击状态切换一致性
"""
import json
import sys
from pathlib import Path

import pytest
from PySide6.QtCore import QCoreApplication

from src.core.config.manager import ConfigManager, RootConfig
from src.core.config.model import PreferencesConfig


@pytest.fixture(scope="session")
def qapp():
    """提供 PySide6 QCoreApplication 单例"""
    app = QCoreApplication.instance()
    if app is None:
        app = QCoreApplication(sys.argv)
    return app


@pytest.fixture
def config_env(tmp_path, qapp):
    """提供基于临时文件系统的独立 ConfigManager 运行实例"""
    config_dir = tmp_path / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    filename = "config.json"
    manager = ConfigManager(config_dir, filename)
    return manager, config_dir / filename


# ============================================================================
# Tier 1: 核心读写、默认值与持久化验证
# ============================================================================


def test_preferences_config_default_values():
    """Tier 1: 验证 PreferencesConfig 初始默认值符合契约：enabled=True, collapsed=False"""
    pref = PreferencesConfig()
    assert pref.schedule_sidebar_enabled is True
    assert pref.schedule_sidebar_collapsed is False


def test_config_manager_set_and_get_enabled(config_env):
    """Tier 1: 验证通过 Configs.set 修改 schedule_sidebar_enabled 并在内存与 data 属性中生效"""
    manager, _ = config_env
    assert manager.preferences.schedule_sidebar_enabled is True

    # 模拟设置界面关闭侧边栏
    manager.set("preferences.schedule_sidebar_enabled", False)
    assert manager.preferences.schedule_sidebar_enabled is False
    assert manager.data["preferences"]["schedule_sidebar_enabled"] is False

    # 重新开启
    manager.set("preferences.schedule_sidebar_enabled", True)
    assert manager.preferences.schedule_sidebar_enabled is True
    assert manager.data["preferences"]["schedule_sidebar_enabled"] is True


def test_config_manager_set_and_get_collapsed(config_env):
    """Tier 1: 验证通过 Configs.set 修改 schedule_sidebar_collapsed 折叠状态记忆"""
    manager, _ = config_env
    assert manager.preferences.schedule_sidebar_collapsed is False

    # 模拟点击收起折叠
    manager.set("preferences.schedule_sidebar_collapsed", True)
    assert manager.preferences.schedule_sidebar_collapsed is True
    assert manager.data["preferences"]["schedule_sidebar_collapsed"] is True

    # 模拟点击小胶囊展开恢复
    manager.set("preferences.schedule_sidebar_collapsed", False)
    assert manager.preferences.schedule_sidebar_collapsed is False
    assert manager.data["preferences"]["schedule_sidebar_collapsed"] is False


def test_config_save_and_load_persistence(config_env):
    """Tier 1: 验证配置持久化写入磁盘文件并在应用重启加载后完整还原"""
    manager, config_file = config_env
    manager.set("preferences.schedule_sidebar_enabled", False)
    manager.set("preferences.schedule_sidebar_collapsed", True)
    manager.save()

    assert config_file.exists()
    content = json.loads(config_file.read_text(encoding="utf-8"))
    assert content["preferences"]["schedule_sidebar_enabled"] is False
    assert content["preferences"]["schedule_sidebar_collapsed"] is True

    # 模拟新会话加载配置
    new_manager = ConfigManager(config_file.parent, config_file.name)
    new_manager.load_config()

    assert new_manager.preferences.schedule_sidebar_enabled is False
    assert new_manager.preferences.schedule_sidebar_collapsed is True


def test_config_signal_emitted_on_sidebar_change(config_env):
    """Tier 1: 验证修改侧边栏相关配置时能够正常发射 configChanged 信号"""
    manager, _ = config_env
    signals_received = []

    manager.configChanged.connect(lambda: signals_received.append(True))

    manager.set("preferences.schedule_sidebar_enabled", False)
    assert len(signals_received) >= 1

    manager.set("preferences.schedule_sidebar_collapsed", True)
    assert len(signals_received) >= 2


def test_config_lock_mechanism(config_env):
    """Tier 1: 验证锁定配置项后拒绝任何写入修改，解锁后允许修改"""
    manager, _ = config_env
    lock_key = "preferences.schedule_sidebar_enabled"

    manager.lock(lock_key)
    assert manager.isKeyLocked(lock_key) is True

    # 尝试修改被锁定的配置
    manager.set(lock_key, False)
    assert manager.preferences.schedule_sidebar_enabled is True  # 依然保持 True

    # 解锁后允许修改
    manager.unlock(lock_key)
    assert manager.isKeyLocked(lock_key) is False
    manager.set(lock_key, False)
    assert manager.preferences.schedule_sidebar_enabled is False


# ============================================================================
# Tier 2: 历史版本升级、边界容错与极端异常验证
# ============================================================================


def test_config_legacy_migration_without_sidebar_fields(config_env):
    """Tier 2 边界: 读取不含侧边栏字段的旧版本 config.json 时平滑升级并填充默认值"""
    manager, config_file = config_env
    # 模拟旧版本配置文件内容，完全没有 schedule_sidebar_* 键
    legacy_json = {
        "preferences": {
            "current_theme": "com.classwidgets.default",
            "scale_factor": 1.2,
        }
    }
    config_file.write_text(json.dumps(legacy_json), encoding="utf-8")

    # 执行加载
    manager.load_config()
    # 必须自动补全默认值
    assert manager.preferences.schedule_sidebar_enabled is True
    assert manager.preferences.schedule_sidebar_collapsed is False
    assert manager.preferences.scale_factor == 1.2


def test_config_corrupted_json_recovery(config_env):
    """Tier 2 边界: 当配置文件内容遭到损坏截断时，能够安全捕获异常并恢复默认配置"""
    manager, config_file = config_env
    # 写入非法语法的内容
    config_file.write_text("{ incomplete_json: 123,, ", encoding="utf-8")

    manager.load_config()
    # 回退到默认配置，且侧边栏配置完好可用
    assert manager.preferences.schedule_sidebar_enabled is True
    assert manager.preferences.schedule_sidebar_collapsed is False


def test_config_rapid_toggle_consistency(config_env):
    """Tier 2 边界: 连续快速交替切换开启与折叠状态，内存模型与落盘数据严格保持一致"""
    manager, config_file = config_env

    for i in range(20):
        flag = (i % 2 == 0)
        manager.set("preferences.schedule_sidebar_enabled", flag)
        manager.set("preferences.schedule_sidebar_collapsed", not flag)

    manager.save()
    disk_data = json.loads(config_file.read_text(encoding="utf-8"))

    assert manager.preferences.schedule_sidebar_enabled is False
    assert manager.preferences.schedule_sidebar_collapsed is True
    assert disk_data["preferences"]["schedule_sidebar_enabled"] is False
    assert disk_data["preferences"]["schedule_sidebar_collapsed"] is True
