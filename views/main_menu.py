import discord
from discord import ui, Interaction, SelectOption
from .away_modal import AwayModal

class LanguageSelect(ui.Select):
    def __init__(self):
        options = [
            SelectOption(label="English", value="en"),
            SelectOption(label="Русский", value="ru"),
        ]
        super().__init__(placeholder="Select your language...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        lang = self.values[0]
        view = AbsenceTypeView(lang)
        await interaction.response.edit_message(content="Choose absence type:" if lang == "en" else "Выберите тип отсутствия:", view=view)

class AbsenceTypeSelect(ui.Select):
    def __init__(self, lang):
        self.lang = lang
        options_en = [
            SelectOption(label="Skipping a week", description="Won't reach weekly limit"),
            SelectOption(label="Skipping 1 day 5v5"),
        ]
        options_ru = [
            SelectOption(label="Пропускаю неделю", description="Не смогу набить недельный лимит"),
            SelectOption(label="Пропускаю 1 день 5 на 5"),
        ]
        options = options_en if lang == "en" else options_ru
        super().__init__(placeholder="Select absence type..." if lang == "en" else "Выберите тип отсутствия...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: Interaction):
        absence_type = self.values[0]
        await interaction.response.send_modal(AwayModal(absence_type=absence_type, lang=self.lang))

class AbsenceTypeView(ui.View):
    def __init__(self, lang):
        super().__init__(timeout=60)
        self.add_item(AbsenceTypeSelect(lang))

class MainMenu(ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(LanguageSelect())