import re
from collections import defaultdict
from typing import Dict, List, Tuple, Any


class EmojiParser:
    EMOJI_PATTERN = re.compile(
        "["
        "\U0001F600-\U0001F64F"
        "\U0001F300-\U0001F5FF"
        "\U0001F680-\U0001F6FF"
        "\U0001F1E0-\U0001F1FF"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001F900-\U0001F9FF"
        "\U0001FA00-\U0001FA6F"
        "\U0001FA70-\U0001FAFF"
        "\U00002600-\U000026FF"
        "\U00002700-\U000027BF"
        "]+"
    )

    EMOJI_NAMES = {
        "😂": "Face with Tears of Joy",
        "❤️": "Red Heart",
        "🔥": "Fire",
        "😍": "Smiling Face with Heart-Eyes",
        "😭": "Loudly Crying Face",
        "😊": "Smiling Face with Smiling Eyes",
        "🙏": "Folded Hands",
        "👍": "Thumbs Up",
        "💀": "Skull",
        "✨": "Sparkles",
        "🎉": "Party Popper",
        "😎": "Smiling Face with Sunglasses",
        "💖": "Sparkling Heart",
        "🥺": "Pleading Face",
        "🤣": "Rolling on the Floor Laughing",
        "😘": "Face Blowing a Kiss",
        "🥰": "Smiling Face with Hearts",
        "😢": "Crying Face",
        "💔": "Broken Heart",
        "🤔": "Thinking Face",
        "😅": "Grinning Face with Sweat",
        "😔": "Pensive Face",
        "😊": "Smiling Face with Smiling Eyes",
        "👀": "Eyes",
        "💯": "Hundred Points",
        "🙌": "Raising Hands",
        "💕": "Two Hearts",
        "😌": "Relieved Face",
        "🙃": "Upside-Down Face",
        "😜": "Winking Face with Tongue",
        "😏": "Smirking Face",
        "😊": "Smiling Face with Smiling Eyes",
        "☺️": "Smiling Face",
        "🙂": "Slightly Smiling Face",
        "🤗": "Hugging Face",
        "🤩": "Star-Struck",
        "🤫": "Shushing Face",
        "🤭": "Face with Hand Over Mouth",
        "🤔": "Thinking Face",
        "🤐": "Zipper-Mouth Face",
        "🤨": "Face with Raised Eyebrow",
        "😐": "Neutral Face",
        "😑": "Expressionless Face",
        "😶": "Face Without Mouth",
        "🙄": "Face with Rolling Eyes",
        "😏": "Smirking Face",
        "😣": "Persevering Face",
        "😥": "Disappointed but Relieved Face",
        "😮": "Face with Open Mouth",
        "🤐": "Zipper-Mouth Face",
        "😯": "Hushed Face",
        "😪": "Sleepy Face",
        "😫": "Tired Face",
        "😴": "Sleeping Face",
        "😛": "Face with Tongue",
        "😜": "Winking Face with Tongue",
        "😝": "Squinting Face with Tongue",
        "🤤": "Drooling Face",
        "😒": "Unamused Face",
        "😓": "Downcast Face with Sweat",
        "😔": "Pensive Face",
        "😕": "Confused Face",
        "🙃": "Upside-Down Face",
        "🫠": "Melting Face",
        "🫡": "Saluting Face",
        "🫢": "Face with Open Eyes and Hand Over Mouth",
        "🫣": "Face with Peeking Eye",
        "🫤": "Face with Diagonal Mouth",
        "🫥": "Dotted Line Face",
        "🫦": "Biting Lip",
    }

    def __init__(self):
        self.emoji_counts: Dict[str, int] = defaultdict(int)
        self.emoji_by_person: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))

    def analyze_messages(self, messages: List[Dict]) -> Dict[str, Any]:
        for msg in messages:
            sender = msg.get('sender', 'Unknown')
            text = msg.get('text', '')
            self._extract_emojis(sender, text)

        return self.get_stats()

    def _extract_emojis(self, sender: str, text: Any):
        if isinstance(text, list):
            text = ' '.join([t if isinstance(t, str) else t.get('text', '') for t in text])
        
        text_str = str(text)
        emojis = self.EMOJI_PATTERN.findall(text_str)
        
        for emoji in emojis:
            for char in emoji:
                if char.strip():
                    self.emoji_counts[char] += 1
                    self.emoji_by_person[sender][char] += 1

    def get_stats(self) -> Dict[str, Any]:
        sorted_emojis = sorted(self.emoji_counts.items(), key=lambda x: x[1], reverse=True)
        
        person_stats = {}
        for person, emojis in self.emoji_by_person.items():
            person_stats[person] = sorted(emojis.items(), key=lambda x: x[1], reverse=True)[:20]

        return {
            'total_emojis': sum(self.emoji_counts.values()),
            'unique_emojis': len(self.emoji_counts),
            'top_emojis': sorted_emojis[:20],
            'by_person': person_stats,
        }

    def get_emoji_name(self, emoji: str) -> str:
        return self.EMOJI_NAMES.get(emoji, "Unknown Emoji")

    def get_emoji_by_person(self, person: str, limit: int = 10) -> List[Tuple[str, int]]:
        if person not in self.emoji_by_person:
            return []
        sorted_emojis = sorted(self.emoji_by_person[person].items(), key=lambda x: x[1], reverse=True)
        return sorted_emojis[:limit]

    def reset(self):
        self.emoji_counts = defaultdict(int)
        self.emoji_by_person = defaultdict(lambda: defaultdict(int))
