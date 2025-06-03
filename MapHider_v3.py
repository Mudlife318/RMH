import obspython as obs
import time
from dataclasses import dataclass
from typing import Optional


class Hotkey:
    """Manages OBS hotkey registration and callbacks."""
    
    def __init__(self, callback, obs_settings, hotkey_id: str):
        self.obs_data = obs_settings
        self.hotkey_id = obs.OBS_INVALID_HOTKEY_ID
        self.hotkey_saved_key = None
        self.callback = callback
        self._id = hotkey_id

        self.load_hotkey()
        self.register_hotkey()
        self.save_hotkey()

    def register_hotkey(self):
        """Register the hotkey with OBS."""
        description = str(self._id)
        self.hotkey_id = obs.obs_hotkey_register_frontend(
            str(self._id), description, self.callback
        )
        obs.obs_hotkey_load(self.hotkey_id, self.hotkey_saved_key)

    def load_hotkey(self):
        """Load saved hotkey configuration."""
        self.hotkey_saved_key = obs.obs_data_get_array(
            self.obs_data, str(self._id)
        )
        obs.obs_data_array_release(self.hotkey_saved_key)

    def save_hotkey(self):
        """Save current hotkey configuration."""
        self.hotkey_saved_key = obs.obs_hotkey_save(self.hotkey_id)
        obs.obs_data_set_array(
            self.obs_data, str(self._id), self.hotkey_saved_key
        )
        obs.obs_data_array_release(self.hotkey_saved_key)


@dataclass
class ScriptSettings:
    """Holds script configuration settings."""
    map_image_name: str = ""
    rust_scene_name: str = ""
    reveal_delay: float = 0.0


# Global settings instance
settings = ScriptSettings()
hotkey_instance: Optional[Hotkey] = None


def toggle_map_visibility():
    """Toggle the visibility of the map hider image."""
    current_scene = obs.obs_scene_from_source(obs.obs_frontend_get_current_scene())
    scene_item = obs.obs_scene_find_source(current_scene, settings.map_image_name)
    
    if scene_item:
        current_visibility = obs.obs_sceneitem_visible(scene_item)
        obs.obs_sceneitem_set_visible(scene_item, not current_visibility)


def mapkey_callback(pressed: bool):
    """
    Callback function for the map hotkey.
    
    Args:
        pressed: True when key is pressed, False when released
    """
    # Check if we're in the correct scene
    if settings.rust_scene_name and settings.rust_scene_name != obs.obs_source_get_name(obs.obs_frontend_get_current_scene()):
        return
    
    if pressed:
        toggle_map_visibility()
    else:
        # Add delay before revealing map
        time.sleep(settings.reveal_delay)
        toggle_map_visibility()


def script_description() -> str:
    """Return the script description shown in OBS."""
    return (
        "Rust Map Hider using Hotkey within Game.\n\n"
        "Settings:\n"
        "• Map Hider Image: The name of your Map Hider Image source\n"
        "• OBS Scene To Cover: The scene that you want the hotkey to affect\n"
        "• Reveal Delay: Time before the map cover disappears (seconds)\n\n"
        "Setup:\n"
        "1. Configure the settings above\n"
        "2. Go to OBS Hotkeys and set 'RustMap Push to Hide' to your map key "
        "(e.g., Shift+G)\n\n"
        "Follow & Support Appreciated\n"
        "Twitch/Patreon: Mudlife318"
    )


def script_properties():
    """Define the script properties UI."""
    props = obs.obs_properties_create()
    
    obs.obs_properties_add_text(
        props, "MapHiderImage", "Map Hider Image:", obs.OBS_TEXT_DEFAULT
    )
    obs.obs_properties_add_text(
        props, "OBSsceneToCover", "OBS Scene To Cover:", obs.OBS_TEXT_DEFAULT
    )
    obs.obs_properties_add_float_slider(
        props, "rust_map_delay", "Reveal Delay (seconds):", 0.0, 3.0, 0.05
    )
    
    return props


def script_update(obs_settings):
    """Update script settings when properties change."""
    global settings
    
    settings.map_image_name = obs.obs_data_get_string(obs_settings, "MapHiderImage")
    settings.rust_scene_name = obs.obs_data_get_string(obs_settings, "OBSsceneToCover")
    settings.reveal_delay = obs.obs_data_get_double(obs_settings, "rust_map_delay")


def script_load(obs_settings):
    """Initialize the script when loaded."""
    global hotkey_instance, settings
    
    # Create hotkey instance
    hotkey_instance = Hotkey(mapkey_callback, obs_settings, "RustMap Push to Hide")
    
    # Load initial settings
    settings.map_image_name = obs.obs_data_get_string(obs_settings, "MapHiderImage")
    settings.rust_scene_name = obs.obs_data_get_string(obs_settings, "OBSsceneToCover")
    settings.reveal_delay = obs.obs_data_get_double(obs_settings, "rust_map_delay")


def script_save(obs_settings):
    """Save script settings."""
    if hotkey_instance:
        hotkey_instance.save_hotkey()


def script_unload():
    """Clean up when script is unloaded."""
    global hotkey_instance
    hotkey_instance = None