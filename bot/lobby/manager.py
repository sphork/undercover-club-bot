from dataclasses import dataclass, field
from typing import Dict, Set, Tuple


@dataclass
class Lobby:
    chat_id: int
    owner_id: int
    players: Set[int] = field(default_factory=set)
    max_players: int = 12
    is_open: bool = True

    def add(self, user_id: int) -> Tuple[bool, str]:
        if not self.is_open:
            return False, 'Лобби закрыто.'
        if len(self.players) >= self.max_players:
            return False, 'Лобби заполнено.'
        if user_id in self.players:
            return False, 'Вы уже в лобби.'
        self.players.add(user_id)
        return True, 'Вы присоединились к лобби.'

    def remove(self, user_id: int) -> Tuple[bool, str]:
        if user_id not in self.players:
            return False, 'Вас нет в лобби.'
        self.players.remove(user_id)
        return True, 'Вы покинули лобби.'


class LobbyManager:
    def __init__(self) -> None:
        self._lobbies: Dict[int, Lobby] = {}

    def get(self, chat_id: int) -> Lobby | None:
        return self._lobbies.get(chat_id)

    def create(self, chat_id: int, owner_id: int) -> Tuple[bool, str]:
        if chat_id in self._lobbies and self._lobbies[chat_id].is_open:
            return False, 'В этом чате уже есть активное лобби.'
        lobby = Lobby(chat_id=chat_id, owner_id=owner_id)
        lobby.players.add(owner_id)
        self._lobbies[chat_id] = lobby
        return True, 'Создано новое лобби.'

    def cancel(self, chat_id: int, by_user: int) -> Tuple[bool, str]:
        lobby = self._lobbies.get(chat_id)
        if not lobby:
            return False, 'Лобби не найдено.'
        if lobby.owner_id != by_user:
            return False, 'Только создатель лобби может отменить его.'
        lobby.is_open = False
        self._lobbies.pop(chat_id, None)
        return True, 'Лобби отменено.'

    def start(self, chat_id: int, by_user: int) -> Tuple[bool, str]:
        lobby = self._lobbies.get(chat_id)
        if not lobby:
            return False, 'Лобби не найдено.'
        if lobby.owner_id != by_user:
            return False, 'Только создатель лобби может начать игру.'
        if len(lobby.players) < 4:
            return False, 'Нужно минимум 4 игрока, чтобы начать.'
        lobby.is_open = False
        # На следующем шаге здесь будет инициализация игры
        self._lobbies.pop(chat_id, None)
        return True, 'Игра стартует!'

    def list_players(self, chat_id: int) -> str:
        lobby = self._lobbies.get(chat_id)
        if not lobby:
            return 'Лобби не найдено.'
        if not lobby.players:
            return 'В лобби пока нет игроков.'
        lines = [f'Игроков: {len(lobby.players)}/{lobby.max_players}']
        for i, uid in enumerate(lobby.players, start=1):
            mark = '👑' if uid == lobby.owner_id else '•'
            lines.append(f'{i}. {mark} {uid}')
        return '\n'.join(lines)


lobbies = LobbyManager()
