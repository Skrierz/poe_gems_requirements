import pytest

from poe.core import core


class TestGetCharacterData:
    character_name = 'Skrierz'

    def test_returns_valid_data(self):
        data = core.get_character_data(self.character_name)

        assert data['character']['name'] == self.character_name

    def test_returns_valid_gems(self):
        data = core.get_character_data(self.character_name)

        gems = []
        for item in data['items']:
            try:
                item['socketedItems']
            except KeyError:
                continue

            gems.extend([i['typeLine'] for i in item['socketedItems']])
        assert [x[0] for _, v in core.get_equipped_gems_requirements(data).items() for x in v] == gems

