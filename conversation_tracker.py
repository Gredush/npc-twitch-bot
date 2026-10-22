from topic_manager import TopicManager


class ConversationTracker:

    def get_current_topic(self):

        manager = TopicManager()

        topic, confidence = manager.detect_topic()

        if confidence < 5:
            return None

        return topic