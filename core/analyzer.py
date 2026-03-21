import json
import calendar
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple, Any, Optional


class ChatAnalyzer:
    def __init__(self, data: Dict[str, Any] = None, min_word_length: int = 3):
        self.min_word_length = min_word_length
        self._reset_stats()
        if data:
            self.data = data
            self._analyze()

    def _reset_stats(self):
        self.data = None
        self.participants: Dict[str, int] = {}
        self.char_count: Dict[str, int] = defaultdict(int)
        self.word_count: Dict[str, int] = defaultdict(int)
        self.words_per_person: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.all_words: Dict[str, int] = defaultdict(int)
        self.date_stats: Dict[str, Dict[str, int]] = {}
        self.hour_stats: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.day_stats: Dict[str, Dict[str, int]] = {}
        self.heatmap_data: Dict[str, Dict[Tuple[int, int], int]] = defaultdict(lambda: defaultdict(int))
        self.messages: List[Dict] = []
        self.total_messages = 0
        self.date_range: Tuple[str, str] = ("", "")

    def load_data(self, data: Dict[str, Any]):
        self.data = data
        self._reset_stats()
        self.data = data
        self._analyze()

    def load_from_file(self, filepath: str) -> bool:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.load_data(data)
            return True
        except Exception as e:
            print(f"Error loading file: {e}")
            return False

    def _analyze(self):
        if not self.data or 'messages' not in self.data:
            return

        messages = self.data['messages']
        self.total_messages = len(messages)
        
        dates = []

        for msg in messages:
            if msg.get('type') != 'message':
                continue

            sender = msg.get('from', 'Unknown')
            text = msg.get('text', '')
            date_str = msg.get('date', '')

            if not date_str:
                continue

            dates.append(date_str[:10])

            self._init_participant(sender)
            self.participants[sender] += 1

            date_part = date_str[:10]
            hour_part = date_str[11:13]

            self._process_date_stats(sender, date_part)
            self._process_hour_stats(sender, hour_part)
            self._process_day_stats(sender, date_part)
            self._process_heatmap(sender, date_part, hour_part)
            self._process_text(sender, text)
            self._process_counts(sender, text)

            self.messages.append({
                'sender': sender,
                'text': text,
                'date': date_str,
                'date_obj': self._parse_date(date_str)
            })

        if dates:
            dates.sort()
            self.date_range = (dates[0], dates[-1])

    def _init_participant(self, sender: str):
        if sender not in self.participants:
            self.participants[sender] = 0
            self.char_count[sender] = 0
            self.word_count[sender] = 0
            self.words_per_person[sender] = defaultdict(int)

    def _parse_date(self, date_str: str) -> Optional[datetime]:
        try:
            return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        except:
            try:
                return datetime.strptime(date_str[:19], '%Y-%m-%dT%H:%M:%S')
            except:
                return None

    def _process_date_stats(self, sender: str, date: str):
        if date not in self.date_stats:
            self.date_stats[date] = {}
        if sender not in self.date_stats[date]:
            self.date_stats[date][sender] = 0
        self.date_stats[date][sender] += 1

    def _process_hour_stats(self, sender: str, hour: str):
        self.hour_stats[hour][sender] += 1

    def _process_day_stats(self, sender: str, date_str: str):
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            day_name = calendar.day_name[date_obj.weekday()]
            if sender not in self.day_stats:
                self.day_stats[sender] = {}
            if day_name not in self.day_stats[sender]:
                self.day_stats[sender][day_name] = 0
            self.day_stats[sender][day_name] += 1
        except:
            pass

    def _process_heatmap(self, sender: str, date_str: str, hour: str):
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            day_of_week = date_obj.weekday()
            hour_int = int(hour)
            self.heatmap_data[sender][(day_of_week, hour_int)] += 1
        except:
            pass

    def _process_text(self, sender: str, text: Any):
        if isinstance(text, list):
            text = ' '.join([t if isinstance(t, str) else t.get('text', '') for t in text])
        
        words = str(text).lower().split()
        for word in words:
            clean_word = ''.join(c for c in word if c.isalnum())
            if len(clean_word) > self.min_word_length:
                self.all_words[clean_word] += 1
                self.words_per_person[sender][clean_word] += 1

    def _process_counts(self, sender: str, text: Any):
        if isinstance(text, list):
            text = ' '.join([t if isinstance(t, str) else t.get('text', '') for t in text])
        
        text_str = str(text)
        self.char_count[sender] += len(text_str.replace(" ", "").replace("\n", ""))
        self.word_count[sender] += len(text_str.split())

    def get_summary(self) -> Dict[str, Any]:
        return {
            'total_messages': self.total_messages,
            'total_words': sum(self.word_count.values()),
            'total_characters': sum(self.char_count.values()),
            'total_participants': len(self.participants),
            'total_days': len(self.date_stats),
            'date_range': self.date_range,
            'participants': self.participants,
        }

    def get_most_used_words(self, limit: int = 20) -> List[Tuple[str, int]]:
        sorted_words = sorted(self.all_words.items(), key=lambda x: x[1], reverse=True)
        return sorted_words[:limit]

    def get_words_by_person(self, person: str, limit: int = 10) -> List[Tuple[str, int]]:
        if person not in self.words_per_person:
            return []
        sorted_words = sorted(self.words_per_person[person].items(), key=lambda x: x[1], reverse=True)
        return sorted_words[:limit]

    def get_hourly_activity(self) -> Dict[str, int]:
        result = {}
        for hour in range(24):
            hour_str = f"{hour:02d}"
            total = sum(self.hour_stats[hour_str].values())
            result[hour_str] = total
        return result

    def get_hourly_by_person(self) -> Dict[str, Dict[str, int]]:
        return dict(self.hour_stats)

    def get_daily_activity(self) -> Dict[str, int]:
        day_totals = {}
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']:
            total = sum(
                stats.get(day, 0) 
                for stats in self.day_stats.values()
            )
            day_totals[day] = total
        return day_totals

    def get_daily_by_person(self) -> Dict[str, Dict[str, int]]:
        return self.day_stats

    def get_heatmap_data(self, person: Optional[str] = None) -> List[List[int]]:
        heatmap = [[0] * 24 for _ in range(7)]
        
        if person:
            data = self.heatmap_data.get(person, {})
        else:
            data = defaultdict(int)
            for person_data in self.heatmap_data.values():
                for key, value in person_data.items():
                    data[key] += value

        for (day, hour), count in data.items():
            if 0 <= day < 7 and 0 <= hour < 24:
                heatmap[day][hour] += count

        return heatmap

    def get_averages(self) -> Dict[str, Any]:
        total_days = len(self.date_stats) if self.date_stats else 1
        
        return {
            'words_per_message': sum(self.word_count.values()) / self.total_messages if self.total_messages else 0,
            'chars_per_message': sum(self.char_count.values()) / self.total_messages if self.total_messages else 0,
            'messages_per_day': self.total_messages / total_days,
            'words_per_day': sum(self.word_count.values()) / total_days,
            'chars_per_day': sum(self.char_count.values()) / total_days,
        }

    def get_per_person_averages(self) -> Dict[str, Dict[str, float]]:
        result = {}
        for person in self.participants:
            msg_count = self.participants[person]
            result[person] = {
                'words_per_message': self.word_count[person] / msg_count if msg_count else 0,
                'chars_per_message': self.char_count[person] / msg_count if msg_count else 0,
            }
        return result

    def get_date_activity(self) -> Dict[str, int]:
        return {date: sum(senders.values()) for date, senders in self.date_stats.items()}
