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

        if days >= 365:

            return (
                f"re @{username}, xathikes enan xrono 😂"
            )

        if days >= 180:

            return (
                f"@{username} epistrofi meta apo poly kairo 👀"
            )

        if days >= 90:

            return (
                f"@{username} xathikes re 😄"
            )

        if days >= 30:

            return (
                f"kalos ton @{username} 😄"
            )

        return None