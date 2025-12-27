

class SettingsManager:
    def __init__(self, db):
        self.db = db

    def save_mode(self, key, value):
        """Сохраняет булевы значения (True/False)"""
        # Преобразуем True -> "1", False -> "0" для надежности
        self.db.set_setting(key, "1" if value else "0")

    def load_mode(self, key, default=False):
        """Загружает булевы значения"""
        val = self.db.get_setting(key)
        if val is None:
            return default
        return val == "1"

    def save_tags(self, tags_list):
        """Сохраняет список тегов как строку через запятую"""
        tags_str = ",".join(tags_list)
        self.db.set_setting("selected_tags", tags_str)

    def load_tags(self):
        """Загружает строку и превращает её обратно в список"""
        tags_str = self.db.get_setting("selected_tags", "")
        if not tags_str:
            return []
        return tags_str.split(",")
    
    # settings_manager.py
    def save_last_tag(self, tag):
        self.db.set_setting("last_used_tag", tag)

    def load_last_tag(self):
        tag = self.db.get_setting("last_used_tag")
        return tag if tag else "default"

