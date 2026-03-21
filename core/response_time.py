from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple, Any, Optional


class ResponseTimeAnalyzer:
    RESPONSE_THRESHOLD_SECONDS = 300
    
    def __init__(self):
        self.response_times: Dict[str, List[float]] = defaultdict(list)
        self.conversation_starters: Dict[str, int] = defaultdict(int)
        self.conversation_closers: Dict[str, int] = defaultdict(int)
        self.avg_response_by_person: Dict[str, float] = {}
        self.response_pairs: Dict[Tuple[str, str], List[float]] = defaultdict(list)
        self.message_timestamps: List[Tuple[str, datetime]] = []
        self.conversation_gaps: List[Tuple[datetime, datetime, float]] = []

    def analyze_messages(self, messages: List[Dict], gap_threshold_hours: float = 2.0) -> Dict[str, Any]:
        valid_messages = []
        
        for msg in messages:
            if 'date_obj' in msg and msg['date_obj'] is not None:
                valid_messages.append(msg)
        
        valid_messages.sort(key=lambda x: x['date_obj'])
        
        self._analyze_conversations(valid_messages, gap_threshold_hours)
        self._analyze_response_times(valid_messages)
        
        return self.get_stats()

    def _analyze_conversations(self, messages: List[Dict], gap_threshold_hours: float):
        if len(messages) < 2:
            return

        gap_threshold = timedelta(hours=gap_threshold_hours)
        
        prev_msg = messages[0]
        self.conversation_starters[prev_msg['sender']] += 1
        
        for i, msg in enumerate(messages[1:], 1):
            time_diff = msg['date_obj'] - prev_msg['date_obj']
            
            if time_diff > gap_threshold:
                self.conversation_starters[msg['sender']] += 1
                self.conversation_closers[prev_msg['sender']] += 1
                self.conversation_gaps.append((prev_msg['date_obj'], msg['date_obj'], time_diff.total_seconds() / 3600))
            
            prev_msg = msg
        
        if messages:
            self.conversation_closers[messages[-1]['sender']] += 1

    def _analyze_response_times(self, messages: List[Dict]):
        if len(messages) < 2:
            return

        prev_sender = None
        prev_time = None

        for msg in messages:
            sender = msg['sender']
            msg_time = msg['date_obj']
            
            if prev_sender is not None and sender != prev_sender:
                if prev_time is not None:
                    time_diff = (msg_time - prev_time).total_seconds()
                    
                    if time_diff < self.RESPONSE_THRESHOLD_SECONDS * 10:
                        self.response_times[sender].append(time_diff)
                        self.response_pairs[(prev_sender, sender)].append(time_diff)
            
            prev_sender = sender
            prev_time = msg_time

        for person, times in self.response_times.items():
            if times:
                self.avg_response_by_person[person] = sum(times) / len(times)

    def get_stats(self) -> Dict[str, Any]:
        all_times = []
        for times in self.response_times.values():
            all_times.extend(times)

        avg_response = sum(all_times) / len(all_times) if all_times else 0

        return {
            'average_response_time': avg_response,
            'average_response_time_formatted': self._format_time(avg_response),
            'by_person': {
                person: {
                    'average': self.avg_response_by_person.get(person, 0),
                    'average_formatted': self._format_time(self.avg_response_by_person.get(person, 0)),
                    'count': len(times),
                    'min': min(times) if times else 0,
                    'max': max(times) if times else 0,
                }
                for person, times in self.response_times.items()
            },
            'conversation_starters': dict(self.conversation_starters),
            'conversation_closers': dict(self.conversation_closers),
            'total_conversations': len(self.conversation_gaps) + 1,
            'conversation_pairs': {
                f"{pair[0]} -> {pair[1]}": {
                    'average': sum(times) / len(times) if times else 0,
                    'count': len(times),
                }
                for pair, times in self.response_pairs.items()
            },
        }

    def get_response_time_distribution(self, person: str) -> Dict[str, int]:
        times = self.response_times.get(person, [])
        
        distribution = {
            'instant': 0,
            'fast': 0,
            'normal': 0,
            'slow': 0,
            'very_slow': 0,
        }
        
        for t in times:
            if t < 30:
                distribution['instant'] += 1
            elif t < 120:
                distribution['fast'] += 1
            elif t < 300:
                distribution['normal'] += 1
            elif t < 900:
                distribution['slow'] += 1
            else:
                distribution['very_slow'] += 1
        
        return distribution

    def get_fastest_responders(self, limit: int = 5) -> List[Tuple[str, float]]:
        valid_responders = [(person, avg) for person, avg in self.avg_response_by_person.items() if avg > 0]
        return sorted(valid_responders, key=lambda x: x[1])[:limit]

    def get_slowest_responders(self, limit: int = 5) -> List[Tuple[str, float]]:
        valid_responders = [(person, avg) for person, avg in self.avg_response_by_person.items() if avg > 0]
        return sorted(valid_responders, key=lambda x: x[1], reverse=True)[:limit]

    def _format_time(self, seconds: float) -> str:
        if seconds <= 0:
            return "N/A"
        
        if seconds < 60:
            return f"{seconds:.0f}s"
        elif seconds < 3600:
            minutes = seconds / 60
            return f"{minutes:.1f}m"
        else:
            hours = seconds / 3600
            return f"{hours:.1f}h"

    def reset(self):
        self.response_times = defaultdict(list)
        self.conversation_starters = defaultdict(int)
        self.conversation_closers = defaultdict(int)
        self.avg_response_by_person = {}
        self.response_pairs = defaultdict(list)
        self.message_timestamps = []
        self.conversation_gaps = []
