from typing import List, Optional, Literal
from datetime import datetime

from pydantic import AnyHttpUrl, validator

from schemas import BaseSchema


class ChatMessage(BaseSchema):
    username: str
    text: str


class ChatConfig(BaseSchema):
    server_url: str
    youtube_chat_id: str


class YoutubePageInfo(BaseSchema):
    total_results: int
    results_per_page: int


class YoutubeThumbnail(BaseSchema):
    height: int
    width: int
    url: AnyHttpUrl


class YoutubeThumbnailSet(BaseSchema):
    default: YoutubeThumbnail
    high: YoutubeThumbnail
    maxres: YoutubeThumbnail
    medium: YoutubeThumbnail
    standard: YoutubeThumbnail


class YoutubeBroadcastSnippet(BaseSchema):
    actual_start_time: datetime
    channel_id: str
    description: str
    is_default_broadcast: bool
    live_chat_id: Optional[str] = None
    published_at: datetime
    scheduled_start_time: datetime
    thumbnails: YoutubeThumbnailSet
    title: str


class YoutubeBroadcast(BaseSchema):
    etag: str
    id: str
    kind: str
    snippet: Optional[YoutubeBroadcastSnippet]


class YoutubeChatTextMessageDetails(BaseSchema):
    message_text: str


class YoutubeChatDeletedMessageDetails(BaseSchema):
    deleted_message_id: str


class YoutubeUserDetails(BaseSchema):
    channel_id: str
    channel_url: AnyHttpUrl
    display_name: str
    profile_image_url: AnyHttpUrl


class YoutubeChatUserBannedDetails(BaseSchema):
    banned_user_details: YoutubeUserDetails
    ban_type: str
    ban_duration_seconds: int


class YoutubeChatSuperDetails(BaseSchema):
    amount_micros: int
    currency: str
    amount_display_string: str
    tier: int


class YoutubeChatSuperChat(YoutubeChatSuperDetails):
    user_comment: str


class YoutubeSuperStickerMetadata(BaseSchema):
    sticker_id: str
    alt_text: str
    language: str


class YoutubeSuperStickerDetails(YoutubeChatSuperDetails):
    super_sticker_metadata: YoutubeSuperStickerMetadata


class YoutubeChatMessageSnippet(BaseSchema):
    message_type: Literal[
        "chatEndedEvent",
        "messageDeletedEvent",
        "newSponsorEvent",
        "sponsorOnlyModeEndedEvent",
        "sponsorOnlyModeStartedEvent",
        "superChatEvent",
        "superStickerEvent",
        "textMessageEvent",
        "tombstone",
        "userBannedEvent",
    ] = "textMessageEvent"
    live_chat_id: str
    author_channel_id: str
    published_at: datetime
    has_display_content: bool = False
    display_message: Optional[str]
    text_message_details: Optional[YoutubeChatTextMessageDetails] = None
    message_deleted_details: Optional[YoutubeChatDeletedMessageDetails] = None
    user_banned_details: Optional[YoutubeChatUserBannedDetails] = None
    super_chat_details: Optional[YoutubeChatSuperChat] = None
    super_sticker_details: Optional[YoutubeSuperStickerDetails] = None

    @validator("message_type", pre=True)
    def fill_message_type(cls, v, values):
        if v:
            return v
        if "type" in values:
            return values["type"]
        raise ValueError("Couldn't find a type for the Youtube message snippet")


class YoutubeChatMessageAuthor(BaseSchema):
    channel_id: str
    channel_url: str
    display_name: str
    profile_image_url: AnyHttpUrl
    is_verified: bool = False
    is_chat_owner: bool = False
    is_chat_sponsor: bool = False
    is_chat_moderator: bool = False


class YoutubeChatMessage(BaseSchema):
    etag: str
    id: str
    kind: str
    snippet: Optional[YoutubeChatMessageSnippet] = None
    author_details: Optional[YoutubeChatMessageAuthor] = None


class YoutubeBroadcastResponse(BaseSchema):
    etag: str
    items: List[YoutubeBroadcast]
    kind: str
    page_info: YoutubePageInfo


class YoutubeChatResponse(BaseSchema):
    etag: str
    items: List[YoutubeChatMessage]
    kind: str
    page_info: YoutubePageInfo
    next_page_token: Optional[str] = None
    polling_interval_millis: Optional[int] = None
    offline_at: Optional[datetime]
