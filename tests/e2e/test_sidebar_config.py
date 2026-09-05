# -*- coding: utf-8 -*-
"""
Class-Widgets-2 侧边栏配置管理与持久化测试 (Tier 1 & Tier 2)

覆盖范围:
- Tier 1: PreferencesConfig 字段默认值、ConfigManager 点分键写入与读取、
          JSON 持久化落盘与二次加载还原、变更信号触发、键锁定安全防御
- Tier 2: 旧版无字段配置平滑升级兼容、损坏 JSON 自动容错回退、
          类型校验与类型转换、快速连击状态切换一致性、嵌套字段解析与自动建目录
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


def test_sidebar_config_defaults(config_env):
    """Tier 1: 验证侧边栏配置项默认值符合契约：enabled=True, collapsed=False"""
    manager, _ = config_env
    manager.load_config()

    assert manager.preferences.schedule_sidebar_enabled is True
    assert manager.preferences.schedule_sidebar_collapsed is False
    assert manager.data["preferences"]["schedule_sidebar_enabled"] is True
    assert manager.data["preferences"]["schedule_sidebar_collapsed"] is False


def test_preferences_config_model_defaults():
    """Tier 1: 验证 PreferencesConfig 模型类自身默认值"""
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


def test_sidebar_config_persistence_and_restore(config_env):
    """Tier 1: 验证配置持久化写入磁盘文件并在应用重启加载后完整还原"""
    manager, config_file = config_env
    manager.load_config()

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
    assert new_manager.data["preferences"]["schedule_sidebar_enabled"] is False
    assert new_manager.data["preferences"]["schedule_sidebar_collapsed"] is True


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
    assert manager.preferences.schedule_sidebar_enabled is True

    # 解锁后允许修改
    manager.unlock(lock_key)
    assert manager.isKeyLocked(lock_key) is False
    manager.set(lock_key, False)
    assert manager.preferences.schedule_sidebar_enabled is False


@pytest.mark.parametrize("target_key,val1,val2", [
    ("preferences.schedule_sidebar_enabled", False, True),
    ("preferences.schedule_sidebar_collapsed", True, False),
])
def test_config_roundtrip_values(config_env, target_key, val1, val2):
    """Tier 1: 循环修改两组键值并在 data 字典与模型对象之间交叉比对一致性"""
    manager, _ = config_env
    manager.set(target_key, val1)
    field_name = target_key.split(".")[-1]
    assert getattr(manager.preferences, field_name) is val1
    assert manager.data["preferences"][field_name] is val1

    manager.set(target_key, val2)
    assert getattr(manager.preferences, field_name) is val2
    assert manager.data["preferences"][field_name] is val2


# ============================================================================
# Tier 2: 历史版本升级、边界容错与极端异常验证
# ============================================================================


def test_config_legacy_migration_without_sidebar_fields(config_env):
    """Tier 2 边界: 读取不含侧边栏字段的旧版本 config.json 时平滑升级并填充默认值"""
    manager, config_file = config_env
    legacy_json = {
        "preferences": {
            "current_theme": "com.classwidgets.default",
            "scale_factor": 1.2,
        }
    }
    config_file.write_text(json.dumps(legacy_json), encoding="utf-8")

    manager.load_config()
    assert manager.preferences.schedule_sidebar_enabled is True
    assert manager.preferences.schedule_sidebar_collapsed is False
    assert manager.preferences.scale_factor == 1.2


def test_config_corrupted_json_recovery(config_env):
    """Tier 2 边界: 当配置文件内容遭到损坏截断时，能够安全捕获异常并恢复默认配置"""
    manager, config_file = config_env
    config_file.write_text("{ incomplete_json: 123,, ", encoding="utf-8")

    manager.load_config()
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


def test_config_auto_create_nested_directory(tmp_path, qapp):
    """Tier 2 边界: 配置文件所在的深层多级父目录不存在时，调用 save 自动安全创建父目录"""
    deep_dir = tmp_path / "deep" / "nested" / "path" / "config"
    assert not deep_dir.exists()
    filename = "deep_config.json"
    manager = ConfigManager(deep_dir, filename)

    manager.set("preferences.schedule_sidebar_enabled", True)
    manager.save()

    assert deep_dir.exists()
    assert (deep_dir / filename).exists()


@pytest.mark.parametrize("empty_input", ["", "   ", "{}", "[]"])
def test_config_empty_or_minimal_file_recovery(tmp_path, qapp, empty_input):
    """Tier 2 边界: 空文件或极简内容时安全容错回退为可用配置"""
    cfg_dir = tmp_path / "empty_test"
    cfg_dir.mkdir(parents=True, exist_ok=True)
    cfg_file = cfg_dir / "config.json"
    cfg_file.write_text(empty_input, encoding="utf-8")

    manager = ConfigManager(cfg_dir, "config.json")
    manager.load_config()

    assert manager.preferences.schedule_sidebar_enabled is True
    assert manager.preferences.schedule_sidebar_collapsed is False


def test_sidebar_custom_config_defaults(config_env):
    """Tier 1: 验证侧边栏自定义功能新增字段的默认值契约"""
    manager, _ = config_env
    manager.load_config()

    assert manager.preferences.schedule_sidebar_edge == "right"
    assert manager.preferences.schedule_sidebar_offset_y == 0
    assert manager.preferences.schedule_sidebar_custom_appearance is False
    assert manager.preferences.schedule_sidebar_corner_radius == 22.0
    assert manager.preferences.schedule_sidebar_opacity == 1.0


def test_sidebar_custom_config_read_write_persistence(config_env):
    """Tier 1: 验证侧边栏自定义位置、偏移与外观的点分键读写与落盘持久化"""
    manager, config_file = config_env

    # 写入自定义设置
    manager.set("preferences.schedule_sidebar_edge", "left")
    manager.set("preferences.schedule_sidebar_offset_y", 60)
    manager.set("preferences.schedule_sidebar_custom_appearance", True)
    manager.set("preferences.schedule_sidebar_corner_radius", 18.0)
    manager.set("preferences.schedule_sidebar_opacity", 0.85)
    manager.save()

    # 重新加载验证
    reloaded = ConfigManager(config_file.parent, config_file.name)
    reloaded.load_config()

    assert reloaded.preferences.schedule_sidebar_edge == "left"
    assert reloaded.preferences.schedule_sidebar_offset_y == 60
    assert reloaded.preferences.schedule_sidebar_custom_appearance is True
    assert reloaded.preferences.schedule_sidebar_corner_radius == 18.0
    assert reloaded.preferences.schedule_sidebar_opacity == 0.85

