import re
import json
from collections import defaultdict
from typing import Dict, List, Tuple, Any, Set
from pathlib import Path


class SentimentAnalyzer:
    POSITIVE_WORDS = {
        'good', 'great', 'awesome', 'excellent', 'amazing', 'wonderful', 'fantastic',
        'love', 'happy', 'joy', 'beautiful', 'perfect', 'best', 'brilliant', 'superb',
        'nice', 'cool', 'yay', 'woohoo', 'haha', 'lol', 'thanks', 'thank', 'appreciate',
        'helpful', 'kind', 'friendly', 'lovely', 'sweet', 'cute', 'adorable', 'proud',
        'excited', 'thrilled', 'delighted', 'grateful', 'blessed', 'lucky', 'fortunate',
        'win', 'won', 'winner', 'success', 'successful', 'achieve', 'achievement',
        'congrats', 'congratulations', 'celebrate', 'celebration', 'party',
        'yes', 'absolutely', 'definitely', 'sure', 'certainly', 'of course',
        'please', 'pleasure', 'enjoy', 'enjoyed', 'enjoying', 'fun', 'funny',
        'hilarious', 'wonderful', 'marvelous', 'outstanding', 'impressive',
        'genius', 'smart', 'clever', 'bright', 'shine', 'shining', 'glow',
        'peace', 'peaceful', 'calm', 'relax', 'relaxed', 'relaxing', 'comfortable',
        'safe', 'safety', 'secure', 'trust', 'trusted', 'trustworthy', 'reliable',
        'hope', 'hopeful', 'optimistic', 'positive', 'bright', 'sunny',
        'friend', 'friends', 'friendship', 'together', 'support', 'supportive',
        'agree', 'agreed', 'agreement', 'understand', 'understanding', 'fair',
        'welcome', 'glad', 'pleased', 'satisfied', 'content', 'peaceful',
    }

    NEGATIVE_WORDS = {
        'bad', 'terrible', 'awful', 'horrible', 'worst', 'hate', 'dislike',
        'sad', 'unhappy', 'angry', 'mad', 'furious', 'upset', 'annoyed',
        'frustrated', 'disappointed', 'disappointing', 'boring', 'bored',
        'tired', 'exhausted', 'drained', 'stressed', 'stress', 'anxiety',
        'worried', 'worry', 'fear', 'afraid', 'scared', 'terrified',
        'lonely', 'alone', 'isolated', 'abandoned', 'rejected', 'ignored',
        'hurt', 'pain', 'painful', 'suffer', 'suffering', 'struggle',
        'fail', 'failed', 'failure', 'lose', 'lost', 'loser', 'losing',
        'problem', 'issue', 'trouble', 'difficult', 'hard', 'tough',
        'sorry', 'apologize', 'apology', 'regret', 'mistake', 'error',
        'wrong', 'incorrect', 'false', 'lie', 'lies', 'liar', 'deceive',
        'ugly', 'stupid', 'dumb', 'idiot', 'fool', 'ridiculous', 'absurd',
        'never', 'no', 'not', 'none', 'nothing', 'nobody', 'nowhere',
        'cannot', "can't", "won't", "don't", "didn't", "doesn't", "isn't", "aren't",
        'stop', 'quit', 'leave', 'gone', 'left', 'over', 'end', 'ended',
        'broken', 'break', 'damage', 'destroy', 'destroyed', 'ruin', 'ruined',
        'suck', 'sucks', 'crap', 'shit', 'damn', 'hell', 'wtf', 'omg',
        'cry', 'crying', 'tears', 'depressed', 'depression', 'miserable',
        'angry', 'rage', 'furious', 'outraged', 'offended', 'insulted',
        'confused', 'confusing', 'complicated', 'messy', 'chaos', 'chaotic',
        'sick', 'ill', 'disease', 'dying', 'death', 'dead', 'kill', 'killed',
    }

    SLANG_WORDS = {
        'lol': 'Laughing Out Loud',
        'lmao': 'Laughing My Ass Off',
        'rofl': 'Rolling On Floor Laughing',
        'brb': 'Be Right Back',
        'btw': 'By The Way',
        'idk': 'I Don\'t Know',
        'imo': 'In My Opinion',
        'imho': 'In My Humble Opinion',
        'tbh': 'To Be Honest',
        'ngl': 'Not Gonna Lie',
        'fyi': 'For Your Information',
        'asap': 'As Soon As Possible',
        'atm': 'At The Moment',
        'bbl': 'Be Back Later',
        'bbs': 'Be Back Soon',
        'g2g': 'Got To Go',
        'gtg': 'Got To Go',
        'ttyl': 'Talk To You Later',
        'ttys': 'Talk To You Soon',
        'hbu': 'How About You',
        'wbu': 'What About You',
        'wyd': 'What You Doing',
        'wya': 'Where You At',
        'omw': 'On My Way',
        'nvm': 'Never Mind',
        'ikr': 'I Know Right',
        'ily': 'I Love You',
        'ilu': 'I Love You',
        'ily2': 'I Love You Too',
        'bff': 'Best Friends Forever',
        'bae': 'Before Anyone Else',
        'thot': 'That Ho Over There',
        'fam': 'Family',
        'bro': 'Brother',
        'sis': 'Sister',
        'dude': 'Dude',
        'yo': 'Yo',
        'sup': 'What\'s Up',
        'wassup': 'What\'s Up',
        'wazzup': 'What\'s Up',
        'yo': 'Hey',
        'hey': 'Hello',
        'hi': 'Hello',
        'hola': 'Hello',
        'cya': 'See You',
        'cu': 'See You',
        'gonna': 'Going To',
        'gotta': 'Got To',
        'wanna': 'Want To',
        'kinda': 'Kind Of',
        'sorta': 'Sort Of',
        'lemme': 'Let Me',
        'gimme': 'Give Me',
        'dunno': 'Don\'t Know',
        'cuz': 'Because',
        'cause': 'Because',
        'tho': 'Though',
        'rn': 'Right Now',
        'rn': 'Right Now',
        'fr': 'For Real',
        'frfr': 'For Real For Real',
        'cap': 'Lie',
        'no cap': 'No Lie',
        'bet': 'Okay/Sure',
        'slay': 'Do Well',
        'based': 'Agreeable',
        'cringe': 'Embarrassing',
        'simp': 'Someone Overly Desperate',
        'sus': 'Suspicious',
        'pog': 'Amazing',
        'poggers': 'Amazing',
        'gw': 'Good Work',
        'gl': 'Good Luck',
        'hf': 'Have Fun',
        'gg': 'Good Game',
        'wp': 'Well Played',
        'nt': 'Nice Try',
        'ez': 'Easy',
        'rekt': 'Wrecked',
        'salty': 'Bitter/Upset',
        'triggered': 'Upset/Offended',
        'snowflake': 'Oversensitive Person',
        'karen': 'Entitled Woman',
        'simp': 'Desperate Person',
        'chad': 'Confident Man',
        'stacy': 'Attractive Woman',
        'normie': 'Normal Person',
        'noob': 'New/Inexperienced',
        'pro': 'Professional',
        'hacker': 'Very Skilled',
        'og': 'Original',
        'goat': 'Greatest Of All Time',
        'w': 'Win',
        'l': 'Loss',
        'f': 'Respects/Pay Respects',
        'rip': 'Rest In Peace',
        'fml': 'Fuck My Life',
        'tfl': 'The Fuck',
        'wtf': 'What The Fuck',
        'stfu': 'Shut The Fuck Up',
        'gtfo': 'Get The Fuck Out',
        'af': 'As Fuck',
        'asf': 'As Fuck',
        'mf': 'Motherfucker',
        'tf': 'The Fuck',
        'bs': 'Bullshit',
        'lmfao': 'Laughing My Fucking Ass Off',
    }

    def __init__(self):
        self.word_sentiments: Dict[str, Dict[str, int]] = defaultdict(lambda: {'positive': 0, 'negative': 0, 'neutral': 0})
        self.person_sentiments: Dict[str, Dict[str, int]] = defaultdict(lambda: {'positive': 0, 'negative': 0, 'neutral': 0})
        self.slang_usage: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
        self.total_slang: Dict[str, int] = defaultdict(int)
        self.message_sentiments: List[Dict] = []

    def analyze_messages(self, messages: List[Dict]) -> Dict[str, Any]:
        for msg in messages:
            sender = msg.get('sender', 'Unknown')
            text = msg.get('text', '')
            self._analyze_text(sender, text)

        return self.get_stats()

    def _analyze_text(self, sender: str, text: Any):
        if isinstance(text, list):
            text = ' '.join([t if isinstance(t, str) else t.get('text', '') for t in text])
        
        text_str = str(text).lower()
        words = re.findall(r'\b\w+\b', text_str)

        positive_count = 0
        negative_count = 0
        neutral_count = 0

        for word in words:
            if word in self.POSITIVE_WORDS:
                positive_count += 1
                self.word_sentiments[word]['positive'] += 1
            elif word in self.NEGATIVE_WORDS:
                negative_count += 1
                self.word_sentiments[word]['negative'] += 1
            else:
                neutral_count += 1
                self.word_sentiments[word]['neutral'] += 1

            if word in self.SLANG_WORDS:
                self.slang_usage[sender][word] += 1
                self.total_slang[word] += 1

        self.person_sentiments[sender]['positive'] += positive_count
        self.person_sentiments[sender]['negative'] += negative_count
        self.person_sentiments[sender]['neutral'] += neutral_count

        if positive_count > negative_count:
            sentiment = 'positive'
        elif negative_count > positive_count:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        self.message_sentiments.append({
            'sender': sender,
            'positive': positive_count,
            'negative': negative_count,
            'neutral': neutral_count,
            'sentiment': sentiment,
        })

    def get_stats(self) -> Dict[str, Any]:
        total_positive = sum(s['positive'] for s in self.person_sentiments.values())
        total_negative = sum(s['negative'] for s in self.person_sentiments.values())
        total_neutral = sum(s['neutral'] for s in self.person_sentiments.values())
        total = total_positive + total_negative + total_neutral

        return {
            'overall': {
                'positive': total_positive,
                'negative': total_negative,
                'neutral': total_neutral,
                'positive_ratio': total_positive / total if total else 0,
                'negative_ratio': total_negative / total if total else 0,
            },
            'by_person': dict(self.person_sentiments),
            'top_positive_words': self._get_top_words('positive'),
            'top_negative_words': self._get_top_words('negative'),
            'slang_usage': {
                'total': dict(self.total_slang),
                'by_person': dict(self.slang_usage),
            },
        }

    def _get_top_words(self, sentiment_type: str, limit: int = 10) -> List[Tuple[str, int]]:
        words = [(word, counts[sentiment_type]) for word, counts in self.word_sentiments.items() if counts[sentiment_type] > 0]
        return sorted(words, key=lambda x: x[1], reverse=True)[:limit]

    def get_person_sentiment(self, person: str) -> Dict[str, Any]:
        if person not in self.person_sentiments:
            return {'positive': 0, 'negative': 0, 'neutral': 0}
        
        stats = self.person_sentiments[person]
        total = sum(stats.values())
        
        return {
            'positive': stats['positive'],
            'negative': stats['negative'],
            'neutral': stats['neutral'],
            'positive_ratio': stats['positive'] / total if total else 0,
            'negative_ratio': stats['negative'] / total if total else 0,
        }

    def get_top_slang(self, limit: int = 20) -> List[Tuple[str, int, str]]:
        sorted_slang = sorted(self.total_slang.items(), key=lambda x: x[1], reverse=True)
        return [(word, count, self.SLANG_WORDS.get(word, 'Unknown')) for word, count in sorted_slang[:limit]]

    def get_slang_by_person(self, person: str, limit: int = 10) -> List[Tuple[str, int, str]]:
        if person not in self.slang_usage:
            return []
        
        sorted_slang = sorted(self.slang_usage[person].items(), key=lambda x: x[1], reverse=True)
        return [(word, count, self.SLANG_WORDS.get(word, 'Unknown')) for word, count in sorted_slang[:limit]]

    def reset(self):
        self.word_sentiments = defaultdict(lambda: {'positive': 0, 'negative': 0, 'neutral': 0})
        self.person_sentiments = defaultdict(lambda: {'positive': 0, 'negative': 0, 'neutral': 0})
        self.slang_usage = defaultdict(lambda: defaultdict(int))
        self.total_slang = defaultdict(int)
        self.message_sentiments = []
