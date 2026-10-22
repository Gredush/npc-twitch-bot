from relationship_manager import (
    RelationshipManager
)


class ReturningViewer:

    def should_welcome_back(
        self,
        username
    ):

        days = (
            RelationshipManager()
            .returning_viewer_days(
                username
            )
        )

        return days >= 30

    def welcome_message(
        self,
        username
    ):

        days = (
            RelationshipManager()
            .returning_viewer_days(
                username
            )
        )

        if days >= 180:
            return (
                "xathikes arketa 😄"
            )

        if days >= 90:
            return (
                "epistrofi meta apo poly kairo 👀"
            )

        if days >= 30:
            return (
                "kalos ton 😄"
            )

        return None