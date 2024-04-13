import logging
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from infrastructure.database.models import BotUser
from infrastructure.database.repo.base import BaseRepo


class UserRepo(BaseRepo):
    async def get_or_create_user(
        self,
        chat_id: int,
        name: Optional[str] = None,
        last_name: Optional[str] = None,
        username: Optional[str] = None,
        referral_code: int = None,
        referred_by: int = None,
        referral_count: int = 0,
        referral_link: str = None,
        pref_language: str = "en",
    ):
        """
        Creates or updates a new user in the database and returns the user object.
        :param chat_id: The user's ID.
        :param name: The user's full name.
        :param last_name: The user's language.
        :param username: The user's username. It's an optional parameter.
        :param referral_code: The user's referral code.
        :param referred_by: Chat id of the referrer.
        :param referral_count: Number of user's referral
        :param referral_link: The User's referral link
        :param pref_language: The user's selected language
        :return: User object, None if there was an error while making a transaction.
        """

        insert_stmt = (
            insert(BotUser)
            .values(
                ChatID=chat_id,
                Name=username,
                Lastname=name,
                Username=last_name,
                ReferralCode=referral_code,
                ReferredBy=referred_by,
                ReferralCount=referral_count,
                ReferralLink=referral_link,
                PrefLanguage=pref_language,
            )
            .on_conflict_do_update(
                index_elements=[BotUser.ChatID],
                set_=dict(
                    ChatID=chat_id,
                    Name=username,
                    Lastname=name,
                    Username=last_name,
                    ReferralCode=referral_code,
                    ReferredBy=referred_by,
                    ReferralCount=referral_count,
                    ReferralLink=referral_link,
                    PrefLanguage=pref_language,
                ),
            )
            .returning(BotUser)
        )
        result = await self.session.execute(insert_stmt)

        await self.session.commit()
        return result.scalar_one()

    async def check_user_exists(self, chat_id: int) -> bool:
        """
        Checks if a user exists in the database by chat_id.
        :param chat_id: The user's ID to check.
        :return: True if user exists, otherwise False.
        """
        query = select(BotUser).where(BotUser.ChatID == chat_id)
        result = await self.session.execute(query)
        user = result.scalar_one_or_none()
        return user is not None

    async def update_referrer_data(self, referrer_chat_id: int):
        try:
            # Start a transaction explicitly to handle multistep operations safely
            async with self.session.begin():
                stmt = (
                    update(BotUser)
                    .values(ReferralCount=BotUser.ReferralCount + 1)
                    .where(BotUser.ChatID == referrer_chat_id)
                )
                result = await self.session.execute(stmt)

                # Check if the update has affected any rows
                if result.rowcount == 0:
                    logging.warning(
                        f"No referrer found with ChatID {referrer_chat_id} to update."
                    )
                    return  # Early exit if no rows are updated

                # Refresh the referrer instance to reflect updated values
                referrer = await self.session.get(BotUser, referrer_chat_id)
                if referrer:
                    await self.session.refresh(referrer)
                    logging.info(
                        f"Referrer data updated for ChatID {referrer_chat_id}. "
                        f"Referral count is now {referrer.ReferralCount}."
                    )

        except Exception as e:
            logging.error(
                f"Failed to update referrer data for ChatID {referrer_chat_id}: {e}"
            )
            raise  # Optionally re-raise the exception to signal the error to caller functions

    async def update_user_referrer(self, chat_id: int, referrer_chat_id: int):
        try:
            stmt = (
                update(BotUser)
                .values(ReferredBy=referrer_chat_id)
                .where(BotUser.ChatID == chat_id)
            )
            result = await self.session.execute(stmt)
            if result.rowcount:
                logging.info(
                    f"Updated referrer for user {chat_id} to {referrer_chat_id}"
                )
            else:
                logging.warning(
                    f"No user found with ChatID {chat_id} to update referrer."
                )

            await self.session.commit()
        except Exception as e:
            logging.error(f"Failed to update referrer for user {chat_id}: {e}")
            await self.session.rollback()  # Roll back in case of an error
            raise
